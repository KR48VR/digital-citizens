"""Baselines the digital citizens must beat, and ceilings they cannot be expected to beat.

A simulation is only worth paying for if it beats what an analyst could get for free from the
data already in hand. These are the free alternatives.
"""
from __future__ import annotations

from collections import Counter

import numpy as np
import pandas as pd

from ..data.benchmark import Benchmark, Key


def uniform(bench: Benchmark) -> dict[Key, list[float]]:
    qmap = bench.qmap
    return {k: [1.0 / qmap[k[0]].k] * qmap[k[0]].k for k in bench.real}


def population_marginal(bench: Benchmark) -> dict[Key, list[float]]:
    """Give every segment the overall population's shares: the 'everyone is average' baseline.

    If a simulator cannot beat this on segments, it has no segment-level information at all.
    """
    out: dict[Key, list[float]] = {}
    for (qid, g) in bench.real:
        if (qid, "ALL") in bench.real:
            out[(qid, g)] = list(bench.real[(qid, "ALL")].probs)
    return out


def leave_one_group_out_mean(bench: Benchmark) -> dict[Key, list[float]]:
    """For each (question, group) the average shares over the OTHER groups that answered it.

    For GlobalOpinionQA this is the 'other countries' average' baseline, which prior work found
    hard for LLMs to beat on country-level means.
    """
    by_q: dict[str, dict[str, list[float]]] = {}
    for (qid, g), d in bench.real.items():
        if g != "ALL":
            by_q.setdefault(qid, {})[g] = d.normalised()
    out: dict[Key, list[float]] = {}
    for qid, groups in by_q.items():
        for g in groups:
            others = [v for h, v in groups.items() if h != g]
            if others:
                out[(qid, g)] = list(np.mean(others, axis=0))
    return out


def previous_wave(bench: Benchmark, prev: Benchmark) -> dict[Key, list[float]]:
    """Use last wave's shares (same question, same group) as the prediction for this wave."""
    return {k: list(d.probs) for k, d in prev.real.items() if k in bench.real and len(d.probs) == len(bench.real[k].probs)}


# ---- individual-level baselines (need a respondents table with one column per item, option label or NaN)


def modal_answer(train: pd.Series) -> str | None:
    s = train.dropna().astype(str)
    return None if s.empty else s.value_counts().idxmax()


def demographic_cell_modal(train: pd.DataFrame, test: pd.DataFrame, item: str, cells: list[str], min_cell: int = 15) -> pd.Series:
    """Predict each test person's answer as the modal answer among training people in the same demographic cell."""
    overall = modal_answer(train[item])
    key_train = train[cells].astype(str).agg("|".join, axis=1)
    key_test = test[cells].astype(str).agg("|".join, axis=1)
    modes = {}
    for key, grp in train.groupby(key_train):
        s = grp[item].dropna().astype(str)
        if len(s) >= min_cell:
            modes[key] = s.value_counts().idxmax()
    return key_test.map(lambda k: modes.get(k, overall))


def knn_predict(train_x: pd.DataFrame, train_y: pd.Series, test_x: pd.DataFrame, k: int = 25, chunk: int = 64) -> pd.Series:
    """k-nearest-neighbour respondents by matching-rate on categorical answers to OTHER items.

    Simple, fast, no LLM: if digital twins cannot beat this, the 'twin' is adding nothing beyond
    'people who answered similarly before'. Ties are broken by the most common answer among neighbours.
    """
    both = pd.concat([train_x, test_x], axis=0)
    codes = np.empty(both.shape, dtype=np.int16)
    for j, c in enumerate(both.columns):
        codes[:, j] = pd.factorize(both[c].astype(str).where(both[c].notna(), None))[0]
    tx, sx = codes[: len(train_x)], codes[len(train_x):]
    valid_t = train_y.notna().to_numpy()
    tx, ty = tx[valid_t], train_y[valid_t].astype(str).to_numpy()
    preds: list[str] = []
    for start in range(0, len(sx), chunk):
        rows = sx[start : start + chunk]
        known = (rows[:, None, :] >= 0) & (tx[None, :, :] >= 0)
        match = (rows[:, None, :] == tx[None, :, :]) & known
        denom = known.sum(axis=2)
        sim = np.where(denom > 0, match.sum(axis=2) / np.maximum(denom, 1), 0.0)
        idx = np.argsort(-sim, axis=1)[:, :k]
        for nb in idx:
            preds.append(Counter(ty[nb]).most_common(1)[0][0])
    return pd.Series(preds, index=test_x.index)


def demographic_regression(
    train: pd.DataFrame,
    test: pd.DataFrame,
    item: str,
    options: list[str],
    demo_cols: list[str],
    segment_keys: list[str],
    min_n: int = 30,
    C: float = 0.5,
) -> dict[Key, list[float]]:
    """'MRP-lite': a regularised multinomial logistic regression of the answer on demographics, fitted on
    one wave's respondents and used to predict the next wave's segment shares (weighted). This is roughly
    what a competent analyst does with last wave's data and this wave's demographics, and it is the bar a
    digital-citizen simulator must clear on known questions."""
    from sklearn.linear_model import LogisticRegression
    from sklearn.preprocessing import OneHotEncoder

    tr = train[train[item].notna()]
    if len(tr) < 50 or tr[item].nunique() < 2:
        return {}
    enc = OneHotEncoder(handle_unknown="ignore")
    X = enc.fit_transform(tr[demo_cols].astype(str))
    y = tr[item].astype(str)
    clf = LogisticRegression(C=C, max_iter=2000)
    clf.fit(X, y, sample_weight=tr["weight"].to_numpy())
    Xt = enc.transform(test[demo_cols].astype(str))
    P = clf.predict_proba(Xt)
    classes = list(clf.classes_)
    full = np.zeros((len(test), len(options)))
    for j, o in enumerate(options):
        if o in classes:
            full[:, j] = P[:, classes.index(o)]
    w = test["weight"].to_numpy()
    out: dict[Key, list[float]] = {}

    def agg(mask: np.ndarray) -> list[float] | None:
        if mask.sum() < min_n:
            return None
        v = (full[mask] * w[mask, None]).sum(axis=0)
        return list(v / v.sum()) if v.sum() > 0 else None

    v = agg(np.ones(len(test), bool))
    if v is not None:
        out[(item, "ALL")] = v
    for key in segment_keys:
        for val in test[key].unique():
            if val == "NA":
                continue
            v = agg((test[key] == val).to_numpy())
            if v is not None:
                out[(item, f"{key}={val}")] = v
    return out
