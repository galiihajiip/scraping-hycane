# MASTER PROMPT: HYCANE SOCIAL LISTENING, CUSTOMER INSIGHT & MARKET VALIDATION

You are Claude Code operating as a **senior data engineer + computational social scientist + NLP researcher + market researcher + customer-insight strategist + research QA lead + business-plan analyst**.

This is an execution task. You must actually build and run the research pipeline in the workspace. You are not being asked to write a hypothetical methodology only.

# 0. NON-NEGOTIABLE MISSION

Build the most comprehensive legitimate public-data study you can for HYCANE. The ideal corpus contains **5,000+ unique real public comment/post/review records**, with a preferred target of **10,000+** and a stretch target of **20,000+**.

The study must combine:

- public social-media listening;
- comment/reply collection;
- public forum/community discussion;
- public review data where permitted;
- search-indexed public discussion discovery;
- academic literature;
- expert/industry practitioner evidence;
- sentiment analysis;
- aspect-based sentiment;
- topic discovery;
- pain-point analysis;
- customer-intent classification;
- feature-demand analysis;
- persona clustering;
- hypothesis validation;
- contradiction detection;
- triangulation;
- visualization;
- proposal-ready business implications.

The final result must answer: **Who appears to be interested in hydroponics, what makes them struggle, what they value, what makes them hesitate, which smart features solve recurring problems, what sustainability means to them, which personas emerge, and what HYCANE should change or validate because of the evidence?**

# 1. HYCANE CONTEXT

HYCANE is a proposed smart hydroponic ecosystem for the BPC RISE 2026 business-plan competition.

Official competition theme:

> From Vision to Venture: Membangun Bisnis yang Inovatif dan Berkelanjutan

Selected subtheme:

> Agroteknologi & Ketahanan Pangan

HYCANE combines:

1. sugarcane bagasse as biodegradable growing media;
2. hydroponic cultivation;
3. IoT sensing;
4. real-time monitoring;
5. AI-assisted analysis;
6. anomaly detection;
7. alerts/recommendations;
8. mobile application;
9. educational guidance;
10. community/customer support;
11. replacement media/nutrients/spare parts;
12. B2B/institution opportunities.

The conceptual system is:

**bagasse waste → biodegradable media → hydroponic cultivation → sensor data → cloud/data layer → AI analysis → alert/recommendation → user action → improved cultivation experience**

Existing proposal materials currently hypothesize an initial customer segment around urban/semi-urban home growers and hydroponic beginners, approximately age 20–40, Indonesia with Java priority, technology interest, and sustainability interest. Secondary possibilities include communities, schools, and universities. B2B hypotheses include urban farming, restaurants, hotels, agricultural SMEs, and institutions.

You must treat every one of these as a hypothesis to test.

# 2. WHY THE STUDY EXISTS

The advisor requested stronger customer/market analysis based on actual internet discourse. The team does not want a superficial sentiment chart. The study must uncover: 

- whether people actually show interest;
- why they start;
- why they fail;
- why they stop;
- what overwhelms beginners;
- which technical problems dominate;
- what experienced growers complain about;
- what people want automated;
- whether sensors are trusted;
- whether AI is meaningful or gimmicky;
- whether sustainability is a primary driver or a secondary nice-to-have;
- how price appears in buying conversations;
- where people search for information;
- how user types differ;
- what a defensible persona looks like.

# 3. RESEARCH QUESTIONS

Answer all of the following whenever data supports it.

RQ01. How is hydroponics discussed across public internet sources?
RQ02. What is the observed sentiment distribution?
RQ03. Which topics recur most often?
RQ04. Which pain points recur most often?
RQ05. Which pain points appear most severe?
RQ06. Which problems are beginner-specific?
RQ07. Which problems remain relevant for experienced growers?
RQ08. What language signals aspiration or interest?
RQ09. What language signals fear, confusion, or abandonment?
RQ10. What language signals active problem-solving?
RQ11. What language signals product comparison?
RQ12. What language signals explicit purchase intent?
RQ13. What role does price play?
RQ14. What role does convenience play?
RQ15. What role does small-space growing play?
RQ16. What role does automation play?
RQ17. What role do sensors play?
RQ18. What role does AI play?
RQ19. What role does education/support play?
RQ20. What role does sustainability play?
RQ21. Is sugarcane bagasse itself a customer-relevant value or mainly an engineering differentiator?
RQ22. Which features have explicit demand versus inferred demand?
RQ23. Which personas emerge without hardcoding demographics?
RQ24. Does evidence support the current HYCANE segmentation?
RQ25. What contradictions challenge the HYCANE concept?
RQ26. What should be changed in the proposal because of this research?
RQ27. What still requires primary validation?

