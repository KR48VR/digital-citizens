"""Twin-2K-500 (Toubia et al., 2025): 2,058 US panelists, ~500 items over 3 waves, plus a wave-4 retest.

We use it for level-3 (individual) validation under a leakage-free protocol:
- a twin is built from a person's wave 1-3 answers to OTHER items (the target item's own earlier
  answer is hidden), and must predict that person's wave-4 answer;
- the ceiling is the humans' own test-retest agreement (wave 1-3 answer vs wave-4 answer);
- the floors are: population modal answer, demographic-cell modal answer, and k-nearest-neighbour
  respondents (people who answered the other items most similarly).
"""
from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd

from ..schema import Persona, Question

DIR = Path("data/raw/twin2k")
DEMO_QIDS = {  # wave 1 demographics (QuestionIDs from the catalog) -> attribute name
    "QID11": "region", "QID12": "sex", "QID13": "age", "QID14": "education", "QID15": "race", "QID18": "religion", "QID20": "politics", "QID21": "income",
}


def load_catalog(path: Path = DIR / "question_catalog.json") -> dict[str, dict]:
    cat = json.loads(Path(path).read_text())
    entries = cat if isinstance(cat, list) else cat.get("questions", list(cat.values()))
    return {e["QuestionID"]: e for e in entries if isinstance(e, dict) and "QuestionID" in e}


def load_responses(dir_: Path = DIR) -> tuple[pd.DataFrame, pd.DataFrame]:
    w13 = pd.read_csv(dir_ / "wave1_3_response_label.csv", low_memory=False)
    w4 = pd.read_csv(dir_ / "wave4_response_label.csv", low_memory=False)
    return w13, w4


def categorical_columns(df: pd.DataFrame, max_levels: int = 9, min_valid: int = 500) -> list[str]:
    cols = []
    for c in df.columns:
        if c == "pid":
            continue
        s = df[c].dropna()
        if len(s) < min_valid:
            continue
        if pd.api.types.is_numeric_dtype(s) and s.nunique() > max_levels:
            continue
        if s.nunique() <= max_levels and s.nunique() >= 2:
            cols.append(c)
    return cols


def retest_items(w13: pd.DataFrame, w4: pd.DataFrame, max_levels: int = 9) -> list[str]:
    """Columns present in both waves with a small categorical answer set (the retest items)."""
    common = [c for c in w4.columns if c in w13.columns and c != "pid"]
    cat4 = set(categorical_columns(w4, max_levels))
    return [c for c in common if c in cat4]


def question_for(col: str, catalog: dict[str, dict], options: list[str]) -> Question:
    qid = col.split("_")[0]
    e = catalog.get(qid, {})
    text = (e.get("QuestionText") or "").strip()
    if "_" in col and e.get("Rows") and e.get("RowsID"):
        rid = col.split("_", 1)[1]
        try:
            text = text + " — " + e["Rows"][e["RowsID"].index(rid)]
        except (ValueError, IndexError):
            pass
    if not text:
        text = f"Item {col}"
    cols = e.get("Columns") or e.get("Options") or []
    ordered = [o for o in cols if o in options] + [o for o in options if o not in cols]
    return Question(id=col, text=text, options=ordered, ordinal=bool(e.get("Columns")), source="Twin-2K-500", metadata={"block": e.get("BlockName")})


def demographic_table(w13: pd.DataFrame) -> pd.DataFrame:
    cols = {q: name for q, name in DEMO_QIDS.items() if q in w13.columns}
    out = w13[["pid", *cols]].rename(columns=cols).copy()
    for c in cols.values():
        out[c] = out[c].astype(str)
    return out


def test_retest_accuracy(w13: pd.DataFrame, w4: pd.DataFrame, items: list[str]) -> pd.Series:
    acc = {}
    w13, w4 = w13.set_index("pid"), w4.set_index("pid")
    for c in items:
        a, b = w13[c].align(w4[c], join="inner")
        m = a.notna() & b.notna()
        acc[c] = float((a[m].astype(str) == b[m].astype(str)).mean()) if m.sum() else np.nan
    return pd.Series(acc, name="retest_accuracy")
