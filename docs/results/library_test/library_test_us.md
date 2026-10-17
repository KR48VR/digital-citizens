# Library test: United States (GSS as the library, WVS as the new questions)

Generated 2026-10-17 07:41 UTC; runtime 101s.

New questions: 31 WVS-7 US items (exact 2, close 13, loose 16 matches). Truth: WVS US (n=2,596, fielded 2017) on common bins, 21 groups (20 segments, min n=50). Library: GSS 2024 (n=3,986) and GSS 2022 (n=4,149). Noise floor: median 0.7 pts (population), 1.3 pts (segments). All errors are mean absolute error per bin, in percentage points. 'Fresh small survey' rows: 300 random respondents answer the question; scored against the other respondents (no overlap), 5 repeats, scores averaged.

## Step 1: can a wording search find the right library question?

Two automatic matchers, scored against the hand-checked crosswalk over all 84 WVS items (31 have a GSS match, 53 do not):

| matcher | items_with_a_match | right_match_first | right_match_in_top3 | median_sim_when_match_exists | median_sim_when_no_match | no-match_items_scoring_above_median_matched | no-match_items |
|---|---|---|---|---|---|---|---|
| semantic | 31.00 | 24.00 | 26.00 | 0.62 | 0.44 | 7.00 | 53.00 |
| tfidf | 31.00 | 16.00 | 20.00 | 0.22 | 0.07 | 5.00 | 53.00 |

The last two columns matter: a no-match item that scores as high as a matched one would be given a wrong 'closest question' by an unattended search.

Semantic matcher, item by item:

| wvs_item | quality | hand_match | top1 | top1_sim | rank_of_hand_match |
|---|---|---|---|---|---|
| Q46 | close | happy | happy | 0.56 | 1.00 |
| Q47 | close | health | health | 0.65 | 1.00 |
| Q50 | loose | satfin | satfin | 0.62 | 1.00 |
| Q57 | exact | trust | trust | 0.99 | 1.00 |
| Q64 | close | conclerg | conclerg | 0.80 | 1.00 |
| Q65 | close | conarmy | conarmy | 0.78 | 1.00 |
| Q66 | close | conpress | conpress | 0.75 | 1.00 |
| Q70 | loose | conjudge | conjudge | 0.77 | 1.00 |
| Q71 | loose | confed | conbus | 0.82 |  |
| Q73 | close | conlegis | conbus | 0.79 | 2.00 |
| Q106 | loose | eqwlth | eqwlth | 0.50 | 1.00 |
| Q108 | loose | helpnot | helpnot | 0.60 | 1.00 |
| Q110 | loose | getahead | polviews | 0.50 |  |
| Q122 | loose | immjobs | letin1a | 0.58 | 2.00 |
| Q126 | loose | immcrime | immcrime | 0.54 | 1.00 |
| Q131 | loose | fear | socfrend | 0.50 |  |
| Q171 | close | attend | attend | 0.90 | 1.00 |
| Q182 | loose | homosex | bible | 0.43 |  |
| Q184 | loose | abany | abany | 0.42 | 1.00 |
| Q186 | loose | premarsx | premarsx | 0.43 | 1.00 |
| Q188 | loose | letdie1 | letdie1 | 0.42 | 1.00 |
| Q195 | loose | cappun | cappun | 0.53 | 1.00 |
| Q240 | close | polviews | polviews | 0.60 | 1.00 |
| Q287 | close | class | class | 0.70 | 1.00 |
| Q67 | close | contv | contv | 0.74 | 1.00 |
| Q75 | loose | coneduc | conbus | 0.81 |  |
| Q77 | close | conbus | conbus | 0.79 | 1.00 |
| Q78 | close | confinan | confinan | 0.80 | 1.00 |
| Q165 | loose | god | god | 0.73 | 1.00 |
| Q166 | exact | postlife | postlife | 0.60 | 1.00 |
| Q201 | close | news | news | 0.59 | 1.00 |

## Steps 2-3: how good is the answer, by method

