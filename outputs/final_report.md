# HYCANE Social Listening & Customer Intelligence — Final Report

Study date: 2026-10-07/08 (UTC). Corpus frozen 2026-10-07 21:32 UTC. Every number below cites the saved table it comes from (`outputs/tables/…`). All results describe **observed public digital discourse**, not a representative sample of any population.

---

## 1. Executive Summary

- **Corpus.** 136,019 unique public source objects were collected from 8 platforms. After relevance, unrelated-meaning, spam and duplicate screening, **93,125 gold records** remain. Of these, **91,068 are core-scope customer voice**: cannabis-context and news/promo removed. Indonesian is the second language with **30,703 Indonesian customer-voice records (33.7%)**, mostly YouTube comments on Indonesian tutorials. Timeframe: 2002-01 to 2026-10. Sources: `platform_coverage.csv`, `analysis_results.json`.
- **Strongest pain:** keeping plants alive. PLANT_HEALTH (root rot, yellowing, wilting, pests, *daun kuning*, *layu*) is the most frequent and highest-priority pain under all three weighting schemes. It is followed by nutrients, pH, equipment failure, beginner knowledge and water temperature. COST is the 2nd most frequent pain, but its severity is lower (`pain_point_summary.csv`). The ranking is stable across all eight sensitivity subsets: minimum Spearman ρ = 0.96 vs the core ranking (`pain_point_sensitivity_pct.csv`).
- **Strongest evidence of solution demand:** explicit requests for **education/tutorials** (228 explicit requests on 8 platforms), **community** (62), **TDS/EC monitoring** (46 on 6 platforms) and **pH monitoring** (31 on 6 platforms) (`feature_demand.csv`). Customers ask for answers and guidance far more than for "AI".
- **Strongest evidence against HYCANE assumptions:**
  - **Bagasse is not a customer-recognised value:** 18 mentions in 91k customer-voice records, and most public bagasse talk is about tableware or energy.
  - **Sustainability is rarely a purchase driver:** positive sustainability language in 0.65% of records.
  - **Frugality and DIY substitution are strong:** cheap/DIY language outnumbers premium language about 5:1.
  - **A passive, no-electronics culture exists:** ANTI_AUTOMATION signals on all 8 platforms.
  - The best-known consumer smart garden (AeroGarden) was announced for shutdown in 2024.
- **Personas:** four discourse segments emerged: Self-identified Beginner, Pragmatic Evaluator/DIY Optimizer, Tutorial-Inspired Learner, Struggling Troubleshooter. They are **fragile** (platform-balanced ARI 0.14), so use them as hypotheses for primary research, not as validated segments.
- **Main recommendation:** reposition HYCANE from "smart IoT + AI + bagasse kit" to **"a guided kit that keeps beginners' plants alive"**:
  - pH/TDS monitoring plus plain-language "what to do now" guidance as the core;
  - education/community as the acquisition engine;
  - bagasse media sold on performance and convenience, with sustainability as supporting proof;
  - price justified against the cost of DIY plus failure;
  - no mandatory subscription.

## 2. Research Context

The advisor asked the HYCANE team (BPC RISE 2026; theme "From Vision to Venture: Membangun Bisnis yang Inovatif dan Berkelanjutan"; subtheme Agroteknologi & Ketahanan Pangan) for evidence from real internet discourse. Every HYCANE customer statement in the existing materials is an untested assumption (`outputs/source_inventory.md`):
- segments: urban/home growers, beginners, age 20–40, Indonesia/Java, middle-income, eco-aware, tech-interested;
- price: Rp910,000 kit;
- revenue: premium subscription, bagasse media refills.

The team's own documents state that the prototype is at design stage and that primary market surveys are planned but not done.

## 3. Research Questions

RQ01–RQ27 from `MASTER_PROMPT.md` are answered in Sections 7–16; the mapping is listed in Section 17.

## 4. Data Sources and Coverage

