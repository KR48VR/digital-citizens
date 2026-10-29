"""Blending against correcting: two ways to use AI with a small survey, on the same Singapore draws.

Blending (the scorecard's method) leans each group's survey answer towards the AI's estimate, by a share earned on
other questions. Correcting (prediction-powered inference, as in the "participants saved" page) averages the AI's
guess for every person being estimated, then adds the average gap between the surveyed people's real answers and the
AI's guesses for them, so the AI can never tilt the answer; it can only cut the chance wobble.

Reads docs/results/stress_test/one_method_singapore_correction_cells.csv (scripts/one_method_experiment.py
singapore 10 correction) and writes docs/results/correction_vs_blending.{md,json}.
"""
from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd

RES = Path("docs/results")
CELLS = RES / "stress_test" / "one_method_singapore_correction_cells.csv"
SIZES = (150, 300, 600)
METHODS = [  # (label, config); the scorecard's advice is the blend with record citizens and the chatbot kind
    ("Survey alone", "survey alone"),
    ("Blend: record citizens", "+ record citizens (own survey)"),
    ("Correct: record citizens", "corrected, tuned: record citizens (own survey)"),
    ("Blend: chatbot reading records", "+ chatbot reading records"),
    ("Correct: chatbot reading records", "corrected, tuned: chatbot reading records"),
    ("Blend: record citizens + chatbot reading records", "+ record citizens (own survey) + chatbot reading records"),
    ("Correct: record citizens + chatbot reading records", "corrected, tuned: record citizens + chatbot reading records"),
    ("Blend: record citizens + chatbot (the scorecard's advice)", "+ record citizens (own survey) + chatbot kind"),
]


def saved(points: float, alone: dict[int, float]) -> float:
    """Share of participants saved at a survey of 300: the survey-alone size with the same points off, from the
    survey-alone curve (points off falls as a power of the number of people), against 300."""
    x, y = np.log(list(alone)), np.log([alone[n] for n in alone])
    slope, icept = np.polyfit(x, y, 1)
    n_equiv = float(np.exp((np.log(points) - icept) / slope))
    return 1 - 300 / n_equiv


def main() -> None:
    c = pd.read_csv(CELLS)
    per = c.groupby(["config", "n", "question_id", "group"], as_index=False).agg(mae=("mae_pts", "mean"), ng=("n_group", "mean"))
    med = {(cf, n): per[(per.config == cf) & (per.n == n)].mae.median() for _, cf in METHODS for n in SIZES}
    small = {cf: per[(per.config == cf) & (per.n == 300) & (per.ng < 100)].mae.median() for _, cf in METHODS}
    large = {cf: per[(per.config == cf) & (per.n == 300) & (per.ng >= 100)].mae.median() for _, cf in METHODS}
    alone = {n: med[("survey alone", n)] for n in SIZES}
    cmp = pd.read_csv(RES / "stress_test" / "one_method_singapore_correction_comparisons.csv")
    res = {"median": {lab: {n: med[(cf, n)] for n in SIZES} for lab, cf in METHODS},
           "small_groups_300": {lab: small[cf] for lab, cf in METHODS}, "large_groups_300": {lab: large[cf] for lab, cf in METHODS},
           "saved_at_300": {lab: saved(med[(cf, 300)], alone) for lab, cf in METHODS if cf != "survey alone"},
           "comparisons": cmp[cmp.a.str.startswith("corrected")].to_dict("records")}
    lines = ["# Blending against correcting (Singapore, the scorecard's test)", "",
             "Same 10 draws of 150, 300 and 600 people, same 20 questions and 9 groups, scored against the people not drawn.",
             "Median points off across groups and questions (lower is better). \"Participants saved\" is the share of a",
             "300-person survey you could drop and still match it with the survey alone, read off the survey-alone curve.", "",
             "| method | survey of 150 | survey of 300 | survey of 600 | participants saved at 300 |", "|---|---|---|---|---|"]
    for lab, cf in METHODS:
        sv = "" if cf == "survey alone" else f"{100 * res['saved_at_300'][lab]:.0f}%"
        lines.append(f"| {lab} | {med[(cf, 150)]:.2f} | {med[(cf, 300)]:.2f} | {med[(cf, 600)]:.2f} | {sv} |")
    lines += ["", "## By group size, survey of 300", "", "| method | groups under 100 people | groups of 100 or more |", "|---|---|---|"]
    lines += [f"| {lab} | {small[cf]:.2f} | {large[cf]:.2f} |" for lab, cf in METHODS]
    lines += ["", "## Key comparisons (difference in points off, first minus second; 95% range)", "",
              "| first | second | difference | 95% range |", "|---|---|---|---|"]
    lines += [f"| {r['a']}, {r['n_a']} | {r['b']}, {r['n_b']} | {r['difference']:+.2f} | {r['low']:+.2f} to {r['high']:+.2f} |" for r in res["comparisons"]]
    lines += ["", "Correcting is the tuned version (the AI's role shrinks when its guesses track answers loosely); the plain version",
              "is in the full results file. The chatbot kind guesses whole groups, not people, so it cannot be used to correct:",
              "with one guess per group, correcting gives back the survey alone.", "",
              "Code: scripts/one_method_experiment.py (correction design) and scripts/correction_vs_blending.py; full results:",
              "docs/results/stress_test/one_method_singapore_correction.md."]
    (RES / "correction_vs_blending.md").write_text("\n".join(lines) + "\n")
    (RES / "correction_vs_blending.json").write_text(json.dumps(res, indent=1, default=float))
    print("\n".join(lines))


if __name__ == "__main__":
    main()
