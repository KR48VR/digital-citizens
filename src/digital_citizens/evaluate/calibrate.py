"""Calibration: correct a simulator's output with a small sample of real answers.

The documented failure is that simulated groups are too alike (gap slope < 1) and levels are biased.
Two cheap corrections, both fitted on a handful of *calibration* questions and applied to new ones:

- gap scaling: real_gap ~= a * simulated_gap, where gap = (group share - population share) per option.
  Fitted by least squares through the origin on the calibration questions; applied as
  corrected_group = base_population + a * (sim_group - sim_population). The base population can be
  the simulator's own population prediction (no human data for the new question) or the real population
  shares (when a small human sample exists for the question: "humans give the level, the model gives the
  differences").
- power sharpening/softening: p' ~ p ** t, with t chosen on calibration questions to minimise JSD. t < 1
  softens over-confident predictions (the model picked "very" too often in Singapore); t > 1 sharpens.

``loo_evaluate`` runs leave-one-question-out: every question is predicted with corrections fitted on the
others, so the reported gains are out-of-sample.
"""
from __future__ import annotations

from collections.abc import Mapping, Sequence

import numpy as np
import pandas as pd

from ..data.benchmark import Benchmark, Key
from . import harness as H
from . import metrics as M


def _norm(p: Sequence[float]) -> np.ndarray:
    a = np.clip(np.asarray(p, float), 0, None)
    return a / a.sum() if a.sum() > 0 else np.full(len(a), 1 / len(a))


def fit_gap_scale(pred: Mapping[Key, Sequence[float]], real: Mapping[Key, Sequence[float]], items: Sequence[str], groups: Sequence[str]) -> float:
    xs, ys = [], []
    for q in items:
        if (q, "ALL") not in pred or (q, "ALL") not in real:
            continue
        sp, rp = _norm(pred[(q, "ALL")]), _norm(real[(q, "ALL")])
        for g in groups:
            if g == "ALL" or (q, g) not in pred or (q, g) not in real:
                continue
            xs.extend((_norm(pred[(q, g)]) - sp).tolist())
            ys.extend((_norm(real[(q, g)]) - rp).tolist())
    x, y = np.asarray(xs), np.asarray(ys)
    return float((x * y).sum() / (x * x).sum()) if len(x) and (x * x).sum() > 0 else 1.0


def apply_gap_scale(pred: Mapping[Key, Sequence[float]], a: float, items: Sequence[str], groups: Sequence[str], base: Mapping[Key, Sequence[float]] | None = None) -> dict[Key, list[float]]:
    """Return corrected predictions for the given items. ``base`` supplies the population level (default: the simulator's)."""
    out: dict[Key, list[float]] = {}
    for q in items:
        if (q, "ALL") not in pred:
            continue
        sp = _norm(pred[(q, "ALL")])
        bp = _norm(base[(q, "ALL")]) if base and (q, "ALL") in base else sp
        out[(q, "ALL")] = bp.tolist()
        for g in groups:
            if g == "ALL" or (q, g) not in pred:
                continue
            out[(q, g)] = _norm(bp + a * (_norm(pred[(q, g)]) - sp)).tolist()
    return out


def fit_power(pred: Mapping[Key, Sequence[float]], real: Mapping[Key, Sequence[float]], keys: Sequence[Key], grid: Sequence[float] = tuple(np.round(np.arange(0.3, 2.05, 0.05), 2))) -> float:
    best, best_t = float("inf"), 1.0
    for t in grid:
        vals = [M.jsd(_norm(real[k]), _norm(pred[k]) ** t) for k in keys if k in pred and k in real]
        if vals and np.mean(vals) < best:
            best, best_t = float(np.mean(vals)), float(t)
    return best_t


def apply_power(pred: Mapping[Key, Sequence[float]], t: float) -> dict[Key, list[float]]:
    return {k: _norm(_norm(v) ** t).tolist() for k, v in pred.items()}


def loo_evaluate(pred: Mapping[Key, Sequence[float]], bench: Benchmark, groups: Sequence[str], name: str = "sim") -> dict[str, pd.DataFrame]:
    """Leave-one-question-out comparison of: raw simulator; power-calibrated; gap-scaled; gap-scaled on the
    real population level ('human level + model differences'); and the 'everyone is average' floor."""
    real = {k: d.normalised() for k, d in bench.real.items() if k[1] in groups}
    items = sorted({k[0] for k in real if (k[0], "ALL") in pred})
    variants: dict[str, dict[Key, list[float]]] = {f"{name} (raw)": {}, f"{name} + power": {}, f"{name} + gap scaling": {}, "human level + model differences (gap-scaled)": {}, "everyone is average (human level only)": {}}
    fitted = []
    for q in items:
        cal = [i for i in items if i != q]
        a = fit_gap_scale(pred, real, cal, groups)
        t = fit_power(pred, real, [(i, g) for i in cal for g in groups if (i, g) in pred and (i, g) in real])
        fitted.append({"held_out": q, "gap_scale_a": a, "power_t": t})
        raw = {(q, g): list(pred[(q, g)]) for g in groups if (q, g) in pred}
        variants[f"{name} (raw)"].update(raw)
        variants[f"{name} + power"].update(apply_power(raw, t))
        variants[f"{name} + gap scaling"].update(apply_gap_scale(pred, a, [q], groups))
        variants["human level + model differences (gap-scaled)"].update(apply_gap_scale(pred, a, [q], groups, base=real))
        variants["everyone is average (human level only)"].update({(q, g): list(real[(q, "ALL")]) for g in groups if (q, g) in real})
    scored = pd.concat([H.score(v, bench, n) for n, v in variants.items()], ignore_index=True)
    scored = scored[scored.group.isin(groups)]
    scored["level"] = np.where(scored.group == "ALL", "population", "segment")
    seg = pd.concat([H.segment_fidelity(v, bench, n) for n, v in variants.items()], ignore_index=True)
    return {"scored": scored, "segment": seg, "fitted": pd.DataFrame(fitted)}
