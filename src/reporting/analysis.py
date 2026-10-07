"""Assemble final GOLD and compute every analysis table in outputs/tables/.

Denominators: unless stated otherwise, proportions use the CORE customer-voice set:
gold records, in_core_scope (cannabis-context excluded), voice_type != NEWS_OR_PROMO.
"""
from __future__ import annotations

import json
import re

import numpy as np
import pandas as pd
import yaml
from scipy.stats import chi2_contingency, spearmanr

from src.utils.common import ROOT

T = ROOT / "outputs" / "tables"
G = ROOT / "data" / "gold"
MAP = yaml.safe_load(open(ROOT / "config" / "hycane_mapping.yaml"))
PAIN_CODES = list(MAP["pain_map"])
FEATURES = list(MAP["feature_component"])


def explode(s: pd.Series) -> pd.Series:
    return s.fillna("").str.split("|").explode().replace("", np.nan).dropna()


def cramers_v(ct: pd.DataFrame):
    chi2, p, dof, _ = chi2_contingency(ct)
    n = ct.values.sum()
    v = np.sqrt(chi2 / (n * (min(ct.shape) - 1)))
    return dict(chi2=round(chi2, 2), p_value=float(f"{p:.3g}"), dof=int(dof), cramers_v=round(v, 3), n=int(n))


def assemble():
    g = pd.read_parquet(G / "_gold_nlp.parquet")
    pa = G / "_persona_assignments.parquet"
    ta = G / "_topic_assignments.parquet"
    if pa.exists():
        g = g.merge(pd.read_parquet(pa), on="record_id", how="left")
    if ta.exists():
        g = g.merge(pd.read_parquet(ta), on="record_id", how="left")
    sn = ROOT / "config" / "synthesis_notes.yaml"
    labels = (yaml.safe_load(open(sn)) or {}).get("topic_labels", {}) if sn.exists() else {}
    auto = pd.read_csv(T / "topic_summary_auto.csv") if (T / "topic_summary_auto.csv").exists() else pd.DataFrame()
    autolab = dict(zip(auto.topic_id, auto.auto_label)) if len(auto) else {}
    g["topic_label"] = g.topic_id.map(lambda t: (labels.get(int(t)) or {}).get("label") if pd.notna(t) and isinstance(labels.get(int(t)), dict)
                                      else (autolab.get(int(t)) if pd.notna(t) else None))
    g["topic_confidence"] = np.nan
    g["is_customer_voice"] = g.in_core_scope & (g.voice_type != "NEWS_OR_PROMO")
    # pain severity per primary pain; evidence strength placeholder (computed at finding level)
    g["pain_point"] = g.pain_points.fillna("").str.split("|").str[0]
    g["pain_point_severity"] = g.max_pain_severity
    g["pain_point_confidence"] = np.where(g.pain_points.fillna("") != "", "rule_match", "")
    g["intent_confidence"] = np.where(g.intent == "UNKNOWN", 0.0, np.where(g.intents.str.count(r"\|") == 0, 0.8, 0.6))
    g["feature_demand"] = np.where(g.feature_explicit.fillna("") != "", "EXPLICIT_REQUEST",
                                   np.where(g.feature_mentions.fillna("") != "", "MENTION", ""))
    g["feature_confidence"] = np.where(g.feature_demand == "EXPLICIT_REQUEST", 0.7, np.where(g.feature_demand == "MENTION", 0.5, np.nan))
    g["persona_confidence"] = g.get("persona_confidence")
    g["country"] = None
    g["region"] = None
    g["geo_source"] = None
    g["geo_confidence"] = None
    # explicit, source-context geography only
    sub_geo = {"indonesia": "ID", "malaysia": "MY", "singapore": "SG", "philippines": "PH"}
    comm = g.community.fillna("").str.lower()
    m = comm.isin(sub_geo)
    g.loc[m, "country"] = comm[m].map(sub_geo)
    g.loc[m, "geo_source"] = "community_context"
    g.loc[m, "geo_confidence"] = "medium"
    selfrep = g.text_model.str.extract(
        r"(?i)\b(?:i live in|i'?m (?:in|from)|here in|living in|saya (?:tinggal )?di|aku di|domisili)\s+([A-Z][a-zA-Z]+(?: [A-Z][a-zA-Z]+)?)")[0]
    g["self_reported_place"] = selfrep
    g.loc[selfrep.notna() & g.geo_source.isna(), "geo_source"] = "explicit_self_report"
    g.loc[selfrep.notna() & g.geo_confidence.isna(), "geo_confidence"] = "low"
    g["evidence_strength"] = None
    g["text_clean"] = g.text_clean
    return g


