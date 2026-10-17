# Record-anchored citizens: does learning from more countries help?

Generated 2026-10-17 04:06 UTC; runtime 1268s.

## Singapore

| method | pop_mae | seg_mae_median | seg_mae_mean | gap_r | gap_slope | dispersion |
|---|---|---|---|---|---|---|
| claude zero-shot | 4.850 | 4.980 | 6.290 | 0.540 | 0.360 | 0.650 |
| record-anchored, trained on 2 countries | 3.920 | 4.210 | 6.330 | 0.700 | 0.520 | 0.780 |
| record-anchored, trained on 61 countries (90,669 people) | 2.950 | 3.660 | 4.540 | 0.730 | 0.420 | 0.660 |
| human level + record differences (2 countries) | 0.000 | 2.070 | 2.710 | 0.700 | 0.520 | 0.750 |
| human level + record differences (61 countries) | 0.000 | 1.910 | 2.580 | 0.730 | 0.420 | 0.660 |
| everyone is average (human level only) | 0.000 | 2.560 | 4.200 |  | 0.000 | 0.000 |

## China

| method | pop_mae | seg_mae_median | seg_mae_mean | gap_r | gap_slope | dispersion |
|---|---|---|---|---|---|---|
| claude zero-shot | 3.680 | 3.450 | 5.330 | 0.450 | 0.250 | 0.790 |
| record-anchored, trained on 2 countries | 4.160 | 4.120 | 4.850 | 0.710 | 0.790 | 1.040 |
| record-anchored, trained on 61 countries (89,645 people) | 3.240 | 3.490 | 5.040 | 0.740 | 0.460 | 0.800 |
| human level + record differences (2 countries) | 0.000 | 1.310 | 1.700 | 0.710 | 0.790 | 1.020 |
| human level + record differences (61 countries) | 0.000 | 1.000 | 1.400 | 0.740 | 0.460 | 0.700 |
| everyone is average (human level only) | 0.000 | 1.170 | 1.710 |  | 0.000 | 0.000 |

## Singapore examples (share choosing the option, %)

| item | group | real | claude | record_2c | record_all | human_level+record_all |
|---|---|---|---|---|---|---|
| job worry: very much | ALL | 30.2 | 20.0 | 15.2 | 22.9 | 30.2 |
| job worry: very much | ethnic=Malay | 51.7 | 25.0 | 15.8 | 28.7 | 36.0 |
| job worry: very much | ethnic=Chinese | 26.3 | 18.0 | 14.8 | 21.1 | 28.4 |
| job worry: very much | education3=Lower | 29.3 | 20.0 | 19.6 | 25.1 | 32.4 |
| job worry: very much | education3=Higher | 28.0 | 20.0 | 14.2 | 21.8 | 29.1 |
| job worry: very much | age_band=60+ | 22.3 | 14.0 | 11.3 | 16.4 | 23.7 |
| petition: would never | ALL | 56.1 | 38.0 | 36.6 | 48.0 | 56.1 |
| petition: would never | ethnic=Malay | 67.5 | 38.0 | 43.4 | 66.0 | 74.1 |
| petition: would never | ethnic=Chinese | 53.3 | 38.0 | 35.4 | 44.7 | 52.8 |
| petition: would never | education3=Lower | 88.4 | 57.0 | 59.0 | 74.6 | 82.7 |
| petition: would never | education3=Higher | 38.6 | 25.0 | 26.3 | 34.7 | 42.8 |
| petition: would never | age_band=60+ | 79.3 | 55.0 | 47.9 | 63.0 | 71.0 |
| army rule: very bad | ALL | 57.9 | 35.0 | 31.7 | 40.7 | 57.9 |
| army rule: very bad | ethnic=Malay | 56.5 | 32.0 | 26.3 | 31.7 | 48.9 |
| army rule: very bad | ethnic=Chinese | 57.8 | 34.0 | 31.2 | 41.9 | 59.0 |
| army rule: very bad | education3=Lower | 48.5 | 29.0 | 18.8 | 34.6 | 51.8 |
| army rule: very bad | education3=Higher | 62.9 | 39.0 | 37.9 | 44.9 | 62.0 |
| army rule: very bad | age_band=60+ | 58.7 | 32.0 | 30.0 | 43.3 | 60.5 |
