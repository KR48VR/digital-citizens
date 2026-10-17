"""World Values Survey wave 7 (2017-2022) country files: Singapore 2020, China 2018, United States 2017.

Files come from scripts/download_wvs.py (WVS site, no login; WVS terms of use apply: research use, cite
the WVS, do not redistribute the microdata). Each country has a numeric CSV (codes) and a text CSV
(labels) with identical row order; we zip them to get option labels in code order. Question wording comes
from the WVS7 codebook (``wvs7_wording.json``, extracted from the Singapore results book; the master
questionnaire is the same across countries).

Segments available in all three countries: sex, age band, education (3), income (3), religion, ethnic
group (country-specific), marital status, employment, urban/rural (not Singapore, which is all urban).
Weights: W_WEIGHT.
"""
from __future__ import annotations

import glob
import json
import re
from pathlib import Path

import numpy as np
import pandas as pd

from ..schema import Distribution, Persona, Question
from .benchmark import Benchmark

RAW = Path("data/raw/wvs")
WORDING = json.loads((Path(__file__).parent / "wvs7_wording.json").read_text())
COUNTRY_FILES = {"Singapore": "Singapore", "China": "China", "United States": "United_States"}


def available_countries(raw: Path = RAW) -> dict[str, str]:
    """Country display name -> file tag, for every WVS7 country file present under data/raw/wvs."""
    out: dict[str, str] = dict(COUNTRY_FILES)
    for d in sorted(raw.glob("*WVS_Wave_7_*_Csv_v*")):
        m = re.search(r"WVS_Wave_7_(.+?)_Csv_v", d.name)
        if m and d.is_dir() and any(d.glob("*.csv")):
            tag = m.group(1)
            out.setdefault(tag.replace("_", " "), tag)
    return out

# Curated items (variable -> topic). Everything with >2 ordered codes is treated as ordinal unless listed in NOMINAL.
ITEMS: dict[str, str] = {
    "Q1": "values", "Q2": "values", "Q3": "values", "Q4": "values", "Q5": "values", "Q6": "values",
    "Q8": "children", "Q9": "children", "Q14": "children", "Q17": "children",
    "Q18": "neighbours", "Q19": "neighbours", "Q22": "neighbours",
    "Q29": "gender", "Q30": "gender", "Q33": "gender",
    "Q46": "wellbeing", "Q47": "wellbeing", "Q48": "wellbeing", "Q49": "wellbeing", "Q50": "wellbeing",
    "Q57": "trust", "Q58": "trust", "Q59": "trust", "Q60": "trust", "Q61": "trust", "Q62": "trust", "Q63": "trust",
    "Q64": "institutions", "Q65": "institutions", "Q66": "institutions", "Q69": "institutions", "Q70": "institutions", "Q71": "institutions", "Q72": "institutions", "Q73": "institutions", "Q76": "institutions",
    "Q106": "economy", "Q107": "economy", "Q108": "economy", "Q109": "economy", "Q110": "economy", "Q111": "environment",
    "Q121": "immigration", "Q122": "immigration", "Q126": "immigration", "Q130": "immigration",
    "Q131": "security", "Q142": "security", "Q144": "security",
    "Q158": "science", "Q163": "science",
    "Q164": "religion", "Q171": "religion", "Q173": "religion",
    "Q177": "morality", "Q180": "morality", "Q182": "morality", "Q184": "morality", "Q185": "morality", "Q186": "morality", "Q188": "morality", "Q195": "morality",
    "Q199": "politics", "Q209": "politics", "Q211": "politics", "Q222": "politics",
    "Q235": "politics", "Q236": "politics", "Q237": "politics", "Q238": "politics", "Q240": "politics",
    "Q250": "democracy", "Q252": "democracy", "Q253": "democracy", "Q254": "identity", "Q287": "class",
}
NOMINAL = {"Q57", "Q111", "Q8", "Q9", "Q14", "Q17", "Q18", "Q19", "Q22", "Q33", "Q173", "Q222"}
DEFAULT_SEGMENTS = ["sex", "age_band", "education3", "income3", "religion", "ethnic", "born_in_country", "urban_rural"]
RELIGION_SHORT = {"Do not belong to a denomination": "No religion", "Catholic (Roman/Greek/etc)": "Catholic", "Protestant": "Protestant", "Orthodox (Russian/Greek/etc.)": "Orthodox", "Jew": "Jewish", "Muslim": "Muslim", "Hindu": "Hindu", "Buddhist": "Buddhist", "Other Christian (Jehova witnesses, Mormons, etc.)": "Other Christian", "Other": "Other religion"}


def _tag(country: str) -> str:
    return available_countries().get(country) or COUNTRY_FILES.get(country) or country.replace(" ", "_")


def _read(country: str, kind: str) -> pd.DataFrame:
    tag = _tag(country)
    files = glob.glob(str(RAW / f"*{tag}_{kind}_v*" / "*.csv"))
    if not files:
        raise FileNotFoundError(f"no WVS {kind} file for {country}; run scripts/download_wvs.py")
    df = pd.read_csv(files[0], sep=";", index_col=False, low_memory=False, encoding="utf-8-sig")
    df.columns = [c.split(" ")[0] for c in df.columns]
    return df


def load_country(country: str) -> tuple[pd.DataFrame, pd.DataFrame]:
    num, txt = _read(country, "Csv"), _read(country, "CsvText")
    if num.shape != txt.shape:
        raise ValueError("numeric and text files differ in shape")
    return num, txt


def option_labels(num: pd.Series, txt: pd.Series) -> tuple[list[int], list[str]]:
    m = pd.DataFrame({"code": num, "label": txt.astype(str)})
    m = m[m["code"] >= 0].drop_duplicates("code").sort_values("code")
    return [int(c) for c in m["code"]], [l.strip() for l in m["label"]]


