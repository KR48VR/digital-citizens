# Where to start: assessment of the United States, China, Singapore and alternatives

**Recommendation in one paragraph.** Build the gold standard on the **United States** and run
**Singapore as the transfer test from day one**. Defer mainland **China** to a later phase, and use
**Taiwan** (open Mandarin-language survey data) as the Mandarin pilot in the meantime. The US is the only
place where every level of the test plan can be run today on open data; Singapore is small, well-measured,
has a government-backed persona dataset and the same cross-national questionnaires as the US, so it is
the cheapest place to prove the method travels. China has good academic microdata but new surveys need a
state licence, remote data access is a cross-border transfer under Chinese law, and every published test
shows even Chinese-built models answer "like Americans"; it is the hardest place to validate, not the
easiest. Your hunches were right on the US and on China having good data; the twist is that *having* data
and being *able to validate against it from outside China* are different things.

## 1. Scoring the candidates

| Criterion | United States | Singapore | China (mainland) | Taiwan | South Korea / Japan | UK |
|---|---|---|---|---|---|---|
| Open individual-level attitude data (L1, L2) | Excellent: GSS 1972-2024, ANES 2024, CES 2024 (60k), Pew ATP, all open or free registration | Good via cross-national surveys (WVS-7 n=2,012, Asian Barometer 2020/2023, Pew 2022/2026); national statistics microdata only on-site for local university staff | Good but gated: CGSS 2023 (n=11,326, free registration, overseas allowed), CFPS panel (application), CSS; no census microdata after 2000 | Good: Taiwan Social Change Survey free via SRDA, Asian Barometer, WVS-8 under way | Good: KGSS, JGSS (academic access) | Excellent: Understanding Society, BSA, BES |
| A panel for individual-level tests (L3) | Yes: Twin-2K-500 (open), GSS panel, Pew ATP; note PSID forbids LLM use | Closed: Singapore Life Panel (ages 50-70, SMU) and NUS panel do not release data; would need a partner or our own panel | CFPS, CHARLS (application) | TSCS panels | KLIPS etc. | Understanding Society |
| Experiments to test effects (L4) | Yes: 70-experiment replication set, Twin-2K-500 experiments and 40-product pricing study | None public; must be commissioned (cheap at n=2,000) | None public; fieldwork needs a licensed domestic agency | Some academic | Some | Some |
| Same questions asked across countries | WVS-7/8, Pew Global, ISSP | WVS-7 (WVS-8 planned 2025-26, funding pending), Asian Barometer, Pew Global 2026 | WVS-7 only; not in WVS-8 list, not in Asian Barometer wave 6, ISSP lapsed | WVS-8, ISSP, Asian Barometer 6 | WVS-8, ISSP, Asian Barometer 6 | WVS-7, ISSP |
| Census-grounded persona skeleton | Nemotron-Personas-USA (1M records, CC BY) | Nemotron-Personas-Singapore (148k records, all 55 planning areas, co-launched with AI Singapore, Jan 2026) | None | None | Nemotron-Korea, Nemotron-Japan | None |
| How well LLMs already know the population | Best of any country, but Pew still measured 12-point errors | Unknown: no published benchmark (an opportunity) | Poor: Chinese and US models both skew to US views on values questions | Zero-shot below a simple supervised model | Japan: near-zero agreement in one WVS study | Good |
| Language | English | English for surveys; Mandarin, Malay, Tamil for realism | Mandarin (simplified); regional variation | Mandarin (traditional) | Korean / Japanese | English |
| Regulatory and practical friction | Low | Low-moderate (statistics microdata gated; government receptive: AI Singapore, SSRC 5-year grant on policy simulation at NUS) | High (survey licence, PIPL cross-border rules, politically sensitive items, model content limits) | Low | Low | Low |
| Size and heterogeneity | 335M, very heterogeneous | 6.1M total, 3.7M citizens; 4 ethnic groups, 55 planning areas; tractable as a *whole* population | 1.4B, extreme urban/rural and regional variation | 23M | 52M / 125M | 68M |

Sources for the data landscape are listed in `docs/01_what_the_evidence_says.md` and in the research
notes (GSS, ANES, CES, Pew ATP, CGSS/CFPS access pages, Singapore DOS AMAP page, WVS and Asian Barometer
coverage pages, NVIDIA Nemotron dataset cards).

## 2. Why the United States first