| method | pop_mae_median | pop_mae_mean | seg_mae_median | seg_mae_mean | seg_mae_over_floor | gap_r | gap_slope | n_items | n_cells |
|---|---|---|---|---|---|---|---|---|---|
| uniform | 14.73 | 15.72 | 15.78 | 16.25 | 14.33 |  | 0.00 | 31 | 651 |
| everyone is average (true level, no spread) [oracle] | 0.00 | 0.00 | 2.87 | 3.71 | 1.50 |  | 0.00 | 31 | 651 |
| library 2024: matched GSS question, used as is | 11.10 | 11.71 | 10.73 | 12.40 | 9.33 | 0.60 | 0.52 | 31 | 651 |
| library 2022: matched GSS question, used as is | 10.25 | 12.10 | 11.21 | 12.92 | 9.91 | 0.56 | 0.59 | 31 | 651 |
| library 2024: headline only, no spread | 11.10 | 11.71 | 11.34 | 12.46 | 10.06 |  | 0.00 | 31 | 651 |
| record citizens alone (61-country model, no library) | 5.16 | 5.71 | 5.21 | 6.00 | 3.73 | 0.81 | 0.55 | 31 | 651 |
| library 2024 headline + record spread | 11.10 | 11.71 | 11.10 | 12.01 | 9.65 | 0.81 | 0.55 | 31 | 651 |
| library 2024 as is, averaged with headline + record spread | 11.10 | 11.71 | 10.80 | 12.11 | 9.49 | 0.76 | 0.47 | 31 | 651 |
| true level + record spread [oracle level] | 0.00 | 0.00 | 1.84 | 2.29 | 0.51 | 0.81 | 0.55 | 31 | 651 |
| fresh small survey (n=300): crosstab only | 2.75 | 3.06 | 5.14 | 5.69 | 3.85 | 0.52 | 0.82 | 31 | 651 |
| fresh small survey (n=300) + record spread | 2.66 | 2.83 | 3.35 | 3.60 | 2.05 | 0.83 | 0.75 | 31 | 651 |
| fresh small survey (n=300) + demographics-only spread | 2.50 | 2.84 | 3.96 | 4.30 | 2.63 | 0.54 | 0.53 | 31 | 651 |
| library 2024 as is, averaged with small survey (n=300) + record spread | 5.39 | 5.96 | 5.66 | 6.50 | 4.21 | 0.79 | 0.61 | 31 | 651 |
| library 2024 + survey-difference shift learned from the other 9 confidence questions (anchors) [confidence items only] | 7.92 | 8.43 | 8.69 | 9.35 | 7.50 | 0.48 | 0.41 | 10 | 210 |

`seg_mae_over_floor` is the median segment error minus what survey sampling noise alone would produce; `gap_r`/`gap_slope` say whether group differences are reproduced (1 = perfectly).

## By how close the library match is (segment error, median points)

| method | exact | close | loose |
|---|---|---|---|
| everyone is average (true level, no spread) [oracle] | 4.38 | 2.21 | 3.19 |
| fresh small survey (n=300) + demographics-only spread | 3.56 | 3.57 | 4.28 |
| fresh small survey (n=300) + record spread | 3.46 | 3.11 | 3.51 |
| fresh small survey (n=300): crosstab only | 5.19 | 4.73 | 5.47 |
| library 2022: matched GSS question, used as is | 10.30 | 9.42 | 12.81 |
| library 2024 + survey-difference shift learned from the other 9 confidence questions (anchors) [confidence items only] |  | 8.98 | 6.84 |
| library 2024 as is, averaged with headline + record spread | 10.53 | 9.19 | 12.08 |
| library 2024 as is, averaged with small survey (n=300) + record spread | 4.81 | 4.67 | 6.15 |
| library 2024 headline + record spread | 11.20 | 9.03 | 12.00 |
| library 2024: headline only, no spread | 10.72 | 9.52 | 11.94 |
| library 2024: matched GSS question, used as is | 9.30 | 8.89 | 12.04 |
| record citizens alone (61-country model, no library) | 6.56 | 3.62 | 6.38 |
| true level + record spread [oracle level] | 1.85 | 1.63 | 2.06 |
| uniform | 17.83 | 19.49 | 12.04 |

