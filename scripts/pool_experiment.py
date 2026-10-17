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


def main() -> None:
    country, packet_file, zs_file = "Singapore", "packet_wvs_singapore.json", "predictions_wvs_singapore_claude_in_session.json"
    t0 = time.time()
    bench = wvs.benchmark(country)
    packet = json.load(open(OUT / packet_file)); tg = [q["id"] for q in packet["questions"]]; groups = packet["groups"]
    zs = {(r["question_id"], r["group"]): r["probs"] for r in json.load(open(OUT / zs_file))}
    cache = OUT / f"record_all_{country.lower().replace(' ', '_')}_pred.json"
    if cache.exists():
        rec = {(r["question_id"], r["group"]): r["probs"] for r in json.loads(cache.read_text())}
        print("loaded cached record-anchored predictions", flush=True)
    else:
        others = [wvs.benchmark(n, segment_keys=["sex"]) for n in sorted(wvs.available_countries()) if n != country]
        print(f"{len(others)} other countries, {sum(len(b.respondents) for b in others):,} respondents", flush=True)
        rec = cross_country_transfer(others, bench, tg, DEMO, groups)
        cache.write_text(json.dumps([{"question_id": q, "group": g, "probs": p} for (q, g), p in rec.items()]))
    sources = {"claude zero-shot": zs, "record-anchored citizens": rec}
    design = sys.argv[1] if len(sys.argv) > 1 else "total"
    res = loo_bayes_evaluate(bench, sources, groups, local_n=(0, 150, 300, 600) if design == "total" else (0, 25, 50, 100), design=design, draws=3)
    s = res["scored"]
    order = list(dict.fromkeys(s.method))
    tab = s[s.level == "segment"].groupby("method").mae_pts.agg(["median", "mean"]).reindex(order)
    pop = s[s.level == "population"].groupby("method").mae_pts.agg(["median", "mean"]).reindex(order)
    seg = res["segment"].groupby("method")[["gap_r", "gap_slope", "dispersion_ratio"]].median().reindex(order)
    summary = pd.concat([pop.add_prefix("pop_"), tab.add_prefix("seg_"), seg], axis=1).round(2).reset_index()
    al = res["alphas"].groupby("local_n")[["claude zero-shot", "record-anchored citizens"]].median().round(1).reset_index()
    lines = [f"# Bayesian pooling, {country} ({len(tg)} questions x {len(groups)} groups), leave-one-question-out, design = {design}", "",
             f"Generated {time.strftime('%Y-%m-%d %H:%M')} UTC; runtime {time.time()-t0:.0f}s.", "",
             "Design 'total' = one local survey of n respondents, each group gets whoever fell into it (realistic); 'per_group' = n from each group. Errors in points per answer option, average of 3 draws.", "",
             H.to_markdown(summary), "", "Fitted source weights (worth in respondents, median over folds), by local sample size:", "", H.to_markdown(al), ""]
    (OUT / f"bayes_pooling_{country.lower().replace(' ', '_')}_{design}.md").write_text("\n".join(lines))
    summary.to_csv(OUT / f"bayes_pooling_{country.lower().replace(' ', '_')}_{design}.csv", index=False)
    print("\n".join(lines))


if __name__ == "__main__":
    main()
