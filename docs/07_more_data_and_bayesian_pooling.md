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
| Local survey of 150 alone | 2.2 | 4.8 / 5.3 | 84% |
| Pooled + local survey of 150 | 1.9 | 3.0 / 3.6 | 57% |
| Local survey of 300 alone | 1.8 | 3.6 / 3.9 | 90% |
| Pooled + local survey of 300 | 1.6 | 2.7 / 3.1 | 69% |
| Local survey of 600 alone | 1.4 | 2.7 / 3.0 | 89% |
| Pooled + local survey of 600 | 1.4 | 2.4 / 2.7 | 77% |

(Local-survey rows corrected 17 Oct, later in the day: each simulated survey is now scored against the
respondents not in it and the scores, not the predictions, are averaged over draws. The first version
averaged three draws before scoring, which made a 150-person survey behave like one of 450. See docs/08 §4.)

Learned weights: the record-anchored citizens are worth about 27-36 real respondents per group, the
model's own guesses about 8-11. The "other countries' average" was tried as a third source and received
zero weight for segments, as it should (it is the same for every group).

What this says, plainly:

1. **Pooling the two simulators beats either alone** (2.5 vs 3.0 and 4.9 points on population shares;
   3.4 vs 3.7 and 5.0 on segments). This is the right default when there is no local data.
2. **A small local survey plus the simulators beats both.** 150 real Singaporeans, spread across groups
   as they fall, give 4.8 points of error on groups when read straight off the survey (a group of 15-20
   people is noisy); pooled with the simulators, 2.9. At 300 answers the pair is 3.6 vs 2.6; at 600, 2.7
   vs 2.4. The simulators are worth most for the smallest groups: with 150 answers the error for Indian
   respondents falls from 8.2 to 2.9 points, Malays 6.2 to 3.6, Muslims 6.5 to 3.9, while the big Chinese
   group barely moves (2.5 to 2.3). The learned weights say why: the record-anchored citizens count for
   about 27-36 real respondents per group, the model for 8-11, so they matter where a survey has fewer
   real people than that.
3. **The price is flattened differences.** A small survey's group differences come out too large (noise
   inflates them: 2.1 times the real spread at 150 answers), the pooled estimate's too small (57% of the
   real size at 150, 69% at 300, 77% at 600). Use the pooled numbers for each group's level and for
   which groups differ most; as the survey grows, trust its own differences for how large a gap is.
   A better pooling rule would weight the prior by group size rather than one weight for all.
4. **The honest ranking for a new Singapore question is:** ask 150-300 real people if you can and pool
   them with the simulators (3.0 / 2.7 points on groups); if you cannot, use the pooled prior
   (record-anchored citizens plus the model) and expect about 3.4 points on segments with group
   differences under-stated by half; never use the model alone (5.0).

This also answers the "superforecasting" idea precisely: the machinery for weighting sources by track
record and updating with evidence works and is built, but the evidence it is fed matters more than the
weighting. The sources that would make it shine are Singapore's own published crosstabs (IPS, DOS,
REACH), which carry the local facts no foreign record can, and those are the next thing to comb.

## 5. Results: Singapore's own published findings as evidence (the ledger)

Two research passes combed Singapore's official, academic and commercial sources (list and verdicts in
`docs/sources/singapore_published_findings.md`). 96 findings with group breakdowns were mapped onto 25 of
the World Values Survey questions we test, with a confidence score for how close the wording, population
and year are (`data/ledger/singapore.csv`). Each finding enters the pool as pseudo-respondents: sample size
times confidence, spread over the answer options. Scored against the WVS-7 Singapore answers on the 67
cells the ledger covers (`docs/results/stress_test/ledger_experiment_singapore.md`):

| Estimate for the covered cells | Error, median / mean (points) |
|---|---|
| Pooled prior: record-anchored citizens + model, no local evidence | **3.8 / 4.4** |
| Published findings alone | 8.0 / 8.3 |
| Pooled prior + published findings at face value | 6.8 / 7.2 |
| Pooled prior + published findings with a learned weight | 4.0 / 4.5 |
| Everyone is average (real population level) | 2.9 / 4.4 |

The learned weight, fitted question by question on the other questions, settles at about **1% of face
value**: a published result from 1,000 people is worth about 10 respondents when it is asked in different
words, by a different survey, in a different year. Even the 16 rows with near-identical wording were a
median 4.7 points from the WVS answer; rows with loose wording matches were 9-10 points off; opt-in online
polls 19 points. Part of this is genuine change between 2020 and 2024, but most of it is what survey
researchers call house and wording effects, and it is larger than the simulators' own error.

Where published numbers did help, even at face value, was where the prior was weak and the wording close:
unwillingness to have neighbours of another race (error 10.5 → 5.9), signing petitions among the young
(2.4 → 1.7), attending demonstrations, satisfaction with how the political system works, importance of
democracy, feeling safe. Where they hurt, badly, was wherever a plausible-looking match was really a
different question: "following politics closely" (an opt-in poll's 76%) against "interested in politics",
"get rid of elections and let experts decide" against "experts make decisions", a 2016 reading of trust
against a 2020 one.

**What this means for the plan.**

1. Public findings are worth collecting, but as a *check* and as *priors with learned weights*, never at
   face value. The pooling layer now learns that weight, so the machinery is safe to feed.
2. The only published evidence worth much is a question asked in the same words, of the same population,
   recently. That argues for *running* the questions you care about, even on a small sample, over mining
   other people's questions; a 150-person survey beat every simulator and every published proxy in section 4.
3. The record-anchored citizens remain the best starting point when nothing local exists. Their value is
   that they carry the structure of a person, which published tables do not.
4. News reports, social media and commercial polls were the weakest tier (opt-in polls 19 points off) and
   should be treated as topic salience signals, not as answer shares.
