# Playbook: running a digital-citizens study

How to answer "how would these groups respond to X?" with AI, so that it works instead of flattening groups.
Written from the October 2026 project (United States, Singapore, China). Plain-language findings:
the scorecard page. Method detail: docs/09 (the one-method test behind every headline number), docs/06-08
and docs/results/.

## The recipe in one line

A few hundred real people answer the question. AI fills in each group's answer: the group's own answers are
blended with an AI estimate, and the fewer people a group has, the more the estimate counts. Which AI depends on
whether the question has been asked before. Brand new: blend your survey with both kinds of AI (record citizens
learned from your own survey, and the chatbot); it pays off most for groups with fewer than about 100 people in
the survey. Asked in large surveys in other countries: blend with record citizens learned from them, no chatbot.
Asked, worded the same, in the latest round of a large survey in your country: reuse those answers. Never borrow
numbers from other surveys or published reports. Always show the scorecard, against the survey alone.

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
- Blend each group's own survey answers with record citizens' estimate:
  estimate = (worth x record citizens' shares + the group's answers) / (worth + people in the group).
  Fit the worth on other questions only (leave one question out). In Singapore it came out at about 58 people
  for record citizens learned from other countries.
- For a brand-new question, also blend in the chatbot's estimate (same formula, its own fitted worth). Both
  kinds together came out ahead at every survey size; the lead was clear with 150 people in both countries and
  with 300 in the US, and within chance elsewhere (gaps under about half a point count as about the same).
  When record citizens learned from other countries that asked the question, the chatbot added nothing.
- If you use a chatbot, use the best one available. Five chatbots blended by track record did about as well as
  the best alone; a simple average did worse; a small open model added nothing (docs/10).
- If the same question was asked recently in the same large survey, its answers by group are the best prior
  (US: answers from two years earlier were 2.4 points off without any new survey).

## Step 4. Measure with the scorecard

- **One method for every headline number.** Draw small surveys (150, 300, 600 people, ten draws each) from a
  large real survey; estimate each group's answer from the survey alone, and with each kind of AI combined in
  the same way; score every estimate against the people not drawn. `scripts/one_method_experiment.py`.
  Never mix setups across the page (the earlier page did, and was rebuilt on 17 Oct 2026).
- **Points off**: gap between estimate and real answer, percentage points per answer option, per group and
  question, averaged over draws. Report the **median** across groups and questions, and say what it means where it first appears
  (the middle score: half did better, half worse).
- **Survey alone** = each group's answer read straight off the people in the survey. Always report against it.
- **Less error** = (survey alone points off − method points off) / survey alone points off, from unrounded values.
- Secondary check, analysts only: **standout groups** (the quarter of group answers furthest from the national
  average, `scripts/standout_split.py`). Compared with the survey alone they gained no more than other groups;
  compared with giving every group the overall answer ("No AI") they gain most. Say which comparison you use.
- Best possible in the one-method test: about 1.5 points in Singapore and 1.7 in the US
  (`scripts/yardstick_noise.py`): even a perfect estimate lands this far off, because the people it is checked
  against are a sample too. Reading guide, with the page's labels: 1.5-1.7 best possible, 3 good enough to act
  on, 5 the rough level only, 15 guessing blind (splitting answers evenly across the choices).
- Score groups, not individuals: people repeat only about 70-80% of their own answers weeks later, but groups'
  answer shares move a median of under 2 points (`docs/results/self_agreement_twin2k.md`).
- Group differences reproduced (gap slope) shows how far the chatbot makes groups look too alike: 81% US, 36%
  Singapore, 25% China.
- Harness: `evaluate/harness.py` (`score`, `segment_fidelity`); scripts in `scripts/*_experiment.py`.

**Scoring rules learned the hard way**
- Score a small sample against the people **not** in it, and average scores across draws, not predictions.
  (Averaging predictions first made a 300-person survey look like 1,500 and was corrected on 17 Oct 2026.)
- Never claim a capability that was not tested (the chatbot "drafting questions" claim was removed).
- Check example groups in the data before naming them (people over 60 were not a standout group in Singapore;
  Indian and Malay Singaporeans and young adults were, and in the US Republicans, Democrats and Black Americans).
