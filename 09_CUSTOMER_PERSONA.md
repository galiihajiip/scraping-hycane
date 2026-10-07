# 09 Customer Persona Construction

Generate personas from evidence, not stereotypes.

## Inputs
Experience, intent, pain points, outcomes, feature demand, price language, sustainability attitude, technology attitude, urban/small-space context, content behavior, and platform patterns.

## Clustering
Test KMeans, hierarchical clustering, and/or HDBSCAN. Do not fix the number before inspecting the data. Compare silhouette/stability, minimum cluster size, and qualitative interpretability.

## Persona card
Each persona must include:
- name;
- record count and corpus share;
- platforms/languages/timeframe;
- confidence;
- experience;
- context;
- goals;
- jobs-to-be-done;
- ranked pain points;
- desired outcomes;
- feature priorities;
- objections;
- purchase signals;
- trust drivers;
- relevant channels;
- anonymized evidence examples;
- source IDs.

## Important
Do not infer sensitive traits. Do not infer age from writing style. If age is rarely public, explicitly say the corpus does not validate age.

## Existing HYCANE segmentation validation
For urban/home grower, beginner, age 20-40, Indonesia/Java, middle-market, technology interest, sustainability interest, schools/universities, and B2B: classify as Supported, Partially Supported, Not Supported, or Not Enough Evidence.

## Strategy bridge
`persona -> problem -> feature -> message -> channel -> revenue opportunity`
