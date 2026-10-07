"""Unsupervised topic discovery on core-scope gold records.

Primary: BERTopic (multilingual MiniLM embeddings -> UMAP -> HDBSCAN -> c-TF-IDF), seeded random_state.
Fallback / robustness: TF-IDF -> NMF; agreement with BERTopic reported as NMI/ARI.
Topic labels are assigned by a researcher after reading top terms and representative records
(config/topic_labels.yaml); unlabeled topics keep their auto-generated term label.
"""
from __future__ import annotations

import re

import numpy as np
import pandas as pd
import yaml
from bertopic import BERTopic
from hdbscan import HDBSCAN
from sklearn.cluster import KMeans
from sklearn.decomposition import NMF
from sklearn.feature_extraction.text import CountVectorizer, ENGLISH_STOP_WORDS, TfidfVectorizer
from sklearn.metrics import adjusted_rand_score, normalized_mutual_info_score, silhouette_score
from umap import UMAP

from src.utils.common import ROOT

ID_STOP = {"yang", "dan", "di", "ke", "dari", "ini", "itu", "dengan", "untuk", "pada", "ada", "tidak", "juga", "saya",
           "aku", "kamu", "kita", "kami", "bisa", "akan", "sudah", "atau", "karena", "jadi", "kalau", "lagi", "aja",
           "sih", "nya", "dong", "kok", "ya", "yg", "gak", "ga", "nggak", "udah", "banget", "lebih", "seperti", "bagi",
           "oleh", "dalam", "agar", "tapi", "namun", "the", "amp", "nbsp", "https", "http", "www", "com"}
STOP = list(ENGLISH_STOP_WORDS | ID_STOP | {"just", "like", "really", "get", "got", "know", "think", "don", "ve",
                                             "ll", "im", "use", "using", "used", "make", "want", "good", "need",
                                             "thanks", "thank", "lol", "yeah", "did", "does", "doing", "going",
                                             "way", "thing", "things", "lot", "bit", "pretty", "probably", "maybe",
                                             "actually", "say", "said", "look", "looks", "looking", "sure", "try"})
LABELS_PATH = ROOT / "config" / "topic_labels.yaml"


