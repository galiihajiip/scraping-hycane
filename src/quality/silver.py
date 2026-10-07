"""BRONZE -> SILVER: cleaning, extraction, language, relevance, scope, spam, deduplication.

Nothing is deleted: every bronze occurrence is kept with flags; gold selection happens in gold.py.
"""
from __future__ import annotations

import re
import unicodedata
from collections import defaultdict

import emoji
import numpy as np
import pandas as pd
from datasketch import MinHash, MinHashLSH
from lingua import Language, LanguageDetectorBuilder

from src.normalization.normalize import html_to_text
from src.utils.common import ROOT, load_yaml, sha256

F = load_yaml("filters.yaml")
SILVER = ROOT / "data" / "silver"

URL_RE = re.compile(r"https?://\S+|www\.\S+", re.I)
MENTION_RE = re.compile(r"(?<!\w)@[\w.\-]+")
HASHTAG_RE = re.compile(r"(?<!\w)#(\w+)")
STRONG_RE = re.compile(
    r"(hydroponi|hidroponi|hydroponik|kratky|\bdwc\b|deep water culture|aeroponi|aerogarden|aero garden|"
    r"click ?(and|&|n) ?grow|lettuce ?grow|gardyn|rise gardens?|tower ?garden|\bnft (system|channel|pipe|gully)|"
    r"ebb (and|&|n) flow|flood (and|&) drain|rockwool|rock wool|net ?pots?|nutrient solution|\bab ?mix|nutrisi ab|"
    r"rakit apung|wick system|sistem wick|soilless|tanpa tanah|\bhydro (setup|system|garden|grow|tote|bucket)|"
    r"grow ?tent|clay pebbles|hydroton|leca\b|\bpak ?choy|\bpakcoy|smart garden|indoor garden)", re.I)
WEAK_RE = re.compile(r"(\bph\b|\bec\b|\btds\b|\bppm\b|reservoir|nutrient|nutrisi|air ?pump|air ?stone|airstone|"
                     r"grow ?lights?|seedlings?|semai|selada|lettuce|kangkung|sawi|root rot|akar busuk)", re.I)
CANNABIS_RE = re.compile(F["scope"]["cannabis_regex"], re.I)
EXCL = {k: re.compile(v, re.I) for k, v in F["scope"]["exclusion_meanings"].items()}
PROMO_RE = re.compile(F["spam"]["promo_regex"], re.I)
BAGASSE_RE = re.compile(r"(bagasse|ampas tebu|limbah tebu|sugar ?cane (waste|fiber|fibre|pulp))", re.I)
BAGASSE_MEDIA_RE = re.compile(r"(media tanam|growing (media|medium)|substrate|hidroponi|hydroponi|seedling|semai|"
                              r"compost|kompos|pupuk|potting|soil (mix|amendment)|rockwool|cocopeat|tanam)", re.I)
SOCIAL_PROMO_RE = re.compile(r"(sub(scribe)? ?back|subscribe (to )?my|visit my channel|check out my channel|cek channel|"
                             r"mampir (ke )?(channel|chanel)|follow back|saling subscribe|sub balik)", re.I)
HYDRO_COMMUNITIES = {c.lower() for c in F["relevance"]["hydroponic_only_communities"]} | {
    "gardenweb_hydroponics", "hydroponics"}

LANGS = [Language.ENGLISH, Language.INDONESIAN, Language.MALAY, Language.SPANISH, Language.PORTUGUESE,
         Language.GERMAN, Language.FRENCH, Language.DUTCH, Language.ITALIAN, Language.TAGALOG, Language.JAPANESE,
         Language.CHINESE, Language.THAI, Language.VIETNAMESE, Language.POLISH, Language.RUSSIAN, Language.TURKISH,
         Language.SWEDISH, Language.FINNISH, Language.CATALAN, Language.KOREAN, Language.ARABIC, Language.HINDI,
         Language.DANISH, Language.CZECH, Language.ROMANIAN, Language.HUNGARIAN, Language.GREEK, Language.UKRAINIAN]
DETECTOR = LanguageDetectorBuilder.from_languages(*LANGS).with_preloaded_language_models().build()


def clean_text(raw: str, is_html: bool) -> str:
    t = html_to_text(raw) if is_html else raw
    t = unicodedata.normalize("NFKC", t)
    t = re.sub(r"[ \t ]+", " ", t)
    t = re.sub(r"\n\s*\n+", "\n\n", t)
    return t.strip()


def model_text(t: str) -> str:
    t = URL_RE.sub(" ", t)
    t = re.sub(r"(.)\1{3,}", r"\1\1", t)  # repeated characters (model text only)
    return re.sub(r"\s+", " ", t).strip()


def norm_for_hash(t: str) -> str:
    t = URL_RE.sub("", t.lower())
    t = MENTION_RE.sub("", t)
    t = re.sub(r"[^\w\s]", "", t)
    return re.sub(r"\s+", " ", t).strip()


