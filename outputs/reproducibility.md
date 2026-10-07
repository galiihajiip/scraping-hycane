# Reproducibility

## Setup
```bash
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
.venv/bin/python -m playwright install chromium   # only for dashboard QA screenshots
cp .env.example .env                               # optional: add API keys to enable more collectors
```

## Re-run
```bash
./run_pipeline.sh process   # rebuild bronze → silver → gold → tables → figures → dashboard → reports → tests from existing raw captures
./run_pipeline.sh collect   # resume collection (checkpointed; completed requests are skipped)
./run_pipeline.sh all
```
Individual stages: see `run_pipeline.sh` (each is `python -m <module>`).

## Determinism
- Random seeds: 42 for UMAP, KMeans, NMF, persona clustering, bootstrap resampling, sampling of threads and validation records.
- Sentiment probabilities and embeddings are cached by text SHA-256 in `data/cache/`; re-runs reuse them. Deleting the cache re-computes them; transformer inference on Apple MPS may differ from CPU in the last decimal places.
- Raw captures are immutable and never overwritten; re-collection writes new files under a new `run_id`, and source-ID dedup resolves overlap.
- Live sources change over time (deleted posts, new posts). Re-collection will not reproduce the same corpus; re-processing the saved raw captures will.

## Provenance
`gold.record_id` → `raw_capture_path` (gzip JSON containing the platform object and request metadata) → `query_id` / `collection_run_id` → `data/logs/request_ledger.csv`. `provenance_hash` = SHA-256(record_id | raw path | SHA-256(text_raw)). `tests/test_integrity.py` re-checks a sample of records against their raw captures.

## Configuration
All rules and weights are in `config/` (`project.yaml`, `source_targets.yaml`, `queries.yaml`, `filters.yaml`, `taxonomy.yaml`, `hycane_mapping.yaml`, `academic_curated.yaml`, `synthesis_notes.yaml`). Mid-run changes are recorded in comments in those files (for example, dropping r/DWC and capping comment threads at 500).

## Versions
Model identifiers and thresholds: `data/manifests/model_manifest.json`. Package versions: `requirements.txt`. Git commit: `outputs/final_manifest.json`.
