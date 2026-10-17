# Library test: United States (GSS as the library, WVS as the new questions)

Generated 2026-10-17 06:58 UTC; runtime 45s.

New questions: 31 WVS-7 US items (exact 2, close 13, loose 16 matches). Truth: WVS US (n=2,596, fielded 2017) on common bins, 21 groups (20 segments, min n=50). Library: GSS 2024 (n=3,986) and GSS 2022 (n=4,149). Noise floor: median 0.7 pts (population), 1.3 pts (segments). All errors are mean absolute error per bin, in percentage points.

## Step 1: can a wording search find the right library question?

Of the 31 WVS items with a hand-checked GSS match, the TF-IDF search puts the right one first for 16, in the top 3 for 20. Median top-1 similarity: 0.22 for items that have a match vs 0.07 for items that do not.

| wvs_item | quality | hand_match | top1 | top1_sim | rank_of_hand_match |
|---|---|---|---|---|---|
| Q46 | close | happy | happy | 0.11 | 1.00 |
| Q47 | close | health | happy | 0.19 | 2.00 |
| Q50 | loose | satfin | satfin | 0.24 | 1.00 |
| Q57 | exact | trust | trust | 0.83 | 1.00 |
| Q64 | close | conclerg | coneduc | 0.22 |  |
| Q65 | close | conarmy | coneduc | 0.24 | 3.00 |
| Q66 | close | conpress | conpress | 0.42 | 1.00 |
| Q70 | loose | conjudge | coneduc | 0.26 |  |
| Q71 | loose | confed | coneduc | 0.23 |  |
| Q73 | close | conlegis | coneduc | 0.26 |  |
| Q106 | loose | eqwlth | fepresch | 0.07 |  |
| Q108 | loose | helpnot | helppoor | 0.10 | 3.00 |
| Q110 | loose | getahead | getahead | 0.08 | 1.00 |
| Q122 | loose | immjobs | immjobs | 0.09 | 1.00 |
| Q126 | loose | immcrime | immcrime | 0.11 | 1.00 |
| Q131 | loose | fear | socfrend | 0.08 |  |
| Q171 | close | attend | attend | 0.56 | 1.00 |
| Q182 | loose | homosex | god | 0.04 |  |
| Q184 | loose | abany | abany | 0.09 | 1.00 |
| Q186 | loose | premarsx | teensex | 0.11 |  |
| Q188 | loose | letdie1 | god | 0.04 |  |
| Q195 | loose | cappun | cappun | 0.22 | 1.00 |
| Q240 | close | polviews | trust | 0.19 | 3.00 |
| Q287 | close | class | class | 0.55 | 1.00 |
| Q67 | close | contv | coneduc | 0.26 |  |
| Q75 | loose | coneduc | coneduc | 0.26 | 1.00 |
| Q77 | close | conbus | conbus | 0.49 | 1.00 |
| Q78 | close | confinan | confinan | 0.37 | 1.00 |
| Q165 | loose | god | god | 0.36 | 1.00 |
| Q166 | exact | postlife | postlife | 0.74 | 1.00 |
| Q201 | close | news | natenrgy | 0.07 |  |

## Steps 2-3: how good is the answer, by method

| method | pop_mae_median | pop_mae_mean | seg_mae_median | seg_mae_mean | seg_mae_over_floor | gap_r | gap_slope | n_items | n_cells |
|---|---|---|---|---|---|---|---|---|---|
| uniform | 14.73 | 15.72 | 15.78 | 16.25 | 14.33 |  | 0.00 | 31 | 651 |
| everyone is average (true level, no spread) [oracle] | 0.00 | 0.00 | 2.87 | 3.71 | 1.50 |  | 0.00 | 31 | 651 |
| library 2024: matched GSS question, used as is | 11.10 | 11.71 | 10.73 | 12.40 | 9.33 | 0.60 | 0.52 | 31 | 651 |
| library 2022: matched GSS question, used as is | 10.25 | 12.10 | 11.21 | 12.92 | 9.91 | 0.56 | 0.59 | 31 | 651 |
| library 2024: headline only, no spread | 11.10 | 11.71 | 11.34 | 12.46 | 10.06 |  | 0.00 | 31 | 651 |

`seg_mae_over_floor` is the median segment error minus what survey sampling noise alone would produce; `gap_r`/`gap_slope` say whether group differences are reproduced (1 = perfectly).

## By how close the library match is (segment error, median points)

| method | exact | close | loose |
|---|---|---|---|
| everyone is average (true level, no spread) [oracle] | 4.38 | 2.21 | 3.19 |
| library 2022: matched GSS question, used as is | 10.30 | 9.42 | 12.81 |
| library 2024: headline only, no spread | 10.72 | 9.52 | 11.94 |
| library 2024: matched GSS question, used as is | 9.30 | 8.89 | 12.04 |
| uniform | 17.83 | 19.49 | 12.04 |