| Platform | Family | Unique objects | Gold | Customer voice (core) | Threads | % Indonesian | Date range |
|---|---|---:|---:|---:|---:|---:|---|
| YouTube (Data API v3) | youtube | 83,303 | 55,271 | 54,622 | 896 videos | 56.0 | 2013–2026 |
| Reddit (Arctic Shift archive) | reddit | 22,402 | 19,625 | 18,931 | 17,041 | 0.3 | 2009–2026 |
| GardenWeb/Houzz forum | forums | 10,904 | 10,778 | 10,548 | 1,620 | 0 | 2002–2025 |
| Mastodon | mastodon | 2,953 | 2,286 | 2,212 | 2,212 | 0.2 | 2017–2026 |
| Hacker News | hackernews | 8,868 | 1,850 | 1,678 | 979 | 0 | 2008–2026 |
| Bluesky | bluesky | 3,238 | 1,689 | 1,608 | 1,245 | 6.0 | 2014–2026 |
| Lemmy | lemmy | 3,358 | 1,218 | 1,075 | 844 | 0 | 2020–2026 |
| Stack Exchange (gardening) | stackexchange | 993 | 408 | 394 | 221 | 0 | 2011–2026 |
| **Total** | 8 families | **136,019** | **93,125** | **91,068** | | 33.7 | 2002–2026 |

Source: `platform_coverage.csv`.

Not obtained:
- **Not configured:** X, TikTok, Instagram, Facebook, Threads, Reddit OAuth (no credentials).
- **Blocked:** Kaskus (search depends on robots-disallowed `/api/`), Kompasiana (ToS prohibits data mining), Quora (403), marketplaces (no permitted review access).

Full detail: `outputs/source_access_audit.md`, `outputs/collection_completion_report.md`.

**Targets:** minimum 5,000 met. Preferred 10,000 met. Stretch 20,000 met (gold 93,125; customer voice 91,068).

**Platform balance:** YouTube contributes 60% of customer voice, so every key result is re-run without YouTube (Section 6).

## 5. Methodology (summary)

Full detail in `outputs/methodology.md`. In brief:
- **Data layers:** RAW (immutable gzip API responses) → BRONZE → SILVER → GOLD → INSIGHT.
- **Cleaning and screening:** language identification (lingua, with Malay→Indonesian correction for Indonesian-query YouTube records); transparent relevance scoring; unrelated-meaning exclusions; cannabis-context scoping; rule-based spam codes.
- **Dedup:** six layers (source ID, exact, normalised, URL+text, MinHash LSH, MiniLM cosine ≥ 0.95).
- **Sentiment:** XLM-R selected over three alternatives on a 420-record validation sample.
- **Seeded taxonomy:** aspect sentiment, pain points, intent, features and contradiction probes (`config/taxonomy.yaml`).
- **Topics:** BERTopic (KMeans k = 35 on UMAP) plus an NMF fallback.
- **Personas:** KMeans on discourse profiles with stability tests.
- **Evidence streams:** academic (OpenAlex, 677 works; 14 curated) and expert (7 sources) kept separate, then triangulated.

## 6. Data Quality

Source: `data_quality_report.md`, `data_quality_metrics.csv`.

| Metric | Value |
|---|---:|
| Bronze occurrences → unique objects | 150,708 → 136,019 (9.8% were the same object hit by several queries) |
| Irrelevant (silver) | 22.9% |
| Unrelated-meaning exclusions | 443 |
| Spam among relevant | 0.31% |
| Text duplicates among relevant | 2.9% |
| Semantic duplicates removed | 348 |
| Cannabis-context share of gold | 1.5% |
| Missing timestamps | 0% |
| Mean language confidence | 0.76 |
| Geo known | 1.2% |
| Largest single thread | 0.58% of customer voice |
| Request error rate | 1.3% (5,142 requests) |

### Validation (LLM reference labels, n = 420, not human-verified)

Sources: `model_validation.json`, `rule_validation.json`.

**Sentiment**

| Model | 3-class accuracy | 3-class macro-F1 | 5-class macro-F1 |
|---|---:|---:|---:|
| XLM-R (chosen) | 0.72 | 0.66 | 0.39 |
| XLM-R + IndoRoBERTa | 0.61 | 0.58 | — |
| Lexicon baseline | 0.57 | 0.48 | — |

- **XLM-R accuracy on Indonesian text:** 0.84.
- **Edge cases (3-class accuracy):** Indonesian slang 0.83, Indonesian negation 0.78, code-switching 0.76, emoji 0.78, technical shorthand 0.71, English negation 0.66, sarcasm cues 0.64.
- **Weak spots:** NEGATIVE precision is low (0.40), so the model over-calls negativity in technical text. The 5-class score is low because the reference rarely uses AMBIGUOUS. Read MIXED and AMBIGUOUS as "uncertain".

**Rules** (held-out half)

