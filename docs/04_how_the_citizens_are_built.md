# How the digital citizens are built

## 1. The idea in one picture

```
 official statistics      real survey respondents        LLM
 (census margins)         (GSS, WVS, CGSS, panels)        |
        |                         |                       |
        v                         v                       v
 [persona skeleton] ---> [anchor each persona to a   ---> [response engine:
  demographics,           real respondent's record]        role-play one person, or
  location, weights       values, trust, media,            predict a group's shares]
                          consumption, politics                 |
                                                                v
                                          [calibration layer: correct bias with a
                                           small real-human sample; re-weight to census]
                                                                |
                                                                v
                                    [validation harness: score vs real people at 5 levels]
```

Every digital citizen is therefore three things: a **demographic skeleton** that matches the census,
a **real respondent's answers** it is anchored to (so it has a personality that came from a person, not
from the model's imagination), and an **LLM response engine** whose output is corrected and scored.

## 2. The layers, and why each exists

| Layer | What it is | Source today | Why |
|---|---|---|---|
| 0. Population skeleton | Joint distribution of age, sex, ethnicity, education, income, location | US: ACS/Census via Nemotron-Personas-USA or PUMS; Singapore: Nemotron-Personas-Singapore re-weighted to DOS 2024 tables (`population/synth.py`) | Without it, the model's own idea of "a Singaporean" is biased toward young, educated, urban |
| 1. Real-respondent anchor | A real (anonymous) survey respondent's answers to 50-200 items | US: GSS 2024 respondents (`data/gss.py`); Singapore: WVS-7 respondents (download by form); China: CGSS | Research shows real records carry the individual signal that demographics alone cannot |
| 2. Narrative (optional) | Short life description | Nemotron persona text, or an LLM summary of the record | Adds realism; but can add stereotype, so it is switchable and ablated (`--persona-style`) |
| 3. Response engine | The LLM answering as the persona, or predicting a group's shares | Anthropic models by default (`simulate/llm.py`); country-specific models (Qwen, DeepSeek, SEA-LION) pluggable via the same interface | Two modes because the evidence says distribution prompts are usually better and cheaper, but role-play is needed for individual-level and for free-text reactions |
| 4. Calibration | Correct systematic bias and re-weight | `evaluate/calibrate.py` (human level + simulated differences; gap scaling; power); raking to census margins (`population/synth.py`) | The only remedy with strong evidence; tested in `docs/06_how_to_make_it_work.md` |
| 5. Validation | Score vs real people | `evaluate/` | See `docs/02_how_we_measure_accuracy.md` |

## 3. What is in this repository now (v0)

- `src/digital_citizens/schema.py`: the data types (Persona, Question, Distribution, Response).
- `data/`: loaders that turn real data into benchmarks:
  GSS 2022/2024 with exact codebook wording for 84 attitude items and 10 segment types;
  GlobalOpinionQA (WVS + Pew) for 100+ countries including the US, China and Singapore;
  Twin-2K-500 for individual-level tests; WVS wave 7 microdata for Singapore, China and the US (77 items,
  segments by ethnicity, religion, age, education, income, urban/rural; `scripts/download_wvs.py` fetches
  the files with the container browser); Nemotron-Personas-Singapore as a persona skeleton.
- `population/synth.py`: iterative proportional fitting and raking to make a persona bank match census
  margins, plus sampling a synthetic population of any size.
- `simulate/`: prompt builders for both response modes, option shuffling to detect order effects, answer
  parsers, a cached Anthropic client, and a deterministic mock so the whole pipeline runs without an API key.
- `evaluate/`: the metrics, the free baselines (uniform, "everyone is average", last wave, demographic
  regression, other-countries' average, modal, demographic-cell, k-NN), the scoring harness, and the
  individual-level protocol for Twin-2K-500.
- `cli.py`: `dc baselines gss|goqa|twin2k|wvs`, `dc personas singapore`, `dc simulate gss|goqa [--mock]`,
  and the blind-test workflow `dc packet` (export questions without answers) / `dc score-packet`.
- `tests/`: 19 tests (metrics, raking, prompts, mock end-to-end, loader smoke tests on the real files).
- `docs/results/`: the baseline reports produced on the real data.

Not yet built (phase 1): the calibration/rectification layer; the effects (L4) runner for experiments
and pricing; fine-tuning; a CGSS loader (needs registration);
Mandarin/Malay/Tamil prompt variants; cost tracking; a results dashboard.

## 4. Running it

```
uv venv .venv && uv pip install --python .venv/bin/python -e .
.venv/bin/python -I scripts/download_data.py          # GSS, GlobalOpinionQA, Twin-2K-500, Nemotron SG
.venv/bin/python -I -m pytest -q
.venv/bin/python -I -m digital_citizens.cli baselines gss
.venv/bin/python -I -m digital_citizens.cli baselines goqa
.venv/bin/python -I -m digital_citizens.cli baselines twin2k
.venv/bin/python -I -m digital_citizens.cli simulate gss --mock --limit 5          # dry run, no key
ANTHROPIC_API_KEY=... .venv/bin/python -I -m digital_citizens.cli simulate gss --mode distribution --limit 20
ANTHROPIC_API_KEY=... .venv/bin/python -I -m digital_citizens.cli simulate gss --mode roleplay --personas 300 --limit 10
```

Every model call is cached on disk under `data/cache/llm/` keyed by model, prompt and settings, so
re-scoring is free and results are reproducible.

## 5. Rough cost of a first real run (for budgeting)

- Distribution mode, GSS: 84 questions x 60 segment cells x 3 repeats = about 15,000 short calls.
- Role-play mode, GSS: 300 personas x 84 questions = about 25,000 calls with ~1,500-token prompts.
- GlobalOpinionQA, three countries: about 1,800 questions x 3 countries x 3 repeats = about 16,000 calls.
At current list prices for a mid-size model this is tens of dollars per full pass, not thousands; the
expensive part of the programme is human fieldwork for calibration, not model calls.