### Population level, by match quality

| method | exact | close | loose |
|---|---|---|---|
| everyone is average (true level, no spread) [oracle] | 0.00 | 0.00 | 0.00 |
| library 2022: matched GSS question, used as is | 9.87 | 7.95 | 11.78 |
| library 2024: headline only, no spread | 10.82 | 7.27 | 12.64 |
| library 2024: matched GSS question, used as is | 10.82 | 7.27 | 12.64 |
| uniform | 16.71 | 18.93 | 11.69 |

## Per question (segment error, median points)

| question_id | question | gss_match | quality | library 2024: matched GSS question, used as is |
|---|---|---|---|---|
| Q106 | Reduce income differences vs incentives | eqwlth | loose | 9.9 |
| Q108 | Government vs individual responsibility | helpnot | loose | 11.9 |
| Q110 | Hard work vs luck gets you ahead | getahead | loose | 5.7 |
| Q122 | Immigrants and jobs | immjobs | loose | 11.1 |
| Q126 | Immigrants raise terrorism / crime risk | immcrime | loose | 14.7 |
| Q131 | Feels safe in neighbourhood | fear | loose | 4.1 |
| Q165 | Believes in God | god | loose | 2.8 |
| Q166 | Believes in life after death | postlife | exact | 10.6 |
| Q171 | Religious attendance | attend | close | 6.0 |
| Q182 | Homosexuality acceptable | homosex | loose | 15.6 |
| Q184 | Abortion | abany | loose | 22.5 |
| Q186 | Sex before marriage acceptable | premarsx | loose | 18.5 |
| Q188 | Euthanasia | letdie1 | loose | 26.3 |
| Q195 | Death penalty | cappun | loose | 13.6 |
| Q201 | Reads a newspaper | news | close | 5.5 |
| Q240 | Left-right / liberal-conservative | polviews | close | 3.0 |
| Q287 | Subjective social class | class | close | 10.9 |
| Q46 | Happiness | happy | close | 6.4 |
| Q47 | Self-rated health | health | close | 2.0 |
| Q50 | Satisfaction with household finances | satfin | loose | 9.5 |
| Q57 | Most people can be trusted | trust | exact | 8.9 |
| Q64 | Confidence: churches / organized religion | conclerg | close | 7.0 |
| Q65 | Confidence: armed forces / military | conarmy | close | 6.1 |
| Q66 | Confidence: the press | conpress | close | 12.9 |
| Q67 | Confidence: television | contv | close | 20.6 |
| Q70 | Confidence: courts / Supreme Court | conjudge | loose | 5.4 |
| Q71 | Confidence: government / executive branch | confed | loose | 16.7 |
| Q73 | Confidence: parliament / Congress | conlegis | close | 22.4 |
| Q75 | Confidence: universities / education | coneduc | loose | 14.2 |
| Q77 | Confidence: major companies | conbus | close | 29.9 |
| Q78 | Confidence: banks | confinan | close | 20.1 |

### Per question, population level

| question_id | library 2024: matched GSS question, used as is |
|---|---|
| Q106 | 8.7 |
| Q108 | 10.8 |
| Q110 | 4.1 |
| Q122 | 11.9 |
| Q126 | 13.4 |
| Q131 | 1.8 |
| Q165 | 3.4 |
| Q166 | 11.8 |
| Q171 | 5.5 |
| Q182 | 15.0 |
| Q184 | 22.3 |
| Q186 | 18.1 |
| Q188 | 26.0 |
| Q195 | 13.6 |
| Q201 | 5.4 |
| Q240 | 2.4 |
| Q287 | 11.1 |
| Q46 | 6.1 |
| Q47 | 1.2 |
| Q50 | 9.5 |
| Q57 | 9.8 |
| Q64 | 7.3 |
| Q65 | 5.6 |
| Q66 | 11.9 |
| Q67 | 20.7 |
| Q70 | 4.3 |
| Q71 | 14.8 |
| Q73 | 22.6 |
| Q75 | 13.9 |
| Q77 | 29.9 |
| Q78 | 20.2 |

## Per group (median over questions)

