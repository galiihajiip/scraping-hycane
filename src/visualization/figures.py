"""Static figures (PNG + SVG) generated only from saved tables / gold data.

Palette: reference data-viz palette (single series = slot-1 blue; sequential = one-hue blue ramp; sentiment =
blue (positive) <-> red (negative) with gray neutral). Every figure carries a footer with n, denominator,
timeframe, analysis layer and material exclusions.
"""
from __future__ import annotations

import json

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402
from matplotlib.colors import LinearSegmentedColormap  # noqa: E402

from src.utils.common import ROOT  # noqa: E402

T = ROOT / "outputs" / "tables"
FIG = ROOT / "outputs" / "figures"
FIG.mkdir(parents=True, exist_ok=True)
BLUE, ORANGE, AQUA, YELLOW, MAGENTA, GREEN, VIOLET, RED = ("#2a78d6", "#eb6834", "#1baf7a", "#eda100", "#e87ba4",
                                                         "#008300", "#4a3aa7", "#e34948")
CAT = [BLUE, ORANGE, AQUA, YELLOW, MAGENTA, GREEN, VIOLET, RED]
INK, INK2, MUTED, GRID, SURF = "#0b0b0b", "#52514e", "#8a8984", "#e6e5e1", "#fcfcfb"
SENT_COL = {"POSITIVE": BLUE, "NEUTRAL": "#b9b8b2", "MIXED": VIOLET, "AMBIGUOUS": "#dcdbd6", "NEGATIVE": RED}
SENT_ORDER = ["POSITIVE", "NEUTRAL", "MIXED", "AMBIGUOUS", "NEGATIVE"]
SEQ = LinearSegmentedColormap.from_list("blue", ["#f4f8fd", "#cde2fb", "#86b6ef", "#3987e5", "#1c5cab", "#0d366b"])
EXCL = "Excl.: irrelevant, unrelated meanings, spam, duplicates, cannabis-context, news/promo"

plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 9.5, "axes.edgecolor": GRID, "axes.labelcolor": INK2,
                     "xtick.color": INK2, "ytick.color": INK2, "axes.titleweight": "bold", "axes.titlesize": 12,
                     "axes.titlecolor": INK, "figure.facecolor": SURF, "axes.facecolor": SURF, "axes.grid": False,
                     "axes.spines.top": False, "axes.spines.right": False, "svg.fonttype": "none"})


def R():
    return json.loads((T / "analysis_results.json").read_text())


def footer(fig, n, denom=None, tf=None, layer="GOLD customer-voice core", excl=EXCL):
    tf = tf or R()["timeframe_customer_voice"]
    txt = f"n = {n:,}" + (f" | denominator = {denom}" if denom else "") + f" | timeframe {tf} | layer: {layer}\n{excl}"
    fig.text(0.01, -0.95 / fig.get_figheight(), txt, fontsize=7.5, color=MUTED, va="bottom", ha="left")


def save(fig, name):
    fig.savefig(FIG / f"{name}.png", dpi=170, bbox_inches="tight")
    fig.savefig(FIG / f"{name}.svg", bbox_inches="tight")
    plt.close(fig)


def hbar(ax, labels, values, color=BLUE, fmt="{:,.0f}", xlabel=""):
    y = np.arange(len(labels))[::-1]
    ax.barh(y, values, color=color, height=0.68, edgecolor=SURF, linewidth=2)
    ax.set_yticks(y, labels)
    ax.xaxis.grid(True, color=GRID, lw=0.6)
    ax.set_axisbelow(True)
    ax.set_xlabel(xlabel)
    mx = max(values) if len(values) else 1
    for yy, vv in zip(y, values):
        ax.text(vv + mx * 0.01, yy, fmt.format(vv), va="center", fontsize=8, color=INK2)


