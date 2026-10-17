# Stress test: Claude answering in-session, zero-shot, no calibration (17 Oct 2026)

**What was done.** With no API key available, the model in the working session (Claude Fable 5.1) acted as
the simulator. The harness exported question packets *without answers* (`packet_*.json`), the model wrote
its predicted answer shares for each question and group from general knowledge (`predictions_*.py`), and
the harness then scored them against the real shares and against the free baselines on the same cells.
Three cross-country questions and two US questions whose real shares had appeared earlier in the session
were excluded. Reproduce with `dc packet ...` and `dc score-packet ...`.

**Caveats.** This is one model, one prompt, no retrieval, no calibration, and the surveys (GSS 2024, WVS
wave 7) were public before the model's training cutoff, so some answers may be remembered rather than
inferred. It is a floor for what the method can do, not a result to quote as accuracy.

## Cross-country: 30 WVS/Pew questions x United States, China, Singapore

| | Claude in-session | Other countries' average (free baseline) | Uniform guess |
|---|---|---|---|
| Median error per answer option, all 90 cells | **2.7 pts** | 4.8 pts | 16.2 pts |
| United States | **2.0 pts** (JSD 0.014) | 4.9 pts (JSD 0.043) | 15.6 |
| Singapore | **3.0 pts** (JSD 0.025) | 3.9 pts (JSD 0.027) | 16.3 |
| China | **3.9 pts** (JSD 0.053) | 5.3 pts (JSD 0.051) | 17.5 |

Reading: the model beats the strongest free baseline in all three countries on points error, clearly in
the US, modestly in Singapore, and only marginally in China (tied on JSD). This is the Western-bias
pattern the literature predicts: the model knows American opinion best. Worst misses were all in China
(donating to campaigns, views of the EU, "casual sex" and "political violence" scales), where the model
over- or under-estimated how concentrated Chinese answers are.

## United States: 25 GSS 2024 questions x 7 groups (all adults; Democrats; Republicans; 18-29; 65+; Black adults; graduates)

| | Claude in-session | Copy 2022 answers | Regression on demographics | "Everyone is average" |
|---|---|---|---|---|
| Population shares, median error per option | 3.4 pts | **1.4 pts** | 1.3 pts | (exact by construction) |
| Segment shares, median error per option | 4.3 pts | 2.3 pts | **2.0 pts** | 3.8 pts |
| Segment-difference recovery (r / slope / dispersion ratio) | 0.87 / 0.81 / 1.12 | 0.90 / 0.92 / 1.10 | **0.90 / 0.94 / 1.03** | 0 / 0 / 0 |
| Worst group (median error) | 18-29 and Black adults, ~5.1 pts | 18-29, 3.7 pts | 18-29, 2.8 pts | Republicans, 6.5 pts |

Reading:
- On questions a survey has asked before, **the model is 2-3 times worse than simply reusing last wave's
  answers**. Nobody should use a simulator for questions that already have survey data.
- The model gets **direction and rough size of group differences right** (r = 0.87, slope 0.81), with a
  slight tendency to exaggerate them (dispersion ratio 1.12). It did not regress to the mean on these items.
- Its misses are **stale priors**, not noise: it predicted 68% of adults call early-teen sex "always wrong"
  (real: 46%); 65% approve of the school-prayer ruling (real: 46%); 27% of under-30s never go to a bar
  (real: 48%); 32% of Republicans never read a newspaper (real: 52%). The model's picture of America lags
  the 2024 web-survey data on morality, religion and media habits. This is exactly what a calibration
  layer with a small fresh human sample is for.
- On many items it was within 1-3 points: gun ownership, belief in God, confidence in the executive,
  views on immigrants and crime.

## Singapore segments: 20 WVS-7 questions x 10 groups (all; Chinese; Malay; Indian; 21-29; 60+; lower and higher education; Muslims; no religion)

Ground truth is the WVS wave 7 Singapore microdata (n = 2,012, fielded 2019-20), loaded by `data/wvs.py`.

| | Claude in-session | "Everyone is average" (real population shares copied to each group) |
|---|---|---|
| Population shares, median error per option | 4.9 pts (JSD 0.019) | (exact by construction) |
| Segment shares, median error per option | 5.0 pts (6.3 mean) | **2.6 pts** (4.2 mean) |
| Segment-difference recovery (r / slope / dispersion ratio) | 0.54 / **0.36** / **0.65** | 0 / 0 / 0 |
| Worst groups (median error) | 60+ (6.6), 18-29 (6.0), lower education (6.0), Muslims (6.0), Malays (5.9) | |

