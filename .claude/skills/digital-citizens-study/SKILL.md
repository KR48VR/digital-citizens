---
name: digital-citizens-study
description: Run or extend a digital-citizens study in this repository - estimate how population groups respond to a question using record citizens (AI built on real survey records), score it against real answers with the scorecard, and decide using the five rules. Use when asked to add a country or city, test a new question, run a pilot, rebuild record citizens, or re-score the chatbot kind.
---

# Digital-citizens study

Read `docs/playbook/playbook.md` first; it is the step-by-step method. Key facts:

- **Recipe:** real people give the overall answer; record citizens fill in the groups; the chatbot kind fills
  in groups well in the United States, but in Singapore helped only standout groups; never borrow numbers from
  other surveys or published reports.
- **Environment:** Python in `.venv` (create with `uv venv .venv && uv pip install --python .venv/bin/python -e .`).
  Run scripts with `.venv/bin/python -I`. Raw data in `data/raw/` is git-ignored; fetch with
  `scripts/download_data.py` (GSS, GlobalOpinionQA, Twin-2K, Nemotron) and `scripts/download_wvs.py`
  (World Values Survey via headless Chromium at /opt/pw-browsers/chromium).
- **Code map:** loaders `src/digital_citizens/data/{gss,wvs,ledger}.py`; record citizens
  `evaluate/transfer.py` (`cross_country_transfer`, `small_survey_holdout`); pooling `evaluate/bayes.py`;
  scoring `evaluate/harness.py`; experiments `scripts/*_experiment.py`; tests `tests/` (run `pytest -q`).
- **Scorecard:** points off per group, reported separately for most groups and standout groups (the quarter of
  group answers furthest from the national average; `scripts/standout_split.py`), less error versus No AI from
  unrounded values, noise floor about 1.3. Score small samples against hold-out people and average scores
  across draws.
- **Before claiming anything:** check it in the data (standout groups, fieldwork dates, untested capabilities).
- **Reporting:** use the `c-suite-explainer` skill, `docs/playbook/glossary.md` and the page template in
  `docs/playbook/templates/scorecard_page/`. QA with `docs/playbook/qa_checklist.md`.
- **Pages:** public-facing scorecard https://claude.ai/artifact/1EfjB41MM2Nn69EwY5Ht45 ;
  private casebook (method, QA log, King and AI, package) https://claude.ai/artifact/Pqi6H7QszpxTH9KjXi5Lz2 ; index in `docs/playbook/README.md`.

Commit and push to the session's branch after each meaningful change; never commit raw data.
