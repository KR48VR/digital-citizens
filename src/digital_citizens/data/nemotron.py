"""NVIDIA Nemotron-Personas loaders (Singapore, USA, ...): census-grounded synthetic persona skeletons.

These give a demographic *skeleton* plus LLM-written narrative. They contain no attitudes or
behaviour, so they cannot be ground truth; they are a starting population whose demographics
we can check and re-weight against official statistics, and then attach survey-anchored answers to.
"""
from __future__ import annotations

import re
from pathlib import Path

import numpy as np
import pandas as pd

from ..schema import Persona

SG_PATH = Path("data/raw/nemotron/Nemotron-Personas-Singapore-train-00000-of-00002.parquet")

# Singapore Department of Statistics, resident population by ethnic group, 2024 (Population in Brief 2024,
# rounded). Used only as a sanity check of the persona bank; replace with the exact table when you cite it.
SG_ETHNIC_TARGET_2024 = {"Chinese": 0.74, "Malay": 0.136, "Indian": 0.091, "Others": 0.033}

ATTR_COLS = ["sex", "age", "marital_status", "education_level", "occupation", "industry", "planning_area"]


def load(path: str | Path = SG_PATH, columns: list[str] | None = None) -> pd.DataFrame:
    return pd.read_parquet(path, columns=columns)


def infer_ethnicity(text: str) -> str:
    """Rough ethnicity tag from the cultural_background narrative (the dataset has no explicit field)."""
    t = (text or "").lower()
    hits = {
        "Chinese": any(w in t for w in ("chinese", "hokkien", "teochew", "cantonese", "hakka", "hainanese", "peranakan")),
        "Malay": any(w in t for w in ("malay", "javanese", "boyanese", "bugis")),
        "Indian": any(w in t for w in ("indian", "tamil", "punjabi", "sikh", "malayali", "telugu", "sindhi", "gujarati")),
        "Others": any(w in t for w in ("eurasian", "caucasian", "filipino", "burmese", "japanese", "korean", "thai", "vietnamese", "arab", "european")),
    }
    tagged = [k for k, v in hits.items() if v]
    if len(tagged) == 1:
        return tagged[0]
    if "Chinese" in tagged and "Malay" in tagged and "peranakan" in t:
        return "Chinese"
    return "Mixed/unclear" if len(tagged) > 1 else "Unknown"


def age_band(age: float) -> str:
    if age < 30:
        return "18-29"
    if age < 45:
        return "30-44"
    if age < 65:
        return "45-64"
    return "65+"


def to_personas(df: pd.DataFrame, country: str = "Singapore", narrative_cols: tuple[str, ...] = ("persona", "cultural_background"), weights: np.ndarray | None = None) -> list[Persona]:
    out = []
    for i, (_, r) in enumerate(df.iterrows()):
        attrs = {c: (int(r[c]) if c == "age" else str(r[c])) for c in ATTR_COLS if c in df.columns}
        if "age" in attrs:
            attrs["age_band"] = age_band(attrs["age"])
        if "cultural_background" in df.columns:
            attrs["ethnicity_inferred"] = infer_ethnicity(str(r["cultural_background"]))
        narrative = "\n".join(str(r[c]) for c in narrative_cols if c in df.columns and isinstance(r[c], str))
        out.append(Persona(id=str(r.get("uuid", i)), country=country, attributes=attrs, narrative=narrative, weight=float(weights[i]) if weights is not None else 1.0, source="nemotron"))
    return out


def demographic_report(df: pd.DataFrame) -> dict[str, dict[str, float]]:
    rep: dict[str, dict[str, float]] = {}
    for c in ["sex", "marital_status", "education_level", "industry"]:
        if c in df.columns:
            rep[c] = df[c].value_counts(normalize=True).round(4).to_dict()
    if "age" in df.columns:
        rep["age_band"] = df["age"].map(age_band).value_counts(normalize=True).round(4).to_dict()
    if "cultural_background" in df.columns:
        rep["ethnicity_inferred"] = df["cultural_background"].map(infer_ethnicity).value_counts(normalize=True).round(4).to_dict()
    return rep
