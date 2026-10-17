# Library test (United States)

Produced by `scripts/library_experiment.py`. The 'library' workflow tested end to end: a new question arrives
(a World Values Survey item, with the real US answer by group held out as truth), the closest previously asked
question is found in a library of other surveys (the General Social Survey 2022 and 2024), that survey is used as
the base, and record-anchored citizens spread it to groups. Plain-language write-up: `docs/08_library_test.md`.

| File | Contents |
|---|---|
| `library_test_us.md` | The report: search accuracy, every method's error at population and group level, by match quality, per question, per group, worked examples |
| `library_test_us.csv` | The method summary table |
| `library_test_us_cells.csv` | Every question x group x method score (mean absolute error per answer bin, noise floor, match quality) |
| `search_matches.csv` | What each automatic matcher proposed for every WVS question, and the rank of the hand-checked match |
| `record_all_us_pred.json` | Cached record-citizen predictions (mapping learned on the other 61 WVS countries), on the full WVS answer options |

The question pairs and bin mappings are in `src/digital_citizens/library/crosswalk_us.py`.
