"""RAW -> BRONZE. Parse every raw capture into the canonical record schema (05_DATA_SCHEMA.md).

Bronze keeps one row per (platform, source_id, raw capture) occurrence — duplicates across captures are kept
here and resolved in dedup. Raw text is never modified; text_clean is derived.
"""
from __future__ import annotations

import html as htmlmod
import json
import re
from datetime import datetime, timezone

import pandas as pd
from bs4 import BeautifulSoup

from src.utils.common import ROOT, author_hash, iter_raw, sha256

BRONZE = ROOT / "data" / "bronze"


def ts(v):
    if v is None or v == "":
        return None
    try:
        if isinstance(v, (int, float)) or (isinstance(v, str) and v.isdigit()):
            return datetime.fromtimestamp(int(v), timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
        return pd.Timestamp(v).tz_convert("UTC").strftime("%Y-%m-%dT%H:%M:%SZ") if pd.Timestamp(v).tzinfo \
            else pd.Timestamp(v).strftime("%Y-%m-%dT%H:%M:%SZ")
    except Exception:
        return None


def html_to_text(s: str | None) -> str:
    if not s:
        return ""
    if "<" not in s and "&" not in s:
        return s
    soup = BeautifulSoup(s, "lxml")
    for br in soup.find_all(["br", "p", "li"]):
        br.append("\n")
    return htmlmod.unescape(soup.get_text())


def rec(**kw):
    base = dict(record_id=None, source_family=None, platform=None, source_type=None, record_type=None,
                source_url=None, source_id=None, parent_id=None, thread_id=None, thread_title=None,
                community=None, query_id=None, collection_run_id=None, created_at=None, collected_at=None,
                text_raw=None, text_is_html=False, author_id_hash=None, author_public_profile_location=None,
                platform_language=None, likes=None, replies=None, shares=None, views=None, rating=None,
                is_reply=False, is_repost=False, is_quote=False, access_method=None, raw_capture_path=None,
                extra=None)
    base.update(kw)
    base["record_id"] = f"{base['platform']}:{base['source_id']}"
    if isinstance(base["extra"], (dict, list)):
        base["extra"] = json.dumps(base["extra"], ensure_ascii=False)[:2000]
    return base


def common(meta, path):
    return dict(query_id=meta.get("query_id"), collection_run_id=meta.get("run_id"),
                collected_at=meta.get("captured_at"), raw_capture_path=path,
                access_method=meta.get("access_method"))


# ------------------------------------------------------------------ reddit
def _reddit_comments(nodes, out, link_id, title, sub, c, depth=0):
    for n in nodes or []:
        if not isinstance(n, dict):
            continue
        kind = n.get("kind")
        d = n.get("data", n)
        if kind == "more" or d.get("body") is None:
            continue
        out.append(rec(source_family="reddit", platform="reddit", source_type="reddit_comment",
                       record_type="comment_record",
                       source_url=f"https://www.reddit.com/r/{sub or d.get('subreddit')}/comments/{link_id}/_/{d['id']}/",
                       source_id=f"t1_{d['id']}", parent_id=d.get("parent_id"), thread_id=f"t3_{link_id}",
                       thread_title=title, community=sub, created_at=ts(d.get("created_utc")),
                       text_raw=d.get("body"), author_id_hash=author_hash("reddit", d.get("author")),
                       likes=d.get("score"), is_reply=not str(d.get("parent_id", "")).startswith("t3_"),
                       extra={"depth": depth}, **c))
        rep = d.get("replies")
        if isinstance(rep, dict):
            rep = rep.get("data", {}).get("children")
        _reddit_comments(rep, out, link_id, title, sub, c, depth + 1)


def parse_reddit():
    out, titles = [], {}
    for path, meta, pl in iter_raw("reddit"):
        c = common(meta, path)
        if meta.get("stage") in ("posts_full", "posts_keyword"):
            for d in pl.get("data") or []:
                titles[d["id"]] = d.get("title")
                body = d.get("selftext") or ""
                if body in ("[removed]", "[deleted]"):
                    body = ""
                out.append(rec(source_family="reddit", platform="reddit", source_type="reddit_submission",
                               record_type="post_record",
                               source_url=f"https://www.reddit.com{d.get('permalink', '')}",
                               source_id=f"t3_{d['id']}", thread_id=f"t3_{d['id']}", thread_title=d.get("title"),
                               community=d.get("subreddit"), created_at=ts(d.get("created_utc")),
                               text_raw=(d.get("title") or "") + ("\n\n" + body if body else ""),
                               author_id_hash=author_hash("reddit", d.get("author")), likes=d.get("score"),
                               replies=d.get("num_comments"), is_repost=bool(d.get("crosspost_parent")),
                               extra={"flair": d.get("link_flair_text"), "over_18": d.get("over_18"),
                                      "crosspost_parent": d.get("crosspost_parent"), "url": d.get("url")}, **c))
    for path, meta, pl in iter_raw("reddit"):
        if meta.get("stage") == "comments_tree":
            pid = meta["post_id"]
            _reddit_comments(pl.get("data"), out, pid, titles.get(pid), meta.get("subreddit"), common(meta, path))
    return out


# ------------------------------------------------------------------ bluesky
def _bsky_post(p, c, root_uri=None, thread_title=None):
    r = p.get("record", {})
    uri = p["uri"]
    handle = p.get("author", {}).get("handle")
    reply = r.get("reply") or {}
    return rec(source_family="bluesky", platform="bluesky", source_type="bluesky_post",
               record_type="comment_record" if reply else "post_record",
               source_url=f"https://bsky.app/profile/{p.get('author', {}).get('did')}/post/{uri.split('/')[-1]}",
               source_id=uri, parent_id=(reply.get("parent") or {}).get("uri"),
               thread_id=(reply.get("root") or {}).get("uri") or root_uri or uri, thread_title=thread_title,
               created_at=ts(r.get("createdAt")), text_raw=r.get("text"),
               author_id_hash=author_hash("bluesky", p.get("author", {}).get("did")),
               platform_language=",".join(r.get("langs") or []) or None, likes=p.get("likeCount"),
               replies=p.get("replyCount"), shares=p.get("repostCount"), is_reply=bool(reply),
               is_quote=bool((r.get("embed") or {}).get("$type", "").startswith("app.bsky.embed.record")),
               extra={"quoteCount": p.get("quoteCount")}, **c)


def parse_bluesky():
    out = []
    for path, meta, pl in iter_raw("bluesky"):
        c = common(meta, path)
        if meta.get("stage") == "search":
            for p in pl.get("posts") or []:
                out.append(_bsky_post(p, c))
        elif meta.get("stage") == "thread":
            root = pl.get("thread", {})
            if "post" not in root:
                continue
            title = (root["post"].get("record") or {}).get("text", "")[:200]
            stack = list(root.get("replies") or [])
            while stack:
                n = stack.pop()
                if isinstance(n, dict) and "post" in n:
                    out.append(_bsky_post(n["post"], c, root_uri=root["post"]["uri"], thread_title=title))
                    stack.extend(n.get("replies") or [])
    return out


# ------------------------------------------------------------------ mastodon
def parse_mastodon():
    out = []
    for path, meta, pl in iter_raw("mastodon"):
        c = common(meta, path)
        for s in pl or []:
            if s.get("reblog"):
                s = s["reblog"]
            acct = s.get("account", {})
            out.append(rec(source_family="mastodon", platform="mastodon", source_type="mastodon_status",
                           record_type="comment_record" if s.get("in_reply_to_id") else "post_record",
                           source_url=s.get("url") or s.get("uri"), source_id=s.get("uri"),
                           parent_id=s.get("in_reply_to_id"), thread_id=s.get("uri"),
                           created_at=ts(s.get("created_at")), text_raw=s.get("content"), text_is_html=True,
                           author_id_hash=author_hash("mastodon", acct.get("url")),
                           platform_language=s.get("language"), likes=s.get("favourites_count"),
                           replies=s.get("replies_count"), shares=s.get("reblogs_count"),
                           is_reply=bool(s.get("in_reply_to_id")),
                           extra={"instance_seen": meta.get("instance"), "tags": [t["name"] for t in s.get("tags", [])]},
                           **c))
    return out


# ------------------------------------------------------------------ lemmy
def parse_lemmy():
    out = []
    for path, meta, pl in iter_raw("lemmy"):
        c = common(meta, path)
        for v in pl.get("posts") or []:
            p = v["post"]
            if p.get("removed") or p.get("deleted"):
                continue
            out.append(rec(source_family="lemmy", platform="lemmy", source_type="lemmy_post",
                           record_type="post_record", source_url=p.get("ap_id"), source_id=p.get("ap_id"),
                           thread_id=p.get("ap_id"), thread_title=p.get("name"),
                           community=v.get("community", {}).get("name"), created_at=ts(p.get("published")),
                           text_raw=(p.get("name") or "") + ("\n\n" + p["body"] if p.get("body") else ""),
                           author_id_hash=author_hash("lemmy", v.get("creator", {}).get("actor_id")),
                           likes=v.get("counts", {}).get("score"), replies=v.get("counts", {}).get("comments"),
                           extra={"nsfw": p.get("nsfw")}, **c))
        for v in pl.get("comments") or []:
            cm = v["comment"]
            if cm.get("removed") or cm.get("deleted"):
                continue
            out.append(rec(source_family="lemmy", platform="lemmy", source_type="lemmy_comment",
                           record_type="comment_record", source_url=cm.get("ap_id"), source_id=cm.get("ap_id"),
                           parent_id=cm.get("path"), thread_id=f"lemmy_post:{v['post'].get('ap_id')}",
                           thread_title=v["post"].get("name"), community=v.get("community", {}).get("name"),
                           created_at=ts(cm.get("published")), text_raw=cm.get("content"),
                           author_id_hash=author_hash("lemmy", v.get("creator", {}).get("actor_id")),
                           likes=v.get("counts", {}).get("score"), replies=v.get("counts", {}).get("child_count"),
                           is_reply=cm.get("path", "0.x").count(".") > 1, **c))
    return out


# ------------------------------------------------------------------ hacker news
def parse_hackernews():
    out = []
    for path, meta, pl in iter_raw("hackernews"):
        c = common(meta, path)
        for h in pl.get("hits") or []:
            is_story = "story" in (h.get("_tags") or []) and not h.get("comment_text")
            text = (h.get("title") or "") + ("\n\n" + h["story_text"] if h.get("story_text") else "") \
                if is_story else h.get("comment_text")
            out.append(rec(source_family="hackernews", platform="hackernews",
                           source_type="hn_story" if is_story else "hn_comment",
                           record_type="post_record" if is_story else "comment_record",
                           source_url=f"https://news.ycombinator.com/item?id={h['objectID']}",
                           source_id=h["objectID"], parent_id=h.get("parent_id"),
                           thread_id=f"hn_{h.get('story_id') or h['objectID']}",
                           thread_title=h.get("story_title") or h.get("title"), created_at=ts(h.get("created_at_i")),
                           text_raw=text, text_is_html=True, author_id_hash=author_hash("hackernews", h.get("author")),
                           likes=h.get("points"), replies=h.get("num_comments"), is_reply=not is_story, **c))
    return out


# ------------------------------------------------------------------ stack exchange
def parse_stackexchange():
    out, qtitle = [], {}
    raws = list(iter_raw("stackexchange"))
    for path, meta, pl in raws:
        if meta.get("stage") == "questions":
            for q in pl.get("items") or []:
                qtitle[q["question_id"]] = q.get("title")
    for path, meta, pl in raws:
        c = common(meta, path)
        st = meta.get("stage")
        for it in pl.get("items") or []:
            own = (it.get("owner") or {})
            if st == "questions":
                out.append(rec(source_family="stackexchange", platform="stackexchange", source_type="se_question",
                               record_type="post_record", source_url=it.get("link"),
                               source_id=f"q{it['question_id']}", thread_id=f"se_q{it['question_id']}",
                               thread_title=it.get("title"), community="gardening",
                               created_at=ts(it.get("creation_date")),
                               text_raw=f"<p>{htmlmod.escape(it.get('title', ''))}</p>" + (it.get("body") or ""),
                               text_is_html=True, author_id_hash=author_hash("se", own.get("user_id")),
                               likes=it.get("score"), replies=it.get("answer_count"), views=it.get("view_count"),
                               extra={"tags": it.get("tags")}, **c))
            elif st == "answers":
                out.append(rec(source_family="stackexchange", platform="stackexchange", source_type="se_answer",
                               record_type="comment_record",
                               source_url=f"https://gardening.stackexchange.com/a/{it['answer_id']}",
                               source_id=f"a{it['answer_id']}", parent_id=f"q{it['question_id']}",
                               thread_id=f"se_q{it['question_id']}", thread_title=qtitle.get(it["question_id"]),
                               community="gardening", created_at=ts(it.get("creation_date")),
                               text_raw=it.get("body"), text_is_html=True,
                               author_id_hash=author_hash("se", own.get("user_id")), likes=it.get("score"),
                               is_reply=True, extra={"accepted": it.get("is_accepted")}, **c))
            elif st == "comments":
                out.append(rec(source_family="stackexchange", platform="stackexchange", source_type="se_comment",
                               record_type="comment_record",
                               source_url=f"https://gardening.stackexchange.com/posts/comments/{it['comment_id']}",
                               source_id=f"c{it['comment_id']}", parent_id=str(it.get("post_id")),
                               thread_id=f"se_post{it.get('post_id')}", community="gardening",
                               created_at=ts(it.get("creation_date")), text_raw=it.get("body"), text_is_html=True,
                               author_id_hash=author_hash("se", own.get("user_id")), likes=it.get("score"),
                               is_reply=True, **c))
    return out


# ------------------------------------------------------------------ forums (gardenweb)
def parse_forums():
    out = []
    for path, meta, store in iter_raw("forums"):
        c = common(meta, path)
        tid = str(meta.get("thread_id"))
        q = (store.get("data") or {}).get(tid) or {}
        if not q:
            continue
        title = q.get("title")
        out.append(rec(source_family="forums", platform="gardenweb", source_type="forum_thread_start",
                       record_type="post_record", source_url=meta.get("url"), source_id=f"gw_q{tid}",
                       thread_id=f"gw_{tid}", thread_title=title, community="gardenweb_hydroponics",
                       created_at=ts(q.get("created")),
                       text_raw=f"<p>{htmlmod.escape(title or '')}</p>" + (q.get("htmlBody") or ""),
                       text_is_html=True, author_id_hash=author_hash("gardenweb", q.get("userId")),
                       likes=q.get("numberOfLikes"), replies=q.get("numberOfAnswers"),
                       extra={"tags": [t.get("label") for t in q.get("tags") or []]}, **c))
        for aid, a in (q.get("answerObjectsMap") or {}).items():
            body = a.get("htmlBody")
            if not body:
                continue
            out.append(rec(source_family="forums", platform="gardenweb", source_type="forum_reply",
                           record_type="comment_record", source_url=f"{meta.get('url')}#n={aid}",
                           source_id=f"gw_a{aid}", parent_id=f"gw_q{tid}", thread_id=f"gw_{tid}",
                           thread_title=title, community="gardenweb_hydroponics", created_at=ts(a.get("created")),
                           text_raw=body, text_is_html=True, author_id_hash=author_hash("gardenweb", a.get("userId")),
                           likes=a.get("numberOfLikes"), is_reply=True, **c))
    return out


def parse_youtube():
    out = []
    for path, meta, pl in iter_raw("youtube"):
        if meta.get("stage") != "comment_threads":
            continue
        c = common(meta, path)
        vid, title = meta.get("video_id"), meta.get("video_title")
        for th in pl.get("items") or []:
            top = th["snippet"]["topLevelComment"]
            items = [(top, False)] + [(r, True) for r in (th.get("replies") or {}).get("comments", [])]
            for cm, is_rep in items:
                sn = cm["snippet"]
                out.append(rec(source_family="youtube", platform="youtube", source_type="youtube_comment",
                               record_type="comment_record",
                               source_url=f"https://www.youtube.com/watch?v={vid}&lc={cm['id']}",
                               source_id=cm["id"], parent_id=sn.get("parentId") or vid, thread_id=f"yt_{vid}",
                               thread_title=title, community=None, created_at=ts(sn.get("publishedAt")),
                               text_raw=sn.get("textOriginal") or sn.get("textDisplay"),
                               author_id_hash=author_hash("youtube", (sn.get("authorChannelId") or {}).get("value")),
                               likes=sn.get("likeCount"), replies=th["snippet"].get("totalReplyCount") if not is_rep else None,
                               is_reply=is_rep, **c))
    return out


PARSERS = {"youtube": parse_youtube, "reddit": parse_reddit, "bluesky": parse_bluesky, "mastodon": parse_mastodon, "lemmy": parse_lemmy,
           "hackernews": parse_hackernews, "stackexchange": parse_stackexchange, "forums": parse_forums}


def main():
    BRONZE.mkdir(parents=True, exist_ok=True)
    frames = []
    for name, fn in PARSERS.items():
        try:
            rows = fn()
        except Exception as e:
            print(f"  ! parser {name} failed: {e!r}")
            continue
        df = pd.DataFrame(rows)
        if df.empty:
            print(f"  {name}: 0")
            continue
        df["text_raw"] = df["text_raw"].fillna("").astype(str)
        for col in ("source_id", "parent_id", "thread_id", "thread_title", "community", "platform_language",
                    "query_id", "author_id_hash", "source_url"):
            df[col] = df[col].map(lambda v: None if v is None or (isinstance(v, float) and v != v) else str(v))
        df["text_raw_sha256"] = df["text_raw"].map(sha256)
        df["provenance_hash"] = (df["record_id"] + "|" + df["raw_capture_path"] + "|" + df["text_raw_sha256"]).map(sha256)
        df.to_parquet(BRONZE / f"{name}.parquet", index=False)
        print(f"  {name}: {len(df)} bronze rows, {df.record_id.nunique()} unique ids")
        frames.append(df)
    allf = pd.concat(frames, ignore_index=True)
    for col in ("likes", "replies", "shares", "views", "rating"):
        allf[col] = pd.to_numeric(allf[col], errors="coerce")
    allf.to_parquet(BRONZE / "all_bronze.parquet", index=False)
    print("TOTAL bronze", len(allf), "unique", allf.record_id.nunique())


if __name__ == "__main__":
    main()