def _age_band(a: float) -> str:
    if pd.isna(a) or a < 0:
        return "NA"
    return "18-29" if a < 30 else "30-44" if a < 45 else "45-59" if a < 60 else "60+"


def _religion(label: str) -> str:
    m = re.search(r"\{([^}]+)\}", label)
    if m:
        return m.group(1).strip()
    return RELIGION_SHORT.get(label.strip(), label.strip())


def _ethnic(label: str) -> str:
    if not isinstance(label, str) or label.startswith("-"):
        return "NA"
    lab = label.split(": ", 1)[-1]
    return {"South Asian Indian, Pakistan, etc.": "Indian", "Caucasian white": "Others", "Eurasian": "Others", "Two plus, non-Hispanic": "Other, Non-Hispanic"}.get(lab, lab)


def load_respondents(country: str, items: list[str] | None = None) -> tuple[pd.DataFrame, dict[str, Question]]:
    num, txt = load_country(country)
    items = [i for i in (list(ITEMS) if items is None else items) if i in num.columns]
    out = pd.DataFrame(index=num.index)
    out["pid"] = [f"wvs7_{_tag(country)}_{i}" for i in range(len(num))]
    out["weight"] = num["W_WEIGHT"].astype(float)
    def col(var: str, fn, default: str = "NA") -> pd.Series:
        if var not in num.columns:
            return pd.Series(default, index=num.index)
        return fn(num[var], txt[var])

    out["sex"] = col("Q260", lambda n, t: t.astype(str).where(n >= 0, "NA"))
    out["age"] = col("Q262", lambda n, t: n.astype(float), default=float("nan"))
    out["age_band"] = out["age"].map(_age_band)
    out["education3"] = col("Q275R", lambda n, t: t.astype(str).where(n >= 0, "NA"))
    out["income3"] = col("Q288R", lambda n, t: t.astype(str).where(n >= 0, "NA"))
    out["religion"] = col("Q289", lambda n, t: t.astype(str).map(_religion).where(n >= 0, "NA"))
    out["ethnic"] = col("Q290", lambda n, t: t.map(_ethnic))
    out["born_in_country"] = col("Q263", lambda n, t: pd.Series(np.where(n == 1, "Born here", np.where(n == 2, "Immigrant", "NA")), index=n.index))
    out["marital"] = col("Q273", lambda n, t: t.astype(str).where(n >= 0, "NA"))
    out["employment"] = col("Q279", lambda n, t: t.astype(str).where(n >= 0, "NA"))
    out["urban_rural"] = col("H_URBRURAL", lambda n, t: t.astype(str).where(n >= 0, "NA"))
    out["region"] = col("N_REGION_WVS", lambda n, t: t.astype(str))
    questions: dict[str, Question] = {}
    for it in items:
        codes, labels = option_labels(num[it], txt[it])
        if len(codes) < 2:
            continue
        mapping = dict(zip(codes, labels))
        out[it] = num[it].map(lambda c: mapping.get(int(c)) if pd.notna(c) and c >= 0 else None)
        text = WORDING.get(it, f"WVS item {it}")
        questions[it] = Question(id=it, text=text, options=labels, ordinal=(it not in NOMINAL and len(labels) > 2), source=f"WVS7 {country}", topic=ITEMS.get(it))
    return out, questions


def _weighted_shares(answers: pd.Series, weights: pd.Series, options: list[str]) -> tuple[list[float], int]:
    m = answers.notna()
    if m.sum() == 0:
        return [float("nan")] * len(options), 0
    w, a = weights[m], answers[m]
    sums = [float(w[a == o].sum()) for o in options]
    tot = sum(sums)
    return ([s / tot for s in sums] if tot > 0 else [1 / len(options)] * len(options)), int(m.sum())


def benchmark(country: str, items: list[str] | None = None, segment_keys: list[str] | None = None, min_n: int = 30) -> Benchmark:
    df, qmap = load_respondents(country, items)
    seg_keys = [k for k in (DEFAULT_SEGMENTS if segment_keys is None else segment_keys) if df[k].nunique() > 1]
    real = {}
    for it, q in qmap.items():
        probs, n = _weighted_shares(df[it], df["weight"], q.options)
        if n >= min_n:
            real[(it, "ALL")] = Distribution(question_id=it, group="ALL", probs=probs, n=n)
        for key in seg_keys:
            for val, grp in df.groupby(key):
                if val == "NA":
                    continue
                probs, n = _weighted_shares(grp[it], grp["weight"], q.options)
                if n >= min_n:
                    real[(it, f"{key}={val}")] = Distribution(question_id=it, group=f"{key}={val}", probs=probs, n=n)
    return Benchmark(name=f"wvs7_{_tag(country).lower()}", country=country, questions=list(qmap.values()), real=real, respondents=df, segment_keys=seg_keys, notes="WVS wave 7 country file v5.1; weighted by W_WEIGHT; DK/NA treated as missing.")


def to_personas(df: pd.DataFrame, qmap: dict[str, Question], record_items: list[str], country: str) -> list[Persona]:
    cols = ["age", "sex", "ethnic", "religion", "education3", "income3", "marital", "employment", "born_in_country", "urban_rural", "region"]
    out = []
    for _, r in df.iterrows():
        attrs = {c: (int(r[c]) if c == "age" and pd.notna(r[c]) else r[c]) for c in cols if c in df.columns and r[c] != "NA"}
        rec = {qmap[it].text: str(r[it]) for it in record_items if it in df.columns and it in qmap and isinstance(r[it], str)}
        out.append(Persona(id=str(r["pid"]), country=country, attributes=attrs, record=rec, weight=float(r["weight"]), source="wvs7"))
    return out
