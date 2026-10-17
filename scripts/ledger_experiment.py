"""Does Singapore's own published evidence (the ledger) cut the error on matching questions?

For every (question, group) cell with ledger evidence: compare the pooled prior (Claude + record-anchored
citizens, weights learned on other questions) with the same prior updated by the ledger pseudo-counts,
and with the ledger evidence alone. Scored against WVS-7 Singapore real shares. Also reports coverage.
Usage: .venv/bin/python -I scripts/ledger_experiment.py data/ledger/singapore.csv
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from digital_citizens.data import ledger as L  # noqa: E402
from digital_citizens.data import wvs  # noqa: E402
from digital_citizens.evaluate import harness as H  # noqa: E402
from digital_citizens.evaluate.bayes import fit_alphas, pool  # noqa: E402

OUT = Path("docs/results/stress_test")


def main(ledger_path: str) -> None:
    led = L.load(ledger_path)
    bench = wvs.benchmark("Singapore")
    packet = json.load(open(OUT / "packet_wvs_singapore.json")); tg = [q["id"] for q in packet["questions"]]; groups = packet["groups"]
    zs = {(r["question_id"], r["group"]): r["probs"] for r in json.load(open(OUT / "predictions_wvs_singapore_claude_in_session.json"))}
    for extra in ["predictions_wvs_singapore_round2_zeroshot.json"]:
        if (OUT / extra).exists():
            zs.update({(r["question_id"], r["group"]): r["probs"] for r in json.load(open(OUT / extra))})
    rec: dict = {}
    for f in sorted(OUT.glob("record_all_singapore_pred*.json")):
        rec.update({(r["question_id"], r["group"]): r["probs"] for r in json.loads(f.read_text())})
    real = {k: d.normalised() for k, d in bench.real.items()}
    # source weights learned where both simulators exist (prior-only regime, all groups)
    both = [k for k in real if k in zs and k in rec]
    alphas = fit_alphas([({"claude zero-shot": zs[k], "record-anchored citizens": rec[k]}, real[k], None) for k in both], ["claude zero-shot", "record-anchored citizens"])
    a_rec = alphas["record-anchored citizens"]
    prior: dict = {}
    for k in real:
        if k in zs and k in rec:
            prior[k] = pool({"claude zero-shot": zs[k], "record-anchored citizens": rec[k]}, alphas).tolist()
        elif k in rec:
            prior[k] = list(np.asarray(rec[k], float) / np.sum(rec[k]))
    def prior_sources(k):
        return ({"claude zero-shot": zs[k], "record-anchored citizens": rec[k]}, alphas) if k in zs else ({"record-anchored citizens": rec[k]}, {"record-anchored citizens": a_rec})
    counts = L.ledger_counts(led, bench, reference=prior)
    cov = L.coverage(led, bench, groups)
    covered = [k for k in counts if k in real and k in prior]
    # Learn how much a published number is really worth: a global scale on the ledger pseudo-counts,
    # fitted leave-one-question-out (so each question's scale comes from the other questions).
    from digital_citizens.evaluate.metrics import jsd
    grid = [0.005, 0.01, 0.02, 0.03, 0.05, 0.075, 0.1, 0.15, 0.2, 0.3, 0.5, 0.75, 1.0]
    scaled: dict = {}
    fitted_scales = {}
    for q in sorted({k[0] for k in covered}):
        cal = [k for k in covered if k[0] != q]
        best, best_s = float("inf"), 0.0
        for sc in grid:
            err = np.mean([jsd(real[k], pool(*prior_sources(k), counts[k] * sc)) for k in cal])
            if err < best:
                best, best_s = err, sc
        fitted_scales[q] = best_s
        for k in covered:
            if k[0] == q:
                scaled[k] = pool(*prior_sources(k), counts[k] * best_s).tolist()
    variants = {
        "pooled prior (no local evidence)": {k: prior[k] for k in covered},
        "pooled prior + ledger evidence at face value": {k: pool(*prior_sources(k), counts[k]).tolist() for k in covered},
        "pooled prior + ledger evidence, learned weight": scaled,
        "ledger evidence alone": {k: (counts[k] / counts[k].sum()).tolist() if counts[k].sum() > 0 else prior[k] for k in covered},
        "everyone is average (real level)": {k: real[(k[0], "ALL")] for k in covered if (k[0], "ALL") in real},
    }
    scored = pd.concat([H.score(v, bench, n) for n, v in variants.items()], ignore_index=True)
    summ = scored.groupby("method")[["mae_pts", "jsd"]].agg(["median", "mean"]).round(2)
    summ.columns = ["_".join(c) for c in summ.columns]
    percell = scored.pivot_table(index=["question_id", "group"], columns="method", values="mae_pts").round(1).reset_index()
    by_item = scored[scored.method.isin(["pooled prior (no local evidence)", "pooled prior + ledger evidence at face value", "pooled prior + ledger evidence, learned weight"])].pivot_table(index="question_id", columns="method", values="mae_pts", aggfunc="mean").round(2).reset_index()
    # ledger-alone error by the confidence I assigned and by sampling type
    rows_tier = []
    for _, r in led.iterrows():
        k = (str(r["maps_to"]), str(r["group"]) or "ALL")
        if k in real:
            c = L.to_pseudocounts(r, bench.qmap[k[0]].k, np.asarray(prior.get(k)) if k in prior else None)
            if c.sum() > 0:
                rows_tier.append({"confidence": float(r["confidence"]), "sampling": r["sampling"], "mae_pts": 100 * float(np.mean(np.abs(c / c.sum() - np.asarray(real[k]))))})
    tier = pd.DataFrame(rows_tier)
    tier["tier"] = pd.cut(tier["confidence"], [0, 0.39, 0.69, 1.0], labels=["<0.4 (loose match)", "0.4-0.69", ">=0.7 (same wording)"])
    tier_tab = tier.groupby("tier", observed=True)["mae_pts"].agg(["count", "median", "mean"]).round(2).reset_index()
    samp_tab = tier.groupby("sampling")["mae_pts"].agg(["count", "median", "mean"]).round(2).reset_index()
    lines = [f"# Ledger experiment: Singapore published evidence vs WVS-7 ({len(covered)} cells covered; {len(set(k[0] for k in covered))} questions)", "",
             f"Learned weight on ledger evidence (leave-one-question-out, median over questions): {np.median(list(fitted_scales.values())):.3f} of face value (a published n of 1,000 is worth about {1000*np.median(list(fitted_scales.values())):.0f} respondents).", "",
             "## Ledger rows alone: error by the confidence assigned and by sampling type", "", H.to_markdown(tier_tab), "", H.to_markdown(samp_tab), "",
             f"Ledger rows: {len(led)}; cells with evidence: {len(counts)}; prior available for {len(prior)} cells. Weights: " + ", ".join(f"{k} = {v:.1f}" for k, v in alphas.items()), "",
             "## By question (mean error over covered cells)", "", H.to_markdown(by_item), "",
             "## Error on covered cells (points per answer option)", "", H.to_markdown(summ.reset_index()), "",
             "## Per cell", "", H.to_markdown(percell, 1), "",
             "## Coverage by question", "", H.to_markdown(cov[cov.rows > 0]), ""]
    (OUT / "ledger_experiment_singapore.md").write_text("\n".join(lines))
    scored.to_csv(OUT / "ledger_experiment_singapore_cells.csv", index=False)
    print("\n".join(lines))


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "data/ledger/singapore.csv")
