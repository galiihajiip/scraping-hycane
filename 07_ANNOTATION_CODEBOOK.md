# 07 Annotation Codebook

## Sentiment
- POSITIVE
- NEUTRAL
- NEGATIVE
- MIXED
- AMBIGUOUS

## Experience
- NEVER_TRIED
- BEGINNER
- INTERMEDIATE
- EXPERIENCED
- PROFESSIONAL_COMMERCIAL
- UNKNOWN

Use explicit evidence only.

## Intent
- AWARENESS
- INSPIRATION
- INFORMATION_SEEKING
- PROBLEM_SOLVING
- COMPARISON
- PURCHASE_EXPLORATION
- EXPLICIT_PURCHASE_INTENT
- POST_PURCHASE
- RECOMMENDATION
- ABANDONMENT_FRUSTRATION
- UNKNOWN

## Pain points
SETUP, KNOWLEDGE, NUTRIENTS, PH, EC_TDS, WATER, TEMPERATURE, OXYGEN, PLANT_HEALTH, LIGHT, TIME, COST, SPACE, EQUIPMENT, SENSOR, AUTOMATION, SOFTWARE, AI, MEDIA, SUSTAINABILITY, SUPPORT.

## Outcomes
Ease, lower maintenance, less failure, clearer guidance, stable nutrient conditions, healthier plants, yield, lower cost, small-space usability, confidence, automation, sustainability.

## Feature demand
- EXPLICIT_REQUEST
- STRONG_INFERRED
- WEAK_INFERRED
- NO_EVIDENCE
- CONTRADICTORY

## Purchase signal
HIGH = explicit buy/order intent.
MEDIUM = price/recommendation inquiry in clear buying context.
LOW = general product curiosity.
NONE = no purchase signal.

## Sustainability signal
POSITIVE, NEUTRAL, SKEPTICAL, NEGATIVE, ABSENT.

## Evidence strength
E0 unsupported; E1 single anecdote; E2 repeated within one platform; E3 repeated cross-platform; E4 primary research/validated structured evidence; E5 direct peer-reviewed/official evidence.

## Annotation workflow
Build a stratified validation set, annotate, adjudicate disagreements, measure agreement, update rules, and rerun analysis.

Prefer short anonymized paraphrases in final reports. Keep source URLs internally.
