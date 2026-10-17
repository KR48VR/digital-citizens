# One method, the United States: a small real survey with and without AI

Generated 2026-10-17 14:29 UTC; runtime 696s; 10 draws per survey size; 25 questions x 6 groups.

Points off per answer option for each group: middle result over groups and questions of the
per-cell average across draws (average in brackets; 95% interval from resampling questions and
draws after it). Part of every score is chance in the people the estimate is checked against.

| method | survey of 150 | survey of 300 | survey of 600 |
|---|---|---|---|
| survey alone | 6.37 (6.81; 5.73-6.82) | 4.90 (5.22; 4.37-5.35) | 3.65 (3.99; 3.32-4.00) |
| + chatbot kind | 3.76 (4.31; 3.04-4.43) | 3.38 (3.84; 2.94-3.93) | 3.20 (3.48; 2.77-3.42) |
| + record citizens | 2.43 (3.21; 2.09-2.92) | 2.44 (3.24; 2.11-2.86) | 2.39 (3.03; 2.10-2.75) |
| + record citizens (own survey) | 4.22 (4.46; 3.78-4.64) | 3.45 (3.76; 3.05-3.82) | 2.92 (3.31; 2.64-3.21) |
| + demographics only (own survey) | 5.09 (5.41; 4.50-5.64) | 4.38 (4.65; 3.82-4.79) | 3.53 (3.83; 3.17-3.80) |
| + record citizens + chatbot kind | 2.50 (3.03; 2.03-3.04) | 2.50 (3.02; 2.11-2.99) | 2.34 (2.91; 2.09-2.70) |
| + record citizens (own survey) + chatbot kind | 2.93 (3.60; 2.68-3.54) | 2.90 (3.30; 2.52-3.33) | 2.67 (3.07; 2.37-3.01) |
| + last round's answers | 2.31 (2.92; 2.00-2.67) | 2.40 (2.93; 2.09-2.75) | 2.43 (2.94; 2.18-2.82) |
| chatbot kind alone, no survey | 4.39 (5.15; 3.16-5.72) | 4.37 (5.11; 3.21-5.61) | 4.42 (5.18; 3.29-5.72) |
| record citizens alone, no survey | 2.43 (3.32; 2.08-3.02) | 2.48 (3.44; 2.16-3.03) | 2.52 (3.48; 2.20-3.16) |
| last round's answers alone, no survey | 2.37 (2.97; 1.95-2.79) | 2.39 (3.04; 2.10-2.83) | 2.50 (3.15; 2.12-3.00) |

Key comparisons (difference in points off, A minus B; negative means A is closer; 95% interval):

| A | B | difference | 95% interval |
|---|---|---|---|
| + record citizens, survey of 300 | survey alone, survey of 600 | -1.21 | -1.56 to -0.75 |
| + record citizens (own survey), survey of 150 | survey alone, survey of 300 | -0.68 | -1.12 to -0.18 |
| + record citizens (own survey), survey of 300 | survey alone, survey of 600 | -0.20 | -0.54 to +0.17 |
| + chatbot kind, survey of 150 | survey alone, survey of 300 | -1.14 | -1.79 to -0.40 |
| + chatbot kind, survey of 300 | survey alone, survey of 600 | -0.27 | -0.69 to +0.28 |
| + chatbot kind, survey of 150 | + record citizens (own survey), survey of 150 | -0.46 | -1.10 to +0.20 |
| + chatbot kind, survey of 300 | + record citizens (own survey), survey of 300 | -0.07 | -0.47 to +0.52 |
| + chatbot kind, survey of 600 | + record citizens (own survey), survey of 600 | +0.28 | -0.11 to +0.47 |
| + record citizens (own survey) + chatbot kind, survey of 300 | + record citizens (own survey), survey of 300 | -0.55 | -0.91 to -0.13 |
| + record citizens + chatbot kind, survey of 300 | + record citizens, survey of 300 | +0.06 | -0.23 to +0.38 |

Worth of each AI source, in real respondents per group (middle of the leave-one-question-out fits):

| config | n | chat | rec_past | rec_own | demo_own | last |
|---|---|---|---|---|---|---|
| + chatbot kind | 150 | 89.2 |  |  |  |  |
| + chatbot kind | 300 | 93.2 |  |  |  |  |
| + chatbot kind | 600 | 92.5 |  |  |  |  |
| + demographics only (own survey) | 150 |  |  |  | 226.6 |  |
| + demographics only (own survey) | 300 |  |  |  | 182.3 |  |
| + demographics only (own survey) | 600 |  |  |  | 131.7 |  |
| + last round's answers | 150 |  |  |  |  | 324.6 |
| + last round's answers | 300 |  |  |  |  | 321.1 |
| + last round's answers | 600 |  |  |  |  | 291.4 |
| + record citizens | 150 |  | 322.3 |  |  |  |
| + record citizens | 300 |  | 320.1 |  |  |  |
| + record citizens | 600 |  | 291.4 |  |  |  |
| + record citizens (own survey) | 150 |  |  | 685.2 |  |  |
| + record citizens (own survey) | 300 |  |  | 955.4 |  |  |
| + record citizens (own survey) | 600 |  |  | 857.8 |  |  |
| + record citizens (own survey) + chatbot kind | 150 | 3077.0 |  | 3279.6 |  |  |
| + record citizens (own survey) + chatbot kind | 300 | 797.2 |  | 1257.6 |  |  |
| + record citizens (own survey) + chatbot kind | 600 | 437.7 |  | 1047.4 |  |  |
| + record citizens + chatbot kind | 150 | 104.7 | 328.2 |  |  |  |
| + record citizens + chatbot kind | 300 | 107.7 | 299.5 |  |  |  |
| + record citizens + chatbot kind | 600 | 89.1 | 285.4 |  |  |  |

Average number of people from each group in a sample:

| group | 150 | 300 | 600 |
|---|---|---|---|
| age_band=18-29 | 23.0 | 46.0 | 92.0 |
| age_band=65+ | 34.0 | 68.0 | 134.0 |
| education=Bachelor's or higher | 54.0 | 108.0 | 218.0 |
| party3=Democrat (incl. leaners) | 62.0 | 122.0 | 246.0 |
| party3=Republican (incl. leaners) | 47.0 | 93.0 | 186.0 |
| race_eth=Black, non-Hispanic | 30.0 | 59.0 | 117.0 |

