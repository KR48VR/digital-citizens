# Ledger experiment: Singapore published evidence vs WVS-7 (67 cells covered; 25 questions)

Learned weight on ledger evidence (leave-one-question-out, median over questions): 0.010 of face value (a published n of 1,000 is worth about 10 respondents).

## Ledger rows alone: error by the confidence assigned and by sampling type

| tier | count | median | mean |
|---|---|---|---|
| <0.4 (loose match) | 31 | 9.310 | 9.830 |
| 0.4-0.69 | 49 | 8.090 | 8.230 |
| >=0.7 (same wording) | 16 | 4.740 | 6.370 |

| sampling | count | median | mean |
|---|---|---|---|
| online_panel | 17 | 9.850 | 9.990 |
| opt_in | 3 | 19.370 | 20.080 |
| probability | 76 | 7.890 | 7.630 |

Ledger rows: 96; cells with evidence: 73; prior available for 886 cells. Weights: claude zero-shot = 31.3, record-anchored citizens = 84.0

## By question (mean error over covered cells)

| question_id | pooled prior (no local evidence) | pooled prior + ledger evidence at face value | pooled prior + ledger evidence, learned weight |
|---|---|---|---|
| Q111 | 0.450 | 9.670 | 0.670 |
| Q121 | 4.250 | 7.950 | 4.450 |
| Q131 | 2.690 | 2.010 | 2.410 |
| Q142 | 6.330 | 9.340 | 6.260 |
| Q164 | 1.690 | 2.210 | 1.660 |
| Q171 | 5.150 | 6.380 | 5.210 |
| Q19 | 10.530 | 5.870 | 9.800 |
| Q199 | 4.820 | 17.290 | 5.470 |
| Q209 | 2.430 | 1.740 | 2.200 |
| Q211 | 11.620 | 9.380 | 11.460 |
| Q235 | 8.150 | 8.240 | 8.050 |
| Q236 | 2.980 | 15.340 | 1.680 |
| Q238 | 2.260 | 11.080 | 2.980 |
| Q250 | 2.870 | 2.170 | 2.840 |
| Q252 | 2.740 | 2.320 | 2.380 |
| Q46 | 0.650 | 5.320 | 0.430 |
| Q49 | 1.260 | 2.710 | 1.240 |
| Q57 | 2.330 | 10.300 | 3.990 |
| Q6 | 2.870 | 7.090 | 2.900 |
| Q62 | 1.880 | 14.660 | 3.090 |
| Q63 | 2.580 | 14.860 | 4.620 |
| Q64 | 6.740 | 3.840 | 6.430 |
| Q66 | 3.480 | 4.400 | 3.440 |
| Q70 | 2.530 | 8.070 | 2.860 |
| Q71 | 4.610 | 5.300 | 4.610 |

## Error on covered cells (points per answer option)

| method | mae_pts_median | mae_pts_mean | jsd_median | jsd_mean |
|---|---|---|---|---|
| everyone is average (real level) | 2.940 | 4.400 | 0.010 | 0.030 |
| ledger evidence alone | 8.030 | 8.320 | 0.040 | 0.050 |
| pooled prior (no local evidence) | 3.810 | 4.430 | 0.010 | 0.020 |
| pooled prior + ledger evidence at face value | 6.830 | 7.240 | 0.030 | 0.040 |
| pooled prior + ledger evidence, learned weight | 3.990 | 4.490 | 0.010 | 0.020 |

## Per cell

