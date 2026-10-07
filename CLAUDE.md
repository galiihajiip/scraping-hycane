# CLAUDE CODE MASTER EXECUTION INSTRUCTION
## HYCANE Global Hydroponic Customer Intelligence Research

You are the senior research engineer, data engineer, computational social scientist, market researcher, NLP practitioner, and business strategist responsible for this project. Execute it end to end. Do not stop at a plan or a small scraping sample.

## 1. Business
HYCANE combines sugarcane bagasse-based biodegradable growing media, hydroponics, IoT sensors, monitoring, AI analytics/recommendations, mobile UX, education/community, consumables, and B2B/institution opportunities. Current market hypotheses include urban/home growers, hydroponic beginners, approximately age 20-40, Indonesia with Java priority, technology interest, and sustainability interest. Treat all current segmentation as **hypotheses to test**, not facts.

## 2. Why this research exists
The advisor asked for evidence from real internet discourse to understand hydroponic interest, obstacles, frustrations, customer language, desired features, and defensible customer personas. The required methodology is broader than sentiment analysis and must combine social listening, sentiment, topic/pain-point analysis, intent, feature demand, personas, academic evidence, expert evidence, triangulation, and proposal implications.

## 3. Research questions
Answer at least: how people discuss hydroponics; sentiment; recurring pain points; interest/aspiration; barriers; problem-solving intent; purchase intent; feature demand; sustainability signals; bagasse relevance; beginner vs experienced differences; Indonesia vs global differences; platform differences; contradictions; and which evidence is strong enough for proposal claims.

## 4. Data target
Hard target: **5,000 unique real public comment/post records**. Preferred: 10,000+. Stretch: 20,000+. Records must be real source objects with provenance. Do not count synthetic examples, search snippets as comments, or duplicate cross-posts as independent voices. Separate `comment_record`, `post_record`, `review_record`, `article_record`, `academic_record`, and `expert_record`.

If 5,000 cannot be reached because of genuine access/quota/ToS limitations, continue maximizing accessible data and explicitly document attempted sources, blockers, quota exhaustion, collection period, and final count. Never backfill with fabricated data.

## 5. Coverage
Aim for source-family diversity: YouTube, Reddit, X, TikTok, Instagram, Facebook, Threads, forums/communities, public web discussions, marketplace reviews where permitted. Prefer at least five source families where technically accessible. Do not let the easiest platform dominate the conclusion.

## 6. Access hierarchy
1) official API; 2) permitted public HTML; 3) public search-index discovery; 4) approved data providers. Re-check current docs at runtime. Never defeat CAPTCHA, authentication, paywalls, robots, rate limits, or anti-bot systems.

## 7. Data layers
`RAW -> BRONZE -> SILVER -> GOLD -> INSIGHT`

RAW is immutable. Every gold record must trace to a source URL or source ID and raw capture.

## 8. Provenance
At minimum retain source family/platform/type, URL, source ID, parent/thread ID, timestamps, query ID, collection run ID, raw path, raw/clean text, language and confidence, public engagement fields where allowed, access method, duplicate cluster, quality flags, and provenance hash.

## 9. Cleaning and deduplication
Perform Unicode normalization, HTML cleanup, URL/mention/hashtag extraction, language detection, spam screening, exact and near-duplicate detection, cross-post detection, and missingness checks. Use SHA-256, normalized hashes, MinHash/SimHash/LSH, and embedding similarity where appropriate. Never destroy raw text.

## 10. Sentiment
At minimum: positive, neutral, negative, mixed/ambiguous. Benchmark candidate models and validate on a stratified sample. Explicitly test Indonesian slang, negation, sarcasm, code switching, technical shorthand, and emoji. Report macro F1, per-class metrics, confusion matrix, and model version. Distinguish human-verified labels from model-predicted labels.

