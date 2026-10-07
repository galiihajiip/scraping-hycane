# Executive Summary — HYCANE Social Listening

**Scope.**
- 136,019 unique public posts and comments were collected from 8 platforms: YouTube, Reddit, GardenWeb forum, Mastodon, Hacker News, Bluesky, Lemmy and Stack Exchange.
- After screening: **93,125 gold records**, of which **91,068 are core customer voice**. 30,703 are Indonesian-language.
- Discourse spans 2002–2026; data was collected 7–8 Oct 2026.
- This is observed public discourse, not a population survey.

Source tables are in `outputs/tables/`.

## What people struggle with
Pains ranked by priority (`pain_point_summary.csv`; stable across 8 sensitivity checks, min Spearman 0.96):
1. **Plant health:** root rot, yellowing, wilting, pests (4,754 records; all 8 platforms).
2. **Nutrients:** mixing, AB mix, deficiencies (1,393).
3. **pH control** (687).
4. **Equipment failure:** pumps, leaks, clogs (977).
5. **Beginner knowledge / confusion** (1,688).
6. **Water temperature / heat**, including a tropical "rain, roof, heat" topic in Indonesian videos (459).

**Cost** is the 2nd most frequent pain (1,925 records) but has lower severity.

## What they ask for
Explicit requests (`feature_demand.csv`):

| Request | Explicit requests | Platforms |
|---|---:|---:|
| Education/tutorials | 228 | 8 |
| Community | 62 | 7 |
| TDS/EC monitoring | 46 | 6 |
| pH monitoring | 31 | 6 |
| Logging/history | 30 | 5 |
| Diagnosis | 18 | 5 |

People ask for answers and guidance. "AI" and "anomaly detection" are almost never named.

## What challenges the HYCANE concept
- **Bagasse:** customers don't talk about it as a growing medium (18 of 91k records). Public bagasse talk is mostly tableware and energy.
- **Sustainability:** positive sustainability language in only 0.65% of records. It accompanies 11% of purchase-signal records vs 33% for price.
- **Frugality and DIY:** cheap/DIY language outnumbers premium language about 5:1. "I can build it for a fraction" recurs across 7 platforms.
- **Passive systems:** a no-electronics culture (Kratky, wick) appears on all 8 platforms (189 records).
- **Subscriptions and apps:** seed-pod/subscription lock-in and unreliable app alerts draw complaints. AeroGarden's 2024 shutdown announcement shows the business risk.

## Who they are
Four fragile discourse segments, to test in primary research:
- Self-identified Beginner (16%)
- Pragmatic Evaluator / DIY Optimizer (53%; holds most purchase signals)
- Tutorial-Inspired Learner (16%)
- Struggling Troubleshooter (16%)

Age, income and Java location cannot be validated from this data.

## Verdicts on current HYCANE assumptions
| Verdict | Hypotheses |
|---|---|
| Supported | Beginners; pH/EC monitoring demand |
| Partially supported | Home/urban growers; Indonesian discourse; tech interest; AI as "diagnosis"; small-SME B2B |
| Not supported | Sustainability as purchase driver; bagasse as customer-recognised value |
| Not enough evidence | Age 20–40; price acceptance; schools as buyers; app subscription |

Detail: `hypothesis_validation.csv`.

## Recommendation
Position HYCANE as **"a guided kit that keeps beginners' plants alive"**:
- pH/EC monitoring plus plain-language next steps at the core;
- education and community (YouTube creators, workshops) as the main channel;
- tropical heat guidance;
- bagasse media sold on convenience and performance once lab-validated, with sustainability as supporting proof;
- pricing justified against DIY plus failure costs, with an entry tier;
- no mandatory subscription.

**Before making hard claims, validate:** price acceptance at Rp910,000, bagasse media performance, and a 4-week home pilot.
