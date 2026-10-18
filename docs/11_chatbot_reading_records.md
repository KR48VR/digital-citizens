# 11. Letting the chatbot read each person's answers, and checking it is not remembering

**The question.** The chatbot kind is told only what kind of person, or which group, it is answering for. Does
it get more accurate if it first reads each real person's own survey answers? And is the chatbot simply
remembering the published survey results?

**The difference from record citizens.** Both start from a person's real answers to other survey questions. Record citizens use a statistical model that learns, from real people who answered the new question, how those answers link to it, then apply that pattern. The chatbot reads the person's answers and fills the gap with what it has read about people in general; it learns no pattern from the data and needs no real answers to the new question.

**The short answer.** Reading each person's answers made the chatbot about as good as record citizens for groups, and
clearly better for individual people, but it adds little once a survey is blended with both kinds of AI, and
it costs chatbot fees. Not adopted yet. Three checks, run on both chatbots, found no sign that they remember the published
answers; only questions asked after its knowledge was frozen can rule that out.

## 1. The 100-person trial

`scripts/record_reading_trial.py` (plan / run / score). 100 Singaporeans (a third each Chinese, Malay and
Indian), 20 questions from the one-method test, Claude Opus 5.5 at low effort, one batch, about $2.58. Two arms,
same chatbot: told only demographics, or also the person's answers to the 57 other survey questions.

- Individual people: top choice right 47.0% against 52.0%, a gain of 5.0 points (95% range 3.1 to 6.8,
  resampling people); better for 61 people, worse for 21.
- Groups (against everyone else in the survey): mixed, within chance for groups of 21 to 34 people.

Results: `docs/results/record_reading_trial.md`.

## 2. The full test, in the one-method test

`record_reading_trial.py plan full` / `run full` (record arm only, all 1,997 respondents with 15+ of the 20
answers; cap $85, about $30.26), then `scripts/one_method_experiment.py singapore 10 reading`, which adds the
chatbot reading each person's answers (each group's estimate is the weighted average of the guesses for its people not drawn
into the survey) and record citizens learned from the same 57 questions, on the same draws. Every method shared
with the main results came out identical.

| Median points off, Singapore | 150 | 300 | 600 |
|---|---|---|---|
| Survey alone | 5.1 | 3.7 | 2.7 |
| + chatbot kind (Claude Fable 5.1) | 3.5 | 3.2 | 2.6 |
| + chatbot (Claude Opus), asked the usual way | 3.2 | 3.1 | 2.4 |
| + chatbot reading each person's answers | 3.1 | 3.0 | 2.5 |
| + record citizens (own survey) | 3.6 | 2.9 | 2.5 |
| + record citizens (own survey, same 57 questions) | 3.5 | 2.9 | 2.5 |
| + both kinds of AI (record citizens + chatbot kind) | 3.1 | 2.7 | 2.3 |
| + record citizens + chatbot reading each person's answers | 2.7 | 2.6 | 2.4 |

The Claude Opus row is the five-chatbot panel's (version not recorded), so it may not be the same Opus.
Every difference between the chatbot reading each person's answers and the chatbot kind, Claude Opus asked the usual way,
record citizens, or both kinds of AI had a 95% range crossing zero (for example, with record citizens blended
in: -0.45 at 150, range -0.70 to +0.05; -0.12 at 300, range -0.41 to +0.16). Results:
`docs/results/stress_test/one_method_singapore_reading.md`.

## 3. Memory checks

Warning signs were written into the scripts before running.

1. **Asked directly** (`scripts/memory_check.py`, about $0.18): with the survey named and its published figures
   requested, 5.3 points off nationally (median over questions; 4.8 by the average); unnamed, 4.5 (5.2 by the
   average); naming moved the median over all 200 group-question cells by -0.01. Exact recall would be under 1
   point. It said "estimate" for all 20 questions.
2. **Famous against little-known questions** (same script, free): seven famous questions written into the
   script before the check was run. The chatbots' edge over record citizens (each with no survey) was no better
   on famous questions (chatbot kind +2.2 against +0.8; chatbot reading each person's answers +1.7 against +1.2). The planned
   rank correlation between the edge and check 1's recall pointed towards memory (+0.68 and +0.41), but the
   unnamed guesses showed the same link or stronger (+0.76 and +0.58), so it tracks how easy a question is to
   guess; holding that constant leaves +0.03 and -0.27. Added after seeing this: the link with how much naming
   the survey helped, -0.51 and -0.42, where memory would make it positive.
3. **Disguised questions** (`scripts/disguise_check.py`, about $4.85): 150 people, the original prompt run again
   and a disguised one (questions reworded, answer options reversed, survey not named), in one batch: top choice
   right 53.3% and 52.9% (53.8% in the full test); combined answers 3.6 and 3.4 points off.

4. **Checks 1 and 3 for the scorecard's chatbot** (`scripts/memory_check_chatbot.py`, Claude Fable 5.1, about
   $0.76; the first attempt was refused for low credit before anything was sent): group answer shares for each
   question, named, unnamed (twice) and disguised; one of 80 answers unreadable, so 19 questions. Nationally 4.5
   named against 5.5 and 6.0 unnamed (medians over questions), but question by question naming moved the national
   answer by a median of +0.08 and brought it closer on only 7 of 19; across all cells +0.33 (further off when
   named). Disguised minus unnamed across all cells: -0.06. It said "estimate" for 19 and "partly" for 1. The
   scorecard's own estimates were 4.9 points off nationally.

Results: `docs/results/memory_check.md`, `docs/results/disguise_check.md`, `docs/results/memory_check_chatbot.md`.

## 4. What it means

- Our advice does not change: blend a small survey with record citizens and the chatbot.
- The chatbot reading each person's answers is a candidate for very small surveys, to try in a pilot; it costs about $30 in
  chatbot fees per 2,000 people and 20 questions, where record citizens need no chatbot.
- Next: questions asked after the chatbot's knowledge was frozen (a newer survey round, or a pilot's own
  questions), the only full check for memory.
