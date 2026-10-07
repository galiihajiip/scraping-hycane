# Collection Completion Report

Generated 2026-10-07 22:26 UTC from `data/logs/request_ledger.csv`, `data/manifests/collection_runs.csv`, and `outputs/tables/platform_coverage.csv`.

## Headline
- Unique source objects collected (silver): **136,019** (bronze occurrences incl. cross-query repeats: 150,708)
- Gold records (relevant, non-spam, de-duplicated): **93,125**
- Gold core scope (cannabis-context excluded): **91,723**
- Customer-voice core (also excluding news/promotional posts): **91,068**
- Target check: minimum 5,000 → MET on gold records; MET on customer-voice core. Preferred 10,000 → MET (gold).
- Platforms with gold data: bluesky, gardenweb, hackernews, lemmy, mastodon, reddit, stackexchange, youtube (8)
- Posting timeframe of gold records: 2002-01-28 to 2026-10-07; collection runs: 2026-10-07T18:58:20Z to 2026-10-07T21:32:28Z

## Raw capture files per platform directory
| platform | raw_files |
|---|---|
| forums | 1,626 |
| stackexchange | 20 |
| hackernews | 263 |
| mastodon | 207 |
| lemmy | 235 |
| web | 0 |
| marketplace | 0 |
| youtube | 1,405 |
| academic | 90 |
| facebook | 0 |
| threads | 0 |
| bluesky | 175 |
| reddit | 607 |
| expert | 0 |
| tiktok | 0 |
| instagram | 0 |
| x | 0 |

## Requests by source (ledger)
| source | requests | success | failed | retries | first | last |
|---|---|---|---|---|---|---|
| bluesky | 220 | 198 | 22 | 0 | 2026-10-07T18:58:21Z | 2026-10-07T19:02:00Z |
| crossref | 93 | 80 | 13 | 0 | 2026-10-07T19:23:36Z | 2026-10-07T19:26:15Z |
| debug | 2 | 2 | 0 | 0 | 2026-10-07T19:00:08Z | 2026-10-07T19:00:11Z |
| forums_gardenweb | 1,739 | 1,738 | 1 | 2 | 2026-10-07T19:08:56Z | 2026-10-07T21:32:23Z |
| hackernews | 374 | 374 | 0 | 0 | 2026-10-07T18:58:21Z | 2026-10-07T19:03:19Z |
| lemmy | 266 | 244 | 22 | 0 | 2026-10-07T18:58:21Z | 2026-10-07T19:06:00Z |
| mastodon | 218 | 211 | 7 | 0 | 2026-10-07T18:58:20Z | 2026-10-07T19:02:20Z |
| openalex | 90 | 90 | 0 | 0 | 2026-10-07T19:22:52Z | 2026-10-07T19:25:46Z |
| reddit_arcticshift | 713 | 710 | 3 | 330 | 2026-10-07T18:57:04Z | 2026-10-07T21:32:15Z |
| stackexchange | 20 | 20 | 0 | 0 | 2026-10-07T18:58:20Z | 2026-10-07T18:58:39Z |
| youtube_api | 1,407 | 1,406 | 1 | 0 | 2026-10-07T20:17:03Z | 2026-10-07T20:25:22Z |

## Coverage by platform
| platform | source_family | raw_bronze_rows | unique_source_objects | relevant | gold_records | gold_core_scope | customer_voice_core | threads_customer_voice | date_min | date_max | pct_indonesian |
|---|---|---|---|---|---|---|---|---|---|---|---|
| bluesky | bluesky | 3,708 | 3,238 | 1,842 | 1,689 | 1,642 | 1,608 | 1,245 | 2014-05-03 | 2026-10-07 | 6.04 |
| gardenweb | forums | 10,904 | 10,904 | 10,904 | 10,778 | 10,591 | 10,548 | 1,620 | 2002-01-28 | 2025-09-06 | 0.00 |
| hackernews | hackernews | 10,859 | 8,868 | 1,877 | 1,850 | 1,699 | 1,678 | 979 | 2008-03-27 | 2026-10-06 | 0.00 |
| lemmy | lemmy | 10,338 | 3,358 | 1,406 | 1,218 | 1,109 | 1,075 | 844 | 2020-12-08 | 2026-10-05 | 0.00 |
| mastodon | mastodon | 7,812 | 2,953 | 2,358 | 2,286 | 2,229 | 2,212 | 2,212 | 2017-06-02 | 2026-10-07 | 0.17 |
| reddit | reddit | 22,567 | 22,402 | 21,077 | 19,625 | 19,009 | 18,931 | 17,041 | 2009-02-05 | 2026-10-07 | 0.32 |
| stackexchange | stackexchange | 1,217 | 993 | 412 | 408 | 398 | 394 | 221 | 2011-06-11 | 2026-07-23 | 0.00 |
| youtube | youtube | 83,303 | 83,303 | 64,988 | 55,271 | 55,046 | 54,622 | 896 | 2013-07-17 | 2026-10-07 | 56.03 |

## Gold exclusions (silver → gold)
| exclusion_reason | n |
|---|---|
| nan | 93,473 |
| not_relevant | 31,155 |
| too_short | 7,823 |
| duplicate | 3,013 |
| spam | 329 |
| unrelated_meaning | 226 |

## Blockers and gaps
See `outputs/source_access_audit.md`. Not configured (no credentials): YouTube Data API, X API, TikTok Research API, Meta (Instagram/Facebook), Threads, Reddit OAuth. Blocked by robots/ToS/anti-bot: Kaskus search, Kompasiana, Quora, marketplace reviews. Reddit was collected through the Arctic Shift archive; the r/DWC full sample was dropped mid-run (cannabis-dominated, outside core scope) and the comment-thread sample capped at 500 threads to finish within the archive's rate limit.

## Next-capacity estimate (not collected)
- YouTube Data API with one default key: ~10,000 units/day ≈ 60–90 searches + several thousand comment pages/day → likely the largest single source of Indonesian-language discourse.
- Reddit official API (OAuth): similar subreddits; adds live comment trees beyond archive coverage.
- GardenWeb: 1374 of the 3,000 sampled thread links remain uncollected at ~15 s/page.
