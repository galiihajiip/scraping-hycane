"""SILVER -> GOLD selection + seeded-taxonomy labels (pain points, aspects, intent, experience, features,
purchase/price/sustainability signals, voice type, contradiction probes).

All rules live in config/taxonomy.yaml. Labels from this module are model-predicted (rule-based) and are
audited against the validation sample; they are never presented as human-verified.
"""
from __future__ import annotations

import re

import pandas as pd

from src.utils.common import ROOT, load_yaml

T = load_yaml("taxonomy.yaml")
FLAGS = re.I
C = lambda rx: re.compile(rx, FLAGS)

PROBLEM = C(T["problem_cue"])
PAIN = {k: (C(v["rx"]), v["severity"]) for k, v in T["pain_points"].items()}
PAIN_DIRECT = {k: C(v) for k, v in T.get("pain_points_direct", {}).items()}
ASPECT = {k: C(v) for k, v in T["aspects"].items()}
INTENT = {k: C(v) for k, v in T["intent"].items()}
EXPER = {k: C(v) for k, v in T["experience"].items()}
FEAT_EXPLICIT = C(T["features"]["explicit_cue"])
FEAT = {k: C(v) for k, v in T["features"]["catalog"].items()}
PURCH = {k: C(v) for k, v in T["purchase_signal"].items()}
PRICE = {k: C(v) for k, v in T["price_signal"].items()}
SUST = {k: C(v) for k, v in T["sustainability_signal"].items()}
VOICE = {k: C(v) for k, v in T["voice_type"].items()}
CONTRA = {k: C(v) for k, v in T["contradiction_probes"].items()}
SENT_SPLIT = re.compile(r"(?<=[.!?\n])\s+")

INTENT_PRIORITY = ["EXPLICIT_PURCHASE_INTENT", "ABANDONMENT_FRUSTRATION", "PURCHASE_EXPLORATION", "COMPARISON",
                   "PROBLEM_SOLVING", "POST_PURCHASE", "RECOMMENDATION", "INFORMATION_SEEKING", "INSPIRATION",
                   "AWARENESS"]
EXP_PRIORITY = ["PROFESSIONAL_COMMERCIAL", "EXPERIENCED", "INTERMEDIATE", "BEGINNER", "NEVER_TRIED"]

# Severity uplift cues (explicit loss / repeated failure / strong emotion)
SEV_UP = C(r"(all (my|the) plants (died|dead)|lost (everything|all|my whole)|every (time|single time)|again and again|"
           r"keeps (happening|dying)|third time|second time|gave up|never again|waste of money|disaster|nightmare|"
           r"semua mati|mati semua|gagal terus|selalu gagal|lagi-lagi|kapok)")


def sentences(t: str):
    return [s for s in SENT_SPLIT.split(t) if s.strip()]


