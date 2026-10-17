# 08. Testing the "library" idea

**The question.** Can we build citizens from several public surveys, and when a new question comes in,
search the library for the closest question that was asked before, use that survey as the base, and let
the AI/record citizens "spread" the answer to every group?

**The short answer.** The search step works well enough. The spread step works well. The base step does
not: a matched question from a *different* survey is roughly 10 points off at the national level even
when the wording is nearly identical, because different surveys reach different people in different ways
and years. What does work is to take the national number from a small fresh survey of the exact question
and let record-based citizens spread it, or, with no fresh survey at all, to let the citizens answer from
their own past records. Both beat the library by a wide margin.

Numbers: `docs/results/library_test/library_test_us.md`. Code: `src/digital_citizens/library/`,
`scripts/library_experiment.py`.

## 1. How the test was set up

The United States is the one place where two different, full-detail surveys of the same population are on
disk, so it is where the idea can be tested honestly.

- **New questions:** 31 questions from the World Values Survey (US, 2,596 people, fielded 2017). The real
  answers, by group, are the truth we score against, held back from every method.
- **The library:** the General Social Survey 2022 (4,149 people) and 2024 (3,986 people), 84 questions each,
  with every person's answers. Each of the 31 new questions was hand-matched to the GSS question that asks
  the closest thing: 2 matches are near-identical in wording, 13 are close, 16 are loose.
- **Common scale:** the two surveys use different answer options, so both were put on 2-4 common bins
  (for example "a great deal / some / little or none"). All errors below are on those bins.
- **Groups:** sex, four age bands, two education levels, four race/ethnicity groups, four religion groups,
  four regions. Twenty groups, each with at least 50 real respondents.
- **Error:** mean absolute error per answer bin, in percentage points. Survey sampling noise alone would
  give about 0.7 points nationally and 1.3 points per group, so nothing can beat that floor.
- **Spread:** "record citizens" are the US respondents themselves. Each person's answer to the new question
  is predicted from their answers to the other ~80 questions, with the mapping learned on the other 61
  countries in the World Values Survey (90,085 people). No language model is involved.

## 2. Step by step

### Step 1: can a search find the right question in the library?

| Matcher | Right question ranked first | In the top three | Proposes a match for questions that have none |
|---|---|---|---|
| Word overlap | 16 of 31 | 20 of 31 | 5 of 53 score as high as a true match |
| Meaning-based (small local model) | 24 of 31 | 26 of 31 | 7 of 53 score as high as a true match |