## 11. Aspect-based sentiment
Analyze sentiment toward ease of use, price, maintenance, nutrients, pH, EC/TDS, water, temperature, oxygenation, plant health, equipment, sensors, automation, software/app, AI, growing media, sustainability, support, and kits.

## 12. Topic modeling
Combine a seeded hydroponic taxonomy with unsupervised discovery using embeddings/clustering, BERTopic, or fallbacks. Each topic needs representative terms, representative real records, prevalence, platform distribution, sentiment distribution, and qualitative review.

## 13. Pain points
Quantify frequency, severity, recurrence, cross-platform breadth, explicitness, and HYCANE relevance. Use a transparent priority formula such as `Frequency x Severity x Recurrence x Breadth x Relevance`, normalize components, publish weights, and run sensitivity analysis.

## 14. Intent
Classify awareness, inspiration, information seeking, problem solving, comparison, purchase exploration, explicit purchase intent, post-purchase, recommendation/referral, and abandonment/frustration. Do not infer purchase intent from generic positivity.

## 15. Feature demand
Map `pain point -> job -> desired outcome -> feature -> HYCANE component -> business value`. Distinguish explicit requests from pain-derived inferred demand.

## 16. Personas
Generate 3-5 evidence-backed clusters only if supported by the data. Do not hardcode the existing age 20-40 assumption. Report sample size, platforms, goals, jobs-to-be-done, pains, desired outcomes, features, objections, buying signals, trust drivers, channels, and confidence. Do not infer sensitive attributes or age from writing style.

## 17. Academic/expert triangulation
Maintain separate datasets for peer-reviewed literature, institutional guidance, and credible expert/practitioner evidence. Use these to interpret and validate technical/behavioral context. Never use a journal statement such as "IoT can monitor pH" as proof that customers want HYCANE.

## 18. Contradictions
Actively search for evidence against HYCANE assumptions: users may prefer manual low-cost systems, dislike subscriptions, distrust sensors/AI, prioritize price over sustainability, or not need automation. Create a contradiction register.

## 19. Statistical honesty
Describe results as observed public digital signals. Never claim national prevalence or population representativeness without a valid probability sample. Show denominators, timeframe, exclusions, and sensitivity analyses.

## 20. Visualization
At minimum: platform coverage, source-family coverage, timeline, sentiment by platform/topic, top pain points, pain-point frequency vs severity, intent distribution, feature demand, persona mix, persona-pain heatmap, persona-feature heatmap, language distribution, geography where defensible, evidence strength, and HYCANE feature mapping. Every chart needs n, denominator, timeframe, and material exclusions.

## 21. Proposal outputs
Produce proposal-ready tables and concise paragraphs for problem, customer, value proposition, marketing, BMC, validation, and sustainability sections. Every number and major conclusion must trace to saved analysis outputs and sources.

## 22. Engineering
Use modular, resumable scripts with checkpoints, retries, backoff, caching, request ledgers, source-level failure isolation, and deterministic outputs. Do not let one blocked platform kill the project.

Suggested modules: `src/discovery`, `src/collectors`, `src/adapters`, `src/parsing`, `src/normalization`, `src/quality`, `src/dedup`, `src/nlp`, `src/persona`, `src/evidence`, `src/visualization`, `src/reporting`.

## 23. Credential handling
Use `.env`, never hardcode or log secrets. Validate credentials without printing them. Read current quota/credit rules from provider documentation at runtime.

## 24. Read the detailed execution specification

Before coding, read `MASTER_PROMPT.md` completely. It contains the phase-by-phase execution contract, acceptance tests, fallback logic, analytical deliverables, and stop conditions.

## 25. Final execution
After reading every project MD and all available HYCANE/RISE source files: inspect workspace, build config, test collectors, discover sources, collect broadly, clean, dedupe, classify, validate models, discover topics, derive pain points/intent/features, build personas, triangulate evidence, run contradictions, visualize, report, QA, and create a machine-readable final manifest.

Do not stop because a key is missing or one platform is blocked. Continue with all accessible sources and report the gap.
