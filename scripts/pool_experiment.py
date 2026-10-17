"""Bayesian pooling experiment for Singapore: combine Claude zero-shot, record-anchored citizens (all
countries) and the other-countries average as weighted priors, then update with 0/50/100/300 local answers.
Leave-one-question-out throughout. Writes docs/results/stress_test/bayes_pooling_singapore.md/.csv."""
from __future__ import annotations

import json
import sys
import time
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from digital_citizens.data import wvs  # noqa: E402
from digital_citizens.evaluate import harness as H  # noqa: E402
from digital_citizens.evaluate.bayes import loo_bayes_evaluate  # noqa: E402
from digital_citizens.evaluate.transfer import cross_country_transfer  # noqa: E402

OUT = Path("docs/results/stress_test")
DEMO = ["sex", "age_band", "education3", "income3", "religion", "born_in_country"]


def main(country: str = "Singapore", packet_file: str = "packet_wvs_singapore.json", zs_file: str = "predictions_wvs_singapore_claude_in_session.json") -> None:
    t0 = time.time()
    bench = wvs.benchmark(country)
    packet = json.load(open(OUT / packet_file)); tg = [q["id"] for q in packet["questions"]]; groups = packet["groups"]
    zs = {(r["question_id"], r["group"]): r["probs"] for r in json.load(open(OUT / zs_file))}
    others = [wvs.benchmark(n, segment_keys=["sex"]) for n in sorted(wvs.available_countries()) if n != country]
    print(f"{len(others)} other countries, {sum(len(b.respondents) for b in others):,} respondents", flush=True)
    rec = cross_country_transfer(others, bench, tg, DEMO, groups)
    # other-countries average of the population shares, applied to every group (the cheap prior)
    om: dict = {}
    for q in tg:
        k = bench.qmap[q].k
        rows = [b.real[(q, "ALL")].normalised() for b in others if (q, "ALL") in b.real and b.qmap[q].k == k]
        if rows:
            m = np.mean(rows, axis=0).tolist()
            for g in groups:
                om[(q, g)] = m
    sources = {"claude zero-shot": zs, "record-anchored citizens": rec, "other countries' average": om}
    res = loo_bayes_evaluate(bench, sources, groups, local_n=(0, 50, 100, 300), draws=3)
    s = res["scored"]
    order = list(dict.fromkeys(s.method))
    tab = s[s.level == "segment"].groupby("method").mae_pts.agg(["median", "mean"]).reindex(order)
    pop = s[s.level == "population"].groupby("method").mae_pts.agg(["median", "mean"]).reindex(order)
    seg = res["segment"].groupby("method")[["gap_r", "gap_slope", "dispersion_ratio"]].median().reindex(order)
    summary = pd.concat([pop.add_prefix("pop_"), tab.add_prefix("seg_"), seg], axis=1).round(2).reset_index()
    summary.to_csv(OUT / f"bayes_pooling_{country.lower().replace(' ', '_')}.csv", index=False)
    al = res["alphas"][["claude zero-shot", "record-anchored citizens", "other countries' average"]].median().round(1)
    lines = [f"# Bayesian pooling, {country} ({len(tg)} questions x {len(groups)} groups), leave-one-question-out", "",
             f"Generated {time.strftime('%Y-%m-%d %H:%M')} UTC; runtime {time.time()-t0:.0f}s. Sources are weighted priors; weights (worth in respondents, median over folds): " + ", ".join(f"{k} = {v}" for k, v in al.items()) + ".", "",
             "Errors in points per answer option; 'local answers' are real respondents from the same group, drawn at random (average of 3 draws).", "",
             H.to_markdown(summary), ""]
    (OUT / f"bayes_pooling_{country.lower().replace(' ', '_')}.md").write_text("\n".join(lines))
    print("\n".join(lines))


if __name__ == "__main__":
    main(*sys.argv[1:])