Reading: **this is the regression-to-the-mean failure, measured.** The model predicted only about a third
of the real differences between Singapore's groups (slope 0.36) and its predicted groups were a third less
spread out than the real ones (dispersion ratio 0.65). Examples:

- Signing a petition: real Singaporeans with lower education 2% have / 10% might / 88% never; the model
  said 10 / 33 / 57. The education gradient was flattened and the whole population was made more activist
  than it is (real 15 / 29 / 56 vs predicted 22 / 40 / 38).
- Worry about losing a job: 52% of Malay respondents "very much" worried; the model said 25%.
- Army rule: 58% of Singaporeans call it "very bad"; the model said 35%. Respect for human rights: 73%
  chose the moderate "fairly much respect"; the model spread answers toward the extremes.
- Where the model was right, it was very right: religion's importance among Malays (81 / 16 / 2 / 1 real
  vs 80 / 16 / 3 / 1 predicted) and abortion views among Malays.
- One caricature: the model made Singaporeans with no religion more militantly secular than they are
  (59% "religion not at all important" predicted vs 31% real).

## China segments: 15 WVS-7 questions x 7 groups (all; urban; rural; 18-29; 60+; lower and higher education)

| | Claude in-session | "Everyone is average" |
|---|---|---|
| Population shares, median error per option | 3.7 pts (5.3 mean) | (exact) |
| Segment shares, median error per option | 3.5 pts (5.3 mean) | **1.2 pts** (1.7 mean) |
| Segment-difference recovery (r / slope / dispersion ratio) | 0.45 / **0.25** / 0.79 | 0 / 0 / 0 |

Reading: China's groups differ less than Singapore's on these items (the "everyone is average" error is
only 1.2 points), so flattening costs less, but the model still reproduced only a quarter of the real
group differences. Its one large miss was a direction error, not a size error: on "having experts, not
government, make decisions", 63% of Chinese respondents said bad or very bad, while the model predicted
77% good or very good (a 35-point miss on one option). It also under-predicted how strongly Chinese
respondents endorse science (40% at the top of the scale, predicted 23%) and democracy as important (47%
at the top, predicted 34%).

## Remedies tested (see `docs/06_how_to_make_it_work.md` for the full table)

| Singapore, segment cells | error (pts, median / mean) | share of real group differences recovered |
|---|---|---|
| Zero-shot model | 5.0 / 6.3 | 36% (r 0.54) |
| + gap scaling or power calibration (leave-one-question-out) | 5.1 / 6.3 | 33% |
| In-context anchors (round 2, 12 new questions; zero-shot vs anchored) | 4.3 / 5.6 vs 4.9 / 6.2 | 52% vs 51% |
| Record-anchored citizens, mapping learned from US + China respondents, no LLM | 4.2 / 6.3 | 52% (r 0.70) |
| Human level + record-anchored differences | **2.1 / 2.7** | 52% |
| Human level + model differences | 2.4 / 3.0 | 36% |
| "Everyone is average" (human level only) | 2.6 / 4.2 | 0% |
| 300 real answers to the question itself | 1.3 / 1.6 | 94% |

China: record anchoring recovers 79% of group differences vs 25% zero-shot; levels are best left to
humans. Files: `record_transfer_summary.csv`, `combination_summary.csv`, `score_wvs_singapore_round2_*.md`.

## What this changes in the plan

1. **Population-level is workable, segment-level is not yet, outside the US.** On population shares the
   model beat the free cross-country baseline in all three countries (US 2.0, Singapore 3.0, China 3.9
   points on the cross-country set; 4.9 and 3.7 points on the fuller WVS sets). But on *how groups differ*
   it reproduced 81% of real gaps in the US and only 36% (Singapore) and 25% (China). Segment-level
   simulation for Asian populations needs grounding in real respondent records and a calibration layer
   before it can be trusted; the harness now measures exactly this.
2. The next real run should test **new** questions (post-cutoff Pew/GSS 2026 items or a commissioned
   survey), not these classic ones, and should add the calibration layer, since the errors are systematic.
3. Group-level distribution prompts are the right default; individual twins remain unproven here.