The meaning-based matcher handles synonyms ("churches" vs "organized religion", "parliament" vs
"Congress"). Its misses are inside batteries of near-identical questions (it confuses confidence in
Congress with confidence in companies) and across different framings (the ten-point "is homosexuality ever
justifiable" scale vs the GSS "is it wrong" question). The last column is the catch: the search also offers a
confident "closest question" for questions that have no real counterpart (it offered "confidence in
Congress" for "confidence in elections"). A person has to check what it proposes.

### Step 2: how good is the base, taken from the matched question?

| Method | National error (points) | Group error | Share of real group differences reproduced |
|---|---|---|---|
| Know nothing (every answer equally likely) | 14.7 | 15.8 | 0% |
| **Library: the matched GSS 2024 question, used as is** | **11.1** | **10.7** | 52% (correlation 0.60) |
| Library: the GSS 2022 version instead | 10.3 | 11.2 | 59% |
| Library headline only, no spread | 11.1 | 11.3 | 0% |

By how close the match was (national error): near-identical wording 10.8 points, close 7.3, loose 12.6.
The surprise is the first number. "Most people can be trusted" is worded almost the same in both surveys,
yet 37% of the WVS sample agree and 27% of the GSS sample do. "Life after death": 71% vs 82%. The two
surveys reached different people (an online panel in 2017 vs a mixed in-person and web sample in 2024),
and differences of that size between survey houses are normal. They are as large as the differences
between groups we are trying to recover. For comparison, the same survey's previous wave was within 1.4
points in the earlier GSS test (`docs/results/baselines_gss2024.md`). A library of *other* surveys gives
a rough level, not a reliable one.

### Step 3: does spreading with record citizens fix it?

| Method | National error | Group error | Group differences reproduced |
|---|---|---|---|
| Library headline + record spread | 11.1 | 11.1 | 55% (correlation 0.81) |
| **Record citizens alone, no library at all** | **5.2** | **5.2** | 55% (correlation 0.81) |
| True national level + record spread (what spread can do at best) | 0 | 1.8 | 55% (correlation 0.81) |

The spread is right: the record citizens' group pattern correlates 0.81 with the real one, against 0.60
for the library's own group pattern. But a right pattern on a wrong level is still wrong, so adding the
spread to the library's headline gains nothing. With the true level, the same spread lands within 1.8
points of every group, barely above the noise floor. So the spread step is solved for groups this size;
the level is the whole problem.

The second row is the finding I did not expect: record citizens with no library and no fresh survey, just
their own past answers, are twice as accurate as the matched question from another survey, at both the
national and the group level. The people's own records are a better guide to a new question than the
closest question someone else asked.

### Step 4: what if you ask 300 real people the exact question?

| Method | National error | Group error | Group differences reproduced |
|---|---|---|---|
| Fresh survey of 300, groups read straight off it | 2.8 | 5.1 | 82% (correlation 0.52) |
| Fresh survey of 300 + demographics-only spread | 2.5 | 4.0 | 53% |
| **Fresh survey of 300 + record spread** | **2.7** | **3.4** | 75% (correlation 0.83) |
| Library averaged with the above | 5.4 | 5.7 | 61% |

Scored honestly: the 300 are drawn at random, the truth is computed on the *other* respondents, five
repeats, scores averaged. This is where "spreading" earns its keep: 300 people give a good national number
but noisy groups (5.1 points, because each group holds only a few dozen of them), and the record citizens
cut that to 3.4 while keeping the pattern of differences. Mixing the library back in only makes it worse.

### Step 5: can the library be corrected with anchor questions?

If a few of the library's questions are also asked in the fresh survey, the gap between the two surveys
can be measured and applied. Tested on the ten "confidence in institutions" questions, each corrected with
the gap learned from the other nine: national error fell from 14.3 to 7.9 points and group error from 15.5
to 8.1. A real gain, but uneven (it helped seven questions and hurt three) and still worse than record
citizens alone. Anchors make the library usable as a rough prior, not as a base.

## 3. What this means, in plain language

1. **Organise the library as people, not as questions.** The value of a public survey is its respondents
   with their many answers, because those records let the citizens answer *new* questions. Copying the
   closest old question across surveys is the weakest thing we tried. A survey that publishes only
   headlines, or asks only a handful of questions, adds almost nothing.
2. **Get the level from a fresh survey of the exact question, then spread.** Three hundred answers plus
   record spread gets every group within about 3.4 points. Six hundred gets you to what knowing the true
   level would give. Reading groups straight off a 300-person survey is a third worse than spreading it.
3. **With no fresh survey, use the citizens' own records, not another survey's question.** Five points of
   error nationally and per group, with the right pattern of group differences. That is a usable rough
   answer, and twice as good as the library.
4. **The search step needs a person in the loop.** A small meaning-based matcher finds the right question
   most of the time, but it also proposes confident matches for questions that have none.
5. **Anchors are the bridge.** If you do use a library survey, ask a few of its questions in your own
   survey so the house difference can be measured and removed. It halved the error here.

## 4. A correction to an earlier number

`docs/06` originally reported that 300 real answers put every Singapore group within 1.3 points and
recovered 94% of group differences. That calculation averaged five random samples before scoring (so it
behaved like a sample of 1,500) and scored against a truth that included the sampled people. Re-run with
the honest design above (`scripts/small_survey_recheck.py`, `docs/results/stress_test/small_survey_holdout.md`),
the Singapore numbers are:

| Real answers | Groups read straight off the survey | + record spread |
|---|---|---|
| 150 | 4.4 points | 3.4 |
| 300 | 3.2 | 2.9 |
| 600 | 2.6 | 2.3 |

China behaves the same way (3.4 / 2.4 at 150; 2.6 / 2.1 at 300; 2.0 / 1.7 at 600). The conclusion stands,
with smaller numbers: a small fresh survey is still the best realistic option, record spread improves it at
every size, and the "human level + record differences" result of 2.1 points in `docs/06` is what a survey of
about 600 reaches. The headline in that document has been corrected.

## 5. Limits of this test

- One country, where both surveys are unusually rich. The World Values Survey US sample was an online
  panel; part of the 10-point gap is that, not wording.
- The groups are large and coarse. Smaller groups (a single ethnicity in one region, for instance) would
  stress the spread harder and would favour the record citizens over reading groups off a small survey
  even more.
- The common bins throw information away; a finer comparison would need questions with identical scales.
- The record spread used ~80 other answers per person. A library survey with ten questions would spread
  much less well. Richness of the record is the thing to look for when choosing surveys for the library.
