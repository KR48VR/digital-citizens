# One method, Singapore: a small real survey with and without AI

Generated 2026-10-17 16:49 UTC; runtime 2324s; 10 draws per survey size; 20 questions x 9 groups.

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
| + chatbot (Opus) | 3.20 (3.87; 2.77-3.64) | 3.05 (3.36; 2.50-3.41) | 2.43 (2.87; 2.12-2.89) |
| + chatbot (Sonnet) | 3.34 (4.08; 2.99-3.87) | 3.11 (3.48; 2.67-3.63) | 2.50 (2.88; 2.25-2.94) |
| + chatbot (Haiku) | 3.81 (4.53; 3.28-4.32) | 3.33 (3.73; 2.80-3.86) | 2.69 (2.98; 2.29-3.01) |
| + chatbot (Qwen, open, Asian-built) | 5.02 (5.14; 4.36-5.42) | 3.69 (3.85; 3.24-4.14) | 2.69 (2.96; 2.43-3.12) |
| + chatbot panel, averaged | 3.77 (4.56; 3.34-4.54) | 3.27 (3.64; 2.86-3.74) | 2.70 (2.96; 2.30-2.99) |
| + chatbot panel, each weighted | 3.19 (4.02; 2.78-3.73) | 3.03 (3.46; 2.49-3.50) | 2.51 (2.95; 2.16-2.95) |
| + record citizens (own survey) + chatbot panel, averaged | 3.12 (3.55; 2.73-3.54) | 2.65 (2.99; 2.38-3.09) | 2.39 (2.59; 2.07-2.69) |
| + record citizens (own survey) + chatbot panel, each weighted | 2.79 (3.26; 2.43-3.17) | 2.53 (2.92; 2.25-2.90) | 2.31 (2.59; 2.00-2.61) |
| + record citizens + chatbot panel, each weighted | 2.90 (3.68; 2.41-3.56) | 2.72 (3.21; 2.28-3.29) | 2.42 (2.80; 2.05-2.85) |
| + record citizens (own survey, 5 standard questions) | 3.67 (3.95; 3.21-4.08) | 3.07 (3.29; 2.73-3.54) | 2.46 (2.68; 2.15-2.84) |
| + record citizens (own survey, 10 standard questions) | 3.65 (3.93; 3.17-4.06) | 3.10 (3.27; 2.71-3.52) | 2.47 (2.67; 2.18-2.82) |
| + record citizens (own survey, 20 standard questions) | 3.59 (3.95; 3.19-4.10) | 2.97 (3.25; 2.61-3.53) | 2.55 (2.68; 2.21-2.86) |
| + record citizens (own survey, 10 standard questions) + chatbot kind | 3.22 (3.64; 2.77-3.80) | 2.91 (3.20; 2.51-3.34) | 2.40 (2.64; 2.06-2.75) |
| + record citizens (own survey, 20 standard questions) + chatbot kind | 3.27 (3.62; 2.77-3.76) | 2.82 (3.14; 2.44-3.27) | 2.39 (2.65; 2.08-2.76) |
| chatbot kind alone, no survey | 5.14 (6.31; 3.28-7.17) | 5.18 (6.32; 3.23-7.35) | 5.03 (6.39; 3.32-7.27) |
| record citizens alone, no survey | 3.68 (4.57; 2.66-4.97) | 3.71 (4.58; 2.71-5.03) | 3.79 (4.63; 2.68-5.18) |

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
| + chatbot panel, averaged, survey of 300 | + chatbot kind, survey of 300 | +0.11 | -0.30 to +0.49 |
| + chatbot panel, each weighted, survey of 300 | + chatbot kind, survey of 300 | -0.12 | -0.49 to +0.18 |
| + record citizens (own survey) + chatbot panel, averaged, survey of 300 | + record citizens (own survey) + chatbot kind, survey of 300 | -0.06 | -0.31 to +0.30 |
| + record citizens (own survey) + chatbot panel, each weighted, survey of 300 | + record citizens (own survey) + chatbot kind, survey of 300 | -0.18 | -0.44 to +0.10 |
| + record citizens (own survey, 5 standard questions), survey of 300 | + record citizens (own survey), survey of 300 | +0.18 | -0.12 to +0.51 |
| + record citizens (own survey, 10 standard questions), survey of 300 | + record citizens (own survey), survey of 300 | +0.20 | -0.16 to +0.47 |
| + record citizens (own survey, 20 standard questions), survey of 300 | + record citizens (own survey), survey of 300 | +0.08 | -0.21 to +0.43 |
| + record citizens (own survey, 10 standard questions) + chatbot kind, survey of 300 | + record citizens (own survey) + chatbot kind, survey of 300 | +0.21 | -0.09 to +0.54 |
| + record citizens (own survey, 20 standard questions) + chatbot kind, survey of 300 | + record citizens (own survey) + chatbot kind, survey of 300 | +0.12 | -0.14 to +0.46 |

