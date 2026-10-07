"""Sentiment candidates + 5-class mapping, cached by text hash.

Candidates:
  lexicon      VADER (English) + small Indonesian lexicon with negation handling (baseline)
  xlmr         cardiffnlp/twitter-xlm-roberta-base-sentiment (multilingual, 3-class)
  xlmr_id      xlmr for non-Indonesian; w11wo/indonesian-roberta-base-sentiment-classifier for Indonesian
  zeroshot     MoritzLaurer/mDeBERTa-v3-base-xnli-multilingual-nli-2mil7 (benchmark sample only)
5-class mapping from 3-class probabilities: MIXED if p_pos>=0.25 and p_neg>=0.25; AMBIGUOUS if max p<0.5;
otherwise argmax. Thresholds are reported in the model manifest.
"""
from __future__ import annotations

import re

import numpy as np
import pandas as pd
import torch
from transformers import AutoModelForSequenceClassification, AutoTokenizer, pipeline
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

from src.utils.common import ROOT, sha256

CACHE = ROOT / "data" / "cache"
CACHE.mkdir(parents=True, exist_ok=True)
DEVICE = "mps" if torch.backends.mps.is_available() else "cpu"
MODELS = {
    "xlmr": "cardiffnlp/twitter-xlm-roberta-base-sentiment",
    "indo": "w11wo/indonesian-roberta-base-sentiment-classifier",
    "zeroshot": "MoritzLaurer/mDeBERTa-v3-base-xnli-multilingual-nli-2mil7",
}
MIXED_T, AMBIG_T = 0.25, 0.5

ID_POS = {"bagus", "mantap", "mantab", "keren", "suka", "senang", "seneng", "berhasil", "sukses", "subur", "sehat",
          "mudah", "gampang", "praktis", "murah", "hemat", "puas", "rekomen", "top", "josss", "joss", "lancar",
          "cantik", "segar", "panen", "terima kasih", "makasih", "membantu", "bermanfaat", "worth"}
ID_NEG = {"gagal", "mati", "busuk", "layu", "kuning", "mahal", "susah", "sulit", "ribet", "rusak", "bocor", "kecewa",
          "jelek", "parah", "capek", "bingung", "masalah", "kapok", "nyesel", "menyesal", "lambat", "kerdil", "hama",
          "lumut", "jamur", "zonk", "boros"}
ID_NEGATORS = {"tidak", "tak", "bukan", "belum", "gak", "nggak", "ga", "enggak", "ndak", "kurang"}
_vader = SentimentIntensityAnalyzer()


def lexicon_probs(text: str, lang: str):
    if lang == "id" or lang == "ms":
        toks = re.findall(r"\w+", text.lower())
        score = 0
        for i, w in enumerate(toks):
            pol = 1 if w in ID_POS else (-1 if w in ID_NEG else 0)
            if pol and any(t in ID_NEGATORS for t in toks[max(0, i - 2):i]):
                pol = -pol
            score += pol
        pos, neg = sum(1 for w in toks if w in ID_POS), sum(1 for w in toks if w in ID_NEG)
        tot = pos + neg
        if tot == 0:
            return np.array([0.15, 0.7, 0.15])
        p = np.array([neg, 0.5, pos], dtype=float)
        return p / p.sum()
    c = _vader.polarity_scores(text)["compound"]
    v = _vader.polarity_scores(text)
    if v["pos"] >= 0.2 and v["neg"] >= 0.2:  # strong lexical cues on both sides
        return np.array([0.4, 0.2, 0.4])
    return np.array([max(0.0, -c), 1 - abs(c), max(0.0, c)])


def to5(p):
    """p = [neg, neu, pos] -> (label, confidence)."""
    neg, neu, pos = p
    if pos >= MIXED_T and neg >= MIXED_T:
        return "MIXED", float(min(pos, neg) * 2)
    m = int(np.argmax(p))
    if p[m] < AMBIG_T:
        return "AMBIGUOUS", float(p[m])
    return ["NEGATIVE", "NEUTRAL", "POSITIVE"][m], float(p[m])


