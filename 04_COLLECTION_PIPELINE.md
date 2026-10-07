# 04 Collection Pipeline

## Goal
Build a resilient, resumable multi-source collection system.

## Directory pattern
```text
data/raw/{youtube,reddit,x,tiktok,instagram,facebook,threads,forums,marketplace,web,academic,expert}
data/{bronze,silver,gold,reference,manifests,logs}
src/{discovery,collectors,adapters,parsing,normalization,quality,dedup,nlp,persona,evidence,visualization,reporting,utils}
config/
outputs/
tests/
```

## Workflow
1. Create project metadata.
2. Generate query manifest.
3. Discover source objects.
4. Collect metadata.
5. Collect comments/replies where legitimate.
6. Save raw payloads.
7. Parse to common schema.
8. Normalize.
9. Quality screen.
10. Deduplicate.
11. Detect language.
12. Analyze.
13. Iterate query expansion.

## Resumability
Each collector must support checkpoints, pagination state, retry, exponential backoff, caching, and restart. A single source failure must never terminate the project.

## Request ledger
Log timestamp, source, endpoint class, query ID, page/cursor, result count, status, retry count, latency, and quota/credit information where available. Never log secrets.

## Dominant-thread control
Store thread/source object IDs. Calculate each thread's share of the corpus. Run both raw and thread-normalized sensitivity analysis when a thread is dominant.

## Completion report
Create `outputs/collection_completion_report.md` with attempted, configured, accessible, raw, parsed, final counts, failure reasons, quota blockers, timeframe, and next-capacity estimate.
