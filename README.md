# Digital Citizens

Census-grounded, survey-anchored AI personas that simulate how populations and segments respond to
products, strategies and policies, **together with the harness that measures how wrong they are**.

Status (October 2026): v0. The measurement machinery runs end to end on real human data for the United
States, Singapore and China; the model-driven simulation runs with a mock and is ready for an API key.
A first in-session stress test (the model writing answer shares blind, then scored) is in `docs/results/stress_test/`.

## The result in one line

AI cannot replace asking real people, but it can stretch a small survey a long way. A few hundred real
people answer your question. AI then fills in each group's answer, about as accurately as a survey twice
the size.

The AI that stretches a small survey best is the kind that learns from patterns in real people's past
survey answers. We call the digital citizens built this way record citizens.

The gain is biggest for small groups.

The more common use of AI, a chatbot answering in place of people, also helps. For a brand-new question,
combining it with record citizens worked best. We call this the chatbot kind.

Which AI to add depends on whether your question has been asked before: brand new (most product and policy
questions) - record citizens learned from your own survey plus the chatbot kind; asked in large surveys in
other countries - record citizens learned from those countries, no chatbot needed; asked recently in the
same large survey - reuse those answers.

All of this comes from one test (`scripts/one_method_experiment.py`, write-up in docs/09): small surveys of
150, 300 and 600 people drawn ten times from a large real survey, each group's answer worked out the same way
with and without each kind of AI, and checked against the people not drawn.

| Points off for a typical group, survey of 300 | Singapore | United States |
|---|---|---|
| Survey alone | 3.7 | 4.9 |
| Brand-new question: + chatbot kind | 3.2 | 3.4 |
| Brand-new question: + record citizens learned from your survey | 2.9 | 3.5 |
| Brand-new question: + both | 2.7 | 2.9 |
| Asked in other countries: + record citizens learned from them | 2.7 | not tested |
| Asked two years earlier in the same survey: + those answers | not tested | 2.4 |
| For comparison: survey of 600 alone | 2.7 | 3.7 |

Separate checks: borrowing the most similar question from a different survey was typically 11 points off,
and published findings 8 points off; neither helped.

"Points off" is the gap between our estimate and what real people said, in percentage points, for a typical
group (half of all group answers land closer); survey noise alone gives about 1.3, guessing blind about 15.
Each record citizen is a real, anonymous survey respondent whose own past answers predict their answer to a
new question. The chatbot kind guesses from a description of a person. The plain-language scorecard with charts is
at https://claude.ai/artifact/1EfjB41MM2Nn69EwY5Ht45 (private; share from the page). How it was made, the QA log
and a playbook for next time are in the private casebook at https://claude.ai/artifact/Pqi6H7QszpxTH9KjXi5Lz2 and in [docs/playbook/](docs/playbook/README.md).

## Read first

| Document | What it answers |
|---|---|
| [docs/01_what_the_evidence_says.md](docs/01_what_the_evidence_says.md) | What research (to Oct 2026) shows about LLM-simulated respondents, and when they fail |
| [docs/02_how_we_measure_accuracy.md](docs/02_how_we_measure_accuracy.md) | The five-level test plan, the free baselines to beat, ceilings, pass marks, anti-leakage rules |
| [docs/03_where_to_start.md](docs/03_where_to_start.md) | US vs China vs Singapore (and Taiwan, Korea, Japan, UK): recommendation and phased plan |
| [docs/04_how_the_citizens_are_built.md](docs/04_how_the_citizens_are_built.md) | Architecture, what is in the code, how to run it, rough costs |
| [docs/05_open_questions.md](docs/05_open_questions.md) | Decisions needed from you |
| [docs/06_how_to_make_it_work.md](docs/06_how_to_make_it_work.md) | Remedies for regression-to-the-mean, tested on real data, and the build plan that follows |
| [docs/07_more_data_and_bayesian_pooling.md](docs/07_more_data_and_bayesian_pooling.md) | Combing more public surveys (61 WVS countries, CES, 96 published Singapore findings) and pooling sources the Bayesian way: what it bought |
| [docs/08_library_test.md](docs/08_library_test.md) | The 'library' idea tested end to end on the US: search for the closest previously asked question, use that survey as the base, spread with record citizens |
| [docs/09_one_method.md](docs/09_one_method.md) | The one test behind every headline number: a small survey with and without each kind of AI |
| [docs/sources/singapore_published_findings.md](docs/sources/singapore_published_findings.md) | Singapore sources combed for the evidence ledger, with trust levels and what was unusable |
| [docs/results/](docs/results/README.md) | Baseline numbers measured on the real data |
| [docs/results/stress_test/](docs/results/stress_test/README.md) | First stress test: the session's own model vs real shares in the US, Singapore and China |
| [docs/results/library_test/](docs/results/library_test/library_test_us.md) | Library test numbers: 31 WVS questions answered from the GSS library, with and without record spread |

## Quick start

```
uv venv .venv && uv pip install --python .venv/bin/python -e .
.venv/bin/python -I scripts/download_data.py     # ~190 MB: GSS 2022/2024, GlobalOpinionQA, Twin-2K-500, Nemotron-Personas-Singapore
.venv/bin/python -I -m pytest -q                  # 31 tests
.venv/bin/python -I -m digital_citizens.cli baselines gss
.venv/bin/python -I -m digital_citizens.cli baselines goqa
.venv/bin/python -I -m digital_citizens.cli baselines twin2k
.venv/bin/python scripts/download_wvs.py data/raw/wvs      # WVS wave 7 Singapore/China/US via headless browser
.venv/bin/python -I -m digital_citizens.cli baselines wvs --countries Singapore
.venv/bin/python -I -m digital_citizens.cli personas singapore
.venv/bin/python -I -m digital_citizens.cli simulate gss --mock --limit 5                 # dry run
ANTHROPIC_API_KEY=... .venv/bin/python -I -m digital_citizens.cli simulate gss --mode distribution --limit 20
```

## Layout

```
src/digital_citizens/
  schema.py            Persona, Question, Distribution, Response
  data/                gss.py (US GSS 2022/2024), wvs.py (WVS-7, any of 62 countries), ledger.py (published findings as priors),
                       globalopinionqa.py (WVS+Pew, 100+ countries),
                       twin2k.py (US panel with retest), nemotron.py (Singapore persona skeleton), benchmark.py
  population/synth.py  IPF / raking to census margins; synthetic population sampling
  simulate/            prompts.py (role-play + distribution modes), llm.py (Anthropic client, cache, mock), runner.py
  evaluate/            metrics.py, baselines.py, harness.py, individual.py, calibrate.py (human-level + model-difference
                       corrections), transfer.py (record-anchored citizens without an LLM), bayes.py (weighted-source pooling)
  library/             crosswalk_us.py (WVS<->GSS question pairs on common bins), harmonise.py (common segments, bins,
                       re-levelling), search.py (closest-question search: word overlap or local sentence embeddings)
  cli.py               dc baselines | personas | simulate
scripts/                 download_data.py, download_wvs.py, *_experiment.py (each writes a report under docs/results/)
tests/
docs/
data/raw, data/cache   (git-ignored)
```

## Data and licences

GSS (NORC, public use), WVS wave 7 (WVS Association terms: research use, cite, do not redistribute; fetched
by `scripts/download_wvs.py`), GlobalOpinionQA (Anthropic, CC BY-NC-SA 4.0: validation only, not commercial
training), Twin-2K-500 (CC BY 4.0), Nemotron-Personas (NVIDIA, CC BY 4.0). CGSS, CFPS, Pew ATP and ANES
microdata need a registration or account and are not downloaded automatically.
