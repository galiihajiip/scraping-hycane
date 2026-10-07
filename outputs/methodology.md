# Methodology

Design: exploratory computational social-listening study with three separate evidence streams — (A) customer voice from public posts and comments, (B) academic literature, (C) expert/institutional guidance. The streams are never pooled into one denominator. Results describe **observed public digital discourse**, not a probability sample of any population.

## 1. Discovery and collection
- **Query taxonomy** (`config/queries.yaml`): 14 clusters (core, beginner, interest, failure, nutrients, water/environment, IoT, AI, purchase/price, sustainability, bagasse, small space, experience, product names) in Bahasa Indonesia and English. Each query has a stable ID (`{cluster}_{lang}_{index}`), stored on every record (`query_id`, `all_query_ids`).
- **Access hierarchy**: official/public APIs first, then robots.txt-compliant public HTML. No authentication, CAPTCHA, paywall, robots or anti-bot control was bypassed. Platform status is in `outputs/source_access_audit.md`.
- **Collectors** (`src/collectors/`): Reddit via the Arctic Shift research archive (monthly/quarterly-stratified post samples in hydroponic communities, keyword search in general and Southeast-Asian communities, then comment trees for a subreddit × year round-robin sample of threads); Bluesky search + reply threads; Mastodon hashtag timelines on 5 instances; Lemmy search on 4 instances; Hacker News (Algolia) by year windows; Stack Exchange gardening (questions, answers, comments); GardenWeb/Houzz hydroponics forum (listing pages, then a seeded-random thread sample, checked against robots.txt per URL). YouTube Data API collector is implemented but not configured.
- **Engineering**: per-source minimum request interval, retries with exponential or fixed backoff, `Retry-After` handling, checkpoints (`data/checkpoints/`), request ledger (`data/logs/request_ledger.csv`), run manifest (`data/manifests/collection_runs.csv`), source-level failure isolation.

## 2. Data layers
`RAW` (immutable gzip JSON per API response, with request metadata) → `BRONZE` (canonical schema, one row per capture occurrence; `src/normalization/normalize.py`) → `SILVER` (one row per platform object; cleaning, extraction, language, relevance, scope, spam, dedup flags; `src/quality/silver.py`) → `GOLD` (relevant, in-meaning, non-spam, canonical records with NLP labels; `src/nlp/run_nlp.py`, `src/reporting/analysis.py`) → `INSIGHT` (tables, synthesis; `src/reporting/synthesis.py`). Every gold record keeps `raw_capture_path` and a `provenance_hash` = SHA-256(record_id | raw path | SHA-256(text_raw)).

## 3. Cleaning
Unicode NFKC, HTML-to-text, whitespace normalisation; URL, @mention, #hashtag extraction; emoji counts. `text_raw` is never modified; `text_clean` is human-readable; `text_model` additionally strips URLs and squeezes repeated characters (model input only).

