"""United States: record citizens versus the chatbot, on the same 25 GSS 2024 questions and 7 groups.

The chatbot was scored on this packet earlier (docs/results/stress_test/README.md). Record citizens were
not, because the record method was first built on the World Values Survey, where the chatbot did well in
the US and the fixes were aimed at Singapore and China. This script fills that gap.

Record citizens here: each GSS 2024 respondent's answer to a question is predicted from their answers to
the other GSS questions plus demographics, with the mapping learned on GSS 2022 respondents (different
people, two years earlier). This is the US counterpart of learning the mapping from other countries.

Writes docs/results/stress_test/us_records_vs_chatbot.md / .csv.
"""
from __future__ import annotations

import json
import sys
import time
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from digital_citizens.data import gss  # noqa: E402
from digital_citizens.evaluate import harness as H  # noqa: E402
from digital_citizens.evaluate.calibrate import apply_gap_scale  # noqa: E402
from digital_citizens.evaluate.transfer import cross_country_transfer  # noqa: E402

OUT = Path("docs/results/stress_test")
DEMO = ["age_band", "sex", "race_eth", "education", "region", "income4", "religion4"]


def main() -> None:
    t0 = time.time()
    packet = json.load(open(OUT / "packet_gss.json"))
    tg = [q["id"] for q in packet["questions"]]; groups = packet["groups"]
    zs = {(r["question_id"], r["group"]): r["probs"] for r in json.load(open(OUT / "predictions_gss_claude_in_session.json"))}
    b24 = gss.benchmark(2024)
    b22 = gss.benchmark(2022, segment_keys=["sex"])
    real = {k: d.normalised() for k, d in b24.real.items()}
    rec = cross_country_transfer([b22], b24, tg, DEMO, groups, C=0.3, min_n=30)
    print(f"record citizens: {len(rec)} cells, {len({q for q, _ in rec})} questions", flush=True)
    variants = {
        "chatbot on its own": zs,
        "record citizens on their own (mapping from GSS 2022)": rec,
        "real overall number, every group the same": {(q, g): real[(q, "ALL")] for q in tg for g in groups if (q, g) in real},
        "real overall number + chatbot group differences": apply_gap_scale(zs, 1.0, tg, groups, base=real),
        "real overall number + record citizens' group differences": apply_gap_scale(rec, 1.0, tg, groups, base=real),
    }
    rows, cells = [], []
    for name, v in variants.items():
        s = H.score(v, b24, name); s = s[s.group.isin(groups) & s.question_id.isin(tg)]
        seg = H.segment_fidelity(v, b24.subset(tg), name)
        seg = seg[seg.question_id.isin(tg)]
        sg = s[s.group != "ALL"]
        rows.append({"method": name, "pop_median": s[s.group == "ALL"].mae_pts.median(), "seg_median": sg.mae_pts.median(), "seg_mean": sg.mae_pts.mean(),
                     "gap_r": seg.gap_r.median(), "gap_slope": seg.gap_slope.median(), "n_cells": len(sg)})
        cells.append(sg)
    df = pd.DataFrame(rows).round(2)
    df.to_csv(OUT / "us_records_vs_chatbot.csv", index=False)
    allc = pd.concat(cells)
    byg = allc.groupby(["group", "method"]).mae_pts.median().unstack("method")[list(variants)].round(1)
    lines = ["# United States: record citizens versus the chatbot (GSS 2024, 25 questions x 6 groups)", "", f"Generated {time.strftime('%Y-%m-%d %H:%M')} UTC; runtime {time.time()-t0:.0f}s.", "",
             "Same questions and groups the chatbot was scored on in the first stress test. Errors in points per answer option; `seg_median` is the typical group, `seg_mean` includes the big misses; `gap_slope` is the share of real group differences reproduced.", "",
             H.to_markdown(df, 2), "", "## By group (typical error, points)", "", H.to_markdown(byg.reset_index(), 1), ""]
    (OUT / "us_records_vs_chatbot.md").write_text("\n".join(lines))
    print("\n".join(lines))


if __name__ == "__main__":
    main()