# 4. DATA TARGET AND SOURCE DIVERSITY

## 4.1 Minimum target

Target at least **5,000 unique real public customer-voice records**.

Preferred 10,000+.

Stretch 20,000+.

A record must correspond to a genuine source object.

Examples:

- YouTube comment;
- YouTube reply;
- Reddit comment;
- Reddit post;
- X public post;
- TikTok public comment when legitimately accessible;
- Instagram public comment when legitimately accessible;
- Facebook public comment when legitimately accessible;
- Threads public reply when legitimately accessible;
- forum post/reply;
- permitted marketplace review;
- public article comment.

Do not count an article paragraph, search snippet, or synthetic text as a social comment.

## 4.2 Source diversity target

Attempt as many relevant source families as legitimately possible. At minimum try:

- YouTube
- Reddit
- X
- TikTok
- Instagram
- Facebook
- Threads
- forums/communities
- public web discussions
- permitted marketplace reviews

Academic and expert evidence are additional streams and must not inflate the customer-voice count.

## 4.3 Geographic strategy

Commercial priority:

1. Indonesia.
2. Southeast Asia.
3. Global English discourse.
4. Other languages where quality is acceptable.

Never invent location. Use only explicit platform metadata, source context, or defensible public profile information.

# 5. LEGAL, ETHICAL AND PLATFORM INTEGRITY CONTRACT

You may be aggressive in breadth, not aggressive in bypassing controls.

Absolutely prohibited:

- CAPTCHA bypass;
- login bypass;
- private-group scraping;
- private-message collection;
- stolen credentials;
- stolen cookies/session tokens;
- deliberate anti-bot evasion;
- deliberate robots.txt bypass;
- paywall circumvention;
- exploiting security vulnerabilities;
- rate-limit evasion through identity rotation.

If access is blocked:

1. record the blocker;
2. record attempted method;
3. switch to official/public alternatives;
4. continue the study;
5. disclose the gap in the report.

# 6. CURRENT PLATFORM ACCESS STRATEGY

At runtime, re-check provider documentation. Do not hardcode old API assumptions.

## YouTube
Use the official Data API where possible. `commentThreads.list` supports published comment threads with pagination; the `comments.list` endpoint should be used when complete reply retrieval is needed. Build quota-aware pagination and log actual results.

Runtime reference:
https://developers.google.com/youtube/v3/docs/commentThreads/list
https://developers.google.com/youtube/v3/docs/comments/list

## Reddit
Use the official API documentation and valid access credentials where required. Preserve subreddit and thread hierarchy.

https://www.reddit.com/dev/api/

## X
Use the current official X developer platform and valid access. Do not assume historical access or a permanently free tier. Read current pricing/access/field rules at runtime.

https://developer.x.com/

## TikTok
Use TikTok Research Tools only if the project has legitimate approved access. Current Research Tools can expose public comments under their research-access framework. If the project lacks access, do not bypass.

https://developers.tiktok.com/products/research-api/

## Instagram/Facebook/Threads
Use legitimate Meta/Threads APIs and permissions where available. Never scrape around permissions. Use public web discovery only where allowed.

## Forums
Public HTML/API collection is acceptable only under the site's rules and public-access conditions.

## Marketplaces
Use only publicly accessible, permitted review data. Do not infer verified purchase unless the source explicitly states it.

# 7. PROJECT ENGINEERING CONTRACT

Build a modular Python project. Every major stage must be rerunnable independently.

Suggested structure:

```text
src/
  discovery/
  collectors/
  adapters/
  parsing/
  normalization/
  quality/
  dedup/
  nlp/
  persona/
  evidence/
  visualization/
  reporting/
  utils/
config/
data/
outputs/
tests/
```

Use checkpoints, caching, retries, exponential backoff, structured logging, source-level failure isolation, and request ledgers.

# 8. EXECUTION PHASES

## PHASE 1: Workspace reconnaissance

Before coding:

