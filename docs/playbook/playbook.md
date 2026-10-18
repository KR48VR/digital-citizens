# Playbook: running a digital-citizens study

How to answer "how would these groups respond to X?" with AI, so that it works instead of flattening groups.
Written from the October 2026 project (United States, Singapore, China). Plain-language findings:
the scorecard page. Method detail: docs/09 (the one-method test behind every headline number), docs/06-08
and docs/results/.

## The recipe in one line

A few hundred real people answer the question. AI fills in each group's answer: the group's own answers are
combined with an AI estimate, and the fewer people a group has, the more the estimate counts. Which AI depends on
whether the question has been asked before. Brand new: record citizens learned from your own survey plus the
chatbot kind. Asked in large surveys in other countries: record citizens learned from them, no chatbot. Asked
recently in the same large survey: reuse those answers. Never borrow numbers from other surveys or published
reports. Always show the scorecard, against the survey alone.

## Step 1. Frame the question

- Write the exact question wording and answer options you will field.
- List the groups the decision turns on (age, ethnicity, religion, education, region, income, party).
  Note which are **small groups**: in a 150-person survey in Singapore, about 14 Indian and 17 Malay
  Singaporeans. These are where AI adds most.
- Decide the country and, if needed, the city or region.

## Step 2. Find rich public records

- You need surveys that publish **every person's answers to many questions**, not headlines.
  Good: World Values Survey (all countries, `scripts/download_wvs.py`), US General Social Survey
  (`scripts/download_data.py`), Asian Barometer, national social surveys, Cooperative Election Study.
  Not usable as records: news stories, press releases and published reports (they give group results,
  not each person's answers).
- Record the **fieldwork dates** and mode (face-to-face, online). Records describe people as they were then.
  Example: Singapore's World Values Survey ran November 2019 to March 2020, as COVID was arriving.
- Check licences: WVS is research use with citation; do not redistribute raw files.

## Step 3. Build record citizens

- Load respondents and groups: `src/digital_citizens/data/wvs.py` or `gss.py` (`load_respondents`, `benchmark`).
- Two ways to learn the pattern from past answers to the new question:
  1. **From past surveys** where the same question was asked (other countries, or an earlier round):
     `evaluate/transfer.py::cross_country_transfer` (61 countries, about 90,000 people, under half an hour).
  2. **From your own small survey** when the question is new: the model is trained on your respondents
     (see `scripts/one_method_experiment.py::draw_cells`). Your survey must include a set of the big survey's
     **standard questions** so your respondents link to the records. About 20 are enough: they kept 80-90% of
     the benefit of 80 (`scripts/rank_standard_questions.py` picks them on other data; docs/10).
- Combine each group's own survey answers with record citizens' estimate:
  estimate = (worth x record citizens' shares + the group's answers) / (worth + people in the group).
  Fit the worth on other questions only (leave one question out). In Singapore it came out at about 58 people
  for record citizens learned from other countries.
- For a brand-new question, also combine the chatbot kind's estimate (same formula, its own fitted worth):
  record citizens from your own survey plus the chatbot kind did best at every survey size in both countries.
  When record citizens learned from other countries that asked the question, the chatbot added nothing.
- If you use a chatbot, use the best one available. Five chatbots combined by track record did about as well as
  the best alone; a simple average did worse; a small open model added nothing (docs/10).
- If the same question was asked recently in the same large survey, its answers by group are the best prior
  (US: answers from two years earlier were 2.4 points off without any new survey).

## Step 4. Measure with the scorecard

- **One method for every headline number.** Draw small surveys (150, 300, 600 people, ten draws each) from a
  large real survey; estimate each group's answer from the survey alone, and with each kind of AI combined in
  the same way; score every estimate against the people not drawn. `scripts/one_method_experiment.py`.
  Never mix setups across the page (the earlier page did, and was rebuilt on 17 Oct 2026).
- **Points off**: gap between estimate and real answer, percentage points per answer option, per group and
  question, averaged over draws. Report the **typical group** (the middle result across groups and questions).
- **Survey alone** = each group's answer read straight off the people in the survey. Always report against it.
- **Less error** = (survey alone points off − method points off) / survey alone points off, from unrounded values.
- Secondary check, analysts only: **standout groups** (the quarter of group answers furthest from the national
  average, `scripts/standout_split.py`). Compared with the survey alone they gained no more than other groups;
  compared with giving every group the overall answer ("No AI") they gain most. Say which comparison you use.
- Best possible (floor) in the one-method test: about 1.5 points in Singapore and 1.7 in the US
  (`scripts/yardstick_noise.py`): even a perfect estimate lands this far off, because the people it is checked
  against are a sample too. Reading guide: about 1.5 best possible, 3 good enough to act on, 5 rough level only,
  15 guessing blind.
- Score groups, not individuals: people repeat only about 70-80% of their own answers weeks later, but a
  typical group's answer shares move under 2 points (`docs/results/self_agreement_twin2k.md`).
- Group differences reproduced (gap slope) shows flattening: chatbot kind 81% US, 36% Singapore, 25% China.
- Harness: `evaluate/harness.py` (`score`, `segment_fidelity`); scripts in `scripts/*_experiment.py`.

**Scoring rules learned the hard way**
- Score a small sample against the people **not** in it, and average scores across draws, not predictions.
  (Averaging predictions first made a 300-person survey look like 1,500 and was corrected on 17 Oct 2026.)
- Never claim a capability that was not tested (the chatbot "drafting questions" claim was removed).
- Check example groups in the data before naming them (people over 60 were not a standout group in Singapore;
  Indian and Malay Singaporeans and young adults were, and in the US Republicans, Democrats and Black Americans).
- Check that every example uses a question that is actually in the records (prayer was not; religious services was).
- Do not generalise from too few cases (an online-polls claim rested on 3 polls and was removed).

## Step 5. Pilot before relying on it

Run one pilot with 600 people on your real question plus the standard questions. Let record citizens fill
in the groups from 300 of them and compare with what all 600 said. If they agree, later surveys can use 300.
In Singapore, 300 real people + AI were about as accurate for each group as 600 people alone (both 2.7 points
off for a typical group). The pilot also shows how much the chatbot kind adds on a truly new question, which our
tests (on well-known survey questions it may have read about) could not.

## Step 6. Decide with the five rules

1. Use AI to stretch a smaller real survey, not to replace it (smaller or more frequent surveys).
2. Pick the AI by asking whether your question has been asked before (three routes above).
3. AI helps most with small groups.
4. Don't borrow numbers from other surveys or published reports (typically 11 and 8 points off); the exception
   is the same question in a recent round of the same large survey.
5. Insist on the scorecard, group by group, against the survey alone.

## Step 7. Report for a C-suite reader

Use the `c-suite-explainer` skill and `glossary.md`. Page order that worked:
short answer → two ways to build a digital citizen, shown with one person → how we measure accuracy
(the one test, points off, the scale, why groups rather than individuals) → what it is worth → where AI helps
most (which AI, by whether the question was asked before; small groups; why the chatbot works better in the
US) → what we tested and where it led (kept, dropped, corrected) → a decision tree for when and how to use AI
→ five short rules → limits and what to test next → full evidence folded away. Define the yardstick before
the first result, give every section one "so what", and say each finding once: the rules point back to the
evidence rather than repeating it.
Template: `templates/scorecard_page/`.

## Step 8. QA before sharing

Run `qa_checklist.md`: trace every number, check contrast and headings, phone width, dark mode, language.
Log findings and fixes.
