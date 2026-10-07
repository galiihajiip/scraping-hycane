"""Validation sample + model evaluation.

sample:   stratified sample of gold records -> data/annotation/validation_sample.csv (blank human columns) and
          data/annotation/annotation_queue_human.csv (the queue for human annotators).
evaluate: compares candidate sentiment models and rule labelers against a reference label file.

Reference labels in this run were produced by an LLM (Claude, in-session) reading each record — they are
NOT human-verified. All metrics are reported as "agreement with LLM reference labels". Human adjudication
of the queue is required before claiming human-validated accuracy.
"""
from __future__ import annotations

import argparse
import json
import re

import numpy as np
import pandas as pd
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix, f1_score

from src.utils.common import ROOT

ANN = ROOT / "data" / "annotation"
ANN.mkdir(parents=True, exist_ok=True)
EDGE = {
    "id_negation": r"\b(tidak|bukan|belum|gak|nggak|ga|enggak)\b",
    "id_slang": r"\b(ribet|parah|mantap|mantab|wkwk\w*|anjir|gokil|bgt|banget|sih|dong)\b",
    "sarcasm_cue": r"(/s\b|yeah right|great, another|just what i needed|oh great|thanks a lot|love how|sure,|totally)",
    "en_negation": r"\b(not|never|no|n't|nothing|nobody)\b",
    "emoji_heavy": None,
    "technical_shorthand": r"\b(ph|ec|tds|ppm|dwc|nft|kratky|rdwc|calmag|ab mix)\b",
    "code_switch": None,
}
EN_WORDS = re.compile(r"\b(the|and|is|my|setup|grow|system|nutrient|price|worth|really)\b", re.I)


def edge_flags(r):
    t = r.text_model
    f = []
    for k, rx in EDGE.items():
        if k == "emoji_heavy":
            if r.emoji_count >= 2:
                f.append(k)
        elif k == "code_switch":
            if r.text_language == "id" and EN_WORDS.search(t):
                f.append(k)
        elif k.startswith("id_") and r.text_language != "id":
            continue
        elif re.search(rx, t, re.I):
            f.append(k)
    return "|".join(f)


