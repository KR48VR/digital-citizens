"""Re-check the 'small real survey' rows with an honest design.

The first version (docs/06, 'record_transfer_summary.csv') averaged five random samples' predictions before
scoring and scored them against a truth that included the sampled people, which flatters a small sample.
This script draws a fresh sample, scores it against the OTHER respondents, repeats, and averages scores.
Writes docs/results/stress_test/small_survey_holdout.md / .csv.
"""
from __future__ import annotations

import json
import sys
import time
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from digital_citizens.data import wvs  # noqa: E402
from digital_citizens.data.benchmark import Benchmark  # noqa: E402
from digital_citizens.evaluate import harness as H  # noqa: E402
from digital_citizens.evaluate.transfer import small_survey_holdout  # noqa: E402
from digital_citizens.schema import Distribution  # noqa: E402

OUT = Path("docs/results/stress_test")
DEMO = ["sex", "age_band", "education3", "income3", "religion", "born_in_country"]


def bench_like(template: Benchmark, real: dict) -> Benchmark:
    return Benchmark(name=template.name, country=template.country, questions=template.questions, real={k: Distribution(question_id=k[0], group=k[1], probs=v, n=0) for k, v in real.items()}, segment_keys=template.segment_keys)


def main() -> None:
    t0 = time.time()
    rows = []
    for country, packet_file in [("Singapore", "packet_wvs_singapore.json"), ("China", "packet_wvs_china.json")]:
        bench = wvs.benchmark(country)
        packet = json.load(open(OUT / packet_file)); tg = [q["id"] for q in packet["questions"]]; groups = packet["groups"]
        for n_cal in (150, 300, 600):
            reps = small_survey_holdout(bench, tg, DEMO, groups, n_cal=n_cal, reps=5, min_n=30)
            for name in ["crosstab", "demographics model", "demographics + record model"]:
                ss, segs = [], []
                for r in reps:
                    b = bench_like(bench, r["truth"])
                    ss.append(H.score(r[name], b, name)); segs.append(H.segment_fidelity(r[name], b, name))
                s = pd.concat(ss); s = s[s.group.isin(groups)]
                seg = pd.concat(segs)
                pop, sg = s[s.group == "ALL"], s[s.group != "ALL"]
                rows.append({"country": country, "n_answers": n_cal, "method": {"crosstab": "small survey: read groups straight off it", "demographics model": "small survey + demographics-only spread", "demographics + record model": "small survey + record spread"}[name],
                             "pop_mae_median": pop.mae_pts.median(), "seg_mae_median": sg.mae_pts.median(), "seg_mae_mean": sg.mae_pts.mean(), "gap_r": seg.gap_r.median(), "gap_slope": seg.gap_slope.median(), "n_cells": len(s) // len(reps)})
    df = pd.DataFrame(rows).round(2)
    df.to_csv(OUT / "small_survey_holdout.csv", index=False)
    old = pd.read_csv(OUT / "record_transfer_summary.csv")
    old = old[old.exp == "sg_small_sample"]
    lines = ["# Small real survey, re-checked with a hold-out design", "", f"Generated {time.strftime('%Y-%m-%d %H:%M')} UTC; runtime {time.time()-t0:.0f}s.", "",
             "A fresh random sample of n respondents answers the question; the truth is computed on everyone else; 5 repeats; scores (not predictions) are averaged. "
             "Errors are mean absolute error per answer option, in points. Items and groups are the Singapore / China stress-test packets.", "",
             H.to_markdown(df, 2), "",
             "## What the first version reported for Singapore (n=300), and why it was too good", "",
             "The earlier rows averaged the five samples' predictions before scoring (so they behaved like one sample of 1,500) and scored them against a truth that included the sampled people:", "",
             H.to_markdown(old.drop(columns=["exp"]), 2), "",
             "The hold-out numbers above replace these in docs/06.", ""]
    (OUT / "small_survey_holdout.md").write_text("\n".join(lines))
    print("\n".join(lines))


if __name__ == "__main__":
    main()
