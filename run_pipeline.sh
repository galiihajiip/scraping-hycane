#!/usr/bin/env bash
# Full HYCANE pipeline. Each stage is resumable/idempotent; collectors skip checkpointed work.
# Usage: ./run_pipeline.sh [collect|process|all]   (default: process — reuses existing raw captures)
set -euo pipefail
cd "$(dirname "$0")"
PY=".venv/bin/python -W ignore"
MODE="${1:-process}"

if [[ "$MODE" == "collect" || "$MODE" == "all" ]]; then
  $PY -m src.collectors.youtube_api            # NOT_CONFIGURED unless YOUTUBE_API_KEY is set
  $PY -m src.collectors.public_apis            # bluesky, mastodon, lemmy, hackernews, stackexchange
  $PY -m src.collectors.reddit_arcticshift     # slow: archive rate limit
  $PY -m src.collectors.forums_gardenweb --max-threads 3000
  $PY -m src.evidence.academic
  $PY -m src.evidence.expert
fi

if [[ "$MODE" == "process" || "$MODE" == "all" ]]; then
  $PY -m src.normalization.normalize           # RAW -> BRONZE
  $PY -m src.quality.silver                    # BRONZE -> SILVER (clean, language, relevance, spam, dedup)
  $PY -m src.nlp.run_nlp                       # GOLD candidates + rules + sentiment + aspects + semantic dedup
  $PY -m src.nlp.topics                        # BERTopic (KMeans) + NMF fallback
  $PY -m src.persona.cluster                   # persona clustering + robustness
  $PY -m src.reporting.analysis                # final gold + all tables
  $PY -m src.nlp.validation evaluate || true   # needs data/annotation/llm_reference_labels.csv
  $PY -m src.reporting.synthesis               # hypothesis validation, contradictions, triangulation, evidence strength
  $PY -m src.visualization.figures
  $PY -m src.visualization.dashboard
  $PY -m src.reporting.reports                 # markdown reports + final manifest
  .venv/bin/python -m pytest -q tests/
fi
