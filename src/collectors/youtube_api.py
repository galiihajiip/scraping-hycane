"""YouTube Data API v3 collector (official API only; requires YOUTUBE_API_KEY).

Quota model (default 10,000 units/day): search.list = 100 units, videos.list = 1, commentThreads.list = 1,
comments.list = 1. The collector tracks units spent in the checkpoint and stops at the configured budget.
Stages: search (Indonesian-first query set) -> video metadata -> comment threads (capped per video) ->
reply expansion for threads whose replies were truncated.
"""
from __future__ import annotations

import argparse
import os
import random

from src.utils.common import Checkpoint, Http, env_present, load_yaml, log_run, new_run_id, save_raw, utcnow

API = "https://www.googleapis.com/youtube/v3"
Q = load_yaml("queries.yaml")


def queries():
    out = []
    for cname, c in Q["clusters"].items():
        for i, t in enumerate(c.get("id_terms") or []):
            out.append((f"YT_{cname[:1]}_id_{i:02d}", t, "id", "ID"))
        for i, t in enumerate((c.get("en_terms") or [])[:1]):
            out.append((f"YT_{cname[:1]}_en_{i:02d}", t, "en", None))
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--budget", type=int, default=9500)
    ap.add_argument("--max-videos", type=int, default=600)
    ap.add_argument("--comments-per-video", type=int, default=300)
    ap.add_argument("--test", action="store_true")
    a = ap.parse_args()
    if not env_present("YOUTUBE_API_KEY"):
        print("youtube: NOT_CONFIGURED (YOUTUBE_API_KEY missing)")
        log_run(run_id=new_run_id("youtube"), source="youtube", started_at=utcnow(), ended_at=utcnow(),
                status="NOT_CONFIGURED", note="YOUTUBE_API_KEY missing")
        return
    key = os.environ["YOUTUBE_API_KEY"]
    http = Http("youtube_api", 0.2)
    ck = Checkpoint("youtube")
    from datetime import datetime
    from zoneinfo import ZoneInfo
    day = datetime.now(ZoneInfo("America/Los_Angeles")).strftime("%Y-%m-%d")  # YouTube quota resets at PT midnight
    units = ck.state.get("units_by_day", {}).get(day, 0)
    run_id, started = new_run_id("youtube"), utcnow()

    def call(ep, params, cost, qid, page):
        nonlocal units
        if units + cost > a.budget:
            return "EXHAUSTED", None
        st, code, pl = http.get(f"{API}/{ep}", params | {"key": key}, ep, qid, page)
        units += cost
        ck.state.setdefault("units_by_day", {})[day] = units
        ck.save()
        if code == 403 and pl is None:
            return "BLOCKED", None
        return st, pl

    if a.test:
        st, pl = call("videos", {"part": "id", "id": "dQw4w9WgXcQ"}, 1, "TEST", 0)
        print("youtube test:", st)
        return
    # ---- search
    videos = dict(ck.state.get("videos", {}))
    for qid, term, lang, region in queries():
        key_ = f"search:{qid}"
        if ck.done(key_):
            continue
        params = {"part": "snippet", "q": term, "type": "video", "maxResults": 50, "order": "relevance",
                  "relevanceLanguage": lang}
        if region:
            params["regionCode"] = region
        st, pl = call("search", params, 100, qid, 0)
        if st != "SUCCESS":
            print("  search stop:", st)
            break
        save_raw("youtube", run_id, f"search_{qid}", pl, {"endpoint": "search.list", "params": params,
                                                          "query_id": qid, "query_text": term, "stage": "search",
                                                          "access_method": "youtube_data_api_v3"})
        for it in pl.get("items") or []:
            vid = it["id"].get("videoId")
            if vid and vid not in videos:
                videos[vid] = {"query_id": qid, "lang": lang}
        ck.state["videos"] = videos
        ck.mark(key_, len(pl.get("items") or []))
        print(f"  search [{term}] videos total {len(videos)}")
    # ---- video metadata (50 ids / unit)
    ids = sorted(videos)
    for i in range(0, len(ids), 50):
        k = f"videos:{i}"
        if ck.done(k):
            continue
        st, pl = call("videos", {"part": "snippet,statistics", "id": ",".join(ids[i:i + 50])}, 1, "YT_META", i)
        if st != "SUCCESS":
            break
        save_raw("youtube", run_id, f"videos_{i}", pl, {"endpoint": "videos.list", "query_id": "YT_META",
                                                        "stage": "videos", "access_method": "youtube_data_api_v3"})
        for it in pl.get("items") or []:
            videos[it["id"]]["comments"] = int(it.get("statistics", {}).get("commentCount", 0) or 0)
            videos[it["id"]]["title"] = it["snippet"]["title"]
        ck.state["videos"] = videos
        ck.mark(k)
    # ---- comment threads: Indonesian-query videos first, then others; seeded shuffle within group
    rng = random.Random(42)
    cand = [v for v in ids if videos[v].get("comments", 0) >= 3]
    rng.shuffle(cand)
    cand.sort(key=lambda v: 0 if videos[v]["lang"] == "id" else 1)
    for vid in cand[:a.max_videos]:
        k = f"threads:{vid}"
        if ck.done(k):
            continue
        token, got, page = None, 0, 0
        while got < a.comments_per_video:
            params = {"part": "snippet,replies", "videoId": vid, "maxResults": 100, "order": "relevance",
                      "textFormat": "plainText"}
            if token:
                params["pageToken"] = token
            st, pl = call("commentThreads", params, 1, videos[vid]["query_id"], page)
            if st != "SUCCESS":
                break
            save_raw("youtube", run_id, f"threads_{vid}_{page}", pl,
                     {"endpoint": "commentThreads.list", "params": {k2: v2 for k2, v2 in params.items()},
                      "query_id": videos[vid]["query_id"], "video_id": vid, "video_title": videos[vid].get("title"),
                      "stage": "comment_threads", "access_method": "youtube_data_api_v3"})
            got += len(pl.get("items") or [])
            token = pl.get("nextPageToken")
            page += 1
            if not token:
                break
        ck.mark(k, got)
        if units >= a.budget:
            print("  quota budget reached")
            break
    log_run(run_id=run_id, source="youtube", started_at=started, ended_at=utcnow(),
            status="SUCCESS" if units < a.budget else "EXHAUSTED", requests="", objects=len(videos),
            note=f"units={units}")
    print("youtube done; units used", units)


if __name__ == "__main__":
    main()
