"""GOLD build: rule labels + sentiment candidates + aspect sentiment + embeddings + semantic dedup + topics.

Run after silver. Produces data/gold/hycane_social_listening_gold.{parquet,csv,jsonl}.
The production sentiment model is chosen in data/manifests/model_manifest.json (written by validation.py);
default is xlmr_id until validation has been run.
"""
from __future__ import annotations

import json
import re

import numpy as np
import pandas as pd

from src.nlp import sentiment as S
from src.nlp.rules import ASPECT, build_gold, sentences
from src.utils.common import ROOT, sha256

GOLD = ROOT / "data" / "gold"
EMB_MODEL = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"


def production_model():
    p = ROOT / "data" / "manifests" / "model_manifest.json"
    if p.exists():
        return json.loads(p.read_text()).get("sentiment_production_model", "xlmr_id")
    return "xlmr_id"


def embeddings(texts: list[str]) -> np.ndarray:
    path = ROOT / "data" / "cache" / "emb_minilm.parquet"
    cache = pd.read_parquet(path) if path.exists() else pd.DataFrame(columns=["h", "v"])
    known = dict(zip(cache.h, cache.v))
    hs = [sha256(t) for t in texts]
    todo = sorted({h: t for h, t in zip(hs, texts) if h not in known}.items())
    if todo:
        from sentence_transformers import SentenceTransformer
        m = SentenceTransformer(EMB_MODEL, device=S.DEVICE)
        V = m.encode([t[:1000] for _, t in todo], batch_size=64, show_progress_bar=True, normalize_embeddings=True)
        new = pd.DataFrame({"h": [h for h, _ in todo], "v": list(V.astype(np.float32))})
        cache = pd.concat([cache, new], ignore_index=True)
        cache.to_parquet(path, index=False)
        known.update(dict(zip(new.h, new.v)))
    return np.vstack([np.asarray(known[h], dtype=np.float32) for h in hs])


def aspect_sentiment(g: pd.DataFrame) -> pd.DataFrame:
    """Sentence-level XLM-R sentiment for sentences that mention each aspect."""
    pairs = []
    for rid, t, asp in zip(g.record_id, g.text_model, g.aspect_labels):
        if not asp:
            continue
        ss = sentences(t)[:40]
        for a in asp.split("|"):
            sel = [s for s in ss if ASPECT[a].search(s)][:3]
            if sel:
                pairs.append((rid, a, " ".join(sel)[:600]))
    if not pairs:
        return pd.DataFrame(columns=["record_id", "aspect", "aspect_sentiment", "aspect_confidence"])
    P = S.cached("xlmr", [p[2] for p in pairs], lambda ts: S.get("xlmr").probs(ts))
    labs = [S.to5(p) for p in P]
    return pd.DataFrame({"record_id": [p[0] for p in pairs], "aspect": [p[1] for p in pairs],
                         "aspect_sentiment": [l for l, _ in labs], "aspect_confidence": [round(c, 3) for _, c in labs]})


def semantic_dedup(g: pd.DataFrame, E: np.ndarray, thr=0.95):
    """Flag records whose embedding is >= thr cosine to an earlier record from a different thread/author."""
    order = np.argsort(g.created_at.fillna("9999").values)
    flags = np.zeros(len(g), dtype=bool)
    canon = [None] * len(g)
    En = E[order]
    for start in range(0, len(order), 2000):
        block = En[start:start + 2000]
        sims = block @ En[:start + len(block)].T
        for i in range(len(block)):
            gi = start + i
            row = sims[i, :gi]
            if row.size and row.max() >= thr:
                j = int(row.argmax())
                if g.n_chars.values[order[gi]] >= 40:
                    flags[order[gi]] = True
                    canon[order[gi]] = g.record_id.values[order[j]]
    return flags, canon


def main():
    g = build_gold().reset_index(drop=True)
    print("gold (pre-semantic-dedup)", len(g))
    E = embeddings(g.text_model.tolist())
    flags, canon = semantic_dedup(g, E)
    g["semantic_duplicate_of"] = canon
    print("semantic near-duplicates flagged", int(flags.sum()))
    sem = g[flags][["record_id", "semantic_duplicate_of", "platform", "text_model"]]
    sem.to_csv(ROOT / "data" / "manifests" / "semantic_duplicates.csv", index=False)
    keep = ~flags
    g, E = g[keep].reset_index(drop=True), E[keep]
    np.save(ROOT / "data" / "cache" / "gold_embeddings.npy", E)
    # ---- sentiment candidates
    sc = S.score(g, ("lexicon", "xlmr", "xlmr_id"))
    g = pd.concat([g, sc], axis=1)
    prod = production_model()
    g["sentiment"] = g[f"sent_{prod}"]
    g["sentiment_confidence"] = g[f"sent_{prod}_conf"]
    g["sentiment_model"] = prod
    g["sentiment_label_source"] = "model_predicted"
    # ---- aspect sentiment
    asp = aspect_sentiment(g)
    asp.to_parquet(GOLD / "aspect_sentiment.parquet", index=False)
    agg = asp.groupby("record_id").apply(
        lambda d: "|".join(f"{a}:{s}" for a, s in zip(d.aspect, d.aspect_sentiment)), include_groups=False)
    g["aspect_sentiment"] = g.record_id.map(agg).fillna("")
    g.to_parquet(GOLD / "_gold_nlp.parquet", index=False)
    print("gold after NLP", len(g))


if __name__ == "__main__":
    main()
