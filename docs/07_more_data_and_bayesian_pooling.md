# Combing more public data, and pooling it the Bayesian way

Two ideas from the project owner, both tested here: (1) feed the record-based fix more surveys, and
(2) treat every source of evidence, cross-national surveys, each country's own published numbers, and
the simulator's guesses, as forecasters whose weights are learned from their track record, then update
with whatever local data exists. The second is a Bayesian pooling layer; the attitude is the
superforecaster's: many partially informed sources, weighted by past accuracy, revised as evidence lands.

## 1. How the pooling works (plain version)

For any question and group, each source gives a predicted set of answer shares. We treat each source as
"worth N respondents": a source that has been accurate on past questions is worth many respondents, a
poor one is worth few. The estimate is the respondent-weighted average of the sources, plus any real
local answers counted one for one. The weights are learned on other questions, never on the one being
predicted, so the reported gains are out-of-sample. As real local data grows, the sources fade out on
their own. The code is `evaluate/bayes.py`; it accepts any source, including a published crosstab from a
government report with a stated confidence.

## 2. Public data worth combing, by country

What each adds: **records** (individual-level answers, the raw material for record-anchored citizens),
**levels** (published toplines and crosstabs that become priors), **panels** (same people over time,
for individual-level tests), **experiments** (reactions to variants).

| Country | Source | Access | Adds | Status here |
|---|---|---|---|---|
| Cross-national | World Values Survey wave 7, all countries | Open, no login (scripted) | Records: ~90,000 people, 60+ countries, same questionnaire | Downloaded, used below |
| Cross-national | WVS wave 6 (2010-14), EVS, ISSP, Asian Barometer, Pew Global Attitudes | WVS/EVS open; ISSP and Asian Barometer by registration; Pew by account | Records and levels for time trends and East Asian coverage | Not yet |
| Singapore | Department of Statistics tables (data.gov.sg, SingStat), General Household Survey 2025, Census 2020 | Open aggregates; microdata only on-site for local universities | Levels, census margins for weighting | Margins used for persona checks |
| Singapore | Institute of Policy Studies surveys (race, religion, social cohesion, 2024 n = 4,000), National Youth Survey, REACH polls, HDB sample household survey, MOM labour-force tables | Published reports and tables; microdata by partnership | Levels and crosstabs by ethnicity, age, income: ideal Bayesian priors | To collect; needs a table-extraction pipeline |
| Singapore | Asian Barometer waves 5-6 (2020, 2023), Pew 2022 religion survey, Pew 2026 Global Attitudes | Academic application / Pew account | Records (n ≈ 1,000 each), recent levels | Needs an account or partner |
| Singapore | Singapore Life Panel (SMU), IPS panel (NUS) | Closed | Panels | Partner only |
| China | CGSS 2021/2023 (n ≈ 11,000), CFPS panel, CSS | Registration (overseas allowed) / application | Records, panels, within-China regional structure | Needs registration in your name or an institution's |
| China | WVS 6 and 7, Asian Barometer 4-5, Zuobiao ideology survey (n ≈ 460,000, opt-in) | WVS open; others academic | Records | WVS downloaded |
| China | National Bureau of Statistics yearbooks, provincial statistical tables | Open aggregates | Levels and census margins | To collect |
| Taiwan (Mandarin pilot) | Taiwan Social Change Survey, TEDS election surveys, Asian Barometer 6 | Free via SRDA (registration) | Records in Mandarin with open access | Not yet |
| United States | GSS 1972-2024, CES 2024 (60,000 people, direct download), ANES 2024, Pew ATP, ACS public-use microdata | GSS and CES open; ANES and Pew by account | Records at scale, panels, census margins | GSS used; CES next |
| United States | Twin-2K-500, the 70-experiment replication set | Open | Panels and experiments | Twin-2K-500 used |

Rule of thumb: for a new city or segment, the Bayesian layer lets us start from the cross-national
records and the country's published tables on day one, and improve every time a local number arrives,
instead of waiting for a full local survey.

## 3. Results: feeding the record-based fix 61 countries instead of 2

Record-anchored citizens predict a Singapore respondent's answer to a new question from their answers to
the other 70 questions, using a mapping learned from respondents elsewhere. With the mapping learned from
US and Chinese respondents only (5,600 people) the method already beat the model's own guesses on group
differences. Learning it from all 61 other WVS-7 countries (90,669 people) improves it further
(`docs/results/stress_test/record_transfer_all_countries.md`; leave-nothing-in: Singapore's own data is
never used in the mapping):

| Singapore, 20 questions x 10 groups | Population error (pts) | Segment error, median / mean (pts) | Group differences: direction (r) / size captured |
|---|---|---|---|
| Model zero-shot | 4.9 | 5.0 / 6.3 | 0.54 / 36% |
| Record-anchored, mapping from 2 countries | 3.9 | 4.2 / 6.3 | 0.70 / 52% |
| Record-anchored, mapping from 61 countries | **3.0** | **3.7 / 4.5** | **0.73** / 42% |
| Human level + record differences (2 countries) | (human) | 2.1 / 2.7 | 0.70 / 52% |
| Human level + record differences (61 countries) | (human) | **1.9 / 2.6** | 0.73 / 42% |
| Everyone is average (human level only) | (human) | 2.6 / 4.2 | 0 |