def stacked_sent(ax, df, title):
    df = df[[c for c in SENT_ORDER if c in df.columns]]
    left = np.zeros(len(df))
    y = np.arange(len(df))[::-1]
    for c in df.columns:
        ax.barh(y, df[c].values, left=left, color=SENT_COL[c], label=c.title(), height=0.7, edgecolor=SURF, linewidth=1.5)
        left += df[c].values
    ax.set_yticks(y, df.index)
    ax.set_xlim(0, 100)
    ax.set_xlabel("% of records")
    ax.set_title(title, loc="left", pad=26)
    ax.legend(ncol=5, loc="lower left", bbox_to_anchor=(0, 1.0), frameon=False, fontsize=8)


def heat(ax, M, fmt="{:.0f}", cbar_label="%"):
    im = ax.imshow(M.values, cmap=SEQ, aspect="auto")
    ax.set_xticks(range(M.shape[1]), M.columns, rotation=45, ha="right", fontsize=8)
    ax.set_yticks(range(M.shape[0]), M.index, fontsize=8)
    vmax = np.nanmax(M.values) if M.size else 1
    for i in range(M.shape[0]):
        for j in range(M.shape[1]):
            val = M.values[i, j]
            if val > 0:
                ax.text(j, i, fmt.format(val), ha="center", va="center", fontsize=6.5,
                        color="white" if val > vmax * 0.55 else INK)
    plt.colorbar(im, ax=ax, fraction=0.03, pad=0.02, label=cbar_label)


