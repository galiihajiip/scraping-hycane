# Data Quality Report

Source tables: `outputs/tables/data_quality_metrics.csv`, `missingness.csv`, `spam_reason_codes.csv`, `thread_dominance_top30.csv`, `gold_exclusions.csv`, `data/manifests/semantic_duplicates.csv`.

## Key rates
| metric | value |
|---|---|
| bronze_rows | 150,708.0000 |
| unique_source_objects | 136,019.0000 |
| source_id_duplicate_rate | 0.0975 |
| irrelevant_rate | 0.2290 |
| unrelated_meaning_excluded | 443.0000 |
| spam_rate_among_relevant | 0.0031 |
| text_duplicate_rate_among_relevant | 0.0288 |
| semantic_duplicates | 348.0000 |
| cannabis_context_share_of_gold | 0.0151 |
| news_or_promo_share_of_core | 0.0071 |
| missing_timestamp_rate_gold | 0.0000 |
| mean_language_confidence_gold | 0.7570 |
| low_language_confidence_share | 0.1774 |
| geo_known_rate_gold | 0.0124 |
| gold_records | 93,125.0000 |
| gold_core_scope | 91,723.0000 |
| customer_voice_core | 91,068.0000 |
| requests_logged | 5,142.0000 |
| request_error_rate | 0.0134 |
| requests_with_retries_share | 0.0325 |

Notes:
- `source_id_duplicate_rate` = share of bronze rows that were the same platform object captured by more than one query/instance (resolved by source ID; not text duplicates).
- Spam score is a transparent rule score (reason codes below), not a calibrated probability; negativity is never a spam signal.
- Text duplicates combine exact, normalised-exact and MinHash (5-char shingles, 128 perms, Jaccard ≥ 0.85) near-duplicates; semantic duplicates use multilingual MiniLM cosine ≥ 0.95 on texts ≥ 40 characters.
- Thread dominance: the largest single thread holds 0.58% of customer-voice records (warning threshold 2%).

## Spam reason codes (silver)
| spam_reason | n |
|---|---|
| AUTHOR_REPEATED_TEXT | 2,501 |
| LOW_ALPHA | 1,772 |
| MANY_URLS | 1,403 |
| PROMO_TERMS | 1,141 |
| HASHTAG_STUFFING | 617 |
| LINK_ONLY | 301 |
| CHANNEL_SELF_PROMO | 9 |

## Top threads by customer-voice records
| platform | thread_id | n | share_of_customer_voice |
|---|---|---|---|
| youtube | yt_1WhAqlxk1Sc | 526 | 0.01 |
| youtube | yt_7dqfuTu0cO8 | 493 | 0.01 |
| youtube | yt_JXKfIASdSqM | 488 | 0.01 |
| youtube | yt_luon_YiYROE | 464 | 0.01 |
| youtube | yt_OYVcbVhg4xk | 446 | 0.00 |
| youtube | yt_i3-9u-HtFG8 | 426 | 0.00 |
| youtube | yt_DcG3sqwpSa0 | 424 | 0.00 |
| youtube | yt_zOKZCuwjWi8 | 419 | 0.00 |
| youtube | yt_cun-_s0bQAc | 416 | 0.00 |
| youtube | yt_kLz_7oXXxsg | 416 | 0.00 |

## Missingness (gold, top 25 fields)
| field | missing_n | missing_pct |
|---|---|---|
| evidence_strength | 93,125 | 100.00 |
| topic_confidence | 93,125 | 100.00 |
| rating | 93,125 | 100.00 |
| exclusion_meaning | 93,125 | 100.00 |
| duplicate_reason | 93,125 | 100.00 |
| exclusion_reason | 93,125 | 100.00 |
| author_public_profile_location | 93,125 | 100.00 |
| semantic_duplicate_of | 93,125 | 100.00 |
| region | 93,125 | 100.00 |
| views | 92,962 | 99.82 |
| country | 92,897 | 99.76 |
| contradiction_flags | 92,770 | 99.62 |
| feature_explicit | 92,665 | 99.51 |
| self_reported_place | 92,191 | 99.00 |
| geo_source | 91,966 | 98.76 |
| geo_confidence | 91,966 | 98.76 |
| spam_reason_codes | 91,788 | 98.56 |
| duplicate_cluster_id | 91,563 | 98.32 |
| hashtags | 90,024 | 96.67 |
| platform_language | 89,502 | 96.11 |
| shares | 89,150 | 95.73 |
| mentions | 88,853 | 95.41 |
| urls | 88,325 | 94.85 |
| price_signal | 86,960 | 93.38 |
| pain_points | 81,917 | 87.96 |

Engagement fields are platform-dependent (e.g., Mastodon/Bluesky provide likes/reposts; archive Reddit scores are point-in-time; HN comments have no score). Missing values are left missing, never imputed.

## Audit samples
`data/annotation/audit_*.csv` hold 100-record samples of raw/clean pairs, likely duplicates, borderline-relevance records and spam candidates for manual inspection.
