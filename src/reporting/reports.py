"""Data-driven reports + final machine-readable manifest. Interpretive reports (final_report.md etc.) are
written by the researcher and cite the tables these numbers come from."""
from __future__ import annotations

import json
import subprocess
from datetime import datetime, timezone

import pandas as pd

from src.utils.common import ROOT

T = ROOT / "outputs" / "tables"
O = ROOT / "outputs"


def md_table(df: pd.DataFrame, floatfmt=2) -> str:
    df = df.copy()
    cols = list(df.columns)
    out = ["| " + " | ".join(map(str, cols)) + " |", "|" + "---|" * len(cols)]
    for _, r in df.iterrows():
        out.append("| " + " | ".join(f"{x:,.{floatfmt}f}" if isinstance(x, float) else (f"{x:,}" if isinstance(x, int) else str(x))
                                     for x in r.values) + " |")
    return "\n".join(out)


def collection_report(res):
    led = pd.read_csv(ROOT / "data" / "logs" / "request_ledger.csv")
    runs = pd.read_csv(ROOT / "data" / "manifests" / "collection_runs.csv")
    cov = pd.read_csv(T / "platform_coverage.csv")
    by = led.groupby("source").agg(requests=("status", "size"), success=("status", lambda s: (s == "SUCCESS").sum()),
                                   failed=("status", lambda s: (s != "SUCCESS").sum()),
                                   retries=("retries", "sum"), first=("ts", "min"), last=("ts", "max")).reset_index()
    excl = pd.read_csv(T / "gold_exclusions.csv")
    raw_files = {p.name: sum(1 for _ in p.rglob("*.json.gz")) for p in (ROOT / "data" / "raw").iterdir() if p.is_dir()}
    c = res["counts"]
    txt = f"""# Collection Completion Report

Generated {datetime.now(timezone.utc):%Y-%m-%d %H:%M} UTC from `data/logs/request_ledger.csv`, `data/manifests/collection_runs.csv`, and `outputs/tables/platform_coverage.csv`.

## Headline
- Unique source objects collected (silver): **{res['data_quality']['unique_source_objects']:,}** (bronze occurrences incl. cross-query repeats: {res['data_quality']['bronze_rows']:,})
- Gold records (relevant, non-spam, de-duplicated): **{c['gold']:,}**
- Gold core scope (cannabis-context excluded): **{c['core']:,}**
- Customer-voice core (also excluding news/promotional posts): **{c['customer_voice']:,}**
- Target check: minimum 5,000 → {'MET' if c['gold'] >= 5000 else 'NOT MET'} on gold records; {'MET' if c['customer_voice'] >= 5000 else 'NOT MET'} on customer-voice core. Preferred 10,000 → {'MET' if c['gold'] >= 10000 else 'NOT MET'} (gold).
- Platforms with gold data: {', '.join(c['platforms'])} ({len(c['platforms'])})
- Posting timeframe of gold records: {c['date_min']} to {c['date_max']}; collection runs: {runs.started_at.min()} to {runs.ended_at.max()}

## Raw capture files per platform directory
{md_table(pd.Series(raw_files).rename_axis('platform').reset_index(name='raw_files'))}

## Requests by source (ledger)
{md_table(by)}

## Coverage by platform
{md_table(cov)}

## Gold exclusions (silver → gold)
{md_table(excl)}

## Blockers and gaps
See `outputs/source_access_audit.md`. Not configured (no credentials): YouTube Data API, X API, TikTok Research API, Meta (Instagram/Facebook), Threads, Reddit OAuth. Blocked by robots/ToS/anti-bot: Kaskus search, Kompasiana, Quora, marketplace reviews. Reddit was collected through the Arctic Shift archive; the r/DWC full sample was dropped mid-run (cannabis-dominated, outside core scope) and the comment-thread sample capped at 500 threads to finish within the archive's rate limit.

## Next-capacity estimate (not collected)
- YouTube Data API with one default key: ~10,000 units/day ≈ 60–90 searches + several thousand comment pages/day → likely the largest single source of Indonesian-language discourse.
- Reddit official API (OAuth): similar subreddits; adds live comment trees beyond archive coverage.
- GardenWeb: {max(0, 3000 - raw_files.get('forums', 0))} of the 3,000 sampled thread links remain uncollected at ~15 s/page.
"""
    (O / "collection_completion_report.md").write_text(txt)


