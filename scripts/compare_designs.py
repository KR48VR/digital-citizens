"""Boosted small groups against the normal design, from the saved one-method results.

Compares one_method_<country>_cells.csv (normal random survey) with one_method_<country>_boost_cells.csv (small
groups over-sampled and weighted back), for the typical group and for each group, with 95% intervals from
resampling questions (shared) and survey draws (separately per design, as they are different draws).

Writes docs/results/stress_test/boost_vs_standard.md.
"""
from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd

OUT = Path("docs/results/stress_test")
METHODS = ["survey alone", "+ record citizens (own survey) + chatbot kind"]
BOOSTED = {"singapore": "Malay and Indian Singaporeans, 20% of the sample each", "us": "Black adults, 30% of the sample"}


def cube(cells, config, n, group=None):
    c = cells[(cells.config == config) & (cells.n == n)]
    if group:
        c = c[c.group == group]
    return c.pivot_table(index=["question_id", "group"], columns="draw", values="mae_pts")


def boot_median_diff(a, b, B=1000, seed=1):
    """Middle result of A minus B, resampling questions jointly and draws separately."""
    rng = np.random.default_rng(seed)
    qs = sorted(set(a.index.get_level_values(0)) & set(b.index.get_level_values(0)))
    pa = {q: np.where(a.index.get_level_values(0) == q)[0] for q in qs}
    pb = {q: np.where(b.index.get_level_values(0) == q)[0] for q in qs}
    A, Bm = a.to_numpy(), b.to_numpy()
    point = np.nanmedian(np.nanmean(A, 1)) - np.nanmedian(np.nanmean(Bm, 1))
    out = []
    for _ in range(B):
        qi = rng.integers(0, len(qs), len(qs))
        ra = np.concatenate([pa[qs[i]] for i in qi]); rb = np.concatenate([pb[qs[i]] for i in qi])
        da = rng.integers(0, A.shape[1], A.shape[1]); db = rng.integers(0, Bm.shape[1], Bm.shape[1])
        out.append(np.nanmedian(np.nanmean(A[ra][:, da], 1)) - np.nanmedian(np.nanmean(Bm[rb][:, db], 1)))
    return point, np.percentile(out, 2.5), np.percentile(out, 97.5)


def main() -> None:
    lines = ["# Boosting small groups: boosted survey against a normal random survey of the same size", "",
             "Points off, middle result over questions (and groups, for the typical group). Difference = boosted minus",
             "normal; negative means boosting helped. 95% interval from resampling questions and survey draws.", ""]
    for tag, name in [("singapore", "Singapore"), ("us", "United States")]:
        std = pd.read_csv(OUT / f"one_method_{tag}_cells.csv")
        bst = pd.read_csv(OUT / f"one_method_{tag}_boost_cells.csv")
        lines += [f"## {name} (boosted: {BOOSTED[tag]}), survey of 300", "",
                  "| group | method | normal | boosted | difference (95% interval) |", "|---|---|---|---|---|"]
        for g in [None] + sorted(std.group.unique()):
            for m in METHODS:
                a, b = cube(bst, m, 300, g), cube(std, m, 300, g)
                d, lo, hi = boot_median_diff(a, b)
                nb = np.nanmedian(np.nanmean(b.to_numpy(), 1)); na = np.nanmedian(np.nanmean(a.to_numpy(), 1))
                lines.append(f"| {g or 'typical group'} | {m} | {nb:.2f} | {na:.2f} | {d:+.2f} ({lo:+.2f} to {hi:+.2f}) |")
        lines.append("")
    (OUT / "boost_vs_standard.md").write_text("\n".join(lines) + "\n")
    print("\n".join(lines))


if __name__ == "__main__":
    main()
