# Playbook: running a digital-citizens study

How to answer "how would these groups respond to X?" with AI, so that it works instead of flattening groups.
Written from the October 2026 project (United States, Singapore, China). Plain-language findings:
the scorecard page. Method detail: docs/06, docs/07, docs/08 and docs/results/.

## The recipe in one line

Real people give the overall answer. Record citizens (AI built on real people's past survey answers) fill in
the groups. The chatbot kind (a chatbot answering in character) only fills in groups well in the United States.
Never borrow numbers from other surveys, polls or the news. Always show the scorecard.

## Step 1. Frame the question

- Write the exact question wording and answer options you will field.
- List the groups the decision turns on (age, ethnicity, religion, education, region, income, party).
  Note which are **small groups** (few people in a survey) and which are likely **standout groups**
  (answer very differently from the average). Do not assume: check standout groups in the data (step 3).
- Decide the country and, if needed, the city or region.

## Step 2. Find rich public records

- You need surveys that publish **every person's answers to many questions**, not headlines.
  Good: World Values Survey (all countries, `scripts/download_wvs.py`), US General Social Survey
  (`scripts/download_data.py`), Asian Barometer, national social surveys, Cooperative Election Study.
  Useless as records: news stories, press releases, opt-in online polls.
- Record the **fieldwork dates** and mode (face-to-face, online). Records describe people as they were then.
  Example: Singapore's World Values Survey ran November 2019 to March 2020, as COVID was arriving.
- Check licences: WVS is research use with citation; do not redistribute raw files.

## Step 3. Build record citizens

- Load respondents and groups: `src/digital_citizens/data/wvs.py` or `gss.py` (`load_respondents`, `benchmark`).
- Two ways to learn the pattern from past answers to the new question:
  1. **From other countries** where the same question was asked:
     `evaluate/transfer.py::cross_country_transfer` (61 countries, about 90,000 people, under half an hour).
  2. **From your own small survey** when the question is new: `evaluate/transfer.py::small_survey_holdout`.
     Your survey must include a set of the big survey's **standard questions**, so your respondents link to the records.
- Optional: weigh the chatbot kind and record citizens by track record: `evaluate/bayes.py` (pooling).
  Record citizens earned about three times the weight of the chatbot in Singapore.

## Step 4. Measure with the scorecard

- **Points off**: gap between estimate and real answer, percentage points per answer option, per group.
  - "Most groups" = middle result (median over group-by-question cells).
  - "Including standout groups" = average (mean), which standout misses push up.
- **No AI** = the real overall answer given to every group. Always report against it.
- **Less error** = (No AI points off − method points off) / No AI points off.
- Noise floor: about 1.4 points (two surveys of the same people differ this much by chance).
  Reading guide: 1.4 as close as any survey can get, about 3 good enough to act on, 5 rough level only,
  16 guessing blind.
- Group differences reproduced (gap slope) shows flattening: chatbot kind 81% US, 36% Singapore, 25% China.
- Harness: `evaluate/harness.py` (`score`, `segment_fidelity`); scripts in `scripts/*_experiment.py`.

**Scoring rules learned the hard way**
- Score a small sample against the people **not** in it, and average scores across draws, not predictions.
  (Averaging predictions first made a 300-person survey look like 1,500 and was corrected on 17 Oct 2026.)
- Never claim a capability that was not tested (the chatbot "drafting questions" claim was removed).
- Check example groups in the data before naming them (people over 60 were not a standout group in Singapore).

## Step 5. Pilot before relying on it

Run one pilot with 600 people on your real question plus the standard questions. Let record citizens fill
in the groups from 300 of them and compare with what all 600 said. If they agree, later surveys can use 300.
In our tests, 300 real people + record citizens were about as accurate for each group as 600 without AI
(about 3 points off).

## Step 6. Decide with the five rules

1. Use AI as record citizens, to stretch a smaller real survey (smaller or more frequent surveys).
2. Record citizens help most with small groups and standout groups.
3. Chatbots are much less useful, except in the United States.
4. Don't borrow numbers from other surveys, polls or the news (11, 8 and 19 points off).
5. Insist on the scorecard, group by group, against real answers.

## Step 7. Report for a C-suite reader

Use the `c-suite-explainer` skill and `glossary.md`. Page order that worked:
short answer → two ways to build a digital citizen, shown with one person → what it is worth →
how we measure accuracy → where AI helps most (small groups, standout groups, why the chatbot works
only in the US) → five rules → limits and areas for further experimentation → full evidence folded away.
Template: `templates/scorecard_page/`.

## Step 8. QA before sharing

Run `qa_checklist.md`: trace every number, check contrast and headings, phone width, dark mode, language.
Log findings and fixes.