class HF3:
    def __init__(self, name, order):
        self.tok = AutoTokenizer.from_pretrained(name)
        self.mod = AutoModelForSequenceClassification.from_pretrained(name).to(DEVICE).eval()
        self.order = order  # index map to [neg, neu, pos]
        self.version = f"{name}@{getattr(self.mod.config, '_commit_hash', None) or 'local'}"

    @torch.no_grad()
    def probs(self, texts, bs=32):
        out = []
        for i in range(0, len(texts), bs):
            enc = self.tok(texts[i:i + bs], truncation=True, max_length=256, padding=True, return_tensors="pt").to(DEVICE)
            p = torch.softmax(self.mod(**enc).logits.float(), -1).cpu().numpy()
            out.append(p[:, self.order])
        return np.vstack(out) if out else np.zeros((0, 3))


def _label_order(name):
    cfg = AutoModelForSequenceClassification.from_pretrained(name).config
    lab = {v.lower(): int(k) for k, v in cfg.id2label.items()}
    return [lab["negative"], lab["neutral"], lab["positive"]]


def cached(model_key: str, texts: list[str], fn) -> np.ndarray:
    path = CACHE / f"sent_{model_key}.parquet"
    cache = pd.read_parquet(path) if path.exists() else pd.DataFrame(columns=["h", "neg", "neu", "pos"])
    known = dict(zip(cache.h, cache[["neg", "neu", "pos"]].values))
    hs = [sha256(t) for t in texts]
    todo = sorted({h: t for h, t in zip(hs, texts) if h not in known}.items())
    if todo:
        P = fn([t for _, t in todo])
        new = pd.DataFrame({"h": [h for h, _ in todo], "neg": P[:, 0], "neu": P[:, 1], "pos": P[:, 2]})
        cache = pd.concat([cache, new], ignore_index=True)
        cache.to_parquet(path, index=False)
        known.update(dict(zip(new.h, new[["neg", "neu", "pos"]].values)))
    return np.array([known[h] for h in hs], dtype=float)


_models = {}


def get(key):
    if key not in _models:
        if key == "xlmr":
            _models[key] = HF3(MODELS["xlmr"], _label_order(MODELS["xlmr"]))
        elif key == "indo":
            _models[key] = HF3(MODELS["indo"], _label_order(MODELS["indo"]))
        elif key == "zeroshot":
            _models[key] = pipeline("zero-shot-classification", model=MODELS["zeroshot"], device=DEVICE)
    return _models[key]


def zeroshot_probs(texts):
    zs = get("zeroshot")
    labels = ["negative", "neutral", "positive"]
    out = []
    for i in range(0, len(texts), 16):
        res = zs([t[:1000] for t in texts[i:i + 16]], candidate_labels=labels,
                 hypothesis_template="The sentiment of this text is {}.", multi_label=False)
        for r in res:
            d = dict(zip(r["labels"], r["scores"]))
            out.append([d["negative"], d["neutral"], d["positive"]])
    return np.array(out)


def score(df: pd.DataFrame, candidates=("lexicon", "xlmr", "xlmr_id")) -> pd.DataFrame:
    """Adds sent_{cand}, sent_{cand}_conf and prob columns for each candidate."""
    texts = df.text_model.fillna("").tolist()
    langs = df.text_language.fillna("und").tolist()
    out = pd.DataFrame(index=df.index)
    P = {}
    if "lexicon" in candidates:
        P["lexicon"] = np.array([lexicon_probs(t, l) for t, l in zip(texts, langs)])
    if "xlmr" in candidates or "xlmr_id" in candidates:
        P["xlmr"] = cached("xlmr", texts, lambda ts: get("xlmr").probs(ts))
    if "xlmr_id" in candidates:
        P["xlmr_id"] = P["xlmr"].copy()
        idx = [i for i, l in enumerate(langs) if l in ("id", "ms")]
        if idx:
            P["xlmr_id"][idx] = cached("indo", [texts[i] for i in idx], lambda ts: get("indo").probs(ts))
    if "zeroshot" in candidates:
        P["zeroshot"] = cached("zeroshot", texts, zeroshot_probs)
    for k, p in P.items():
        labs = [to5(x) for x in p]
        out[f"sent_{k}"] = [l for l, _ in labs]
        out[f"sent_{k}_conf"] = [round(c, 3) for _, c in labs]
        out[f"p_{k}_neg"], out[f"p_{k}_neu"], out[f"p_{k}_pos"] = p[:, 0].round(4), p[:, 1].round(4), p[:, 2].round(4)
    return out


def model_versions():
    return {k: v for k, v in MODELS.items()} | {"lexicon": "vaderSentiment 3.3.2 + custom Indonesian lexicon v1",
                                                 "mixed_threshold": MIXED_T, "ambiguous_threshold": AMBIG_T}
