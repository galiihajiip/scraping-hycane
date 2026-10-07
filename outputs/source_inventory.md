# Source Inventory

Inventory date: 2026-10-08. Scope: project workspace (`/Users/macbookpro/Projects/hycane-scraping`) plus HYCANE/RISE materials found in `~/Downloads` and `~/Documents` (searched by filename; read-only). The workspace itself held only the 25 Markdown specification files; it had no datasets, scripts, `.env`, or Git repository before this run.

## A. Project specification pack (workspace)

| File | Type | Relevance | Key information | Use as factual source? | Assumption vs validated |
|---|---|---|---|---|---|
| CLAUDE.md, MASTER_PROMPT.md | Markdown | Execution contract | Targets (5k/10k/20k), access rules, phases, acceptance tests | Yes, for method/rules | Rules, not market facts |
| README.md, 00–22 *.md | Markdown | Method spec | Schema, codebook, query taxonomy, dashboard, QA, report structure | Yes, for method | Hypotheses explicitly labelled |
| SOURCES_VERIFIED_WHEN_PACK_CREATED.md | Markdown | API references | Official API doc URLs | Re-checked at runtime | — |

## B. HYCANE / competition materials (`~/Downloads`, `~/Documents`)

| File | Type | Relevance | Key information found | Factual source? | Assumption vs validated |
|---|---|---|---|---|---|
| Guidebook BPC RISE 2026.pdf (32 pp) | PDF | **High** — competition rules | Theme "From Vision to Venture…", subtheme Agroteknologi & Ketahanan Pangan; BPC proposal must include market analysis (Market Opportunity, Customer Analysis, Competitor Analysis, TAM/SAM/SOM, Customer Persona optional), STP, marketing mix, risk; appendices may include "hasil riset pasar/survei (jika ada)" | Yes (rules) | Official rules |
| Checklist BPC RISE 2026.pdf (3 pp) | PDF | High — reviewer checklist | Asks for evidence of the problem from target users (interviews, surveys, observation, or relevant secondary data), numbers with sources, validation evidence with respondent counts, tested willingness to pay | Yes (rules) | Shows what evidence reviewers expect |
| BMC HYCANE RISE.png | Image | **High** — current BMC | Segments: Indonesia (Java priority), age 20–40, middle income, environmentally aware, interested in smart farming, beginners to hobbyists; channels IG/TikTok/FB/Threads/WhatsApp, marketplace, communities, workshops, school/campus, direct B2B; revenue: kit, replacement media, nutrients & spare parts, B2B packages, workshops, premium feature subscription | No (it is the object under test) | **All segment/behaviour statements are assumptions** |
| BMC HYCANE.pdf / BMC HYCANE_Kami Pasti Juara(_UPNVJT).pdf | PDF | High | Same BMC content in text form | No | Assumptions |
| HYCANE_Proposal_BMC_LUMINUX_KamiPastiJuara.pdf (56 pp) / .docx | PDF/DOCX | **High** — main business source | Target urban/semi-urban, age 20–40, limited space, tech interest; TAM/SAM/SOM table (SOM 880,266); HPP Rp675,285/unit, price Rp910,000 (35% markup), 100-unit batch costing; marketing via IG/TikTok/YouTube | Business facts as the team's own figures only | TAM/SAM/SOM and pricing are team projections; no primary survey reported |
| BPC FESTAFORA 2026_…HYCANE(-2).pdf/.docx (15–16 pp) | PDF/DOCX | High | Year-1 target 400 kits; primary market survey listed as an early-stage agenda; validation **targets** (SUS ≥70, 30-day retention ≥60%, pH deviation ≤0.2, ≥50% willing to buy at Rp910,000, ≥40% media repurchase in 90 days) stated as targets, not results; personas described as illustrative, to be validated in a pilot | Team claims only | Explicitly unvalidated |
| RB_…HYCANE…_REVISI.pdf/.docx (AGTION 2026, 31 pp) | PDF/DOCX | Medium | Kit = compact hydroponic system + bagasse media + pH/TDS-EC/temperature/water-level IoT module + mobile app; IRR 33.61%, payback ~1 yr 10 mo "projections based on initial team assumptions, to be updated after prototype and market testing" | Team claims only | Projections |
| CaneBioKit (ASPIRE) .pdf/.docx + PPT | PDF/DOCX | Medium — technical concept | Bagasse matrix + beneficial microbes + ESP32 pH/EC/water-level IoT; states the concept will progress "toward an experimental prototype" | Technical concept only | Prototype not yet built/tested |
| MASTER_PROMPT_REVISI_PROPOSAL_AGTION_HYCANE.md, PROMPT_CLAUDE_BPC_RISE_2026_HYCANE.md | Markdown | Medium — prior prompts | Instructs not to fabricate market data/surveys; confirms team (Galih Aji Pangestu, Stevyka Frista Aninda, Putri Ayu Ajeng Nina Zuraida, UPN "Veteran" Jawa Timur) | No | — |
| HYCANE_Social_Listening_…zip / folder | Archive/folder | Duplicate | Same spec pack as the workspace | No | — |
| Ecobotanix (FESTAFORA 2025), LUMINUX/ASPIRE/EC/HoloMine/INCEPTION/MONE guidebooks, BMC templates | Various | Low/none | Other competitions or teams; Ecobotanix is a comparable biodegradable IoT hydroponic kit concept (cassava starch) — a potential competitor reference | No | — |
| "Prototype sticker PDF" (named in SOURCES_VERIFIED…) | — | — | **Not found** by filename search | — | Gap |

## C. Implications for this study

1. No primary customer evidence exists in the HYCANE materials; every segment, persona, price acceptance and feature-demand statement is a hypothesis. This study tests them against public discourse only (secondary, observational evidence).
2. The RISE checklist explicitly accepts "relevant secondary data" as problem evidence but also asks for respondent counts and tested willingness to pay, which social listening cannot supply. Primary validation stays required.
3. Price anchor for the pricing analysis: Rp910,000 per kit (team figure).
