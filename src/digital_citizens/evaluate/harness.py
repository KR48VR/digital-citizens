"""Score predicted answer shares against a Benchmark and summarise fidelity at each level."""
from __future__ import annotations

import numpy as np
import pandas as pd

from ..data.benchmark import Benchmark, Key
from . import metrics as M


def score(pred: dict[Key, list[float]], bench: Benchmark, name: str = "pred") -> pd.DataFrame:
    """One row per (question, group) with distributional metrics. Missing predictions are skipped."""
    qmap = bench.qmap
    rows = []
    for key, d in bench.real.items():
        if key not in pred:
            continue
        q = qmap[key[0]]
        real, sim = d.normalised(), list(pred[key])
        if len(sim) != len(real):
            continue
        row = {
            "method": name,
            "question_id": key[0],
            "group": key[1],
            "k": q.k,
            "ordinal": q.ordinal,
            "n_real": d.n,
            "jsd": M.jsd(real, sim),
            "tv": M.total_variation(real, sim),
            "mae_pts": 100.0 * float(np.mean(np.abs(np.asarray(real) - np.asarray(sim)))),  # Pew-style: avg abs error per option, in points
            "top_box_err": M.top_box_error(real, sim, 0),
            "max_abs_err": float(np.max(np.abs(np.asarray(real) - np.asarray(sim)))),
            "entropy_ratio": M.entropy_ratio(sim, real),
        }
        if q.ordinal:
            row["wd"] = M.wasserstein_ordinal(real, sim)
            row["representativeness"] = M.representativeness(real, sim)
        rows.append(row)
    return pd.DataFrame(rows)


def noise_floor(bench: Benchmark, draws: int = 100, default_n: int | None = None) -> pd.DataFrame:
    """Expected JSD from survey sampling noise alone, per (question, group)."""
    rows = []
    for (qid, g), d in bench.real.items():
        n = d.n or default_n
        if not n:
            continue
        rows.append({"question_id": qid, "group": g, "n": n, "jsd_noise_floor": M.noise_floor_jsd(d.probs, n, draws)})
    return pd.DataFrame(rows)


def summarise(scored: pd.DataFrame, by: tuple[str, ...] = ("method",)) -> pd.DataFrame:
    cols = [c for c in ["jsd", "tv", "mae_pts", "top_box_err", "max_abs_err", "entropy_ratio", "wd", "representativeness"] if c in scored.columns]
    agg = scored.groupby(list(by))[cols].agg(["median", "mean"])
    agg.columns = [f"{a}_{b}" for a, b in agg.columns]
    agg["n_cells"] = scored.groupby(list(by)).size()
    return agg.reset_index()


def segment_fidelity(pred: dict[Key, list[float]], bench: Benchmark, name: str = "pred") -> pd.DataFrame:
    """Level-2 diagnostics per question: does the prediction reproduce how segments differ?

    gap_r / gap_slope: correlation and slope of predicted segment-minus-population gaps on real gaps.
    dispersion_ratio: Var(predicted segment summaries) / Var(real segment summaries); 1 = right spread.
    """
    rows = []
    for q in bench.questions:
        pop_key = (q.id, "ALL")
        if pop_key not in bench.real or pop_key not in pred:
            continue
        real_segs = {g: d.normalised() for g, d in bench.segments_for(q.id).items() if (q.id, g) in pred}
        if len(real_segs) < 3:
            continue
        sim_segs = {g: list(pred[(q.id, g)]) for g in real_segs}
        gr = M.gap_recovery(bench.real[pop_key].normalised(), real_segs, pred[pop_key], sim_segs)
        summ = M.mean_position if q.ordinal else (lambda p: M._norm(p)[0])
        disp = M.dispersion_ratio([summ(v) for v in real_segs.values()], [summ(v) for v in sim_segs.values()])
        rows.append({"method": name, "question_id": q.id, "n_segments": len(real_segs), "gap_r": gr["r"], "gap_slope": gr["slope"], "dispersion_ratio": disp})
    return pd.DataFrame(rows)


def to_markdown(df: pd.DataFrame, floatfmt: int = 3) -> str:
    d = df.copy()
    for c in d.columns:
        if pd.api.types.is_float_dtype(d[c]):
            d[c] = d[c].map(lambda v: "" if pd.isna(v) else f"{v:.{floatfmt}f}")
    cols = list(d.columns)
    lines = ["| " + " | ".join(cols) + " |", "|" + "|".join(["---"] * len(cols)) + "|"]
    for _, r in d.iterrows():
        lines.append("| " + " | ".join(str(r[c]) for c in cols) + " |")
    return "\n".join(lines)
