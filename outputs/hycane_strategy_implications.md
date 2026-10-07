# HYCANE Strategy Implications

Chain: observed discourse → pain → job → outcome → HYCANE response → business value → proposal section. Mapping: `outputs/tables/hycane_feature_mapping.csv`.

## 1. Feature priorities (evidence-weighted)
| Priority | Feature | Customer evidence | External support | Decision |
|---|---|---|---|---|
| 1 | pH + TDS/EC monitoring with plain-language "what to do now" | EXPLICIT_REQUEST, 6 platforms; PH/EC/nutrient pains ≈ 2.5k | Extension EX002/EX003; W4414415519; W4412063293 | **Core** |
| 2 | Guided beginner mode + education library + community | Education 228 explicit (8 platforms); community 62; KNOWLEDGE pain top-5 | W7203544811; W7160388792; EX003 | **Core**, also the acquisition channel |
| 3 | Diagnosis (photo/symptom → cause → fix) | Diagnostics explicit (5 platforms); PLANT_HEALTH #1 pain | EX001; EX004 | **Core** (start rule-based / human-in-the-loop) |
| 4 | Water-temperature monitoring + heat guidance | Tropical heat/rain topic; TEMPERATURE pain rank 6 | EX001; EX004 | Include (low cost sensor) |
| 5 | Water-level alert / reminders | Strong inferred; reminder lights praised by smart-garden owners | — | Include, must work without opening the app |
| 6 | Logging/history/dashboard | Explicit (5 platforms), mostly Pragmatic Evaluators | — | Include, keep simple |
| 7 | "AI" anomaly detection | 1 mention; AI sentiment split | EX005 warns about automation limits | Present as diagnosis, not "AI" |
| 8 | Automated dosing | Contradicted by passive-system preference (189) | EX005 | Exclude from MVP |
| 9 | Bagasse biodegradable media | Not salient (18 mentions); rockwool complaints (~160) | Only analogues (W4293085516, W4390103616) | Keep as consumable; **lab-validate first**; market on convenience |

## 2. Proposal impact table
| Finding | Evidence level | Current proposal statement | Recommended change | Proposal section |
|---|---|---|---|---|
| Plant health, nutrients, pH and equipment failure are the most frequent recurring frictions | E3 cross-platform + E5 extension/academic (insight level 4) | Problem framed around urban land scarcity and food security | Add a user-level problem: "beginners lose plants to invisible water-chemistry and root problems" | Latar Belakang / Problem |
| Small space is a context, not a pain | E3 (rarely voiced as pain) | "Solusi urban farming pada ruang terbatas" as a headline value | Keep as a fit attribute; don't make it the main value | Value Proposition |
| Beginners are the most visible segment | E3 | "Pemula hingga pegiat hidroponik" | Make beginners primary; experienced hobbyists secondary | Customer Segments / STP |
| Age 20–40 untestable | E0 | "Usia 20–40 th" | Label as assumption; add an age question to the survey | Customer Segments |
| Sustainability is not a voiced purchase driver | E3 (absence) vs academic E4 | "Peduli lingkungan" as a behavioural segment | Move to brand/supporting message; lead with success/ease | Customer Segments / Marketing |
| Bagasse is not customer-salient; efficacy unproven | E3 (absence) + academic gap | Bagasse media as first value proposition | Reframe: "media tanam praktis, tidak gatal, mudah dibuang" (performance/convenience) + circularity; add lab validation | Value Proposition / Validation |
| Frugality / DIY substitution | E3 (7 platforms) + academic/expert E5 | Middle-income, Rp910,000 kit | Entry tier and price justification vs DIY + failure cost; test WTP | Revenue / Pricing |
| Subscription and app reliability concerns | E3 (low volume) + market event E3 | "Langganan fitur premium" | Make the kit fully usable without subscription; monetise open refills and workshops first | Revenue Streams |
| Education and community most requested | E3 + E4/E5 | Education listed under Customer Relationship | Elevate to a key channel (creator partnerships, workshops) | Channels / Customer Relationship |
| Indonesian YouTube is the main learning arena | E3 (30.7k ID records) | Channels: IG, TikTok, FB, Threads, WhatsApp | Add YouTube creator partnerships as a primary channel; IG/TikTok untested here | Channels / Marketing |
| B2B: small hydroponic businesses discuss monitoring time and capital | E2–E3 + E4 case study | Restaurants, hotels, supermarkets | Start with small hydroponic SMEs/farmer groups | Customer Segments (B2B) |

## 3. BMC changes
| Block | Change |
|---|---|
| Customer Segments | Primary: beginner home growers (Indonesia). Secondary: pragmatic hobbyists. B2B: small hydroponic SMEs. Age/income → "to validate". |
| Value Proposition | "Fewer dead plants: know your pH/nutrients and what to do next"; bagasse media = convenient, low-waste refill (after validation). |
| Channels | YouTube creator partnerships + workshops + community; marketplace for kits and refills. |
| Customer Relationships | In-app guided steps, community Q&A, diagnosis support. |
| Revenue Streams | Kit tiers (entry without sensors, monitoring add-on); open media/nutrient refills; workshops; premium software only after retention is proven. |
| Key Activities | Media lab validation; sensor calibration UX; content production. |
| Key Partners | Hydroponic YouTube creators/communities; extension/university labs for media testing. |
| Cost Structure | Content and community costs rise; AI R&D deprioritised to "diagnosis rules first". |

## 4. Message territories (from observed language; to test, not final slogans)
- **Success and confidence:** "panen pertama", "gak gagal lagi", "know what's wrong".
- **Guidance:** "step by step", "dipandu", "tutorial lengkap".
- **Practicality:** "praktis", "gak ribet", "mudah untuk pemula".
- **Value vs DIY:** "cheaper than a failed season".
- **Sustainability:** supporting line only.

## 5. Assumption register
| ID | Assumption | Reason | Evidence | Confidence | Validation plan |
|---|---|---|---|---|---|
| A1 | Beginners will pay for guidance + monitoring | Top pains are guidance-solvable | Pains E3; WTP E0 | Medium (problem) / Low (payment) | Concept + price test (n = 150) |
| A2 | Rp910,000 acceptable | Team costing | No WTP evidence; frugality signals | Low | Van Westendorp / Gabor-Granger |
| A3 | Bagasse media performs like rockwool | Concept | Academic gap | Low | Lab trial |
| A4 | Monitoring reduces failure | Expert logic | No field data | Medium | 4-week pilot |
| A5 | App alerts are used | Smart-garden owners value reminders | App complaints | Medium | Pilot retention D30 |
| A6 | YouTube creators drive acquisition | Indonesian learning arena | 30.7k ID YouTube records | Medium | Creator pilot campaign |
