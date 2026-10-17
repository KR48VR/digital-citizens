"""US General Social Survey (NORC) loader: real respondents, exact question wording, weighted shares.

Why GSS: open download, 1972-2024, ~4,000 respondents per wave, hundreds of attitude items, full
demographics, survey weights. A respondent's row becomes a digital citizen anchored to a real
person's answers; the wave's weighted shares become ground truth for the population and for segments.

Wording below is taken from the GSS 2024 codebook. Option labels are the GSS value labels, lightly
cleaned for presentation (numeric scale points get their anchor text).
"""
from __future__ import annotations

import re
import warnings
from pathlib import Path

import numpy as np
import pandas as pd

from ..schema import Distribution, Persona, Question
from .benchmark import Benchmark

RAW = Path("data/raw/gss")

SPEND_STEM = (
    "We are faced with many problems in this country, none of which can be solved easily or inexpensively. "
    "I'm going to name some of these problems, and for each one I'd like you to tell me whether you think we're spending "
    "too much money on it, too little money, or about the right amount. Are we spending too much, too little, or about the right amount on: "
)
CONF_STEM = (
    "I am going to name some institutions in this country. As far as the people running these institutions are concerned, "
    "would you say you have a great deal of confidence, only some confidence, or hardly any confidence at all in them? "
)
AGREE4 = ["Strongly agree", "Agree", "Disagree", "Strongly disagree"]
WRONG4 = ["Always wrong", "Almost always wrong", "Wrong only sometimes", "Not wrong at all"]
SPEND3 = ["Too little", "About right", "Too much"]
CONF3 = ["A great deal", "Only some", "Hardly any"]

