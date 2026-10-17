# How we will measure and verify that the digital citizens are accurate enough

**The honest answer first.** Nobody can "make sure" a simulated population is accurate in the abstract.
What we can do is (1) compare it against real people on every kind of question we care about, (2) report
the error alongside every result, (3) only use it for decisions where that error is acceptable, and
(4) keep a small stream of real human answers flowing so the simulation is corrected, not just graded.
This document is the test plan that makes those four things concrete.

## 1. The five levels of fidelity

Each level has a **metric** (how we score), a **floor** (a free, no-AI method the citizens must beat),
and a **ceiling** (the best score anyone could get given that real surveys are themselves noisy).

| Level | Question it answers | Metric(s) | Floor to beat | Ceiling |
|---|---|---|---|---|
| L1 Population | Does the simulated city/country give the right answer shares? | Average absolute error per option (points); Jensen-Shannon divergence (JSD); for ordered scales, Wasserstein distance | "Other countries' average"; "last wave's answer"; uniform | Survey sampling noise (JSD ~0.0002 at n=4,000; ~0.0006 at n=1,000) |
| L2 Segments | Does it get *how groups differ* (age, income, ethnicity, party, neighbourhood)? | Same as L1 per segment; **gap recovery** (correlation and slope of simulated group-vs-population gaps on real gaps); **dispersion ratio** (spread of simulated group answers / spread of real ones, ideal 1.0) | "Everyone is average" (population shares copied to every segment); regression on demographics from last wave | Sampling noise per segment (JSD ~0.001 at n=500) |
| L3 Individuals | Can a twin predict what *this* person will say next? | Accuracy; **normalized accuracy** = accuracy / that person's own test-retest accuracy | Population modal answer; demographic-cell modal answer; k-nearest-neighbour respondents | Human test-retest, same people asked again two weeks later: answers match 69% of the time on average on 105 Twin-2K-500 items (our calculation, `results/baselines_twin2k.md`; 81% on yes/no items, 42-58% on 5-7 option scales) and 81.25% on GSS items (Park et al. 2024, *Generative Agent Simulations of 1,000 People*, arXiv:2411.10109; 1,052 US adults, sd 8.1 points). Both US samples. Group answers barely move: on Twin-2K-500 the same people's answer shares shift 1.7 points for a typical group (`results/self_agreement_twin2k.md`), which is why accuracy is judged on groups. |
| L4 Effects | Does a product/price/policy change move the simulated people the way it moves real people? | Sign agreement; correlation of effect sizes; recovery of which segments react most | "No effect"; expert forecasts | Replication reliability of the human experiment |
| L5 Forecasts | Can it predict a survey *before* it is fielded? | Share of items within the survey's margin of error; calibration of stated uncertainty | Last wave; trend extrapolation | Margin of error of the new survey |

Two testing regimes cut across these levels, because they answer different business questions:

- **New question, known population** (the real use case: "how would Tampines residents react to a new
  transport fee?"). The simulator has never seen human answers to the question. Score it on held-out
  questions, including questions written *after* the model's training cutoff.
- **Known question, new people or new wave** (digital twins, panels). The simulator has seen the
  question and some people's answers; it predicts other people or the next wave.

## 2. The bar, measured on real data today (no AI involved)

The free baselines are already strong. Numbers from `docs/results/` (this repository, October 2026):

| Dataset | What was predicted | Free method | Error (average absolute error per answer option, in points, median question) |
|---|---|---|---|
| GSS 2024 (US, 84 questions, 3,986 people) | Population shares | Copy the 2022 shares | 1.4 points (JSD 0.001); guessing evenly: 13.7 points |
| GSS 2024 | Shares in 10 kinds of segment (3,099 cells) | Copy 2022 shares / regression on demographics | 2.8 / 2.7 points (JSD 0.003); gap recovery r = 0.77, slope 0.77, dispersion ratio 0.98 |
| GSS 2024 | Shares in segments | "Everyone is average" | 3.0 points on the median question (4.0 mean); clearly worse only on party and ideology splits |
| Twin-2K-500 (US, 105 retest items) | A person's answer two weeks later | Nearest-neighbour respondents (no AI) | 54.8% correct vs 69.4% test-retest ceiling = 0.79 normalized accuracy |
| GlobalOpinionQA (WVS + Pew; 1,252 questions, 12 countries) | A country's answer shares | Average of the other countries asked | 6.8 points overall (US 7.0, China 6.4, Singapore 3.6; JSD 0.031 / 0.039 / 0.027); guessing evenly: 16 points |

| WVS wave 7 microdata (Singapore n = 2,012; China 3,036; US 2,596; 74-77 items each) | Shares in segments (sex, age, education, income, religion, ethnicity, urban/rural) | "Everyone is average" | Singapore 2.1 pts median (3.0 mean); China 1.4 (2.3): groups differ modestly on most items, strongly on ethnicity and religion |

(Per-option error is smaller on questions with many options, which is why Singapore's WVS-heavy set
scores lower; JSD is the fairer cross-dataset comparison.)

**First blind stress test (this session's model, no calibration; `docs/results/stress_test/`):** population
shares within 2-5 points in all three countries, better than the free cross-country baseline; but
segment differences were reproduced at 81% of their real size in the US and only 36% in Singapore and
25% in China. The regression-to-the-mean problem is therefore real for Asian populations and is now
measurable with this harness (gap slope and dispersion ratio).

For comparison, Pew's 2026 digital twins (Claude Opus 4.6) had a 12.4-point average error on new
questions in the "new question, known population" regime. So the realistic goal for a first version is
to **beat the free baselines above and stay well under Pew's 12 points on new questions, with segment
differences in the right direction and roughly the right size**, not to match a real survey's 1-3 point precision.

## 3. Proposed pass marks for a "gold standard" (to be agreed with you)

| Level | Must beat | Target for v1 | Stretch |
|---|---|---|---|
| L1 new questions | Other-countries'-average baseline on >= 70% of questions | <= 6 points average absolute error on toplines; no option with 0% simulated share when >= 5% of humans chose it; "not sure" rate within 2x of humans | <= 4 points |
| L2 segments | "Everyone is average" on >= 70% of cells | Gap recovery r >= 0.6 and slope between 0.7 and 1.3; dispersion ratio between 0.7 and 1.3; <= 8 points per segment | r >= 0.75 (the regression baseline's level) |
| L3 individuals | k-NN by >= 5 points of accuracy | Normalized accuracy >= 0.85 | >= 0.9 |
| L4 effects | Sign agreement >= 80% | Effect-size correlation >= 0.7 (published GPT-4 result: 0.85 on US experiments) | Correct ranking of segments by effect size |
| L5 forecasts | Last wave | >= 70% of pre-registered items inside the survey's margin of error | >= 85% |

A country or segment is only called "validated" when it passes L1 and L2 on held-out questions in at
least two topic areas, and the result has been checked once on a survey fielded after the simulation was
locked (L5).

## 4. Specific tests for the known failure modes

| Failure mode | Test | Where it lives |
|---|---|---|
| Regression to the mean (everyone sounds alike) | Dispersion ratio < 0.7, entropy ratio < 0.8, gap slope < 0.7 | `evaluate/metrics.py`, `evaluate/harness.py` |
| Caricature (groups exaggerated) | Dispersion ratio > 1.3, gap slope > 1.3, wrong-sign gaps | same |
| Hyper-accuracy / too confident | "Not sure" and "depends" shares vs humans; knowledge items | GSS "depends"/"don't know" options kept where the survey offers them |
| Answer-order and wording artefacts | Options shuffled per call; paraphrase pairs; report instability as a JSD | `simulate/runner.py` (`shuffle_options`) |
| Western / US bias | Same questions scored per country; compare Singapore and China gaps against the US gap | `data/globalopinionqa.py` |
| Memorised survey results (contamination) | Compare error on questions fielded before vs after the model's training cutoff; pre-registered forecasts | L5 |
| Model drift between versions | A fixed probe set re-run on every model version; all calls cached with model id | `simulate/llm.py` disk cache |
| Persona text adds stereotypes | Ablation: demographics only vs + narrative vs + real record | `--persona-style` flag |

## 5. Rules that keep the test honest

1. **Hold-out vault.** A fixed set of questions per country is never used for prompting, fine-tuning or
   calibration. It is opened only for the periodic report.
2. **Pre-registration.** Before a new survey wave or a commissioned survey is fielded, the simulation's
   predictions are written to the repository with a timestamp and hash. The score is computed after.
3. **Report the floor next to the score.** Every table shows the best free baseline on the same cells.
4. **Report per segment, not just overall.** Pew found errors 30% larger for some groups; we report the
   worst segment, not the average.
5. **Human-in-the-loop calibration.** Each new country or topic area gets a real survey of 1,000-2,000
   people on 30-60 questions. Half calibrates the simulator ("rectification"); half is the vault.
6. **Freeze and version.** Model id, prompt text, persona bank version and calibration data are recorded
   with every result; results are not comparable across versions unless the probe set says they are.

## 6. Glossary

- **Answer shares / distribution**: the percentages choosing each option (for example 22 / 57 / 21).
- **JSD (Jensen-Shannon divergence)**: a 0-to-1 score of how different two sets of answer shares are;
  0 means identical. Roughly, JSD 0.003 is about 5 points of total difference, 0.03 about 16 points.
- **Average absolute error per option (points)**: the Pew-style score; 12.4 means each answer option's share
  was off by 12.4 points on average.
- **Total variation (TV)**: half the sum of absolute differences; 0.05 means answer shares are off by
  5 points in total.
- **Segment**: a group defined by attributes (women 30-44 in Bedok; Republicans; graduates).
- **Gap recovery**: whether the simulation reproduces how much a segment differs from the whole population.
- **Dispersion ratio**: how spread-out the simulated segment answers are compared with real ones.
- **Normalized accuracy**: how well a twin predicts a person, as a fraction of how well that person
  predicts themselves on a repeat survey.
- **Rectification / calibration**: using a small sample of real answers to correct the simulation's bias.
