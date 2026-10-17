# What the research says about AI "digital citizens" (as of October 2026)

**Plain-language summary.** Large language models (LLMs) can imitate how *groups* of people answer
survey questions reasonably well, but they are unreliable at imitating *individuals*, they tend to
make everyone inside a group sound the same, they are too confident, and they know Western (especially
American) opinion far better than Asian opinion. Nobody, including the best commercial vendors, has
shown a simulated population that can replace a real survey for important decisions. What has been
shown is that a simulation *plus a small real-human check* can be useful and much cheaper than a full
survey. Everything we build should be designed around that fact.

## 1. The main findings, in order of importance for this project

1. **Group averages: moderate accuracy, unpredictable misses.** The most rigorous recent test is Pew
   Research Center's September 2026 study: they built "digital twins" of their own panelists (using each
   person's demographics and past answers) with Claude Opus 4.6 and other models and re-ran three real
   surveys of about 300 questions. The twins were off by an average of 12.4 percentage points per answer
   option; on 28% of questions the error exceeded 15 points. Errors were bigger for Republicans and Black
   adults, the twins picked "not sure" four times less often than real people, and on nearly half the
   questions some answer option was never chosen by any twin. Pew's conclusion: "not an adequate
   replacement for traditional polling". [Pew 2026](https://www.pewresearch.org/data-labs/2026/09/30/can-ai-stand-in-for-human-survey-takers-not-really/)

