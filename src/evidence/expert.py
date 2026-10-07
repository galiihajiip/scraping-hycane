"""Expert / institutional / credible-practitioner evidence (separate stream; never counted as customer voice).

Each record was read in-session (WebFetch or local PDF text extraction) on the retrieval date. Statements are
paraphrases unless marked as quotes. Sources that could not be read (HTTP 403, unreadable PDF) are listed in
EXCLUDED with the reason, and are not used for findings.
"""
from __future__ import annotations

import pandas as pd

from src.utils.common import ROOT, sha256

RETRIEVED = "2026-10-08"
RECORDS = [
    dict(source_url="https://planttalk.colostate.edu/topics/miscellaneous/2043-root-disease-problems-management-hydroponic-systems/",
         expert_role="University extension (institutional guidance)", organization="Colorado State University Extension (PlantTalk Colorado)",
         expertise_domain="plant pathology / hydroponic root disease", publication_date=None, topic="PLANT_HEALTH|OXYGEN|TEMPERATURE",
         statement_summary="Root rot (mainly Pythium) is the most common root disease in hydroponic systems; it targets stressed plants. Management: root-zone temperature ~68-72°F, higher dissolved oxygen via aeration, clean/disinfected systems, balanced nutrient solution, regular monitoring of soluble salts and pH.",
         quote_or_paraphrase="QUOTE: \"Low oxygen levels in the nutrient solution favor disease so increase dissolved oxygen levels through proper aeration.\"",
         relevance="Supports temperature + oxygen + EC/pH monitoring as preventive levers against the most common failure mode.",
         credibility_notes="Land-grant university extension; no author/date shown.", evidence_strength="E5"),
    dict(source_url="https://ccd.uky.edu/sites/default/files/2025-06/ccd-ta-01_monitoring-ph-ec.pdf",
         expert_role="Extension associates / assistant extension professor", organization="University of Kentucky, Center for Crop Diversification (CCD-TA-01)",
         expertise_domain="greenhouse nutrient management", publication_date="2025-06", topic="PH|EC_TDS|SENSOR",
         statement_summary="Regular pH and EC monitoring is recommended for controlled-environment growers; a pH or EC meter provides a simple, accessible method for weekly monitoring; imbalanced pH causes stunted growth, leaf discoloration and yield penalties; EC indicates salinity/nutrient availability.",
         quote_or_paraphrase="QUOTE: \"using a pH or EC meter can provide a simple and accessible method for weekly monitoring.\"",
         relevance="Institutional basis that pH/EC are the core monitored variables; written for commercial greenhouse growers, not home beginners.",
         credibility_notes="Named authors: C. Byrd, Q. Ying, A. Sharma (UK Dept. of Horticulture). Commercial-grower audience.", evidence_strength="E5"),
    dict(source_url="https://extension.illinois.edu/blogs/good-growing/2017-09-07-home-hydroponics",
         expert_role="University extension educator blog", organization="University of Illinois Extension (Good Growing blog)",
         expertise_domain="home horticulture", publication_date="2017-09-07", topic="KNOWLEDGE|PH|EC_TDS|LIGHT|COST|WATER",
         statement_summary="Home hydroponics can supply greens year-round but needs supplemental light unless a very bright window is available; weekly pH and EC testing and full water changes about every two weeks are advised; DIY passive systems are economical relative to commercial kits; beginners should start with lettuce in a simple passive system.",
         quote_or_paraphrase="QUOTE: \"If you notice that your pH is off in your system...the nutrients become unavailable to the plants.\"",
         relevance="Directly addresses the home-grower segment: confirms routine-maintenance burden and recommends simple, low-cost passive systems (a contradiction risk for high-tech kits).",
         credibility_notes="Extension blog; author not named on page.", evidence_strength="E5"),
    dict(source_url="https://projects.sare.org/media/pdf/H/y/d/Hydroponic-problems-Class-3.pdf",
         expert_role="Field specialist in horticulture (training deck)", organization="University of Missouri Extension / North Central SARE (USDA NIFA award 2019-38640-29879)",
         expertise_domain="hydroponic crop problems", publication_date=None, topic="TEMPERATURE|OXYGEN|NUTRIENTS|EC_TDS|LIGHT|PLANT_HEALTH",
         statement_summary="Training material for growers: lists environmental problems, diseases, pests and algae; lettuce root-zone ~75°F and air never over 77°F; dissolved oxygen should be no less than 6 ppm and falls as temperature rises; burned tips indicate high EC/improper mixing; yellow foliage indicates lack of nutrients; leggy pale plants indicate poor light.",
         quote_or_paraphrase="PARAPHRASE of slides 'Temperature and dissolved oxygen' and 'Abiotic disorders' (J. C. Cabrera, field specialist).",
         relevance="Maps visible symptoms to measurable causes (temperature, DO, EC) — the logic HYCANE's anomaly/recommendation layer would encode.",
         credibility_notes="Named extension specialist; USDA-funded training project.", evidence_strength="E5"),
    dict(source_url="https://ask.ifas.ufl.edu/publication/AE610",
         expert_role="University researchers (extension publication)", organization="University of Florida IFAS Extension (EDIS AE610)",
         expertise_domain="hydroponic nutrient efficiency / sensing", publication_date=None, topic="SENSOR|AUTOMATION|NUTRIENTS|EC_TDS",
         statement_summary="In NFT lettuce, sensor-based monitoring and automated EC-based dosing improve precision but have limits: continuously replenishing premixed solution to hold a constant EC wastes nutrients and raises cost; nutrient supply should follow growth stage.",
         quote_or_paraphrase="QUOTE: \"Although sensor-based monitoring and automated dosing enhance precision, they have limitations.\"",
         relevance="Expert caution: sensors alone do not solve nutrient management — interpretation/recommendation matters. Supports AI-recommendation framing, cautions against 'automation solves everything' claims.",
         credibility_notes="Authors K. Vought, H. Bayabil, A. Martin-Ryals; commercial/NFT context.", evidence_strength="E5"),
    dict(source_url="https://texasstandard.org/stories/aerogarden-scotts-miracle-gro-shutting-down-gardening-kit-discontinued/",
         expert_role="Technology journalists (public radio)", organization="Texas Standard",
         expertise_domain="consumer technology market", publication_date="2024-11-14", topic="SOFTWARE|SUPPORT|COST",
         statement_summary="Scotts Miracle-Gro announced it would shut down the AeroGarden smart indoor-garden line after end of 2024, four years after acquiring it; product support would continue and devices could be used without the app; framed as a pandemic-era consumer-tech boom that did not sustain.",
         quote_or_paraphrase="QUOTE: \"Users can also still use the product without needing the app.\"",
         relevance="Market contradiction: the best-known consumer smart-hydroponic brand faced business viability problems; app dependency was a user concern.",
         credibility_notes="Journalism, not peer-reviewed; reason for closure not detailed.", evidence_strength="E3"),
    dict(source_url="https://www.bobvila.com/diy/aerogarden-relaunch-news/",
         expert_role="Home/DIY journalist", organization="Bob Vila",
         expertise_domain="consumer home products", publication_date="2025-03-07", topic="SOFTWARE|SUPPORT",
         statement_summary="AeroGarden announced a relaunch in spring 2025 after winding down in fall 2024 'due to numerous business challenges'; the company committed that the app would remain supported and updated and growth history kept.",
         quote_or_paraphrase="QUOTE: \"the app will also remain supported and updated.\"",
         relevance="Shows volatility of consumer smart-garden businesses and the importance of app/support continuity to users.",
         credibility_notes="Consumer journalism; ownership after relaunch not specified.", evidence_strength="E3"),
]
EXCLUDED = [
    dict(source_url="https://extension.okstate.edu/fact-sheets/electrical-conductivity-and-ph-guide-for-hydroponics.html",
         reason="HTTP 403 on fetch; not read, not used"),
    dict(source_url="BPTP Riau (2018) Petunjuk Teknis Budidaya Sayuran Hidroponik",
         reason="Located via search metadata only; full text not retrieved; not used for findings"),
    dict(source_url="FAO / InterAcademy 'Simplified hydroponics for urban agriculture'",
         reason="Located via search metadata only; not read; not used for findings"),
]


def main():
    df = pd.DataFrame(RECORDS)
    df.insert(0, "expert_evidence_id", [f"EX{i + 1:03d}" for i in range(len(df))])
    df["expert_name_hash"] = df.organization.map(lambda o: sha256(o)[:12])
    df["retrieved_at"] = RETRIEVED
    df.to_parquet(ROOT / "data" / "gold" / "expert_evidence.parquet", index=False)
    df.to_csv(ROOT / "data" / "gold" / "expert_evidence.csv", index=False)
    pd.DataFrame(EXCLUDED).to_csv(ROOT / "data" / "gold" / "expert_evidence_excluded.csv", index=False)
    print("expert records", len(df), "excluded", len(EXCLUDED))


if __name__ == "__main__":
    main()
