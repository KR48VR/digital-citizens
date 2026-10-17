# Stress test: claude_fable_5.1_in_session on goqa packet `packet_goqa.json`

30 questions x 3 groups; predictions written without access to the answers; scored against the real shares. Lower is better for jsd/tv/mae_pts.

## country

| method | jsd_median | jsd_mean | tv_median | tv_mean | mae_pts_median | mae_pts_mean | top_box_err_median | top_box_err_mean | max_abs_err_median | max_abs_err_mean | entropy_ratio_median | entropy_ratio_mean | wd_median | wd_mean | representativeness_median | representativeness_mean | n_cells |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| claude_fable_5.1_in_session | 0.025 | 0.033 | 0.117 | 0.127 | 2.731 | 3.536 | 0.045 | 0.069 | 0.079 | 0.103 | 1.094 | 1.182 | 0.169 | 0.214 | 0.970 | 0.962 | 90 |
| other_countries_mean | 0.038 | 0.052 | 0.163 | 0.189 | 4.811 | 5.601 | 0.092 | 0.127 | 0.140 | 0.164 | 1.136 | 1.261 | 0.315 | 0.328 | 0.943 | 0.943 | 90 |
| uniform | 0.327 | 0.331 | 0.556 | 0.541 | 16.233 | 16.144 | 0.143 | 0.243 | 0.371 | 0.416 | 1.730 | 2.402 | 1.371 | 1.569 | 0.771 | 0.732 | 90 |

## By country (median)

| group | jsd_claude_fable_5.1_in_session | jsd_other_countries_mean | jsd_uniform | mae_pts_claude_fable_5.1_in_session | mae_pts_other_countries_mean | mae_pts_uniform |
|---|---|---|---|---|---|---|
| country=China | 0.053 | 0.051 | 0.368 | 3.901 | 5.318 | 17.524 |
| country=Singapore | 0.025 | 0.027 | 0.311 | 2.980 | 3.940 | 16.333 |
| country=United States | 0.014 | 0.043 | 0.296 | 2.040 | 4.866 | 15.631 |

## Worst 10 cells for claude_fable_5.1_in_session

| question_id | group | k | jsd | mae_pts | max_abs_err |
|---|---|---|---|---|---|
| goqa_2295 | country=China | 6 | 0.133 | 13.012 | 0.390 |
| goqa_134 | country=China | 5 | 0.121 | 10.969 | 0.153 |
| goqa_2476 | country=Singapore | 7 | 0.098 | 5.417 | 0.146 |
| goqa_2492 | country=China | 13 | 0.095 | 4.677 | 0.300 |
| goqa_2294 | country=China | 13 | 0.090 | 4.215 | 0.274 |
| goqa_2456 | country=China | 13 | 0.079 | 4.220 | 0.273 |
| goqa_2476 | country=China | 7 | 0.077 | 7.578 | 0.194 |
| goqa_2396 | country=China | 7 | 0.074 | 5.457 | 0.159 |
| goqa_2551 | country=Singapore | 5 | 0.072 | 5.680 | 0.130 |
| goqa_2295 | country=Singapore | 6 | 0.072 | 9.333 | 0.277 |
