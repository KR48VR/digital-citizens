# Stress test: claude_fable_5.1_in_session on gss packet `packet_gss.json`

25 questions x 7 groups; predictions written without access to the answers; scored against the real shares. Lower is better for jsd/tv/mae_pts.

## population

| method | jsd_median | jsd_mean | tv_median | tv_mean | mae_pts_median | mae_pts_mean | top_box_err_median | top_box_err_mean | max_abs_err_median | max_abs_err_mean | entropy_ratio_median | entropy_ratio_mean | wd_median | wd_mean | representativeness_median | representativeness_mean | n_cells |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| claude_fable_5.1_in_session | 0.005 | 0.008 | 0.074 | 0.078 | 3.357 | 4.306 | 0.027 | 0.051 | 0.063 | 0.072 | 1.005 | 0.999 | 0.104 | 0.159 | 0.962 | 0.955 | 25 |
| demographic_regression_2022->2024 | 0.001 | 0.002 | 0.027 | 0.032 | 1.347 | 1.892 | 0.012 | 0.022 | 0.025 | 0.030 | 0.995 | 0.993 | 0.043 | 0.058 | 0.987 | 0.982 | 25 |
| population_marginal_for_segments | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 1.000 | 1.000 | 0.000 | 0.000 | 1.000 | 1.000 | 25 |
| previous_wave_2022 | 0.001 | 0.002 | 0.029 | 0.034 | 1.353 | 1.936 | 0.018 | 0.023 | 0.023 | 0.032 | 0.991 | 0.992 | 0.052 | 0.062 | 0.986 | 0.981 | 25 |

## segment

| method | jsd_median | jsd_mean | tv_median | tv_mean | mae_pts_median | mae_pts_mean | top_box_err_median | top_box_err_mean | max_abs_err_median | max_abs_err_mean | entropy_ratio_median | entropy_ratio_mean | wd_median | wd_mean | representativeness_median | representativeness_mean | n_cells |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| claude_fable_5.1_in_session | 0.007 | 0.011 | 0.080 | 0.091 | 4.326 | 5.134 | 0.037 | 0.057 | 0.073 | 0.083 | 1.016 | 1.002 | 0.120 | 0.176 | 0.958 | 0.948 | 150 |
| demographic_regression_2022->2024 | 0.002 | 0.004 | 0.041 | 0.050 | 2.032 | 2.717 | 0.018 | 0.028 | 0.036 | 0.045 | 1.000 | 0.997 | 0.070 | 0.091 | 0.979 | 0.973 | 150 |
| population_marginal_for_segments | 0.006 | 0.010 | 0.079 | 0.085 | 3.814 | 4.621 | 0.046 | 0.054 | 0.069 | 0.074 | 1.021 | 1.034 | 0.158 | 0.206 | 0.950 | 0.941 | 150 |
| previous_wave_2022 | 0.003 | 0.005 | 0.050 | 0.054 | 2.264 | 2.920 | 0.022 | 0.031 | 0.040 | 0.048 | 0.995 | 0.993 | 0.080 | 0.103 | 0.976 | 0.970 | 150 |

## Segment differences (gap recovery; dispersion ratio ideal = 1)

| method | gap_r | gap_slope | dispersion_ratio |
|---|---|---|---|
| claude_fable_5.1_in_session | 0.866 | 0.811 | 1.115 |
| demographic_regression_2022->2024 | 0.900 | 0.936 | 1.028 |
| previous_wave_2022 | 0.895 | 0.922 | 1.101 |

## By group (median mae_pts)

| group | claude_fable_5.1_in_session | demographic_regression_2022->2024 | population_marginal_for_segments | previous_wave_2022 |
|---|---|---|---|---|
| ALL | 3.357 | 1.347 | 0.000 | 1.353 |
| age_band=18-29 | 5.087 | 2.827 | 3.500 | 3.672 |
| age_band=65+ | 4.010 | 2.030 | 3.440 | 2.290 |
| education=Bachelor's or higher | 4.751 | 1.797 | 3.407 | 1.959 |
| party3=Democrat (incl. leaners) | 3.649 | 1.542 | 4.337 | 1.850 |
| party3=Republican (incl. leaners) | 4.141 | 2.583 | 6.497 | 2.192 |
| race_eth=Black, non-Hispanic | 5.070 | 1.771 | 4.276 | 1.725 |

## Worst 10 cells for claude_fable_5.1_in_session

| question_id | group | k | jsd | mae_pts | max_abs_err |
|---|---|---|---|---|---|
| teensex | party3=Democrat (incl. leaners) | 4 | 0.076 | 13.345 | 0.264 |
| teensex | age_band=18-29 | 4 | 0.072 | 14.108 | 0.282 |
| teensex | education=Bachelor's or higher | 4 | 0.062 | 12.125 | 0.243 |
| teensex | ALL | 4 | 0.051 | 11.023 | 0.220 |
| socbar | age_band=18-29 | 7 | 0.048 | 6.019 | 0.205 |
| prayer | party3=Democrat (incl. leaners) | 2 | 0.045 | 23.349 | 0.233 |
| eqwlth | age_band=18-29 | 7 | 0.038 | 5.817 | 0.142 |
| news | race_eth=Black, non-Hispanic | 5 | 0.038 | 8.980 | 0.225 |
| news | party3=Republican (incl. leaners) | 5 | 0.037 | 8.277 | 0.205 |
| socfrend | education=Bachelor's or higher | 7 | 0.037 | 4.751 | 0.119 |
