# Baselines on GlobalOpinionQA (WVS wave 7 + Pew Global Attitudes)

Questions used: 1252 (answered by at least 2 of the selected countries); countries: United States, China, Singapore, Japan, Germany, Britain, India (Current national sample), Indonesia, Malaysia, S. Korea, Vietnam, Taiwan ROC.

The 'other countries' mean' baseline predicts a country's answer shares as the average of every other country that was asked the same question. Prior work found LLMs struggle to beat it on country means.

## By country (median over questions)

| country | jsd_other_countries_mean | jsd_uniform |
|---|---|---|
| Britain | 0.015 | 0.107 |
| China | 0.039 | 0.257 |
| Germany | 0.026 | 0.153 |
| India (Current national sample) | 0.074 | 0.105 |
| Indonesia | 0.040 | 0.159 |
| Japan | 0.037 | 0.171 |
| Malaysia | 0.036 | 0.226 |
| S. Korea | 0.030 | 0.164 |
| Singapore | 0.027 | 0.286 |
| Taiwan ROC | 0.029 | 0.336 |
| United States | 0.031 | 0.150 |
| Vietnam | 0.048 | 0.286 |

| country | n_other_countries_mean | n_uniform |
|---|---|---|
| Britain | 845 | 845 |
| China | 365 | 365 |
| Germany | 1085 | 1085 |
| India (Current national sample) | 367 | 367 |
| Indonesia | 813 | 813 |
| Japan | 826 | 826 |
| Malaysia | 508 | 508 |
| S. Korea | 563 | 563 |
| Singapore | 271 | 271 |
| Taiwan ROC | 212 | 212 |
| United States | 911 | 911 |
| Vietnam | 388 | 388 |

Sampling-noise floor assuming n=1,000 per country: median JSD 0.0006

## Overall

| method | jsd_median | jsd_mean | tv_median | tv_mean | mae_pts_median | mae_pts_mean | top_box_err_median | top_box_err_mean | max_abs_err_median | max_abs_err_mean | entropy_ratio_median | entropy_ratio_mean | wd_median | wd_mean | representativeness_median | representativeness_mean | n_cells |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| other_countries_mean | 0.031 | 0.057 | 0.160 | 0.187 | 6.820 | 8.510 | 0.083 | 0.114 | 0.139 | 0.162 | 1.071 | 1.179 | 0.295 | 0.359 | 0.929 | 0.913 | 7154 |
| uniform | 0.168 | 0.192 | 0.390 | 0.392 | 16.222 | 17.449 | 0.149 | 0.199 | 0.291 | 0.317 | 1.398 | 1.711 | 0.878 | 1.016 | 0.781 | 0.772 | 7154 |