### Population level, by match quality

| method | exact | close | loose |
|---|---|---|---|
| everyone is average (true level, no spread) [oracle] | 0.00 | 0.00 | 0.00 |
| fresh small survey (n=300) + demographics-only spread | 1.98 | 2.46 | 2.60 |
| fresh small survey (n=300) + record spread | 2.89 | 2.58 | 2.97 |
| fresh small survey (n=300): crosstab only | 2.69 | 2.62 | 2.96 |
| library 2022: matched GSS question, used as is | 9.87 | 7.95 | 11.78 |
| library 2024 + survey-difference shift learned from the other 9 confidence questions (anchors) [confidence items only] |  | 8.44 | 4.00 |
| library 2024 as is, averaged with headline + record spread | 10.82 | 7.27 | 12.64 |
| library 2024 as is, averaged with small survey (n=300) + record spread | 5.63 | 4.29 | 6.00 |
| library 2024 headline + record spread | 10.82 | 7.27 | 12.64 |
| library 2024: headline only, no spread | 10.82 | 7.27 | 12.64 |
| library 2024: matched GSS question, used as is | 10.82 | 7.27 | 12.64 |
| record citizens alone (61-country model, no library) | 5.98 | 3.15 | 6.92 |
| true level + record spread [oracle level] | 0.00 | 0.00 | 0.00 |
| uniform | 16.71 | 18.93 | 11.69 |

## Per question (segment error, median points)

| question_id | question | gss_match | quality | library 2024: matched GSS question, used as is | record citizens alone (61-country model, no library) | library 2024 headline + record spread | fresh small survey (n=300) + record spread | fresh small survey (n=300) + demographics-only spread | library 2024 as is, averaged with small survey (n=300) + record spread |
|---|---|---|---|---|---|---|---|---|---|
| Q106 | Reduce income differences vs incentives | eqwlth | loose | 9.9 | 15.1 | 8.7 | 4.0 | 4.8 | 5.4 |
| Q108 | Government vs individual responsibility | helpnot | loose | 11.9 | 7.2 | 11.9 | 3.5 | 4.6 | 6.3 |
| Q110 | Hard work vs luck gets you ahead | getahead | loose | 5.7 | 7.0 | 4.3 | 4.3 | 3.4 | 3.9 |
| Q122 | Immigrants and jobs | immjobs | loose | 11.1 | 9.7 | 11.9 | 4.0 | 4.0 | 5.9 |
| Q126 | Immigrants raise terrorism / crime risk | immcrime | loose | 14.7 | 9.5 | 12.8 | 3.7 | 4.0 | 6.6 |
| Q131 | Feels safe in neighbourhood | fear | loose | 4.1 | 8.1 | 2.9 | 4.3 | 4.8 | 2.9 |
| Q165 | Believes in God | god | loose | 2.8 | 5.0 | 3.3 | 2.8 | 4.0 | 2.3 |
| Q166 | Believes in life after death | postlife | exact | 10.6 | 9.9 | 11.7 | 3.5 | 3.6 | 7.3 |
| Q171 | Religious attendance | attend | close | 6.0 | 2.9 | 5.8 | 3.1 | 3.5 | 2.8 |
| Q182 | Homosexuality acceptable | homosex | loose | 15.6 | 5.8 | 15.2 | 3.6 | 4.1 | 8.0 |
| Q184 | Abortion | abany | loose | 22.5 | 2.3 | 21.9 | 4.4 | 6.4 | 10.7 |
| Q186 | Sex before marriage acceptable | premarsx | loose | 18.5 | 2.6 | 18.1 | 3.0 | 4.1 | 9.4 |
| Q188 | Euthanasia | letdie1 | loose | 26.3 | 3.0 | 26.2 | 3.6 | 5.0 | 13.5 |
| Q195 | Death penalty | cappun | loose | 13.6 | 12.5 | 13.7 | 2.7 | 3.0 | 6.7 |
| Q201 | Reads a newspaper | news | close | 5.5 | 6.0 | 5.4 | 3.4 | 4.1 | 4.0 |
| Q240 | Left-right / liberal-conservative | polviews | close | 3.0 | 8.7 | 3.3 | 3.7 | 4.2 | 2.3 |
| Q287 | Subjective social class | class | close | 10.9 | 2.1 | 11.1 | 2.9 | 2.9 | 4.7 |
| Q46 | Happiness | happy | close | 6.4 | 2.6 | 6.3 | 5.5 | 5.0 | 3.2 |
| Q47 | Self-rated health | health | close | 2.0 | 3.2 | 1.8 | 3.1 | 3.1 | 2.2 |
| Q50 | Satisfaction with household finances | satfin | loose | 9.5 | 3.6 | 9.4 | 3.5 | 4.4 | 4.4 |
| Q57 | Most people can be trusted | trust | exact | 8.9 | 3.5 | 10.4 | 3.6 | 3.7 | 3.9 |
| Q64 | Confidence: churches / organized religion | conclerg | close | 7.0 | 5.6 | 7.3 | 2.7 | 4.1 | 4.3 |
| Q65 | Confidence: armed forces / military | conarmy | close | 6.1 | 12.5 | 6.6 | 3.3 | 4.1 | 3.2 |
| Q66 | Confidence: the press | conpress | close | 12.9 | 2.6 | 11.8 | 2.3 | 2.8 | 6.1 |
| Q67 | Confidence: television | contv | close | 20.6 | 4.2 | 20.5 | 3.7 | 2.9 | 8.4 |
| Q70 | Confidence: courts / Supreme Court | conjudge | loose | 5.4 | 9.3 | 4.4 | 3.7 | 3.2 | 3.7 |
| Q71 | Confidence: government / executive branch | confed | loose | 16.7 | 4.5 | 16.3 | 2.9 | 3.5 | 7.5 |
| Q73 | Confidence: parliament / Congress | conlegis | close | 22.4 | 4.6 | 22.1 | 2.3 | 2.5 | 10.1 |
| Q75 | Confidence: universities / education | coneduc | loose | 14.2 | 5.8 | 13.0 | 3.4 | 3.5 | 7.6 |
| Q77 | Confidence: major companies | conbus | close | 29.9 | 2.6 | 30.4 | 2.8 | 3.8 | 14.5 |
| Q78 | Confidence: banks | confinan | close | 20.1 | 1.9 | 20.9 | 3.2 | 3.8 | 10.0 |

