"""GlobalOpinionQA (Anthropic, 2023): WVS wave 7 + Pew Global Attitudes questions with per-country shares.

Each row has a question, an option list, and a dict country -> shares. We turn it into a Benchmark
whose groups are "country=<name>". Useful for level-1 (population) fidelity across many countries
at once, including the US, China and Singapore. Caveats: fielded 2017-2022; the answer shares are
public and may be in LLM training data (contamination), so use it as a floor, not a final exam.
"""
from __future__ import annotations

import ast
import re
from pathlib import Path

import pandas as pd

from ..schema import Distribution, Question
from .benchmark import Benchmark

DEFAULT_PATH = Path("data/raw/globalopinionqa/llm_global_opinions.parquet")
SCALE_WORDS = ("very", "somewhat", "agree", "important", "often", "never", "satisfied", "good", "bad", "much", "little", "strongly", "always", "sometimes", "fairly", "completely", "great deal", "quite")


def _parse_selections(s: str) -> dict[str, list[float]]:
    m = re.search(r"\{.*\}", s, flags=re.S)
    return ast.literal_eval(m.group(0)) if m else {}


def _looks_ordinal(options: list[str]) -> bool:
    opts = [o.lower() for o in options if "dk" not in o.lower() and "refused" not in o.lower()]
    if len(opts) < 3:
        return False
    return sum(any(w in o for w in SCALE_WORDS) for o in opts) >= max(2, len(opts) // 2)


def load(path: str | Path = DEFAULT_PATH) -> pd.DataFrame:
    df = pd.read_parquet(path)
    df["selections"] = df["selections"].map(_parse_selections)
    df["options"] = df["options"].map(ast.literal_eval)
    return df


def benchmark(countries: list[str], path: str | Path = DEFAULT_PATH, min_countries: int = 1, keep_dk: bool = True) -> Benchmark:
    """Questions answered in at least ``min_countries`` of ``countries``; groups are country=<name>.

    ``keep_dk=False`` drops the 'DK/Refused' option and renormalises (useful when the simulator
    never produces DK answers; but note humans do, and that gap is itself a finding).
    """
    df = load(path)
    questions: list[Question] = []
    real: dict[tuple[str, str], Distribution] = {}
    for i, row in df.iterrows():
        sel = {c: v for c, v in row["selections"].items() if c in countries}
        if len(sel) < min_countries:
            continue
        raw_options = list(row["options"])
        keep_idx = [j for j, o in enumerate(raw_options) if isinstance(o, str) and o.strip()]
        if len(keep_idx) < 2:
            continue
        options = [raw_options[j] for j in keep_idx]
        if len(keep_idx) != len(raw_options):  # drop blank/NaN options and their shares
            sel = {c: [v[j] for j in keep_idx] for c, v in sel.items() if len(v) == len(raw_options)}
            if len(sel) < min_countries:
                continue
        dk_idx = [j for j, o in enumerate(options) if "dk" in o.lower() or "refused" in o.lower()]
        if not keep_dk and dk_idx:
            keep = [j for j in range(len(options)) if j not in dk_idx]
            options = [options[j] for j in keep]
            sel = {c: [v[j] for j in keep] for c, v in sel.items()}
        qid = f"goqa_{i}"
        questions.append(
            Question(
                id=qid,
                text=str(row["question"]).strip(),
                options=options,
                ordinal=_looks_ordinal(options),
                source=f"GlobalOpinionQA/{row['source']}",
                metadata={"countries": sorted(sel)},
            )
        )
        for c, probs in sel.items():
            real[(qid, f"country={c}")] = Distribution(question_id=qid, group=f"country={c}", probs=[float(p) for p in probs], n=None)
    return Benchmark(
        name="globalopinionqa",
        country="multi",
        questions=questions,
        real=real,
        segment_keys=["country"],
        notes="Shares from WVS7/Pew GAS as packaged by Anthropic (2023). n per country not provided (typically ~1,000-2,000).",
    )


def other_countries_mean(df_or_bench: Benchmark, qid: str, exclude: str, all_countries: dict[str, list[float]]) -> list[float] | None:
    """Mean share vector across every other country that answered the question (a strong, cheap baseline)."""
    rows = [v for c, v in all_countries.items() if c != exclude]
    if not rows:
        return None
    k = len(rows[0])
    return [sum(r[j] for r in rows) / len(rows) for j in range(k)]
