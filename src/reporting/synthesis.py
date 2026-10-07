"""INSIGHT layer: hypothesis validation, contradiction register, triangulation matrix, evidence strength,
persona summary. Verdict rules are explicit below; researcher notes come from config/synthesis_notes.yaml.
"""
from __future__ import annotations

import json
import re

import numpy as np
import pandas as pd
import yaml

from src.utils.common import ROOT

T = ROOT / "outputs" / "tables"
G = ROOT / "data" / "gold"
NOTES_P = ROOT / "config" / "synthesis_notes.yaml"


def load_notes():
    return yaml.safe_load(NOTES_P.read_text()) if NOTES_P.exists() else {}


def rx_count(v, pattern):
    m = v.text_model.str.contains(pattern, case=False, regex=True)
    return int(m.sum()), int(v[m].platform.nunique()), v[m]


def evidence_level(n, platforms_3plus):
    """Codebook E-levels for a customer signal (E4 = primary research is not available in this study)."""
    if n == 0:
        return "E0"
    if n == 1:
        return "E1"
    if platforms_3plus >= 2:
        return "E3"
    return "E2"


def main():
    notes = load_notes()
    g = pd.read_parquet(G / "hycane_social_listening_gold.parquet")
    v = g[g.is_customer_voice].copy()
    N = len(v)
    res = json.loads((T / "analysis_results.json").read_text())
    pp = pd.read_csv(T / "pain_point_summary.csv").set_index("pain_point")
    fd = pd.read_csv(T / "feature_demand.csv").set_index("feature")
    cp = pd.read_csv(T / "contradiction_probe_counts.csv").set_index("contradiction")
    asp = pd.read_csv(T / "aspect_sentiment_summary.csv", index_col=0)
    ac = yaml.safe_load(open(ROOT / "config" / "academic_curated.yaml"))
    acad = [a for a in ac if isinstance(a, dict) and "id" in a]
    exp = pd.read_parquet(G / "expert_evidence.parquet")

    # ---------------- persona summary (names from notes)
    prof = pd.read_json(T / "persona_profiles.json")
    pn = notes.get("persona_names", {})
    prof["persona_name"] = prof.persona_cluster.map(lambda c: (pn.get(int(c)) or {}).get("name", f"Cluster {c}"))
    prof["persona_description"] = prof.persona_cluster.map(lambda c: (pn.get(int(c)) or {}).get("description", ""))
    rob = json.loads((T / "persona_robustness.json").read_text())
    sel = pd.read_csv(T / "persona_model_selection.csv").set_index("k")
    k = rob["k"]
    prof["silhouette_k"] = sel.loc[k, "silhouette"]
    prof["bootstrap_ari_k"] = sel.loc[k, "bootstrap_ari_mean"]
    prof["confidence"] = np.where((sel.loc[k, "bootstrap_ari_mean"] >= 0.75) & (sel.loc[k, "silhouette"] >= 0.25), "MEDIUM",
                                  "LOW (fragile clustering)")
    for c in ["platforms", "languages", "defining_features", "experience", "intents", "pains", "features",
              "explicit_features", "price", "sentiment", "contradictions"]:
        prof[c] = prof[c].map(lambda x: json.dumps(x, ensure_ascii=False))
    prof.to_csv(T / "persona_summary.csv", index=False)

    # ---------------- hypothesis metrics
    H = {}
    n_space, p_space, _ = rx_count(v, r"(apartment|balcon|small space|tiny (space|apartment)|kitchen counter|countertop|"
                                     r"indoor|windowsill|condo|no (yard|garden)|lahan sempit|balkon|teras|apartemen|\bkos\b|rumah)")
    n_comm = int((v.author_experience_signal == "PROFESSIONAL_COMMERCIAL").sum())
    H["H01"] = dict(metric="records with home/indoor/small-space context", n=n_space, pct=round(n_space / N * 100, 2),
                    platforms=p_space, contrast=f"PROFESSIONAL_COMMERCIAL signal n={n_comm}")
    beg = v.author_experience_signal.isin(["BEGINNER", "NEVER_TRIED"])
    known = v.author_experience_signal != "UNKNOWN"
    H["H02"] = dict(metric="beginner/never-tried among records with an explicit experience signal", n=int(beg.sum()),
                    pct=round(beg.sum() / max(1, known.sum()) * 100, 2), denominator=int(known.sum()),
                    beginner_problem_solving_pct=round((v[beg].intents.fillna("").str.contains("PROBLEM_SOLVING")).mean() * 100, 2),
                    nonbeginner_problem_solving_pct=round((v[~beg & known].intents.fillna("").str.contains("PROBLEM_SOLVING")).mean() * 100, 2),
                    platforms=int(v[beg].platform.nunique()))
    n_age, p_age, age_df = rx_count(v, r"\b(i'?m|i am|aku|saya)\s+(\d{2})\s*(yo|y/o|years? old|tahun)\b|\bumur (saya|aku) \d{2}")
    ages = age_df.text_model.str.extract(r"(\d{2})\s*(?:yo|y/o|years? old|tahun)", expand=False).dropna().astype(int)
    H["H03"] = dict(metric="explicit self-reported age", n=n_age, pct=round(n_age / N * 100, 3),
                    ages_in_20_40=int(ages.between(20, 40).sum()), ages_reported=int(len(ages)),
                    note="Age is not inferred from writing style; only explicit self-reports are counted.")
    idn = v[v.text_language == "id"]
    H["H04"] = dict(metric="Indonesian-language customer-voice records", n=len(idn), pct=round(len(idn) / N * 100, 2),
                    platforms=int(idn.platform.nunique()),
                    indonesia_community_context=int((g.country == "ID").sum()),
                    java_mentions=rx_count(v, r"\b(jawa|java|jakarta|surabaya|bandung|semarang|yogya|jogja|malang|bekasi|bogor|depok|tangerang)\b")[0])
    ps = pd.read_csv(T / "price_signal_summary.csv").set_index("price_signal").n
    H["H05"] = dict(metric="price language", objection=int(ps.get("OBJECTION", 0)), cheap=int(ps.get("CHEAP_LANGUAGE", 0)),
                    premium=int(ps.get("PREMIUM_LANGUAGE", 0)), question=int(ps.get("QUESTION", 0)),
                    subscription=int(ps.get("SUBSCRIPTION", 0)), cost_pain=int(pp.loc["COST", "count"]) if "COST" in pp.index else 0,
                    diy_cheaper_contradiction=int(cp.n_customer_voice.get("PRICE_OVER_FEATURES", 0)))
    tech = v.aspect_labels.fillna("").str.contains(r"sensors|automation|software_app|\bAI\b")
    tech_asp = asp.loc[[a for a in ["sensors", "automation", "software_app", "AI"] if a in asp.index]]
    H["H06"] = dict(metric="records discussing sensors/automation/app/AI", n=int(tech.sum()), pct=round(tech.mean() * 100, 2),
                    platforms=int(v[tech].platform.nunique()),
                    aspect_sentiment=tech_asp[[c for c in ["POSITIVE", "NEGATIVE", "n"] if c in tech_asp.columns]].to_dict(orient="index"),
                    anti_automation=int(cp.n_customer_voice.get("ANTI_AUTOMATION", 0)))
    sus_pos = v.sustainability_signal == "POSITIVE"
    sus_any = v.sustainability_signal != "ABSENT"
    pur = v.purchase_signal.isin(["HIGH", "MEDIUM"])
    H["H07"] = dict(metric="sustainability signal", any_n=int(sus_any.sum()), any_pct=round(sus_any.mean() * 100, 2),
                    positive_n=int(sus_pos.sum()), skeptical_n=int((v.sustainability_signal == "SKEPTICAL").sum()),
                    purchase_records=int(pur.sum()), purchase_with_sustainability=int((pur & sus_any).sum()),
                    purchase_with_sustainability_pct=round((pur & sus_any).sum() / max(1, pur.sum()) * 100, 2),
                    purchase_with_cost_or_price_pct=round((pur & (v.price_signal.fillna("") != "")).sum() / max(1, pur.sum()) * 100, 2))
    n_sch, p_sch, _ = rx_count(v, r"\b(school|classroom|teacher|students?|science fair|university|college|campus|"
                                  r"sekolah|guru|siswa|mahasiswa|kampus|universitas|library|perpustakaan)\b")
    H["H08"] = dict(metric="school/education/community-institution context", n=n_sch, pct=round(n_sch / N * 100, 2), platforms=p_sch)
    n_b2b, p_b2b, _ = rx_count(v, r"\b(restaurant|chef|hotel|cafe|caf[eé]|grocer|supermarket|farmers? market|"
                                  r"wholesale|commercial (farm|grow|operation)|my (customers|farm business)|restoran|hotel|"
                                  r"jual(an)? (sayur|selada)|supplier)\b")
    H["H09"] = dict(metric="B2B/commercial context (restaurants, hotels, markets, commercial growers)", n=n_b2b,
                    pct=round(n_b2b / N * 100, 2), platforms=p_b2b, professional_signal=n_comm)
    H["H10"] = dict(metric="bagasse/ampas tebu mentions", customer_voice=res["bagasse_mentions_customer_voice"],
                    all_gold=res["bagasse_mentions_gold"], media_terms=res["growing_media_terms"],
                    rockwool_concern=res["rockwool_negative_or_env_concern"])
    mon = ["ph_monitoring", "tds_ec_monitoring", "temperature_monitoring", "water_level_monitoring", "alerts"]
    H["H11"] = dict(metric="monitoring features", mentions=int(fd.loc[mon, "mentions"].sum()),
                    explicit=int(fd.loc[mon, "explicit_requests"].sum()),
                    pain_ph_ec_nutrients=int(sum(pp["count"].get(c, 0) for c in ["PH", "EC_TDS", "NUTRIENTS"])),
                    sensor_distrust=int(cp.n_customer_voice.get("SENSOR_DISTRUST", 0)),
                    classes=fd.loc[mon, "demand_class"].to_dict())
    ai = ["ai_anomaly_detection", "recommendations", "diagnostics"]
    H["H12"] = dict(metric="AI features", mentions=int(fd.loc[ai, "mentions"].sum()), explicit=int(fd.loc[ai, "explicit_requests"].sum()),
                    ai_aspect=asp.loc["AI"].to_dict() if "AI" in asp.index else {},
                    ai_skepticism=int(cp.n_customer_voice.get("AI_SKEPTICISM", 0)), classes=fd.loc[ai, "demand_class"].to_dict())
    H["H13"] = dict(metric="app & subscription", app_dislike=int(cp.n_customer_voice.get("APP_DISLIKE", 0)),
                    subscription_dislike=int(cp.n_customer_voice.get("SUBSCRIPTION_DISLIKE", 0)),
                    subscription_mentions=int(ps.get("SUBSCRIPTION", 0)),
                    app_aspect=asp.loc["software_app"].to_dict() if "software_app" in asp.index else {},
                    remote_app_mentions=int(fd.loc["remote_app_control", "mentions"]),
                    dashboard_mentions=int(fd.loc["dashboard", "mentions"]))
    (T / "hypothesis_metrics.json").write_text(json.dumps(H, indent=1, default=str))
    hv = notes.get("hypotheses", {})
    from src.utils.common import PROJECT
    rows = []
    for hid, text in PROJECT["hypotheses"].items():
        nt = hv.get(hid, {})
        rows.append(dict(hypothesis_id=hid, hypothesis=text, verdict=nt.get("verdict", "PENDING_REVIEW"),
                         key_metrics=json.dumps(H.get(hid, {}), default=str, ensure_ascii=False),
                         rationale=nt.get("rationale", ""), proposal_action=nt.get("action", ""),
                         primary_validation=nt.get("validation", "")))
    pd.DataFrame(rows).to_csv(T / "hypothesis_validation.csv", index=False)

    # ---------------- contradiction register
    cn = notes.get("contradictions", {})
    crows = []
    for code, r in cp.iterrows():
        nt = cn.get(code, {})
        crows.append(dict(contradiction_id=code, assumption_challenged=nt.get("assumption", ""), n_customer_voice=int(r.n_customer_voice),
                          pct_of_voice=r.pct_of_voice, n_platforms=int(r.n_platforms), platforms=r.platforms,
                          evidence_level=evidence_level(int(r.n_customer_voice), len([1 for x in eval(r.platforms).values() if x >= 3]) if isinstance(r.platforms, str) else 0),
                          example_paraphrases=nt.get("examples", ""), interpretation=nt.get("interpretation", ""),
                          implication=nt.get("implication", ""), example_record_ids=r.example_record_ids))
    for extra in notes.get("contradictions_extra", []):
        crows.append(extra)
    pd.DataFrame(crows).sort_values("n_customer_voice", ascending=False, key=lambda s: pd.to_numeric(s, errors="coerce").fillna(-1)).to_csv(
        T / "contradiction_register.csv", index=False)

    # ---------------- evidence strength + triangulation
    erows, trows = [], []
    for code, r in pp.iterrows():
        lvl = evidence_level(int(r["count"]), int(r.platforms_with_3plus))
        acad_ids = [a["id"] for a in acad if code in a.get("supports", [])]
        exp_ids = exp[exp.topic.str.contains(code)].expert_evidence_id.tolist()
        if lvl == "E3" and acad_ids and exp_ids:
            interp, conf, ins = "Customer + academic + expert agree", "HIGH", 4
        elif lvl == "E3" and (acad_ids or exp_ids):
            interp, conf, ins = "Cross-platform customer signal with partial external support", "MEDIUM-HIGH", 4
        elif lvl == "E3":
            interp, conf, ins = "Customer signal only (cross-platform)", "MEDIUM", 3
        elif lvl == "E2" and (acad_ids or exp_ids):
            interp, conf, ins = "External evidence strong; low customer salience in corpus", "LOW-MEDIUM", 2
        else:
            interp, conf, ins = "Weak / single-platform customer signal", "LOW", 1 if lvl in ("E0", "E1") else 2
        finding = f"Pain point {code}"
        erows.append(dict(finding=finding, finding_type="pain_point", n=int(r["count"]), platforms_with_3plus=int(r.platforms_with_3plus),
                          evidence_level=lvl, insight_level=ins))
        trows.append(dict(finding=finding, customer_signal=f"n={int(r['count'])} ({r.corpus_share:.1%} of {N:,}); {int(r.platforms_with_3plus)} platforms with ≥3; {lvl}",
                          academic_evidence="; ".join(acad_ids) or "none in curated set",
                          expert_evidence="; ".join(exp_ids) or "none", overall_interpretation=interp, confidence=conf,
                          insight_level=ins))
    for f, r in fd.iterrows():
        n = int(r.explicit_requests)
        lvl = evidence_level(n, int(r.explicit_platforms) if n >= 3 else 0)
        erows.append(dict(finding=f"Explicit request: {f}", finding_type="feature_explicit", n=n,
                          platforms_with_3plus=int(r.explicit_platforms), evidence_level=lvl, insight_level=None))
    for code, r in cp.iterrows():
        n = int(r.n_customer_voice)
        p3 = len([1 for x in eval(r.platforms).values() if x >= 3]) if isinstance(r.platforms, str) else 0
        erows.append(dict(finding=f"Contradiction: {code}", finding_type="contradiction", n=n, platforms_with_3plus=p3,
                          evidence_level=evidence_level(n, p3), insight_level=None))
    for extra in notes.get("triangulation_extra", []):
        trows.append(extra)
    pd.DataFrame(erows).to_csv(T / "evidence_strength.csv", index=False)
    pd.DataFrame(trows).to_csv(T / "triangulation_matrix.csv", index=False)
    # topic summary (labelled)
    ts = pd.read_csv(T / "topic_summary_auto.csv")
    tl = notes.get("topic_labels", {})
    ts["topic_label"] = ts.topic_id.map(lambda t: tl.get(int(t), {}).get("label") if isinstance(tl.get(int(t)), dict) else None).fillna(ts.auto_label)
    ts["researcher_review"] = ts.topic_id.map(lambda t: tl.get(int(t), {}).get("review", "") if isinstance(tl.get(int(t)), dict) else "")
    ts.to_csv(T / "topic_summary.csv", index=False)
    print("synthesis done; hypotheses", len(rows), "contradictions", len(crows), "triangulation rows", len(trows))


if __name__ == "__main__":
    main()
