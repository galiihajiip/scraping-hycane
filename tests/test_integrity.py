"""Data-integrity, provenance and output QA tests. Run: .venv/bin/python -m pytest -q tests/"""
import gzip
import json
import random
import re
from pathlib import Path

import pandas as pd
import pytest

ROOT = Path(__file__).resolve().parents[1]
GOLD = ROOT / "data" / "gold" / "hycane_social_listening_gold.parquet"


@pytest.fixture(scope="module")
def gold():
    return pd.read_parquet(GOLD)


def test_gold_ids_unique(gold):
    assert gold.record_id.is_unique


def test_every_gold_record_has_source_reference(gold):
    assert gold.source_id.notna().all()
    assert (gold.source_url.fillna("") != "").mean() > 0.99
    assert gold.raw_capture_path.notna().all()


def test_raw_captures_exist(gold):
    paths = gold.raw_capture_path.unique()
    missing = [p for p in paths if not (ROOT / p).exists()]
    assert not missing, f"{len(missing)} raw captures missing, e.g. {missing[:3]}"


def test_gold_text_traces_to_raw(gold):
    """Sample gold records and confirm the source ID occurs in the referenced immutable raw capture."""
    rng = random.Random(0)
    sample = gold.sample(min(150, len(gold)), random_state=1)
    for _, r in sample.iterrows():
        with gzip.open(ROOT / r.raw_capture_path, "rt", encoding="utf-8") as f:
            raw = f.read()
        sid = str(r.source_id)
        key = sid.split("_", 1)[1] if sid.startswith(("t1_", "t3_")) else sid
        key = re.sub(r"^(gw_[qa]|q|a|c)(?=\d)", "", key)
        assert key in raw, f"{r.record_id} not found in {r.raw_capture_path}"


def test_provenance_hash_present(gold):
    assert gold.provenance_hash.str.len().eq(64).all()


def test_no_academic_or_expert_in_customer_corpus(gold):
    assert not gold.platform.isin(["academic", "expert", "openalex", "crossref"]).any()
    assert (ROOT / "data" / "gold" / "academic_evidence.parquet").exists()
    assert (ROOT / "data" / "gold" / "expert_evidence.parquet").exists()


def test_no_raw_author_handles(gold):
    assert "author" not in gold.columns
    assert gold.author_id_hash.dropna().str.fullmatch(r"[0-9a-f]{20}").all()


def test_no_secrets_in_logs():
    pat = re.compile(r"(AIza[0-9A-Za-z_\-]{20,}|Bearer\s+[A-Za-z0-9\-._~+/]{20,}|client_secret=|api_key=\w{10,}|key=[A-Za-z0-9_\-]{30,})")
    for p in list((ROOT / "data" / "logs").glob("*")) + list((ROOT / "data" / "manifests").glob("*")):
        if p.is_file() and p.stat().st_size < 200_000_000:
            assert not pat.search(p.read_text(errors="ignore")), f"possible secret in {p}"


def test_env_not_committed():
    gi = (ROOT / ".gitignore").read_text()
    assert ".env" in gi


def test_customer_voice_count_matches_results(gold):
    res = json.loads((ROOT / "outputs" / "tables" / "analysis_results.json").read_text())
    assert int(gold.is_customer_voice.sum()) == res["counts"]["customer_voice"]
    assert len(gold) == res["counts"]["gold"]


def test_sentiment_labels_valid(gold):
    assert set(gold.sentiment.unique()) <= {"POSITIVE", "NEUTRAL", "NEGATIVE", "MIXED", "AMBIGUOUS"}
    assert (gold.sentiment_label_source == "model_predicted").all()


@pytest.mark.parametrize("name", ["01_platform_coverage", "02_source_family_coverage", "03_timeline",
                                  "04_sentiment_by_platform", "05_sentiment_by_topic", "06_top_pain_points",
                                  "07_painpoint_frequency_severity", "08_intent_distribution", "09_feature_demand",
                                  "10_persona_distribution", "11_persona_painpoints", "12_persona_features",
                                  "13_language_distribution", "14_geography_explicit", "15_platform_topic_heatmap",
                                  "16_evidence_strength", "17_hycane_feature_mapping", "18_contradictions"])
def test_figures_exist(name):
    assert (ROOT / "outputs" / "figures" / f"{name}.png").exists()
    assert (ROOT / "outputs" / "figures" / f"{name}.svg").exists()


@pytest.mark.parametrize("name", ["platform_coverage", "sentiment_summary", "topic_summary", "pain_point_summary",
                                  "intent_summary", "feature_demand", "persona_summary", "hypothesis_validation",
                                  "contradiction_register", "evidence_strength", "triangulation_matrix"])
def test_required_tables_exist(name):
    assert (ROOT / "outputs" / "tables" / f"{name}.csv").exists()


def test_dashboard_exists():
    html = (ROOT / "outputs" / "dashboard" / "index.html").read_text()
    assert "plotly" in html and len(html) > 100_000


def test_no_synthetic_marker(gold):
    assert not gold.raw_capture_path.str.contains("synthetic|fake|sample_data", case=False).any()
