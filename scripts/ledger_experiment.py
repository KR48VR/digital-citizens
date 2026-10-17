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
    rec = {(r["question_id"], r["group"]): r["probs"] for r in json.loads((OUT / "record_all_singapore_pred.json").read_text())}
    sources = {"claude zero-shot": zs, "record-anchored citizens": rec}
    real = {k: d.normalised() for k, d in bench.real.items() if k[1] in groups}
    # weights learned on all 20 questions with no local data (prior-only regime)
    cells = [({s: sources[s][k] for s in sources}, real[k], None) for k in real if all(k in sources[s] for s in sources)]
    alphas = fit_alphas(cells, list(sources))
    prior = {k: pool({s: sources[s][k] for s in sources}, alphas).tolist() for k in real if all(k in sources[s] for s in sources)}
    counts = L.ledger_counts(led, bench, reference=prior)
    cov = L.coverage(led, bench, groups)
    covered = [k for k in counts if k in real and k in prior]
    variants = {
        "pooled prior (no local evidence)": {k: prior[k] for k in covered},
        "pooled prior + ledger evidence": {k: pool({s: sources[s][k] for s in sources}, alphas, counts[k]).tolist() for k in covered},
        "ledger evidence alone": {k: (counts[k] / counts[k].sum()).tolist() if counts[k].sum() > 0 else prior[k] for k in covered},
        "everyone is average (real level)": {k: real[(k[0], "ALL")] for k in covered if (k[0], "ALL") in real},
    }
    scored = pd.concat([H.score(v, bench, n) for n, v in variants.items()], ignore_index=True)
    summ = scored.groupby("method")[["mae_pts", "jsd"]].agg(["median", "mean"]).round(2)
    summ.columns = ["_".join(c) for c in summ.columns]
    percell = scored.pivot_table(index=["question_id", "group"], columns="method", values="mae_pts").round(1).reset_index()
    lines = [f"# Ledger experiment: Singapore published evidence vs WVS-7 ({len(covered)} cells covered out of {len(real)})", "",
             f"Ledger rows: {len(led)}; rows mapped to tested questions: {int((led['maps_to'].isin(tg)).sum())}. Weights: " + ", ".join(f"{k} = {v:.1f}" for k, v in alphas.items()), "",
             "## Error on covered cells (points per answer option)", "", H.to_markdown(summ.reset_index()), "",
             "## Per cell", "", H.to_markdown(percell, 1), "",
             "## Coverage by question", "", H.to_markdown(cov[cov.rows > 0]), ""]
    (OUT / "ledger_experiment_singapore.md").write_text("\n".join(lines))
    scored.to_csv(OUT / "ledger_experiment_singapore_cells.csv", index=False)
    print("\n".join(lines))


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "data/ledger/singapore.csv")
