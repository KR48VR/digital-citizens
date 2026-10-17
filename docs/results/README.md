# Results so far (baselines only; no LLM calls yet)

Produced by `dc baselines gss`, `dc baselines goqa`, `dc baselines twin2k` and `dc personas singapore` on
17 October 2026. These establish the bar a digital-citizen simulator must clear.

| Report | Headline |
|---|---|
| `baselines_gss2024.md` | Copying 2022 answers predicts 2024 US answer shares within 1.4 points per answer option (median question; 2.0 mean); segment shares within 2.8 points; a demographic regression reproduces segment differences with r = 0.77 and the right amount of spread (dispersion ratio 0.98). "Everyone is average" is only clearly worse on party and ideology splits. |
| `baselines_globalopinionqa.md` | The average of other countries predicts a country's shares with median JSD 0.027 (Singapore), 0.031 (US), 0.039 (China), i.e. about 7 points per answer option (3.6 for Singapore's WVS-heavy set). Uniform guessing: JSD 0.15-0.29, 16 points. |
| `baselines_twin2k.md` | On 105 retest items, people agree with themselves 69.4% of the time two weeks later; a no-AI nearest-neighbour rule gets 54.8% (0.79 normalized); modal answer 53.4%. |
| `personas_singapore.md` | The Nemotron Singapore persona bank matches official sex and broad age shares; ethnicity (inferred from narrative text) is roughly right for Chinese (73% vs 74%) but under-represents Indian (6% vs 9%) and "Others" residents; it carries no explicit ethnicity, religion or income fields. |

The `*_cells.csv` files hold every question x group score for further analysis.
