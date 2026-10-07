"""Academic evidence collection: OpenAlex (primary), Crossref and Semantic Scholar (supplementary).

Output: data/gold/academic_evidence.parquet — a separate evidence stream, never merged with customer voice.
Method/sample/finding fields are abstract-derived heuristics and flagged as such; curated findings are written
by hand into outputs/academic_expert_synthesis.md with explicit citations.
"""
from __future__ import annotations

import re

import pandas as pd

from src.utils.common import ROOT, Checkpoint, Http, log_run, new_run_id, save_raw, utcnow

DOMAINS = {
    "adoption_barriers": ["hydroponic adoption barriers", "home hydroponics consumer adoption",
                          "urban agriculture hydroponics households motivation", "hidroponik rumah tangga perkotaan"],
    "beginner_knowledge": ["hydroponic farming knowledge training beginners", "hydroponic system failure causes"],
    "nutrients_ph_ec": ["hydroponic nutrient solution pH EC management", "electrical conductivity nutrient solution lettuce",
                        "nutrient solution temperature dissolved oxygen hydroponic"],
    "iot_monitoring": ["IoT hydroponic monitoring pH TDS", "smart hydroponic system sensor monitoring",
                       "internet of things hidroponik monitoring", "low-cost sensors hydroponics accuracy calibration"],
    "ai_prediction": ["machine learning hydroponics prediction", "artificial intelligence hydroponic anomaly detection",
                      "deep learning plant growth hydroponic"],
    "growing_media_bagasse": ["sugarcane bagasse growing media", "bagasse substrate hydroponic",
                              "biodegradable growing media rockwool alternative", "ampas tebu media tanam"],
    "sustainability": ["hydroponics sustainability life cycle assessment", "rockwool waste environmental impact",
                       "hydroponic water use efficiency"],
    "consumer_acceptance": ["consumer acceptance smart farming technology", "technology acceptance model smart agriculture",
                            "willingness to pay hydroponic vegetables", "consumer perception hydroponic produce"],
    "indonesia_context": ["hydroponics Indonesia urban farming", "urban farming Indonesia food security",
                          "hidroponik Indonesia"],
}

OA = Http("openalex", 0.25)
CR = Http("crossref", 0.5)
SS = Http("semantic_scholar", 3.5)
MAILTO = "params-mailto-omitted"


def inv_to_text(inv):
    if not inv:
        return ""
    pos = {}
    for w, idx in inv.items():
        for i in idx:
            pos[i] = w
    return " ".join(pos[i] for i in sorted(pos))


METHOD_RX = [("systematic_review", r"systematic review|meta-analy|scoping review|PRISMA"),
             ("review", r"\breview\b|state of the art|overview"),
             ("survey", r"survey|questionnaire|respondents|kuesioner|responden"),
             ("experiment", r"experiment|treatment|randomi[sz]ed|greenhouse trial|were grown|cultivated"),
             ("system_development", r"prototype|we (design|develop)|was (designed|developed)|implemented|arduino|esp32|raspberry"),
             ("modelling", r"model(l)?ing|simulation|machine learning|neural network|regression"),
             ("lca", r"life cycle assessment|\bLCA\b"),
             ("case_study", r"case study|interview")]


def heur_method(t):
    return "|".join(m for m, rx in METHOD_RX if re.search(rx, t, re.I)) or "unspecified"


def heur_sample(t):
    m = re.search(r"\b(n\s*=\s*\d+|\d{2,5}\s+(respondents|participants|farmers|households|consumers|users))", t, re.I)
    return m.group(0) if m else None


def main():
    run_id = new_run_id("academic")
    ck = Checkpoint("academic")
    started = utcnow()
    rows = []
    for dom, qs in DOMAINS.items():
        for q in qs:
            qid = f"AC_{dom}_{abs(hash(q)) % 10000:04d}"
            st, code, pl = OA.get("https://api.openalex.org/works",
                                  {"search": q, "per-page": 25, "sort": "relevance_score:desc",
                                   "filter": "type:article|review|book-chapter|proceedings-article,has_abstract:true"},
                                  "openalex_works", qid)
            if st != "SUCCESS":
                print("  ! openalex", q, st, code)
                continue
            path = save_raw("academic", run_id, f"openalex_{dom}_{q[:40]}", pl,
                            {"endpoint": "openalex/works", "query": q, "domain": dom, "stage": "openalex",
                             "access_method": "openalex_api"})
            for w in pl.get("results") or []:
                ab = inv_to_text(w.get("abstract_inverted_index"))
                loc = (w.get("primary_location") or {})
                src = (loc.get("source") or {})
                countries = sorted({c for a in w.get("authorships") or [] for c in (a.get("countries") or [])})
                rows.append(dict(
                    evidence_id=w["id"].split("/")[-1], source_type=w.get("type"), title=w.get("title"),
                    authors="; ".join(a["author"]["display_name"] for a in (w.get("authorships") or [])[:8]),
                    year=w.get("publication_year"), doi=w.get("doi"), url=loc.get("landing_page_url") or w.get("doi"),
                    publisher=src.get("host_organization_name"), journal=src.get("display_name"),
                    source_kind=src.get("type"), is_peer_reviewed_venue=src.get("type") == "journal",
                    cited_by=w.get("cited_by_count"), abstract=ab,
                    keywords="; ".join(k.get("display_name") for k in (w.get("keywords") or [])[:8]),
                    country="; ".join(countries), method=heur_method(ab), sample=heur_sample(ab),
                    finding=None, domain=dom, query=q, query_id=qid, retrieval_api="openalex",
                    raw_capture_path=path, retrieved_at=utcnow(), relevance_score=w.get("relevance_score")))
            print(f"  openalex [{q}] {len(pl.get('results') or [])}")
    # Semantic Scholar: supplementary TLDRs for top-cited items (rate-limited without key)
    df = pd.DataFrame(rows)
    df = df.sort_values(["relevance_score"], ascending=False).drop_duplicates("evidence_id")
    df["domains_all"] = df.evidence_id.map(pd.DataFrame(rows).groupby("evidence_id").domain.agg(
        lambda s: "|".join(sorted(set(s)))))
    # Crossref cross-check of DOI metadata (publisher/type) for a sample
    cr_ok = 0
    for i, r in df.head(60).iterrows():
        if not isinstance(r.doi, str) or not r.doi:
            continue
        doi = r.doi.replace("https://doi.org/", "")
        st, code, pl = CR.get(f"https://api.crossref.org/works/{doi}", None, "crossref_work", "AC_CROSSREF", doi)
        if st == "SUCCESS":
            m = pl.get("message", {})
            df.at[i, "crossref_type"] = m.get("type")
            df.at[i, "crossref_container"] = "; ".join(m.get("container-title") or [])
            cr_ok += 1
    df["evidence_strength"] = df.apply(
        lambda r: "E5" if r.is_peer_reviewed_venue and r.source_type in ("article", "review") else
        ("E4" if r.source_type in ("proceedings-article", "book-chapter") else "E3"), axis=1)
    out = ROOT / "data" / "gold" / "academic_evidence.parquet"
    out.parent.mkdir(parents=True, exist_ok=True)
    df.to_parquet(out, index=False)
    df.drop(columns=["abstract"]).to_csv(ROOT / "data" / "gold" / "academic_evidence_index.csv", index=False)
    log_run(run_id=run_id, source="academic", started_at=started, ended_at=utcnow(), status="SUCCESS",
            objects=len(df), note=f"crossref_checked={cr_ok}")
    print("academic works", len(df), "crossref checked", cr_ok)


if __name__ == "__main__":
    main()
