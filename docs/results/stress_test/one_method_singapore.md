# One method, Singapore: a small real survey with and without AI

Generated 2026-10-17 14:27 UTC; runtime 616s; 10 draws per survey size; 20 questions x 9 groups.

Points off per answer option for each group: middle result over groups and questions of the
per-cell average across draws (average in brackets; 95% interval from resampling questions and
draws after it). Part of every score is chance in the people the estimate is checked against.

| method | survey of 150 | survey of 300 | survey of 600 |
|---|---|---|---|
| survey alone | 5.08 (5.21; 4.45-5.41) | 3.74 (3.90; 3.30-4.15) | 2.68 (2.94; 2.46-3.09) |
| + chatbot kind | 3.46 (4.30; 2.87-4.28) | 3.15 (3.59; 2.58-3.68) | 2.62 (2.94; 2.19-3.04) |
| + record citizens | 2.94 (3.64; 2.44-3.51) | 2.72 (3.18; 2.30-3.21) | 2.32 (2.75; 2.05-2.83) |
| + record citizens (own survey) | 3.62 (3.95; 3.15-4.13) | 2.90 (3.15; 2.59-3.35) | 2.46 (2.62; 2.15-2.81) |
| + demographics only (own survey) | 3.80 (4.10; 3.32-4.30) | 3.22 (3.40; 2.80-3.70) | 2.47 (2.72; 2.20-2.90) |
| + record citizens + chatbot kind | 2.91 (3.63; 2.37-3.54) | 2.74 (3.20; 2.26-3.24) | 2.38 (2.78; 2.06-2.84) |
| + record citizens (own survey) + chatbot kind | 3.13 (3.48; 2.61-3.55) | 2.71 (3.00; 2.38-3.04) | 2.35 (2.59; 2.01-2.68) |
| chatbot kind alone, no survey | 5.14 (6.31; 3.27-7.19) | 5.18 (6.32; 3.25-7.35) | 5.03 (6.39; 3.38-7.13) |
| record citizens alone, no survey | 3.68 (4.57; 2.65-4.98) | 3.71 (4.58; 2.71-5.01) | 3.79 (4.63; 2.66-5.18) |

Key comparisons (difference in points off, A minus B; negative means A is closer; 95% interval):

| A | B | difference | 95% interval |
|---|---|---|---|
| + record citizens, survey of 300 | survey alone, survey of 600 | +0.03 | -0.39 to +0.40 |
| + record citizens (own survey), survey of 150 | survey alone, survey of 300 | -0.12 | -0.57 to +0.37 |
| + record citizens (own survey), survey of 300 | survey alone, survey of 600 | +0.21 | -0.20 to +0.55 |
| + chatbot kind, survey of 150 | survey alone, survey of 300 | -0.28 | -0.74 to +0.48 |
| + chatbot kind, survey of 300 | survey alone, survey of 600 | +0.47 | -0.01 to +0.85 |
| + chatbot kind, survey of 150 | + record citizens (own survey), survey of 150 | -0.16 | -0.68 to +0.66 |
| + chatbot kind, survey of 300 | + record citizens (own survey), survey of 300 | +0.26 | -0.25 to +0.68 |
| + chatbot kind, survey of 600 | + record citizens (own survey), survey of 600 | +0.16 | -0.17 to +0.54 |
| + record citizens (own survey) + chatbot kind, survey of 150 | + record citizens (own survey), survey of 150 | -0.49 | -0.99 to -0.07 |
| + record citizens (own survey) + chatbot kind, survey of 300 | + record citizens (own survey), survey of 300 | -0.19 | -0.55 to +0.06 |
| + record citizens (own survey) + chatbot kind, survey of 600 | + record citizens (own survey), survey of 600 | -0.11 | -0.40 to +0.17 |
| + record citizens (own survey) + chatbot kind, survey of 150 | + chatbot kind, survey of 150 | -0.33 | -0.98 to -0.02 |
| + record citizens (own survey) + chatbot kind, survey of 300 | + chatbot kind, survey of 300 | -0.44 | -0.82 to -0.07 |
| + record citizens (own survey) + chatbot kind, survey of 600 | + chatbot kind, survey of 600 | -0.27 | -0.60 to +0.00 |
| + record citizens (own survey) + chatbot kind, survey of 300 | survey alone, survey of 600 | +0.02 | -0.36 to +0.25 |
| + record citizens + chatbot kind, survey of 300 | + record citizens, survey of 300 | +0.03 | -0.28 to +0.29 |

Worth of each AI source, in real respondents per group (middle of the leave-one-question-out fits):

| config | n | chat | rec_past | rec_own | demo_own |
|---|---|---|---|---|---|
| + chatbot kind | 150 | 31.6 |  |  |  |
| + chatbot kind | 300 | 32.3 |  |  |  |
| + chatbot kind | 600 | 32.2 |  |  |  |
| + demographics only (own survey) | 150 |  |  |  | 5000.0 |
| + demographics only (own survey) | 300 |  |  |  | 5000.0 |
| + demographics only (own survey) | 600 |  |  |  | 5000.0 |
| + record citizens | 150 |  | 58.4 |  |  |
| + record citizens | 300 |  | 57.9 |  |  |
| + record citizens | 600 |  | 57.3 |  |  |
| + record citizens (own survey) | 150 |  |  | 165.2 |  |
| + record citizens (own survey) | 300 |  |  | 259.5 |  |
| + record citizens (own survey) | 600 |  |  | 321.3 |  |
| + record citizens (own survey) + chatbot kind | 150 | 138.9 |  | 215.4 |  |
| + record citizens (own survey) + chatbot kind | 300 | 109.6 |  | 277.3 |  |
| + record citizens (own survey) + chatbot kind | 600 | 101.0 |  | 374.5 |  |
| + record citizens + chatbot kind | 150 | 15.0 | 47.9 |  |  |
| + record citizens + chatbot kind | 300 | 13.3 | 49.0 |  |  |
| + record citizens + chatbot kind | 600 | 12.4 | 47.7 |  |  |

Average number of people from each group in a sample:

| group | 150 | 300 | 600 |
|---|---|---|---|
| age_band=18-29 | 25.0 | 50.0 | 101.0 |
| age_band=60+ | 39.0 | 79.0 | 160.0 |
| education3=Higher | 76.0 | 154.0 | 306.0 |
| education3=Lower | 27.0 | 54.0 | 108.0 |
| ethnic=Chinese | 116.0 | 231.0 | 463.0 |
| ethnic=Indian | 14.0 | 28.0 | 57.0 |
| ethnic=Malay | 17.0 | 35.0 | 69.0 |
| religion=Muslim | 20.0 | 41.0 | 81.0 |
| religion=No religion | 36.0 | 71.0 | 141.0 |

