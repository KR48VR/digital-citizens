# Bayesian pooling, Singapore (20 questions x 10 groups), leave-one-question-out, design = total

Generated 2026-10-17 07:51 UTC; runtime 89s.

Design 'total' = one local survey of n respondents, each group gets whoever fell into it (realistic); 'per_group' = n from each group. Errors in points per answer option, average of 3 draws.

| method | pop_median | pop_mean | seg_median | seg_mean | gap_r | gap_slope | dispersion_ratio |
|---|---|---|---|---|---|---|---|
| claude zero-shot alone | 4.850 | 5.290 | 4.980 | 6.290 | 0.540 | 0.360 | 0.650 |
| record-anchored citizens alone | 2.950 | 3.720 | 3.660 | 4.540 | 0.730 | 0.420 | 0.660 |
| prior only (no local answers) | 2.510 | 3.480 | 3.380 | 4.460 | 0.720 | 0.400 | 0.620 |
| local survey of 150 alone | 2.220 | 2.210 | 4.800 | 5.300 | 0.450 | 0.840 | 2.100 |
| local survey of 300 alone | 1.750 | 1.750 | 3.560 | 3.900 | 0.650 | 0.900 | 1.670 |
| local survey of 600 alone | 1.420 | 1.360 | 2.730 | 3.040 | 0.730 | 0.890 | 1.210 |
| pooled + local survey of 150 | 1.880 | 1.920 | 2.950 | 3.620 | 0.590 | 0.570 | 0.800 |
| pooled + local survey of 300 | 1.590 | 1.620 | 2.650 | 3.140 | 0.720 | 0.690 | 0.850 |
| pooled + local survey of 600 | 1.350 | 1.300 | 2.400 | 2.690 | 0.740 | 0.770 | 0.990 |

Fitted source weights (worth in respondents, median over folds), by local sample size:

| local_n | claude zero-shot | record-anchored citizens |
|---|---|---|
| 0 | 27.400 | 97.300 |
| 150 | 11.400 | 35.800 |
| 300 | 9.500 | 31.800 |
| 600 | 8.200 | 26.900 |