- Check that every example uses a question that is actually in the records (prayer was not; religious services was).
- Do not generalise from too few cases (an online-polls claim rested on 3 polls and was removed).

## Step 5. Pilot when you will survey a topic more than once

Survey 600 people once, with your question plus the standard questions. Blend 300 of them with both kinds of AI
and check each group's answer against what the other 300 said; check the 300 alone the same way, and judge
across all groups together (one small group is too few people to check on its own). Never check against people
who were in the blended 300: that flatters the blend. If the blend comes out closer, later surveys on the topic
can use 300 people blended with both kinds of AI. In our test, 300 people blended with both kinds of AI were
about as accurate as 600 alone in Singapore (both a median of 2.7 points off). The pilot also shows how much the
chatbot adds on a truly new question, which our tests (on well-known survey questions it may have read about)
could not. For a one-off survey, skip the pilot and treat small-group answers with some caution.

## Step 6. Decide with the decision tree

The scorecard's five questions, in order; each answer either ends or says where to go next:
1. Groups or individual people? Individuals: ask them (people repeat only 70-80% of their own answers).
2. Your exact question, worded the same, in the latest round of a large public survey in your country? Reuse
   those answers.
3. Asked in large surveys in other countries? Blend your survey with record citizens learned from them; adding
   the chatbot does not help. Brand new? You need a survey: go on.
4. Will any group you care about have fewer than about 100 people in your survey? Blend your survey with both
   kinds of AI and go on. Otherwise a survey alone may be enough.
5. Will you survey the topic more than once? Pilot first (step 5). A one-off: skip the pilot, treat small-group
   answers with some caution.

Two rules that always apply: don't borrow numbers from other surveys or published reports (a median of 8 to 11
points off; the exception is step 2); insist on the scorecard, group by group, against the survey alone.

## Step 7. Report for a C-suite reader

Use the `c-suite-explainer` skill and `glossary.md`. Build the page in layers, so a reader without a stats or
tech background can follow the main path in a few minutes while the detail stays one click away:
1. **The answer**: a short summary that names each kind of AI and when each works best; right under it, one
   picture per case it describes, with how to read the numbers (points off, groups, the median) above the bars;
   then what counts as good enough (the scale, each level explained from the tests) and why about 3 points will do.
2. **Two kinds of digital citizen, shown with one person**; where record citizens learn from, folded.
3. **What to do**: the questions in order (a decision tree), each answer saying where to go next or what to do,
   with a number and its meaning; the step-by-step how-to folded under it; then any remaining rules. No separate
   worked example: a scenario before the decision logic confused readers.
4. **How we know**: the one test in three steps (groups versus individuals folded), then one picture and one
   "so what" per finding, in the summary's order (survey size, small groups, the two kinds side by side, with the
   table of each AI and the chatbot detail folded), then the map of what we tested, folded. The blend is
   explained where the reader first meets it, under the picture in the answer.
5. **Limits and what to test next**: two short lists, "What we have not shown yet" and "What to test next",
   one or two sentences each; caveats live here, not in the summary. No closing advice that contradicts the
   decision tree.
6. **The evidence in full, for analysts**, folded.
Say each finding once (explain a caveat where it is first needed, then refer back), use one label for every
takeaway ("So what"), point cross-references at headings that exist, link every number in "What to do" to where
it is shown and every finding in "How we know" to the full evidence for analysts (a link into a fold opens it),
link the casebook marked "private; access on request", number the five sections and give each its own colour band
(matched in the contents bar, so a team can say "section 4, the purple band"), and test the page
on a cold reader (a helper agent playing an executive with no stats background) before sharing.
Template: `templates/scorecard_page/`.

## Step 8. QA before sharing

Run `qa_checklist.md`: trace every number, check flow and integration, contrast and headings, phone width,
dark mode, language. Use three independent helper agents before sharing: one recomputes every number and claim
from the raw results, one reads the page cold as an executive with no stats background, one checks the casebook
and playbook package against the final page. Revise in one integrated pass against the agreed principles, not
one comment at a time, and list every change with its new wording. Log findings and fixes; leave decisions that
would reverse an earlier choice of King's as open items for King.