def main():
    res = R()
    nvoice = res["counts"]["customer_voice"]
    cov = pd.read_csv(T / "platform_coverage.csv")
    # 01 platform coverage
    c = cov.sort_values("customer_voice_core", ascending=False)
    fig, ax = plt.subplots(figsize=(8, 4.2))
    hbar(ax, c.platform.tolist(), c.customer_voice_core.tolist(), xlabel="customer-voice records (core scope)")
    ax.set_title("Platform coverage — customer-voice records", loc="left")
    footer(fig, nvoice, f"{res['counts']['gold']:,} gold records")
    save(fig, "01_platform_coverage")
    # 02 source family funnel (raw -> gold)
    fig, ax = plt.subplots(figsize=(9, 4.4))
    stages = ["unique_source_objects", "relevant", "gold_records", "customer_voice_core"]
    x = np.arange(len(c))
    w = 0.2
    for i, st in enumerate(stages):
        ax.bar(x + (i - 1.5) * w, c[st], width=w, color=CAT[i], label=st.replace("_", " "), edgecolor=SURF, lw=1)
    ax.set_xticks(x, c.platform)
    ax.set_yscale("log")
    ax.set_ylabel("records (log scale)")
    ax.legend(frameon=False, ncol=4, fontsize=8, loc="lower left", bbox_to_anchor=(0, 1.0))
    ax.set_title("Source-family coverage: collection-to-gold funnel", loc="left", pad=22)
    footer(fig, int(c.unique_source_objects.sum()), "unique source objects", layer="SILVER -> GOLD")
    save(fig, "02_source_family_coverage")
    # 03 timeline
    tl = pd.read_csv(T / "timeline_monthly.csv", index_col=0)
    tl.index = pd.PeriodIndex(tl.index, freq="M")
    yr = tl.groupby(tl.index.year).sum()
    fig, ax = plt.subplots(figsize=(9, 4))
    bottom = np.zeros(len(yr))
    order = yr.sum().sort_values(ascending=False).index
    for i, p in enumerate(order):
        ax.bar(yr.index, yr[p], bottom=bottom, color=CAT[i % 8] if i < 8 else MUTED, label=p, edgecolor=SURF, lw=1)
        bottom += yr[p].values
    ax.legend(frameon=False, ncol=4, fontsize=8)
    ax.set_ylabel("customer-voice records")
    ax.set_title("Timeline — records by year of posting", loc="left")
    footer(fig, int(yr.values.sum()), layer="GOLD customer-voice core (by created_at)")
    save(fig, "03_timeline")
    # 04 sentiment by platform
    sp = pd.read_csv(T / "sentiment_by_platform.csv", index_col=0)
    lab = [f"{i} (n={int(n):,})" for i, n in zip(sp.index, sp.n)]
    fig, ax = plt.subplots(figsize=(9, 4))
    stacked_sent(ax, sp.drop(columns="n").set_axis(lab), "Sentiment by platform (model-predicted)")
    t = res["sentiment_platform_test"]
    footer(fig, nvoice, f"records per platform | chi²={t['chi2']}, p={t['p_value']}, Cramér's V={t['cramers_v']}")
    save(fig, "04_sentiment_by_platform")
    # 05 sentiment by topic
    if (T / "sentiment_by_topic.csv").exists():
        st = pd.read_csv(T / "sentiment_by_topic.csv", index_col=0).head(20)
        lab = [f"{str(i)[:42]} (n={int(n)})" for i, n in zip(st.index, st.n)]
        fig, ax = plt.subplots(figsize=(10, 7))
        stacked_sent(ax, st.drop(columns="n").set_axis(lab), "Sentiment by topic (20 largest topics)")
        footer(fig, int(st.n.sum()), "records per topic")
        save(fig, "05_sentiment_by_topic")
    # 06 top pain points
    pp = pd.read_csv(T / "pain_point_summary.csv").sort_values("count", ascending=False)
    fig, ax = plt.subplots(figsize=(8, 6))
    hbar(ax, pp.pain_point.tolist(), (pp.corpus_share * 100).round(2).tolist(), fmt="{:.1f}%",
         xlabel="% of customer-voice records mentioning the pain (with a problem cue)")
    ax.set_title("Pain points — frequency", loc="left")
    footer(fig, int(pp["count"].sum()), f"{nvoice:,} customer-voice records (multi-label)")
    save(fig, "06_top_pain_points")
    # 07 frequency x severity
    fig, ax = plt.subplots(figsize=(8, 6))
    sev = pp.mean_severity + 2 * pp.negative_share
    ax.scatter(pp.corpus_share * 100, sev, s=40 + pp.platform_breadth * 260, color=BLUE, alpha=0.75,
               edgecolor=SURF, linewidth=2)
    for _, r in pp.iterrows():
        ax.annotate(r.pain_point, (r.corpus_share * 100, r.mean_severity + 2 * r.negative_share), fontsize=7.5,
                    color=INK2, xytext=(4, 3), textcoords="offset points")
    ax.set_xscale("log")
    ax.set_xlabel("frequency: % of customer-voice records (log)")
    ax.set_ylabel("severity index = mean rule severity + 2 × negative share")
    ax.axhline(sev.median(), color=GRID, lw=1)
    ax.axvline((pp.corpus_share * 100).median(), color=GRID, lw=1)
    ax.set_title("Pain-point frequency × severity (bubble = platform breadth)", loc="left")
    footer(fig, int(pp["count"].sum()), f"{nvoice:,} customer-voice records")
    save(fig, "07_painpoint_frequency_severity")
    # 08 intent distribution
    it = pd.read_csv(T / "intent_summary.csv").sort_values("n_primary", ascending=False)
    fig, ax = plt.subplots(figsize=(8, 4.8))
    hbar(ax, it.intent.tolist(), it.pct_primary.tolist(), fmt="{:.1f}%", xlabel="% of customer-voice records (primary intent)")
    ax.set_title("Customer intent (primary label; rule-based)", loc="left")
    footer(fig, nvoice, f"{nvoice:,} customer-voice records")
    save(fig, "08_intent_distribution")
    # 08b intent by platform heatmap
    ip = pd.read_csv(T / "intent_by_platform.csv", index_col=0)
    fig, ax = plt.subplots(figsize=(10, 4.2))
    heat(ax, ip.drop(columns="n"))
    ax.set_title("Intent by platform (% of platform's records)", loc="left")
    t = res["intent_platform_test"]
    footer(fig, nvoice, f"records per platform | Cramér's V={t['cramers_v']}")
    save(fig, "08b_intent_by_platform")
    # 09 feature demand
    fd = pd.read_csv(T / "feature_demand.csv")
    fd = fd.sort_values("mentions", ascending=True)
    fig, ax = plt.subplots(figsize=(9, 6))
    y = np.arange(len(fd))
    ax.barh(y + 0.2, fd.mentions, height=0.38, color=BLUE, label="mentions", edgecolor=SURF, lw=1.5)
    ax.barh(y - 0.2, fd.explicit_requests, height=0.38, color=ORANGE, label="explicit requests", edgecolor=SURF, lw=1.5)
    ax.set_yticks(y, [f"{f}  [{c}]" for f, c in zip(fd.feature, fd.demand_class)], fontsize=8)
    ax.legend(frameon=False, loc="lower right")
    ax.set_xlabel("customer-voice records")
    ax.set_title("Feature demand — mentions vs explicit requests (class in brackets)", loc="left")
    footer(fig, nvoice, f"{nvoice:,} customer-voice records")
    save(fig, "09_feature_demand")
    # 10-12 personas
    if (T / "persona_summary.csv").exists():
        ps = pd.read_csv(T / "persona_summary.csv")
        fig, ax = plt.subplots(figsize=(8, 3.6))
        hbar(ax, [f"P{int(a)} {b}" for a, b in zip(ps.persona_cluster, ps.persona_name)], ps.n.tolist(),
             xlabel="customer-voice records with >=2 discourse features")
        ax.set_title("Persona (discourse-segment) distribution", loc="left")
        footer(fig, int(ps.n.sum()), "informative customer-voice records")
        save(fig, "10_persona_distribution")
        names = dict(zip(ps.persona_cluster.astype(int), ps.persona_name))
        for fname, title, out in [("persona_x_painpoint_pct.csv", "Persona × pain point (% of persona records)", "11_persona_painpoints"),
                                  ("persona_x_feature_pct.csv", "Persona × feature mention (% of persona records)", "12_persona_features")]:
            M = pd.read_csv(T / fname, index_col=0)
            M.index = [f"P{int(i)} {names.get(int(i), '')}"[:34] for i in M.index]
            fig, ax = plt.subplots(figsize=(11, 3.8))
            heat(ax, M, fmt="{:.0f}")
            ax.set_title(title, loc="left")
            footer(fig, int(ps.n.sum()), "records per persona")
            save(fig, out)
    # 13 language
    lg = pd.read_csv(T / "language_distribution.csv").head(12)
    fig, ax = plt.subplots(figsize=(7, 4))
    hbar(ax, lg.text_language.tolist(), lg.gold.tolist(), xlabel="gold records")
    ax.set_xscale("log")
    ax.set_title("Language distribution (lingua detector)", loc="left")
    footer(fig, res["counts"]["gold"], "gold records (all scopes)", layer="GOLD")
    save(fig, "13_language_distribution")
    # 14 geography (explicit only)
    geo = pd.read_csv(T / "geography_explicit_sources.csv")
    gc = pd.read_csv(T / "geography_country_context.csv")
    fig, axs = plt.subplots(1, 2, figsize=(9, 3.2))
    hbar(axs[0], geo.geo_source.tolist(), geo.n.tolist(), xlabel="records")
    axs[0].set_title("Geo signal source", loc="left", fontsize=10)
    if len(gc):
        hbar(axs[1], gc.country.tolist(), gc.n.tolist(), xlabel="records")
    axs[1].set_title("Country (community context)", loc="left", fontsize=10)
    footer(fig, int(geo.n.sum()), f"{res['counts']['gold']:,} gold; geo known rate {res['data_quality']['geo_known_rate_gold']:.1%}",
           layer="GOLD", excl="Only explicit community context or explicit self-report; no inferred location")
    save(fig, "14_geography_explicit")
    # 15 platform x topic
    if (T / "platform_x_topic_pct.csv").exists():
        pt = pd.read_csv(T / "platform_x_topic_pct.csv", index_col=0)
        pt = pt.loc[pt.sum(axis=1).sort_values(ascending=False).index[:22]]
        pt.index = [str(i)[:40] for i in pt.index]
        fig, ax = plt.subplots(figsize=(9, 8))
        heat(ax, pt, fmt="{:.0f}")
        ax.set_title("Platform × topic (% of each platform's records)", loc="left")
        footer(fig, nvoice, "records per platform (columns sum to 100% over all topics)")
        save(fig, "15_platform_topic_heatmap")
    # 16 evidence strength
    if (T / "evidence_strength.csv").exists():
        es = pd.read_csv(T / "evidence_strength.csv")
        cnt = es.evidence_level.value_counts().sort_index()
        fig, ax = plt.subplots(figsize=(7, 3.2))
        ax.bar(cnt.index, cnt.values, color=BLUE, edgecolor=SURF, lw=2, width=0.6)
        ax.set_ylabel("findings")
        ax.set_title("Evidence strength of findings (E0–E5 codebook)", loc="left")
        footer(fig, int(cnt.sum()), "findings in evidence_strength.csv", layer="INSIGHT")
        save(fig, "16_evidence_strength")
    # 17 HYCANE mapping
    mp = pd.read_csv(T / "hycane_feature_mapping.csv").sort_values("count")
    fig, ax = plt.subplots(figsize=(9, 6.5))
    y = np.arange(len(mp))
    cols = [BLUE if r >= 0.7 else ("#86b6ef" if r >= 0.5 else "#cde2fb") for r in mp.hycane_relevance]
    ax.barh(y, mp["count"], color=cols, edgecolor=SURF, lw=2)
    ax.set_yticks(y, [f"{p} → {c[:38]}" for p, c in zip(mp.pain_point, mp.hycane_component)], fontsize=7.5)
    ax.set_xlabel("customer-voice records with the pain")
    for yy, (n, r) in enumerate(zip(mp["count"], mp.hycane_relevance)):
        ax.text(n + mp["count"].max() * 0.01, yy, f"{n:,} | rel {r}", va="center", fontsize=7, color=INK2)
    ax.set_title("HYCANE pain → component mapping (shade = researcher-set relevance)", loc="left")
    footer(fig, nvoice, f"{nvoice:,} customer-voice records", layer="INSIGHT (mapping weights in config/hycane_mapping.yaml)")
    save(fig, "17_hycane_feature_mapping")
    # 18 contradictions
    cp = pd.read_csv(T / "contradiction_probe_counts.csv").sort_values("n_customer_voice", ascending=False)
    fig, ax = plt.subplots(figsize=(8, 3.8))
    hbar(ax, cp.contradiction.tolist(), cp.n_customer_voice.tolist(), color=RED, xlabel="customer-voice records matching probe")
    ax.set_title("Contradiction probes — evidence against HYCANE assumptions", loc="left")
    footer(fig, int(cp.n_customer_voice.sum()), f"{nvoice:,} customer-voice records")
    save(fig, "18_contradictions")
    # 19 saturation
    if (T / "saturation_curve.csv").exists():
        sat = pd.read_csv(T / "saturation_curve.csv")
        fig, ax = plt.subplots(figsize=(8, 3.6))
        ax.plot(sat.records, sat.new_per_100.rolling(5, min_periods=1).mean(), color=BLUE, lw=2)
        ax.set_xlabel("customer-voice records (collection order)")
        ax.set_ylabel("new topic×pain combos per 100 (rolling 5)")
        ax.set_title("Saturation — marginal novelty per 100 new records", loc="left")
        footer(fig, int(sat.records.max()), layer="GOLD customer-voice core")
        save(fig, "19_saturation")
    print("figures written:", len(list(FIG.glob("*.png"))))


if __name__ == "__main__":
    main()
