# 11 Validation and Statistics

## Basic reporting
For every major result report n, denominator, percentage, timeframe, platform/source scope, and exclusions.

## Cross-platform tests
Where assumptions permit, use chi-square/Fisher tests, effect sizes, bootstrap differences, or other suitable methods. Do not report p-values without practical context.

## Robustness
Run at least:
1. all data;
2. high-confidence sentiment only;
3. dominant-thread-controlled;
4. spam-excluded;
5. duplicate-excluded.

Check whether the top findings remain stable.

## Persona robustness
Test alternate cluster counts, random seeds, platform-balanced samples, and dominant-platform removal. Mark fragile personas.

## Saturation
Track `new_high_value_topics_per_100_new_records`. Document diminishing returns instead of declaring saturation merely because a numeric target was met.

## Data-quality statistics
Compute duplicate rate, spam rate, irrelevant rate, missing timestamp rate, language confidence, geo-known rate, source error rate, and blocked-source rate.

## Model evaluation
Report precision, recall, macro F1, confusion matrix, class distribution, validation sample composition, and model versions.

## Forbidden statistical claims
Do not convert sentiment into market size, likes into willingness-to-pay, platform demographics into project demographics, or social counts into national prevalence.
