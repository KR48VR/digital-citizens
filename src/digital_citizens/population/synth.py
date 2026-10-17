"""Make a persona bank match a population: iterative proportional fitting (IPF) and raking.

Use cases:
- You have a persona bank (e.g. NVIDIA Nemotron personas, or real survey respondents) and the
  official census margins for a city/country. ``rake`` gives each persona a weight so that the
  weighted bank matches the margins on age, sex, ethnicity, education, region, ... simultaneously.
- You have a seed cross-tab and want to fit it to new margins: ``ipf``.
- ``sample_population`` then draws a synthetic population of any size from the weighted bank.
"""
from __future__ import annotations

from collections.abc import Mapping

import numpy as np
import pandas as pd


def ipf(seed: np.ndarray, marginals: list[np.ndarray], max_iter: int = 200, tol: float = 1e-8) -> np.ndarray:
    """N-dimensional iterative proportional fitting.

    ``seed`` is an N-dim contingency table of non-negative counts; ``marginals[i]`` is the target
    1-D margin for axis i. All targets are rescaled to the total of ``marginals[0]``.
    """
    x = np.asarray(seed, dtype=float).copy()
    targets = [np.asarray(m, dtype=float) for m in marginals]
    if len(targets) != x.ndim:
        raise ValueError("need one marginal per axis")
    total = targets[0].sum()
    targets = [t * (total / t.sum()) for t in targets]
    for _ in range(max_iter):
        max_dev = 0.0
        for axis, target in enumerate(targets):
            other = tuple(i for i in range(x.ndim) if i != axis)
            current = x.sum(axis=other)
            with np.errstate(divide="ignore", invalid="ignore"):
                factor = np.where(current > 0, target / current, 0.0)
            shape = [1] * x.ndim
            shape[axis] = -1
            x = x * factor.reshape(shape)
            max_dev = max(max_dev, float(np.abs(x.sum(axis=other) - target).max()))
        if max_dev < tol:
            break
    return x


def margins(df: pd.DataFrame, col: str, weights: np.ndarray | None = None) -> dict[str, float]:
    w = np.ones(len(df)) if weights is None else np.asarray(weights, float)
    s = pd.Series(w, index=df.index).groupby(df[col].astype(str)).sum()
    return (s / s.sum()).to_dict()


def rake(
    df: pd.DataFrame,
    targets: Mapping[str, Mapping[str, float]],
    base_weights: np.ndarray | None = None,
    max_iter: int = 100,
    tol: float = 1e-7,
) -> np.ndarray:
    """Iterative raking: returns weights so weighted margins of each column match ``targets``.

    ``targets``: {column: {category: share}}. Categories present in ``df`` but missing from a
    column's target get weight 0 for that column (they are treated as out of population).
    """
    w = np.ones(len(df)) if base_weights is None else np.asarray(base_weights, float).copy()
    cols = {c: df[c].astype(str).to_numpy() for c in targets}
    for _ in range(max_iter):
        max_dev = 0.0
        for col, target in targets.items():
            tshare = {k: v / sum(target.values()) for k, v in target.items()}
            vals = cols[col]
            total = w.sum()
            for cat, share in tshare.items():
                mask = vals == cat
                cur = w[mask].sum()
                if cur > 0:
                    w[mask] *= (share * total) / cur
                    max_dev = max(max_dev, abs(cur / total - share))
            w[~np.isin(vals, list(tshare))] = 0.0
        if max_dev < tol:
            break
    return w


def margin_error(df: pd.DataFrame, targets: Mapping[str, Mapping[str, float]], weights: np.ndarray | None = None) -> dict[str, float]:
    """Total-variation distance between weighted margins and each target column (0 = perfect)."""
    out = {}
    for col, target in targets.items():
        tshare = {k: v / sum(target.values()) for k, v in target.items()}
        got = margins(df, col, weights)
        keys = set(tshare) | set(got)
        out[col] = 0.5 * sum(abs(tshare.get(k, 0.0) - got.get(k, 0.0)) for k in keys)
    return out


def sample_population(df: pd.DataFrame, n: int, weights: np.ndarray | None = None, seed: int = 0) -> pd.DataFrame:
    rng = np.random.default_rng(seed)
    p = None if weights is None else np.asarray(weights, float) / np.sum(weights)
    idx = rng.choice(len(df), size=n, replace=True, p=p)
    return df.iloc[idx].reset_index(drop=True)
