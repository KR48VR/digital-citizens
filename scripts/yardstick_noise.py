"""How far a perfect estimate would still score in the one-method test, from chance in the people checked against.

In scripts/one_method_experiment.py every estimate is scored against the respondents not drawn. They are a
sample too, so even the true population answer would not match them exactly. For each question and group this
works out the expected gap, per answer option, between the hold-out group's weighted shares and the population
shares: sqrt(2/pi) * sqrt(p(1-p) / n_eff), with n_eff = (sum w)^2 / sum w^2 for the group, scaled to the
hold-out (everyone minus a 300-person sample), and p taken from the full survey.

Writes docs/results/stress_test/yardstick_noise.md.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from digital_citizens.data import gss, wvs  # noqa: E402

OUT = Path("docs/results/stress_test")


def noise(bench, tg, groups, n_sample=300):
    df = bench.respondents
    w = df["weight"].to_numpy()
    vals = []
    for t in tg:
        y = df[t]
        valid = y.notna().to_numpy()
        opts = bench.qmap[t].options
        total = valid.sum()
        for g in groups:
            col, val = g.split("=", 1)
            m = valid & (df[col].astype(str) == val).to_numpy()
            if m.sum() < 30:
                continue
            ww = w[m]
            n_eff = ww.sum() ** 2 / (ww ** 2).sum() * (total - n_sample) / total
            p = np.array([ww[(y[m] == o).to_numpy()].sum() for o in opts])
            p = p / p.sum()
            vals.append(100 * np.mean(np.sqrt(2 / np.pi) * np.sqrt(p * (1 - p) / n_eff)))
    return float(np.median(vals)), float(np.mean(vals))


def main() -> None:
    rows = []
    p = json.load(open(OUT / "packet_wvs_singapore.json"))
    rows.append(("Singapore", *noise(wvs.benchmark("Singapore"), [q["id"] for q in p["questions"]], [g for g in p["groups"] if g != "ALL"])))
    p = json.load(open(OUT / "packet_gss.json"))
    rows.append(("United States", *noise(gss.benchmark(2024), [q["id"] for q in p["questions"]], [g for g in p["groups"] if g != "ALL"])))
    lines = ["# Chance in the yardstick of the one-method test", "",
             "Expected points off for a perfect estimate, because the people it is checked against are a sample too",
             "(hold-out = everyone minus a 300-person survey). Middle result over groups and questions (average).", "",
             "| country | middle result | average |", "|---|---|---|"]
    lines += [f"| {c} | {m:.2f} | {a:.2f} |" for c, m, a in rows]
    (OUT / "yardstick_noise.md").write_text("\n".join(lines) + "\n")
    print("\n".join(lines))


if __name__ == "__main__":
    main()
