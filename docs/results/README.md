# Results so far (baselines only; no LLM calls yet)

Produced by `dc baselines gss`, `dc baselines goqa`, `dc baselines twin2k` and `dc personas singapore` on
17 October 2026. These establish the bar a digital-citizen simulator must clear.

| Report | Headline |
|---|---|
| `baselines_gss2024.md` | Copying 2022 answers predicts 2024 US answer shares within 1.4 points per answer option (median question; 2.0 mean); segment shares within 2.8 points; a demographic regression reproduces segment differences with r = 0.77 and the right amount of spread (dispersion ratio 0.98). "Everyone is average" is only clearly worse on party and ideology splits. |
| `baselines_globalopinionqa.md` | The average of other countries predicts a country's shares with median JSD 0.027 (Singapore), 0.031 (US), 0.039 (China), i.e. about 7 points per answer option (3.6 for Singapore's WVS-heavy set). Uniform guessing: JSD 0.15-0.29, 16 points. |
| `baselines_twin2k.md` | On 105 retest items, people agree with themselves 69.4% of the time two weeks later; a no-AI nearest-neighbour rule gets 54.8% (0.79 normalized); modal answer 53.4%. |
| `self_agreement_twin2k.md` | Same people asked twice: 69.2% of answers repeated (80.9% on two-choice items, 44% on six- or seven-choice), but answer shares moved only 1.2 points for everyone and 1.7 for a typical group of 100+; smaller groups moved more. |
| `baselines_wvs7_singapore.md`, `_china.md`, `_united_states.md` | WVS wave 7 microdata (n = 2,012 / 3,036 / 2,596), 74-77 items, 1,500-2,100 question x group cells each. Segments differ most by ethnicity (3.0 pts) and religion (2.6 pts) in Singapore; by age (2.3) and education in China. |
| `stress_test/` | Blind in-session predictions scored against real shares: US good (segment gaps 81% recovered), Singapore and China flattened (36% and 25% of real group differences). |
| `library_test/` | The 'library' idea tested on the US: the closest question from another survey is ~11 points off nationally (10 even with identical wording); record citizens alone 5.2; a fresh 300-person survey + record spread 2.7 national / 3.4 per group. |
| `stress_test/small_survey_holdout.md` | Small real surveys re-scored honestly (fresh sample, hold-out truth): Singapore 300 answers give 3.2 points per group, 2.9 with record spread; 600 give 2.6 / 2.3. Replaces the earlier 1.3-point figure. |
| `personas_singapore.md` | The Nemotron Singapore persona bank matches official sex and broad age shares; ethnicity (inferred from narrative text) is roughly right for Chinese (73% vs 74%) but under-represents Indian (6% vs 9%) and "Others" residents; it carries no explicit ethnicity, religion or income fields. |

The `*_cells.csv` files hold every question x group score for further analysis.
