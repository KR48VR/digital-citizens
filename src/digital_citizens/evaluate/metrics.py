"""Fidelity metrics.

Every function takes answer-share vectors (any non-negative numbers; they are normalised).
Conventions:
- ``real`` / ``p`` is the human ground truth, ``sim`` / ``q`` is the simulation.
- Lower is better for divergences (jsd, total_variation, wasserstein_ordinal, top_box_error).
- Ratios (dispersion_ratio, entropy_ratio) are ideal at 1.0: below 1 means the simulation is
  flatter / less varied than people ("regression to the mean"); above 1 means caricature.
"""
from __future__ import annotations

from collections.abc import Mapping, Sequence

import numpy as np


def _norm(p: Sequence[float]) -> np.ndarray:
    a = np.asarray(p, dtype=float)
    a = np.where(np.isfinite(a), a, 0.0)
    a = np.clip(a, 0.0, None)
    s = a.sum()
    return a / s if s > 0 else np.full(a.shape, 1.0 / len(a))


def entropy(p: Sequence[float], base: float = 2.0) -> float:
    a = _norm(p)
    nz = a[a > 0]
    return float(-(nz * np.log(nz)).sum() / np.log(base))


def jsd(p: Sequence[float], q: Sequence[float], base: float = 2.0) -> float:
    """Jensen-Shannon divergence. With base 2 it lies in [0, 1]; 0 = identical."""
    a, b = _norm(p), _norm(q)
    m = 0.5 * (a + b)

    def kl(x: np.ndarray, y: np.ndarray) -> float:
        mask = x > 0
        return float((x[mask] * np.log(x[mask] / y[mask])).sum())

    return (0.5 * kl(a, m) + 0.5 * kl(b, m)) / np.log(base)


def total_variation(p: Sequence[float], q: Sequence[float]) -> float:
    a, b = _norm(p), _norm(q)
    return float(0.5 * np.abs(a - b).sum())


def wasserstein_ordinal(p: Sequence[float], q: Sequence[float]) -> float:
    """1-Wasserstein distance between two distributions over ordered options at unit spacing."""
    a, b = _norm(p), _norm(q)
    return float(np.abs(np.cumsum(a) - np.cumsum(b))[:-1].sum())


def representativeness(p: Sequence[float], q: Sequence[float]) -> float:
    """1 - WD/(K-1), in [0, 1]; the OpinionQA 'representativeness' score for ordinal questions."""
    k = len(p)
    if k < 2:
        return 1.0
    return 1.0 - wasserstein_ordinal(p, q) / (k - 1)


def top_box_error(p: Sequence[float], q: Sequence[float], index: int = 0) -> float:
    a, b = _norm(p), _norm(q)
    return float(abs(a[index] - b[index]))


def mean_position(p: Sequence[float]) -> float:
    """Mean option position (0..K-1) for an ordinal question; a one-number summary of a distribution."""
    a = _norm(p)
    return float((a * np.arange(len(a))).sum())


def entropy_ratio(sim: Sequence[float], real: Sequence[float]) -> float:
    hr = entropy(real)
    return float("nan") if hr == 0 else entropy(sim) / hr


def pearson(x: Sequence[float], y: Sequence[float]) -> float:
    a, b = np.asarray(x, float), np.asarray(y, float)
    mask = np.isfinite(a) & np.isfinite(b)
    a, b = a[mask], b[mask]
    if len(a) < 3 or a.std() == 0 or b.std() == 0:
        return float("nan")
    return float(np.corrcoef(a, b)[0, 1])


def dispersion_ratio(real_values: Sequence[float], sim_values: Sequence[float]) -> float:
    """Var(sim segment summaries) / Var(real segment summaries).

    Feed it one summary number per segment (e.g. mean position, or share choosing option 0)
    for the same question. 1.0 = segments differ by as much as in reality. <1 = flattened.
    """
    r, s = np.asarray(real_values, float), np.asarray(sim_values, float)
    mask = np.isfinite(r) & np.isfinite(s)
    r, s = r[mask], s[mask]
    if len(r) < 2 or r.var() == 0:
        return float("nan")
    return float(s.var() / r.var())


def gap_recovery(
    real_pop: Sequence[float],
    real_segments: Mapping[str, Sequence[float]],
    sim_pop: Sequence[float],
    sim_segments: Mapping[str, Sequence[float]],
) -> dict[str, float]:
    """How well the simulation reproduces *how segments differ from the population*.

    For each segment and option we take gap = share(segment) - share(population), in the real data
    and in the simulation, then report the correlation and the regression slope of simulated gaps on
    real gaps. r near 1 and slope near 1 = segment differences are reproduced; slope well below 1 =
    the simulation flattens groups toward the average; slope above 1 = exaggerates them.
    """
    xs: list[float] = []
    ys: list[float] = []
    rp, sp = _norm(real_pop), _norm(sim_pop)
    for key, rs in real_segments.items():
        if key not in sim_segments:
            continue
        rseg, sseg = _norm(rs), _norm(sim_segments[key])
        xs.extend((rseg - rp).tolist())
        ys.extend((sseg - sp).tolist())
    x, y = np.asarray(xs), np.asarray(ys)
    out = {"r": pearson(x, y), "slope": float("nan"), "n_pairs": float(len(x))}
    if len(x) >= 3 and x.var() > 0:
        out["slope"] = float(np.cov(x, y, bias=True)[0, 1] / x.var())
    return out


def sign_agreement(real_effects: Sequence[float], sim_effects: Sequence[float]) -> float:
    r, s = np.asarray(real_effects, float), np.asarray(sim_effects, float)
    mask = np.isfinite(r) & np.isfinite(s) & (r != 0)
    if mask.sum() == 0:
        return float("nan")
    return float((np.sign(r[mask]) == np.sign(s[mask])).mean())


def normalized_accuracy(sim_accuracy: float, retest_accuracy: float) -> float:
    """Park et al. (2024) normalisation: simulated accuracy divided by the humans' own test-retest
    accuracy. 1.0 means the simulation predicts a person as well as that person predicts themself
    two weeks later. Can exceed 1 when the simulation is steadier than the humans."""
    return float("nan") if retest_accuracy <= 0 else sim_accuracy / retest_accuracy


def noise_floor_jsd(p: Sequence[float], n: int, draws: int = 200, seed: int = 0) -> float:
    """Expected JSD between the true distribution and a random sample of n respondents from it.

    A perfect simulator compared against a survey of n people cannot be expected to score better
    than this; it is the 'ceiling' (floor on the divergence) imposed by survey sampling noise.
    """
    rng = np.random.default_rng(seed)
    a = _norm(p)
    if n <= 0:
        return float("nan")
    vals = []
    for _ in range(draws):
        counts = rng.multinomial(n, a)
        vals.append(jsd(a, counts))
    return float(np.mean(vals))


def accuracy(pred: Sequence[int], truth: Sequence[int]) -> float:
    a, b = np.asarray(pred), np.asarray(truth)
    mask = (a >= 0) & (b >= 0)
    return float("nan") if mask.sum() == 0 else float((a[mask] == b[mask]).mean())
