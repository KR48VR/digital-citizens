---
name: digital-citizens-study
description: Run or extend a digital-citizens study in this repository - estimate how population groups respond to a question using record citizens (AI built on real survey records), score it against real answers with the scorecard, and decide using the five rules. Use when asked to add a country or city, test a new question, run a pilot, rebuild record citizens, or re-score the chatbot kind.
---

# Digital-citizens study

Read `docs/playbook/playbook.md` first; it is the step-by-step method. Key facts:

- **Recipe:** a few hundred real people answer; record citizens fill in each group's answer (group's own answers
  combined with record citizens' estimate, worth fitted leave-one-question-out); the chatbot kind helps less
  and adds nothing on top of record citizens; never borrow numbers from other surveys or published reports.
- **Environment:** Python in `.venv` (create with `uv venv .venv && uv pip install --python .venv/bin/python -e .`).
  Run scripts with `.venv/bin/python -I`. Raw data in `data/raw/` is git-ignored; fetch with
  `scripts/download_data.py` (GSS, GlobalOpinionQA, Twin-2K, Nemotron) and `scripts/download_wvs.py`
  (World Values Survey via headless Chromium at /opt/pw-browsers/chromium).
- **Code map:** loaders `src/digital_citizens/data/{gss,wvs,ledger}.py`; record citizens
  `evaluate/transfer.py` (`cross_country_transfer`, `small_survey_holdout`); pooling `evaluate/bayes.py`;
  scoring `evaluate/harness.py`; experiments `scripts/*_experiment.py`; tests `tests/` (run `pytest -q`).
- **Scorecard:** one method for every headline number, `scripts/one_method_experiment.py` (small surveys of
  150/300/600 drawn ten times, every method combined the same way, scored against the people not drawn).
  Report points off for a typical group and less error than the survey alone, from unrounded values.
  Standout groups (`scripts/standout_split.py`) are a secondary, analysts-only check. Noise floor about 1.3.
- **Before claiming anything:** check it in the data (example groups, fieldwork dates, untested capabilities), and check that every
  number on a page comes from the same setup.
- **Reporting:** use the `c-suite-explainer` skill, `docs/playbook/glossary.md` and the page template in
  `docs/playbook/templates/scorecard_page/`. QA with `docs/playbook/qa_checklist.md`.
- **Pages:** public-facing scorecard https://claude.ai/artifact/1EfjB41MM2Nn69EwY5Ht45 ;
  private casebook (method, QA log, King and AI, package) https://claude.ai/artifact/Pqi6H7QszpxTH9KjXi5Lz2 ; index in `docs/playbook/README.md`.

Commit and push to the session's branch after each meaningful change; never commit raw data.