def run(g: pd.DataFrame, E: np.ndarray, seed=42, k_grid=(20, 25, 30, 35, 40)):
    """BERTopic with KMeans clustering on UMAP space (HDBSCAN-EOM collapsed into one cluster on this corpus;
    HDBSCAN-leaf left ~50% outliers — both reported as robustness checks)."""
    docs = g.text_model.str.slice(0, 1500).tolist()
    U = UMAP(n_neighbors=15, n_components=5, min_dist=0.0, metric="cosine", random_state=seed).fit_transform(E)
    sweep = {}
    for k in k_grid:
        lab = KMeans(k, random_state=seed, n_init=5).fit_predict(U)
        sweep[k] = round(float(silhouette_score(U, lab, sample_size=min(5000, len(U)), random_state=0)), 4)
    k_best = max(sweep, key=sweep.get)
    leaf = HDBSCAN(min_cluster_size=max(30, len(U) // 300), min_samples=5, cluster_selection_method="leaf").fit_predict(U)

    class _Identity:  # BERTopic expects a fit/transform reducer; pass precomputed UMAP space
        def fit(self, X, y=None):
            return self

        def transform(self, X):
            return X

    vec = CountVectorizer(stop_words=STOP, ngram_range=(1, 2), token_pattern=r"(?u)\b[a-zA-Z][a-zA-Z]{2,}\b")
    tm = BERTopic(umap_model=_Identity(), hdbscan_model=KMeans(k_best, random_state=seed, n_init=5),
                  vectorizer_model=vec, calculate_probabilities=False, verbose=False)
    topics, _ = tm.fit_transform(docs, U)
    topics = np.array(topics)
    info = tm.get_topic_info()
    tf = TfidfVectorizer(stop_words=STOP, min_df=5, max_df=0.5, ngram_range=(1, 2),
                         token_pattern=r"(?u)\b[a-zA-Z][a-zA-Z]{2,}\b")
    X = tf.fit_transform(docs)
    nmf = NMF(n_components=k_best, random_state=seed, init="nndsvda", max_iter=400)
    nmf_topic = nmf.fit_transform(X).argmax(1)
    terms = np.array(tf.get_feature_names_out())
    nmf_terms = [", ".join(terms[np.argsort(-c)[:10]]) for c in nmf.components_]
    lm = leaf != -1
    agree = dict(k_selected=k_best, silhouette_sweep=sweep,
                 nmi_vs_nmf=round(normalized_mutual_info_score(topics, nmf_topic), 3),
                 ari_vs_nmf=round(adjusted_rand_score(topics, nmf_topic), 3),
                 hdbscan_leaf_clusters=int(leaf.max() + 1), hdbscan_leaf_outlier_share=round(float((~lm).mean()), 3),
                 nmi_vs_hdbscan_leaf_nonoutliers=round(normalized_mutual_info_score(topics[lm], leaf[lm]), 3))
    return tm, topics, info, nmf_topic, nmf_terms, agree


def summarize(g, E, topics, tm):
    labels = yaml.safe_load(LABELS_PATH.read_text()) if LABELS_PATH.exists() else {}
    rows = []
    for t in sorted(set(topics)):
        idx = np.where(topics == t)[0]
        sub = g.iloc[idx]
        terms = [w for w, _ in (tm.get_topic(t) or [])][:12] if t != -1 else []
        cen = E[idx].mean(0)
        cen /= np.linalg.norm(cen) + 1e-9
        sims = E[idx] @ cen
        rep = idx[np.argsort(-sims)[:5]]
        auto = "_".join(terms[:4]) if terms else "outliers"
        rows.append(dict(
            topic_id=int(t), topic_label=labels.get(int(t), {}).get("label", auto) if isinstance(labels.get(int(t)), dict)
            else labels.get(int(t), auto), auto_label=auto, n=len(idx), share=round(len(idx) / len(g), 4),
            top_terms=", ".join(terms), coherence_proxy_mean_cosine=round(float(sims.mean()), 3),
            platforms=sub.platform.value_counts().to_dict(),
            n_platforms=sub.platform.nunique(), n_threads=sub.thread_id.nunique(),
            sentiment=sub.sentiment.value_counts(normalize=True).round(3).to_dict(),
            pct_negative=round((sub.sentiment == "NEGATIVE").mean(), 3),
            pct_positive=round((sub.sentiment == "POSITIVE").mean(), 3),
            top_pain=sub.pain_points.str.split("|").explode().replace("", np.nan).dropna().value_counts().head(3).to_dict(),
            representative_record_ids="|".join(g.record_id.values[rep]),
            representative_snippets=" || ".join(g.text_model.values[i][:220].replace("\n", " ") for i in rep[:3])))
    return pd.DataFrame(rows).sort_values("n", ascending=False)


def main():
    import json
    g = pd.read_parquet(ROOT / "data" / "gold" / "_gold_nlp.parquet")
    E = np.load(ROOT / "data" / "cache" / "gold_embeddings.npy")
    m = g.in_core_scope.values
    gc, Ec = g[m].reset_index(drop=True), E[m]
    tm, topics, info, nmf_topic, nmf_terms, agree = run(gc, Ec)
    gc["topic_id"] = topics
    gc["nmf_topic"] = nmf_topic
    summ = summarize(gc, Ec, topics, tm)
    summ.to_csv(ROOT / "outputs" / "tables" / "topic_summary_auto.csv", index=False)
    gc[["record_id", "topic_id", "nmf_topic"]].to_parquet(ROOT / "data" / "gold" / "_topic_assignments.parquet", index=False)
    pd.DataFrame({"nmf_topic": range(len(nmf_terms)), "top_terms": nmf_terms}).to_csv(
        ROOT / "outputs" / "tables" / "topic_nmf_fallback.csv", index=False)
    (ROOT / "outputs" / "tables" / "topic_model_diagnostics.json").write_text(json.dumps(agree, indent=1))
    print(agree)
    for _, r in summ.iterrows():
        print(r.topic_id, r.n, r.n_platforms, "|", r.top_terms[:110])


if __name__ == "__main__":
    main()
