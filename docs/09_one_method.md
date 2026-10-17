# 09. One method for every headline number

**Why this exists.** By 17 October the scorecard used three different setups without saying so: the "300 + AI
= 600" box and the small-groups table came from a small survey blended with *both* kinds of AI (docs/07); the
chatbot-versus-record-citizens section started from the full survey's exact overall answer and added *one*
kind of AI ("No AI" comparison); and the short answer credited record citizens alone. King asked why the
methods were mixed. This test replaces all of them with one.

**The test** (`scripts/one_method_experiment.py`). For each country, question and survey size (150, 300,
600), draw a random sample from the large survey, ten times. For every group, estimate the answer shares:

| Method | What it uses |
|---|---|
| Survey alone | the group's own answers in the sample (weighted) |
| + chatbot kind | the group's answers combined with the chatbot's estimate for the group |
| + record citizens | combined with record citizens learned from past surveys (Singapore: 61 other countries; US: GSS 2022) |
| + record citizens (own survey) | combined with record citizens trained on the sample alone (a brand-new question) |
| + demographics only (own survey) | combined with a model trained on the sample using demographics only |
| + record citizens + chatbot kind | combined with both |

Combining: estimate = (worth x AI shares + group's answers) / (worth + people in the group); each source's
worth is fitted on the other questions only. Truth: the weighted answers of the people not drawn. Error:
points off per answer option, averaged over draws for each group and question; the typical group is the
middle result across groups and questions.

## Results (points off for a typical group)

Full tables with averages, 95% intervals and key comparisons: `docs/results/stress_test/one_method_{singapore,us}.md`.

| Survey of 300 | Singapore | United States |
|---|---|---|
| Survey alone | 3.7 | 4.9 |
| + chatbot kind | 3.2 | 3.4 |
| + record citizens learned from your own survey | 2.9 | 3.5 |
| + both (brand-new question) | 2.7 | 2.9 |
| + record citizens learned from past surveys | 2.7 | 2.4 |
| + record citizens from past surveys + chatbot kind | 2.7 | 2.5 |
| + last round's answers to the same question | - | 2.4 |
| Survey of 600 alone | 2.7 | 3.7 |

## What it changed

- **Held:** a few hundred people plus AI are about as accurate as a survey twice the size. Singapore, brand-new
  question: 300 + both kinds of AI 2.7 = 600 alone 2.7 (no detectable difference). US: 300 + both 2.9 beat 600
  alone 3.7.
- **Held:** the gain is biggest for small groups (150-person survey in Singapore, brand-new question: Indian
  8.5 to 3.2, Malay 6.6 to 4.1, Chinese 2.5 to 2.2).
- **New:** which AI to add depends on whether the question was asked before. Brand new: record citizens learned
  from your own survey plus the chatbot kind did best at every size in both countries (on their own the two
  kinds did about equally well). Asked in other countries: record citizens learned from them; the chatbot adds
  nothing. Asked recently in the same survey: reuse those answers.
- **Corrected (independent audit):** the US "record citizens from past surveys" learned from the same questions
  asked two years earlier; reusing those answers directly does as well (2.4, with no new survey), so that row
  is evidence for reuse, not for stretching a survey. It no longer supports any headline claim.
- **Changed:** standout groups gain no more than other groups compared with the survey alone (Singapore, 300:
  29% less error for both). The earlier "biggest for standout groups" came from the No AI comparison.
- **Changed:** the demographics-only shortcut did worse than record citizens at 150 and 300 people in both
  countries; the earlier limit saying it came close is withdrawn.
- **Caveat:** the questions are well known and their results are published, so the chatbot may have read
  them; its value on a truly new question is untested until a pilot.
