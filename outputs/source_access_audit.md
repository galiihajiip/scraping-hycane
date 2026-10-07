# Source Access Audit

Checked at runtime on 2026-10-07/08 UTC. HTTP codes are from unauthenticated test requests with a descriptive research User-Agent. "Capacity" is the observed yield in this run, not a platform-wide estimate. No CAPTCHA, login, robots.txt, paywall or anti-bot control was bypassed.

| Source | Status | Access method | Credentials | Quota / rate limit (observed) | Capacity (this run) | Blocker | Fallback |
|---|---|---|---|---:|---:|---|---|
| Reddit | **SUCCESS via archive (official API not configured)** | Arctic Shift public Reddit research archive API (`/api/posts/search`, `/api/comments/tree`) | none | Per-IP rate window; ~40% of requests needed retries (HTTP 422 "slow down"); paced at 2.5 s + 10 s fixed backoff | see `collection_completion_report.md` | Official `www.reddit.com/*.json` returns **403** unauthenticated; no `REDDIT_CLIENT_ID` for OAuth | Official Reddit OAuth API when credentials are added |
| YouTube | **SUCCESS** | YouTube Data API v3 (`search.list` 100 units, `videos.list`, `commentThreads.list` 1 unit) | `YOUTUBE_API_KEY` (added by user 2026-10-08) | 10,000 units/day; 7,445 used | 83,303 comment records from 1,061 videos (all eligible videos; ≤300 threads/video) | Candidate video list exhausted, not quota | — |
| X (Twitter) | **NOT_CONFIGURED** | X API v2 search | `X_BEARER_TOKEN` missing | `api.x.com` returned 401 | 0 | No paid/academic access | Bluesky and Mastodon used as microblog substitutes (different populations; not equivalent) |
| TikTok | **NOT_CONFIGURED** | TikTok Research API (approval required) | none | — | 0 | No approved research access | None legitimate without approval |
| Instagram | **NOT_CONFIGURED** | Meta Graph API | none | — | 0 | No app/permissions | None |
| Facebook | **NOT_CONFIGURED** | Meta Graph API / Content Library | none | — | 0 | No approval; Indonesian hydroponic groups are mostly private/login-gated | None |
| Threads | **NOT_CONFIGURED** | Threads API | none | — | 0 | No token | None |
| Bluesky | **SUCCESS** | Public AppView `app.bsky.feed.searchPosts` + `getPostThread` (unauthenticated) | none | ~1 req/s, no throttling seen | see completion report | — | — |
| Mastodon | **SUCCESS** | Public hashtag timelines on 5 instances | none | ~1 req/s | see completion report | Full-text search requires auth; hashtags only | — |
| Lemmy | **SUCCESS** | Public `/api/v3/search` on 4 instances | none | ~1 req/s | see completion report | Search is fuzzy → relevance filter required | — |
| Hacker News | **SUCCESS** | HN Algolia official search API | none | none observed | see completion report | Max 1,000 hits/query → yearly windows | — |
| Stack Exchange | **SUCCESS** | API v2.3, gardening.stackexchange.com (CC BY-SA) | none (300 req/day keyless) | 296/300 remaining after first call | see completion report | — | — |
| Forums — GardenWeb (Houzz) | **SUCCESS (rate-limited by design)** | Public HTML; robots.txt-checked per URL (`urllib.robotparser`); 4 s spacing | none | ~15 s per thread page | see completion report | Only first 50 answers per thread are server-rendered | — |
| Forums — Kaskus (ID) | **BLOCKED** | Public HTML | none | — | 0 | Search results are client-rendered from `/api/`, which robots.txt **disallows** | Would need permitted access or a data agreement |
| Forums — Kompasiana (ID) | **BLOCKED (ToS)** | — | — | — | 0 | robots.txt header explicitly prohibits text and data mining | Written permission from PT Kompas Cyber Media |
| Quora | **BLOCKED** | — | — | HTTP 403 | 0 | Anti-bot / login | None |
| THCFarmer / RollItUp forums | **BLOCKED / out of scope** | — | — | HTTP 403 | 0 | 403; cannabis-focused | None |
| Marketplaces (Tokopedia, Shopee, Amazon) | **NOT_CONFIGURED / BLOCKED** | — | — | Tokopedia timed out; Shopee review data loads through internal APIs | 0 | No permitted public review API; anti-bot protections | Manual, permitted review sampling or seller partnership in primary research |
| Web search (DuckDuckGo HTML) | **FAILED** | — | — | timeout | 0 | Not reachable; search-engine scraping not permitted by most ToS | `SEARCH_API_KEY` for an approved search API |
| OpenAlex | **SUCCESS** | Official API | none | polite pool | 677 works | — | — |
| Crossref | **SUCCESS** | Official API | none | — | 48 DOIs cross-checked | — | — |
| Semantic Scholar | **RATE-LIMITED** | Official API | `SEMANTIC_SCHOLAR_API_KEY` missing | HTTP 429 on keyless shared pool | 0 | Shared-pool throttling | OpenAlex used as primary academic index |
| Expert/institutional web pages | **SUCCESS (curated)** | Read in-session (WebFetch / PDF text) | none | — | 7 sources; 3 excluded (403 or unread) | Oklahoma State fact sheet returned 403 | — |

## Source-family count
Attempted families: YouTube, Reddit, X, TikTok, Instagram, Facebook, Threads, Bluesky, Mastodon, Lemmy, Hacker News, Stack Exchange, forums (GardenWeb, Kaskus, Kompasiana, Quora, cannabis forums), marketplaces, web search, academic APIs, expert web = **20+ families attempted**. Families yielding customer-voice data: YouTube, Reddit, Bluesky, Mastodon, Lemmy, Hacker News, Stack Exchange, GardenWeb forum = **8**.

## Note on the Reddit archive
Arctic Shift is a third-party, publicly accessible archive of Reddit data maintained for research use. It was used because the official Reddit API requires OAuth credentials this project does not have. Its use is disclosed here and in the limitations; the official API should replace it when credentials are available. Only public subreddit content is collected, and author names are salted-hashed.
