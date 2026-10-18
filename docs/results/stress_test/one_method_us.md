# One method, the United States: a small real survey with and without AI

Generated 2026-10-17 16:51 UTC; runtime 2457s; 10 draws per survey size; 25 questions x 6 groups.

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
| + record citizens (own survey) + chatbot kind | 2.95 (3.60; 2.68-3.54) | 2.90 (3.30; 2.52-3.33) | 2.67 (3.07; 2.37-3.01) |
| + last round's answers | 2.31 (2.92; 2.00-2.67) | 2.40 (2.93; 2.09-2.75) | 2.43 (2.94; 2.18-2.82) |
| + chatbot (Opus) | 3.30 (3.97; 2.82-4.07) | 3.18 (3.72; 2.75-3.73) | 2.97 (3.45; 2.70-3.41) |
| + chatbot (Sonnet) | 3.64 (4.23; 3.26-4.28) | 3.52 (3.86; 3.06-4.05) | 3.16 (3.45; 2.81-3.50) |
| + chatbot (Haiku) | 4.30 (4.82; 3.85-4.92) | 3.87 (4.19; 3.40-4.19) | 3.30 (3.61; 2.94-3.58) |
| + chatbot (Qwen, open, Asian-built) | 6.17 (6.63; 5.63-6.72) | 4.82 (5.18; 4.29-5.27) | 3.66 (3.99; 3.32-3.98) |
| + chatbot panel, averaged | 5.17 (5.29; 4.35-5.55) | 4.21 (4.53; 3.63-4.75) | 3.41 (3.77; 3.11-3.74) |
| + chatbot panel, each weighted | 3.23 (3.90; 2.85-4.06) | 3.19 (3.61; 2.76-3.72) | 2.96 (3.37; 2.65-3.38) |
| + record citizens (own survey) + chatbot panel, averaged | 3.71 (3.91; 3.27-4.08) | 3.33 (3.53; 2.86-3.64) | 2.84 (3.17; 2.54-3.08) |
| + record citizens (own survey) + chatbot panel, each weighted | 2.87 (3.33; 2.51-3.41) | 2.82 (3.19; 2.41-3.29) | 2.65 (3.04; 2.34-3.03) |
| + record citizens + chatbot panel, each weighted | 2.47 (3.00; 2.00-3.04) | 2.53 (3.02; 2.08-3.04) | 2.40 (2.91; 2.10-2.73) |
| + record citizens (own survey, 5 standard questions) | 4.68 (4.99; 4.20-5.20) | 3.96 (4.23; 3.40-4.32) | 3.24 (3.66; 2.93-3.62) |
| + record citizens (own survey, 10 standard questions) | 4.50 (4.87; 4.07-5.06) | 3.82 (4.13; 3.35-4.20) | 3.23 (3.59; 2.90-3.52) |
| + record citizens (own survey, 20 standard questions) | 4.41 (4.73; 3.94-4.91) | 3.75 (4.07; 3.34-4.17) | 3.22 (3.51; 2.82-3.44) |
| + record citizens (own survey, 10 standard questions) + chatbot kind | 3.23 (3.76; 2.82-3.83) | 3.13 (3.43; 2.70-3.53) | 2.97 (3.28; 2.59-3.24) |
| + record citizens (own survey, 20 standard questions) + chatbot kind | 3.21 (3.71; 2.79-3.78) | 3.12 (3.42; 2.70-3.52) | 2.88 (3.24; 2.55-3.15) |
| chatbot kind alone, no survey | 4.39 (5.15; 3.17-5.58) | 4.37 (5.11; 3.21-5.59) | 4.42 (5.18; 3.21-5.57) |
| record citizens alone, no survey | 2.43 (3.32; 2.08-3.01) | 2.48 (3.44; 2.17-3.01) | 2.52 (3.48; 2.19-3.16) |
| last round's answers alone, no survey | 2.37 (2.97; 1.94-2.78) | 2.39 (3.04; 2.10-2.85) | 2.50 (3.15; 2.11-3.00) |

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
| + record citizens (own survey) + chatbot kind, survey of 150 | + record citizens (own survey), survey of 150 | -1.27 | -1.60 to -0.64 |
| + record citizens (own survey) + chatbot kind, survey of 300 | + record citizens (own survey), survey of 300 | -0.55 | -0.91 to -0.13 |
| + record citizens (own survey) + chatbot kind, survey of 600 | + record citizens (own survey), survey of 600 | -0.24 | -0.53 to +0.03 |
| + record citizens (own survey) + chatbot kind, survey of 150 | + chatbot kind, survey of 150 | -0.81 | -1.13 to -0.18 |
| + record citizens (own survey) + chatbot kind, survey of 300 | + chatbot kind, survey of 300 | -0.48 | -0.88 to -0.16 |
| + record citizens (own survey) + chatbot kind, survey of 600 | + chatbot kind, survey of 600 | -0.52 | -0.74 to -0.14 |
| + record citizens (own survey) + chatbot kind, survey of 300 | survey alone, survey of 600 | -0.75 | -1.13 to -0.28 |
| + record citizens + chatbot kind, survey of 300 | + record citizens, survey of 300 | +0.06 | -0.23 to +0.38 |
| + chatbot panel, averaged, survey of 300 | + chatbot kind, survey of 300 | +0.82 | +0.25 to +1.35 |
| + chatbot panel, each weighted, survey of 300 | + chatbot kind, survey of 300 | -0.19 | -0.56 to +0.25 |
| + record citizens (own survey) + chatbot panel, averaged, survey of 300 | + record citizens (own survey) + chatbot kind, survey of 300 | +0.43 | +0.05 to +0.72 |
| + record citizens (own survey) + chatbot panel, each weighted, survey of 300 | + record citizens (own survey) + chatbot kind, survey of 300 | -0.08 | -0.36 to +0.25 |
| + record citizens (own survey, 5 standard questions), survey of 300 | + record citizens (own survey), survey of 300 | +0.51 | +0.03 to +0.84 |
| + record citizens (own survey, 10 standard questions), survey of 300 | + record citizens (own survey), survey of 300 | +0.37 | -0.02 to +0.70 |
| + record citizens (own survey, 20 standard questions), survey of 300 | + record citizens (own survey), survey of 300 | +0.30 | -0.06 to +0.66 |
| + record citizens (own survey, 10 standard questions) + chatbot kind, survey of 300 | + record citizens (own survey) + chatbot kind, survey of 300 | +0.23 | -0.08 to +0.55 |
| + record citizens (own survey, 20 standard questions) + chatbot kind, survey of 300 | + record citizens (own survey) + chatbot kind, survey of 300 | +0.21 | -0.12 to +0.54 |
| + record citizens, survey of 300 | + chatbot kind, survey of 300 | -0.94 | -1.41 to -0.46 |