China (15 questions x 7 groups): record-anchored from 61 countries gets the population within 3.2 points
(model: 3.7) and, with human levels, segment error of 1.0 / 1.4 points, now below the "everyone is
average" floor (1.2 / 1.7).

What more countries buy: the *direction* of group differences gets more reliable (r 0.54 → 0.73) and the
levels get much closer, but the *size* of the differences is still under-stated (42-52% of the real
gaps). Concrete cells in Singapore: lower-educated residents who would never sign a petition, real 88%:
model 57%, record-anchored (2 countries) 59%, record-anchored (61 countries) 75%, with human level 83%.
Malay respondents very worried about losing their job, real 52%: model 25%, 2 countries 16%, 61 countries
29%, with human level 36%. The second case shows the remaining gap: no amount of foreign data knows
Singapore-specific facts like the Malay community's economic anxiety; that needs Singapore's own data,
which is what the Bayesian layer is for.

## 4. Results: Bayesian pooling with local data

Setup (`scripts/pool_experiment.py`, `evaluate/bayes.py`): two sources, the model's zero-shot guesses and
the record-anchored citizens (61-country mapping), are pooled as weighted priors and then updated with one
simulated local survey of 150, 300 or 600 Singaporeans, where each group gets whoever happened to fall
into the sample (a 150-person survey contains about 18 Malays and 40 people aged 60+). Source weights are
learned on the other 19 questions with local samples of the same size, so they are out-of-sample.

| Singapore, 20 questions x 10 groups | Population error (median) | Segment error, median / mean | Group differences, size captured |
|---|---|---|---|
| Model zero-shot alone | 4.9 | 5.0 / 6.3 | 36% |
| Record-anchored citizens alone | 3.0 | 3.7 / 4.5 | 42% |
| **Pooled prior, no local data** | **2.5** | **3.4 / 4.5** | 40% |
| Local survey of 150 alone | 1.0 | 2.4 / 2.9 | 95% |
| Pooled + local survey of 150 | 1.2 | 2.3 / 3.0 | 62% |
| Local survey of 300 alone | 0.8 | 1.7 / 1.9 | 99% |
| Pooled + local survey of 300 | 0.8 | 1.6 / 2.2 | 79% |
| Local survey of 600 alone | 0.4 | 1.1 / 1.2 | 96% |
| Pooled + local survey of 600 | 0.4 | 1.1 / 1.4 | 86% |

Learned weights: the record-anchored citizens are worth about 27-36 real respondents per group, the
model's own guesses about 8-11. The "other countries' average" was tried as a third source and received
zero weight for segments, as it should (it is the same for every group).

What this says, plainly:

1. **Pooling the two simulators beats either alone** (2.5 vs 3.0 and 4.9 points on population shares;
   3.4 vs 3.7 and 5.0 on segments). This is the right default when there is no local data.
2. **A small local survey beats the simulators quickly.** 150 real Singaporeans, spread across groups as
   they fall, already give lower error than any simulator, and capture 95% of the real group differences.
3. **Adding the simulators to a local survey helps only the typical cell, slightly, and hurts the big
   gaps.** With 150 local answers the pooled estimate improves the median cell (2.3 vs 2.4) but shrinks the
   large real differences (size captured 62% vs 95%), so the mean error is no better. By 600 the prior is
   irrelevant. The simulators' remaining value is therefore for questions with no local data at all, and
   for the smallest groups inside a small survey. The per-group breakdown
   (`bayes_pooling_singapore_total_cells.csv`) confirms this only for the smallest group: with a 150-person
   survey, pooling cuts the error for Indian respondents (about 14 people in such a survey) from 3.9 to 3.3
   points and for the no-religion group from 2.6 to 2.1, but it *worsens* Malays (4.0 → 4.4), people aged
   60+ (2.4 → 3.0) and the young (2.8 → 3.4), because the simulators pull these distinctive groups toward
   the average. A better pooling rule would weight the prior by group size, not one weight for all.
4. **The honest ranking for a new Singapore question is:** ask 150-300 real people if you can (cheap, and
   it wins); if you cannot, use the pooled prior (record-anchored citizens plus the model) and expect about
   3.5 points of error on segments with group differences under-stated by half; never use the model alone.

This also answers the "superforecasting" idea precisely: the machinery for weighting sources by track
record and updating with evidence works and is built, but the evidence it is fed matters more than the
weighting. The sources that would make it shine are Singapore's own published crosstabs (IPS, DOS,
REACH), which carry the local facts no foreign record can, and those are the next thing to comb.
