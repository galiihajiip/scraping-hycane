"""Evidence-based persona clustering over discourse profiles (09_CUSTOMER_PERSONA.md).

Unit of analysis: a customer-voice record (core scope, not news/promo) with >= 2 informative discourse features.
Authors rarely post more than once in the corpus, so personas are *discourse profiles*, not demographic people.
No age, gender, income or other sensitive attribute is inferred.

Features (binary): experience level, primary intent, pain points, feature mentions, price signals,
sustainability signal, kit/brand ownership, small-space context, tech-attitude aspects, contradiction flags.
Model selection: KMeans k=2..8 on TF-IDF-weighted binary features (cosine geometry via L2 normalisation),
silhouette + bootstrap stability (mean ARI over 20 resamples) + Ward agreement; robustness on a
platform-balanced sample and with the dominant platform removed.
"""
from __future__ import annotations

import json

import numpy as np
import pandas as pd
from sklearn.cluster import AgglomerativeClustering, KMeans
from sklearn.metrics import adjusted_rand_score, silhouette_score
from sklearn.preprocessing import normalize

from src.utils.common import ROOT

OUT = ROOT / "outputs" / "tables"


def features(g: pd.DataFrame) -> pd.DataFrame:
    F = pd.DataFrame(index=g.index)
    for e in ["NEVER_TRIED", "BEGINNER", "INTERMEDIATE", "EXPERIENCED", "PROFESSIONAL_COMMERCIAL"]:
        F[f"exp:{e}"] = (g.author_experience_signal == e).astype(int)
    for i in ["EXPLICIT_PURCHASE_INTENT", "PURCHASE_EXPLORATION", "COMPARISON", "PROBLEM_SOLVING", "POST_PURCHASE",
              "RECOMMENDATION", "ABANDONMENT_FRUSTRATION", "INSPIRATION", "INFORMATION_SEEKING"]:
        F[f"intent:{i}"] = g.intents.fillna("").str.split("|").map(lambda L: i in L).astype(int)
    for col, pre in [("pain_points", "pain"), ("feature_mentions", "feat"), ("price_signal", "price"),
                     ("contradiction_flags", "contra")]:
        d = g[col].fillna("").str.get_dummies("|")
        d = d[[c for c in d.columns if c.strip()]]  # empty string = absence, not a feature
        d.columns = [f"{pre}:{c}" for c in d.columns]
        F = F.join(d)
    F["sust:any"] = g.sustainability_signal.isin(["POSITIVE", "SKEPTICAL", "NEGATIVE"]).astype(int)
    asp = g.aspect_labels.fillna("")
    F["ctx:kit_brand"] = asp.str.contains("hydroponic_kit").astype(int)
    F["ctx:small_space"] = g.pain_points.fillna("").str.contains("SPACE").astype(int) | \
        g.text_model.str.contains(r"(apartment|balcon|small space|kitchen counter|lahan sempit|balkon|kos\b)", case=False).astype(int)
    F["tech:sensor_automation_app"] = asp.str.contains(r"(sensors|automation|software_app|AI)").astype(int)
    F["purchase:HIGH_MEDIUM"] = g.purchase_signal.isin(["HIGH", "MEDIUM"]).astype(int)
    return F.fillna(0).astype(int)


def weight(F: pd.DataFrame) -> np.ndarray:
    idf = np.log((1 + len(F)) / (1 + F.sum(0).values)) + 1
    return normalize(F.values * idf)


def bootstrap_ari(X, k, n=20, seed=42):
    rng = np.random.default_rng(seed)
    base = KMeans(k, random_state=seed, n_init=10).fit(X)
    aris = []
    for b in range(n):
        idx = rng.choice(len(X), len(X), replace=True)
        km = KMeans(k, random_state=seed + b + 1, n_init=10).fit(X[idx])
        aris.append(adjusted_rand_score(base.predict(X), km.predict(X)))
    return float(np.mean(aris)), float(np.std(aris))