def sample(n_total=420, seed=42):
    g = pd.read_parquet(ROOT / "data" / "gold" / "hycane_social_listening_gold.parquet")
    v = g[g.is_customer_voice & (g.text_model.str.len() <= 1500)].copy()
    v["edge"] = v.apply(edge_flags, axis=1)
    v["lang3"] = v.text_language.where(v.text_language.isin(["en", "id"]), "other")
    v["conf_band"] = pd.cut(v.sentiment_confidence, [0, .5, .7, .9, 1.01], labels=["<.5", ".5-.7", ".7-.9", ">=.9"])
    rng = np.random.default_rng(seed)
    picks = []
    # 1) all Indonesian records up to 80 (scarce, priority market)
    idn = v[v.lang3 == "id"]
    picks.append(idn.sample(min(80, len(idn)), random_state=seed))
    # 2) targeted edge cases (40 each where available)
    for k in ["sarcasm_cue", "en_negation", "emoji_heavy", "technical_shorthand", "code_switch", "id_slang", "id_negation"]:
        d = v[v.edge.str.contains(k) & ~v.record_id.isin(pd.concat(picks).record_id)]
        picks.append(d.sample(min(20, len(d)), random_state=seed))
    # 3) stratified remainder: platform x predicted sentiment x confidence band
    rest = v[~v.record_id.isin(pd.concat(picks).record_id)]
    remaining = n_total - len(pd.concat(picks))
    strata = rest.groupby(["platform", "sentiment"], observed=True)
    per = max(2, remaining // max(1, strata.ngroups))
    for _, d in strata:
        picks.append(d.sample(min(per, len(d)), random_state=seed))
    s = pd.concat(picks).drop_duplicates("record_id")
    if len(s) > n_total:
        s = s.sample(n_total, random_state=seed)
    s = s.sample(frac=1, random_state=seed)  # blind order
    cols = ["record_id", "platform", "text_language", "edge", "thread_title", "text_model"]
    out = s[cols].copy()
    for c in ["human_sentiment", "human_intent", "human_pain_points", "human_experience", "human_notes", "annotator_id"]:
        out[c] = ""
    out.to_csv(ANN / "validation_sample.csv", index=False)
    out.to_csv(ANN / "annotation_queue_human.csv", index=False)
    comp = dict(n=len(out), by_platform=s.platform.value_counts().to_dict(), by_language=s.lang3.value_counts().to_dict(),
                by_predicted_sentiment=s.sentiment.value_counts().to_dict(),
                by_conf_band=s.conf_band.value_counts().astype(int).to_dict(),
                edge_case_counts={k: int(s.edge.str.contains(k).sum()) for k in EDGE})
    (ANN / "validation_sample_composition.json").write_text(json.dumps(comp, indent=1, default=str))
    print(json.dumps(comp, indent=1, default=str))


def _metrics(y, p, labels):
    rep = classification_report(y, p, labels=labels, output_dict=True, zero_division=0)
    return dict(n=int(len(y)), accuracy=round(accuracy_score(y, p), 4),
                macro_f1=round(f1_score(y, p, labels=labels, average="macro", zero_division=0), 4),
                per_class={k: {m: round(v, 3) for m, v in rep[k].items()} for k in labels if k in rep},
                confusion_matrix=dict(labels=labels, matrix=confusion_matrix(y, p, labels=labels).tolist()))


def evaluate(ref_path=ANN / "llm_reference_labels.csv"):
    ref = pd.read_csv(ref_path)
    g = pd.read_parquet(ROOT / "data" / "gold" / "hycane_social_listening_gold.parquet")
    s = pd.read_csv(ANN / "validation_sample.csv")[["record_id", "edge"]]
    d = ref.merge(g, on="record_id", how="inner").merge(s, on="record_id", how="left")
    out = {"reference": "LLM reference labels (Claude, in-session) — NOT human-verified", "n_reference": int(len(d))}
    L5 = ["POSITIVE", "NEUTRAL", "NEGATIVE", "MIXED", "AMBIGUOUS"]
    L3 = ["POSITIVE", "NEUTRAL", "NEGATIVE"]
    to3 = lambda x: {"MIXED": "NEUTRAL", "AMBIGUOUS": "NEUTRAL"}.get(x, x)
    models = {}
    for m in ["lexicon", "xlmr", "xlmr_id"]:
        models[m] = dict(five_class=_metrics(d.ref_sentiment, d[f"sent_{m}"], L5),
                         three_class=_metrics(d.ref_sentiment.map(to3), d[f"sent_{m}"].map(to3), L3))
        sub = {}
        for k in EDGE:
            dd = d[d.edge.fillna("").str.contains(k)]
            if len(dd) >= 5:
                sub[k] = dict(n=len(dd), acc5=round(accuracy_score(dd.ref_sentiment, dd[f"sent_{m}"]), 3),
                              acc3=round(accuracy_score(dd.ref_sentiment.map(to3), dd[f"sent_{m}"].map(to3)), 3))
        for lang in ["en", "id"]:
            dd = d[d.text_language == lang]
            if len(dd) >= 5:
                sub[f"lang_{lang}"] = dict(n=len(dd), macro_f1_5=round(f1_score(dd.ref_sentiment, dd[f"sent_{m}"], labels=L5, average="macro", zero_division=0), 3),
                                           acc3=round(accuracy_score(dd.ref_sentiment.map(to3), dd[f"sent_{m}"].map(to3)), 3))
        models[m]["slices"] = sub
    out["sentiment"] = models
    best = max(models, key=lambda m: models[m]["five_class"]["macro_f1"])
    out["sentiment_production_model"] = best
    # ---- intent (primary) and pain-point detection (multi-label, per code precision/recall)
    if "ref_intent" in d:
        dd = d[d.ref_intent.notna()]
        labs = sorted(set(dd.ref_intent) | set(dd.intent))
        out["intent"] = _metrics(dd.ref_intent, dd.intent, labs)
        out["intent"]["purchase_intent_precision"] = round(
            ((dd.intent == "EXPLICIT_PURCHASE_INTENT") & (dd.ref_intent == "EXPLICIT_PURCHASE_INTENT")).sum() /
            max(1, (dd.intent == "EXPLICIT_PURCHASE_INTENT").sum()), 3)
    if "ref_pain_points" in d:
        dd = d.copy()
        R = dd.ref_pain_points.fillna("").str.split("|").map(lambda L: {x for x in L if x})
        P = dd.pain_points.fillna("").str.split("|").map(lambda L: {x for x in L if x})
        codes = sorted(set().union(*R) | set().union(*P))
        per = {}
        for c in codes:
            tp = sum(c in r and c in p for r, p in zip(R, P))
            fp = sum(c not in r and c in p for r, p in zip(R, P))
            fn = sum(c in r and c not in p for r, p in zip(R, P))
            per[c] = dict(tp=tp, fp=fp, fn=fn, precision=round(tp / max(1, tp + fp), 3), recall=round(tp / max(1, tp + fn), 3))
        TP = sum(x["tp"] for x in per.values()); FP = sum(x["fp"] for x in per.values()); FN = sum(x["fn"] for x in per.values())
        out["pain_points"] = dict(micro_precision=round(TP / max(1, TP + FP), 3), micro_recall=round(TP / max(1, TP + FN), 3),
                                  per_code=per)
    if "ref_experience" in d:
        dd = d[d.ref_experience.notna()]
        labs = sorted(set(dd.ref_experience) | set(dd.author_experience_signal))
        out["experience"] = _metrics(dd.ref_experience, dd.author_experience_signal, labs)
    if "ref_relevant" in d:
        out["relevance_precision_llm"] = round(d.ref_relevant.astype(str).str.upper().eq("Y").mean(), 3)
    (ROOT / "outputs" / "tables" / "model_validation.json").write_text(json.dumps(out, indent=1))
    man = ROOT / "data" / "manifests" / "model_manifest.json"
    from src.nlp.sentiment import model_versions
    mm = json.loads(man.read_text()) if man.exists() else {}
    mm.update(dict(sentiment_candidates=model_versions(), sentiment_production_model=best,
                   embedding_model="sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2",
                   language_detector="lingua-language-detector (29 languages, preloaded)",
                   rule_taxonomy="config/taxonomy.yaml", validation_reference=out["reference"],
                   validation_n=int(len(d))))
    man.write_text(json.dumps(mm, indent=1))
    print(json.dumps({m: models[m]["five_class"]["macro_f1"] for m in models}), "->", best)
    return out


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("cmd", choices=["sample", "evaluate"])
    a = ap.parse_args()
    sample() if a.cmd == "sample" else evaluate()
