"""Pick a short set of standard questions without using the target survey's own answers.

Association between every pair of questions is measured (Cramer's V) on other data: for Singapore, the World
Values Survey in ten other Asia-Pacific places; for the United States, the General Social Survey 2022. Questions
are then chosen greedily so that, together, they are as closely associated as possible with every other question
(each question counts by its strongest link to the chosen set). The order of choice is saved; the first K form the
K-question set used in scripts/one_method_experiment.py.

Writes docs/results/stress_test/standard_questions_<country>.json.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from digital_citizens.data import gss, wvs  # noqa: E402

OUT = Path("docs/results/stress_test")
NEIGHBOURS = ["Malaysia", "Indonesia", "Thailand", "Philippines", "Vietnam", "Japan", "South Korea", "Taiwan ROC", "Hong Kong SAR", "Australia"]


def cramers_v(a: pd.Series, b: pd.Series) -> float:
    ok = a.notna() & b.notna()
    if ok.sum() < 50:
        return 0.0
    t = pd.crosstab(a[ok], b[ok]).to_numpy().astype(float)
    if min(t.shape) < 2:
        return 0.0
    n = t.sum()
    expected = t.sum(1, keepdims=True) * t.sum(0, keepdims=True) / n
    chi2 = ((t - expected) ** 2 / np.where(expected > 0, expected, 1)).sum()
    return float(np.sqrt(chi2 / n / (min(t.shape) - 1)))


def greedy_order(df: pd.DataFrame, items: list[str], k_max: int = 25) -> list[str]:
    V = np.zeros((len(items), len(items)))
    for i in range(len(items)):
        for j in range(i + 1, len(items)):
            V[i, j] = V[j, i] = cramers_v(df[items[i]], df[items[j]])
    np.fill_diagonal(V, 1.0)
    chosen: list[int] = []
    cover = np.zeros(len(items))
    for _ in range(min(k_max, len(items))):
        gains = [(np.maximum(cover, V[c]).sum(), c) for c in range(len(items)) if c not in chosen]
        best = max(gains)[1]
        chosen.append(best)
        cover = np.maximum(cover, V[best])
    return [items[c] for c in chosen]


def main() -> None:
    country = sys.argv[1] if len(sys.argv) > 1 else "singapore"
    if country == "us":
        items = [q.id for q in gss.benchmark(2024).questions]
        df = gss.load_respondents(2022, items)
        items = [i for i in items if i in df.columns]
        source = "General Social Survey 2022"
    else:
        sg = wvs.benchmark("Singapore")
        items = [q.id for q in sg.questions if q.id in sg.respondents.columns]
        frames = [wvs.load_respondents(c, items)[0] for c in NEIGHBOURS]
        df = pd.concat([f[[i for i in items if i in f.columns]] for f in frames], ignore_index=True)
        items = [i for i in items if i in df.columns]
        source = "World Values Survey wave 7: " + ", ".join(NEIGHBOURS)
    order = greedy_order(df.astype("object"), items)
    tag = "us" if country == "us" else "singapore"
    json.dump({"source": source, "people": len(df), "order": order}, open(OUT / f"standard_questions_{tag}.json", "w"), indent=1)
    print(tag, len(df), "people;", "first 20:", order[:20])


if __name__ == "__main__":
    main()