def run(g: pd.DataFrame, seed=42):
    voice = g[g.in_core_scope & (g.voice_type != "NEWS_OR_PROMO")].copy()
    F = features(voice)
    informative = F.sum(1) >= 2
    voice, F = voice[informative], F[informative]
    # drop ultra-rare features (<0.5% of records) to stabilise clusters
    keep = F.columns[F.mean() >= 0.005]
    F = F[keep]
    X = weight(F)
    sel = []
    for k in range(2, 9):
        km = KMeans(k, random_state=seed, n_init=10).fit(X)
        sil = silhouette_score(X, km.labels_, sample_size=min(6000, len(X)), random_state=0)
        ward = AgglomerativeClustering(k, linkage="ward").fit_predict(X[:6000])
        ari_ward = adjusted_rand_score(km.labels_[:6000], ward)
        stab, stab_sd = bootstrap_ari(X, k, n=12, seed=seed)
        sel.append(dict(k=k, silhouette=round(sil, 4), bootstrap_ari_mean=round(stab, 3), bootstrap_ari_sd=round(stab_sd, 3),
                        ari_vs_ward=round(ari_ward, 3), min_cluster_share=round(np.bincount(km.labels_).min() / len(X), 3)))
    sel = pd.DataFrame(sel)
    # choose: among k in 3..6 with min cluster share >= 5% and stability >= 0.6, maximise silhouette + stability
    cand = sel[(sel.k.between(3, 6)) & (sel.min_cluster_share >= 0.05) & (sel.bootstrap_ari_mean >= 0.6)]
    if cand.empty:
        cand = sel[sel.k.between(3, 6)]
    k = int(cand.assign(score=cand.silhouette.rank() + cand.bootstrap_ari_mean.rank()).sort_values(
        ["score", "silhouette"], ascending=False).iloc[0].k)
    km = KMeans(k, random_state=seed, n_init=20).fit(X)
    voice["persona_cluster"] = km.labels_
    d = km.transform(X)
    srt = np.sort(d, 1)
    voice["persona_confidence"] = np.round(1 - srt[:, 0] / (srt[:, 1] + 1e-9), 3)
    # ---- robustness: platform-balanced sample and dominant-platform removal
    rng = np.random.default_rng(seed)
    dom = voice.platform.value_counts().index[0]
    cap = int(voice.platform.value_counts().median())
    bal_idx = np.concatenate([rng.choice(np.where(voice.platform.values == p)[0],
                                         min(cap, (voice.platform == p).sum()), replace=False)
                              for p in voice.platform.unique()])
    km_bal = KMeans(k, random_state=seed, n_init=10).fit(X[bal_idx])
    nd = np.where(voice.platform.values != dom)[0]
    km_nd = KMeans(k, random_state=seed, n_init=10).fit(X[nd]) if len(nd) > k * 20 else None
    robust = dict(dominant_platform=dom, ari_platform_balanced=round(adjusted_rand_score(km.labels_[bal_idx], km_bal.labels_), 3),
                  ari_without_dominant=round(adjusted_rand_score(km.labels_[nd], km_nd.labels_), 3) if km_nd else None,
                  n_balanced=int(len(bal_idx)), n_without_dominant=int(len(nd)))
    # ---- profile: lift of each feature within cluster vs overall
    prof = []
    base = F.mean()
    for c in range(k):
        m = voice.persona_cluster.values == c
        rate = F[m].mean()
        lift = (rate / base.replace(0, np.nan)).fillna(0)
        top = rate[(rate >= 0.08)].index
        top = sorted(top, key=lambda f: -lift[f])[:14]
        sub = voice[m]
        prof.append(dict(
            persona_cluster=c, n=int(m.sum()), share=round(m.mean(), 4),
            platforms=sub.platform.value_counts().to_dict(), languages=sub.text_language.value_counts().head(4).to_dict(),
            date_min=str(sub.created_at.min())[:10], date_max=str(sub.created_at.max())[:10],
            mean_confidence=round(sub.persona_confidence.mean(), 3),
            defining_features={f: dict(rate=round(rate[f], 3), lift=round(lift[f], 2)) for f in top},
            experience=sub.author_experience_signal.value_counts(normalize=True).round(3).head(4).to_dict(),
            intents=sub.intent.value_counts(normalize=True).round(3).head(5).to_dict(),
            pains=sub.pain_points.str.split("|").explode().replace("", np.nan).dropna().value_counts().head(6).to_dict(),
            features=sub.feature_mentions.str.split("|").explode().replace("", np.nan).dropna().value_counts().head(6).to_dict(),
            explicit_features=sub.feature_explicit.str.split("|").explode().replace("", np.nan).dropna().value_counts().head(6).to_dict(),
            price=sub.price_signal.str.split("|").explode().replace("", np.nan).dropna().value_counts().head(5).to_dict(),
            purchase_high_medium=int(sub.purchase_signal.isin(["HIGH", "MEDIUM"]).sum()),
            sentiment=sub.sentiment.value_counts(normalize=True).round(3).to_dict(),
            contradictions=sub.contradiction_flags.str.split("|").explode().replace("", np.nan).dropna().value_counts().head(5).to_dict(),
            example_record_ids="|".join(sub.sort_values("persona_confidence", ascending=False).record_id.head(12))))
    return voice, F, sel, k, pd.DataFrame(prof), robust


def main():
    g = pd.read_parquet(ROOT / "data" / "gold" / "_gold_nlp.parquet")
    voice, F, sel, k, prof, robust = run(g)
    sel.to_csv(OUT / "persona_model_selection.csv", index=False)
    prof.to_json(OUT / "persona_profiles.json", orient="records", indent=1, force_ascii=False)
    voice[["record_id", "persona_cluster", "persona_confidence"]].to_parquet(
        ROOT / "data" / "gold" / "_persona_assignments.parquet", index=False)
    (OUT / "persona_robustness.json").write_text(json.dumps(robust | {"k": k, "n": int(len(voice)),
                                                                       "n_features": int(F.shape[1])}, indent=1))
    print(sel.to_string())
    print("k =", k, robust)
    for _, r in prof.iterrows():
        print(r.persona_cluster, r.n, r.share, list(r.defining_features)[:8])


if __name__ == "__main__":
    main()
