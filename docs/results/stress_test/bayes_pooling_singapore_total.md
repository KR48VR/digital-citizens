# Bayesian pooling, Singapore (20 questions x 10 groups), leave-one-question-out, design = total

Generated 2026-10-17 04:53 UTC; runtime 1804s.

Design 'total' = one local survey of n respondents, each group gets whoever fell into it (realistic); 'per_group' = n from each group. Errors in points per answer option, average of 3 draws.

| method | pop_median | pop_mean | seg_median | seg_mean | gap_r | gap_slope | dispersion_ratio |
|---|---|---|---|---|---|---|---|
| claude zero-shot alone | 4.850 | 5.290 | 4.980 | 6.290 | 0.540 | 0.360 | 0.650 |
| record-anchored citizens alone | 2.950 | 3.720 | 3.660 | 4.540 | 0.730 | 0.420 | 0.660 |
| prior only (no local answers) | 2.510 | 3.480 | 3.380 | 4.460 | 0.720 | 0.400 | 0.620 |
| pooled + local survey of 150 | 1.150 | 1.320 | 2.290 | 3.020 | 0.750 | 0.620 | 0.750 |
| local survey of 150 alone | 0.990 | 1.240 | 2.360 | 2.900 | 0.820 | 0.950 | 1.380 |
| pooled + local survey of 300 | 0.750 | 0.850 | 1.610 | 2.190 | 0.860 | 0.790 | 0.670 |
| local survey of 300 alone | 0.780 | 0.830 | 1.700 | 1.900 | 0.910 | 0.990 | 1.250 |
| pooled + local survey of 600 | 0.440 | 0.470 | 1.100 | 1.390 | 0.930 | 0.860 | 0.810 |
| local survey of 600 alone | 0.410 | 0.470 | 1.050 | 1.150 | 0.960 | 0.960 | 1.040 |

Fitted source weights (worth in respondents, median over folds), by local sample size:

| local_n | claude zero-shot | record-anchored citizens |
|---|---|---|
| 0 | 27.400 | 97.300 |
| 150 | 11.400 | 35.800 |
| 300 | 9.500 | 31.800 |
| 600 | 8.200 | 26.900 |