| Rule set | Precision | Recall | Other |
|---|---:|---:|---|
| Pain points, per code | 0.27 | 0.31 | — |
| Pain points, any-pain detection | 0.48 | 0.36 | — |
| Intent | — | — | Accuracy 0.45; macro-F1 0.29 |
| Experience | — | — | Accuracy 0.82 |
| Relevance | 0.93 | — | — |

**Interpretation:**
- Treat pain-point counts as **indicative signal volumes**: relative rankings that proved stable, not exact prevalence.
- Treat intent shares as rough.

## 7. Sentiment Findings

Sources: `sentiment_summary.csv`, `sentiment_by_platform.csv`, `sentiment_by_language.csv`, `sentiment_sensitivity.csv`.

- **Customer voice (n = 91,068):** Neutral 35.4%, Positive 25.4%, Ambiguous 17.3%, Negative 16.0%, Mixed 5.9%.
- **Indonesian vs English:** Indonesian-language voice is more positive (28.4% positive vs 11.0% negative) than English (23.4% vs 19.1%). This is driven by gratitude/tutorial-appreciation comments: the "Gratitude for tutorials" topic is 93% positive.
- **Platform differences** are significant but small to moderate: χ² = 8,577, df = 28, Cramér's V = 0.15. Q&A/forum platforms (Stack Exchange, GardenWeb, Hacker News) are the least positive; YouTube and Bluesky the most.
- **Most negative topics** (`sentiment_by_topic.csv`):
  - Pests: 45% negative
  - Herbs/basil & pod-based growing: 34%
  - Algae & oxygenation: 29%
  - Vertical-farming debate: 27%
  - Tomatoes & peppers: 25%
  - Root health: 23%
- **Most negative aspects** (`aspect_sentiment_summary.csv`):
  - plant_health: 39% negative
  - ease_of_use: 28%
  - sustainability: 26%
  - price: 24%
  - temperature: 24%
  - AI: 23% negative vs 22% positive
- **Sensors:** more negative (12%) than positive (6%).

Sentiment is never used as purchase intent.

## 8. Topic Findings

35 topics, each present on 6–8 platforms (`topic_summary.csv`, `15_platform_topic_heatmap.png`). Silhouette sweep 0.33–0.36. Agreement with NMF is low (NMI 0.18), so topics are one lens among several. Four clusters stand out:

1. **Learning and appreciation (Indonesian YouTube):**
   - conversational replies to creators (5,580)
   - gratitude for tutorials (5,250)
   - learning intent (3,419)
   - video feedback (2,075)

   The Indonesian audience treats YouTube creators as teachers.
2. **Technical chemistry:**
   - nutrient mixing/ppm (4,453)
   - AB mix, fertilizer & rockwool (3,080)
   - TDS/PPM meters & calibration (2,257)
   - water source & changes (3,037)
3. **Hardware and DIY builds:**
   - pumps, PVC & electricity (1,902)
   - reservoirs & DWC plumbing (1,772)
   - DIY NFT pipe specs (1,655)
   - plastic/container safety (1,715)
   - DIY project updates (1,186)
4. **Failure modes:**
   - root health (3,105)
   - pests (1,123)
   - algae & oxygenation (920)
   - heat, rain & water temperature (1,702), a distinctly tropical/Indonesian topic (*hujan, atap, panas*)

Commercial "buying: price, where to buy, start-up capital" is its own topic (2,733 records).

**Saturation:** new topic × pain combinations per 100 records fell from 16.8 in the first 1,000 records to 0 in the last 1,000 (`saturation_curve.csv`), so the corpus has saturated on themes.

## 9. Pain-Point Findings

| Rank (A) | Pain | Records | % of voice | Platforms with ≥3 | Negative share | Indonesian records |
|---:|---|---:|---:|---:|---:|---:|
| 1 | PLANT_HEALTH | 4,754 | 5.2% | 8 | 0.37 | 967 |
| 2 | NUTRIENTS | 1,393 | 1.5% | 8 | 0.34 | 248 |
| 3 | PH | 687 | 0.8% | 8 | 0.32 | 106 |
| 4 | EQUIPMENT | 977 | 1.1% | 8 | 0.41 | 175 |
| 5 | KNOWLEDGE | 1,688 | 1.9% | 8 | 0.35 | 151 |
| 6 | TEMPERATURE | 459 | 0.5% | 8 | 0.38 | 106 |
| 7 | EC_TDS | 439 | 0.5% | 7 | 0.33 | 164 |
| 8 | COST | 1,925 | 2.1% | 8 | 0.31 | 385 |