### Per question, population level

| question_id | library 2024: matched GSS question, used as is | record citizens alone (61-country model, no library) | library 2024 headline + record spread | fresh small survey (n=300) + record spread | fresh small survey (n=300) + demographics-only spread | library 2024 as is, averaged with small survey (n=300) + record spread |
|---|---|---|---|---|---|---|
| Q106 | 8.7 | 15.2 | 8.7 | 3.5 | 3.9 | 4.6 |
| Q108 | 10.8 | 7.5 | 10.8 | 3.0 | 3.4 | 6.1 |
| Q110 | 4.1 | 7.1 | 4.1 | 3.4 | 2.4 | 2.8 |
| Q122 | 11.9 | 9.7 | 11.9 | 3.6 | 3.6 | 5.4 |
| Q126 | 13.4 | 9.0 | 13.4 | 2.5 | 2.4 | 5.9 |
| Q131 | 1.8 | 8.7 | 1.8 | 3.8 | 2.9 | 2.9 |
| Q165 | 3.4 | 5.2 | 3.4 | 2.5 | 2.6 | 2.8 |
| Q166 | 11.8 | 9.7 | 11.8 | 3.2 | 1.5 | 7.5 |
| Q171 | 5.5 | 1.6 | 5.5 | 2.6 | 2.3 | 1.9 |
| Q182 | 15.0 | 5.2 | 15.0 | 2.7 | 2.4 | 7.7 |
| Q184 | 22.3 | 1.2 | 22.3 | 4.0 | 5.9 | 10.7 |
| Q186 | 18.1 | 1.6 | 18.1 | 2.1 | 2.6 | 9.3 |
| Q188 | 26.0 | 2.6 | 26.0 | 2.9 | 4.6 | 13.2 |
| Q195 | 13.6 | 12.6 | 13.6 | 1.8 | 2.0 | 6.9 |
| Q201 | 5.4 | 5.8 | 5.4 | 3.0 | 2.8 | 3.8 |
| Q240 | 2.4 | 8.8 | 2.4 | 3.1 | 3.2 | 1.7 |
| Q287 | 11.1 | 1.8 | 11.1 | 2.7 | 2.2 | 4.9 |
| Q46 | 6.1 | 1.5 | 6.1 | 4.8 | 4.0 | 3.0 |
| Q47 | 1.2 | 3.2 | 1.2 | 2.6 | 2.5 | 1.8 |
| Q50 | 9.5 | 3.6 | 9.5 | 3.2 | 3.2 | 4.3 |
| Q57 | 9.8 | 2.2 | 9.8 | 2.6 | 2.5 | 3.7 |
| Q64 | 7.3 | 5.4 | 7.3 | 2.4 | 3.4 | 4.3 |
| Q65 | 5.6 | 12.5 | 5.6 | 2.5 | 3.3 | 3.1 |
| Q66 | 11.9 | 2.5 | 11.9 | 1.7 | 2.0 | 5.6 |
| Q67 | 20.7 | 4.4 | 20.7 | 3.3 | 2.4 | 8.8 |
| Q70 | 4.3 | 8.7 | 4.3 | 3.1 | 2.3 | 2.8 |
| Q71 | 14.8 | 4.3 | 14.8 | 2.7 | 2.5 | 6.7 |
| Q73 | 22.6 | 5.1 | 22.6 | 1.8 | 1.9 | 10.3 |
| Q75 | 13.9 | 6.7 | 13.9 | 2.2 | 2.2 | 7.5 |
| Q77 | 29.9 | 2.0 | 29.9 | 2.4 | 3.2 | 14.3 |
| Q78 | 20.2 | 1.7 | 20.2 | 1.8 | 1.9 | 10.4 |