def label(text: str, title: str | None) -> dict:
    t = text or ""
    title = title if isinstance(title, str) else None
    tt = f"{title}\n{t}" if title and title not in t else t
    sents = sentences(t)
    # ---- pain points: topic term AND a problem cue in the same sentence
    pains, sev = [], {}
    for code, (rx, base) in PAIN.items():
        hit = [s for s in sents if (rx.search(s) and PROBLEM.search(s)) or
               (code in PAIN_DIRECT and PAIN_DIRECT[code].search(s))]
        if hit:
            pains.append(code)
            sev[code] = min(5, base + (1 if SEV_UP.search(t) else 0) + (1 if len(hit) >= 2 else 0))
    aspects = [k for k, rx in ASPECT.items() if rx.search(t)]
    # thread/video titles are used as context for PROBLEM_SOLVING only (titles like "Cara ..." are not the commenter's intent)
    intents = [k for k in INTENT_PRIORITY if INTENT[k].search(tt if k == "PROBLEM_SOLVING" else t)]
    # AWARENESS only as a fallback for third-person/news-style hydroponic mentions
    primary_intent = next((k for k in intents if k != "AWARENESS"), intents[0] if intents else "UNKNOWN")
    exps = [k for k in EXP_PRIORITY if EXPER[k].search(tt)]
    experience = exps[0] if exps else "UNKNOWN"
    # ---- features: mention vs explicit request (explicit cue in the same sentence)
    feat_m, feat_x = [], []
    for k, rx in FEAT.items():
        ss = [s for s in sents if rx.search(s)]
        if ss:
            feat_m.append(k)
            if any(FEAT_EXPLICIT.search(s) for s in ss):
                feat_x.append(k)
    purchase = next((k for k in ("HIGH", "MEDIUM", "LOW") if PURCH[k].search(t)), "NONE")
    prices = [k for k, rx in PRICE.items() if rx.search(t)]
    sus = next((k for k in ("NEGATIVE", "SKEPTICAL", "POSITIVE", "NEUTRAL") if SUST[k].search(t)), "ABSENT")
    if VOICE["NEWS_OR_PROMO"].search(t) and not re.search(r"\b(i|my|i'm|saya|aku)\b", t[:200], re.I):
        voice = "NEWS_OR_PROMO"
    elif VOICE["QUESTION"].search(t[-300:]) or VOICE["QUESTION"].search(sents[0] if sents else ""):
        voice = "QUESTION"
    elif VOICE["PERSONAL_EXPERIENCE"].search(t):
        voice = "PERSONAL_EXPERIENCE"
    else:
        voice = "OPINION_OR_OTHER"
    contra = [k for k, rx in CONTRA.items() if rx.search(t)]
    return dict(pain_points="|".join(pains), pain_severity="|".join(f"{k}:{v}" for k, v in sev.items()),
                max_pain_severity=max(sev.values()) if sev else 0, aspect_labels="|".join(aspects),
                intents="|".join(intents), intent=primary_intent, author_experience_signal=experience,
                feature_mentions="|".join(feat_m), feature_explicit="|".join(feat_x),
                purchase_signal=purchase, price_signal="|".join(prices), sustainability_signal=sus,
                voice_type=voice, contradiction_flags="|".join(contra))


def build_gold():
    s = pd.read_parquet(ROOT / "data" / "silver" / "silver.parquet")
    s["exclusion_reason"] = ""
    s.loc[~s.is_relevant, "exclusion_reason"] = "not_relevant"
    s.loc[(s.exclusion_reason == "") & (s.exclusion_meaning != ""), "exclusion_reason"] = "unrelated_meaning"
    s.loc[(s.exclusion_reason == "") & s.is_spam, "exclusion_reason"] = "spam"
    s.loc[(s.exclusion_reason == "") & (s.duplicate_status != "canonical"), "exclusion_reason"] = "duplicate"
    s.loc[(s.exclusion_reason == "") & (s.n_chars < 15), "exclusion_reason"] = "too_short"
    s.loc[(s.exclusion_reason == "") & s.text_model.str.fullmatch(r"\s*\[?(deleted|removed)\]?\s*", case=False),
          "exclusion_reason"] = "deleted"
    excl = s.exclusion_reason.value_counts()
    excl.rename_axis("exclusion_reason").reset_index(name="n").to_csv(
        ROOT / "outputs" / "tables" / "gold_exclusions.csv", index=False)
    g = s[s.exclusion_reason == ""].copy()
    g["in_core_scope"] = ~g.cannabis_context
    print("gold candidates", len(g), "| core scope", int(g.in_core_scope.sum()))
    labs = pd.DataFrame([label(t, ti) for t, ti in zip(g.text_model, g.thread_title)], index=g.index)
    g = pd.concat([g, labs], axis=1)
    g["evidence_type"] = "customer_voice_public_post"
    g.loc[g.voice_type == "NEWS_OR_PROMO", "evidence_type"] = "news_or_promotional_post"
    return g


if __name__ == "__main__":
    g = build_gold()
    g.to_parquet(ROOT / "data" / "gold" / "_gold_rules.parquet", index=False)
    print(g.intent.value_counts().head(12))
    print(g.pain_points.str.split("|").explode().value_counts().head(22))