2. **Individuals: close to no signal.** The Columbia "Twin-2K-500" team built twins of 2,058 Americans from
   500+ of their own answers and tested them on 19 new studies: the twin-to-human correlation at the
   individual level averaged about 0.2, barely better than a generic model with no personal information
   ([Peng et al. 2025/26](https://arxiv.org/abs/2509.19088)). A 74-country study found simulated answers
   explained about 1% of the variation between individuals and about 4% between countries
   ([Chen et al. 2026, Nature Human Behaviour](https://www.nature.com/articles/s41562-026-02611-4)).
   The one strong positive result, Stanford's interview-based agents (85% of people's own test-retest
   accuracy; [Park et al. 2024](https://arxiv.org/abs/2411.10109)), needed a two-hour interview per person
   and the agents are not public.

3. **"Regression to the mean" is real, and so is its opposite.** Simulated respondents are less varied than
   real people: in the first careful study, the spread of answers was about half the real spread (standard
   deviation 16 vs 31; [Bisbee et al. 2024](https://doi.org/10.1017/pan.2024.5)), and twins "flatten"
   the differences inside identity groups ([Wang, Morgenstern & Dickerson 2025](https://arxiv.org/abs/2402.01908)).
   But models also *caricature*: when told a persona's demographics they exaggerate differences between
   groups by 2 to 4 times and sometimes aim at the wrong group entirely
   ([Chen, Zhu & Zheng 2026](https://arxiv.org/abs/2607.26348); [Cheng et al. 2023](https://arxiv.org/abs/2310.11501)).
   So we must measure spread in both directions, not just "is the average right".

4. **Asking for the group's answer distribution beats role-playing many personas.** Several 2025-26 papers
   find that one prompt asking "what share of this group would pick each option" is more accurate and
   5 times cheaper than sampling hundreds of individual personas, which collapse toward a few answers
   ([Gong, Sanders & Schneier 2026](https://arxiv.org/abs/2603.20229);
   [Meister, Guestrin & Hashimoto](https://arxiv.org/abs/2411.05403); [Ozkan 2026](https://arxiv.org/abs/2607.18310)).
   Individual role-play only pays off when you have rich real records per person.

5. **The fix that works is a small real-human sample used to correct the simulation.** "Rectification"
   with a few hundred real answers cut simulation bias from 24-86% to under 5% and increased effective
   sample size ([Krsteski et al. 2026](https://arxiv.org/abs/2510.11408); see also
   [Tigre & Souto 2026](https://arxiv.org/abs/2609.13148) and prediction-powered inference
   [Wang et al. 2026](https://arxiv.org/abs/2609.07987)). Temperature tweaks and "be diverse" instructions
   do almost nothing ([Ziaei 2026](https://arxiv.org/abs/2609.25760)). Fine-tuning on survey data improves
   distributions (up to 46% lower error; [SubPOP, Suh et al. 2025](https://arxiv.org/abs/2502.16761)) but
   can erase cross-cultural differences if done naively.

6. **Western bias is large and matters for Asia.** Models' default opinions sit closest to US, Canadian
   and European respondents ([Durmus et al. 2023, Anthropic](https://arxiv.org/abs/2306.16388)); agreement
   with real answers drops from kappa 0.24 (US) to 0.02 (Japan) in one WVS study
   ([Qu & Wang 2024](https://doi.org/10.1057/s41599-024-03609-x)). Chinese-built models (Qwen, DeepSeek)
   answer value questions "more like Americans than Chinese" ([arXiv 2512.13723](https://arxiv.org/abs/2512.13723)),
   and the one Taiwan (Mandarin) benchmark found zero-shot LLMs at ~52% accuracy versus 58% for a plain
   supervised model trained on the same survey ([Ku et al. 2026](https://arxiv.org/abs/2607.03091)).
   No published benchmark tests LLMs on Singaporean opinion specifically. That is a gap we can fill.

7. **Simple baselines are hard to beat.** The average of neighbouring countries beat every LLM at predicting
   a country's mean answers in the European Social Survey ([Wang 2026](https://arxiv.org/abs/2609.16395)).
   Our own runs (see `docs/results/`) show the same thing: last wave's answers predict this wave within
   about 3 points, and a nearest-neighbour rule reaches 79% of the human test-retest ceiling on Twin-2K-500
   with no AI at all. A digital citizen that cannot beat these is not worth paying for.

8. **Other reproducible failure modes we will test for.** Answer-order and wording artefacts unlike humans'
   ([Dominguez-Olmedo et al. 2024](https://arxiv.org/abs/2306.07951); [Tjuatja et al. 2024](https://aclanthology.org/2024.tacl-1.56/));
   "hyper-accuracy" on knowledge questions (98% correct vs 52% of real adults in Pew's test);
   instability across model versions ([Bisbee et al. 2024](https://doi.org/10.1017/pan.2024.5));
   persona prompting sometimes making results worse ([Hu & Collier 2024](https://aclanthology.org/2024.acl-long.554/)).

## 2. What this means for what we build

- The product is **a measured simulator**, not a promise of accuracy: every answer it gives should come
  with the error observed on comparable real questions.
- Build at the **group level first** (segments, cities, countries), using distribution prompts; add
  individual-level twins only where we have rich real records and a panel to test against.
- Always keep a **real-human calibration sample** in the loop for every new country and topic area; use it
  to correct the simulation, not just to grade it.
- Treat **variance** (how much people differ) as a first-class output and test it in both directions.
- Expect to need **country-specific models, prompts and languages** for Singapore and China, and expect
  the first results there to be worse than in the US.

## 3. Key sources (verified links)

| Work | What it is | Why it matters here |
|---|---|---|
| [Argyle et al. 2023](https://doi.org/10.1017/pan.2023.2) | "Silicon samples" with GPT-3 and ANES | Origin of the idea; defines "algorithmic fidelity" |
| [Santurkar et al. 2023 (OpinionQA)](https://arxiv.org/abs/2303.17548) | 1,498 Pew questions, 60 US groups | Standard US subgroup benchmark and metrics |
| [Durmus et al. 2023 (GlobalOpinionQA)](https://arxiv.org/abs/2306.16388) | WVS + Pew Global, 100+ countries | Cross-country benchmark we use (US, China, Singapore) |
| [Bisbee et al. 2024](https://doi.org/10.1017/pan.2024.5) | ANES feeling thermometers | Documented variance collapse and version drift |
| [Park et al. 2024](https://arxiv.org/abs/2411.10109) | 1,052 interview-based agents | Best individual-level result; interviews beat demographics |
| [Ashokkumar, Hewitt et al. 2026, Nature](https://doi.org/10.1038/s41586-026-10742-x) | 70 US experiments | Treatment effects predicted with r = 0.85 |
| [Toubia et al. 2025 (Twin-2K-500)](https://arxiv.org/abs/2505.17479) | 2,058 US panelists, retest wave | Open individual-level testbed we use |
| [Peng et al. 2025/26 "Funhouse mirrors"](https://arxiv.org/abs/2509.19088) | 19 studies on Twin-2K-500 | Twin-human r = 0.20; five named distortions |
| [Pew Research 2026](https://www.pewresearch.org/data-labs/2026/09/30/can-ai-stand-in-for-human-survey-takers-not-really/) | Pew's own twins, 3 waves | 12.4-point average error; the current state of the art |
| [Hu et al. 2026 (SimBench, ICLR)](https://arxiv.org/abs/2510.17516) | 20 datasets, 130+ countries | Best model scores 40.8/100; instruction tuning hurts diverse items |
| [Gong, Sanders & Schneier 2026](https://arxiv.org/abs/2603.20229) | CES, distribution vs persona prompts | Distribution prompting wins on 77% of cells |
| [Krsteski et al. 2026](https://arxiv.org/abs/2510.11408) | Rectification with human samples | The remedy that works |
| [Chen et al. 2026, Nature Human Behaviour](https://www.nature.com/articles/s41562-026-02611-4) | 74 countries | ~1% individual, ~4% country variance explained |
| [Ku et al. 2026](https://arxiv.org/abs/2607.03091) | Taiwan election survey, Mandarin | Mandarin zero-shot below supervised baseline |
| [Suh et al. 2025 (SubPOP)](https://arxiv.org/abs/2502.16761) | Fine-tuning on Pew/GSS | Fine-tuning cuts distribution error up to 46% |
| [Binz et al. 2025 (Centaur), Nature](https://www.nature.com/articles/s41586-025-09215-4) | 10M human choices | Fine-tuned "human behaviour" foundation model |

A longer list, including vendors' self-published claims (Aaru, Artificial Societies, Evidenza, Simile and
others, none independently peer-reviewed), is in the research notes that produced this brief.
