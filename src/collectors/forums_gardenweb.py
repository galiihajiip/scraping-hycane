"""GardenWeb (Houzz) Hydroponics forum collector — permitted public HTML.

robots.txt (checked at runtime) disallows only /discussions/*sort=* and /discussions/*view=* among discussion
paths; this collector requests plain listing pages (/discussions/hydroponics/p/N) and plain thread pages only.
Thread content is read from the server-rendered QuestionAnswerStore JSON embedded in the page.
"""
from __future__ import annotations

import argparse
import json
import random
import re
import urllib.robotparser

from bs4 import BeautifulSoup

from src.utils.common import PROJECT, SOURCES, Checkpoint, Http, log_run, new_run_id, save_raw, utcnow

CFG = SOURCES["sources"]["forums_gardenweb"]
BASE = "https://www.houzz.com"
TAGS = ["hydroponics"]
http = Http("forums_gardenweb", CFG["min_interval_s"])
THREAD_RE = re.compile(r'href="(?:https://www\.houzz\.com)?(/discussions/(\d{5,})/[a-z0-9-]+)')


def robots():
    rp = urllib.robotparser.RobotFileParser(BASE + "/robots.txt")
    rp.read()
    return rp


def extract_store(html: str):
    s = BeautifulSoup(html, "lxml")
    for sc in s.find_all("script"):
        t = sc.string or ""
        if '"QuestionAnswerStore"' in t:
            j = json.loads(t[t.find("{"):t.rfind("}") + 1])
            return j["data"]["stores"]["data"]["QuestionAnswerStore"]
    return None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--max-threads", type=int, default=3000)
    ap.add_argument("--max-pages", type=int, default=400)
    a = ap.parse_args()
    rp = robots()
    ua = PROJECT["http"]["user_agent"]
    run_id = new_run_id("forums_gardenweb")
    ck = Checkpoint("forums_gardenweb")
    started, n_req = utcnow(), 0
    threads = dict(ck.state.get("threads", {}))
    for tag in TAGS:
        for page in range(0, a.max_pages):
            url = f"{BASE}/discussions/{tag}" + (f"/p/{page * 30}" if page else "")
            key = f"list:{url}"
            if ck.done(key):
                continue
            if not rp.can_fetch(ua, url):
                print("robots disallow", url)
                break
            st, code, html = http.get(url, None, "listing", f"GW_{tag}", page, expect_json=False)
            n_req += 1
            if st != "SUCCESS":
                print("  ! listing", url, st, code)
                break
            found = {tid: path for path, tid in THREAD_RE.findall(html)}
            new = {k: v for k, v in found.items() if k not in threads}
            threads.update(found)
            ck.state["threads"] = threads
            ck.mark(key, len(found))
            print(f"  listing p{page}: {len(found)} links, {len(new)} new, total {len(threads)}")
            if not new:
                break
    ids = sorted(threads)
    random.Random(42).shuffle(ids)
    n_ok = 0
    for i, tid in enumerate(ids[:a.max_threads]):
        key = f"thread:{tid}"
        if ck.done(key):
            continue
        url = BASE + threads[tid]
        if not rp.can_fetch(ua, url):
            ck.mark(key, "robots_disallow")
            continue
        st, code, html = http.get(url, None, "thread", "GW_hydroponics", tid, expect_json=False)
        n_req += 1
        if st != "SUCCESS":
            ck.mark(key, f"{st}:{code}")
            continue
        store = extract_store(html)
        if store:
            save_raw("forums", run_id, f"gardenweb_{tid}", store,
                     {"forum": "gardenweb_houzz", "url": url, "thread_id": tid, "query_id": "GW_hydroponics",
                      "stage": "thread", "access_method": "public_html_robots_compliant"})
            n_ok += 1
        ck.mark(key, "ok" if store else "no_store")
        if i % 50 == 0:
            print(f"  threads {i}/{min(len(ids), a.max_threads)} ok={n_ok}")
    log_run(run_id=run_id, source="forums_gardenweb", started_at=started, ended_at=utcnow(), status="SUCCESS",
            requests=n_req, objects=n_ok)
    print("DONE threads", n_ok)


if __name__ == "__main__":
    main()