Source: `pain_point_summary.csv`; denominator 91,068; priority = Frequency × Severity × Recurrence × Breadth × Relevance.

**Robustness of the ranking:**
- Scheme A vs B (weighted additive): Spearman 0.99.
- Scheme A vs C (relevance removed): 0.987.
- Top 5 by frequency in every sensitivity subset: PLANT_HEALTH, COST, KNOWLEDGE, NUTRIENTS, EQUIPMENT.
  - Subsets: high-confidence sentiment only, cannabis included, news/promo included, YouTube excluded, comments only, posts only, thread-normalised.

**Beginner vs experienced** (`pain_beginner_vs_experienced.csv`; n = 11,135 beginner/never-tried vs 2,100 experienced/intermediate/professional):
- KNOWLEDGE pain is about equally common in both groups (4.2% vs 4.0%).
- Experienced and commercial growers voice more COST (7.1% vs 2.2%), PLANT_HEALTH (10.2% vs 6.0%), EQUIPMENT and AUTOMATION pain.

**Indonesia vs global** (`pain_indonesian_vs_global.csv`):
- Indonesian records mention every pain at lower rates, because many are short appreciation comments.
- Relatively, EC_TDS is *more* frequent in Indonesian records (0.53% vs 0.46%). Questions on ppm, AB mix strength and TDS meters are characteristic.

**Space and the rule caveat:** SPACE is almost never voiced as a problem (9 records). AUTOMATION/SENSOR/SOFTWARE/AI pains are rare. Pain rules have low precision (Section 6), so the ordering is more reliable than the absolute numbers.

## 10. Customer Intent and Purchase Signals

Source: `intent_summary.csv`, `intent_by_platform.csv`, `purchase_signal_by_platform.csv`.

Primary intent (n = 91,068):

| Intent | Share | Records |
|---|---:|---:|
| Unknown | 35.5% | |
| Information seeking | 25.5% | |
| Inspiration | 13.9% | |
| Awareness | 8.1% | |
| Problem solving | 6.7% | |
| Recommendation | 5.9% | |
| Comparison | 1.9% | |
| Purchase exploration | 1.0% | 931 |
| Post-purchase | 0.7% | 662 |
| Explicit purchase intent | 0.45% | 407 |
| Abandonment/frustration | 0.34% | 314 |