def detect_lang(t: str):
    t = t[:600]
    if len(re.sub(r"\W", "", t)) < 8:
        return "und", 0.0
    conf = DETECTOR.compute_language_confidence_values(t)
    if not conf:
        return "und", 0.0
    top = conf[0]
    return top.language.iso_code_639_1.name.lower(), round(top.value, 3)


def detect_langs_parallel(texts):
    """Batch lingua detection (multi-threaded); same rules as detect_lang."""
    out = [("und", 0.0)] * len(texts)
    idx = [i for i, t in enumerate(texts) if len(re.sub(r"\W", "", t[:600])) >= 8]
    res = DETECTOR.compute_language_confidence_values_in_parallel([texts[i][:600] for i in idx])
    for i, conf in zip(idx, res):
        if conf:
            out[i] = (conf[0].language.iso_code_639_1.name.lower(), round(conf[0].value, 3))
    return out


def main():
    b = pd.read_parquet(ROOT / "data" / "bronze" / "all_bronze.parquet")
    print("bronze rows", len(b))
    # ---- occurrence-level dedup by platform source ID (same object captured by several queries/instances)
    b = b.sort_values(["record_id", "collected_at"])
    occ = b.groupby("record_id").agg(n_captures=("raw_capture_path", "size"),
                                     all_query_ids=("query_id", lambda s: "|".join(sorted(set(map(str, s))))))
    s = b.drop_duplicates("record_id", keep="first").merge(occ, on="record_id").reset_index(drop=True)
    print("unique source objects", len(s))

    s["text_clean"] = [clean_text(r, h) for r, h in zip(s.text_raw, s.text_is_html)]
    s["urls"] = s.text_clean.map(lambda t: "|".join(URL_RE.findall(t)))
    s["n_urls"] = s.text_clean.map(lambda t: len(URL_RE.findall(t)))
    s["mentions"] = s.text_clean.map(lambda t: "|".join(MENTION_RE.findall(t)))
    s["hashtags"] = s.text_clean.map(lambda t: "|".join(h.lower() for h in HASHTAG_RE.findall(t)))
    s["emoji_count"] = s.text_clean.map(emoji.emoji_count)
    s["text_model"] = s.text_clean.map(model_text)
    s["n_chars"] = s.text_model.str.len()

    print("language detection ...")
    langs = detect_langs_parallel(s.text_model.tolist())
    s["text_language_detected"] = [l for l, _ in langs]
    # lingua often labels Indonesian as Malay; reassign ms -> id when the record came from an Indonesian query
    qid = s.query_id.fillna("")
    id_query = qid.str.contains(r"_id_") | s.community.fillna("").str.lower().eq("indonesia")
    s["text_language"] = np.where((s.text_language_detected == "ms") & id_query, "id", s.text_language_detected)
    s["language_reassigned"] = (s.text_language != s.text_language_detected)
    s["language_confidence"] = [c for _, c in langs]

    # ---- relevance
    ctx = (s.thread_title.fillna("")).astype(str)
    comm = s.community.fillna("").str.lower()
    strong = s.text_model.str.contains(STRONG_RE)
    weak = s.text_model.str.contains(WEAK_RE)
    in_hydro_comm = comm.isin(HYDRO_COMMUNITIES) | s.extra.fillna("").str.contains('"hydroponic"', regex=False)
    title_strong = ctx.str.contains(STRONG_RE)
    s["relevance_score"] = np.select(
        [strong, in_hydro_comm, title_strong & weak, title_strong, weak], [1.0, 0.8, 0.7, 0.6, 0.3], 0.0)
    s["relevance_basis"] = np.select(
        [strong, in_hydro_comm, title_strong & weak, title_strong, weak],
        ["text_strong_term", "hydroponic_community", "thread_title+weak_term", "thread_title", "weak_term_only"],
        "none")
    s["bagasse_mention"] = s.text_model.str.contains(BAGASSE_RE)
    s["bagasse_media_context"] = s.bagasse_mention & s.text_model.str.contains(BAGASSE_MEDIA_RE)
    up = s.bagasse_media_context & (s.relevance_score < 0.7)
    s.loc[up, "relevance_score"] = 0.7
    s.loc[up, "relevance_basis"] = "bagasse_growing_context"
    s["is_relevant"] = s.relevance_score >= 0.6

    # ---- scope flags
    full = s.text_model + " " + ctx
    s["cannabis_context"] = full.str.contains(CANNABIS_RE)
    excl = pd.Series("", index=s.index)
    for k, rx in EXCL.items():
        hit = s.text_model.str.contains(rx)
        # hydro_power only excludes when no hydroponic term is present; the others are unrelated meanings
        # even when a hydroponic-looking token (rockwool, gardyn, hydroponics) appears.
        excl = np.where(hit & (~strong if k == "hydro_power" else True), k, excl)
    s["exclusion_meaning"] = excl

    # ---- spam
    s["norm_hash"] = s.text_model.map(norm_for_hash).map(sha256)
    alpha = s.text_model.map(lambda t: sum(c.isalpha() for c in t) / max(1, len(t)))
    auth_rep = s[s.author_id_hash.notna()].groupby(["author_id_hash", "norm_hash"]).size()
    rep_set = set(auth_rep[auth_rep >= F["spam"]["repeated_author_text_threshold"]].index)
    codes, score = [], []
    for i, r in s.iterrows():
        c = []
        if PROMO_RE.search(r.text_model) or PROMO_RE.search(r.urls or ""):
            c.append("PROMO_TERMS")
        if r.n_urls > F["spam"]["max_urls"]:
            c.append("MANY_URLS")
        if r.n_urls >= 1 and len(URL_RE.sub("", r.text_clean).strip()) < 25:
            c.append("LINK_ONLY")
        if alpha[i] < F["spam"]["min_alpha_ratio"] and r.n_chars > 0:
            c.append("LOW_ALPHA")
        if (r.author_id_hash, r.norm_hash) in rep_set:
            c.append("AUTHOR_REPEATED_TEXT")
        if SOCIAL_PROMO_RE.search(r.text_model):
            c.append("CHANNEL_SELF_PROMO")
        if len(r.hashtags.split("|")) >= 8:
            c.append("HASHTAG_STUFFING")
        codes.append("|".join(c))
        w = {"PROMO_TERMS": .35, "MANY_URLS": .25, "LINK_ONLY": .4, "LOW_ALPHA": .3, "AUTHOR_REPEATED_TEXT": .45,
             "HASHTAG_STUFFING": .3, "CHANNEL_SELF_PROMO": .5}
        score.append(round(min(1.0, sum(w[x] for x in c)), 2))
    s["spam_reason_codes"] = codes
    s["spam_probability"] = score  # transparent rule score, not a calibrated probability
    s["is_spam"] = s.spam_probability >= 0.5

    # ---- text dedup: exact, normalized, URL+text, MinHash near-duplicates
    s["exact_hash"] = s.text_clean.map(sha256)
    s["url_text_hash"] = (s.source_url.fillna("") + "|" + s.norm_hash).map(sha256)
    s["duplicate_cluster_id"] = None
    s["duplicate_status"] = "canonical"
    s["duplicate_reason"] = ""
    order = s.sort_values("created_at", na_position="last").index
    first_by = {}
    for i in order:
        h = s.at[i, "norm_hash"]
        if s.at[i, "n_chars"] < 15:
            continue
        if h in first_by:
            s.at[i, "duplicate_status"] = "duplicate"
            s.at[i, "duplicate_reason"] = "exact" if s.at[i, "exact_hash"] == s.at[first_by[h], "exact_hash"] \
                else "normalized_exact"
            s.at[i, "duplicate_cluster_id"] = f"dc_{h[:12]}"
            s.at[first_by[h], "duplicate_cluster_id"] = f"dc_{h[:12]}"
        else:
            first_by[h] = i
    cfg = F["dedup"]
    lsh = MinHashLSH(threshold=cfg["minhash_threshold"], num_perm=cfg["minhash_num_perm"])
    mh = {}
    k = cfg["shingle_size"]
    for i in order:
        if s.at[i, "duplicate_status"] != "canonical" or s.at[i, "n_chars"] < cfg["min_chars_for_near_dup"]:
            continue
        t = norm_for_hash(s.at[i, "text_model"])
        m = MinHash(num_perm=cfg["minhash_num_perm"], seed=1)
        for j in range(max(1, len(t) - k + 1)):
            m.update(t[j:j + k].encode())
        hits = lsh.query(m)
        if hits:
            canon = hits[0]
            s.at[i, "duplicate_status"] = "near_duplicate"
            s.at[i, "duplicate_reason"] = "minhash_near_duplicate"
            cid = s.at[canon, "duplicate_cluster_id"] or f"dc_mh_{canon}"
            s.at[canon, "duplicate_cluster_id"] = cid
            s.at[i, "duplicate_cluster_id"] = cid
        else:
            lsh.insert(i, m)
            mh[i] = m
    # reddit cross-posts
    xp = s.extra.fillna("").str.contains('"crosspost_parent": "t3_', regex=False)
    s.loc[xp, "is_cross_post"] = True
    s["is_cross_post"] = s.get("is_cross_post", False)
    s["is_cross_post"] = s["is_cross_post"].fillna(False).astype(bool)

    SILVER.mkdir(parents=True, exist_ok=True)
    s.to_parquet(SILVER / "silver.parquet", index=False)
    print("silver rows", len(s))
    print(s.groupby("platform").agg(n=("record_id", "size"), relevant=("is_relevant", "sum"),
                                    cannabis=("cannabis_context", "sum"), spam=("is_spam", "sum"),
                                    dup=("duplicate_status", lambda x: (x != "canonical").sum())))


if __name__ == "__main__":
    main()