| question_id | group | everyone is average (real level) | ledger evidence alone | pooled prior (no local evidence) | pooled prior + ledger evidence at face value | pooled prior + ledger evidence, learned weight |
|---|---|---|---|---|---|---|
| Q111 | ALL | 0.0 | 11.4 | 0.4 | 9.7 | 0.7 |
| Q121 | ALL | 0.0 | 11.3 | 2.9 | 10.4 | 3.5 |
| Q121 | age_band=18-29 | 4.2 | 9.8 | 5.4 | 7.0 | 5.4 |
| Q121 | age_band=60+ | 1.0 | 9.9 | 4.5 | 6.4 | 4.5 |
| Q131 | ALL | 0.0 | 2.9 | 2.7 | 2.0 | 2.4 |
| Q142 | ALL | 0.0 | 5.2 | 5.0 | 5.1 | 5.0 |
| Q142 | age_band=60+ | 7.9 | 9.7 | 9.8 | 9.7 | 9.8 |
| Q142 | education3=Higher | 1.1 | 16.5 | 3.8 | 12.4 | 3.7 |
| Q142 | education3=Lower | 2.0 | 9.3 | 4.6 | 8.3 | 4.6 |
| Q142 | ethnic=Chinese | 2.0 | 10.9 | 3.9 | 10.3 | 3.6 |
| Q142 | ethnic=Indian | 3.8 | 10.1 | 4.7 | 5.9 | 4.7 |
| Q142 | ethnic=Malay | 10.7 | 15.6 | 12.6 | 13.6 | 12.6 |
| Q164 | ALL | 0.0 | 3.1 | 1.2 | 2.8 | 1.1 |
| Q164 | ethnic=Malay | 7.8 | 1.4 | 1.5 | 1.3 | 1.5 |
| Q164 | religion=Buddhist | 4.5 | 4.1 | 3.0 | 2.9 | 3.0 |
| Q164 | religion=Hindu | 4.1 | 2.7 | 1.6 | 1.3 | 1.6 |
| Q164 | religion=Muslim | 7.7 | 1.4 | 1.6 | 1.3 | 1.6 |
| Q164 | religion=No religion | 8.2 | 5.2 | 1.2 | 3.6 | 1.2 |
| Q171 | ALL | 0.0 | 6.8 | 3.9 | 6.7 | 4.5 |
| Q171 | age_band=18-29 | 3.3 | 9.2 | 2.8 | 7.7 | 2.7 |
| Q171 | age_band=60+ | 2.1 | 8.0 | 4.0 | 6.9 | 4.1 |
| Q171 | ethnic=Malay | 9.6 | 7.2 | 7.5 | 7.1 | 7.4 |
| Q171 | religion=Buddhist | 5.5 | 9.4 | 2.7 | 8.9 | 3.3 |
| Q171 | religion=Catholic | 9.0 | 6.8 | 8.1 | 5.9 | 8.0 |
| Q171 | religion=Hindu | 7.1 | 3.3 | 4.8 | 2.5 | 4.6 |
| Q171 | religion=Muslim | 8.3 | 6.3 | 7.2 | 6.2 | 7.1 |
| Q171 | religion=No religion | 12.1 | 6.7 | 3.9 | 6.1 | 3.9 |
| Q171 | religion=Protestant | 12.2 | 6.6 | 6.6 | 5.9 | 6.5 |
| Q19 | ALL | 0.0 | 5.6 | 10.5 | 5.9 | 9.8 |
| Q199 | ALL | 0.0 | 19.4 | 4.6 | 16.7 | 5.2 |
| Q199 | age_band=18-29 | 3.5 | 17.1 | 3.7 | 14.7 | 4.3 |
| Q199 | age_band=60+ | 3.4 | 23.7 | 6.2 | 20.5 | 7.0 |
| Q209 | age_band=18-29 | 16.7 | 2.4 | 2.4 | 1.7 | 2.2 |
| Q211 | age_band=18-29 | 11.6 | 9.0 | 11.6 | 9.4 | 11.5 |
| Q235 | ALL | 0.0 | 3.3 | 7.9 | 3.1 | 7.1 |
| Q235 | ethnic=Malay | 2.1 | 12.8 | 9.5 | 11.1 | 9.5 |
| Q235 | religion=Buddhist | 4.1 | 11.5 | 13.5 | 12.0 | 13.4 |
| Q235 | religion=Catholic | 5.7 | 12.7 | 13.8 | 13.2 | 13.8 |
| Q235 | religion=Hindu | 2.9 | 5.6 | 3.3 | 4.2 | 3.3 |
| Q235 | religion=Muslim | 2.9 | 11.7 | 7.9 | 9.9 | 8.0 |
| Q235 | religion=No religion | 1.9 | 5.9 | 4.1 | 5.2 | 4.1 |
| Q235 | religion=Protestant | 4.9 | 8.4 | 5.3 | 7.1 | 5.3 |
| Q236 | ALL | 0.0 | 17.8 | 3.0 | 15.3 | 1.7 |
| Q238 | ALL | 0.0 | 12.1 | 2.3 | 11.1 | 3.0 |
| Q250 | ALL | 0.0 | 2.2 | 2.9 | 2.2 | 2.8 |
| Q252 | ALL | 0.0 | 2.6 | 2.7 | 2.3 | 2.4 |
| Q46 | ALL | 0.0 | 7.6 | 0.6 | 5.3 | 0.4 |
| Q49 | ALL | 0.0 | 3.5 | 1.1 | 3.0 | 1.1 |
| Q49 | age_band=18-29 | 1.9 | 2.9 | 1.3 | 2.7 | 1.2 |
| Q49 | age_band=60+ | 1.3 | 4.0 | 1.5 | 2.5 | 1.5 |
| Q57 | ALL | 0.0 | 10.6 | 2.3 | 10.3 | 4.0 |
| Q6 | ALL | 0.0 | 7.0 | 1.4 | 6.8 | 2.1 |
| Q6 | age_band=18-29 | 4.2 | 12.1 | 1.8 | 9.0 | 1.3 |
| Q6 | age_band=60+ | 3.7 | 14.3 | 2.0 | 9.8 | 2.0 |
| Q6 | education3=Higher | 2.2 | 13.2 | 2.4 | 11.5 | 2.7 |
| Q6 | education3=Lower | 3.9 | 8.9 | 5.1 | 7.1 | 4.8 |
| Q6 | ethnic=Malay | 23.7 | 1.6 | 2.8 | 0.4 | 2.7 |
| Q6 | religion=Muslim | 22.5 | 4.8 | 1.7 | 4.2 | 1.8 |
| Q6 | religion=No religion | 21.2 | 8.5 | 5.9 | 7.8 | 5.7 |
| Q62 | ALL | 0.0 | 15.4 | 1.9 | 14.7 | 3.1 |
| Q63 | ALL | 0.0 | 15.5 | 2.6 | 14.9 | 4.6 |
| Q64 | age_band=18-29 | 4.7 | 3.5 | 6.7 | 3.8 | 6.4 |
| Q66 | ALL | 0.0 | 3.5 | 2.0 | 3.1 | 2.0 |
| Q66 | age_band=18-29 | 5.1 | 6.3 | 5.0 | 5.7 | 4.9 |
| Q70 | age_band=18-29 | 2.4 | 9.2 | 2.5 | 8.1 | 2.9 |
| Q71 | ALL | 0.0 | 2.3 | 4.8 | 2.8 | 4.7 |
| Q71 | age_band=18-29 | 4.1 | 8.4 | 4.5 | 7.8 | 4.5 |