| group | n_truth | n_gss2024 | library 2024: matched GSS question, used as is |
|---|---|---|---|
| age_band4=18-29 | 623 | 377 | 11.1 |
| age_band4=30-44 | 804 | 751 | 10.4 |
| age_band4=45-59 | 612 | 560 | 9.3 |
| age_band4=60+ | 533 | 839 | 12.3 |
| education3=Higher | 1311 | 958 | 9.3 |
| education3=Middle | 1191 | 1413 | 10.0 |
| race_eth=Black, non-Hispanic | 207 | 502 | 14.5 |
| race_eth=Hispanic | 448 | 447 | 12.6 |
| race_eth=Other, non-Hispanic | 206 | 275 | 9.8 |
| race_eth=White, non-Hispanic | 1710 | 1350 | 9.1 |
| region4=Midwest | 681 | 597 | 9.8 |
| region4=Northeast | 372 | 404 | 11.1 |
| region4=South | 887 | 999 | 10.7 |
| region4=West | 631 | 602 | 10.8 |
| religion4=Catholic | 582 | 504 | 11.5 |
| religion4=No religion | 1183 | 735 | 8.6 |
| religion4=Other religion | 248 | 294 | 13.8 |
| religion4=Protestant | 504 | 1036 | 12.4 |
| sex=Female | 1193 | 1401 | 10.5 |
| sex=Male | 1378 | 1185 | 10.4 |

## Worked examples (share choosing the option, %)

| question | group | real | library 2024: matched GSS question, used as is |
|---|---|---|---|
| Most people can be trusted: Most people can be trusted | ALL | 37.2 | 27.4 |
| Most people can be trusted: Most people can be trusted | age_band4=18-29 | 33.1 | 7.0 |
| Most people can be trusted: Most people can be trusted | age_band4=60+ | 47.1 | 34.8 |
| Most people can be trusted: Most people can be trusted | race_eth=Black, non-Hispanic | 16.9 | 14.0 |
| Most people can be trusted: Most people can be trusted | race_eth=Hispanic | 28.6 | 16.0 |
| Most people can be trusted: Most people can be trusted | religion4=No religion | 30.2 | 29.3 |
| Most people can be trusted: Most people can be trusted | religion4=Protestant | 47.8 | 26.4 |
| Most people can be trusted: Most people can be trusted | region4=South | 33.1 | 20.7 |
| Homosexuality acceptable: Acceptable | ALL | 44.4 | 55.3 |
| Homosexuality acceptable: Acceptable | age_band4=18-29 | 54.0 | 65.2 |
| Homosexuality acceptable: Acceptable | age_band4=60+ | 34.7 | 44.9 |
| Homosexuality acceptable: Acceptable | race_eth=Black, non-Hispanic | 23.0 | 41.8 |
| Homosexuality acceptable: Acceptable | race_eth=Hispanic | 44.1 | 53.9 |
| Homosexuality acceptable: Acceptable | religion4=No religion | 52.5 | 75.3 |
| Homosexuality acceptable: Acceptable | religion4=Protestant | 31.1 | 37.8 |
| Homosexuality acceptable: Acceptable | region4=South | 38.7 | 48.8 |
| Confidence: parliament / Congress: A great deal | ALL | 1.9 | 5.8 |
| Confidence: parliament / Congress: A great deal | age_band4=18-29 | 3.4 | 7.2 |
| Confidence: parliament / Congress: A great deal | age_band4=60+ | 0.2 | 4.0 |
| Confidence: parliament / Congress: A great deal | race_eth=Black, non-Hispanic | 2.4 | 6.8 |
| Confidence: parliament / Congress: A great deal | race_eth=Hispanic | 2.3 | 11.9 |
| Confidence: parliament / Congress: A great deal | religion4=No religion | 2.4 | 5.7 |
| Confidence: parliament / Congress: A great deal | religion4=Protestant | 0.6 | 4.1 |
| Confidence: parliament / Congress: A great deal | region4=South | 2.0 | 6.1 |
| Religious attendance: Weekly or more | ALL | 29.3 | 24.4 |
| Religious attendance: Weekly or more | age_band4=18-29 | 23.7 | 16.8 |
| Religious attendance: Weekly or more | age_band4=60+ | 41.0 | 34.1 |
| Religious attendance: Weekly or more | race_eth=Black, non-Hispanic | 44.8 | 25.8 |
| Religious attendance: Weekly or more | race_eth=Hispanic | 28.7 | 20.6 |
| Religious attendance: Weekly or more | religion4=No religion | 14.0 | 5.2 |
| Religious attendance: Weekly or more | religion4=Protestant | 50.7 | 39.9 |
| Religious attendance: Weekly or more | region4=South | 34.6 | 28.8 |
| Abortion: For | ALL | 37.5 | 59.8 |
| Abortion: For | age_band4=18-29 | 43.7 | 66.8 |
| Abortion: For | age_band4=60+ | 30.1 | 58.2 |
| Abortion: For | race_eth=Black, non-Hispanic | 26.8 | 70.0 |
| Abortion: For | race_eth=Hispanic | 37.8 | 55.5 |
| Abortion: For | religion4=No religion | 45.5 | 81.6 |
| Abortion: For | religion4=Protestant | 27.6 | 46.4 |
| Abortion: For | region4=South | 32.0 | 54.4 |
