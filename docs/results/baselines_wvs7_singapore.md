# Baselines on WVS wave 7, Singapore

Questions: 77; respondents: 2012; cells: 2002; segments: sex, age_band, education3, income3, religion, ethnic, born_in_country.

## Population level

| method | jsd_median | jsd_mean | tv_median | tv_mean | mae_pts_median | mae_pts_mean | top_box_err_median | top_box_err_mean | max_abs_err_median | max_abs_err_mean | entropy_ratio_median | entropy_ratio_mean | wd_median | wd_mean | representativeness_median | representativeness_mean | n_cells |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| population_marginal_for_segments | 0.000 | -0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 1.000 | 1.000 | 0.000 | 0.000 | 1.000 | 1.000 | 77 |
| uniform | 0.128 | 0.132 | 0.347 | 0.333 | 15.146 | 15.144 | 0.154 | 0.176 | 0.239 | 0.266 | 1.279 | 1.464 | 0.690 | 0.938 | 0.824 | 0.810 | 77 |

Sampling-noise floor: median JSD 0.0003

## Segment level

| method | jsd_median | jsd_mean | tv_median | tv_mean | mae_pts_median | mae_pts_mean | top_box_err_median | top_box_err_mean | max_abs_err_median | max_abs_err_mean | entropy_ratio_median | entropy_ratio_mean | wd_median | wd_mean | representativeness_median | representativeness_mean | n_cells |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| population_marginal_for_segments | 0.004 | 0.011 | 0.054 | 0.072 | 2.097 | 3.043 | 0.017 | 0.036 | 0.042 | 0.059 | 1.008 | 1.034 | 0.100 | 0.190 | 0.976 | 0.964 | 1925 |
| uniform | 0.134 | 0.141 | 0.351 | 0.343 | 14.983 | 15.546 | 0.154 | 0.184 | 0.251 | 0.275 | 1.290 | 1.540 | 0.700 | 0.979 | 0.816 | 0.802 | 1925 |

Sampling-noise floor at segment level: median JSD 0.0017

## 'Everyone is average' error by segment type (median mae_pts): how much segments actually differ

| segment_type | mae_pts | jsd |
|---|---|---|
| age_band | 2.044 | 0.003 |
| born_in_country | 1.149 | 0.001 |
| education3 | 1.941 | 0.003 |
| ethnic | 3.012 | 0.008 |
| income3 | 2.085 | 0.004 |
| religion | 2.601 | 0.006 |
| sex | 0.856 | 0.001 |

## Segment groups available

ALL, age_band=18-29, age_band=30-44, age_band=45-59, age_band=60+, born_in_country=Born here, born_in_country=Immigrant, education3=Higher, education3=Lower, education3=Middle, ethnic=Chinese, ethnic=Indian, ethnic=Malay, ethnic=Others, income3=High, income3=Low, income3=Medium, religion=Buddhist, religion=Catholic, religion=Hindu, religion=Muslim, religion=No religion, religion=Other religion, religion=Protestant, sex=Female, sex=Male