SCHEMA_COLS = ["record_id", "source_family", "platform", "source_type", "record_type", "source_url", "source_id",
               "parent_id", "thread_id", "thread_title", "community", "query_id", "all_query_ids", "collection_run_id",
               "created_at", "collected_at", "text_raw", "text_clean", "text_model", "text_language",
               "language_confidence", "author_id_hash", "author_public_profile_location", "author_experience_signal",
               "country", "region", "geo_source", "geo_confidence", "self_reported_place", "likes", "replies", "shares",
               "views", "rating", "is_reply", "is_repost", "is_quote", "is_cross_post", "spam_probability",
               "spam_reason_codes", "relevance_score", "relevance_basis", "duplicate_cluster_id", "duplicate_status",
               "n_captures", "cannabis_context", "in_core_scope", "voice_type", "is_customer_voice", "sentiment",
               "sentiment_confidence", "sentiment_model", "sentiment_label_source", "sent_lexicon", "sent_xlmr",
               "sent_xlmr_id", "aspect_labels", "aspect_sentiment", "topic_id", "topic_label", "nmf_topic",
               "pain_point", "pain_points", "pain_severity", "pain_point_severity", "pain_point_confidence", "intent",
               "intents", "intent_confidence", "feature_mentions", "feature_explicit", "feature_demand",
               "feature_confidence", "purchase_signal", "price_signal", "sustainability_signal",
               "contradiction_flags", "persona_cluster", "persona_confidence", "evidence_type", "evidence_strength",
               "urls", "mentions", "hashtags", "emoji_count", "raw_capture_path", "provenance_hash", "access_method"]


def save_gold(g):
    cols = [c for c in SCHEMA_COLS if c in g.columns]
    out = g[cols].copy()
    out.to_parquet(G / "hycane_social_listening_gold.parquet", index=False)
    out.to_csv(G / "hycane_social_listening_gold.csv", index=False)
    out.to_json(G / "hycane_social_listening_gold.jsonl", orient="records", lines=True, force_ascii=False)
    return out


