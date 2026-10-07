"""Collectors for open public APIs: Bluesky, Mastodon, Lemmy, Hacker News (Algolia), Stack Exchange.

Each source runs in isolation; one failing source never stops the others. All requests are logged in the
request ledger; all payloads are saved as immutable raw captures.
"""
from __future__ import annotations

import argparse
import traceback
from datetime import datetime, timezone

from src.utils.common import (SOURCES, Checkpoint, Http, iter_raw, load_yaml, log_run, new_run_id, save_raw,
                              utcnow)

Q = load_yaml("queries.yaml")


def all_terms():
    out = []
    for cname, c in Q["clusters"].items():
        for lang in ("id", "en"):
            for i, t in enumerate(c.get(f"{lang}_terms") or []):
                out.append((f"{cname[:1]}_{lang}_{i:02d}", t, lang))
    return out


# ------------------------------------------------------------------ Bluesky
def bluesky(run_id):
    cfg = SOURCES["sources"]["bluesky"]
    http = Http("bluesky", cfg["min_interval_s"])
    ck = Checkpoint("bluesky")
    n_req = n_obj = 0
    for qid, term, lang in all_terms():
        key = f"q:{qid}:{term}"
        if ck.done(key):
            continue
        cursor, got = None, 0
        for page in range(cfg["max_pages_per_query"]):
            params = {"q": term, "limit": 100, "sort": "latest"}
            if cursor:
                params["cursor"] = cursor
            st, code, pl = http.get(f"{cfg['base_url']}/app.bsky.feed.searchPosts", params, "searchPosts",
                                    f"BS_{qid}", page)
            n_req += 1
            if st != "SUCCESS":
                print(f"  ! bluesky {term} {st} {code}")
                break
            posts = pl.get("posts") or []
            if posts:
                save_raw("bluesky", run_id, f"search_{qid}_{page}", pl,
                         {"endpoint": "app.bsky.feed.searchPosts", "params": params, "query_id": f"BS_{qid}",
                          "query_text": term, "query_lang": lang, "stage": "search",
                          "access_method": "bluesky_public_appview"})
            got += len(posts)
            cursor = pl.get("cursor")
            if not cursor or not posts:
                break
        n_obj += got
        ck.mark(key, got)
        print(f"  bluesky [{term}] {got}")
    # reply threads for posts with replies (conversation comments)
    seen, cands = set(), []
    for path, meta, pl in iter_raw("bluesky"):
        if meta.get("stage") != "search":
            continue
        for p in pl.get("posts") or []:
            if p["uri"] in seen:
                continue
            seen.add(p["uri"])
            if (p.get("replyCount") or 0) >= 2 and not p["record"].get("reply"):
                cands.append((p.get("replyCount", 0), p["uri"], meta.get("query_id")))
    cands.sort(reverse=True)
    for rc, uri, qid in cands[:400]:
        key = f"thread:{uri}"
        if ck.done(key):
            continue
        st, code, pl = http.get(f"{cfg['base_url']}/app.bsky.feed.getPostThread", {"uri": uri, "depth": 6},
                                "getPostThread", qid, uri)
        n_req += 1
        if st == "SUCCESS":
            save_raw("bluesky", run_id, f"thread_{uri.split('/')[-1]}", pl,
                     {"endpoint": "app.bsky.feed.getPostThread", "query_id": qid, "stage": "thread",
                      "root_uri": uri, "access_method": "bluesky_public_appview"})
            n_obj += rc
        ck.mark(key, st)
    return n_req, n_obj


# ------------------------------------------------------------------ Mastodon
def mastodon(run_id):
    cfg = SOURCES["sources"]["mastodon"]
    http = Http("mastodon", cfg["min_interval_s"])
    ck = Checkpoint("mastodon")
    n_req = n_obj = 0
    for inst in cfg["instances"]:
        for tag in cfg["hashtags"]:
            key = f"{inst}:{tag}"
            if ck.done(key):
                continue
            max_id, got = None, 0
            for page in range(cfg["max_pages_per_tag"]):
                params = {"limit": 40}
                if max_id:
                    params["max_id"] = max_id
                st, code, pl = http.get(f"https://{inst}/api/v1/timelines/tag/{tag}", params, "tag_timeline",
                                        f"MA_{tag}", page)
                n_req += 1
                if st != "SUCCESS" or not pl:
                    break
                save_raw("mastodon", run_id, f"{inst}_{tag}_{page}", pl,
                         {"endpoint": "timelines/tag", "instance": inst, "params": params, "query_id": f"MA_{tag}",
                          "query_text": f"#{tag}", "stage": "tag", "access_method": "mastodon_public_api"})
                got += len(pl)
                max_id = pl[-1]["id"]
                if len(pl) < 40:
                    break
            n_obj += got
            ck.mark(key, got)
            print(f"  mastodon {inst} #{tag} {got}")
    return n_req, n_obj


