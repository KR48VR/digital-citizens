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


def _draw_counts(df: pd.DataFrame, q: str, options: Sequence[str], groups: Sequence[str], design: str, n: int, rng: np.random.Generator) -> dict[str, np.ndarray]:
    """Simulate a local survey. design='per_group': n respondents from each group separately (optimistic).
    design='total': one survey of n respondents overall; each group gets whoever fell into it (realistic)."""
    valid = df[q].notna().to_numpy()
    out: dict[str, np.ndarray] = {}
    if design == "total":
        take = rng.choice(np.where(valid)[0], size=min(n, int(valid.sum())), replace=False)
        sub = df.iloc[take]
        for g in groups:
            m = np.ones(len(sub), bool) if g == "ALL" else (sub[g.split("=", 1)[0]].astype(str) == g.split("=", 1)[1]).to_numpy()
            out[g] = np.array([float((sub[q][m] == o).sum()) for o in options])
        return out
    for g in groups:
        mask = valid if g == "ALL" else valid & (df[g.split("=", 1)[0]].astype(str) == g.split("=", 1)[1]).to_numpy()
        idx = np.where(mask)[0]
        take = rng.choice(idx, size=min(n, len(idx)), replace=False)
        out[g] = np.array([float((df[q].iloc[take] == o).sum()) for o in options])
    return out


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
            acc_pool: dict[str, list] = {g: [] for g in groups}
            acc_alone: dict[str, list] = {g: [] for g in groups}
            for _ in range(draws if n_loc > 0 else 1):
                counts = _draw_counts(df, q, options, groups, design, n_loc, rng) if n_loc > 0 else {}
                for g in groups:
                    key = (q, g)
                    if key not in real or not all(key in source_preds[s] for s in names):
                        continue
                    src = {s: source_preds[s][key] for s in names}
                    c = counts.get(g)
                    acc_pool[g].append(pool(src, alphas, c))
                    if n_loc > 0:
                        acc_alone[g].append(_norm(c) if c is not None and c.sum() > 0 else pool(src, alphas))
            for g in groups:
                key = (q, g)
                if acc_pool[g]:
                    variants[tag][key] = np.mean(acc_pool[g], axis=0).tolist()
                    if n_loc == 0:
                        for s in names:
                            variants[f"{s} alone"][key] = list(_norm(source_preds[s][key]))
                    else:
                        variants[f"local survey of {n_loc} alone"][key] = np.mean(acc_alone[g], axis=0).tolist()
    scored = pd.concat([H.score(v, bench, name) for name, v in variants.items() if v], ignore_index=True)
    scored = scored[scored.group.isin(groups)]
    scored["level"] = np.where(scored.group == "ALL", "population", "segment")
    seg = pd.concat([H.segment_fidelity(v, bench, name) for name, v in variants.items() if v], ignore_index=True)
    return {"scored": scored, "segment": seg, "alphas": pd.DataFrame(fitted)}
