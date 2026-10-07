"""Reddit collector via the Arctic Shift public Reddit archive API.

Official Reddit OAuth is preferred but unavailable (no REDDIT_CLIENT_ID; unauthenticated www.reddit.com JSON
returns 403). Arctic Shift is a public research archive of Reddit data; it is used read-only, rate-limited,
with no authentication bypass. Stages (each checkpointed, resumable):
  1. monthly-stratified post sampling in hydroponic-specific subreddits
  2. keyword post search in general / Southeast-Asian subreddits
  3. comment trees for a stratified sample of threads
"""
from __future__ import annotations

import argparse
import random
from collections import defaultdict
from datetime import datetime, timezone

from src.utils.common import (SOURCES, Checkpoint, Http, iter_raw, log_run, new_run_id, save_raw, utcnow)

CFG = SOURCES["sources"]["reddit"]
BASE = CFG["base_url"]
http = Http("reddit_arcticshift", CFG["min_interval_s"], fixed_backoff_s=10)


def month_windows(start_year=2010, start_month=1, step=3):
    """Calendar windows of `step` months (quarterly by default)."""
    now = datetime.now(timezone.utc)
    y, m = start_year, ((start_month - 1) // step) * step + 1
    while (y, m) <= (now.year, now.month):
        ny, nm = (y + 1, m + step - 12) if m + step > 12 else (y, m + step)
        yield f"{y:04d}-{m:02d}-01", f"{ny:04d}-{nm:02d}-01"
        y, m = ny, nm


def stage_posts_full(run_id: str, ck: Checkpoint):
    n_req = n_obj = 0
    for sub in CFG["subreddits_full"]:
        st, code, pl = http.get(f"{BASE}/api/posts/search", {"subreddit": sub, "limit": 1, "sort": "asc"},
                                "posts_first", f"RD_FULL_{sub}", "first", max_retries=10)
        n_req += 1
        if st != "SUCCESS" or not pl.get("data"):
            print(f"  ! {sub} first-post lookup {st} {code}; skipping")
            continue
        first = datetime.fromtimestamp(pl["data"][0]["created_utc"], timezone.utc)
        for after, before in month_windows(first.year, first.month):
            key = f"full:{sub}:{after}"
            if ck.done(key):
                continue
            params = {"subreddit": sub, "after": after, "before": before, "limit": CFG["posts_per_window"],
                      "sort": "desc"}
            st, code, pl = http.get(f"{BASE}/api/posts/search", params, "posts_search", f"RD_FULL_{sub}", after,
                                    max_retries=10)
            n_req += 1
            if st != "SUCCESS":
                print(f"  ! {key} {st} {code}")
                continue
            data = pl.get("data") or []
            if data:
                save_raw("reddit", run_id, f"posts_{sub}_{after}", pl,
                         {"endpoint": "posts/search", "params": params, "query_id": f"RD_FULL_{sub}",
                          "stage": "posts_full", "access_method": "arctic_shift_api"})
                n_obj += len(data)
            ck.mark(key, len(data))
        print(f"  [{sub}] done; cumulative posts {n_obj}")
    return n_req, n_obj


def stage_posts_keyword(run_id: str, ck: Checkpoint, max_per_query=1000):
    n_req = n_obj = 0
    for sub, terms in CFG["subreddits_keyword"].items():
        for term in terms:
            qid = f"RD_KW_{sub}_{term}"
            key = f"kw:{sub}:{term}"
            if ck.done(key):
                continue
            before, got, page = None, 0, 0
            while got < max_per_query:
                params = {"subreddit": sub, "query": term, "limit": 100, "sort": "desc"}
                if before:
                    params["before"] = before
                st, code, pl = http.get(f"{BASE}/api/posts/search", params, "posts_search", qid, page, max_retries=10)
                n_req += 1
                if st != "SUCCESS":
                    print(f"  ! {qid} {st} {code}")
                    break
                data = pl.get("data") or []
                if not data:
                    break
                save_raw("reddit", run_id, f"kw_{sub}_{term}_{page}", pl,
                         {"endpoint": "posts/search", "params": params, "query_id": qid, "stage": "posts_keyword",
                          "access_method": "arctic_shift_api"})
                got += len(data)
                n_obj += len(data)
                page += 1
                before = int(min(d["created_utc"] for d in data))
                if len(data) < 100:
                    break
            ck.mark(key, got)
            print(f"  [{qid}] {got}")
    return n_req, n_obj


def collected_posts():
    posts = {}
    for path, meta, pl in iter_raw("reddit"):
        if meta.get("stage") not in ("posts_full", "posts_keyword"):
            continue
        for d in pl.get("data") or []:
            posts.setdefault(d["id"], (d, meta))
    return posts


def stage_comments(run_id: str, ck: Checkpoint, seed=42):
    """Stratified thread sample: by subreddit x year, preferring threads with >=3 comments."""
    rng = random.Random(seed)
    posts = collected_posts()
    strata = defaultdict(list)
    for pid, (d, meta) in posts.items():
        if (d.get("num_comments") or 0) < 3:
            continue
        yr = datetime.fromtimestamp(d["created_utc"], timezone.utc).year
        strata[(d.get("subreddit"), yr)].append(pid)
    for k in strata:
        strata[k].sort()
        rng.shuffle(strata[k])
    budget = CFG["comment_threads_max"]
    chosen, keys = [], sorted(strata)
    # round-robin over strata so no subreddit-year dominates
    while len(chosen) < budget and any(strata[k] for k in keys):
        for k in keys:
            if strata[k] and len(chosen) < budget:
                chosen.append(strata[k].pop())
    n_req = n_obj = 0
    for i, pid in enumerate(chosen):
        key = f"tree:{pid}"
        if ck.done(key):
            continue
        params = {"link_id": f"t3_{pid}", "limit": 300, "start_breadth": 40, "start_depth": 6}
        st, code, pl = http.get(f"{BASE}/api/comments/tree", params, "comments_tree", "RD_TREE", pid,
                                max_retries=10)
        n_req += 1
        if st != "SUCCESS":
            print(f"  ! tree {pid} {st} {code}")
            continue
        save_raw("reddit", run_id, f"tree_{pid}", pl,
                 {"endpoint": "comments/tree", "params": params, "query_id": "RD_TREE",
                  "stage": "comments_tree", "post_id": pid, "subreddit": posts[pid][0].get("subreddit"),
                  "access_method": "arctic_shift_api"})
        n_obj += len(pl.get("data") or [])
        ck.mark(key, len(pl.get("data") or []))
        if i % 25 == 0:
            print(f"  trees {i}/{len(chosen)}")
    return n_req, n_obj


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--stages", default="full,keyword,comments")
    ap.add_argument("--test", action="store_true")
    a = ap.parse_args()
    if a.test:
        st, code, pl = http.get(f"{BASE}/api/posts/search", {"subreddit": "Hydroponics", "limit": 2}, "test", "TEST")
        print("reddit_arcticshift test:", st, code, (len(pl.get("data") or []) if pl else 0))
        return
    run_id = new_run_id("reddit")
    ck = Checkpoint("reddit_arcticshift")
    started = utcnow()
    totals = {}
    for stage in a.stages.split(","):
        print(f"== stage {stage}")
        fn = {"full": stage_posts_full, "keyword": stage_posts_keyword, "comments": stage_comments}[stage]
        totals[stage] = fn(run_id, ck)
    req = sum(t[0] for t in totals.values())
    obj = sum(t[1] for t in totals.values())
    log_run(run_id=run_id, source="reddit", started_at=started, ended_at=utcnow(), status="SUCCESS",
            requests=req, objects=obj, note=str(totals))
    print("DONE", totals)


if __name__ == "__main__":
    main()
