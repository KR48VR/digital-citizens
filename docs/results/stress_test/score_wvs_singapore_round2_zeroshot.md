# Stress test: claude_zero_shot_round2 on wvs packet `packet_wvs_singapore_round2.json`

12 questions x 9 groups; predictions written without access to the answers; scored against the real shares. Lower is better for jsd/tv/mae_pts.

## population

| method | jsd_median | jsd_mean | tv_median | tv_mean | mae_pts_median | mae_pts_mean | top_box_err_median | top_box_err_mean | max_abs_err_median | max_abs_err_mean | entropy_ratio_median | entropy_ratio_mean | wd_median | wd_mean | representativeness_median | representativeness_mean | n_cells |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| claude_zero_shot_round2 | 0.008 | 0.011 | 0.077 | 0.088 | 4.424 | 4.981 | 0.040 | 0.045 | 0.063 | 0.075 | 1.033 | 1.177 | 0.156 | 0.195 | 0.948 | 0.953 | 12 |
| population_marginal_for_segments | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 1.000 | 1.000 | 0.000 | 0.000 | 1.000 | 1.000 | 12 |
| uniform | 0.171 | 0.151 | 0.369 | 0.355 | 20.286 | 23.226 | 0.237 | 0.241 | 0.328 | 0.317 | 1.440 | 2.079 | 0.703 | 0.684 | 0.787 | 0.794 | 12 |

## segment

| method | jsd_median | jsd_mean | tv_median | tv_mean | mae_pts_median | mae_pts_mean | top_box_err_median | top_box_err_mean | max_abs_err_median | max_abs_err_mean | entropy_ratio_median | entropy_ratio_mean | wd_median | wd_mean | representativeness_median | representativeness_mean | n_cells |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| claude_zero_shot_round2 | 0.010 | 0.015 | 0.087 | 0.100 | 4.295 | 5.632 | 0.034 | 0.046 | 0.071 | 0.088 | 1.028 | 1.176 | 0.167 | 0.212 | 0.948 | 0.944 | 96 |
| population_marginal_for_segments | 0.002 | 0.005 | 0.037 | 0.046 | 1.837 | 2.530 | 0.015 | 0.023 | 0.033 | 0.041 | 0.998 | 1.034 | 0.069 | 0.105 | 0.978 | 0.973 | 96 |
| uniform | 0.161 | 0.151 | 0.362 | 0.356 | 20.049 | 23.127 | 0.226 | 0.239 | 0.318 | 0.318 | 1.426 | 2.139 | 0.690 | 0.714 | 0.792 | 0.790 | 96 |

## Segment differences (gap recovery; dispersion ratio ideal = 1)

| method | gap_r | gap_slope | dispersion_ratio |
|---|---|---|---|
| claude_zero_shot_round2 | 0.672 | 0.519 | 1.606 |
| uniform |  | 0.000 | 0.000 |

## By group (median mae_pts)

| group | claude_zero_shot_round2 | population_marginal_for_segments | uniform |
|---|---|---|---|
| ALL | 4.424 | 0.000 | 20.286 |
| age_band=60+ | 6.744 | 2.080 | 20.545 |
| education3=Higher | 4.168 | 1.531 | 20.779 |
| education3=Lower | 4.836 | 2.568 | 19.358 |
| ethnic=Chinese | 4.861 | 0.541 | 20.315 |
| ethnic=Indian | 3.826 | 2.663 | 19.666 |
| ethnic=Malay | 4.284 | 1.938 | 19.836 |
| religion=Muslim | 4.302 | 2.689 | 20.284 |
| religion=No religion | 3.070 | 1.287 | 19.981 |

## Worst 10 cells for claude_zero_shot_round2

| question_id | group | k | jsd | mae_pts | max_abs_err |
|---|---|---|---|---|---|
| Q130 | ethnic=Malay | 4 | 0.082 | 15.919 | 0.318 |
| Q130 | religion=Muslim | 4 | 0.081 | 15.948 | 0.319 |
| Q17 | ethnic=Malay | 2 | 0.049 | 23.671 | 0.237 |
| Q130 | education3=Higher | 4 | 0.047 | 11.722 | 0.234 |
| Q235 | education3=Lower | 4 | 0.044 | 11.538 | 0.136 |
| Q130 | age_band=60+ | 4 | 0.041 | 11.065 | 0.221 |
| Q17 | religion=Muslim | 2 | 0.040 | 21.579 | 0.216 |
| Q130 | ALL | 4 | 0.039 | 11.122 | 0.222 |
| Q130 | ethnic=Indian | 4 | 0.039 | 11.005 | 0.220 |
| Q235 | age_band=60+ | 4 | 0.037 | 10.585 | 0.129 |
