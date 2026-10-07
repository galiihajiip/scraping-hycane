# 08 Sentiment and Topic Modeling

## Sentiment pipeline
```text
raw text -> language routing -> candidate models -> validation sample -> model comparison -> calibrated labels -> analysis
```

Benchmark multiple approaches when practical: multilingual transformer, Indonesian-specific model, lexicon/rule baseline, zero-shot classifier, optional LLM-assisted classification. Select based on validation performance and qualitative fit, not novelty.

## Indonesian checks
Explicitly test negation (`tidak`, `bukan`, `belum`), slang (`ribet`, `parah`, `mantap`, `wkwk`), English code-switching, technical shorthand, sarcasm, and emoji.

## Evaluation
Report accuracy where appropriate, macro F1, per-class precision/recall, confusion matrix, label distribution, validation sample composition, model version, and thresholding.

## Topic pipeline
Combine:
- seeded business taxonomy;
- embeddings;
- clustering;
- BERTopic where appropriate;
- NMF/LDA fallback;
- keyphrase extraction;
- co-occurrence.

For every major topic provide top terms, representative real records, size, coherence proxy, sentiment, and platform distribution.

## Aspect sentiment
At minimum analyze ease of use, price, maintenance, nutrient management, pH, EC/TDS, water, temperature, oxygen, plant health, equipment, sensors, automation, software/app, AI, growing media, sustainability, support, and hydroponic kits.

## Feature demand
Keep explicit requests separate from pain-derived demand. Never turn every pain point into a feature requirement.
