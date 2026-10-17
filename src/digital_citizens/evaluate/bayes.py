"""Bayesian pooling of evidence for one answer distribution ("superforecasting for surveys").

Every estimate of how a group answers a question is treated as a forecaster with a track record:
- a simulator's prediction (LLM zero-shot, record-anchored citizens, other countries' average, last
  wave, a published crosstab from a local report) contributes a Dirichlet prior with concentration
  alpha_s * p_s, where alpha_s is that source's learned "worth in respondents";
- real local answers (a small sample, or a published count) contribute multinomial counts.

Posterior mean = (sum_s alpha_s * p_s + n * p_sample) / (sum_s alpha_s + n).

alphas are fitted on calibration questions (leave-one-question-out in ``loo_bayes_evaluate``) by
minimising the error of the posterior mean, so a source that has been wrong gets little weight and
a source that has been right behaves like a larger sample. As local data accumulates (n grows) the
prior fades out, which is exactly the behaviour wanted when a country or city gets its own surveys.
"""
from __future__ import annotations

from collections.abc import Mapping, Sequence

import numpy as np
import pandas as pd
from scipy.optimize import minimize

from ..data.benchmark import Benchmark, Key
from ..schema import Distribution
from . import harness as H
from . import metrics as M


def _norm(p: Sequence[float]) -> np.ndarray:
    a = np.clip(np.asarray(p, float), 0, None)
    return a / a.sum() if a.sum() > 0 else np.full(len(a), 1 / len(a))


def pool(sources: Mapping[str, Sequence[float]], alphas: Mapping[str, float], counts: Sequence[float] | None = None) -> np.ndarray:
    """Posterior mean of the answer shares given weighted prior sources and optional real counts."""
    k = len(next(iter(sources.values())))
    num = np.zeros(k)
    den = 0.0
    for name, p in sources.items():
        a = max(float(alphas.get(name, 0.0)), 0.0)
        num += a * _norm(p)
        den += a
    if counts is not None:
        c = np.asarray(counts, float)
        num += c
        den += c.sum()
    return num / den if den > 0 else np.full(k, 1 / k)


def fit_alphas(cells: Sequence[tuple[Mapping[str, Sequence[float]], Sequence[float], Sequence[float] | None]], names: Sequence[str], init: float = 50.0, cap: float = 5000.0) -> dict[str, float]:
    """Choose alphas (>= 0) minimising mean JSD between pooled estimate and real shares over calibration cells.

    ``cells`` is a list of (sources, real_probs, counts_or_None). Optimised in log space (alphas = exp(x)).
    The absolute scale of the alphas (how many respondents a source is worth) is only identified when
    some calibration cells carry real counts, so callers that will pool with local data must calibrate
    with local data of the same design (see ``loo_bayes_evaluate``). ``cap`` bounds runaway weights.
    """
    names = list(names)

    def loss(x: np.ndarray) -> float:
        al = {n: float(np.exp(v)) for n, v in zip(names, x)}
        return float(np.mean([M.jsd(_norm(real), pool(src, al, cnt)) for src, real, cnt in cells]))

    x0 = np.full(len(names), np.log(init))
    res = minimize(loss, x0, method="Nelder-Mead", options={"maxiter": 400, "xatol": 1e-3, "fatol": 1e-7})
    return {n: float(min(np.exp(v), cap)) for n, v in zip(names, res.x)}


def _gmask(df: pd.DataFrame, g: str) -> np.ndarray:
    return np.ones(len(df), bool) if g == "ALL" else (df[g.split("=", 1)[0]].astype(str) == g.split("=", 1)[1]).to_numpy()


def _draw_counts(df: pd.DataFrame, q: str, options: Sequence[str], groups: Sequence[str], design: str, n: int, rng: np.random.Generator, holdout: bool = False):
    """Simulate a local survey. design='per_group': n respondents from each group separately (optimistic).
    design='total': one survey of n respondents overall; each group gets whoever fell into it (realistic).

    With ``holdout=True`` also returns the weighted shares of the respondents NOT drawn, per group: the truth a
    fresh sample should be scored against, so the sample never overlaps the people it is compared with."""
    valid = df[q].notna().to_numpy()
    w = df["weight"].to_numpy() if "weight" in df.columns else np.ones(len(df))
    y = df[q].to_numpy()
    out: dict[str, np.ndarray] = {}
    truth: dict[str, list[float]] = {}
    taken = np.zeros(len(df), bool)
    if design == "total":
        take = rng.choice(np.where(valid)[0], size=min(n, int(valid.sum())), replace=False)
        taken[take] = True
        for g in groups:
            m = taken & _gmask(df, g)
            out[g] = np.array([float((y[m] == o).sum()) for o in options])
    else:
        for g in groups:
            idx = np.where(valid & _gmask(df, g))[0]
            take = rng.choice(idx, size=min(n, len(idx)), replace=False)
            taken[take] = True
            out[g] = np.array([float((y[take] == o).sum()) for o in options])
    if not holdout:
        return out
    for g in groups:
        h = valid & ~taken & _gmask(df, g)
        v = np.array([float(w[h][y[h] == o].sum()) for o in options])
        if v.sum() > 0:
            truth[g] = (v / v.sum()).tolist()
    return out, truth


