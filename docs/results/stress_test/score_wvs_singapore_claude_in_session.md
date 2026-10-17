# Stress test: claude_fable_5.1_in_session on wvs packet `packet_wvs_singapore.json`

20 questions x 10 groups; predictions written without access to the answers; scored against the real shares. Lower is better for jsd/tv/mae_pts.

## population

| method | jsd_median | jsd_mean | tv_median | tv_mean | mae_pts_median | mae_pts_mean | top_box_err_median | top_box_err_mean | max_abs_err_median | max_abs_err_mean | entropy_ratio_median | entropy_ratio_mean | wd_median | wd_mean | representativeness_median | representativeness_mean | n_cells |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| claude_fable_5.1_in_session | 0.018 | 0.018 | 0.129 | 0.118 | 4.854 | 5.286 | 0.057 | 0.078 | 0.105 | 0.105 | 1.015 | 1.032 | 0.243 | 0.253 | 0.941 | 0.938 | 20 |
| population_marginal_for_segments | 0.000 | -0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 1.000 | 1.000 | 0.000 | 0.000 | 1.000 | 1.000 | 20 |
| uniform | 0.112 | 0.116 | 0.333 | 0.307 | 12.371 | 13.550 | 0.097 | 0.138 | 0.244 | 0.253 | 1.290 | 1.276 | 0.674 | 0.926 | 0.815 | 0.815 | 20 |

## segment

| method | jsd_median | jsd_mean | tv_median | tv_mean | mae_pts_median | mae_pts_mean | top_box_err_median | top_box_err_mean | max_abs_err_median | max_abs_err_mean | entropy_ratio_median | entropy_ratio_mean | wd_median | wd_mean | representativeness_median | representativeness_mean | n_cells |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| claude_fable_5.1_in_session | 0.019 | 0.025 | 0.135 | 0.138 | 4.985 | 6.289 | 0.068 | 0.086 | 0.114 | 0.122 | 1.012 | 1.043 | 0.272 | 0.296 | 0.936 | 0.930 | 180 |
| population_marginal_for_segments | 0.005 | 0.014 | 0.074 | 0.091 | 2.557 | 4.204 | 0.031 | 0.057 | 0.057 | 0.078 | 1.009 | 1.042 | 0.115 | 0.218 | 0.971 | 0.953 | 180 |
| uniform | 0.122 | 0.128 | 0.342 | 0.326 | 14.670 | 14.577 | 0.113 | 0.158 | 0.250 | 0.266 | 1.302 | 1.320 | 0.698 | 0.959 | 0.812 | 0.804 | 180 |

## Segment differences (gap recovery; dispersion ratio ideal = 1)

| method | gap_r | gap_slope | dispersion_ratio |
|---|---|---|---|
| claude_fable_5.1_in_session | 0.544 | 0.361 | 0.649 |
| uniform |  | 0.000 | 0.000 |

## By group (median mae_pts)

| group | claude_fable_5.1_in_session | population_marginal_for_segments | uniform |
|---|---|---|---|
| ALL | 4.854 | 0.000 | 12.371 |
| age_band=18-29 | 6.048 | 3.838 | 11.124 |
| age_band=60+ | 6.577 | 2.234 | 16.336 |
| education3=Higher | 3.952 | 1.537 | 9.008 |
| education3=Lower | 6.016 | 4.014 | 14.354 |
| ethnic=Chinese | 3.646 | 0.878 | 11.401 |
| ethnic=Indian | 4.242 | 4.461 | 13.140 |
| ethnic=Malay | 5.895 | 3.166 | 16.241 |
| religion=Muslim | 5.961 | 3.180 | 15.129 |
| religion=No religion | 3.160 | 1.697 | 12.953 |

## Worst 10 cells for claude_fable_5.1_in_session

| question_id | group | k | jsd | mae_pts | max_abs_err |
|---|---|---|---|---|---|
| Q209 | education3=Lower | 3 | 0.095 | 20.925 | 0.314 |
| Q237 | age_band=60+ | 4 | 0.081 | 13.332 | 0.267 |
| Q184 | education3=Lower | 10 | 0.077 | 5.777 | 0.289 |
| Q250 | age_band=18-29 | 10 | 0.076 | 5.986 | 0.222 |
| Q209 | ethnic=Indian | 3 | 0.071 | 20.680 | 0.310 |
| Q142 | ethnic=Malay | 4 | 0.068 | 13.327 | 0.267 |
| Q131 | religion=No religion | 4 | 0.066 | 14.162 | 0.283 |
| Q237 | religion=Muslim | 4 | 0.064 | 13.941 | 0.279 |
| Q209 | ethnic=Malay | 3 | 0.064 | 19.680 | 0.295 |
| Q142 | religion=Muslim | 4 | 0.064 | 12.437 | 0.249 |