- **Platform differences:** intent differs by platform (Cramér's V = 0.22). YouTube is dominated by inspiration and information seeking; Reddit, GardenWeb and Stack Exchange by problem solving and recommendation; Hacker News, Mastodon and Bluesky by awareness and debate.
- **Purchase signals:** HIGH = 330 and MEDIUM = 483 records (0.9% of voice). They are concentrated in the Pragmatic Evaluator persona (779 of 813) and in YouTube and Reddit.
- **What purchase talk looks like in Indonesian:** "where to buy" (*beli di mana*), "how much" (*harga berapa*) and start-up capital (*modal*).
- **Limitation:** the purchase-intent rule has very few validation cases, so its precision is unverified.

## 11. Feature Demand

Source: `feature_demand.csv`; mapping in `hycane_feature_mapping.csv`.

| Feature | Mentions | Explicit requests (platforms) | Class |
|---|---:|---:|---|
| Education (tutorials, guides) | 7,226 | 228 (8) | EXPLICIT_REQUEST |
| Community | 1,171 | 62 (7) | EXPLICIT_REQUEST |
| TDS/EC monitoring | 763 | 46 (6) | EXPLICIT_REQUEST |
| pH monitoring | 615 | 31 (6) | EXPLICIT_REQUEST |
| Trend history / logging | 657 | 30 (5) | EXPLICIT_REQUEST |
| Diagnostics | 311 | 18 (5) | EXPLICIT_REQUEST |
| Dashboard | 360 | 18 (5) | EXPLICIT_REQUEST |
| Beginner mode | 207 | 8 (2) | STRONG_INFERRED |
| Biodegradable media | 73 | 8 (4) | STRONG_INFERRED (but CONTRADICTED by low salience; see H10) |
| Water-level / temperature monitoring | 149 / 53 | 6 / 5 | STRONG_INFERRED |
| Alerts / reminders | 120 / 145 | 3 / 5 | STRONG_INFERRED |
| AI recommendations / anomaly detection | 92 / 1 | 5 / 0 | STRONG_INFERRED (pain-derived only) |
| Automated dosing | 76 | 1 | STRONG_INFERRED and CONTRADICTED (189 anti-automation records) |

**Explicit vs inferred:**
- *Explicit* demand is for education, community, pH/EC monitoring, logging and diagnosis.
- *Inferred* demand (from pains) favours diagnosis and recommendations. Users rarely name "AI" and almost never "anomaly detection".

## 12. Personas

Full detail in `outputs/persona_report.md`.

| Persona | n (share of 31,114 informative records) | Defining signals | Confidence |
|---|---|---|---|
| P0 Self-identified Beginner | 5,026 (16%) | 100% beginner signal; info-seeking + appreciation; education | LOW |
| P1 Pragmatic Evaluator / DIY Optimizer | 16,374 (53%) | Comparison, cost/cheap language, sensors/monitoring, kit brands; 779 purchase signals; most contradictions | LOW |
| P2 Tutorial-Inspired Learner | 4,867 (16%) | YouTube, positive, inspiration + education; almost no pain or purchase | LOW |
| P3 Struggling Troubleshooter | 4,847 (16%) | 96% problem solving; plant health, knowledge, nutrients; most negative; diagnostics | LOW |

**Model selection:** k = 4 (silhouette 0.13; bootstrap ARI 0.75).

**Stability:**
- Platform-balanced ARI: 0.14.
- ARI without YouTube: 0.46.

**Not validated by this data:** age, gender and income are unobservable. Personas are discourse segments.

## 13. Academic and Expert Triangulation

Sources: `triangulation_matrix.csv`, `outputs/academic_expert_synthesis.md`.

**High confidence** (customer + academic + expert agree):
- pH/EC management matters.
- Plant health/root disease is the dominant failure (CSU root-rot guidance).
- Beginners need structured education (Edufarming case; Surabaya household study).
- Cost is a barrier (Cape Town and Surabaya studies; Illinois Extension recommends cheap passive systems).

**Conflicts:**
- **Sensors:** experts warn that sensor-based EC dosing is imprecise (UF/IFAS EX005; 2023 review W4388723157).
- **Sustainability:** academic adoption models include sustainability awareness (Malang millennial farmers, W4416825938), but public discourse rarely voices it.

**Gap:** no study in the 677-work index tests bagasse as a water-culture hydroponic medium.

## 14. Existing HYCANE Hypothesis Validation

Source: `hypothesis_validation.csv`; metrics in `hypothesis_metrics.json`.

| ID | Hypothesis | Verdict |
|---|---|---|
| H01 | Urban/home growers core segment | PARTIALLY_SUPPORTED (home scale dominates; space is context, not pain) |
| H02 | Beginners core segment with recurring friction | **SUPPORTED** |
| H03 | Age 20–40 | NOT_ENOUGH_EVIDENCE |
| H04 | Indonesia (Java) active discourse | PARTIALLY_SUPPORTED (active Indonesian community; Java untestable) |
| H05 | Middle-market price acceptable | NOT_ENOUGH_EVIDENCE (strong frugality/DIY risk signal) |
| H06 | Technology interest | PARTIALLY_SUPPORTED (niche; sensors viewed critically) |
| H07 | Sustainability is a purchase driver | **NOT_SUPPORTED** |
| H08 | Schools/universities/communities | NOT_ENOUGH_EVIDENCE as buyers; supported as channels |
| H09 | B2B (urban farms, restaurants, hotels, SMEs) | PARTIALLY_SUPPORTED for small hydroponic SMEs; hotels/restaurants not evidenced |
| H10 | Bagasse is customer-relevant value | **NOT_SUPPORTED** |
| H11 | Users want pH/EC/temperature/water monitoring | **SUPPORTED** (pH, EC); partial for temperature/water level |
| H12 | Users want AI recommendations/anomaly detection | PARTIALLY_SUPPORTED (want diagnosis/answers, not "AI") |
| H13 | App + subscription accepted | NOT_ENOUGH_EVIDENCE (pod/subscription and app-reliability complaints) |

## 15. Contradictions

Source: `contradiction_register.csv`.

| Contradiction | Customer-voice records | Platforms | Meaning |
|---|---:|---:|---|
| ANTI_AUTOMATION | 189 | 8 | Passive wick/Kratky systems praised as most reliable |
| PRICE_OVER_FEATURES | 42 | 7 | "I can build this for a fraction of the cost" |
| SOIL_PREFERENCE | 33 | 6 | Quitting hydro over pH chasing and heat; back to soil |
| SUSTAINABILITY_SKEPTIC | 30 | 6 | Energy use, *boros listrik* |
| SUBSCRIPTION_DISLIKE | 21 | 7 | ~$5 seed pods and lock-in resented |
| APP_DISLIKE / SENSOR_DISTRUST / AI_SKEPTICISM | 8 / 8 / 3 | 2–3 | App alerts that don't fire, Wi-Fi drops, probe calibration |

Plus three external contradictions (market, sensor limits, bagasse evidence gap); see `contradiction_register.csv`.

**Top contradiction:** the passive/DIY culture. Many hobbyists believe a bucket, an air stone and Kratky beat any kit, and that integrated kits are overpriced.

## 16. HYCANE Strategic Recommendations

Detail in `outputs/hycane_strategy_implications.md`.

1. **Lead value proposition:** "fewer dead plants for beginners." Monitoring + plain-language next steps (pH/EC first), not "AI".
2. **Education and community are the channel.** Partner with Indonesian hydroponic YouTube creators, run workshops, and ship in-app step-by-step guides. Education is the most requested feature.
3. **Design for the tropics.** Water-temperature and rain/heat guidance; low-power pumps; energy disclosure.
4. **Bagasse media:**
   - Validate it technically first (germination and rooting vs rockwool/sponge).
   - Market it on convenience: no itch, no disposal, consistent results.
   - Keep sustainability as supporting proof.
5. **Price against DIY + failure cost.** Offer an entry tier (media + guidance + optional sensor module). Keep refills open and optional. No mandatory subscription.
6. **App reliability:** offline function and reliable push alerts before AI features.
7. **B2B:** start with small hydroponic SMEs (monitoring time, consistency), not hotels.

## 17. Proposal-Ready Insights

See `outputs/proposal_ready_insights.md` (Bahasa Indonesia, every number linked to a table).

**RQ map:**

| Research questions | Section |
|---|---|
| RQ01–03 | 7–8 |
| RQ04–07 | 9 |
| RQ08–12 | 10 |
| RQ13 | pricing file |
| RQ14–20 | 9–11, 13 |
| RQ21 | H10 |
| RQ22 | 11 |
| RQ23 | 12 |
| RQ24 | 14 |
| RQ25 | 15 |
| RQ26 | 16 |
| RQ27 | 19 |

## 18. Limitations

See `outputs/limitations.md`. The most important:
- not a population sample;
- YouTube dominates (60%), and Indonesian volume reflects query design;
- rule-based pain/intent labels have modest precision;
- validation labels are LLM-produced, not human;
- no demographics;
- personas are fragile;
- Reddit came via a third-party archive.

## 19. Next Validation Plan

| Hypothesis | Test | Sample | Metric | Decision rule |
|---|---|---|---|---|
| Beginners value guided monitoring over DIY | Concept test: 3 offers (DIY kit + tutorial; HYCANE basic; HYCANE + sensors) | 150 Indonesian beginners/aspirants (Java + one non-Java city) | Preference share; stated purchase probability | Go if HYCANE-with-sensors ≥ 30% first choice |
| Price acceptance at Rp910,000 | Van Westendorp + Gabor-Granger | Same 150 | Acceptable price range | Keep price if Rp910k is inside the range of acceptable prices; else tier |
| Bagasse media performs | Lab trial vs rockwool/sponge | 3 crops × 30 cells × 3 media | Germination %, rooting days, pH drift | Claim only if non-inferior to rockwool |
| Monitoring reduces failure | 4-week home pilot | 20 households | Plant survival, harvest, app retention (D30 ≥ 60%), pH deviation ≤ 0.2 | Continue if survival ≥ +20 pp vs control |
| Sustainability as driver | Message A/B (ads) | ≥ 1,000 impressions per arm | CTR / sign-ups | Lead with the winning frame |
| SME tier | Discovery interviews | 10 hydroponic SMEs | Monitoring time, willingness to pilot | Build tier if ≥ 4 agree to pilot |
| Age/segment | Survey screener | — | Age band, dwelling, income band | Replace assumed demographics with measured ones |

## 20. Reproducibility

See `outputs/reproducibility.md`:
- `./run_pipeline.sh process` rebuilds everything from the immutable raw captures.
- Seeds are fixed.
- Model outputs are cached by text hash.
- Provenance is tested in `tests/test_integrity.py`.
