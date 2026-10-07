# 19 Output Manifest

## Data
- `data/gold/hycane_social_listening_gold.parquet`
- `data/gold/hycane_social_listening_gold.csv`
- `data/gold/hycane_social_listening_gold.jsonl`
- `data/gold/academic_evidence.parquet`
- `data/gold/expert_evidence.parquet`

## Manifests
- `data/manifests/source_manifest.csv`
- `data/manifests/collection_runs.csv`
- `data/manifests/query_manifest.csv`
- `data/manifests/provenance_manifest.csv`
- `data/manifests/model_manifest.json`

## Analysis tables
- `outputs/tables/platform_coverage.csv`
- `outputs/tables/sentiment_summary.csv`
- `outputs/tables/topic_summary.csv`
- `outputs/tables/pain_point_summary.csv`
- `outputs/tables/intent_summary.csv`
- `outputs/tables/feature_demand.csv`
- `outputs/tables/persona_summary.csv`
- `outputs/tables/hypothesis_validation.csv`
- `outputs/tables/contradiction_register.csv`
- `outputs/tables/evidence_strength.csv`

## Reports
- `outputs/executive_summary.md`
- `outputs/final_report.md`
- `outputs/methodology.md`
- `outputs/data_quality_report.md`
- `outputs/academic_expert_synthesis.md`
- `outputs/persona_report.md`
- `outputs/hycane_strategy_implications.md`
- `outputs/proposal_ready_insights.md`
- `outputs/pricing_research_gaps.md`
- `outputs/limitations.md`
- `outputs/reproducibility.md`
- `outputs/FINAL_STATUS.md`

## Figures
Use deterministic filenames such as:
`01_platform_coverage.png`, `02_source_family_coverage.png`, `03_timeline.png`, `04_sentiment_by_platform.png`, `05_sentiment_by_topic.png`, `06_top_pain_points.png`, `07_painpoint_frequency_severity.png`, `08_intent_distribution.png`, `09_feature_demand.png`, `10_persona_distribution.png`, `11_persona_painpoints.png`, `12_persona_features.png`, `13_language_distribution.png`, `14_evidence_strength.png`, `15_hycane_feature_mapping.png`.

## Dashboard
`outputs/dashboard/index.html`

## Final manifest
Create `outputs/final_manifest.json` with run ID, start/end time, gold n, source families, platforms, languages, timeframe, blocked sources, model versions, Git commit, output paths, and QA status.