# var -> (question text, option labels in the file's category order, ordinal, topic)
ITEMS: dict[str, tuple[str, list[str], bool, str]] = {
    "happy": ("Taken all together, how would you say things are these days--would you say that you are very happy, pretty happy, or not too happy?", ["Very happy", "Pretty happy", "Not too happy"], True, "wellbeing"),
    "life": ("In general, do you find life exciting, pretty routine, or dull?", ["Exciting", "Pretty routine", "Dull"], True, "wellbeing"),
    "health": ("Would you say your own health, in general, is excellent, good, fair, or poor?", ["Excellent", "Good", "Fair", "Poor"], True, "wellbeing"),
    "satfin": ("We are interested in how people are getting along financially these days. So far as you and your family are concerned, would you say that you are pretty well satisfied with your present financial situation, more or less satisfied, or not satisfied at all?", ["Pretty well satisfied", "More or less satisfied", "Not satisfied at all"], True, "economy"),
    "finrela": ("Compared with American families in general, would you say your family income is far below average, below average, average, above average, or far above average?", ["Far below average", "Below average", "Average", "Above average", "Far above average"], True, "economy"),
    "class": ("If you were asked to use one of four names for your social class, which would you say you belong in: the lower class, the working class, the middle class, or the upper class?", ["Lower class", "Working class", "Middle class", "Upper class"], True, "economy"),
    "getahead": ("Some people say that people get ahead by their own hard work; others say that lucky breaks or help from other people are more important. Which do you think is most important?", ["Hard work most important", "Hard work and luck equally important", "Luck or help from others most important"], True, "values"),
    "trust": ("Generally speaking, would you say that most people can be trusted or that you can't be too careful in dealing with people?", ["Most people can be trusted", "Can't be too careful", "Depends"], False, "social"),
    "fear": ("Is there any area right around here--that is, within a mile--where you would be afraid to walk alone at night?", ["Yes", "No"], False, "crime"),
    "gunlaw": ("Would you favor or oppose a law which would require a person to obtain a police permit before he or she could buy a gun?", ["Favor", "Oppose"], False, "policy"),
    "owngun": ("Do you happen to have in your home (or garage) any guns or revolvers?", ["Yes", "No"], False, "behaviour"),
    "cappun": ("Do you favor or oppose the death penalty for persons convicted of murder?", ["Favor", "Oppose"], False, "policy"),
    "courts": ("In general, do you think the courts in this area deal too harshly or not harshly enough with criminals?", ["Too harshly", "Not harshly enough", "About right"], False, "policy"),
    "grass": ("Do you think the use of marijuana should be made legal or not?", ["Should be legal", "Should not be legal"], False, "policy"),
    "abany": ("Please tell me whether or not you think it should be possible for a pregnant woman to obtain a legal abortion if the woman wants it for any reason?", ["Yes", "No"], False, "policy"),
    "sexeduc": ("Would you be for or against sex education in the public schools?", ["For", "Against"], False, "policy"),
    "prayer": ("The United States Supreme Court has ruled that no state or local government may require the reading of the Lord's Prayer or Bible verses in public schools. What are your views on this--do you approve or disapprove of the court ruling?", ["Approve", "Disapprove"], False, "policy"),
    "letdie1": ("When a person has a disease that cannot be cured, do you think doctors should be allowed by law to end the patient's life by some painless means if the patient and his family request it?", ["Yes", "No"], False, "policy"),
    "suicide1": ("Do you think a person has the right to end his or her own life if this person has an incurable disease?", ["Yes", "No"], False, "values"),
    "divlaw": ("Should divorce in this country be easier or more difficult to obtain than it is now?", ["Easier", "More difficult", "Stay as is"], False, "policy"),
    "pornlaw": ("Which of these statements comes closest to your feelings about pornography laws?", ["There should be laws against the distribution of pornography whatever the age", "There should be laws against the distribution of pornography to persons under 18", "There should be no laws forbidding the distribution of pornography"], True, "policy"),
    "spanking": ("Do you strongly agree, agree, disagree, or strongly disagree that it is sometimes necessary to discipline a child with a good, hard spanking?", AGREE4, True, "values"),
    "homosex": ("What about sexual relations between two adults of the same sex--do you think it is always wrong, almost always wrong, wrong only sometimes, or not wrong at all?", WRONG4, True, "values"),
    "premarsx": ("If a man and a woman have sexual relations before marriage, do you think it is always wrong, almost always wrong, wrong only sometimes, or not wrong at all?", WRONG4, True, "values"),
    "xmarsex": ("What is your opinion about a married person having sexual relations with someone other than the marriage partner--is it always wrong, almost always wrong, wrong only sometimes, or not wrong at all?", WRONG4, True, "values"),
    "teensex": ("What about sexual relations before marriage for people in their early teens, say 14 to 16 years old? In that case, do you think sex relations before marriage are always wrong, almost always wrong, wrong only sometimes, or not wrong at all?", WRONG4, True, "values"),
    "pillok": ("Do you strongly agree, agree, disagree, or strongly disagree that methods of birth control should be available to teenagers between the ages of 14 and 16 if their parents do not approve?", AGREE4, True, "values"),
    "fefam": ("Please indicate whether you strongly agree, agree, disagree, or strongly disagree with the following statement: It is much better for everyone involved if the man is the achiever outside the home and the woman takes care of the home and family.", AGREE4, True, "values"),
    "fechld": ("To what extent do you agree or disagree: A working mother can establish just as warm and secure a relationship with her children as a mother who does not work.", AGREE4, True, "values"),
    "fepresch": ("Please indicate whether you strongly agree, agree, disagree, or strongly disagree with the following statement: A preschool child is likely to suffer if his or her mother works.", AGREE4, True, "values"),
    "discaffm": ("What do you think the chances are these days that a man won't get a job or promotion while an equally or less qualified woman gets one instead. Is this very likely, somewhat likely, somewhat unlikely, or very unlikely these days?", ["Very likely", "Somewhat likely", "Somewhat unlikely", "Very unlikely"], True, "values"),
    "wrkwayup": ("Do you agree strongly, agree somewhat, neither agree nor disagree, disagree somewhat, or disagree strongly with this statement: Irish, Italians, Jewish and many other minorities overcame prejudice and worked their way up. Black people should do the same without special favors.", ["Agree strongly", "Agree somewhat", "Neither agree nor disagree", "Disagree somewhat", "Disagree strongly"], True, "race"),
    "affrmact": ("Some people say that because of past discrimination, Black people should be given preference in hiring and promotion. Others say that such preference in hiring and promotion of Black people is wrong because it discriminates against white people. What about your opinion -- are you for or against preferential hiring and promotion of Black people?", ["Strongly for", "Not strongly for", "Not strongly against", "Strongly against"], True, "race"),
    "racdif1": ("On the average Black people have worse jobs, income, and housing than white people. Do you think these differences are mainly due to discrimination?", ["Yes", "No"], False, "race"),
    "helpblk": ("Some people think that Black people have been discriminated against for so long that the government has a special obligation to help improve their living standards. Others believe that the government should not be giving special treatment to Black people. Where would you place yourself on this scale?", ["1 - Government should help Black people", "2", "3 - Agree with both", "4", "5 - No special treatment"], True, "race"),
    "helppoor": ("Some people think that the government in Washington should do everything possible to improve the standard of living of all poor Americans; they are at Point 1 on this scale. Other people think it is not the government's responsibility, and that each person should take care of himself; they are at Point 5. Where would you place yourself on this scale, or haven't you made up your mind on this?", ["1 - Government should help", "2", "3 - Agree with both", "4", "5 - People should take care of themselves"], True, "policy"),
    "helpnot": ("Some people think that the government in Washington is trying to do too many things that should be left to individuals and private businesses. Others disagree and think that the government should do even more to solve our country's problems. Still others have opinions somewhere in between. Where would you place yourself on this scale?", ["1 - Government should do more", "2", "3 - Agree with both", "4", "5 - Government does too much"], True, "policy"),
    "helpsick": ("In general, some people think that it is the responsibility of the government in Washington to see to it that people have help in paying for doctors and hospital bills. Others think that these matters are not the responsibility of the federal government and that people should take care of these things themselves. Where would you place yourself on this scale?", ["1 - Government should help", "2", "3 - Agree with both", "4", "5 - People should take care of themselves"], True, "policy"),
    "eqwlth": ("Some people think that the government in Washington ought to reduce the income differences between the rich and the poor, perhaps by raising the taxes of wealthy families or by giving income assistance to the poor. Others think that the government should not concern itself with reducing this income difference between the rich and the poor. Think of a score of 1 as meaning that the government ought to reduce the income differences between rich and poor, and a score of 7 meaning that the government should not concern itself with reducing income differences. What score between 1 and 7 comes closest to the way you feel?", ["1 - Government should reduce income differences", "2", "3", "4", "5", "6", "7 - Government should not concern itself with reducing income differences"], True, "policy"),
    "natenvir": (SPEND_STEM + "Improving and protecting the environment", SPEND3, True, "spending"),
    "nateduc": (SPEND_STEM + "Improving the nation's education system", SPEND3, True, "spending"),
    "natcrime": (SPEND_STEM + "Halting the rising crime rate", SPEND3, True, "spending"),
    "natfare": (SPEND_STEM + "Welfare", SPEND3, True, "spending"),
    "natheal": (SPEND_STEM + "Improving and protecting the nation's health", SPEND3, True, "spending"),
    "natsci": (SPEND_STEM + "Supporting scientific research", SPEND3, True, "spending"),
    "natarms": (SPEND_STEM + "The military, armaments, and defense", SPEND3, True, "spending"),
    "natspac": (SPEND_STEM + "Space exploration program", SPEND3, True, "spending"),
    "natchld": (SPEND_STEM + "Assistance for childcare", SPEND3, True, "spending"),
    "natsoc": (SPEND_STEM + "Social Security", SPEND3, True, "spending"),
    "natenrgy": (SPEND_STEM + "Developing alternative energy sources", SPEND3, True, "spending"),
    "natdrug": (SPEND_STEM + "Dealing with drug addiction", SPEND3, True, "spending"),
    "natrace": (SPEND_STEM + "Improving the conditions of Black people", SPEND3, True, "spending"),
    "conmedic": (CONF_STEM + "Medicine", CONF3, True, "institutions"),
    "confinan": (CONF_STEM + "Banks and financial institutions", CONF3, True, "institutions"),
    "conpress": (CONF_STEM + "Press", CONF3, True, "institutions"),
    "conlegis": (CONF_STEM + "Congress", CONF3, True, "institutions"),
    "conarmy": (CONF_STEM + "Military", CONF3, True, "institutions"),
    "conbus": (CONF_STEM + "Major companies", CONF3, True, "institutions"),
    "conclerg": (CONF_STEM + "Organized religion", CONF3, True, "institutions"),
    "coneduc": (CONF_STEM + "Education", CONF3, True, "institutions"),
    "confed": (CONF_STEM + "Executive branch of the federal government", CONF3, True, "institutions"),
    "conjudge": (CONF_STEM + "U.S. Supreme Court", CONF3, True, "institutions"),
    "consci": (CONF_STEM + "Scientific community", CONF3, True, "institutions"),
    "contv": (CONF_STEM + "TV", CONF3, True, "institutions"),
    "immjobs": ("There are different opinions about immigrants from other countries living in America. How much do you agree or disagree with the following statement? Immigrants take jobs away from people who were born in America.", ["Agree strongly", "Agree", "Neither agree nor disagree", "Disagree", "Disagree strongly"], True, "immigration"),
    "immcrime": ("There are different opinions about immigrants from other countries living in America. How much do you agree or disagree with the following statement? Immigrants increase crime rates.", ["Agree strongly", "Agree", "Neither agree nor disagree", "Disagree", "Disagree strongly"], True, "immigration"),
    "letin1a": ("Do you think the number of immigrants to America nowadays should be increased a lot, increased a little, remain the same as it is, reduced a little, or reduced a lot?", ["Increased a lot", "Increased a little", "Remain the same as it is", "Reduced a little", "Reduced a lot"], True, "immigration"),
    "colath": ("Consider somebody who is against all churches and religion. Should such a person be allowed to teach in a college or university, or not?", ["Yes, allowed to teach", "Not allowed"], False, "civil_liberties"),
    "libath": ("Consider somebody who is against all churches and religion. If some people in your community suggested that a book he wrote against churches and religion should be removed from the library, would you favor removing this book, or not?", ["Remove", "Not remove"], False, "civil_liberties"),
    "spkrac": ("Consider a person who believes that Black people are genetically inferior. If such a person wanted to make a speech in your community claiming that Black people are inferior, should he be allowed to speak, or not?", ["Yes, allowed to speak", "Not allowed"], False, "civil_liberties"),
    "spkcom": ("Suppose an admitted Communist wanted to make a speech in your community. Should he be allowed to speak, or not?", ["Yes, allowed to speak", "Not allowed"], False, "civil_liberties"),
    "polhitok": ("Are there any situations you can imagine in which you would approve of a policeman striking an adult male citizen?", ["Yes", "No"], False, "policy"),
    "bible": ("Which of these statements comes closest to describing your feelings about the Bible?", ["The Bible is the actual word of God and is to be taken literally, word for word", "The Bible is the inspired word of God but not everything in it should be taken literally, word for word", "The Bible is an ancient book of fables, legends, history, and moral precepts recorded by men", "Other"], True, "religion"),
    "god": ("Which of the statements comes closest to expressing what you believe about God?", ["I don't believe in God", "I don't know whether there is a God and I don't believe there is any way to find out", "I don't believe in a personal God, but I do believe in a Higher Power of some kind", "I find myself believing in God some of the time, but not at others", "While I have doubts, I feel that I do believe in God", "I know God really exists and I have no doubts about it"], True, "religion"),
    "postlife": ("Do you believe there is a life after death?", ["Yes", "No"], False, "religion"),
    "attend": ("How often do you attend religious services?", ["Never", "Less than once a year", "About once or twice a year", "Several times a year", "About once a month", "2-3 times a month", "Nearly every week", "Every week", "Several times a week"], True, "religion"),
    "news": ("How often do you read the newspaper--every day, a few times a week, once a week, less than once a week, or never?", ["Every day", "A few times a week", "Once a week", "Less than once a week", "Never"], True, "media"),
    "socfrend": ("How often do you spend a social evening with friends who live outside the neighborhood?", ["Almost daily", "Once or twice a week", "Several times a month", "About once a month", "Several times a year", "About once a year", "Never"], True, "social"),
    "socbar": ("How often do you go to a bar or tavern?", ["Almost daily", "Once or twice a week", "Several times a month", "About once a month", "Several times a year", "About once a year", "Never"], True, "social"),
    "richwork": ("If you were to get enough money to live as comfortably as you would like for the rest of your life, would you continue to work or would you stop working?", ["Continue to work", "Stop working"], False, "work"),
    "union": ("Do you (or your spouse) belong to a labor union?", ["Yes, respondent belongs", "Yes, spouse belongs", "Yes, both belong", "No, neither belong"], False, "work"),
    "polviews": ("I'm going to show you a seven-point scale on which the political views that people might hold are arranged from extremely liberal--point 1--to extremely conservative--point 7. Where would you place yourself?", ["Extremely liberal", "Liberal", "Slightly liberal", "Moderate, middle of the road", "Slightly conservative", "Conservative", "Extremely conservative"], True, "politics"),
    "partyid": ("Generally speaking, do you usually think of yourself as a Republican, Democrat, Independent, or what?", ["Strong Democrat", "Not very strong Democrat", "Independent, close to Democrat", "Independent", "Independent, close to Republican", "Not very strong Republican", "Strong Republican", "Other party"], False, "politics"),
    "pres20": ("In the 2020 presidential election, did you vote for Joe Biden or Donald Trump?", ["Biden", "Trump", "Other candidate", "Didn't vote for president"], False, "politics"),
}
# category labels in the file that should be treated as missing for an item
DROP_CATEGORIES: dict[str, set[str]] = {"owngun": {"refused"}}