## 4. Language, relevance and scope
- Language: `lingua-language-detector` restricted to 29 languages; confidence retained.
- Relevance score (0–1, transparent): 1.0 strong hydroponic term in text; 0.8 hydroponic-only community; 0.7 thread title strong + weak term in text; 0.6 thread title strong; 0.3 weak term only. Relevant ≥ 0.6.
- Unrelated meanings excluded with logged reason (`exclusion_meaning`): hydroelectric "hydro", bagasse tableware/energy, Rockwool insulation company news, video-game/fiction "hydroponics", a person named Gardyn, bot weekly digests.
- **Scope**: records whose text or thread title mention cannabis are flagged `cannabis_context` and excluded from the core analysis (outside HYCANE's food-crop market and illegal in Indonesia); they remain in gold for sensitivity analysis. Text-based flagging misses implicit cannabis threads (limitation).
- **Voice type**: rule classifier separates `NEWS_OR_PROMO` (press, funding, market reports, ads, institutional announcements) from questions, personal experience and opinion. "Customer voice" = core scope and not news/promo.

## 5. Spam and deduplication
Spam: reason codes `PROMO_TERMS`, `MANY_URLS`, `LINK_ONLY`, `LOW_ALPHA`, `AUTHOR_REPEATED_TEXT`, `HASHTAG_STUFFING`; rule score ≥ 0.5 = spam. Dedup layers: (1) platform source ID across captures; (2) SHA-256 exact text; (3) normalised text hash; (4) URL+text hash (recorded); (5) MinHash LSH near-duplicates (5-char shingles, 128 permutations, threshold 0.85); (6) multilingual MiniLM embedding cosine ≥ 0.95 (texts ≥ 40 chars). Duplicates keep `duplicate_cluster_id`/`duplicate_reason`; the earliest record is canonical.

## 6. Sentiment
Candidates: (a) lexicon baseline (VADER compound for non-Indonesian; custom Indonesian lexicon with negation window); (b) `cardiffnlp/twitter-xlm-roberta-base-sentiment`; (c) (b) routed to `w11wo/indonesian-roberta-base-sentiment-classifier` for Indonesian/Malay text; (d) zero-shot mDeBERTa-XNLI (smoke-tested only; dropped for cost after it mis-read sarcasm and Indonesian "bagus sih tapi ribet"). Five-class mapping from 3-class probabilities: MIXED if p(pos) ≥ 0.25 and p(neg) ≥ 0.25; AMBIGUOUS if max p < 0.5; else argmax. Production model selected by macro-F1 on the validation sample (`outputs/tables/model_validation.json`, `data/manifests/model_manifest.json`).

**Validation reference**: a stratified sample (platform × predicted label, all available Indonesian records up to 80, plus targeted edge cases: sarcasm cues, English and Indonesian negation, Indonesian slang, code-switching, emoji, technical shorthand) was labelled by an LLM (Claude, in-session) reading each record. These are **LLM reference labels, not human-verified labels**; all accuracy figures are agreement with that reference. A blank human annotation queue is provided (`data/annotation/annotation_queue_human.csv`).

## 7. Aspect-based sentiment
For each of 20 aspects (`config/taxonomy.yaml → aspects`), up to three sentences mentioning the aspect are scored with XLM-R and mapped to five classes (`data/gold/aspect_sentiment.parquet`).

## 8. Topics
Seeded taxonomy (pain points, aspects, intents) plus unsupervised discovery: multilingual MiniLM embeddings → UMAP (5-d, cosine, seed 42) → KMeans (k chosen by silhouette over 20–40) inside BERTopic for c-TF-IDF representations. HDBSCAN was tested: EOM selection collapsed to one giant cluster; leaf selection left ~50% outliers (reported in `topic_model_diagnostics.json`). TF-IDF → NMF provides a fallback and an agreement check (NMI/ARI). Labels are assigned after reading top terms and representative records (`config/synthesis_notes.yaml`).

## 9. Pain points, intent, features
- Pain point = topic term **and** a problem cue in the same sentence (e.g., "pH" + "keeps drifting"); severity = base severity per code + uplift for explicit loss/repetition cues. Priority score components (normalised to [0.1, 1]): Frequency (log count), Severity (mean severity + 2 × negative share), Recurrence (share of months), Breadth (share of platforms with ≥ 3 mentions), HYCANE Relevance (researcher weight). Scheme A multiplicative, scheme B weighted additive (F .30, S .25, R .10, B .15, Rel .20), scheme C without relevance; rank correlations reported.
- Intent: 11 classes, multi-label rules with a fixed priority for the primary label; purchase intent requires explicit buying language and is never inferred from positive sentiment.
- Features: mention vs **explicit request** (request cue in the same sentence). Demand class: EXPLICIT_REQUEST (≥ 10 explicit requests on ≥ 2 platforms), STRONG_INFERRED (≥ 150 pain-derived records), WEAK_INFERRED, CONTRADICTORY, NO_EVIDENCE.

## 10. Personas
Unit: customer-voice records with ≥ 2 discourse features (experience, intents, pain points, features, price signals, sustainability, kit/brand, small-space, tech aspects, contradiction flags), TF-IDF-weighted binary vectors. KMeans k = 2–8 compared on silhouette, bootstrap stability (mean ARI over resamples), Ward agreement, and minimum cluster share; robustness on a platform-balanced sample and without the dominant platform. Personas are **discourse segments**, not demographic people; no age, gender, income or other sensitive attribute is inferred.

## 11. Statistics and robustness
Every proportion states its denominator. Platform differences: chi-square with Cramér's V. Sensitivity: all customer voice; high-confidence sentiment only; including cannabis-context; including news/promo; excluding the dominant platform; comments only; posts only; thread-normalised weighting (1/thread size). Saturation: new topic×pain combinations per 100 records in collection order.

## 12. Academic and expert evidence
OpenAlex (677 works across 9 domains; Crossref cross-check for 48 DOIs). Semantic Scholar was rate-limited without a key. A curated subset was read at abstract level (`config/academic_curated.yaml`). Expert/institutional evidence (7 sources) was read in full in-session; unreadable sources are listed as excluded. Triangulation rules are in `src/reporting/synthesis.py`.
