"""Most groups versus standout groups: how much error each kind of AI removes, compared with No AI.

Standout groups are, across all questions in a country, the quarter of group-by-question cells with the
largest No AI error (the group answers furthest from the national average). Most groups are the rest.
Within each set we report the middle result (median) and the average, and "less error" as
(No AI - method) / No AI, computed from unrounded medians.

Methods (each starts from the real overall answer, except No AI which stops there):
  noai      every group gets the real overall answer
  lvl+chat  real overall answer + the chatbot kind's group differences
  lvl+rec   real overall answer + record citizens' group differences

United States: 25 GSS 2024 questions x 6 groups; record citizens learned from GSS 2022.
Singapore: 20 WVS-7 questions x 9 groups; record citizens learned from 61 other countries.

Writes docs/results/stress_test/standout_split.md / .csv and standout_cells.csv.
"""
from __future__ import annotations

import json
import sys
import time
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from digital_citizens.data import gss, wvs  # noqa: E402
from digital_citizens.evaluate import harness as H  # noqa: E402
from digital_citizens.evaluate.calibrate import apply_gap_scale  # noqa: E402
from digital_citizens.evaluate.transfer import cross_country_transfer  # noqa: E402

OUT = Path("docs/results/stress_test")
DEMO_US = ["age_band", "sex", "race_eth", "education", "region", "income4", "religion4"]
METHODS = {"noai": "No AI", "lvl+chat": "with the chatbot kind", "lvl+rec": "with record citizens"}


def _load(path: Path) -> dict:
    return {(r["question_id"], r["group"]): r["probs"] for r in json.load(open(path))}


def _cells(bench, tg, groups, zs, rec, label):
    real = {k: d.normalised() for k, d in bench.real.items()}
    variants = {
        "noai": {(q, g): real[(q, "ALL")] for q in tg for g in groups if (q, g) in real},
        "lvl+chat": apply_gap_scale(zs, 1.0, tg, groups, base=real),
        "lvl+rec": apply_gap_scale(rec, 1.0, tg, groups, base=real),
    }
    out = []
    for name, v in variants.items():
        s = H.score(v, bench, name)
        s = s[s.group.isin(groups) & s.question_id.isin(tg) & (s.group != "ALL")]
        out.append(s.assign(country=label))
    return pd.concat(out)


def us_cells() -> pd.DataFrame:
    packet = json.load(open(OUT / "packet_gss.json"))
    tg, groups = [q["id"] for q in packet["questions"]], packet["groups"]
    zs = _load(OUT / "predictions_gss_claude_in_session.json")
    b24, b22 = gss.benchmark(2024), gss.benchmark(2022, segment_keys=["sex"])
    rec = cross_country_transfer([b22], b24, tg, DEMO_US, groups, C=0.3, min_n=30)
    return _cells(b24, tg, groups, zs, rec, "United States")


def sg_cells() -> pd.DataFrame:
    packet = json.load(open(OUT / "packet_wvs_singapore.json"))
    tg, groups = [q["id"] for q in packet["questions"]], packet["groups"]
    zs = _load(OUT / "predictions_wvs_singapore_claude_in_session.json")
    rec = _load(OUT / "record_all_singapore_pred.json")
    return _cells(wvs.benchmark("Singapore"), tg, groups, zs, rec, "Singapore")


def split(cells: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    rows, members = [], []
    for country, c in cells.groupby("country", sort=False):
        wide = c.pivot_table(index=["question_id", "group"], columns="method", values="mae_pts")
        n_top = round(len(wide) / 4)
        top = wide["noai"].sort_values(ascending=False).index[:n_top]
        wide["set"] = "most groups"
        wide.loc[top, "set"] = "standout groups"
        for s, w in wide.groupby("set"):
            base = w["noai"].median()
            row = {"country": country, "set": s, "cells": len(w)}
            for m in METHODS:
                row[f"{m}_median"] = round(w[m].median(), 2)
                row[f"{m}_mean"] = round(w[m].mean(), 2)
                if m != "noai":
                    row[f"{m}_less_error_pct"] = round(100 * (base - w[m].median()) / base, 1)
            rows.append(row)
        members.append(wide[wide.set == "standout groups"].reset_index().group.value_counts()
                       .rename_axis("group").reset_index(name="standout_cells").assign(country=country))
    return pd.DataFrame(rows), pd.concat(members)


def main() -> None:
    t0 = time.time()
    cells = pd.concat([us_cells(), sg_cells()])
    cells.to_csv(OUT / "standout_cells.csv", index=False)
    summary, members = split(cells)
    summary.to_csv(OUT / "standout_split.csv", index=False)
    lines = [
        "# Most groups versus standout groups",
        "",
        f"Generated {time.strftime('%Y-%m-%d %H:%M UTC', time.gmtime())}; runtime {time.time() - t0:.0f}s.",
        "",
        "Standout groups: across all questions in a country, the quarter of group answers furthest from the",
        "national average (largest No AI error). Most groups: the rest. Points off per answer option; the",
        "middle result within each set. Less error = (No AI - method) / No AI, from unrounded medians.",
        "",
        "| country | groups | cells | No AI | with the chatbot kind | with record citizens |",
        "|---|---|---|---|---|---|",
    ]
    for r in summary.to_dict("records"):
        def cell(m):
            pct = r[f"{m}_less_error_pct"]
            word = f"{pct:.0f}% less error" if pct >= 0 else f"{-pct:.0f}% more error"
            return f"{r[f'{m}_median']:.1f} ({word})"
        lines.append(f"| {r['country']} | {r['set']} | {r['cells']} | {r['noai_median']:.1f} | "
                     f"{cell('lvl+chat')} | {cell('lvl+rec')} |")
    lines += ["", "## Which groups land among the standout cells", "",
              "| country | group | standout cells (of one per question) |", "|---|---|---|"]
    for r in members.to_dict("records"):
        lines.append(f"| {r['country']} | {r['group']} | {r['standout_cells']} |")
    (OUT / "standout_split.md").write_text("\n".join(lines) + "\n")
    print("\n".join(lines))


if __name__ == "__main__":
    main()
