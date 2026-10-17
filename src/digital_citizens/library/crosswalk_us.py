"""Hand-checked crosswalk between World Values Survey wave 7 (United States, fielded 2017) items and
General Social Survey items that ask something similar.

Each pair maps both surveys' answer options onto a common coarse scale ("bins"). ``wvs_map`` / ``gss_map``
list, for each bin, the 0-based option indices that fall into it; options in neither bin are dropped and the
shares renormalised. ``quality`` is a judgement of how close the two questions are:

* exact  - same construct, near-identical wording and scale
* close  - same construct, different scale granularity or minor wording differences
* loose  - related construct, materially different wording or framing

The point of the crosswalk is not to claim the pairs are equivalent; it is to measure what using a 'closest
previous question' from a different survey costs, as a function of how close the match is.
"""
from __future__ import annotations

CONF_BINS = ["A great deal", "Some / quite a lot", "Little or none"]
CONF_WVS = [[0], [1], [2, 3]]
CONF_GSS = [[0], [1], [2]]
JUST3_WVS = [[0, 1, 2], [3, 4, 5, 6], [7, 8, 9]]  # 1-10 'never ... always justifiable' -> low / middle / high
TEN_LOW_MID_HIGH = [[0, 1, 2, 3], [4, 5], [6, 7, 8, 9]]
TEN_HALF = [[0, 1, 2, 3, 4], [5, 6, 7, 8, 9]]