def tables(g: pd.DataFrame):
    T.mkdir(parents=True, exist_ok=True)
    b = pd.read_parquet(ROOT / "data" / "bronze" / "all_bronze.parquet", columns=["platform", "source_family", "record_id"])
    s = pd.read_parquet(ROOT / "data" / "silver" / "silver.parquet",
                        columns=["platform", "record_id", "is_relevant", "exclusion_meaning", "is_spam",
                                 "duplicate_status", "duplicate_reason", "n_chars", "created_at", "text_language",
                                 "language_confidence", "cannabis_context", "spam_reason_codes", "relevance_basis"])
    v = g[g.is_customer_voice]
    res = {}
    tf = f"{str(v.created_at.min())[:10]} to {str(v.created_at.max())[:10]}"
    res["timeframe_customer_voice"] = tf
    # ---------------- coverage
    cov = pd.DataFrame({
        "raw_bronze_rows": b.groupby("platform").size(),
        "unique_source_objects": s.groupby("platform").size(),
        "relevant": s[s.is_relevant].groupby("platform").size(),
        "gold_records": g.groupby("platform").size(),
        "gold_core_scope": g[g.in_core_scope].groupby("platform").size(),
        "customer_voice_core": v.groupby("platform").size(),
        "threads_customer_voice": v.groupby("platform").thread_id.nunique(),
        "date_min": g.groupby("platform").created_at.min().str[:10],
        "date_max": g.groupby("platform").created_at.max().str[:10],
        "pct_indonesian": g.groupby("platform").text_language.apply(lambda x: round((x == "id").mean() * 100, 2)),
    }).fillna(0)
    fam = g.groupby("platform").source_family.first()
    cov.insert(0, "source_family", fam)
    cov = cov.reset_index().rename(columns={"index": "platform"})
    cov.to_csv(T / "platform_coverage.csv", index=False)
    g.groupby(["source_family"]).agg(gold=("record_id", "size"), customer_voice=("is_customer_voice", "sum")).reset_index().to_csv(
        T / "source_family_coverage.csv", index=False)
    # ---------------- data quality
    dq = dict(bronze_rows=len(b), unique_source_objects=len(s),
              source_id_duplicate_rate=round(1 - len(s) / len(b), 4),
              irrelevant_rate=round((~s.is_relevant).mean(), 4),
              unrelated_meaning_excluded=int((s.exclusion_meaning != "").sum()),
              spam_rate_among_relevant=round(s[s.is_relevant].is_spam.mean(), 4),
              text_duplicate_rate_among_relevant=round((s[s.is_relevant].duplicate_status != "canonical").mean(), 4),
              semantic_duplicates=int(len(pd.read_csv(ROOT / "data" / "manifests" / "semantic_duplicates.csv")))
              if (ROOT / "data" / "manifests" / "semantic_duplicates.csv").exists() else None,
              cannabis_context_share_of_gold=round(g.cannabis_context.mean(), 4),
              news_or_promo_share_of_core=round((g[g.in_core_scope].voice_type == "NEWS_OR_PROMO").mean(), 4),
              missing_timestamp_rate_gold=round(g.created_at.isna().mean(), 4),
              mean_language_confidence_gold=round(g.language_confidence.mean(), 3),
              low_language_confidence_share=round((g.language_confidence < 0.5).mean(), 4),
              geo_known_rate_gold=round(g.geo_source.notna().mean(), 4),
              gold_records=len(g), gold_core_scope=int(g.in_core_scope.sum()), customer_voice_core=len(v))
    led = pd.read_csv(ROOT / "data" / "logs" / "request_ledger.csv")
    dq["requests_logged"] = len(led)
    dq["request_error_rate"] = round((led.status != "SUCCESS").mean(), 4)
    dq["requests_with_retries_share"] = round((led.retries.fillna(0) > 0).mean(), 4)
    res["data_quality"] = dq
    pd.Series(dq).rename_axis("metric").reset_index(name="value").to_csv(T / "data_quality_metrics.csv", index=False)
    miss = pd.DataFrame({"missing_n": g.isna().sum() + (g == "").sum(), "missing_pct": ((g.isna().sum() + (g == "").sum()) / len(g) * 100).round(2)})
    miss.rename_axis("field").reset_index().to_csv(T / "missingness.csv", index=False)
    s[s.spam_reason_codes != ""].spam_reason_codes.str.split("|").explode().value_counts().rename_axis(
        "spam_reason").reset_index(name="n").to_csv(T / "spam_reason_codes.csv", index=False)
    # ---------------- language / timeline / threads
    g.groupby(["text_language"]).agg(gold=("record_id", "size"), customer_voice=("is_customer_voice", "sum"),
                                     mean_conf=("language_confidence", "mean")).sort_values("gold", ascending=False).round(3).reset_index().to_csv(
        T / "language_distribution.csv", index=False)
    tl = v.assign(month=v.created_at.str[:7]).groupby(["month", "platform"]).size().unstack(fill_value=0)
    tl.to_csv(T / "timeline_monthly.csv")
    th = v.groupby(["platform", "thread_id"]).size().sort_values(ascending=False)
    thd = th.head(30).rename("n").reset_index()
    thd["share_of_customer_voice"] = (thd.n / len(v)).round(4)
    thd.to_csv(T / "thread_dominance_top30.csv", index=False)
    res["max_thread_share"] = float(thd.share_of_customer_voice.max())
    # ---------------- geography (explicit only)
    geo = g[g.geo_source.notna()].groupby(["geo_source"]).size().rename("n").reset_index()
    geo.to_csv(T / "geography_explicit_sources.csv", index=False)
    g[g.country.notna()].groupby("country").size().rename("n").reset_index().to_csv(T / "geography_country_context.csv", index=False)
    # ---------------- sentiment
    sent_overall = v.sentiment.value_counts().rename("n").to_frame()
    sent_overall["pct"] = (sent_overall.n / len(v) * 100).round(2)
    sent_overall.rename_axis("sentiment").reset_index().assign(denominator=len(v), scope="customer_voice_core").to_csv(
        T / "sentiment_summary.csv", index=False)
    sp = pd.crosstab(v.platform, v.sentiment)
    (sp.div(sp.sum(axis=1), axis=0) * 100).round(2).assign(n=sp.sum(axis=1)).to_csv(T / "sentiment_by_platform.csv")
    res["sentiment_platform_test"] = cramers_v(sp.loc[:, (sp.sum(axis=0) > 0)])
    sl = pd.crosstab(v.text_language.where(v.text_language.isin(["en", "id"]), "other"), v.sentiment)
    (sl.div(sl.sum(axis=1), axis=0) * 100).round(2).assign(n=sl.sum(axis=1)).to_csv(T / "sentiment_by_language.csv")
    if "topic_label" in v and v.topic_label.notna().any():
        st = pd.crosstab(v.topic_label, v.sentiment)
        (st.div(st.sum(axis=1), axis=0) * 100).round(2).assign(n=st.sum(axis=1)).sort_values("n", ascending=False).to_csv(
            T / "sentiment_by_topic.csv")
    # sentiment robustness subsets
    rob = {}
    subsets = {
        "customer_voice_core": v,
        "high_confidence_only(>=0.7)": v[v.sentiment_confidence >= 0.7],
        "include_cannabis_context": g[g.voice_type != "NEWS_OR_PROMO"],
        "include_news_promo": g[g.in_core_scope],
        "exclude_dominant_platform": v[v.platform != v.platform.value_counts().index[0]],
        "comments_only": v[v.record_type == "comment_record"],
        "posts_only": v[v.record_type == "post_record"],
    }
    for name, d in subsets.items():
        vc = d.sentiment.value_counts(normalize=True).mul(100).round(2)
        rob[name] = vc.to_dict() | {"n": len(d)}
    # thread-normalised: weight each record 1/(records in its thread)
    w = 1 / v.groupby("thread_id").record_id.transform("size")
    rob["thread_normalised(weighted)"] = (w.groupby(v.sentiment).sum() / w.sum() * 100).round(2).to_dict() | {"n": len(v)}
    pd.DataFrame(rob).T.to_csv(T / "sentiment_sensitivity.csv")
    # model agreement
    agr = {f"{a}_vs_{b}": round((v[f"sent_{a}"] == v[f"sent_{b}"]).mean(), 4) for a, b in
           [("xlmr", "xlmr_id"), ("xlmr", "lexicon"), ("xlmr_id", "lexicon")]}
    res["sentiment_model_agreement"] = agr
    # aspect sentiment
    asp = pd.read_parquet(G / "aspect_sentiment.parquet")
    asp = asp[asp.record_id.isin(v.record_id)]
    at = pd.crosstab(asp.aspect, asp.aspect_sentiment)
    (at.div(at.sum(axis=1), axis=0) * 100).round(2).assign(n=at.sum(axis=1)).sort_values("n", ascending=False).to_csv(
        T / "aspect_sentiment_summary.csv")
    # ---------------- pain points
    vp = v.assign(pain=v.pain_points.fillna("").str.split("|")).explode("pain").reset_index(drop=True)
    vp = vp[vp.pain != ""]
    sev = v.pain_severity.fillna("").str.split("|").explode().dropna()
    sev = sev[sev != ""].str.split(":", expand=True)
    sev_mean = sev.assign(s=sev[1].astype(int)).groupby(0).s.mean() if len(sev) else pd.Series(dtype=float)
    n_plat = v.platform.nunique()
    months_total = v.created_at.str[:7].nunique()
    rows = []
    pers = v.persona_cluster.notna()
    for code in PAIN_CODES:
        d = vp[vp.pain == code]
        if d.empty:
            rows.append(dict(pain_point=code, count=0))
            continue
        per_plat = d.platform.value_counts()
        pc = d.persona_cluster.dropna().value_counts(normalize=True)
        rows.append(dict(
            pain_point=code, count=len(d), corpus_share=round(len(d) / len(v), 4), denominator=len(v),
            unique_threads=d.thread_id.nunique(), unique_thread_share=round(d.thread_id.nunique() / v.thread_id.nunique(), 4),
            platforms_with_3plus=int((per_plat >= 3).sum()), platform_breadth=round((per_plat >= 3).sum() / n_plat, 3),
            recurrence_months=d.created_at.str[:7].nunique(), recurrence=round(d.created_at.str[:7].nunique() / months_total, 3),
            negative_share=round((d.sentiment == "NEGATIVE").mean(), 3), mean_severity=round(sev_mean.get(code, np.nan), 2),
            explicitness=round(d.intent.isin(["PROBLEM_SOLVING", "ABANDONMENT_FRUSTRATION"]).mean() +
                               0 * 1, 3),
            first_person_share=round((d.voice_type.isin(["PERSONAL_EXPERIENCE", "QUESTION"])).mean(), 3),
            abandonment_cooccurrence=int((d.intents.fillna("").str.contains("ABANDONMENT_FRUSTRATION")).sum()),
            persona_concentration=round(pc.max(), 3) if len(pc) else np.nan,
            top_persona=int(pc.idxmax()) if len(pc) else None,
            hycane_relevance=MAP["pain_map"][code]["relevance"],
            indonesian_count=int((d.text_language == "id").sum()),
            example_record_ids="|".join(d.sort_values("max_pain_severity", ascending=False).record_id.head(8))))
    pp = pd.DataFrame(rows).fillna({"count": 0})
    pp = pp[pp["count"] > 0].copy()

    def norm(x):
        x = x.astype(float)
        return (x - x.min()) / (x.max() - x.min() + 1e-9) * 0.9 + 0.1  # keep in [0.1,1] for multiplicative scheme

    comp = pd.DataFrame({
        "F": norm(np.log1p(pp["count"])), "S": norm(pp.mean_severity.fillna(pp.mean_severity.mean()) + 2 * pp.negative_share),
        "R": norm(pp.recurrence), "B": norm(pp.platform_breadth), "Rel": pp.hycane_relevance.clip(0.1, 1)})
    W_A = dict(F=1, S=1, R=1, B=1, Rel=1)          # scheme A: multiplicative, equal exponents
    W_B = dict(F=0.30, S=0.25, R=0.10, B=0.15, Rel=0.20)  # scheme B: additive weighted
    pp["priority_A_multiplicative"] = np.prod([comp[k] ** w for k, w in W_A.items()], axis=0).round(4)
    pp["priority_B_weighted_additive"] = sum(comp[k] * w for k, w in W_B.items()).round(4)
    pp["priority_C_customer_only(no relevance)"] = np.prod([comp[k] for k in ["F", "S", "R", "B"]], axis=0).round(4)
    for c in ["priority_A_multiplicative", "priority_B_weighted_additive", "priority_C_customer_only(no relevance)"]:
        pp[f"rank_{c.split('_')[1]}"] = pp[c].rank(ascending=False).astype(int)
    pp = pp.sort_values("priority_A_multiplicative", ascending=False)
    pp.to_csv(T / "pain_point_summary.csv", index=False)
    comp.assign(pain_point=pp.pain_point.values if False else pp.sort_index().pain_point.values).to_csv(
        T / "pain_point_priority_components.csv", index=False)
    json.dump(dict(scheme_A=W_A, scheme_B=W_B, scheme_C="F*S*R*B (relevance removed)",
                   normalisation="min-max to [0.1,1]; F uses log1p(count); S = mean rule severity + 2*negative share"),
              open(T / "pain_point_priority_weights.json", "w"), indent=1)
    res["pain_rank_spearman_A_vs_B"] = round(spearmanr(pp.rank_A, pp.rank_B).correlation, 3)
    res["pain_rank_spearman_A_vs_C"] = round(spearmanr(pp.rank_A, pp["rank_C"]).correlation, 3)
    # pain frequency sensitivity across subsets
    sens = {}
    for name, d in {**subsets, "thread_normalised(weighted)": v}.items():
        if name == "thread_normalised(weighted)":
            ww = 1 / v.groupby("thread_id").record_id.transform("size")
            e = v.assign(w=ww, pain=v.pain_points.fillna("").str.split("|")).explode("pain")
            e = e[e.pain != ""]
            sens[name] = (e.groupby("pain").w.sum() / ww.sum() * 100).round(2)
        else:
            sens[name] = (explode(d.pain_points).value_counts() / max(1, len(d)) * 100).round(2)
    sens = pd.DataFrame(sens).fillna(0)
    sens.to_csv(T / "pain_point_sensitivity_pct.csv")
    ranks = sens.rank(ascending=False)
    res["pain_top5_by_subset"] = {c: list(sens[c].sort_values(ascending=False).index[:5]) for c in sens.columns}
    res["pain_rank_min_spearman_vs_core"] = round(min(spearmanr(ranks["customer_voice_core"], ranks[c]).correlation
                                                     for c in ranks.columns if c != "customer_voice_core"), 3)
    # beginner vs experienced pains
    be = v[v.author_experience_signal.isin(["NEVER_TRIED", "BEGINNER"])]
    ex = v[v.author_experience_signal.isin(["INTERMEDIATE", "EXPERIENCED", "PROFESSIONAL_COMMERCIAL"])]
    bx = pd.DataFrame({"beginner_or_never_pct": explode(be.pain_points).value_counts() / max(1, len(be)) * 100,
                       "experienced_pct": explode(ex.pain_points).value_counts() / max(1, len(ex)) * 100}).fillna(0).round(2)
    bx["diff_pp"] = (bx.beginner_or_never_pct - bx.experienced_pct).round(2)
    bx.attrs["n"] = (len(be), len(ex))
    bx.sort_values("diff_pp", ascending=False).to_csv(T / "pain_beginner_vs_experienced.csv")
    res["n_beginner_or_never"], res["n_experienced"] = len(be), len(ex)
    # Indonesia vs global
    idn = v[v.text_language == "id"]
    glob = v[v.text_language != "id"]
    ig = pd.DataFrame({"indonesian_pct": explode(idn.pain_points).value_counts() / max(1, len(idn)) * 100,
                       "non_indonesian_pct": explode(glob.pain_points).value_counts() / max(1, len(glob)) * 100}).fillna(0).round(2)
    ig.to_csv(T / "pain_indonesian_vs_global.csv")
    res["n_indonesian_voice"], res["n_non_indonesian_voice"] = len(idn), len(glob)
    # ---------------- intent
    it = v.intent.value_counts().rename("n_primary").to_frame()
    it["pct_primary"] = (it.n_primary / len(v) * 100).round(2)
    it["n_any_label"] = explode(v.intents).value_counts()
    it.rename_axis("intent").reset_index().assign(denominator=len(v)).to_csv(T / "intent_summary.csv", index=False)
    ip = pd.crosstab(v.platform, v.intent)
    (ip.div(ip.sum(axis=1), axis=0) * 100).round(2).assign(n=ip.sum(axis=1)).to_csv(T / "intent_by_platform.csv")
    res["intent_platform_test"] = cramers_v(ip)
    funnel = ["AWARENESS", "INSPIRATION", "INFORMATION_SEEKING", "PROBLEM_SOLVING", "COMPARISON",
              "PURCHASE_EXPLORATION", "EXPLICIT_PURCHASE_INTENT", "POST_PURCHASE", "RECOMMENDATION", "ABANDONMENT_FRUSTRATION"]
    pd.Series({k: int(v.intents.fillna("").str.contains(k).sum()) for k in funnel}).rename_axis("stage").reset_index(
        name="n_records_any_label").to_csv(T / "intent_funnel.csv", index=False)
    # purchase / price
    pd.crosstab(v.purchase_signal, v.platform, margins=True).to_csv(T / "purchase_signal_by_platform.csv")
    pr = explode(v.price_signal).value_counts().rename("n").rename_axis("price_signal").reset_index()
    pr["pct_of_voice"] = (pr.n / len(v) * 100).round(2)
    pr.assign(denominator=len(v)).to_csv(T / "price_signal_summary.csv", index=False)
    num = v[v.price_signal.fillna("").str.contains("NUMERIC_PRICE")]
    amt = num.text_model.str.extractall(r"(?i)(\$\s?\d[\d,.]*|rp\.?\s?\d[\d.,]*|\d+\s?(?:ribu|rb|juta|jt)\b|\d+\s?(?:usd|dollars|bucks))")[0]
    amt = amt.reset_index().merge(num[["record_id", "platform", "text_language", "intent", "aspect_labels"]].reset_index(),
                                  left_on="level_0", right_on="index")
    amt.rename(columns={0: "price_mention"})[["record_id", "platform", "text_language", "intent", "price_mention", "aspect_labels"]].to_csv(
        T / "price_mentions_extracted.csv", index=False)
    # ---------------- sustainability / bagasse
    sus = v.sustainability_signal.value_counts().rename("n").rename_axis("sustainability_signal").reset_index()
    sus["pct"] = (sus.n / len(v) * 100).round(2)
    sus.assign(denominator=len(v)).to_csv(T / "sustainability_signal_summary.csv", index=False)
    sb = pd.read_parquet(ROOT / "data" / "silver" / "silver.parquet",
                         columns=["record_id", "platform", "text_language", "bagasse_mention", "bagasse_media_context",
                                  "cannabis_context", "duplicate_status", "is_spam", "text_model"])
    sb = sb[sb.bagasse_mention & (sb.duplicate_status == "canonical") & ~sb.is_spam]
    BCTX = {"tableware_packaging": r"(plate|bowl|tableware|packaging|container|cup|straw|piring|kemasan)",
            "energy_fuel": r"(boiler|power|electric|energy|fuel|ethanol|biomass|pellet|btu|listrik)",
            "paper_board": r"(paper|board|plywood|kertas|papan)",
            "growing_media_or_compost": r"(media tanam|growing (media|medium)|substrate|hidroponi|hydroponi|seedling|semai|compost|kompos|pupuk|potting|tanam)",
            "animal_feed_mushroom": r"(feed|pakan|ternak|mushroom|jamur)"}
    for k, rx in BCTX.items():
        sb[k] = sb.text_model.str.contains(rx, case=False)
    res["bagasse_discourse"] = dict(n_all_mentions=len(sb), n_growing_media_context=int(sb.bagasse_media_context.sum()),
                                    contexts={k: int(sb[k].sum()) for k in BCTX})
    res["bagasse_mentions_gold"] = int(g.text_model.str.contains(r"(?i)bagasse|ampas tebu").sum())
    res["bagasse_mentions_customer_voice"] = int(v.text_model.str.contains(r"(?i)bagasse|ampas tebu").sum())
    sb.assign(text_model=sb.text_model.str[:300]).to_csv(T / "bagasse_mentions.csv", index=False)
    media = v[v.aspect_labels.fillna("").str.contains("growing_media")]
    mt = media.text_model.str.lower()
    res["growing_media_terms"] = {k: int(mt.str.contains(rx).sum()) for k, rx in
                                  {"rockwool": r"rock ?wool", "coco": r"coco", "perlite": "perlite", "clay_pebbles": r"clay pebble|hydroton|leca",
                                   "sponge": r"sponge|spons", "peat": r"peat", "rapid_rooter": "rapid rooter",
                                   "biodegradable": "biodegrad", "bagasse": "bagasse|ampas tebu"}.items()}
    res["rockwool_negative_or_env_concern"] = int(mt[mt.str.contains("rock ?wool")].str.contains(
        r"(itch|irritat|lung|dust|mask|glove|environment|waste|landfill|not biodegrad|ph (is )?high|alkaline|soak|hate)").sum())
    # ---------------- features
    fm = explode(v.feature_mentions).value_counts()
    fx = explode(v.feature_explicit).value_counts()
    contra_map = {"ph_monitoring": "SENSOR_DISTRUST", "tds_ec_monitoring": "SENSOR_DISTRUST",
                  "remote_app_control": "APP_DISLIKE", "dashboard": "APP_DISLIKE", "alerts": "APP_DISLIKE",
                  "ai_anomaly_detection": "AI_SKEPTICISM", "recommendations": "AI_SKEPTICISM",
                  "automation_dosing": "ANTI_AUTOMATION", "biodegradable_media": "SUSTAINABILITY_SKEPTIC"}
    cf = explode(v.contradiction_flags).value_counts()
    pain_counts = pp.set_index("pain_point")["count"]
    frows = []
    for f in FEATURES:
        rel_pains = [p for p, m in MAP["pain_map"].items() if f in m["features"]]
        inferred = int(sum(pain_counts.get(p, 0) for p in rel_pains))
        breadth = v[v.feature_mentions.fillna("").str.contains(f)].platform.nunique()
        xb = v[v.feature_explicit.fillna("").str.contains(f)].platform.nunique()
        contra = int(cf.get(contra_map.get(f, "_"), 0))
        nx, nm = int(fx.get(f, 0)), int(fm.get(f, 0))
        if nx >= 10 and xb >= 2:
            cls = "EXPLICIT_REQUEST"
        elif contra >= 10 and contra > nx and inferred < 50:
            cls = "CONTRADICTORY"
        elif inferred >= 150 and len(rel_pains) >= 1:
            cls = "STRONG_INFERRED"
        elif inferred > 0 or nm > 0 or nx > 0:
            cls = "WEAK_INFERRED"
        else:
            cls = "NO_EVIDENCE"
        frows.append(dict(feature=f, hycane_component=MAP["feature_component"][f], mentions=nm, explicit_requests=nx,
                          explicit_platforms=xb, mention_platforms=breadth, related_pains="|".join(rel_pains),
                          pain_derived_count=inferred, contradiction_probe=contra_map.get(f), contradiction_count=contra,
                          demand_class=cls, mention_pct_of_voice=round(nm / len(v) * 100, 2), denominator=len(v),
                          example_explicit_ids="|".join(v[v.feature_explicit.fillna("").str.contains(f)].record_id.head(6))))
    fd = pd.DataFrame(frows).sort_values(["explicit_requests", "pain_derived_count"], ascending=False)
    fd.to_csv(T / "feature_demand.csv", index=False)
    # pain -> job -> outcome -> feature -> component -> value
    mp = pd.DataFrame([dict(pain_point=p, count=int(pain_counts.get(p, 0)), job=m["job"], desired_outcome=m["outcome"],
                            features="|".join(m["features"]), hycane_component=m["component"], business_value=m["value"],
                            hycane_relevance=m["relevance"]) for p, m in MAP["pain_map"].items()]).sort_values("count", ascending=False)
    mp.to_csv(T / "hycane_feature_mapping.csv", index=False)
    # ---------------- contradictions
    crow = []
    for code in explode(g.contradiction_flags).unique():
        d = v[v.contradiction_flags.fillna("").str.contains(code)]
        crow.append(dict(contradiction=code, n_customer_voice=len(d), pct_of_voice=round(len(d) / len(v) * 100, 3),
                         platforms=d.platform.value_counts().to_dict(), n_platforms=d.platform.nunique(),
                         negative_share=round((d.sentiment == "NEGATIVE").mean(), 3) if len(d) else None,
                         example_record_ids="|".join(d.record_id.head(10))))
    pd.DataFrame(crow).sort_values("n_customer_voice", ascending=False).to_csv(T / "contradiction_probe_counts.csv", index=False)
    # ---------------- persona x pain / feature
    if v.persona_cluster.notna().any():
        vpc = v[v.persona_cluster.notna()]
        pxp = pd.crosstab(vp.persona_cluster, vp.pain)
        (pxp.div(vpc.persona_cluster.value_counts().sort_index(), axis=0) * 100).round(2).to_csv(T / "persona_x_painpoint_pct.csv")
        vf = vpc.assign(f=vpc.feature_mentions.fillna("").str.split("|")).explode("f").reset_index(drop=True)
        vf = vf[vf.f != ""]
        pxf = pd.crosstab(vf.persona_cluster, vf.f)
        (pxf.div(vpc.persona_cluster.value_counts().sort_index(), axis=0) * 100).round(2).to_csv(T / "persona_x_feature_pct.csv")
    # platform x topic
    if v.topic_label.notna().any():
        pt = pd.crosstab(v.topic_label, v.platform)
        (pt.div(pt.sum(axis=0), axis=1) * 100).round(2).to_csv(T / "platform_x_topic_pct.csv")
    # ---------------- query yield
    qy = g.assign(q=g.query_id.fillna("none")).groupby(["platform", "q"]).agg(
        gold=("record_id", "size"), customer_voice=("is_customer_voice", "sum"),
        problem_solving=("intent", lambda x: (x == "PROBLEM_SOLVING").sum())).reset_index()
    qy.sort_values("gold", ascending=False).to_csv(T / "query_yield.csv", index=False)
    # ---------------- saturation: new topic x pain combos per 100 records in collection order
    vs = v.sort_values(["collected_at", "record_id"])
    seen, curve = set(), []
    for i, (t, p) in enumerate(zip(vs.topic_id.fillna(-9), vs.pain_points.fillna(""))):
        for c in [f"{int(t)}|{x}" for x in (p.split("|") if p else ["none"])]:
            seen.add(c)
        if (i + 1) % 100 == 0:
            curve.append(dict(records=i + 1, distinct_topic_pain_combos=len(seen)))
    sat = pd.DataFrame(curve)
    if len(sat):
        sat["new_per_100"] = sat.distinct_topic_pain_combos.diff().fillna(sat.distinct_topic_pain_combos)
        sat.to_csv(T / "saturation_curve.csv", index=False)
        res["saturation_last_10_blocks_mean_new_per_100"] = round(sat.new_per_100.tail(10).mean(), 2)
        res["saturation_first_10_blocks_mean_new_per_100"] = round(sat.new_per_100.head(10).mean(), 2)
    # experience distribution
    ex_d = v.author_experience_signal.value_counts().rename("n").rename_axis("experience").reset_index()
    ex_d["pct"] = (ex_d.n / len(v) * 100).round(2)
    ex_d.assign(denominator=len(v)).to_csv(T / "experience_distribution.csv", index=False)
    res["counts"] = dict(gold=len(g), core=int(g.in_core_scope.sum()), customer_voice=len(v),
                         platforms=sorted(g.platform.unique().tolist()), source_families=sorted(g.source_family.unique().tolist()),
                         languages_top=g.text_language.value_counts().head(8).to_dict(),
                         date_min=str(g.created_at.min())[:10], date_max=str(g.created_at.max())[:10])
    (T / "analysis_results.json").write_text(json.dumps(res, indent=1, default=str))
    return res


def main():
    g = assemble()
    save_gold(g)
    res = tables(g)
    print(json.dumps(res["counts"], indent=1))
    print("pain spearman A/B", res["pain_rank_spearman_A_vs_B"], "A/C", res["pain_rank_spearman_A_vs_C"])


if __name__ == "__main__":
    main()