def data_quality_report(res):
    dq = res["data_quality"]
    miss = pd.read_csv(T / "missingness.csv").sort_values("missing_pct", ascending=False).head(25)
    spam = pd.read_csv(T / "spam_reason_codes.csv")
    thd = pd.read_csv(T / "thread_dominance_top30.csv").head(10)
    txt = f"""# Data Quality Report

Source tables: `outputs/tables/data_quality_metrics.csv`, `missingness.csv`, `spam_reason_codes.csv`, `thread_dominance_top30.csv`, `gold_exclusions.csv`, `data/manifests/semantic_duplicates.csv`.

## Key rates
{md_table(pd.Series(dq).rename_axis('metric').reset_index(name='value'), 4)}

Notes:
- `source_id_duplicate_rate` = share of bronze rows that were the same platform object captured by more than one query/instance (resolved by source ID; not text duplicates).
- Spam score is a transparent rule score (reason codes below), not a calibrated probability; negativity is never a spam signal.
- Text duplicates combine exact, normalised-exact and MinHash (5-char shingles, 128 perms, Jaccard ≥ 0.85) near-duplicates; semantic duplicates use multilingual MiniLM cosine ≥ 0.95 on texts ≥ 40 characters.
- Thread dominance: the largest single thread holds {res['max_thread_share']:.2%} of customer-voice records (warning threshold 2%).

## Spam reason codes (silver)
{md_table(spam)}

## Top threads by customer-voice records
{md_table(thd)}

## Missingness (gold, top 25 fields)
{md_table(miss)}

Engagement fields are platform-dependent (e.g., Mastodon/Bluesky provide likes/reposts; archive Reddit scores are point-in-time; HN comments have no score). Missing values are left missing, never imputed.

## Audit samples
`data/annotation/audit_*.csv` hold 100-record samples of raw/clean pairs, likely duplicates, borderline-relevance records and spam candidates for manual inspection.
"""
    (O / "data_quality_report.md").write_text(txt)


def audit_samples():
    s = pd.read_parquet(ROOT / "data" / "silver" / "silver.parquet")
    A = ROOT / "data" / "annotation"
    s.sample(100, random_state=1)[["record_id", "platform", "text_raw", "text_clean"]].to_csv(A / "audit_raw_clean_pairs.csv", index=False)
    s[s.duplicate_status != "canonical"].sample(min(100, (s.duplicate_status != "canonical").sum()), random_state=1)[
        ["record_id", "platform", "duplicate_status", "duplicate_reason", "duplicate_cluster_id", "text_model"]].to_csv(A / "audit_duplicates.csv", index=False)
    b = s[s.relevance_score.between(0.3, 0.7)]
    b.sample(min(100, len(b)), random_state=1)[["record_id", "platform", "relevance_score", "relevance_basis", "thread_title", "text_model"]].to_csv(
        A / "audit_borderline_relevance.csv", index=False)
    sp = s[s.spam_probability > 0]
    sp.sample(min(100, len(sp)), random_state=1)[["record_id", "platform", "spam_probability", "spam_reason_codes", "text_model"]].to_csv(
        A / "audit_spam_candidates.csv", index=False)


def manifest(res, started):
    try:
        commit = subprocess.run(["git", "rev-parse", "HEAD"], capture_output=True, text=True, cwd=ROOT).stdout.strip() or None
    except Exception:
        commit = None
    mm = json.loads((ROOT / "data" / "manifests" / "model_manifest.json").read_text()) if (ROOT / "data" / "manifests" / "model_manifest.json").exists() else {}
    runs = pd.read_csv(ROOT / "data" / "manifests" / "collection_runs.csv")
    blocked = ["youtube (NOT_CONFIGURED)", "x (NOT_CONFIGURED)", "tiktok (NOT_CONFIGURED)", "instagram (NOT_CONFIGURED)",
               "facebook (NOT_CONFIGURED)", "threads (NOT_CONFIGURED)", "reddit official API (NOT_CONFIGURED; archive used)",
               "kaskus (BLOCKED robots /api/)", "kompasiana (BLOCKED ToS)", "quora (BLOCKED 403)",
               "marketplaces (BLOCKED/no permitted API)", "semantic_scholar (RATE-LIMITED)", "web search (FAILED)"]
    qa = (O / "qa_results.txt").read_text() if (O / "qa_results.txt").exists() else "not run"
    outputs = sorted(str(p.relative_to(ROOT)) for p in O.rglob("*") if p.is_file())
    m = dict(run_id=f"hycane_{started:%Y%m%dT%H%M%SZ}", start_time=str(runs.started_at.min()), end_time=f"{datetime.now(timezone.utc):%Y-%m-%dT%H:%M:%SZ}",
             gold_n=res["counts"]["gold"], core_scope_n=res["counts"]["core"], customer_voice_n=res["counts"]["customer_voice"],
             unique_source_objects=res["data_quality"]["unique_source_objects"], bronze_rows=res["data_quality"]["bronze_rows"],
             source_families=res["counts"]["source_families"], platforms=res["counts"]["platforms"],
             languages=res["counts"]["languages_top"], timeframe=dict(min=res["counts"]["date_min"], max=res["counts"]["date_max"]),
             blocked_sources=blocked, model_versions=mm, git_commit=commit,
             academic_records=int(len(pd.read_parquet(ROOT / "data" / "gold" / "academic_evidence.parquet"))),
             expert_records=int(len(pd.read_parquet(ROOT / "data" / "gold" / "expert_evidence.parquet"))),
             qa_status=qa.strip().splitlines()[-1] if qa.strip() else "not run", output_paths=outputs)
    (O / "final_manifest.json").write_text(json.dumps(m, indent=1, default=str))


def main():
    started = datetime.now(timezone.utc)
    res = json.loads((T / "analysis_results.json").read_text())
    audit_samples()
    collection_report(res)
    data_quality_report(res)
    manifest(res, started)
    print("reports + manifest written")


if __name__ == "__main__":
    main()