Worth of each AI source, in real respondents per group (middle of the leave-one-question-out fits):

| config | n | chat | rec_past | rec_own | demo_own | chat_opus | chat_sonnet | chat_haiku | chat_qwen | chat_avg | rec_own_k5 | rec_own_k10 | rec_own_k20 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| + chatbot (Haiku) | 150 |  |  |  |  |  |  | 18.9 |  |  |  |  |  |
| + chatbot (Haiku) | 300 |  |  |  |  |  |  | 19.8 |  |  |  |  |  |
| + chatbot (Haiku) | 600 |  |  |  |  |  |  | 20.8 |  |  |  |  |  |
| + chatbot (Opus) | 150 |  |  |  |  | 37.4 |  |  |  |  |  |  |  |
| + chatbot (Opus) | 300 |  |  |  |  | 38.7 |  |  |  |  |  |  |  |
| + chatbot (Opus) | 600 |  |  |  |  | 38.0 |  |  |  |  |  |  |  |
| + chatbot (Qwen, open, Asian-built) | 150 |  |  |  |  |  |  |  | 1.2 |  |  |  |  |
| + chatbot (Qwen, open, Asian-built) | 300 |  |  |  |  |  |  |  | 1.4 |  |  |  |  |
| + chatbot (Qwen, open, Asian-built) | 600 |  |  |  |  |  |  |  | 1.5 |  |  |  |  |
| + chatbot (Sonnet) | 150 |  |  |  |  |  | 26.2 |  |  |  |  |  |  |
| + chatbot (Sonnet) | 300 |  |  |  |  |  | 27.0 |  |  |  |  |  |  |
| + chatbot (Sonnet) | 600 |  |  |  |  |  | 27.3 |  |  |  |  |  |  |
| + chatbot kind | 150 | 31.6 |  |  |  |  |  |  |  |  |  |  |  |
| + chatbot kind | 300 | 32.3 |  |  |  |  |  |  |  |  |  |  |  |
| + chatbot kind | 600 | 32.2 |  |  |  |  |  |  |  |  |  |  |  |
| + chatbot panel, averaged | 150 |  |  |  |  |  |  |  |  | 17.6 |  |  |  |
| + chatbot panel, averaged | 300 |  |  |  |  |  |  |  |  | 18.4 |  |  |  |
| + chatbot panel, averaged | 600 |  |  |  |  |  |  |  |  | 18.5 |  |  |  |
| + chatbot panel, each weighted | 150 | 10.5 |  |  |  | 21.9 | 6.3 | 0.9 | 0.7 |  |  |  |  |
| + chatbot panel, each weighted | 300 | 9.2 |  |  |  | 23.3 | 7.2 | 1.7 | 0.8 |  |  |  |  |
| + chatbot panel, each weighted | 600 | 11.2 |  |  |  | 18.3 | 6.0 | 3.8 | 1.0 |  |  |  |  |
| + demographics only (own survey) | 150 |  |  |  | 5000.0 |  |  |  |  |  |  |  |  |
| + demographics only (own survey) | 300 |  |  |  | 5000.0 |  |  |  |  |  |  |  |  |
| + demographics only (own survey) | 600 |  |  |  | 5000.0 |  |  |  |  |  |  |  |  |
| + record citizens | 150 |  | 58.4 |  |  |  |  |  |  |  |  |  |  |
| + record citizens | 300 |  | 57.9 |  |  |  |  |  |  |  |  |  |  |
| + record citizens | 600 |  | 57.3 |  |  |  |  |  |  |  |  |  |  |
| + record citizens (own survey) | 150 |  |  | 165.2 |  |  |  |  |  |  |  |  |  |
| + record citizens (own survey) | 300 |  |  | 259.5 |  |  |  |  |  |  |  |  |  |
| + record citizens (own survey) | 600 |  |  | 321.3 |  |  |  |  |  |  |  |  |  |
| + record citizens (own survey) + chatbot kind | 150 | 138.9 |  | 215.4 |  |  |  |  |  |  |  |  |  |
| + record citizens (own survey) + chatbot kind | 300 | 109.6 |  | 277.3 |  |  |  |  |  |  |  |  |  |
| + record citizens (own survey) + chatbot kind | 600 | 101.0 |  | 374.5 |  |  |  |  |  |  |  |  |  |
| + record citizens (own survey) + chatbot panel, averaged | 150 |  |  | 259.6 |  |  |  |  |  | 90.3 |  |  |  |
| + record citizens (own survey) + chatbot panel, averaged | 300 |  |  | 357.2 |  |  |  |  |  | 81.8 |  |  |  |
| + record citizens (own survey) + chatbot panel, averaged | 600 |  |  | 460.7 |  |  |  |  |  | 73.5 |  |  |  |
| + record citizens (own survey) + chatbot panel, each weighted | 150 | 71.1 |  | 375.9 |  | 128.7 | 41.1 | 37.9 | 5.4 |  |  |  |  |
| + record citizens (own survey) + chatbot panel, each weighted | 300 | 29.1 |  | 442.9 |  | 106.2 | 36.6 | 33.3 | 4.8 |  |  |  |  |
| + record citizens (own survey) + chatbot panel, each weighted | 600 | 39.4 |  | 557.1 |  | 67.6 | 33.5 | 29.7 | 5.8 |  |  |  |  |
| + record citizens (own survey, 10 standard questions) | 150 |  |  |  |  |  |  |  |  |  |  | 5000.0 |  |
| + record citizens (own survey, 10 standard questions) | 300 |  |  |  |  |  |  |  |  |  |  | 5000.0 |  |
| + record citizens (own survey, 10 standard questions) | 600 |  |  |  |  |  |  |  |  |  |  | 5000.0 |  |
| + record citizens (own survey, 10 standard questions) + chatbot kind | 150 | 2596.3 |  |  |  |  |  |  |  |  |  | 5000.0 |  |
| + record citizens (own survey, 10 standard questions) + chatbot kind | 300 | 1173.6 |  |  |  |  |  |  |  |  |  | 3888.5 |  |
| + record citizens (own survey, 10 standard questions) + chatbot kind | 600 | 890.0 |  |  |  |  |  |  |  |  |  | 5000.0 |  |
| + record citizens (own survey, 20 standard questions) | 150 |  |  |  |  |  |  |  |  |  |  |  | 5000.0 |
| + record citizens (own survey, 20 standard questions) | 300 |  |  |  |  |  |  |  |  |  |  |  | 5000.0 |
| + record citizens (own survey, 20 standard questions) | 600 |  |  |  |  |  |  |  |  |  |  |  | 5000.0 |
| + record citizens (own survey, 20 standard questions) + chatbot kind | 150 | 709.9 |  |  |  |  |  |  |  |  |  |  | 1345.1 |
| + record citizens (own survey, 20 standard questions) + chatbot kind | 300 | 486.2 |  |  |  |  |  |  |  |  |  |  | 1530.0 |
| + record citizens (own survey, 20 standard questions) + chatbot kind | 600 | 435.6 |  |  |  |  |  |  |  |  |  |  | 2307.2 |
| + record citizens (own survey, 5 standard questions) | 150 |  |  |  |  |  |  |  |  |  | 5000.0 |  |  |
| + record citizens (own survey, 5 standard questions) | 300 |  |  |  |  |  |  |  |  |  | 5000.0 |  |  |
| + record citizens (own survey, 5 standard questions) | 600 |  |  |  |  |  |  |  |  |  | 5000.0 |  |  |
| + record citizens + chatbot kind | 150 | 15.0 | 47.9 |  |  |  |  |  |  |  |  |  |  |
| + record citizens + chatbot kind | 300 | 13.3 | 49.0 |  |  |  |  |  |  |  |  |  |  |
| + record citizens + chatbot kind | 600 | 12.4 | 47.7 |  |  |  |  |  |  |  |  |  |  |
| + record citizens + chatbot panel, each weighted | 150 | 12.9 | 45.7 |  |  | 2.2 | 1.9 | 0.0 | 0.0 |  |  |  |  |
| + record citizens + chatbot panel, each weighted | 300 | 11.0 | 47.7 |  |  | 1.3 | 0.0 | 0.0 | 0.0 |  |  |  |  |
| + record citizens + chatbot panel, each weighted | 600 | 11.9 | 45.3 |  |  | 0.0 | 2.1 | 0.0 | 0.3 |  |  |  |  |

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

