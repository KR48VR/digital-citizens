# United States: record citizens versus the chatbot (GSS 2024, 25 questions x 6 groups)

Generated 2026-10-17 09:38 UTC; runtime 34s.

Same questions and groups the chatbot was scored on in the first stress test. Errors in points per answer option; `seg_median` is the typical group, `seg_mean` includes the big misses; `gap_slope` is the share of real group differences reproduced.

| method | pop_median | seg_median | seg_mean | gap_r | gap_slope | n_cells |
|---|---|---|---|---|---|---|
| chatbot on its own | 3.36 | 4.33 | 5.13 | 0.87 | 0.81 | 150 |
| record citizens on their own (mapping from GSS 2022) | 1.63 | 2.36 | 3.26 | 0.90 | 0.92 | 150 |
| real overall number, every group the same | 0.00 | 3.81 | 4.62 |  | 0.00 | 150 |
| real overall number + chatbot group differences | 0.00 | 2.26 | 2.83 | 0.87 | 0.81 | 150 |
| real overall number + record citizens' group differences | 0.00 | 1.82 | 2.21 | 0.90 | 0.92 | 150 |

## By group (typical error, points)

| group | chatbot on its own | record citizens on their own (mapping from GSS 2022) | real overall number, every group the same | real overall number + chatbot group differences | real overall number + record citizens' group differences |
|---|---|---|---|---|---|
| age_band=18-29 | 5.1 | 3.1 | 3.5 | 2.4 | 2.0 |
| age_band=65+ | 4.0 | 2.3 | 3.4 | 1.8 | 2.0 |
| education=Bachelor's or higher | 4.8 | 2.0 | 3.4 | 1.9 | 1.4 |
| party3=Democrat (incl. leaners) | 3.6 | 2.6 | 4.3 | 2.4 | 1.4 |
| party3=Republican (incl. leaners) | 4.1 | 2.3 | 6.5 | 3.1 | 1.8 |
| race_eth=Black, non-Hispanic | 5.1 | 2.0 | 4.3 | 2.6 | 2.2 |