Worth of each AI source, in real respondents per group (middle of the leave-one-question-out fits):

| config | n | chat | rec_past | rec_own | demo_own | last | chat_opus | chat_sonnet | chat_haiku | chat_qwen | chat_avg | rec_own_k5 | rec_own_k10 | rec_own_k20 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| + chatbot (Haiku) | 150 |  |  |  |  |  |  |  | 51.7 |  |  |  |  |  |
| + chatbot (Haiku) | 300 |  |  |  |  |  |  |  | 55.2 |  |  |  |  |  |
| + chatbot (Haiku) | 600 |  |  |  |  |  |  |  | 54.6 |  |  |  |  |  |
| + chatbot (Opus) | 150 |  |  |  |  |  | 120.6 |  |  |  |  |  |  |  |
| + chatbot (Opus) | 300 |  |  |  |  |  | 126.2 |  |  |  |  |  |  |  |
| + chatbot (Opus) | 600 |  |  |  |  |  | 122.2 |  |  |  |  |  |  |  |
| + chatbot (Qwen, open, Asian-built) | 150 |  |  |  |  |  |  |  |  | 1.7 |  |  |  |  |
| + chatbot (Qwen, open, Asian-built) | 300 |  |  |  |  |  |  |  |  | 2.1 |  |  |  |  |
| + chatbot (Qwen, open, Asian-built) | 600 |  |  |  |  |  |  |  |  | 1.7 |  |  |  |  |
| + chatbot (Sonnet) | 150 |  |  |  |  |  |  | 82.4 |  |  |  |  |  |  |
| + chatbot (Sonnet) | 300 |  |  |  |  |  |  | 84.9 |  |  |  |  |  |  |
| + chatbot (Sonnet) | 600 |  |  |  |  |  |  | 82.9 |  |  |  |  |  |  |
| + chatbot kind | 150 | 89.2 |  |  |  |  |  |  |  |  |  |  |  |  |
| + chatbot kind | 300 | 93.2 |  |  |  |  |  |  |  |  |  |  |  |  |
| + chatbot kind | 600 | 92.5 |  |  |  |  |  |  |  |  |  |  |  |  |
| + chatbot panel, averaged | 150 |  |  |  |  |  |  |  |  |  | 35.3 |  |  |  |
| + chatbot panel, averaged | 300 |  |  |  |  |  |  |  |  |  | 36.6 |  |  |  |
| + chatbot panel, averaged | 600 |  |  |  |  |  |  |  |  |  | 33.7 |  |  |  |
| + chatbot panel, each weighted | 150 | 18.5 |  |  |  |  | 80.0 | 28.3 | 7.4 | 0.0 |  |  |  |  |
| + chatbot panel, each weighted | 300 | 27.4 |  |  |  |  | 77.3 | 28.1 | 6.5 | 0.0 |  |  |  |  |
| + chatbot panel, each weighted | 600 | 31.9 |  |  |  |  | 66.2 | 31.4 | 9.5 | 0.0 |  |  |  |  |
| + demographics only (own survey) | 150 |  |  |  | 226.6 |  |  |  |  |  |  |  |  |  |
| + demographics only (own survey) | 300 |  |  |  | 182.3 |  |  |  |  |  |  |  |  |  |
| + demographics only (own survey) | 600 |  |  |  | 131.7 |  |  |  |  |  |  |  |  |  |
| + last round's answers | 150 |  |  |  |  | 324.6 |  |  |  |  |  |  |  |  |
| + last round's answers | 300 |  |  |  |  | 321.1 |  |  |  |  |  |  |  |  |
| + last round's answers | 600 |  |  |  |  | 291.4 |  |  |  |  |  |  |  |  |
| + record citizens | 150 |  | 322.3 |  |  |  |  |  |  |  |  |  |  |  |
| + record citizens | 300 |  | 320.1 |  |  |  |  |  |  |  |  |  |  |  |
| + record citizens | 600 |  | 291.4 |  |  |  |  |  |  |  |  |  |  |  |
| + record citizens (own survey) | 150 |  |  | 685.2 |  |  |  |  |  |  |  |  |  |  |
| + record citizens (own survey) | 300 |  |  | 955.4 |  |  |  |  |  |  |  |  |  |  |
| + record citizens (own survey) | 600 |  |  | 857.8 |  |  |  |  |  |  |  |  |  |  |
| + record citizens (own survey) + chatbot kind | 150 | 3077.0 |  | 3279.7 |  |  |  |  |  |  |  |  |  |  |
| + record citizens (own survey) + chatbot kind | 300 | 797.2 |  | 1257.6 |  |  |  |  |  |  |  |  |  |  |
| + record citizens (own survey) + chatbot kind | 600 | 437.7 |  | 1047.4 |  |  |  |  |  |  |  |  |  |  |
| + record citizens (own survey) + chatbot panel, averaged | 150 |  |  | 1532.2 |  |  |  |  |  |  | 590.2 |  |  |  |
| + record citizens (own survey) + chatbot panel, averaged | 300 |  |  | 1207.2 |  |  |  |  |  |  | 303.2 |  |  |  |
| + record citizens (own survey) + chatbot panel, averaged | 600 |  |  | 1033.8 |  |  |  |  |  |  | 167.3 |  |  |  |
| + record citizens (own survey) + chatbot panel, each weighted | 150 | 770.5 |  | 5000.0 |  |  | 4458.8 | 682.6 | 478.2 | 0.0 |  |  |  |  |
| + record citizens (own survey) + chatbot panel, each weighted | 300 | 398.7 |  | 2414.1 |  |  | 1231.9 | 262.5 | 137.9 | 0.0 |  |  |  |  |
| + record citizens (own survey) + chatbot panel, each weighted | 600 | 173.9 |  | 1530.1 |  |  | 493.5 | 135.2 | 88.2 | 0.0 |  |  |  |  |
| + record citizens (own survey, 10 standard questions) | 150 |  |  |  |  |  |  |  |  |  |  |  | 5000.0 |  |
| + record citizens (own survey, 10 standard questions) | 300 |  |  |  |  |  |  |  |  |  |  |  | 5000.0 |  |
| + record citizens (own survey, 10 standard questions) | 600 |  |  |  |  |  |  |  |  |  |  |  | 1039.9 |  |
| + record citizens (own survey, 10 standard questions) + chatbot kind | 150 | 5000.0 |  |  |  |  |  |  |  |  |  |  | 4692.4 |  |
| + record citizens (own survey, 10 standard questions) + chatbot kind | 300 | 3518.8 |  |  |  |  |  |  |  |  |  |  | 4646.2 |  |
| + record citizens (own survey, 10 standard questions) + chatbot kind | 600 | 466.0 |  |  |  |  |  |  |  |  |  |  | 840.8 |  |
| + record citizens (own survey, 20 standard questions) | 150 |  |  |  |  |  |  |  |  |  |  |  |  | 5000.0 |
| + record citizens (own survey, 20 standard questions) | 300 |  |  |  |  |  |  |  |  |  |  |  |  | 2060.6 |
| + record citizens (own survey, 20 standard questions) | 600 |  |  |  |  |  |  |  |  |  |  |  |  | 1007.8 |
| + record citizens (own survey, 20 standard questions) + chatbot kind | 150 | 5000.0 |  |  |  |  |  |  |  |  |  |  |  | 5000.0 |
| + record citizens (own survey, 20 standard questions) + chatbot kind | 300 | 1533.2 |  |  |  |  |  |  |  |  |  |  |  | 2008.3 |
| + record citizens (own survey, 20 standard questions) + chatbot kind | 600 | 490.4 |  |  |  |  |  |  |  |  |  |  |  | 958.8 |
| + record citizens (own survey, 5 standard questions) | 150 |  |  |  |  |  |  |  |  |  |  | 5000.0 |  |  |
| + record citizens (own survey, 5 standard questions) | 300 |  |  |  |  |  |  |  |  |  |  | 5000.0 |  |  |
| + record citizens (own survey, 5 standard questions) | 600 |  |  |  |  |  |  |  |  |  |  | 835.8 |  |  |
| + record citizens + chatbot kind | 150 | 104.7 | 328.2 |  |  |  |  |  |  |  |  |  |  |  |
| + record citizens + chatbot kind | 300 | 107.7 | 299.5 |  |  |  |  |  |  |  |  |  |  |  |
| + record citizens + chatbot kind | 600 | 89.1 | 285.4 |  |  |  |  |  |  |  |  |  |  |  |
| + record citizens + chatbot panel, each weighted | 150 | 46.7 | 308.3 |  |  |  | 82.2 | 0.0 | 4.2 | 0.0 |  |  |  |  |
| + record citizens + chatbot panel, each weighted | 300 | 58.0 | 288.4 |  |  |  | 76.5 | 0.0 | 3.7 | 0.0 |  |  |  |  |
| + record citizens + chatbot panel, each weighted | 600 | 56.0 | 282.4 |  |  |  | 50.3 | 0.0 | 2.1 | 0.0 |  |  |  |  |

Average number of people from each group in a sample:

| group | 150 | 300 | 600 |
|---|---|---|---|
| age_band=18-29 | 23.0 | 46.0 | 92.0 |
| age_band=65+ | 34.0 | 68.0 | 134.0 |
| education=Bachelor's or higher | 54.0 | 108.0 | 218.0 |
| party3=Democrat (incl. leaners) | 62.0 | 122.0 | 246.0 |
| party3=Republican (incl. leaners) | 47.0 | 93.0 | 186.0 |
| race_eth=Black, non-Hispanic | 30.0 | 59.0 | 117.0 |

