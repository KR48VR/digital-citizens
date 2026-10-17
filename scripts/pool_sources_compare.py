"""Small survey + AI, one method throughout: which AI does the work? (Singapore or the United States)

Runs the same leave-one-question-out pooling as pool_experiment.py, on the same survey draws (same seed),
with three choices of AI source: record citizens only, the chatbot kind only, and both. In every case the
group's own survey answers are blended with the AI estimate, each source counting by its track record.
Each survey sample is scored against the respondents not in it, and scores are averaged over draws.

Usage: pool_sources_compare.py [draws] [singapore|us]
Writes docs/results/stress_test/pool_sources_compare[_us].md / .csv / _cells.csv.
"""
from __future__ import annotations

import json
import sys
import time
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from digital_citizens.data import gss, wvs  # noqa: E402
from digital_citizens.evaluate.bayes import loo_bayes_evaluate  # noqa: E402
from digital_citizens.evaluate.transfer import cross_country_transfer  # noqa: E402

OUT = Path("docs/results/stress_test")
DEMO_US = ["age_band", "sex", "race_eth", "education", "region", "income4", "religion4"]
CONFIGS = {"record citizens only": ["record citizens"], "chatbot kind only": ["chatbot kind"],
           "record citizens + chatbot kind": ["record citizens", "chatbot kind"]}
SIZES = (150, 300, 600)


def _load(path: Path) -> dict:
    return {(r["question_id"], r["group"]): r["probs"] for r in json.load(open(path))}


def main() -> None:
    t0 = time.time()
    draws = int(sys.argv[1]) if len(sys.argv) > 1 else 5
    country = sys.argv[2] if len(sys.argv) > 2 else "singapore"
    if country == "us":
        packet = json.load(open(OUT / "packet_gss.json"))
        tg, groups = [q["id"] for q in packet["questions"]], packet["groups"]
        bench, b22 = gss.benchmark(2024), gss.benchmark(2022, segment_keys=["sex"])
        rec = cross_country_transfer([b22], bench, tg, DEMO_US, groups, C=0.3, min_n=30)
        all_sources = {"record citizens": rec, "chatbot kind": _load(OUT / "predictions_gss_claude_in_session.json")}
        title, suffix = "the United States", "_us"
    else:
        bench = wvs.benchmark("Singapore")
        groups = json.load(open(OUT / "packet_wvs_singapore.json"))["groups"]
        all_sources = {"record citizens": _load(OUT / "record_all_singapore_pred.json"),
                       "chatbot kind": _load(OUT / "predictions_wvs_singapore_claude_in_session.json")}
        title, suffix = "Singapore", ""
    # like for like: every run uses only the questions that every source covers
    common = set.intersection(*({q for q, _ in src} for src in all_sources.values()))
    all_sources = {n: {k: v for k, v in src.items() if k[0] in common} for n, src in all_sources.items()}
    rows, weights, cells = [], [], []
    for label, names in CONFIGS.items():
        res = loo_bayes_evaluate(bench, {n: all_sources[n] for n in names}, groups, local_n=SIZES, seed=0, draws=draws)
        s = res["scored"]
        s = s[s.level == "segment"]
        cells.append(s.assign(config=label))
        for n in SIZES:
            alone = s[s.method == f"local survey of {n} alone"].mae_pts
            pooled = s[s.method == f"pooled + local survey of {n}"].mae_pts
            rows.append({"config": label, "survey_n": n, "survey_alone_median": alone.median(),
                         "with_ai_median": pooled.median(), "survey_alone_mean": alone.mean(), "with_ai_mean": pooled.mean()})
        a = res["alphas"].groupby("local_n")[names].median()
        for n in SIZES:
            weights.append({"config": label, "survey_n": n, **{f"worth_{k}": round(float(a.loc[n, k]), 1) for k in names}})
        print(label, "done", f"{time.time() - t0:.0f}s", flush=True)
    tab = pd.DataFrame(rows)
    tab.to_csv(OUT / f"pool_sources_compare{suffix}.csv", index=False)
    pd.concat(cells).to_csv(OUT / f"pool_sources_compare{suffix}_cells.csv", index=False)
    w = pd.DataFrame(weights)
    lines = [f"# Small survey + AI in {title}: which AI does the work?", "",
             f"Generated {time.strftime('%Y-%m-%d %H:%M UTC', time.gmtime())}; runtime {time.time() - t0:.0f}s; {draws} draws, seed 0.", "",
             "Same survey draws for every row. Each group's survey answers are blended with the AI estimate(s),",
             "each counting by its track record. Points off per answer option for each group; middle result",
             "(average in brackets). Scored against the respondents not in the sample.", "",
             "| AI used | survey size | survey alone | survey + AI |", "|---|---|---|---|"]
    for r in rows:
        lines.append(f"| {r['config']} | {r['survey_n']} | {r['survey_alone_median']:.2f} ({r['survey_alone_mean']:.2f}) | "
                     f"{r['with_ai_median']:.2f} ({r['with_ai_mean']:.2f}) |")
    lines += ["", "Learned worth of each AI source, in real respondents per group (median over folds):", "",
              "| AI used | survey size | " + " | ".join(c for c in w.columns if c.startswith("worth_")) + " |",
              "|---|---|" + "---|" * sum(c.startswith("worth_") for c in w.columns)]
    for r in w.to_dict("records"):
        lines.append(f"| {r['config']} | {r['survey_n']} | " + " | ".join("" if pd.isna(r[c]) else str(r[c]) for c in w.columns if c.startswith("worth_")) + " |")
    (OUT / f"pool_sources_compare{suffix}.md").write_text("\n".join(lines) + "\n")
    print("\n".join(lines))


if __name__ == "__main__":
    main()
