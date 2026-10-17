# Stress test: claude_fable_5.1_in_session on wvs packet `packet_wvs_china.json`

15 questions x 7 groups; predictions written without access to the answers; scored against the real shares. Lower is better for jsd/tv/mae_pts.

## population

| method | jsd_median | jsd_mean | tv_median | tv_mean | mae_pts_median | mae_pts_mean | top_box_err_median | top_box_err_mean | max_abs_err_median | max_abs_err_mean | entropy_ratio_median | entropy_ratio_mean | wd_median | wd_mean | representativeness_median | representativeness_mean | n_cells |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| claude_fable_5.1_in_session | 0.012 | 0.023 | 0.089 | 0.120 | 3.676 | 4.940 | 0.022 | 0.042 | 0.071 | 0.097 | 1.061 | 1.171 | 0.205 | 0.307 | 0.950 | 0.943 | 15 |
| population_marginal_for_segments | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 1.000 | 1.000 | 0.000 | 0.000 | 1.000 | 1.000 | 15 |
| uniform | 0.149 | 0.173 | 0.385 | 0.395 | 15.707 | 18.466 | 0.153 | 0.185 | 0.298 | 0.289 | 1.376 | 1.719 | 0.920 | 1.367 | 0.777 | 0.758 | 15 |

## segment

| method | jsd_median | jsd_mean | tv_median | tv_mean | mae_pts_median | mae_pts_mean | top_box_err_median | top_box_err_mean | max_abs_err_median | max_abs_err_mean | entropy_ratio_median | entropy_ratio_mean | wd_median | wd_mean | representativeness_median | representativeness_mean | n_cells |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| claude_fable_5.1_in_session | 0.017 | 0.027 | 0.106 | 0.130 | 3.455 | 5.326 | 0.022 | 0.047 | 0.077 | 0.103 | 1.067 | 1.187 | 0.222 | 0.328 | 0.956 | 0.938 | 90 |
| population_marginal_for_segments | 0.001 | 0.004 | 0.034 | 0.045 | 1.169 | 1.711 | 0.010 | 0.019 | 0.026 | 0.036 | 1.005 | 1.021 | 0.069 | 0.104 | 0.985 | 0.979 | 90 |
| uniform | 0.164 | 0.178 | 0.388 | 0.400 | 16.832 | 18.654 | 0.161 | 0.186 | 0.286 | 0.292 | 1.400 | 1.773 | 0.927 | 1.376 | 0.777 | 0.757 | 90 |

## Segment differences (gap recovery; dispersion ratio ideal = 1)

| method | gap_r | gap_slope | dispersion_ratio |
|---|---|---|---|
| claude_fable_5.1_in_session | 0.447 | 0.246 | 0.790 |
| uniform |  | 0.000 | 0.000 |

## By group (median mae_pts)

| group | claude_fable_5.1_in_session | population_marginal_for_segments | uniform |
|---|---|---|---|
| ALL | 3.676 | 0.000 | 15.707 |
| age_band=18-29 | 2.473 | 1.736 | 18.909 |
| age_band=60+ | 3.828 | 2.259 | 14.184 |
| education3=Higher | 2.896 | 1.223 | 18.938 |
| education3=Lower | 3.530 | 0.493 | 15.340 |
| urban_rural=Rural | 2.972 | 0.787 | 16.699 |
| urban_rural=Urban | 3.638 | 0.501 | 16.356 |

## Worst 10 cells for claude_fable_5.1_in_session

| question_id | group | k | jsd | mae_pts | max_abs_err |
|---|---|---|---|---|---|
| Q236 | age_band=18-29 | 4 | 0.175 | 23.891 | 0.438 |
| Q236 | education3=Higher | 4 | 0.141 | 21.654 | 0.369 |
| Q236 | urban_rural=Urban | 4 | 0.132 | 20.747 | 0.373 |
| Q236 | ALL | 4 | 0.120 | 19.799 | 0.347 |
| Q236 | education3=Lower | 4 | 0.114 | 19.051 | 0.335 |
| Q236 | age_band=60+ | 4 | 0.109 | 18.816 | 0.319 |
| Q236 | urban_rural=Rural | 4 | 0.109 | 18.809 | 0.317 |
| Q163 | age_band=60+ | 10 | 0.089 | 6.094 | 0.206 |
| Q163 | urban_rural=Rural | 10 | 0.062 | 5.267 | 0.160 |
| Q64 | urban_rural=Rural | 4 | 0.059 | 12.699 | 0.187 |
