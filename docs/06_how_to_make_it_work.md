# How to make it work instead of regress

The first stress test showed the failure: for Singapore and China the model's zero-shot predictions
reproduced only a quarter to a third of the real differences between groups. This document reports what
we then tried, with numbers, and lays out the build plan that follows from them. All experiments use the
WVS wave 7 microdata (Singapore n = 2,012; China 3,036; US 2,596) and the GSS 2024 (US, 3,986), scored
out-of-sample. Details and files are in `docs/results/stress_test/`.

## 1. What we tried, and what happened

| Remedy | What it is | Singapore result (segment error in points; share of real group differences recovered) | Verdict |
|---|---|---|---|
| Zero-shot model (the baseline failure) | Ask the model what each group would answer | 5.0 pts; 36% | Flattens |
| Stretch the model's group differences (gap scaling) | Learn on other questions how much the model under-states gaps, then scale them up | 5.1 pts; 33% | **No help.** The model's gaps are only half-correlated with reality (r = 0.54), so stretching them stretches noise. The problem is wrong gaps, not just small ones. |
| Sharpen/soften the model's answer shares (power calibration) | Fit one exponent on other questions | 5.0 pts | No help |
| Show the model real answers of each group on 6 other questions (in-context anchoring) | A second blind round of 12 new questions, with and without anchors | 4.3 pts without, 4.9 pts with; 52% vs 51% | **No help** overall. It improved the groups the anchors described best (Malays, 60+) and worsened others. A handful of anchors shifts errors around rather than removing them. |
| Record-anchored citizens, no LLM | Each real Singapore respondent's answers to the other 70 questions predict their answer to the new one, using a mapping learned from US and Chinese respondents, then aggregated by group | 4.2 pts; **52%** (r = 0.70 vs 0.54); population error 3.9 vs 4.9 | **Helps.** Real records carry group structure the model's priors lack. In China: 79% of gaps recovered vs 25%. |
| Human level + record-anchored differences | Humans supply each question's population shares; records supply how groups differ | **2.1 pts median, 2.7 mean** vs 2.6 / 4.2 for "everyone is average" | **Best.** 35% lower mean error than copying the population to every group, and far below any model-only method. |
| Human level + model differences | Same, with the zero-shot model's group differences | 2.4 / 3.0 | Helps, less |
| 300 real answers to the question itself | A small survey; segment shares read straight off it | **1.3 pts; 94%** | Beats everything. For questions you can afford to ask 300 people, do not simulate. |

US comparison: the zero-shot model already recovered 81% of group differences; "human level + model
differences" cut segment error from 3.8 to 2.2 points. China: groups differ so little on these items
(1.2 points) that nothing beats "everyone is average", but record anchoring fixes the direction of the
differences (79% recovered vs 25%).

## 2. What this means

1. **The flattening is not a tuning problem.** Temperature, prompt wording, "be diverse" instructions and
   simple post-hoc stretching do not fix it, here or in the literature. The model does not know how
   Singapore's groups differ; it guesses from stereotypes, half right.
2. **The signal is in real respondent records.** A Malay respondent's 70 other answers say more about how
   she will answer a new question than the word "Malay" does. The citizens must be anchored to real
   records, and the population skeleton (census margins, Nemotron personas) is only the frame those
   records hang on.
3. **Split the job: humans set the level, the model and the records set the differences.** Measuring a
   question's population share needs a few hundred people and is cheap; measuring every segment needs
   thousands. The simulator's value is in the segment breakdown and in reactions to variants (prices,
   messages, designs), not in the topline. This is the "prediction-powered" design the 2026 literature
   converged on, and our numbers agree.
4. **Known question, any country: do not use an LLM.** Last wave's answers (US), a crosstab, or a
   300-person sample all beat the model by 2-4x. The simulator is for *new* questions and *new* variants.

## 3. The build plan that follows (phase 1, US + Singapore)

| Step | What | Why (evidence above) | Needs |
|---|---|---|---|
| 1 | **Record-anchored personas.** Each digital citizen = one real WVS/GSS respondent (anonymous), carrying 50-200 of their real answers, re-weighted to census margins (Nemotron skeleton for Singapore, ACS for the US) | Records recover 52-79% of group differences vs 25-36% for zero-shot | Done for WVS and GSS; add CES 2024 (60k US) and, with partners, IPS or Asian Barometer Singapore |
| 2 | **Role-play with records, not demographics.** The LLM answers *as each respondent*, reading their record; answers are aggregated by segment. Ablate: demographics only vs + record vs + narrative | Park et al.: interview-based agents 85% of human retest; our transfer result | API key; ~25k calls per 100-question run |
| 3 | **Statistical twin as a floor and a feature.** Keep the no-LLM record model from this test as the baseline every LLM run must beat, and as a feature the LLM sees ("people with answers like yours tend to...") | It already beats zero-shot on differences at zero cost | Done (`evaluate/transfer.py`) |
| 4 | **Human-level calibration on every new topic.** For each new product/policy study, field the question to 150-300 people (an omnibus in Singapore costs a few thousand dollars per question); pool the simulators in as weighted priors for the smallest groups and for questions that cannot be fielded | 1.9-2.3 vs 5.0 points; pooled prior alone 3.4 | Fieldwork budget; `evaluate/calibrate.py`, `evaluate/bayes.py` |
| 5 | **Verify differences, not levels, in the gate.** Pass marks for a country: gap recovery r >= 0.7 and slope 0.7-1.3 on held-out questions, with the human-level design | Levels are solved by humans; differences are the simulator's job | Done (harness) |
| 6 | **Fine-tune a small open model on survey panels** (SubPOP recipe) only after 1-4, with cross-country held-out tests to avoid erasing cultural variance | Fine-tuning cut distribution error 46% in the US but can collapse cultural differences | GPU or hosted fine-tuning |
| 7 | **Country-specific models for Mandarin** (Qwen, DeepSeek) tested head-to-head on the same China/Taiwan packets | Published tests show no model is good here yet | API access |

Steps 1, 3, 4 and 5 are built. Steps 2, 6 and 7 need model access.

## 4. What to expect

With records, human-measured levels and the harness in the loop, a realistic phase-1 target for Singapore
is segment shares within 2-3 points and 60-70% of real group differences recovered on new questions, with
every result shown next to its baseline. Individual-level twins remain unproven and are not on this
path. Treatment effects (reactions to variants) are untested here; that is what the commissioned
Singapore survey with embedded experiments is for.