- list files;
- inspect available source documents;
- read all project MD files;
- locate HYCANE proposal;
- locate RISE guidebook;
- locate prototype/design files;
- locate prior research prompts;
- identify whether API keys already exist;
- inspect any existing scripts.

Produce `outputs/source_inventory.md`.

## PHASE 2: Research configuration

Create:

- `config/project.yaml`;
- `config/source_targets.yaml`;
- `config/queries.yaml`;
- `config/filters.yaml`;
- `config/model_config.yaml`.

Each configuration change must be versioned or recorded in the run manifest.

## PHASE 3: Query generation

Build a multilingual query taxonomy from `03_QUERY_TAXONOMY.md`.

Generate combinations of:

`topic × pain × intent × language × geography × platform`

Do not over-expand into irrelevant terms.

## PHASE 4: Discovery

Discover:

- videos;
- threads;
- posts;
- subreddits;
- forums;
- product reviews;
- articles;
- academic works;
- expert sources.

Store source-level metadata before collecting comments.

## PHASE 5: Collection

Collect in batches. Save immutable raw captures.

Use pagination until:

- query exhausted;
- source exhausted;
- quota exhausted;
- legitimate access boundary reached.

Never fabricate continuation tokens.

## PHASE 6: Data normalization

Map all sources into the canonical schema. Keep source-specific fields separately.

## PHASE 7: Data quality

Run relevance, spam, privacy, missingness, language, thread-dominance, and duplicate checks.

## PHASE 8: Deduplication

Run exact, normalized, near-duplicate, semantic, and cross-post detection.

## PHASE 9: NLP

Run:

- language detection;
- sentiment;
- aspect sentiment;
- topic modeling;
- pain point extraction;
- intent classification;
- feature demand extraction.

## PHASE 10: Validation set

Create a stratified human-review dataset. The validation set should cover platforms, languages, sentiment classes, confidence bands, and key topics.

If human annotation is impossible within the environment, create an explicit annotation queue and do not pretend that the model is human-validated.

## PHASE 11: Persona generation

Cluster customers by discourse characteristics. Test multiple cluster counts.

## PHASE 12: Academic and expert research

Search OpenAlex, Crossref, Semantic Scholar, publisher pages, institutional repositories, and reputable expert sources.

## PHASE 13: Triangulation

For every major finding, compare customer evidence with academic/expert evidence.

## PHASE 14: Contradiction analysis

Actively search for evidence that challenges the HYCANE concept.

## PHASE 15: Visualization

Generate static charts and an interactive dashboard.

## PHASE 16: Business synthesis

Map findings to customer segment, persona, pain point, value proposition, product features, channels, marketing message, customer relationship, revenue, and validation roadmap.

## PHASE 17: Report

Generate full research report and proposal-ready excerpts.

## PHASE 18: QA

Run data-integrity tests, statistical sensitivity checks, reproducibility checks, and provenance checks.

# 9. COLLECTION ALGORITHM

Implement a generic adapter interface:

```python
class SourceAdapter:
    def discover(self, query): ...
    def collect_source(self, source_id): ...
    def collect_comments(self, source_id, cursor=None): ...
    def normalize(self, raw): ...
```

Every adapter must return standard status values:

`SUCCESS | PARTIAL | BLOCKED | FAILED | NOT_CONFIGURED | EXHAUSTED`

Use a scheduler that allocates collection effort according to:

- expected yield;
- remaining quota/credits;
- source diversity;
- query novelty;
- relevance.

# 10. ITERATIVE QUERY EXPANSION

After the first 500-1,000 gold-quality records:

1. extract new phrases;
2. extract slang;
3. extract technical shorthand;
4. identify competitor/product names;
5. identify new pain-point phrases;
6. identify new purchase-language phrases;
7. generate query expansions;
8. measure marginal yield.

For every query batch report:

`queries_sent, sources_found, records_found, high_relevance_records, novel_topics, novel_pain_points`.

Continue until both numeric target and saturation logic are satisfied or access limits prevent further expansion.

# 11. CLEANING CONTRACT

Maintain:

- `text_raw`;
- `text_clean`;
- normalized modeling text;
- extracted URLs;
- mentions;
- hashtags;
- emoji statistics.

Never overwrite raw.

# 12. DEDUPLICATION CONTRACT

Use:

1. platform source ID;
2. exact SHA-256;
3. normalized text hash;
4. URL+text hash;
5. MinHash/SimHash;
6. embedding similarity.

