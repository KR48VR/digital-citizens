# Digital Citizens

Census-grounded, survey-anchored AI personas that simulate how populations and segments respond to
products, strategies and policies, **together with the harness that measures how wrong they are**.

Status (October 2026): v0. The measurement machinery runs end to end on real human data for the United
States, Singapore and China; the model-driven simulation runs with a mock and is ready for an API key.
A first in-session stress test (the model writing answer shares blind, then scored) is in `docs/results/stress_test/`.

## Read first

| Document | What it answers |
|---|---|
| [docs/01_what_the_evidence_says.md](docs/01_what_the_evidence_says.md) | What research (to Oct 2026) shows about LLM-simulated respondents, and when they fail |
| [docs/02_how_we_measure_accuracy.md](docs/02_how_we_measure_accuracy.md) | The five-level test plan, the free baselines to beat, ceilings, pass marks, anti-leakage rules |
| [docs/03_where_to_start.md](docs/03_where_to_start.md) | US vs China vs Singapore (and Taiwan, Korea, Japan, UK): recommendation and phased plan |
| [docs/04_how_the_citizens_are_built.md](docs/04_how_the_citizens_are_built.md) | Architecture, what is in the code, how to run it, rough costs |
| [docs/05_open_questions.md](docs/05_open_questions.md) | Decisions needed from you |
| [docs/results/](docs/results/README.md) | Baseline numbers measured on the real data |
| [docs/results/stress_test/](docs/results/stress_test/README.md) | First stress test: the session's own model vs real shares in the US, Singapore and China |

## Quick start

```
uv venv .venv && uv pip install --python .venv/bin/python -e .
.venv/bin/python -I scripts/download_data.py     # ~190 MB: GSS 2022/2024, GlobalOpinionQA, Twin-2K-500, Nemotron-Personas-Singapore
.venv/bin/python -I -m pytest -q                  # 18 tests
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
  data/                gss.py (US GSS 2022/2024), wvs.py (WVS-7 Singapore/China/US microdata), globalopinionqa.py (WVS+Pew, 100+ countries),
                       twin2k.py (US panel with retest), nemotron.py (Singapore persona skeleton), benchmark.py
  population/synth.py  IPF / raking to census margins; synthetic population sampling
  simulate/            prompts.py (role-play + distribution modes), llm.py (Anthropic client, cache, mock), runner.py
  evaluate/            metrics.py, baselines.py, harness.py, individual.py
  cli.py               dc baselines | personas | simulate
scripts/download_data.py
tests/
docs/
data/raw, data/cache   (git-ignored)
```

## Data and licences

GSS (NORC, public use), WVS wave 7 (WVS Association terms: research use, cite, do not redistribute; fetched
by `scripts/download_wvs.py`), GlobalOpinionQA (Anthropic, CC BY-NC-SA 4.0: validation only, not commercial
training), Twin-2K-500 (CC BY 4.0), Nemotron-Personas (NVIDIA, CC BY 4.0). CGSS, CFPS, Pew ATP and ANES
microdata need a registration or account and are not downloaded automatically.
