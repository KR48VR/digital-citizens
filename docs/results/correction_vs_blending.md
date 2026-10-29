# Blending against correcting (Singapore, the scorecard's test)

Same 10 draws of 150, 300 and 600 people, same 20 questions and 9 groups, scored against the people not drawn.
Median points off across groups and questions (lower is better). "Participants saved" is the share of a
300-person survey you could drop and still match it with the survey alone, read off the survey-alone curve.

| method | survey of 150 | survey of 300 | survey of 600 | participants saved at 300 |
|---|---|---|---|---|
| Survey alone | 5.08 | 3.74 | 2.68 |  |
| Blend: record citizens | 3.62 | 2.90 | 2.46 | 42% |
| Correct: record citizens | 4.75 | 3.56 | 2.60 | 9% |
| Blend: chatbot reading records | 3.06 | 2.95 | 2.50 | 39% |
| Correct: chatbot reading records | 4.79 | 3.49 | 2.57 | 13% |
| Blend: record citizens + chatbot reading records | 2.68 | 2.59 | 2.38 | 54% |
| Correct: record citizens + chatbot reading records | 4.67 | 3.49 | 2.55 | 12% |
| Blend: record citizens + chatbot (the scorecard's advice) | 3.13 | 2.71 | 2.35 | 50% |

## By group size, survey of 300

| method | groups under 100 people | groups of 100 or more |
|---|---|---|
| Survey alone | 4.21 | 2.00 |
| Blend: record citizens | 3.25 | 2.05 |
| Correct: record citizens | 3.98 | 1.90 |
| Blend: chatbot reading records | 3.48 | 1.94 |
| Correct: chatbot reading records | 3.96 | 1.90 |
| Blend: record citizens + chatbot reading records | 2.87 | 1.92 |
| Correct: record citizens + chatbot reading records | 3.97 | 1.91 |
| Blend: record citizens + chatbot (the scorecard's advice) | 2.99 | 1.78 |

## Key comparisons (difference in points off, first minus second; 95% range)

| first | second | difference | 95% range |
|---|---|---|---|
| corrected, tuned: record citizens (own survey), 300 | survey alone, 300 | -0.19 | -0.58 to +0.20 |
| corrected, tuned: record citizens (own survey), 300 | + record citizens (own survey), 300 | +0.66 | +0.26 to +0.90 |
| corrected, tuned: record citizens + chatbot reading records, 300 | + record citizens (own survey) + chatbot reading records, 300 | +0.90 | +0.57 to +1.24 |
| corrected, tuned: record citizens + chatbot reading records, 300 | survey alone, 600 | +0.81 | +0.39 to +1.12 |

Correcting is the tuned version (the AI's role shrinks when its guesses track answers loosely); the plain version
is in the full results file. The chatbot kind guesses whole groups, not people, so it cannot be used to correct:
with one guess per group, correcting gives back the survey alone.

Code: scripts/one_method_experiment.py (correction design) and scripts/correction_vs_blending.py; full results:
docs/results/stress_test/one_method_singapore_correction.md.
