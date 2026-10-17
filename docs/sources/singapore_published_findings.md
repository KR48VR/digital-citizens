# Singapore: published survey findings combed for the evidence ledger (17 Oct 2026)

Row-level numbers that were mapped onto World Values Survey questions are in `data/ledger/singapore.csv`
(96 rows, 25 questions, about 50,000 effective respondents after confidence discounts). This note records
the sources behind them, how trustworthy each is as a prior, and what was checked and found unusable, so
the search is not repeated. Two research passes were made: official/academic sources, and media/commercial
polls plus social-media research. Figures were read from the primary PDF or page unless marked unverified.

## Sources used as priors

| Source | Fieldwork | Sample | Sampling | Used for | Confidence given |
|---|---|---|---|---|---|
| IPS Survey on Race, Religion and Language 2024 (Working Papers 59 and 65) | Apr-Aug 2024 | 4,000 citizens and PRs 18+, face-to-face, minority boosters, weighted | probability | religiosity and attendance by age, education, religion; comfort with neighbours of other races | 0.4-0.6 (identity wording differs; 2024 vs 2020) |
| Pew Research, Religion in South and Southeast Asia (topline) | Jun-Sep 2022 | 2,036 citizens and PRs 18+, mobile phone, raked | probability | religion importance, attendance, strong leader vs democracy, by religion | 0.4-0.9 |
| Asian Barometer wave 5 (2020) and wave 6 (2023), IPS slides | Jul-Sep 2020; Sep-Nov 2023 | 1,002 / 1,003 citizens 21+, face-to-face, weighted | probability | strong leader, experts, democracy best, satisfaction with democracy, suitability of democracy | 0.4-0.8 (wave 5 overlaps the WVS fieldwork period) |
| National Youth Survey 2022 (NYC, State of Youth 2024) | 2022 | 3,565 residents 15-34, weighted | probability | petitions, rallies, confidence in institutions, life satisfaction, ages 20-29 | 0.3-0.5 (12-month recall; youth only) |
| IPS Study on Social Capital | Jan-Jul 2016 | 3,000 residents 21+, face-to-face | probability | generalised trust (same wording as WVS), trust in other religions and nationalities | 0.6-0.7 (2016) |
| Singapore Life Panel, SMU ROSA brief on cost of living | Aug 2022 | 6,839 Singaporeans aged 57-76, online panel | online panel | financial insecurity by ethnicity and education, as a proxy for job worry | 0.3 (older adults; different construct) |
| IPS-CNA National Identity Survey (Working Paper 69) | Oct-Nov 2024 | 2,000 citizens and PRs 21-65, online, weighted | online panel | perceived impact of foreigners, by age | 0.3-0.35 |
| IPS Exchange 26, Future of Work | Oct 2022 | 1,010 economically active | online panel | job-change worry | 0.3 |
| Gallup World Poll (via World Happiness Report 2024 and Gallup safety release) | 2021-2024 | ~1,000/yr adults 15+, probability telephone | probability | life evaluation by age; feeling safe at night | 0.35-0.6 |
| Pew science fact sheet | Oct 2019-Mar 2020 | adults 18+ | probability | environment vs growth priority | 0.7 |
| Edelman Trust Barometer 2024 Singapore | Nov 2023 | ~1,150 adults, online | online panel | trust in media and government | 0.3 |
| Reuters Institute Digital News Report 2025 (YouGov) | Jan-Feb 2025 | 2,014 online adults | online panel | trust in news | 0.3 |
| YouGov Singapore, Jul 2025 | May-Jun 2025 | 4,035 adults, online panel with quotas | online panel | job security as a concern | 0.3 |
| Ipsos Global Advisor (Populism 2024; Happiness 2024) | Dec 2023; Dec 2023-Jan 2024 | ~500 adults 21-74, online, "connected segment" | online panel | strong-leader sentiment; happiness | 0.25-0.45 |
| Blackbox SensingSG (Apr 2025) | Mar-Apr 2025 | ~1,500 citizens and PRs 21+, online, weighting undocumented | opt-in | political interest by age | 0.25 |

How the confidence is used: each row contributes its sample size times its confidence as pseudo-respondents
to the matching question and group. Probability samples with near-identical wording get 0.7-0.9; the same
with different wording or a different year 0.4-0.6; opt-in online panels 0.25-0.5; social media is not used.

## Collected but not mapped (kept for later questions)

IPS WP59 cross-racial trust in a national crisis by age and education; IPS WP69 impact of new citizens by
income and education; Pew willingness to accept neighbours of other religions (94-100% yes across groups)
and "should people be able to criticise the government" by religion; General Household Survey 2025 religion
by ethnicity, age and education; Marriage and Parenthood Survey 2021 gender-role items; Ipsos Populism
immigration items (72% say employers should favour locals when jobs are scarce; 47% say immigrants take
jobs); ILO/UN Women 2019 attitudes to migrant workers (52% think they raise crime); YouGov 2025 election
sentiment by generation; Blackbox "right direction" series (84-90%); Reuters brand-level news trust.

## Checked and unusable (do not re-check)

IPS Exchange 16-18 and the 2021 TODAY/LKYSPP pieces (all re-report the WVS 2020 data we test on); IPS
Perceptions of Governance 2025 (voting choice only); POPS post-election surveys; MOH population health
surveys (no self-rated health item); MOM labour force report (no job-security measure); MSE Getting to Net
Zero (no trade-off item); Edelman 2025/2026 PDFs (blocked); Milieu Insight pages (blocked; numbers only
via search snippets); Forward Singapore report (no percentages); REACH (no recent releases with figures);
Kadence youth governance (n=250 with an interest screen); Reddit/HardwareZone corpus studies (non-probability,
directional only); Open Society Barometer (Singapore not included; a widely repeated "57% prefer democracy"
figure is a misattribution).

## Gaps

No non-WVS Singapore source was found for child-rearing values (obedience, independence), self-rated
health by ethnicity or income, neighbours who are immigrants or of a different language, or the WVS
"justifiable" morality scale (IPS Working Paper 66 on moral attitudes has related items by religion and age
and is the next thing to extract).
