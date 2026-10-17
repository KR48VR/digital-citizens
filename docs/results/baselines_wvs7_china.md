# Baselines on WVS wave 7, China

Questions: 74; respondents: 3036; cells: 1480; segments: sex, age_band, education3, income3, religion, born_in_country, urban_rural.

## Population level

| method | jsd_median | jsd_mean | tv_median | tv_mean | mae_pts_median | mae_pts_mean | top_box_err_median | top_box_err_mean | max_abs_err_median | max_abs_err_mean | entropy_ratio_median | entropy_ratio_mean | wd_median | wd_mean | representativeness_median | representativeness_mean | n_cells |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| population_marginal_for_segments | 0.000 | -0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 1.000 | 1.000 | 0.000 | 0.000 | 1.000 | 1.000 | 74 |
| uniform | 0.136 | 0.151 | 0.350 | 0.361 | 15.738 | 16.698 | 0.167 | 0.202 | 0.293 | 0.294 | 1.348 | 1.504 | 0.739 | 1.133 | 0.794 | 0.779 | 74 |

Sampling-noise floor: median JSD 0.0002

## Segment level

| method | jsd_median | jsd_mean | tv_median | tv_mean | mae_pts_median | mae_pts_mean | top_box_err_median | top_box_err_mean | max_abs_err_median | max_abs_err_mean | entropy_ratio_median | entropy_ratio_mean | wd_median | wd_mean | representativeness_median | representativeness_mean | n_cells |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| population_marginal_for_segments | 0.002 | 0.009 | 0.035 | 0.054 | 1.382 | 2.295 | 0.011 | 0.025 | 0.028 | 0.044 | 1.003 | 1.025 | 0.058 | 0.134 | 0.985 | 0.975 | 1406 |
| uniform | 0.144 | 0.156 | 0.358 | 0.366 | 16.496 | 16.926 | 0.166 | 0.203 | 0.284 | 0.298 | 1.345 | 1.539 | 0.736 | 1.136 | 0.787 | 0.778 | 1406 |

Sampling-noise floor at segment level: median JSD 0.0008

## 'Everyone is average' error by segment type (median mae_pts): how much segments actually differ

| segment_type | mae_pts | jsd |
|---|---|---|
| age_band | 1.724 | 0.002 |
| born_in_country | 0.035 | 0.000 |
| education3 | 1.600 | 0.002 |
| income3 | 1.616 | 0.002 |
| religion | 2.635 | 0.006 |
| sex | 0.807 | 0.001 |
| urban_rural | 1.069 | 0.001 |

## Segment groups available

ALL, age_band=18-29, age_band=30-44, age_band=45-59, age_band=60+, born_in_country=Born here, education3=Higher, education3=Lower, education3=Middle, income3=High, income3=Low, income3=Medium, religion=Buddhist, religion=Muslim, religion=No religion, religion=Protestant, sex=Female, sex=Male, urban_rural=Rural, urban_rural=Urban
