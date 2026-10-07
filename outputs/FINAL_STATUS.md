# FINAL STATUS — HYCANE Social Listening

Run completed 2026-10-08 (UTC). Corpus frozen 2026-10-07 21:32 UTC. QA: **42/42 tests passed** (`outputs/qa_results.txt`).

## Counts
| Item | Value |
|---|---|
| Raw bronze occurrences | 150,708 |
| Unique source objects (silver) | 136,019 |
| **Gold records** | **93,125** |
| Gold core scope (cannabis-context excluded) | 91,723 |
| **Customer-voice core** | **91,068** |
| Indonesian-language customer voice | 30,703 (33.7%) |
| Source families / platforms with data | 8: YouTube, Reddit, forums (GardenWeb), Mastodon, Hacker News, Bluesky, Lemmy, Stack Exchange |
| Languages (gold) | en 57,801; id 31,139; tl 1,733; de 313; pt 258; es 256; ms 213; other |
| Date range (posted) | 2002-01-28 → 2026-10-07 |
| Academic works / curated | 677 / 14 |
| Expert sources (read) / excluded | 7 / 3 |
| Targets | 5k ✅ 10k ✅ 20k ✅ |

## Top five pain points (priority scheme A; stable across sensitivity subsets)
1. PLANT_HEALTH (4,754)
2. NUTRIENTS (1,393)
3. PH (687)
4. EQUIPMENT (977)
5. KNOWLEDGE (1,688)

COST is the 2nd by frequency (1,925) but lower severity.

## Top five feature signals (explicit requests, platforms)
1. Education (228; 8)
2. Community (62; 7)
3. TDS/EC monitoring (46; 6)
4. pH monitoring (31; 6)
5. Logging/history (30; 5)

Diagnostics follows (18; 5).

## Personas
4 discourse segments; **fragile** (platform-balanced ARI 0.14):
- Self-identified Beginner (16%)
- Pragmatic Evaluator / DIY Optimizer (53%)
- Tutorial-Inspired Learner (16%)
- Struggling Troubleshooter (16%)

## Top contradiction
A strong passive/DIY culture. ANTI_AUTOMATION signals appear on 8 platforms (189 records), plus "I can build it for a fraction" (7 platforms). Bagasse is almost absent from customer discourse (18 records). Sustainability is rarely a purchase reason.

## Major recommendation
Reposition HYCANE as **"a guided kit that keeps beginners' plants alive"**:
- pH/EC monitoring + plain-language next steps + diagnosis at the core;
- education and community (Indonesian YouTube creators, workshops) as the main channel;
- bagasse media lab-validated and sold on convenience, with sustainability as supporting proof;
- entry tier priced against DIY + failure cost;
- no mandatory subscription.

## Blockers / gaps
| Category | Sources |
|---|---|
| NOT_CONFIGURED (no credentials) | X, TikTok Research API, Instagram, Facebook, Threads, Reddit official OAuth (Reddit collected via the Arctic Shift archive) |
| BLOCKED | Kaskus (robots disallow `/api/`), Kompasiana (ToS bans data mining), Quora (403), marketplaces (no permitted review access) |
| Rate-limited | Semantic Scholar (keyless) |
| Failed | Web search |

## Validation status
- **Sentiment:** XLM-R; 3-class accuracy 0.72, macro-F1 0.66; Indonesian 0.84.
- **Rules (held-out):** pain micro-P/R 0.27/0.31; intent accuracy 0.45.
- **Reference labels:** LLM-produced (n = 420), **not human-verified**. A human annotation queue is ready in `data/annotation/annotation_queue_human.csv`.

## Paths
| Area | Files |
|---|---|
| Reports | `outputs/final_report.md`, `executive_summary.md`, `methodology.md`, `data_quality_report.md`, `collection_completion_report.md`, `source_access_audit.md`, `environment_audit.md`, `source_inventory.md`, `academic_expert_synthesis.md`, `persona_report.md`, `hycane_strategy_implications.md`, `proposal_ready_insights.md` (Bahasa Indonesia), `pricing_research_gaps.md`, `limitations.md`, `reproducibility.md` |
| Tables | `outputs/tables/` (platform_coverage, sentiment_*, topic_summary, pain_point_*, intent_*, feature_demand, persona_*, hypothesis_validation, contradiction_register, evidence_strength, triangulation_matrix, model_validation, rule_validation, …) |
| Figures | `outputs/figures/01_…` through `19_…` (PNG + SVG) |
| Dashboard | `outputs/dashboard/index.html` |
| Gold data | `data/gold/hycane_social_listening_gold.{parquet,csv,jsonl}`, `academic_evidence.parquet`, `expert_evidence.parquet` |
| Manifests | `data/manifests/`, `outputs/final_manifest.json` |
| Rerun | `./run_pipeline.sh process` |