## Per group (median over questions)

| group | n_truth | n_gss2024 | library 2024: matched GSS question, used as is | record citizens alone (61-country model, no library) | library 2024 headline + record spread | fresh small survey (n=300) + record spread | fresh small survey (n=300) + demographics-only spread | library 2024 as is, averaged with small survey (n=300) + record spread |
|---|---|---|---|---|---|---|---|---|
| age_band4=18-29 | 621 | 377 | 11.1 | 3.9 | 10.8 | 3.9 | 4.7 | 6.6 |
| age_band4=30-44 | 802 | 751 | 10.4 | 5.2 | 9.9 | 3.3 | 3.9 | 4.6 |
| age_band4=45-59 | 610 | 560 | 9.3 | 5.5 | 10.7 | 3.7 | 4.7 | 4.8 |
| age_band4=60+ | 531 | 839 | 12.3 | 7.4 | 12.6 | 3.7 | 4.9 | 6.0 |
| education3=Higher | 1308 | 958 | 9.3 | 5.7 | 12.1 | 2.6 | 4.1 | 4.8 |
| education3=Middle | 1188 | 1413 | 10.0 | 5.5 | 9.5 | 3.2 | 3.4 | 5.3 |
| race_eth=Black, non-Hispanic | 205 | 502 | 14.5 | 5.4 | 11.8 | 4.9 | 6.5 | 7.7 |
| race_eth=Hispanic | 446 | 447 | 12.6 | 4.7 | 10.7 | 3.5 | 3.5 | 6.8 |
| race_eth=Other, non-Hispanic | 205 | 275 | 9.8 | 4.8 | 10.5 | 4.6 | 4.5 | 4.9 |
| race_eth=White, non-Hispanic | 1709 | 1350 | 9.1 | 5.7 | 11.3 | 2.7 | 3.2 | 4.5 |
| region4=Midwest | 678 | 597 | 9.8 | 5.8 | 10.7 | 3.2 | 3.3 | 5.1 |
| region4=Northeast | 370 | 404 | 11.1 | 4.8 | 11.3 | 3.2 | 3.3 | 5.8 |
| region4=South | 885 | 999 | 10.7 | 5.7 | 10.9 | 3.1 | 3.6 | 5.5 |
| region4=West | 629 | 602 | 10.8 | 4.6 | 10.6 | 3.0 | 3.2 | 5.6 |
| religion4=Catholic | 580 | 504 | 11.5 | 6.3 | 11.5 | 3.6 | 4.2 | 5.8 |
| religion4=No religion | 1181 | 735 | 8.6 | 4.3 | 10.0 | 3.5 | 3.6 | 4.2 |
| religion4=Other religion | 247 | 294 | 13.8 | 4.0 | 12.5 | 4.5 | 5.2 | 7.0 |
| religion4=Protestant | 503 | 1036 | 12.4 | 6.5 | 11.9 | 3.7 | 5.5 | 6.1 |
| sex=Female | 1188 | 1401 | 10.5 | 5.2 | 9.7 | 3.0 | 3.5 | 5.5 |
| sex=Male | 1376 | 1185 | 10.4 | 5.6 | 12.6 | 3.2 | 3.3 | 5.1 |

