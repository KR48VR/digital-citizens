# Baselines on WVS wave 7, United States

Questions: 77; respondents: 2596; cells: 2079; segments: sex, age_band, education3, income3, religion, ethnic, born_in_country, urban_rural.

## Population level

| method | jsd_median | jsd_mean | tv_median | tv_mean | mae_pts_median | mae_pts_mean | top_box_err_median | top_box_err_mean | max_abs_err_median | max_abs_err_mean | entropy_ratio_median | entropy_ratio_mean | wd_median | wd_mean | representativeness_median | representativeness_mean | n_cells |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| population_marginal_for_segments | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 1.000 | 1.000 | 0.000 | 0.000 | 1.000 | 1.000 | 77 |
| uniform | 0.100 | 0.108 | 0.313 | 0.304 | 13.640 | 14.353 | 0.147 | 0.174 | 0.217 | 0.241 | 1.200 | 1.357 | 0.614 | 0.860 | 0.831 | 0.824 | 77 |

Sampling-noise floor: median JSD 0.0002

## Segment level

| method | jsd_median | jsd_mean | tv_median | tv_mean | mae_pts_median | mae_pts_mean | top_box_err_median | top_box_err_mean | max_abs_err_median | max_abs_err_mean | entropy_ratio_median | entropy_ratio_mean | wd_median | wd_mean | representativeness_median | representativeness_mean | n_cells |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| population_marginal_for_segments | 0.004 | 0.012 | 0.060 | 0.078 | 2.264 | 3.235 | 0.019 | 0.035 | 0.045 | 0.062 | 1.006 | 1.021 | 0.130 | 0.216 | 0.970 | 0.959 | 2002 |
| uniform | 0.105 | 0.115 | 0.315 | 0.311 | 13.224 | 14.528 | 0.151 | 0.174 | 0.227 | 0.248 | 1.209 | 1.393 | 0.629 | 0.873 | 0.835 | 0.822 | 2002 |

Sampling-noise floor at segment level: median JSD 0.0012

## 'Everyone is average' error by segment type (median mae_pts): how much segments actually differ

| segment_type | mae_pts | jsd |
|---|---|---|
| age_band | 2.240 | 0.004 |
| born_in_country | 0.925 | 0.001 |
| education3 | 2.918 | 0.006 |
| ethnic | 2.532 | 0.005 |
| income3 | 2.012 | 0.003 |
| religion | 3.454 | 0.010 |
| sex | 1.482 | 0.002 |
| urban_rural | 0.950 | 0.000 |

## Segment groups available

ALL, age_band=18-29, age_band=30-44, age_band=45-59, age_band=60+, born_in_country=Born here, born_in_country=Immigrant, education3=Higher, education3=Lower, education3=Middle, ethnic=Black, Non-Hispanic, ethnic=Hispanic, ethnic=Other, Non-Hispanic, ethnic=White, non-Hispanic, income3=High, income3=Low, income3=Medium, religion=Catholic, religion=Jewish, religion=No religion, religion=Other Christian, religion=Other religion, religion=Protestant, sex=Female, sex=Male, urban_rural=Rural, urban_rural=Urban