DEMO_COLS = ["age", "sex", "race", "hispanic", "degree", "region", "partyid", "polviews", "income16", "relig", "marital", "xnorcsiz", "wrkstat", "born"]
WEIGHT_COLS = ["wtssnrps", "wtssps"]
DEFAULT_SEGMENTS = ["age_band", "sex", "race_eth", "education", "region", "party3", "ideology3", "income4", "religion4", "urbanicity"]


def _age_band(a: float) -> str:
    if pd.isna(a):
        return "NA"
    return "18-29" if a < 30 else "30-44" if a < 45 else "45-64" if a < 65 else "65+"


def _income4(label: str) -> str:
    if not isinstance(label, str):
        return "NA"
    m = re.search(r"\$([\d,]+)", label)
    lo = int(m.group(1).replace(",", "")) if m else 0
    if label.startswith("under"):
        lo = 0
    return "<$25k" if lo < 25000 else "$25k-$59k" if lo < 60000 else "$60k-$109k" if lo < 110000 else "$110k+"


def _party3(label: str) -> str:
    if not isinstance(label, str):
        return "NA"
    if "democrat" in label:
        return "Democrat (incl. leaners)"
    if "republican" in label:
        return "Republican (incl. leaners)"
    return "Independent" if "independent" in label else "Other"