PAIRS: list[dict] = [
    dict(wvs="Q57", gss="trust", label="Most people can be trusted", quality="exact", bins=["Most people can be trusted", "Need to be careful"], wvs_map=[[0], [1]], gss_map=[[0], [1]], ordinal=False),
    dict(wvs="Q166", gss="postlife", label="Believes in life after death", quality="exact", bins=["Yes", "No"], wvs_map=[[0], [1]], gss_map=[[0], [1]], ordinal=False),
    dict(wvs="Q46", gss="happy", label="Happiness", quality="close", bins=["Very happy", "Fairly happy", "Not happy"], wvs_map=[[0], [1], [2, 3]], gss_map=[[0], [1], [2]], ordinal=True),
    dict(wvs="Q47", gss="health", label="Self-rated health", quality="close", bins=["Good or better", "Fair", "Poor"], wvs_map=[[0, 1], [2], [3, 4]], gss_map=[[0, 1], [2], [3]], ordinal=True),
    dict(wvs="Q64", gss="conclerg", label="Confidence: churches / organized religion", quality="close", bins=CONF_BINS, wvs_map=CONF_WVS, gss_map=CONF_GSS, ordinal=True),
    dict(wvs="Q65", gss="conarmy", label="Confidence: armed forces / military", quality="close", bins=CONF_BINS, wvs_map=CONF_WVS, gss_map=CONF_GSS, ordinal=True),
    dict(wvs="Q66", gss="conpress", label="Confidence: the press", quality="close", bins=CONF_BINS, wvs_map=CONF_WVS, gss_map=CONF_GSS, ordinal=True),
    dict(wvs="Q67", gss="contv", label="Confidence: television", quality="close", bins=CONF_BINS, wvs_map=CONF_WVS, gss_map=CONF_GSS, ordinal=True),
    dict(wvs="Q73", gss="conlegis", label="Confidence: parliament / Congress", quality="close", bins=CONF_BINS, wvs_map=CONF_WVS, gss_map=CONF_GSS, ordinal=True),
    dict(wvs="Q77", gss="conbus", label="Confidence: major companies", quality="close", bins=CONF_BINS, wvs_map=CONF_WVS, gss_map=CONF_GSS, ordinal=True),
    dict(wvs="Q78", gss="confinan", label="Confidence: banks", quality="close", bins=CONF_BINS, wvs_map=CONF_WVS, gss_map=CONF_GSS, ordinal=True),
    dict(wvs="Q171", gss="attend", label="Religious attendance", quality="close", bins=["Weekly or more", "About monthly", "A few times a year", "Rarely or never"], wvs_map=[[0, 1], [2], [3, 4], [5, 6]], gss_map=[[6, 7, 8], [4, 5], [2, 3], [0, 1]], ordinal=True),
    dict(wvs="Q201", gss="news", label="Reads a newspaper", quality="close", bins=["Daily", "Weekly", "Less often or never"], wvs_map=[[0], [1], [2, 3, 4]], gss_map=[[0], [1, 2], [3, 4]], ordinal=True),
    dict(wvs="Q240", gss="polviews", label="Left-right / liberal-conservative", quality="close", bins=["Left / liberal", "Centre / moderate", "Right / conservative"], wvs_map=TEN_LOW_MID_HIGH, gss_map=[[0, 1, 2], [3], [4, 5, 6]], ordinal=True),
    dict(wvs="Q287", gss="class", label="Subjective social class", quality="close", bins=["Upper", "Middle", "Working", "Lower"], wvs_map=[[0], [1, 2], [3], [4]], gss_map=[[3], [2], [1], [0]], ordinal=True),
    dict(wvs="Q70", gss="conjudge", label="Confidence: courts / Supreme Court", quality="loose", bins=CONF_BINS, wvs_map=CONF_WVS, gss_map=CONF_GSS, ordinal=True),
    dict(wvs="Q71", gss="confed", label="Confidence: government / executive branch", quality="loose", bins=CONF_BINS, wvs_map=CONF_WVS, gss_map=CONF_GSS, ordinal=True),
    dict(wvs="Q75", gss="coneduc", label="Confidence: universities / education", quality="loose", bins=CONF_BINS, wvs_map=CONF_WVS, gss_map=CONF_GSS, ordinal=True),
    dict(wvs="Q165", gss="god", label="Believes in God", quality="loose", bins=["Believes", "Does not believe"], wvs_map=[[0], [1]], gss_map=[[2, 3, 4, 5], [0, 1]], ordinal=False),
    dict(wvs="Q50", gss="satfin", label="Satisfaction with household finances", quality="loose", bins=["Not satisfied", "Middling", "Satisfied"], wvs_map=TEN_LOW_MID_HIGH[:1] + [[4, 5, 6]] + [[7, 8, 9]], gss_map=[[2], [1], [0]], ordinal=True),
    dict(wvs="Q110", gss="getahead", label="Hard work vs luck gets you ahead", quality="loose", bins=["Hard work", "Both", "Luck / help"], wvs_map=TEN_LOW_MID_HIGH, gss_map=[[0], [1], [2]], ordinal=True),
    dict(wvs="Q106", gss="eqwlth", label="Reduce income differences vs incentives", quality="loose", bins=["More equal / government should act", "In between", "Incentives / government should not"], wvs_map=TEN_LOW_MID_HIGH, gss_map=[[0, 1, 2], [3], [4, 5, 6]], ordinal=True),
    dict(wvs="Q108", gss="helpnot", label="Government vs individual responsibility", quality="loose", bins=["Government should do more", "In between", "People / government does too much"], wvs_map=TEN_LOW_MID_HIGH, gss_map=[[0, 1], [2], [3, 4]], ordinal=True),
    dict(wvs="Q182", gss="homosex", label="Homosexuality acceptable", quality="loose", bins=["Wrong / never justified", "In between", "Acceptable"], wvs_map=JUST3_WVS, gss_map=[[0, 1], [2], [3]], ordinal=True),
    dict(wvs="Q186", gss="premarsx", label="Sex before marriage acceptable", quality="loose", bins=["Wrong / never justified", "In between", "Acceptable"], wvs_map=JUST3_WVS, gss_map=[[0, 1], [2], [3]], ordinal=True),
    dict(wvs="Q184", gss="abany", label="Abortion", quality="loose", bins=["Against", "For"], wvs_map=TEN_HALF, gss_map=[[1], [0]], ordinal=False),
    dict(wvs="Q188", gss="letdie1", label="Euthanasia", quality="loose", bins=["Against", "For"], wvs_map=TEN_HALF, gss_map=[[1], [0]], ordinal=False),
    dict(wvs="Q195", gss="cappun", label="Death penalty", quality="loose", bins=["Oppose", "Favor"], wvs_map=TEN_HALF, gss_map=[[1], [0]], ordinal=False),
    dict(wvs="Q131", gss="fear", label="Feels safe in neighbourhood", quality="loose", bins=["Feels safe", "Feels unsafe"], wvs_map=[[0, 1], [2, 3]], gss_map=[[1], [0]], ordinal=False),
    dict(wvs="Q126", gss="immcrime", label="Immigrants raise terrorism / crime risk", quality="loose", bins=["Agree", "Neither", "Disagree"], wvs_map=[[2], [1], [0]], gss_map=[[0, 1], [2], [3, 4]], ordinal=True),
    dict(wvs="Q122", gss="immjobs", label="Immigrants and jobs", quality="loose", bins=["Immigrants bad for jobs", "Neither", "Immigrants fine for jobs"], wvs_map=[[0], [1], [2]], gss_map=[[0, 1], [2], [3, 4]], ordinal=True),
]

# WVS items that are not in the curated wvs.ITEMS but are needed by the crosswalk
EXTRA_WVS_ITEMS = ["Q67", "Q75", "Q77", "Q78", "Q165", "Q166", "Q201"]


def by_wvs() -> dict[str, dict]:
    return {p["wvs"]: p for p in PAIRS}
