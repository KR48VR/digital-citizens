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


def fit_alphas(cells: Sequence[tuple[Mapping[str, Sequence[float]], Sequence[float], Sequence[float] | None]], names: Sequence[str], init: float = 50.0) -> dict[str, float]:
    """Choose alphas (>= 0) minimising mean JSD between pooled estimate and real shares over calibration cells.

    ``cells`` is a list of (sources, real_probs, counts_or_None). Optimised in log space (alphas = exp(x)).
    """
    names = list(names)

    def loss(x: np.ndarray) -> float:
        al = {n: float(np.exp(v)) for n, v in zip(names, x)}
        return float(np.mean([M.jsd(_norm(real), pool(src, al, cnt)) for src, real, cnt in cells]))

    x0 = np.full(len(names), np.log(init))
    res = minimize(loss, x0, method="Nelder-Mead", options={"maxiter": 400, "xatol": 1e-3, "fatol": 1e-7})
    return {n: float(np.exp(v)) for n, v in zip(names, res.x)}


def loo_bayes_evaluate(
    bench: Benchmark,
    source_preds: Mapping[str, Mapping[Key, Sequence[float]]],
    groups: Sequence[str],
    local_n: Sequence[int] = (0, 50, 100, 300),
    seed: int = 0,
    draws: int = 3,
) -> dict[str, pd.DataFrame]:
    """Leave-one-question-out: fit source weights on the other questions, then estimate each cell of the
    held-out question with a local sample of n real respondents (n = 0 means prior only).

    Returns scored cells for: each single source; the pooled prior (n = 0); and pooled + local n.
    Also returns the fitted alphas per held-out question.
    """
    rng = np.random.default_rng(seed)
    real = {k: d.normalised() for k, d in bench.real.items() if k[1] in groups}
    names = list(source_preds)
    items = sorted({k[0] for k in real if all((k[0], "ALL") in source_preds[n] for n in names)})
    df = bench.respondents
    variants: dict[str, dict[Key, list[float]]] = {f"{n} alone": {} for n in names}
    variants["pooled prior (n=0)"] = {}
    for n in local_n:
        if n > 0:
            variants[f"pooled + {n} local answers"] = {}
            variants[f"{n} local answers alone"] = {}
    fitted = []
    for q in items:
        cal_cells = []
        for i in items:
            if i == q:
                continue
            for g in groups:
                key = (i, g)
                if key in real and all(key in source_preds[n] for n in names):
                    cal_cells.append(({n: source_preds[n][key] for n in names}, real[key], None))
        alphas = fit_alphas(cal_cells, names)
        fitted.append({"held_out": q, **alphas})
        options = bench.qmap[q].options
        valid = df[q].notna().to_numpy()
        for g in groups:
            key = (q, g)
            if key not in real or not all(key in source_preds[n] for n in names):
                continue
            src = {n: source_preds[n][key] for n in names}
            for n in names:
                variants[f"{n} alone"][key] = list(_norm(src[n]))
            variants["pooled prior (n=0)"][key] = pool(src, alphas).tolist()
            mask = valid if g == "ALL" else valid & (df[g.split("=", 1)[0]].astype(str) == g.split("=", 1)[1]).to_numpy()
            idx_all = np.where(mask)[0]
            for n_loc in local_n:
                if n_loc <= 0:
                    continue
                pooled_acc, alone_acc = [], []
                for _ in range(draws):
                    take = rng.choice(idx_all, size=min(n_loc, len(idx_all)), replace=False)
                    counts = np.array([float((df[q].iloc[take] == o).sum()) for o in options])
                    pooled_acc.append(pool(src, alphas, counts))
                    alone_acc.append(_norm(counts) if counts.sum() > 0 else np.full(len(options), 1 / len(options)))
                variants[f"pooled + {n_loc} local answers"][key] = np.mean(pooled_acc, axis=0).tolist()
                variants[f"{n_loc} local answers alone"][key] = np.mean(alone_acc, axis=0).tolist()
    scored = pd.concat([H.score(v, bench, name) for name, v in variants.items() if v], ignore_index=True)
    scored = scored[scored.group.isin(groups)]
    scored["level"] = np.where(scored.group == "ALL", "population", "segment")
    seg = pd.concat([H.segment_fidelity(v, bench, name) for name, v in variants.items() if v], ignore_index=True)
    return {"scored": scored, "segment": seg, "alphas": pd.DataFrame(fitted)}