## Coverage by question

| question_id | rows | groups_covered | effective_n |
|---|---|---|---|
| Q6 | 20 | ['ALL', 'age_band=18-29', 'age_band=60+', 'education3=Higher', 'education3=Lower', 'ethnic=Malay', 'religion=Muslim', 'religion=No religion'] | 10164.100 |
| Q19 | 1 | ['ALL'] | 2000.000 |
| Q46 | 1 | ['ALL'] | 225.000 |
| Q49 | 4 | ['ALL', 'age_band=18-29', 'age_band=60+'] | 1442.500 |
| Q57 | 1 | ['ALL'] | 2100.000 |
| Q62 | 1 | ['ALL'] | 1800.000 |
| Q63 | 1 | ['ALL'] | 1800.000 |
| Q64 | 1 | ['age_band=18-29'] | 617.750 |
| Q66 | 3 | ['ALL', 'age_band=18-29'] | 1566.950 |
| Q70 | 1 | ['age_band=18-29'] | 617.750 |
| Q71 | 2 | ['ALL', 'age_band=18-29'] | 962.750 |
| Q111 | 1 | ['ALL'] | 700.000 |
| Q121 | 3 | ['ALL', 'age_band=18-29', 'age_band=60+'] | 880.000 |
| Q131 | 1 | ['ALL'] | 600.000 |
| Q142 | 9 | ['ALL', 'age_band=60+', 'education3=Higher', 'education3=Lower', 'ethnic=Chinese', 'ethnic=Indian', 'ethnic=Malay'] | 6878.700 |
| Q164 | 6 | ['ALL', 'ethnic=Malay', 'religion=Muslim', 'religion=No religion'] | 1522.650 |
| Q171 | 18 | ['ALL', 'age_band=18-29', 'age_band=60+', 'ethnic=Malay', 'religion=Muslim', 'religion=No religion'] | 8427.750 |
| Q199 | 3 | ['ALL', 'age_band=18-29', 'age_band=60+'] | 1125.000 |
| Q209 | 1 | ['age_band=18-29'] | 706.000 |
| Q211 | 1 | ['age_band=18-29'] | 529.500 |
| Q235 | 11 | ['ALL', 'ethnic=Malay', 'religion=Muslim', 'religion=No religion'] | 3375.750 |
| Q236 | 1 | ['ALL'] | 702.100 |
| Q238 | 2 | ['ALL'] | 1102.700 |
| Q250 | 1 | ['ALL'] | 401.200 |
| Q252 | 2 | ['ALL'] | 952.350 |