def loo_bayes_evaluate(
    bench: Benchmark,
    source_preds: Mapping[str, Mapping[Key, Sequence[float]]],
    groups: Sequence[str],
    local_n: Sequence[int] = (0, 50, 100, 300),
    design: str = "total",
    seed: int = 0,
    draws: int = 3,
) -> dict[str, pd.DataFrame]:
    """Leave-one-question-out Bayesian pooling.

    For each held-out question and each local sample size n: source weights are fitted on the OTHER
    questions using simulated local samples of the same design and size (so the weights learn how many
    real answers each source is worth), then the held-out question's cells are estimated from the
    weighted sources plus a fresh local sample. Compared against the local sample alone and each source alone.
    """
    rng = np.random.default_rng(seed)
    real = {k: d.normalised() for k, d in bench.real.items() if k[1] in groups}
    names = list(source_preds)
    items = sorted({k[0] for k in real if all((k[0], "ALL") in source_preds[n] for n in names)})
    df = bench.respondents
    variants: dict[str, dict[Key, list[float]]] = {f"{n} alone": {} for n in names}
    for n in local_n:
        tag = "prior only (no local answers)" if n == 0 else f"pooled + local survey of {n}"
        variants[tag] = {}
        if n > 0:
            variants[f"local survey of {n} alone"] = {}
    fitted = []
    draw_sets: dict[tuple[str, int], tuple[dict, dict]] = {}
    for q in items:
        options = bench.qmap[q].options
        for n_loc in local_n:
            cal_cells = []
            for i in items:
                if i == q:
                    continue
                counts_i = _draw_counts(df, i, bench.qmap[i].options, groups, design, n_loc, rng) if n_loc > 0 else {}
                for g in groups:
                    key = (i, g)
                    if key in real and all(key in source_preds[s] for s in names):
                        cal_cells.append(({s: source_preds[s][key] for s in names}, real[key], counts_i.get(g) if n_loc > 0 else None))
            alphas = fit_alphas(cal_cells, names)
            fitted.append({"held_out": q, "local_n": n_loc, **alphas})
            tag = "prior only (no local answers)" if n_loc == 0 else f"pooled + local survey of {n_loc}"
            if n_loc == 0:
                for g in groups:
                    key = (q, g)
                    if key not in real or not all(key in source_preds[s] for s in names):
                        continue
                    src = {s: source_preds[s][key] for s in names}
                    variants[tag][key] = list(pool(src, alphas))
                    for s in names:
                        variants[f"{s} alone"][key] = list(_norm(source_preds[s][key]))
                continue
            # a fresh local sample per draw, scored against the respondents NOT in it; scores (not predictions) are averaged
            for d in range(draws):
                counts, truth_h = _draw_counts(df, q, options, groups, design, n_loc, rng, holdout=True)
                for g in groups:
                    key = (q, g)
                    if key not in real or g not in truth_h or not all(key in source_preds[s] for s in names):
                        continue
                    src = {s: source_preds[s][key] for s in names}
                    c = counts.get(g)
                    draw_sets.setdefault((tag, d), ({}, {}))
                    draw_sets[(tag, d)][0][key] = list(pool(src, alphas, c)); draw_sets[(tag, d)][1][key] = truth_h[g]
                    alone_tag = f"local survey of {n_loc} alone"
                    draw_sets.setdefault((alone_tag, d), ({}, {}))
                    draw_sets[(alone_tag, d)][0][key] = list(_norm(c) if c is not None and c.sum() > 0 else pool(src, alphas)); draw_sets[(alone_tag, d)][1][key] = truth_h[g]
    scored_parts = [H.score(v, bench, name) for name, v in variants.items() if v]
    seg_parts = [H.segment_fidelity(v, bench, name) for name, v in variants.items() if v]
    per_draw_scores, per_draw_segs = [], []
    for (name, d), (pred, truth_h) in draw_sets.items():
        b = Benchmark(name=bench.name, country=bench.country, questions=bench.questions, real={k: Distribution(question_id=k[0], group=k[1], probs=v, n=0) for k, v in truth_h.items()}, segment_keys=bench.segment_keys)
        per_draw_scores.append(H.score(pred, b, name)); per_draw_segs.append(H.segment_fidelity(pred, b, name))
    if per_draw_scores:
        ds = pd.concat(per_draw_scores, ignore_index=True)
        num = [c for c in ["jsd", "tv", "mae_pts", "top_box_err", "max_abs_err", "entropy_ratio", "wd", "representativeness"] if c in ds.columns]
        scored_parts.append(ds.groupby(["method", "question_id", "group"], as_index=False).agg({"k": "first", "ordinal": "first", "n_real": "first", **{c: "mean" for c in num}}))
        seg_parts.append(pd.concat(per_draw_segs, ignore_index=True).groupby(["method", "question_id"], as_index=False).agg({"n_segments": "first", "gap_r": "mean", "gap_slope": "mean", "dispersion_ratio": "mean"}))
    scored = pd.concat(scored_parts, ignore_index=True)
    scored = scored[scored.group.isin(groups)]
    scored["level"] = np.where(scored.group == "ALL", "population", "segment")
    seg = pd.concat(seg_parts, ignore_index=True)
    return {"scored": scored, "segment": seg, "alphas": pd.DataFrame(fitted)}
