# 16 Execution Runbook

## Phase 0 Setup
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
```

## Phase 1 Inspect
Read every MD in this pack. Inspect all HYCANE/RISE source documents available to the agent. Produce `outputs/source_inventory.md`.

## Phase 2 Configure
Create:
```text
config/project.yaml
config/source_targets.yaml
config/queries.yaml
config/filters.yaml
```

## Phase 3 Test connectivity
Run collector test modes. Missing credentials should disable only that connector, not the full run.

## Phase 4 Discovery
Save discovery results and query coverage.

## Phase 5 Collection
Use resumable batch collection and checkpoints.

## Phase 6 Normalize
Map raw objects to canonical schema.

## Phase 7 Quality
Relevance, spam, missingness, privacy, thread dominance.

## Phase 8 Deduplicate
Exact + near duplicate + cross-post analysis.

## Phase 9 NLP
Run sentiment, topics, aspect sentiment, intent, feature demand.

## Phase 10 Personas
Cluster and validate personas.

## Phase 11 Academic/expert
Collect and synthesize literature/expert evidence.

## Phase 12 Synthesis
Create pain-point ranking, contradiction register, HYCANE mappings, and hypothesis validation.

## Phase 13 Visualization
Generate figures and interactive dashboard.

## Phase 14 Report
Generate final report and proposal inserts.

## Phase 15 QA
Run all tests and create `outputs/FINAL_STATUS.md`.

## Expected output tree
```text
outputs/
  executive_summary.md
  final_report.md
  methodology.md
  collection_completion_report.md
  data_quality_report.md
  academic_expert_synthesis.md
  persona_report.md
  hycane_strategy_implications.md
  proposal_ready_insights.md
  pricing_research_gaps.md
  limitations.md
  reproducibility.md
  FINAL_STATUS.md
  tables/
  figures/
  dashboard/
data/raw/
data/bronze/
data/silver/
data/gold/
data/manifests/
data/logs/
config/
src/
tests/
```

Resume previous runs using the manifest and checkpoints. Do not redownload unchanged data unnecessarily.