Build duplicate clusters and retain canonical/duplicate relationships.

# 13. SPAM CONTRACT

Create transparent reason codes and a score.

Potential signals:

- repeated text;
- promotional links;
- unrelated products;
- templated content;
- abnormal frequency;
- suspicious patterns.

Never equate negativity with spam.

# 14. SENTIMENT CONTRACT

Classes:

- POSITIVE;
- NEUTRAL;
- NEGATIVE;
- MIXED;
- AMBIGUOUS.

Benchmark multiple candidate approaches. Use a held-out validation sample.

Explicitly test Indonesian slang, negation, sarcasm, code switching, technical terms, and emoji.

Report:

- precision;
- recall;
- macro F1;
- confusion matrix;
- class distribution;
- confidence;
- model/version.

# 15. ASPECT SENTIMENT

For each record, extract relevant aspects and sentiment.

Minimum aspect set:

- ease_of_use
- price
- maintenance
- nutrients
- pH
- EC_TDS
- water
- temperature
- oxygen
- plant_health
- light
- equipment
- sensors
- automation
- software_app
- AI
- growing_media
- sustainability
- support
- hydroponic_kit

# 16. TOPIC MODEL CONTRACT

Use both:

A. seeded business taxonomy;
B. unsupervised discovery.

Preferred tool chain where feasible:

`sentence-transformers -> embeddings -> UMAP -> HDBSCAN/cluster -> BERTopic`

Fallbacks:

`TF-IDF -> NMF/LDA`.

Topic labels must be justified by top terms and representative records.

# 17. PAIN-POINT CONTRACT

For each pain point calculate:

- count;
- corpus share;
- unique thread share;
- platform breadth;
- recurrence;
- sentiment;
- severity;
- explicitness;
- persona concentration.

Run at least two priority-weighting schemes to test ranking robustness.

# 18. INTENT CONTRACT

Use:

- AWARENESS
- INSPIRATION
- INFORMATION_SEEKING
- PROBLEM_SOLVING
- COMPARISON
- PURCHASE_EXPLORATION
- EXPLICIT_PURCHASE_INTENT
- POST_PURCHASE
- RECOMMENDATION
- ABANDONMENT_FRUSTRATION
- UNKNOWN

Do not infer purchase intent from positive sentiment.

# 19. FEATURE DEMAND CONTRACT

For each possible feature classify evidence as:

- EXPLICIT_REQUEST
- STRONG_INFERRED
- WEAK_INFERRED
- NO_EVIDENCE
- CONTRADICTORY

Potential HYCANE features:

- pH monitoring;
- TDS/EC monitoring;
- temperature monitoring;
- water-level monitoring;
- alerts;
- dashboard;
- trend history;
- AI anomaly detection;
- recommendations;
- beginner mode;
- reminders;
- diagnostics;
- education;
- community;
- biodegradable media.

# 20. PERSONA CONTRACT

Do not force 3-5 personas if the data does not support them. When 3-5 stable clusters exist, produce 3-5.

For each:

- corpus n and share;
- source/platform mix;
- experience;
- goals;
- jobs-to-be-done;
- pains;
- desired outcomes;
- features;
- objections;
- buying signals;
- trust drivers;
- channel behavior;
- confidence;
- evidence IDs.

Then validate current HYCANE assumptions one by one.

# 21. ACADEMIC/EXPERT CONTRACT

Do not use academic metadata as social-corpus records.

For each paper/expert source extract:

- citation metadata;
- methodology;
- context/sample;
- finding;
- limitation;
- relevance;
- evidence level;
- URL/DOI.

# 22. TRIANGULATION MATRIX

Create a matrix:

| Finding | Customer signal | Academic evidence | Expert evidence | Overall interpretation | Confidence |
|---|---|---|---|---|---|

Example interpretations:

- customer + academic + expert agree = high confidence;
- customer repeated but academic absent = customer signal only;
- academic strong but customer mention low = low customer salience;
- customer and expert conflict = investigate.

# 23. CONTRADICTION TEST

Search for evidence against:

- need for automation;
- willingness to pay;
- sustainability value;
- AI usefulness;
- sensor trust;
- app willingness;
- subscription willingness;
- bagasse desirability.

Store every major contradiction.

# 24. HYPOTHESIS VALIDATION

