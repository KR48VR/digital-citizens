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

| | Survey of 150 | 300 | 600 |
|---|---|---|---|
| **Singapore**, survey alone | 5.1 | 3.7 | 2.7 |
| + chatbot kind | 3.5 | 3.2 | 2.6 |
| + record citizens | 2.9 | 2.7 | 2.3 |
| + record citizens (own survey) | 3.6 | 2.9 | 2.5 |
| + demographics only (own survey) | 3.8 | 3.2 | 2.5 |
| + record citizens + chatbot kind | 2.9 | 2.7 | 2.4 |
| **United States**, survey alone | 6.4 | 4.9 | 3.7 |
| + chatbot kind | 3.8 | 3.4 | 3.2 |
| + record citizens | 2.4 | 2.4 | 2.4 |
| + record citizens (own survey) | 4.2 | 3.5 | 2.9 |
| + demographics only (own survey) | 5.1 | 4.4 | 3.5 |
| + record citizens + chatbot kind | 2.5 | 2.5 | 2.3 |

Full tables with averages and draw-to-draw ranges: `docs/results/stress_test/one_method_{singapore,us}.md`.

## What it changed

- **Held:** a few hundred people plus record citizens are about as accurate as a survey twice the size
  (Singapore: 300 + record citizens 2.7 = 600 alone 2.7; US: 150 + record citizens 2.4 beat 600 alone 3.7,
  an easier test because US record citizens learned from the same survey two years earlier).
- **Held:** the gain is biggest for small groups (150-person survey in Singapore: Indian 8.5 to 3.3, Malay
  6.6 to 3.2, Chinese 2.5 to 2.3).
- **Changed:** the chatbot kind is not needed. On its own it helps a small survey, but less than record
  citizens (300 people: a sixth less error in Singapore, a third in the US, against more than a quarter and a
  half); on top of record citizens it adds nothing in either country.
- **Changed:** standout groups gain no more than other groups compared with the survey alone (Singapore, 300:
  29% less error for both). The earlier "biggest for standout groups" came from the No AI comparison, where
  copying the average misses standout groups most. Moved to an analysts' note.
- **New:** for a brand-new question, record citizens learned from your own survey also help, a little less
  (Singapore: 150 + own 3.6 ≈ 300 alone 3.7; US: 300 + own 3.5 beat 600 alone 3.7).
- **Changed:** the earlier limit "a simpler demographics-only shortcut came close" does not hold under this
  test: it did worse than record citizens at 150 and 300 people in both countries (equal at 600 in Singapore).
