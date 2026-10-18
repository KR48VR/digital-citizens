---
name: digital-citizens-study
description: Run or extend a digital-citizens study in this repository - estimate how population groups respond to a question using record citizens (AI built on real survey records), score it against real answers with the scorecard, and decide with the scorecard's five-question decision tree. Use when asked to add a country or city, test a new question, run a pilot, rebuild record citizens, or re-score the chatbot kind.
---

# Digital-citizens study

Read `docs/playbook/playbook.md` first; it is the step-by-step method. Key facts:

- **Recipe:** a few hundred real people answer; AI fills in each group's answer (the group's own answers blended
  with an AI estimate, its share fitted leave-one-question-out). Follow the scorecard's decision tree: brand new -
  blend your survey with both kinds of AI (record citizens learned from your survey, and the chatbot), which pays
  off most for groups under about 100 people; asked in other countries - blend with record citizens learned from
  them, no chatbot; asked, worded the same, in the latest round of a large survey in your country - reuse those
  answers; surveying a topic more than once - pilot first. About 20 standard
  questions are enough to link respondents; use the best available chatbot rather than several. Never borrow
  numbers from other surveys or published reports.
- **Environment:** Python in `.venv` (create with `uv venv .venv && uv pip install --python .venv/bin/python -e .`).
  Run scripts with `.venv/bin/python -I`. Raw data in `data/raw/` is git-ignored; fetch with
  `scripts/download_data.py` (GSS, GlobalOpinionQA, Twin-2K, Nemotron) and `scripts/download_wvs.py`
  (World Values Survey via headless Chromium at /opt/pw-browsers/chromium).
- **Code map:** loaders `src/digital_citizens/data/{gss,wvs,ledger}.py`; record citizens
  `evaluate/transfer.py` (`cross_country_transfer`, `small_survey_holdout`); pooling `evaluate/bayes.py`;
  scoring `evaluate/harness.py`; experiments `scripts/*_experiment.py`; tests `tests/` (run `pytest -q`).
- **Scorecard:** one method for every headline number, `scripts/one_method_experiment.py` (small surveys of
  150/300/600 drawn ten times, every method blended the same way, scored against the people not drawn).
  Report median points off and less error than the survey alone, from unrounded values.
  Standout groups (`scripts/standout_split.py`) are a secondary, analysts-only check. Best possible about 1.5 (Singapore) and 1.7 (US).
- **Before claiming anything:** check it in the data (example groups, fieldwork dates, untested capabilities), and check that every
  number on a page comes from the same setup.
- **Reporting:** use the `c-suite-explainer` skill, `docs/playbook/glossary.md` and the page template in
  `docs/playbook/templates/scorecard_page/`. QA with `docs/playbook/qa_checklist.md`.
- **Pages:** scorecard (private; King shares it) https://claude.ai/artifact/1EfjB41MM2Nn69EwY5Ht45 ;
  casebook (private; access on request: method, QA log, King and AI, package) https://claude.ai/artifact/Pqi6H7QszpxTH9KjXi5Lz2 ; index in `docs/playbook/README.md`.

- **Record-reading trial (next; King approved up to $10):** when King says "Run the record-reading trial", use
  `scripts/record_reading_trial.py`. It needs King's API key as a network secret in the environment settings (header
  `x-api-key`, website `api.anthropic.com`, path prefix `/v1/messages/batches`); the script routes its batch calls
  through the proxy so the secret is attached. Never ask for the key in chat, and never set `ANTHROPIC_API_KEY`,
  which Claude Code itself would pick up and `data/raw/wvs` (run `scripts/download_wvs.py` first if it is missing). Run `plan` (no
  API calls), then `run` (one batch to claude-opus-5-5 at low effort; it refuses to send anything if the worst case
  is over $10; most batches finish within an hour), then `score`. Report to King in plain words: did reading each
  person's survey record make the chatbot more accurate than knowing only their demographics, for individuals and
  for groups, next to the 100 people's own answers; say what it cost. It is a 100-person pilot, a signal, not a
  result. Do not change the scorecard until King decides; then log the exchanges in the casebook
  (`docs/playbook/templates/casebook_page/README.md`).

Commit and push to the session's branch after each meaningful change; never commit raw data.