def _ideology3(label: str) -> str:
    if not isinstance(label, str):
        return "NA"
    return "Liberal" if "liberal" in label else "Conservative" if "conservative" in label else "Moderate"


def _education(label: str) -> str:
    if not isinstance(label, str):
        return "NA"
    return {"less than high school": "No high school diploma", "high school": "High school", "associate/junior college": "Some college / associate", "bachelor's": "Bachelor's or higher", "graduate": "Bachelor's or higher"}.get(label, label)


def _race_eth(race: str, hisp: str) -> str:
    if isinstance(hisp, str) and hisp != "not hispanic":
        return "Hispanic"
    if not isinstance(race, str):
        return "NA"
    return {"white": "White, non-Hispanic", "black": "Black, non-Hispanic"}.get(race, "Other, non-Hispanic")


def _religion4(label: str) -> str:
    if not isinstance(label, str):
        return "NA"
    return {"protestant": "Protestant", "catholic": "Catholic", "none": "No religion"}.get(label, "Other religion")


def _urbanicity(label: str) -> str:
    if not isinstance(label, str):
        return "NA"
    if "central city" in label and "suburb" not in label and "unincorporated" not in label:
        return "Large or medium city"
    if "suburb" in label or "unincorporated area of a large" in label or "unincorporated area of a medium" in label:
        return "Suburb"
    if "small city" in label or "town or village" in label:
        return "Small city or town"
    return "Rural"