# ------------------------------------------------------------------ Lemmy
def lemmy(run_id):
    cfg = SOURCES["sources"]["lemmy"]
    http = Http("lemmy", cfg["min_interval_s"])
    ck = Checkpoint("lemmy")
    n_req = n_obj = 0
    terms = ["hydroponic", "hydroponics", "hidroponik", "kratky", "aerogarden", "click and grow", "rockwool",
             "nutrient solution", "grow tent lettuce", "indoor garden"]
    for inst in cfg["instances"]:
        for term in terms:
            for typ in ("Posts", "Comments"):
                key = f"{inst}:{term}:{typ}"
                if ck.done(key):
                    continue
                got = 0
                for page in range(1, 21):
                    params = {"q": term, "type_": typ, "listing_type": "All", "limit": 50, "page": page,
                              "sort": "New"}
                    st, code, pl = http.get(f"https://{inst}/api/v3/search", params, "search",
                                            f"LE_{term}", page)
                    n_req += 1
                    if st != "SUCCESS":
                        break
                    items = pl.get(typ.lower()) or []
                    if not items:
                        break
                    save_raw("lemmy", run_id, f"{inst}_{term}_{typ}_{page}", pl,
                             {"endpoint": "api/v3/search", "instance": inst, "params": params,
                              "query_id": f"LE_{term}", "query_text": term, "stage": typ.lower(),
                              "access_method": "lemmy_public_api"})
                    got += len(items)
                    if len(items) < 50:
                        break
                n_obj += got
                ck.mark(key, got)
                print(f"  lemmy {inst} {term} {typ} {got}")
    return n_req, n_obj


# ------------------------------------------------------------------ Hacker News
def hackernews(run_id):
    cfg = SOURCES["sources"]["hackernews"]
    http = Http("hackernews", cfg["min_interval_s"])
    ck = Checkpoint("hackernews")
    n_req = n_obj = 0
    terms = ["hydroponic", "hydroponics", "aerogarden", "kratky", "click and grow", "aeroponic",
             "smart garden", "indoor garden lettuce", "vertical farming"]
    years = range(2007, datetime.now(timezone.utc).year + 1)
    for term in terms:
        for tag in ("comment", "story"):
            for y in years:
                key = f"{term}:{tag}:{y}"
                if ck.done(key):
                    continue
                a = int(datetime(y, 1, 1, tzinfo=timezone.utc).timestamp())
                b = int(datetime(y + 1, 1, 1, tzinfo=timezone.utc).timestamp())
                got = 0
                for page in range(0, 5):
                    params = {"query": term, "tags": tag, "hitsPerPage": 200, "page": page,
                              "numericFilters": f"created_at_i>={a},created_at_i<{b}"}
                    st, code, pl = http.get("https://hn.algolia.com/api/v1/search", params, "search",
                                            f"HN_{term}", f"{y}-{page}")
                    n_req += 1
                    if st != "SUCCESS":
                        break
                    hits = pl.get("hits") or []
                    if hits:
                        save_raw("hackernews", run_id, f"{term}_{tag}_{y}_{page}", pl,
                                 {"endpoint": "algolia/search", "params": params, "query_id": f"HN_{term}",
                                  "query_text": term, "stage": tag, "access_method": "hn_algolia_api"})
                    got += len(hits)
                    if page + 1 >= (pl.get("nbPages") or 0):
                        break
                n_obj += got
                ck.mark(key, got)
        print(f"  hn {term} done")
    return n_req, n_obj


