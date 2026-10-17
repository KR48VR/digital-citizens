# Stress test: claude_anchored_round2 on wvs packet `packet_wvs_singapore_round2.json`

12 questions x 9 groups; predictions written without access to the answers; scored against the real shares. Lower is better for jsd/tv/mae_pts.

## population

| method | jsd_median | jsd_mean | tv_median | tv_mean | mae_pts_median | mae_pts_mean | top_box_err_median | top_box_err_mean | max_abs_err_median | max_abs_err_mean | entropy_ratio_median | entropy_ratio_mean | wd_median | wd_mean | representativeness_median | representativeness_mean | n_cells |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| claude_anchored_round2 | 0.010 | 0.014 | 0.084 | 0.100 | 5.293 | 5.835 | 0.030 | 0.049 | 0.083 | 0.093 | 1.020 | 1.146 | 0.161 | 0.183 | 0.949 | 0.951 | 12 |
| population_marginal_for_segments | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 1.000 | 1.000 | 0.000 | 0.000 | 1.000 | 1.000 | 12 |
| uniform | 0.171 | 0.151 | 0.369 | 0.355 | 20.286 | 23.226 | 0.237 | 0.241 | 0.328 | 0.317 | 1.440 | 2.079 | 0.703 | 0.684 | 0.787 | 0.794 | 12 |

## segment

| method | jsd_median | jsd_mean | tv_median | tv_mean | mae_pts_median | mae_pts_mean | top_box_err_median | top_box_err_mean | max_abs_err_median | max_abs_err_mean | entropy_ratio_median | entropy_ratio_mean | wd_median | wd_mean | representativeness_median | representativeness_mean | n_cells |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| claude_anchored_round2 | 0.010 | 0.017 | 0.095 | 0.107 | 4.897 | 6.164 | 0.028 | 0.049 | 0.078 | 0.100 | 1.017 | 1.124 | 0.161 | 0.197 | 0.951 | 0.944 | 96 |
| population_marginal_for_segments | 0.002 | 0.005 | 0.037 | 0.046 | 1.837 | 2.530 | 0.015 | 0.023 | 0.033 | 0.041 | 0.998 | 1.034 | 0.069 | 0.105 | 0.978 | 0.973 | 96 |
| uniform | 0.161 | 0.151 | 0.362 | 0.356 | 20.049 | 23.127 | 0.226 | 0.239 | 0.318 | 0.318 | 1.426 | 2.139 | 0.690 | 0.714 | 0.792 | 0.790 | 96 |

## Segment differences (gap recovery; dispersion ratio ideal = 1)

| method | gap_r | gap_slope | dispersion_ratio |
|---|---|---|---|
| claude_anchored_round2 | 0.648 | 0.505 | 1.575 |
| uniform |  | 0.000 | 0.000 |

## By group (median mae_pts)

| group | claude_anchored_round2 | population_marginal_for_segments | uniform |
|---|---|---|---|
| ALL | 5.293 | 0.000 | 20.286 |
| age_band=60+ | 5.762 | 2.080 | 20.545 |
| education3=Higher | 4.885 | 1.531 | 20.779 |
| education3=Lower | 5.080 | 2.568 | 19.358 |
| ethnic=Chinese | 5.189 | 0.541 | 20.315 |
| ethnic=Indian | 4.379 | 2.663 | 19.666 |
| ethnic=Malay | 3.945 | 1.938 | 19.836 |
| religion=Muslim | 4.276 | 2.689 | 20.284 |
| religion=No religion | 3.639 | 1.287 | 19.981 |

## Worst 10 cells for claude_anchored_round2

| question_id | group | k | jsd | mae_pts | max_abs_err |
|---|---|---|---|---|---|
| Q130 | ethnic=Malay | 4 | 0.112 | 18.419 | 0.368 |
| Q130 | religion=Muslim | 4 | 0.110 | 18.448 | 0.369 |
| Q130 | education3=Higher | 4 | 0.070 | 15.046 | 0.294 |
| Q130 | age_band=60+ | 4 | 0.068 | 14.065 | 0.281 |
| Q130 | ethnic=Indian | 4 | 0.063 | 14.475 | 0.280 |
| Q130 | ALL | 4 | 0.063 | 14.167 | 0.282 |
| Q17 | ethnic=Malay | 2 | 0.061 | 26.671 | 0.267 |
| Q235 | education3=Lower | 4 | 0.059 | 12.038 | 0.187 |
| Q130 | ethnic=Chinese | 4 | 0.056 | 13.310 | 0.265 |
| Q130 | religion=No religion | 4 | 0.053 | 13.129 | 0.259 |