def load_respondents(year: int = 2024, items: list[str] | None = None, raw: Path = RAW) -> pd.DataFrame:
    """One row per respondent: demographics, derived segments, weight, and item answers as option labels."""
    items = list(ITEMS) if items is None else items
    path = raw / f"GSS{year}.dta"
    cols = sorted(set(DEMO_COLS + WEIGHT_COLS + items))
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        with pd.io.stata.StataReader(path) as reader:
            available = set(reader.variable_labels())
        df = pd.read_stata(path, columns=[c for c in cols if c in available], convert_categoricals=True)
    out = pd.DataFrame(index=df.index)
    out["pid"] = [f"gss{year}_{i}" for i in range(len(df))]
    def _num(col: str) -> pd.Series:
        if col not in df:
            return pd.Series(np.nan, index=df.index)
        return pd.to_numeric(df[col].astype(str).str.replace(" or older", "", regex=False), errors="coerce")

    w = _num("wtssnrps").fillna(_num("wtssps"))
    out["weight"] = w.fillna(w.mean()).astype(float)
    out["age"] = _num("age")
    out["age_band"] = out["age"].map(_age_band)
    out["sex"] = df["sex"].astype(str).str.capitalize().replace({"Nan": "NA"})
    out["race_eth"] = [_race_eth(r, h) for r, h in zip(df["race"], df["hispanic"])]
    out["education"] = df["degree"].map(_education)
    out["region"] = df["region"].astype(str).str.capitalize().replace({"Nan": "NA"})
    out["party3"] = df["partyid"].map(_party3)
    out["ideology3"] = df["polviews"].map(_ideology3)
    out["income4"] = df["income16"].map(_income4)
    out["religion4"] = df["relig"].map(_religion4)
    out["marital"] = df["marital"].astype(str).str.capitalize().replace({"Nan": "NA"})
    out["urbanicity"] = df["xnorcsiz"].map(_urbanicity)
    out["work_status"] = df["wrkstat"].astype(str).replace({"nan": "NA"})
    out["born_in_us"] = df["born"].astype(str).map({"yes": "Yes", "no": "No"}).fillna("NA")
    for it in items:
        if it not in df:
            continue
        s = df[it]
        labels = ITEMS[it][1]
        if str(s.dtype) == "category":
            cats = [str(c) for c in s.cat.categories]
            drop = DROP_CATEGORIES.get(it, set())
            keep = [c for c in cats if c not in drop]
            if len(keep) != len(labels):
                raise ValueError(f"{it}: {len(keep)} categories in file vs {len(labels)} labels in ITEMS: {keep}")
            mapping = dict(zip(keep, labels))
            out[it] = s.astype(str).map(mapping)
        else:
            out[it] = s
    return out


