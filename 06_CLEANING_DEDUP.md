# 06 Cleaning and Deduplication

Clean for analysis without rewriting the meaning. Preserve original text in `text_raw`.

## Cleaning
- Unicode normalization.
- HTML cleanup.
- Whitespace normalization.
- URL extraction.
- Mention and hashtag extraction.
- Emoji counts.
- Repeated-character normalization for model text only.
- Language detection.
- Relevance scoring.
- Spam screening.
- Missingness checks.

## Spam signals
Use transparent reason codes: repeated text, link-only promotion, unrelated sales spam, obvious templates, abnormal frequency, suspicious engagement patterns. A complaint containing a product link is not automatically spam.

## Deduplication
Use multiple layers:
1. source ID;
2. SHA-256 exact hash;
3. normalized text hash;
4. URL + text hash;
5. MinHash/SimHash/LSH;
6. sentence-embedding similarity for near duplicates.

Track `duplicate_cluster_id` and `duplicate_reason`: exact duplicate, near duplicate, syndicated, cross-post, repost, quote, boilerplate.

## Audit samples
Inspect at least:
- 100 raw/clean pairs;
- 100 likely duplicates;
- 100 borderline relevance records;
- 100 spam candidates.

Save audit samples and decisions.

## Missingness
Calculate field-level missing counts and percentages. Never invent values.
