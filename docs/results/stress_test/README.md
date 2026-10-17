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

## What this changes in the plan

1. The method is viable at the group level for the US and Singapore without any training, and marginal for
   China, consistent with the literature. Singapore error (3.0 pts) is close to the US (2.0) on these
   WVS items, which is encouraging for the Singapore-second plan.
2. The next real run should test **new** questions (post-cutoff Pew/GSS 2026 items or a commissioned
   survey), not these classic ones, and should add the calibration layer, since the errors are systematic.
3. Group-level distribution prompts are the right default; individual twins remain unproven here.
