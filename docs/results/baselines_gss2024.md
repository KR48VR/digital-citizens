# Baselines on GSS 2024 (United States)

Questions: 84; respondents: 3986; cells (question x group): 3183; segments: age_band, sex, race_eth, education, region, party3, ideology3, income4, religion4, urbanicity.

These are the free, no-LLM predictions a digital-citizen simulator has to beat. Lower JSD/TV is better; entropy_ratio and dispersion_ratio should be near 1.

## Population level (group = ALL)

| method | jsd_median | jsd_mean | tv_median | tv_mean | mae_pts_median | mae_pts_mean | top_box_err_median | top_box_err_mean | max_abs_err_median | max_abs_err_mean | entropy_ratio_median | entropy_ratio_mean | wd_median | wd_mean | representativeness_median | representativeness_mean | n_cells |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| demographic_regression_2022->2024 | 0.001 | 0.002 | 0.025 | 0.032 | 1.417 | 2.014 | 0.014 | 0.023 | 0.024 | 0.030 | 0.996 | 0.996 | 0.042 | 0.060 | 0.986 | 0.980 | 84 |
| population_marginal_for_segments | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 1.000 | 1.000 | 0.000 | 0.000 | 1.000 | 1.000 | 84 |
| previous_wave_2022 | 0.001 | 0.002 | 0.028 | 0.033 | 1.393 | 2.001 | 0.018 | 0.023 | 0.024 | 0.030 | 0.994 | 0.992 | 0.041 | 0.063 | 0.986 | 0.979 | 84 |
| uniform | 0.050 | 0.064 | 0.224 | 0.237 | 13.695 | 14.434 | 0.139 | 0.155 | 0.209 | 0.218 | 1.121 | 1.194 | 0.398 | 0.452 | 0.856 | 0.841 | 84 |

Survey sampling-noise floor (expected JSD of a perfect simulator vs this survey's own sample): median 0.0002

## Segment level (all question x segment cells)

| method | jsd_median | jsd_mean | tv_median | tv_mean | mae_pts_median | mae_pts_mean | top_box_err_median | top_box_err_mean | max_abs_err_median | max_abs_err_mean | entropy_ratio_median | entropy_ratio_mean | wd_median | wd_mean | representativeness_median | representativeness_mean | n_cells |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| demographic_regression_2022->2024 | 0.003 | 0.005 | 0.047 | 0.056 | 2.695 | 3.405 | 0.026 | 0.036 | 0.043 | 0.051 | 0.996 | 0.998 | 0.072 | 0.096 | 0.974 | 0.967 | 3099 |
| population_marginal_for_segments | 0.003 | 0.009 | 0.050 | 0.067 | 2.952 | 4.021 | 0.030 | 0.044 | 0.046 | 0.061 | 1.007 | 1.029 | 0.081 | 0.133 | 0.971 | 0.958 | 3099 |
| previous_wave_2022 | 0.003 | 0.006 | 0.050 | 0.059 | 2.821 | 3.592 | 0.027 | 0.038 | 0.045 | 0.054 | 0.993 | 0.993 | 0.076 | 0.104 | 0.972 | 0.965 | 3098 |
| uniform | 0.056 | 0.072 | 0.238 | 0.247 | 13.984 | 14.985 | 0.140 | 0.161 | 0.215 | 0.228 | 1.143 | 1.232 | 0.410 | 0.476 | 0.853 | 0.835 | 3099 |

Sampling-noise floor at segment level: median JSD 0.0008

## Does the prediction reproduce how segments differ? (per question, averaged)

| method | gap_r | gap_slope | dispersion_ratio |
|---|---|---|---|
| demographic_regression_2022->2024 | 0.769 | 0.772 | 0.976 |
| previous_wave_2022 | 0.743 | 0.769 | 1.044 |
| uniform |  | 0.000 | 0.000 |

## Segment level by segment type (median JSD)

| segment_type | demographic_regression_2022->2024 | population_marginal_for_segments | previous_wave_2022 | uniform |
|---|---|---|---|---|
| age_band | 0.003 | 0.003 | 0.003 | 0.057 |
| education | 0.003 | 0.004 | 0.003 | 0.055 |
| ideology3 | 0.003 | 0.008 | 0.003 | 0.065 |
| income4 | 0.003 | 0.003 | 0.003 | 0.052 |
| party3 | 0.003 | 0.007 | 0.003 | 0.065 |
| race_eth | 0.002 | 0.004 | 0.003 | 0.057 |
| region | 0.003 | 0.001 | 0.003 | 0.053 |
| religion4 | 0.002 | 0.003 | 0.003 | 0.056 |
| sex | 0.002 | 0.001 | 0.002 | 0.052 |
| urbanicity | 0.003 | 0.002 | 0.004 | 0.054 |