## Worked examples (share choosing the option, %)

| question | group | real | library 2024: matched GSS question, used as is | record citizens alone (61-country model, no library) | library 2024 headline + record spread | fresh small survey (n=300) + record spread | fresh small survey (n=300) + demographics-only spread | library 2024 as is, averaged with small survey (n=300) + record spread |
|---|---|---|---|---|---|---|---|---|
| Most people can be trusted: Most people can be trusted | ALL | 37.2 | 27.4 | 34.9 | 27.4 | 39.0 | 37.5 | 33.2 |
| Most people can be trusted: Most people can be trusted | age_band4=18-29 | 33.1 | 7.0 | 29.5 | 21.9 | 32.0 | 29.7 | 19.5 |
| Most people can be trusted: Most people can be trusted | age_band4=60+ | 47.1 | 34.8 | 42.3 | 34.7 | 48.0 | 46.9 | 41.4 |
| Most people can be trusted: Most people can be trusted | race_eth=Black, non-Hispanic | 16.9 | 14.0 | 23.3 | 15.7 | 22.1 | 32.0 | 18.0 |
| Most people can be trusted: Most people can be trusted | race_eth=Hispanic | 28.6 | 16.0 | 26.3 | 18.7 | 29.5 | 30.8 | 22.7 |
| Most people can be trusted: Most people can be trusted | religion4=No religion | 30.2 | 29.3 | 34.1 | 26.5 | 34.8 | 34.5 | 32.1 |
| Most people can be trusted: Most people can be trusted | religion4=Protestant | 47.8 | 26.4 | 41.3 | 33.7 | 49.5 | 47.4 | 38.0 |
| Most people can be trusted: Most people can be trusted | region4=South | 33.1 | 20.7 | 31.9 | 24.3 | 35.3 | 37.9 | 28.0 |
| Homosexuality acceptable: Acceptable | ALL | 44.4 | 55.3 | 36.6 | 55.3 | 50.0 | 45.9 | 52.7 |
| Homosexuality acceptable: Acceptable | age_band4=18-29 | 54.0 | 65.2 | 38.7 | 57.4 | 55.9 | 52.7 | 60.6 |
| Homosexuality acceptable: Acceptable | age_band4=60+ | 34.7 | 44.9 | 33.7 | 52.4 | 42.8 | 36.7 | 43.9 |
| Homosexuality acceptable: Acceptable | race_eth=Black, non-Hispanic | 23.0 | 41.8 | 26.2 | 44.9 | 42.5 | 49.9 | 42.1 |
| Homosexuality acceptable: Acceptable | race_eth=Hispanic | 44.1 | 53.9 | 35.3 | 54.0 | 48.5 | 42.6 | 51.2 |
| Homosexuality acceptable: Acceptable | religion4=No religion | 52.5 | 75.3 | 43.3 | 62.0 | 59.5 | 59.1 | 67.4 |
| Homosexuality acceptable: Acceptable | religion4=Protestant | 31.1 | 37.8 | 29.0 | 47.7 | 38.6 | 34.3 | 38.2 |
| Homosexuality acceptable: Acceptable | region4=South | 38.7 | 48.8 | 32.9 | 51.5 | 45.7 | 46.4 | 47.2 |
| Confidence: parliament / Congress: A great deal | ALL | 1.9 | 5.8 | 3.3 | 5.8 | 1.0 | 1.7 | 3.4 |
| Confidence: parliament / Congress: A great deal | age_band4=18-29 | 3.4 | 7.2 | 4.0 | 6.5 | 1.2 | 2.9 | 4.2 |
| Confidence: parliament / Congress: A great deal | age_band4=60+ | 0.2 | 4.0 | 3.0 | 5.6 | 0.9 | 1.4 | 2.4 |
| Confidence: parliament / Congress: A great deal | race_eth=Black, non-Hispanic | 2.4 | 6.8 | 3.7 | 6.2 | 0.9 | 1.6 | 3.8 |
| Confidence: parliament / Congress: A great deal | race_eth=Hispanic | 2.3 | 11.9 | 3.9 | 6.4 | 1.2 | 2.0 | 6.5 |
| Confidence: parliament / Congress: A great deal | religion4=No religion | 2.4 | 5.7 | 3.4 | 5.9 | 0.9 | 1.4 | 3.3 |
| Confidence: parliament / Congress: A great deal | religion4=Protestant | 0.6 | 4.1 | 3.2 | 5.8 | 1.0 | 1.4 | 2.6 |
| Confidence: parliament / Congress: A great deal | region4=South | 2.0 | 6.1 | 3.5 | 6.1 | 1.1 | 1.6 | 3.6 |
| Religious attendance: Weekly or more | ALL | 29.3 | 24.4 | 27.4 | 24.4 | 34.0 | 31.3 | 29.2 |
| Religious attendance: Weekly or more | age_band4=18-29 | 23.7 | 16.8 | 19.9 | 16.8 | 25.0 | 21.4 | 20.9 |
| Religious attendance: Weekly or more | age_band4=60+ | 41.0 | 34.1 | 39.5 | 36.4 | 48.7 | 44.4 | 41.4 |
| Religious attendance: Weekly or more | race_eth=Black, non-Hispanic | 44.8 | 25.8 | 27.6 | 24.5 | 37.2 | 25.1 | 31.5 |
| Religious attendance: Weekly or more | race_eth=Hispanic | 28.7 | 20.6 | 26.1 | 23.1 | 31.3 | 28.6 | 26.0 |
| Religious attendance: Weekly or more | religion4=No religion | 14.0 | 5.2 | 7.9 | 4.9 | 18.1 | 16.0 | 11.6 |
| Religious attendance: Weekly or more | religion4=Protestant | 50.7 | 39.9 | 59.7 | 56.7 | 64.5 | 59.1 | 52.2 |
| Religious attendance: Weekly or more | region4=South | 34.6 | 28.8 | 30.7 | 27.6 | 37.9 | 31.5 | 33.4 |
| Abortion: For | ALL | 37.5 | 59.8 | 36.4 | 59.8 | 31.2 | 32.3 | 45.5 |
| Abortion: For | age_band4=18-29 | 43.7 | 66.8 | 37.5 | 61.0 | 36.1 | 37.8 | 51.5 |
| Abortion: For | age_band4=60+ | 30.1 | 58.2 | 36.7 | 60.1 | 29.3 | 31.7 | 43.7 |
| Abortion: For | race_eth=Black, non-Hispanic | 26.8 | 70.0 | 27.2 | 50.6 | 24.3 | 35.2 | 47.2 |
| Abortion: For | race_eth=Hispanic | 37.8 | 55.5 | 31.2 | 54.7 | 29.6 | 29.5 | 42.5 |
| Abortion: For | religion4=No religion | 45.5 | 81.6 | 44.1 | 67.5 | 39.9 | 39.4 | 60.7 |
| Abortion: For | religion4=Protestant | 27.6 | 46.4 | 30.2 | 53.7 | 23.0 | 26.3 | 34.7 |
| Abortion: For | region4=South | 32.0 | 54.4 | 34.0 | 57.4 | 28.2 | 32.5 | 41.3 |
