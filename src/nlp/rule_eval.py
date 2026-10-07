"""Evaluate rule labelers on LLM reference labels, split into dev (idx<210, used for rule revision) and
held-out test (idx>=210, never inspected during revision)."""
import json
import importlib

import pandas as pd
from sklearn.metrics import f1_score

from src.utils.common import ROOT


def run(tag):
    import src.nlp.rules as R
    importlib.reload(R)
    ref = pd.read_csv(ROOT / "data/annotation/llm_reference_labels.csv").assign(idx=lambda d: range(len(d)))
    g = pd.read_parquet(ROOT / "data/gold/hycane_social_listening_gold.parquet", columns=["record_id", "text_model", "thread_title"])
    d = ref.merge(g, on="record_id")
    labs = pd.DataFrame([R.label(t, ti) for t, ti in zip(d.text_model, d.thread_title)])
    d = pd.concat([d.reset_index(drop=True), labs], axis=1)
    out = {}
    for split, dd in [("dev", d[d.idx < 210]), ("test", d[d.idx >= 210])]:
        Rs = dd.ref_pain_points.fillna("").map(lambda x: {c for c in str(x).split("|") if c and c != "nan"})
        Ps = dd.pain_points.fillna("").map(lambda x: {c for c in x.split("|") if c})
        tp = sum(len(a & b) for a, b in zip(Rs, Ps)); fp = sum(len(b - a) for a, b in zip(Rs, Ps)); fn = sum(len(a - b) for a, b in zip(Rs, Ps))
        anyR, anyP = Rs.map(bool), Ps.map(bool)
        out[split] = dict(n=len(dd), pain_micro_precision=round(tp / max(1, tp + fp), 3), pain_micro_recall=round(tp / max(1, tp + fn), 3),
                          pain_any_precision=round((anyR & anyP).sum() / max(1, anyP.sum()), 3), pain_any_recall=round((anyR & anyP).sum() / max(1, anyR.sum()), 3),
                          intent_acc=round((dd.ref_intent == dd.intent).mean(), 3),
                          intent_macro_f1=round(f1_score(dd.ref_intent, dd.intent, average="macro", zero_division=0), 3))
    print(tag, json.dumps(out))
    return out, d


if __name__ == "__main__":
    run("current")