def _weighted_shares(answers: pd.Series, weights: pd.Series, options: list[str]) -> tuple[list[float], int]:
    m = answers.notna()
    if m.sum() == 0:
        return [float("nan")] * len(options), 0
    w = weights[m]
    a = answers[m]
    sums = [float(w[a == o].sum()) for o in options]
    tot = sum(sums)
    return [s / tot for s in sums], int(m.sum())


def benchmark(year: int = 2024, items: list[str] | None = None, segment_keys: list[str] | None = None, min_n: int = 30, raw: Path = RAW) -> Benchmark:
    items = [i for i in (list(ITEMS) if items is None else items)]
    seg_keys = DEFAULT_SEGMENTS if segment_keys is None else segment_keys
    df = load_respondents(year, items, raw)
    items = [i for i in items if i in df.columns]
    questions = [Question(id=it, text=ITEMS[it][0], options=ITEMS[it][1], ordinal=ITEMS[it][2], source=f"GSS {year}", topic=ITEMS[it][3]) for it in items]
    real = {}
    for it in items:
        probs, n = _weighted_shares(df[it], df["weight"], ITEMS[it][1])
        if n >= min_n:
            real[(it, "ALL")] = Distribution(question_id=it, group="ALL", probs=probs, n=n)
        for key in seg_keys:
            for val, grp in df.groupby(key):
                if val == "NA":
                    continue
                probs, n = _weighted_shares(grp[it], grp["weight"], ITEMS[it][1])
                if n >= min_n:
                    g = f"{key}={val}"
                    real[(it, g)] = Distribution(question_id=it, group=g, probs=probs, n=n)
    return Benchmark(name=f"gss{year}", country="United States", questions=questions, real=real, respondents=df, segment_keys=list(seg_keys), notes="Weighted by wtssnrps (fallback wtssps); DK/refused treated as missing.")


def to_personas(df: pd.DataFrame, record_items: list[str], attribute_cols: list[str] | None = None) -> list[Persona]:
    """Turn respondents into digital citizens anchored to their real answers on ``record_items``."""
    attribute_cols = attribute_cols or ["age", "sex", "race_eth", "education", "region", "party3", "ideology3", "income4", "religion4", "marital", "urbanicity", "work_status"]
    out = []
    for _, r in df.iterrows():
        attrs = {c: (int(r[c]) if c == "age" and not pd.isna(r[c]) else r[c]) for c in attribute_cols if c in df.columns}
        rec = {ITEMS[it][0]: str(r[it]) for it in record_items if it in df.columns and isinstance(r[it], str)}
        out.append(Persona(id=str(r["pid"]), country="United States", attributes=attrs, record=rec, weight=float(r["weight"]), source="gss"))
    return out
