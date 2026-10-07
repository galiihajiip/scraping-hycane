# Persona Report (evidence-based discourse segments)

## Method
- **Unit:** 31,114 core customer-voice records with at least 2 informative discourse features. Most authors post once, so these are segments of *discourse*, not people.
- **Features:** 46 binary features (experience, intents, pains, feature mentions, price signals, sustainability, kit/brand, small-space, tech aspects, contradictions), TF-IDF weighted.
- **Model:** KMeans k = 2–8 compared on silhouette, bootstrap ARI, Ward agreement and minimum cluster share (`persona_model_selection.csv`). Selected k = 4: silhouette 0.13, bootstrap ARI 0.75, smallest cluster 16%.
- **Robustness** (`persona_robustness.json`):
  - ARI vs platform-balanced refit: 0.14.
  - ARI vs refit without YouTube: 0.46.
  - **The personas are fragile.** Use them as hypotheses for primary research.

**Not inferred:** age, gender, income, location. Too few records state an age explicitly (≈10) to test the 20–40 assumption.

## P0 — Self-identified Beginner
- **Size and sources:** n = 5,026 (16%). YouTube 70%, Reddit 19%, GardenWeb 8%. English 56%, Indonesian 40%.
- **Experience:** 100% explicit beginner signal ("pemula", "first time", "new to").
- **Jobs-to-be-done:** get a first system working; learn the basics.
- **Pains:** plant health (256), knowledge (103), small numbers of nutrient, equipment and temperature pains.
- **Desired outcomes:** clear steps; confidence; first successful harvest.
- **Features:** education (470 mentions, 15 explicit), community, beginner mode.
- **Objections and buying:** no purchase signals; price talk is about cheap starting options.
- **Trust drivers and channels:** creators who explain clearly; YouTube tutorials.
- **Evidence:** `persona_profiles.json` → example_record_ids (cluster 0).

## P1 — Pragmatic Evaluator / DIY Optimizer
- **Size and sources:** n = 16,374 (53%). YouTube 34%, Reddit 29%, GardenWeb 24%, Hacker News 4%. English 82%, Indonesian 17%.
- **Experience:** mostly unstated; 7% professional/commercial; 8% beginner.
- **Jobs-to-be-done:** choose the right system, parts and nutrients at the lowest cost; optimise an existing setup; advise others.
- **Pains:** plant health (2,875), cost (1,605), knowledge (1,190), nutrients (1,092), equipment (775), pH (562).
- **Features:** most monitoring talk sits here (TDS/EC 702 mentions, 44 explicit; pH 567, 31 explicit; logging, dashboard).
- **Objections:**
  - DIY is cheaper (38 PRICE_OVER_FEATURES);
  - passive systems are more reliable (157 ANTI_AUTOMATION);
  - subscription and pod lock-in (17);
  - energy use (28).
- **Buying signals:** 779 of the ~810 HIGH/MEDIUM purchase signals in the persona set.
- **Trust drivers:** specs, comparisons, peer experience.
- **Channels:** Reddit, forums, YouTube reviews.

**HYCANE relevance:** the most likely buyer *and* the toughest critic. Must be convinced on outcomes vs DIY cost.

## P2 — Tutorial-Inspired Learner
- **Size and sources:** n = 4,867 (16%). YouTube 76%. English 64%, Indonesian 35%.
- **Sentiment:** 48% positive.
- **Jobs-to-be-done:** get inspired; collect knowledge; maybe start later.
- **Pains:** few.
- **Features:** education (3,049 mentions, 77 explicit).
- **Buying signals:** almost none (5).

**HYCANE relevance:** top-of-funnel audience for content marketing and workshops, not an immediate buyer.

## P3 — Struggling Troubleshooter
- **Size and sources:** n = 4,847 (16%). Reddit 49%, GardenWeb 24%, YouTube 22%. English 85%, Indonesian 15%.
- **Intent:** 96% problem-solving.
- **Sentiment:** 33% negative.
- **Pains:** plant health (741), knowledge (270), nutrients (155), equipment, cost, pH.
- **Features:** diagnostics (148 mentions, 12 explicit), education, community.
- **Objections:** some return to soil (4 SOIL_PREFERENCE).

**HYCANE relevance:** experiences exactly the failures HYCANE monitoring + guidance targets; at risk of abandonment. Best pilot recruits.

## Validation of existing HYCANE segmentation
| Assumption | Verdict | Basis |
|---|---|---|
| Urban/home growers | Partially supported | Home/hobby scale dominates; small space is a context, not a voiced pain |
| Beginners | Supported | 84% of experience-stated records |
| Age 20–40 | Not enough evidence | Age is not observable |
| Indonesia (Java) | Partially supported | Active Indonesian discourse; Java untestable |
| Middle income | Not enough evidence | Frugality signals dominate |
| Eco-aware | Not supported as driver | — |
| Tech-interested | Partially supported | Niche: P1 subset |
| Schools/communities | Channels, not evidenced buyers | — |
| B2B | Small SMEs plausible; hotels/restaurants not evidenced | — |

## Strategy bridge (persona → problem → feature → message → channel → revenue)
| Persona | Problem | Feature | Message | Channel | Revenue |
|---|---|---|---|---|---|
| P0 | Doesn't know where to start | Guided start + education | "Panen pertamamu, dipandu langkah demi langkah" | YouTube creators, workshops | Starter kit |
| P1 | DIY cost vs reliability | pH/EC monitoring + logging | "Less guesswork than DIY, for less than a failed season" | Reddit/forums, review videos | Kit + sensor module + open refills |
| P2 | Inspired but not started | Free content, community | "Belajar bareng komunitas" | YouTube, Instagram/TikTok (untested) | Workshops, later kit |
| P3 | Plants keep dying | Diagnosis + alerts | "Know what's wrong before it's too late" | Problem-search content, communities | Kit + media refills |