- It is the only country where **all five levels** of the test plan can run on open data this quarter:
  population and segment shares (GSS 2024, CES 2024), individuals with a retest (Twin-2K-500), experiments
  (the 70-study replication set, Twin-2K-500's built-in experiments and pricing study), and a forward test
  (GSS 2026 fieldwork, Pew waves).
- The published literature gives us **reference scores to beat** (Pew's 12.4 points, Park's 0.85 normalized
  accuracy, the 0.85 effect-size correlation) and open benchmarks (OpinionQA, SubPOP, SimBench).
- It is the cheapest place to learn *what works* (prompt form, persona layers, calibration) before paying
  for fieldwork elsewhere.

The risk is the opposite of what you might expect: the US is where models are *best*, so US results will
overstate how well the method travels. That is exactly why Singapore runs in parallel.

## 3. Why Singapore second (and from day one)

- **Whole-population simulation is feasible.** With 3.7M citizens, 55 planning areas and a 148k-record
  census-grounded persona bank already published, Singapore is the one place where "simulate the entire
  population" is a realistic early milestone rather than a slogan.
- **Ground truth exists for L1 and L2 now**: WVS-7 Singapore (n=2,012, 2019-20, open), Asian Barometer waves
  5 and 6 (2020, 2023; academic access), Pew's 2022 religion survey and 2026 Global Attitudes, and the
  Institute of Policy Studies' large face-to-face surveys (published as tables; microdata by partnership).
  GlobalOpinionQA already carries 271 Singapore questions, which our harness scores today.
- **Nobody has published a Singapore benchmark.** Being first to measure how well LLMs reproduce
  Singaporean opinion, across four ethnic groups and in four languages, is a publishable result and a
  credibility asset for everything that follows. Our own first blind test (WVS-7 Singapore microdata,
  20 questions x 10 groups) found population shares within about 5 points but group differences
  flattened to a third of their real size, so the Singapore work must start from real respondent records,
  not from the model's general knowledge (`docs/results/stress_test/`).
- **The government side is receptive**: AI Singapore co-launched the persona dataset, and the Social Science
  Research Council funded a five-year programme on computational social simulations for policy design
  (NUS, with NTU, SMU, SUTD). These are natural partners for panel access and for fieldwork.
- **What is missing, and what it costs**: no public panel and no experiments. A commissioned survey of
  2,000 residents with ethnic boosters, 40-60 questions and two embedded experiments, repeated once for
  test-retest, is roughly S$60-120k with a local fieldwork house. That single survey gives Singapore all
  five levels.
- **Caveats found in the persona bank**: the Nemotron-Singapore cards carry no explicit ethnicity, religion
  or income field (they are only implied in narrative text), occupation sometimes contradicts the narrative,
  and our rough check from the narratives suggests Indian residents are under-represented (about 6% vs 9%
  officially) and "Others" missing. These are fixable with re-weighting (`population/synth.py`) and should
  be verified against NVIDIA's extended version.

## 4. Why not China first

- **Access from outside China is the problem, not the data.** CGSS and CFPS are real and overseas
  registrants can apply, but remote access to data held in China is treated as a cross-border transfer
  under the Personal Information Protection Law, and any new validation survey must be run by a licensed
  domestic agency with statistics-bureau approval. Everything in the test plan that needs *new* human
  answers (L4, L5, calibration) therefore needs a Chinese partner.
- **The models are weakest here.** Our blind test on WVS-7 China found a 35-point directional miss on
  attitudes to technocratic rule and group differences reproduced at a quarter of their real size. Every published test (Zuobiao, WVS, Hofstede, CGSS-based) finds that
  Qwen, DeepSeek and GLM answer value questions closer to American than Chinese respondents, and homogenise
  within groups. Mandarin prompting narrows but does not close the gap.
- **Thin cross-national coverage going forward**: China is not in the WVS-8 country list nor in Asian
  Barometer wave 6, so the "same question across countries" tests get harder, not easier.
- **Sensitive topics** limit which attitudes can be surveyed and which models will answer.

Plan: phase 3, with a university or market-research partner in China, after the method is proven in the
US and Singapore. In the meantime, **Taiwan** gives open Mandarin-language microdata (TSCS, Asian
Barometer 6, WVS-8), low friction, and an existing benchmark paper to compare against, so the Mandarin
prompt and model choices can be developed early. Hong Kong (WVS-7) is a second Mandarin/Cantonese option.

## 5. Suggested sequence

| Phase | Months | Deliverable | Gate to pass |
|---|---|---|---|
| 0 | 0-1 | This repository: harness, baselines, data (done) | Baselines reproduced |
| 1 | 1-3 | US gold standard: L1-L4 on GSS, CES, Twin-2K-500 and the experiment set; prompt form and persona layers chosen by ablation; calibration layer built | Beats baselines on L1/L2; L3 normalized >= 0.85; L4 r >= 0.7 |
| 1 (parallel) | 1-3 | Singapore L1/L2 on WVS-7 and GlobalOpinionQA; persona bank re-weighted to DOS 2024 margins; Mandarin/Malay/Tamil prompt variants | Beats other-countries' average on >= 70% of questions |
| 2 | 3-6 | Commissioned Singapore survey (n=2,000, retest, 2 experiments); L3-L5 for Singapore; pre-registered forecast of WVS-8 Singapore or Pew 2026 items | Passes gold-standard marks in two topic areas |
| 3 | 6-12 | Replication kit: country adapter template proven on Taiwan and one of Korea/Japan/UK; China partner secured; city-level cuts (planning areas; US metros) | Adapter stands up a new country in < 4 weeks |