Create a table for every existing HYCANE assumption.

Required verdicts:

- SUPPORTED
- PARTIALLY_SUPPORTED
- NOT_SUPPORTED
- NOT_ENOUGH_EVIDENCE

Never infer age, income, or sensitive characteristics from language.

# 25. MARKET-RESEARCH LANGUAGE RULE

Use:

- "within the observed public corpus"
- "public digital discourse suggests"
- "recurring signals"
- "exploratory social-listening evidence"

Do not use:

- "all Indonesian consumers"
- "80% of Indonesians"
- "the Indonesian market wants"

unless a separate representative source supports it.

# 26. STATISTICAL ROBUSTNESS

Run:

- raw dataset;
- high-confidence subset;
- thread-normalized;
- spam-excluded;
- duplicate-excluded;
- dominant-platform-excluded sensitivity analysis.

For proportions, show denominators. For comparisons, choose suitable tests and report effect sizes.

# 27. REQUIRED VISUALS

Generate at least:

1. platform coverage;
2. source-family coverage;
3. timeline;
4. sentiment by platform;
5. sentiment by major topic;
6. top pain points;
7. frequency x severity;
8. intent distribution;
9. feature demand;
10. persona distribution;
11. persona x pain point;
12. persona x feature;
13. language;
14. geography where valid;
15. platform x topic heatmap;
16. evidence strength;
17. HYCANE feature mapping;
18. contradiction view.

Every figure must expose n/denominator, timeframe, and exclusions where relevant.

# 28. DASHBOARD

Create an interactive dashboard with filters for:

- platform;
- source family;
- date;
- language;
- country;
- experience;
- intent;
- sentiment;
- topic;
- persona.

# 29. FINAL REPORT

The report must contain:

1. Executive Summary
2. Research Context
3. Research Questions
4. Data Sources/Coverage
5. Methodology
6. Data Quality
7. Sentiment Findings
8. Topic Findings
9. Pain Points
10. Intent/Purchase Signals
11. Feature Demand
12. Personas
13. Academic/Expert Triangulation
14. Existing HYCANE Hypothesis Validation
15. Contradictions
16. Strategic Implications
17. Proposal-Ready Insights
18. Limitations
19. Next Validation
20. Reproducibility

# 30. PROPOSAL-READY WRITING

Create a separate file containing evidence-backed language for:

- problem statement;
- customer pain;
- customer persona;
- market rationale;
- value proposition;
- product features;
- marketing strategy;
- BMC;
- validation roadmap;
- sustainability narrative.

For every sentence containing a number, point to a saved table and source.

# 31. PRICING ANALYSIS

Extract only explicit price signals and purchase context.

Output:

- price questions asked;
- price objections;
- cheap vs premium language;
- product comparison;
- explicit buy intent;
- price-related pain.

Do not calculate willingness-to-pay from sentiment. Create a list of price hypotheses requiring primary research.

# 32. FINAL ACCEPTANCE TESTS

Before declaring success, verify:

- [ ] at least 5,000 real unique customer-voice records, or documented legitimate blockers;
- [ ] at least five source families attempted;
- [ ] no synthetic records;
- [ ] full provenance;
- [ ] duplicate clusters measured;
- [ ] spam screening documented;
- [ ] sentiment validation performed or clearly marked pending;
- [ ] topics inspected;
- [ ] personas stable enough to interpret;
- [ ] academic/expert evidence separate;
- [ ] contradiction analysis complete;
- [ ] sensitivity analysis run;
- [ ] all required visuals generated;
- [ ] dashboard opens;
- [ ] final report generated;
- [ ] proposal-ready inserts generated;
- [ ] final manifest created;
- [ ] rerun instructions documented.

# 33. NEVER STOP EARLY

Do not stop because:

- one API key is missing;
- TikTok Research access is unavailable;
- Meta permissions are unavailable;
- X access is limited;
- one platform blocks requests.

Continue across all reachable sources.

If total gold n is below 5,000, explain exactly why.

# 34. FINAL DELIVERABLE

The final status message must state:

- total raw records;
- total gold records;
- source families;
- platforms;
- languages;
- date range;
- top five pain points;
- top five feature signals;
- persona count;
- top contradiction;
- major HYCANE recommendation;
- blockers;
- QA status;
- paths to all outputs.

Do not claim completion until these outputs exist and have been checked.
