# Digital Citizens

Census-grounded, survey-anchored AI personas that simulate how populations and segments respond to
products, strategies and policies, **together with the harness that measures how wrong they are**.

Status (October 2026): v0. The measurement machinery runs end to end on real human data for the United
States, Singapore and China; the model-driven simulation runs with a mock and is ready for an API key.
A first in-session stress test (the model writing answer shares blind, then scored) is in `docs/results/stress_test/`.

## The result in one line

AI cannot replace asking real people, but it can stretch a small survey a long way. A few hundred real
people give the overall answer. AI then works out how each group differs, as accurately as a survey twice
the size. The AI that does this well learns from real people's past survey answers. A chatbot asked to play
people does it well only in the United States.

| The story, in order | How far off (typical group) | Do groups still look different? | Verdict |
|---|---|---|---|
| 1. AI alone (a chatbot pretends to be people from each group) | 5 points | No, groups come out nearly alike | Drop |
| 2. Citizens built from real people's past survey answers (no chatbot) | under 4 points | Yes, mostly | Keep |
| 3. Borrow the numbers from a similar question in a different survey | 11 points | Partly, but the overall number is far off | Drop |
| 4. Ask 300 real people, let the record citizens fill in the groups | 3 points | Yes | Keep: this is the plan |
| The best it can ever be (exact national number, then fill in) | 2 points | Yes | Only chance is left |

"How far off" is the gap between our estimate and the real survey, in percentage points, for a typical group;
survey noise alone gives about 1.4, guessing blind about 16. The "AI" that works starts from real people: each
record citizen is a real, anonymous survey respondent whose own past answers predict their answer to a new
question. The chatbot kind, which guesses from a description of a person, is the part that flattens groups. The plain-language scorecard with charts is
at https://claude.ai/artifact/1EfjB41MM2Nn69EwY5Ht45 (private; share from the page).

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