# ------------------------------------------------------------------ Stack Exchange
def stackexchange(run_id):
    http = Http("stackexchange", SOURCES["sources"]["stackexchange"]["min_interval_s"])
    ck = Checkpoint("stackexchange")
    base = "https://api.stackexchange.com/2.3"
    n_req = n_obj = 0
    qids = set()
    searches = [("tagged", {"tagged": "hydroponic"}), ("q_hydroponic", {"q": "hydroponic"}),
                ("q_hydroponics", {"q": "hydroponics"}), ("q_kratky", {"q": "kratky"}),
                ("q_aerogarden", {"q": "aerogarden"}), ("q_rockwool", {"q": "rockwool"}),
                ("q_nutrient_solution", {"q": "nutrient solution"})]
    for name, extra in searches:
        for page in range(1, 11):
            key = f"search:{name}:{page}"
            params = {"site": "gardening", "pagesize": 100, "page": page, "filter": "withbody",
                      "order": "desc", "sort": "creation"} | extra
            st, code, pl = http.get(f"{base}/search/advanced", params, "search_advanced", f"SE_{name}", page)
            n_req += 1
            if st != "SUCCESS":
                break
            items = pl.get("items") or []
            if items and not ck.done(key):
                save_raw("stackexchange", run_id, f"questions_{name}_{page}", pl,
                         {"endpoint": "search/advanced", "params": params, "query_id": f"SE_{name}",
                          "stage": "questions", "access_method": "stackexchange_api"})
                ck.mark(key, len(items))
            qids.update(i["question_id"] for i in items)
            n_obj += len(items)
            if not pl.get("has_more"):
                break
    qids = sorted(qids)
    for i in range(0, len(qids), 100):
        chunk = ";".join(map(str, qids[i:i + 100]))
        for kind in ("answers", "comments"):
            for page in range(1, 6):
                key = f"{kind}:{i}:{page}"
                if ck.done(key):
                    continue
                params = {"site": "gardening", "pagesize": 100, "page": page, "filter": "withbody"}
                st, code, pl = http.get(f"{base}/questions/{chunk}/{kind}", params, kind, "SE_children", page)
                n_req += 1
                if st != "SUCCESS":
                    break
                items = pl.get("items") or []
                if items:
                    save_raw("stackexchange", run_id, f"{kind}_{i}_{page}", pl,
                             {"endpoint": f"questions/{{ids}}/{kind}", "params": params, "query_id": "SE_children",
                              "stage": kind, "access_method": "stackexchange_api"})
                n_obj += len(items)
                ck.mark(key, len(items))
                if not pl.get("has_more"):
                    break
    # comments on answers
    aids = set()
    for _, meta, pl in iter_raw("stackexchange"):
        if meta.get("stage") == "answers":
            aids.update(a["answer_id"] for a in pl.get("items") or [])
    aids = sorted(aids)
    for i in range(0, len(aids), 100):
        key = f"answer_comments:{i}"
        if ck.done(key):
            continue
        chunk = ";".join(map(str, aids[i:i + 100]))
        st, code, pl = http.get(f"{base}/answers/{chunk}/comments",
                                {"site": "gardening", "pagesize": 100, "filter": "withbody"}, "answer_comments",
                                "SE_children", i)
        n_req += 1
        if st == "SUCCESS" and pl.get("items"):
            save_raw("stackexchange", run_id, f"answer_comments_{i}", pl,
                     {"endpoint": "answers/{ids}/comments", "query_id": "SE_children", "stage": "comments",
                      "access_method": "stackexchange_api"})
            n_obj += len(pl["items"])
        ck.mark(key, st)
    return n_req, n_obj


SOURCES_FN = {"bluesky": bluesky, "mastodon": mastodon, "lemmy": lemmy, "hackernews": hackernews,
              "stackexchange": stackexchange}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--sources", default=",".join(SOURCES_FN))
    a = ap.parse_args()
    for s in a.sources.split(","):
        run_id = new_run_id(s)
        started = utcnow()
        print(f"=== {s}")
        try:
            req, obj = SOURCES_FN[s](run_id)
            log_run(run_id=run_id, source=s, started_at=started, ended_at=utcnow(), status="SUCCESS",
                    requests=req, objects=obj)
            print(f"=== {s} SUCCESS req={req} obj={obj}")
        except Exception as e:  # source-level isolation
            traceback.print_exc()
            log_run(run_id=run_id, source=s, started_at=started, ended_at=utcnow(), status="FAILED",
                    note=repr(e)[:300])


if __name__ == "__main__":
    main()
