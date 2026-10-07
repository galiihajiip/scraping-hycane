# Academic & Expert Evidence Synthesis

These streams are kept separate from customer voice:
- **Academic:** 677 OpenAlex works across 9 domains (`data/gold/academic_evidence.parquet`). 48 DOIs were cross-checked in Crossref. 14 works were curated at abstract level (`config/academic_curated.yaml`).
- **Expert:** 7 institutional and practitioner sources read in full (`data/gold/expert_evidence.csv`). 3 unread sources were excluded.

Journal statements are used to interpret technical context, never as proof of customer demand.

## High-confidence findings (agree with customer signal)

1. **pH and EC/TDS are the core controllable variables.**
   - Extension guidance recommends weekly pH/EC monitoring (University of Kentucky CCD, EX002) and weekly testing with water changes about every two weeks for home growers (Illinois Extension, EX003).
   - A tropical trial found lettuce does best at EC ≈ 0.9–1.4 dS/m; excessive EC causes saline stress (W4414415519).
   - An Indonesian study (Jakarta) notes manual pH/TDS checks are error-prone (W4412063293).
   - *Customer side:* pH/EC monitoring is explicitly requested on 6 platforms.
2. **Root disease is the dominant failure and is driven by warm, low-oxygen water.**
   - CSU Extension identifies Pythium root rot as the most common root disease and prescribes cooler root zones (68–72°F) plus aeration (EX001).
   - University of Missouri/SARE training sets dissolved oxygen at ≥ 6 ppm and notes it falls as temperature rises (EX004).
   - *Customer side:* PLANT_HEALTH is the #1 pain; a tropical heat/rain topic appears in Indonesian discourse.
3. **Knowledge and education drive adoption.**
   - An Indonesian Edufarming case shows AIoT hydroponics diffuses through demonstrations and group learning (W7203544811).
   - A Surabaya household study lists inadequate technical knowledge among adoption constraints (W7160388792).
   - *Customer side:* education is the most requested feature.
4. **Cost is a barrier.**
   - High setup cost blocks low-income adoption (Cape Town, W7124698067; Surabaya, W7160388792).
   - Illinois Extension recommends cheap passive DIY systems over kits (EX003).
   - *Customer side:* cost is the #2 pain and DIY-substitution language is frequent.

## Conflicts and cautions

- **Sensors are not a full solution.**
  - UF/IFAS (EX005) finds constant-EC automated dosing wastes nutrients.
  - A 2023 review notes EC does not reveal individual ion levels (W4388723157).
  - HYCANE's recommendations must therefore be crop- and stage-aware, and "fully automatic" claims should be avoided.
- **Sustainability:**
  - Academic adoption models among Malang millennial farmers include sustainability awareness (W4416825938, n = 210; sample limited by design to ages 25–40, so it cannot test the age hypothesis).
  - Public discourse rarely voices sustainability, and hydroponics' higher energy use is acknowledged in the literature (W4388723157).
  - Treat as unresolved; test in primary research.
- **Market durability:** Scotts Miracle-Gro announced in Nov 2024 that it would shut down AeroGarden (EX006), which relaunched in 2025 (EX007). Consumer smart-garden economics are fragile, and app continuity matters to users.

## Gaps

- **Bagasse:** no study in the index tests sugarcane bagasse as a water-culture hydroponic seedling medium.
  - Closest analogues: coir + bagasse substrates for soilless tomato (W4293085516) and date-palm waste matching rockwool yield (W4390103616).
  - Indonesian bagasse studies are mostly soil mixes or mushroom substrates (W4385075181).
  - **Media efficacy is unproven.**
- **Most Indonesian IoT-hydroponic papers** are system builds or community-service reports. One reports monitoring time cut from ~3 h to ~30 min/day at a 200 m² business (W7115687377; single case, non-experimental). They show feasibility, not demand.
- **Willingness to pay:** none of the sources measure home growers' willingness to pay for IoT/AI kits in Indonesia.

## Implications

| Area | Implications |
|---|---|
| Product | pH/EC monitoring + stage-aware guidance; temperature/aeration guidance for the tropics; validate bagasse media before claiming performance |
| Segmentation | Beginners; small hydroponic SMEs as a credible B2B start (time saving) |
| Proposal | Cite extension/academic sources for *technical* claims and this study for *customer-signal* claims; label unvalidated items as hypotheses |

## Unresolved questions

1. Does bagasse media match rockwool or sponge on germination and rooting in NFT/rakit-apung systems?
2. What accuracy and calibration interval do low-cost pH probes achieve in Indonesian home conditions?
3. Is sustainability a hidden driver that people don't voice online? This needs a survey or experiment.
