# 10. Three more ideas tested: a panel of chatbots, fewer standard questions, boosting small groups

All three use the one-method test of docs/09 (`scripts/one_method_experiment.py`): small surveys drawn ten
times from a large real survey, every method combined with the group's own answers in the same way, scored
against the people not drawn, with 95% intervals from resampling questions and draws. Numbers below are points
off for a typical group with a survey of 300 people, unless stated. Full tables:
`docs/results/stress_test/one_method_{singapore,us}.md`, `boost_vs_standard.md`.

## Idea 2: a panel of chatbots, each counted by its track record

Blind group predictions came from five models: Claude Fable 5.1 (the original chatbot kind), Claude Opus,
Sonnet and Haiku (helper agents shown only the questions), and Qwen2.5-3B-Instruct, a small open model built by
Alibaba and run locally (`scripts/open_model_panel.py`, `panel_*.json`).

| Survey of 300 | Singapore | United States |
|---|---|---|
| Survey alone | 3.7 | 4.9 |
| + Fable (the chatbot kind on the page) | 3.2 | 3.4 |
| + Opus | 3.1 | 3.2 |
| + Sonnet | 3.1 | 3.5 |
| + Haiku | 3.3 | 3.9 |
| + Qwen 3B (open, Asian-built) | 3.7 | 4.8 |
| + panel, simple average | 3.3 | 4.2 |
| + panel, each counted by track record | 3.0 | 3.2 |
| Brand-new question: + record citizens from your survey + Fable | 2.7 | 2.9 |
| Brand-new question: + record citizens from your survey + weighted panel | 2.5 | 2.8 |

- Weighting by track record makes a panel about as good as its best member (here Opus); the gain over the
  single chatbot is within chance (Singapore -0.12, -0.49 to +0.18; US -0.19, -0.56 to +0.25).
- A simple average is worse than the best member, and clearly worse in the US (+0.82, +0.25 to +1.35), because
  weak members drag it down.
- The small open model added nothing in either country (no better than the survey alone) and was given almost no
  weight. Its answers were very overconfident (92% on one option on average). Larger Asian-built models were not
  tested; they need more memory than this machine has.
- Bigger Claude models did better: Opus > Sonnet > Haiku in both countries.
- With record citizens for a brand-new question, the weighted panel was slightly better than one chatbot
  (Singapore -0.18, -0.44 to +0.10; US -0.08, -0.36 to +0.25): within chance.

**Verdict:** worth it only with weighting by track record, and the gain is small. Picking the best available
model gets most of it.

## Idea 4: fewer standard questions

Short sets were chosen without using the target survey: for Singapore, on the World Values Survey in ten
Asia-Pacific neighbours (16,122 people); for the US, on the General Social Survey 2022
(`scripts/rank_standard_questions.py`). Questions are picked so that, together, they are closely linked to all
the others.

| Survey of 300, brand-new question | Singapore | United States |
|---|---|---|
| Survey alone | 3.7 | 4.9 |
| Record citizens from your survey, 5 standard questions | 3.1 | 4.0 |
| 10 standard questions | 3.1 | 3.8 |
| 20 standard questions | 3.0 | 3.8 |
| All (about 76 in Singapore, 83 in the US) | 2.9 | 3.5 |
| 20 standard questions + chatbot kind | 2.8 | 3.1 |
| All standard questions + chatbot kind | 2.7 | 2.9 |

- In Singapore, 5 to 20 questions were not detectably worse than all of them (20 questions: +0.08, -0.21 to
  +0.43) and kept about 80-90% of the gain.
- In the US, short sets lost more: 20 questions +0.30 (-0.06 to +0.66), 5 questions +0.51 (+0.03 to +0.84).
  20 questions kept about 80% of the gain.
- Adding the chatbot kind narrows the gap (20 questions + chatbot vs all + chatbot: Singapore +0.12, US +0.21,
  both within chance).

**Verdict:** about 20 standard questions keep most of the benefit, which makes the "half the people" budget case
much more realistic than 80 extra questions per person.

## Idea 7: boosting small groups in the survey

Surveys of 300 were drawn with extra people from small groups (Singapore: Malay and Indian, 20% of the sample
each; US: Black adults, 30%) and weighted back to the population (`one_method_*_boost.*`,
`scripts/compare_designs.py`).

| Survey of 300 | Normal | Boosted | Difference (95% interval) |
|---|---|---|---|
| Malay Singaporeans, survey alone | 5.0 | 3.8 | -1.25 (-2.26 to +0.02) |
| Malay Singaporeans, with AI | 3.6 | 3.1 | -0.52 (-1.45 to +0.21) |
| Indian Singaporeans, survey alone | 5.6 | 4.6 | -1.08 (-2.42 to +0.03) |
| Indian Singaporeans, with AI | 3.5 | 3.4 | -0.11 (-1.07 to +0.80) |
| Chinese Singaporeans, with AI | 1.7 | 2.2 | +0.48 (-0.15 to +0.86) |
| Singapore typical group, with AI | 2.7 | 2.7 | +0.02 (-0.25 to +0.31) |
| Black Americans, survey alone | 5.6 | 4.7 | -0.94 (-1.64 to +0.49) |
| Black Americans, with AI | 3.4 | 3.0 | -0.36 (-0.97 to +0.55) |
| US typical group, with AI | 2.9 | 2.8 | -0.13 (-0.40 to +0.24) |

"With AI" = record citizens learned from your own survey plus the chatbot kind.

- Boosting helps the boosted groups by about a point when the survey is read on its own, though with only 20-25
  questions per group the intervals just reach zero.
- Once AI fills in each group's answer, most of that gain is already there: AI and boosting do overlapping jobs.
- The largest group gets a little worse (fewer of its people are asked); the typical group is unchanged.
- At 600 people in the US, boosting Black adults to 30% left too few for checking on some questions.

**Verdict:** use boosting when a specific small group matters most to the decision, especially if the survey
will also be read without AI. With AI, the extra gain is modest.

## Also found and fixed

- In combinations of several sources, capping each source's weight after fitting could distort the balance
  between them. The cap now applies inside the fit. Published figures were unchanged except two analysts'
  comparisons that moved by 0.01-0.02 points.
