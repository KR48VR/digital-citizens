"""How much segment signal do real respondent records carry?

For each target question, predict every respondent's answer from (a) demographics only, or (b)
demographics plus their answers to all the OTHER questions, using a regularised logistic regression
fitted on half the respondents and applied to the other half (2-fold, out-of-sample). Aggregating the
out-of-fold probabilities by segment gives predicted segment shares, which are scored like any simulator.

This is the no-LLM ceiling for 'record-anchored' digital citizens: if the records recover group
differences that the zero-shot model flattens, anchoring personas to real records is the fix.
"""
from __future__ import annotations

import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import OneHotEncoder

from ..data.benchmark import Benchmark, Key


def record_transfer(bench: Benchmark, targets: list[str], demo_cols: list[str], groups: list[str], feature_items: list[str] | None = None, C: float = 0.3, seed: int = 0, min_n: int = 30) -> dict[str, dict[Key, list[float]]]:
    df = bench.respondents
    items = [q.id for q in bench.questions if q.id in df.columns] if feature_items is None else feature_items
    rng = np.random.default_rng(seed)
    fold = rng.integers(0, 2, len(df))
    w = df["weight"].to_numpy()
    out: dict[str, dict[Key, list[float]]] = {"demographics only": {}, "demographics + record": {}}
    for t in targets:
        options = bench.qmap[t].options
        y_all = df[t]
        others = [i for i in items if i != t]
        feats = {"demographics only": df[demo_cols].astype(str), "demographics + record": pd.concat([df[demo_cols].astype(str), df[others].astype(str)], axis=1)}
        for name, X in feats.items():
            P = np.zeros((len(df), len(options)))
            for f in (0, 1):
                tr = (fold != f) & y_all.notna().to_numpy()
                te = fold == f
                enc = OneHotEncoder(handle_unknown="ignore")
                Xtr = enc.fit_transform(X[tr])
                clf = LogisticRegression(C=C, max_iter=3000)
                clf.fit(Xtr, y_all[tr].astype(str), sample_weight=w[tr])
                pr = clf.predict_proba(enc.transform(X[te]))
                for j, o in enumerate(options):
                    if o in clf.classes_:
                        P[te, j] = pr[:, list(clf.classes_).index(o)]
            valid = y_all.notna().to_numpy()
            for g in groups:
                if g == "ALL":
                    mask = valid
                else:
                    key, val = g.split("=", 1)
                    mask = valid & (df[key].astype(str) == val).to_numpy()
                if mask.sum() < min_n:
                    continue
                v = (P[mask] * w[mask, None]).sum(axis=0)
                if v.sum() > 0:
                    out[name][(t, g)] = (v / v.sum()).tolist()
    return out


def small_sample_transfer(bench: Benchmark, targets: list[str], demo_cols: list[str], groups: list[str], n_cal: int = 300, reps: int = 5, C: float = 0.3, seed: int = 0, min_n: int = 30) -> dict[str, dict[Key, list[float]]]:
    """The 'small human sample' regime: only ``n_cal`` random respondents answered the target question.

    Compares three ways of estimating every segment's shares from that small sample: the sample's own
    crosstab (noisy for small groups), a demographics-only regression, and a demographics + record
    regression that borrows strength from everyone's answers to the other questions. Predictions are
    averaged over ``reps`` random calibration samples.
    """
    df = bench.respondents
    items = [q.id for q in bench.questions if q.id in df.columns]
    w = df["weight"].to_numpy()
    acc: dict[str, dict[Key, list[np.ndarray]]] = {"small-sample crosstab": {}, "small sample -> demographics model": {}, "small sample -> demographics + record model": {}}
    rng = np.random.default_rng(seed)
    for t in targets:
        options = bench.qmap[t].options
        y_all = df[t]
        valid = y_all.notna().to_numpy()
        others = [i for i in items if i != t]
        feats = {"small sample -> demographics model": df[demo_cols].astype(str), "small sample -> demographics + record model": pd.concat([df[demo_cols].astype(str), df[others].astype(str)], axis=1)}
        for _ in range(reps):
            cal_idx = rng.choice(np.where(valid)[0], size=min(n_cal, int(valid.sum())), replace=False)
            cal = np.zeros(len(df), bool); cal[cal_idx] = True
            for g in groups:
                mask = valid if g == "ALL" else (valid & (df[g.split("=", 1)[0]].astype(str) == g.split("=", 1)[1]).to_numpy())
                m = mask & cal
                if m.sum() >= 5:
                    v = np.array([float(w[m][(y_all[m] == o).to_numpy()].sum()) for o in options])
                    if v.sum() > 0:
                        acc["small-sample crosstab"].setdefault((t, g), []).append(v / v.sum())
            for name, X in feats.items():
                if y_all[cal].nunique() < 2:
                    continue
                enc = OneHotEncoder(handle_unknown="ignore")
                clf = LogisticRegression(C=C, max_iter=3000)
                clf.fit(enc.fit_transform(X[cal]), y_all[cal].astype(str), sample_weight=w[cal])
                pr = clf.predict_proba(enc.transform(X))
                P = np.zeros((len(df), len(options)))
                for j, o in enumerate(options):
                    if o in clf.classes_:
                        P[:, j] = pr[:, list(clf.classes_).index(o)]
                for g in groups:
                    mask = valid if g == "ALL" else (valid & (df[g.split("=", 1)[0]].astype(str) == g.split("=", 1)[1]).to_numpy())
                    if mask.sum() < min_n:
                        continue
                    v = (P[mask] * w[mask, None]).sum(axis=0)
                    if v.sum() > 0:
                        acc[name].setdefault((t, g), []).append(v / v.sum())
    return {name: {k: np.mean(v, axis=0).tolist() for k, v in d.items()} for name, d in acc.items()}


def cross_country_transfer(train_benches: list[Benchmark], test_bench: Benchmark, targets: list[str], demo_cols: list[str], groups: list[str], C: float = 0.3, min_n: int = 30) -> dict[Key, list[float]]:
    """Learn record -> answer from OTHER countries' respondents and apply it to this country's respondents.

    A digital citizen built purely from a real record (no LLM): the person's answers to the other
    questions, plus demographics, predict their answer to the target question using a mapping learned
    abroad. Tests whether value profiles transfer across countries better than the LLM's priors.
    """
    out: dict[Key, list[float]] = {}
    df_te = test_bench.respondents
    w_te = df_te["weight"].to_numpy()
    for t in targets:
        options = test_bench.qmap[t].options
        shared = [q.id for q in test_bench.questions if q.id != t and all(q.id in b.respondents.columns for b in train_benches) and q.id in df_te.columns]
        cols = demo_cols + shared
        tr = pd.concat([b.respondents[[t, "weight", *cols]] for b in train_benches if t in b.respondents.columns], ignore_index=True)
        tr = tr[tr[t].notna() & tr[t].isin(options)]
        if len(tr) < 100 or tr[t].nunique() < 2:
            continue
        enc = OneHotEncoder(handle_unknown="ignore")
        clf = LogisticRegression(C=C, max_iter=3000)
        clf.fit(enc.fit_transform(tr[cols].astype(str)), tr[t].astype(str), sample_weight=tr["weight"].to_numpy())
        pr = clf.predict_proba(enc.transform(df_te[cols].astype(str)))
        P = np.zeros((len(df_te), len(options)))
        for j, o in enumerate(options):
            if o in clf.classes_:
                P[:, j] = pr[:, list(clf.classes_).index(o)]
        valid = df_te[t].notna().to_numpy()
        for g in groups:
            mask = valid if g == "ALL" else (valid & (df_te[g.split("=", 1)[0]].astype(str) == g.split("=", 1)[1]).to_numpy())
            if mask.sum() < min_n:
                continue
            v = (P[mask] * w_te[mask, None]).sum(axis=0)
            if v.sum() > 0:
                out[(t, g)] = (v / v.sum()).tolist()
    return out


def small_survey_holdout(bench: Benchmark, targets: list[str], demo_cols: list[str], groups: list[str], n_cal: int = 300, reps: int = 5, C: float = 0.3, seed: int = 0, min_n: int = 30) -> list[dict[str, dict[Key, list[float]]]]:
    """A fresh small survey, scored honestly: ``n_cal`` random respondents answer the target question; the truth is
    computed on everyone else (so the sample never overlaps the people it is scored against); each repeat is
    returned separately so that scores, not predictions, are averaged over repeats.

    Per repeat: ``truth`` (hold-out shares by group), ``crosstab`` (the sample's own shares by group), and two
    models fitted on the sample and applied to the hold-out respondents' records: ``demographics model`` and
    ``demographics + record model``.
    """
    df = bench.respondents
    items = [q.id for q in bench.questions if q.id in df.columns]
    w = df["weight"].to_numpy()
    rng = np.random.default_rng(seed)
    out = []
    for _ in range(reps):
        rep: dict[str, dict[Key, list[float]]] = {"truth": {}, "crosstab": {}, "demographics model": {}, "demographics + record model": {}}
        for t in targets:
            options = bench.qmap[t].options
            y_all = df[t]
            valid = y_all.notna().to_numpy()
            cal_idx = rng.choice(np.where(valid)[0], size=min(n_cal, int(valid.sum())), replace=False)
            cal = np.zeros(len(df), bool); cal[cal_idx] = True
            hold = valid & ~cal
            others = [i for i in items if i != t]
            feats = {"demographics model": df[demo_cols].astype(str), "demographics + record model": pd.concat([df[demo_cols].astype(str), df[others].astype(str)], axis=1)}
            P = {}
            if y_all[cal].nunique() >= 2:
                for name, X in feats.items():
                    enc = OneHotEncoder(handle_unknown="ignore")
                    clf = LogisticRegression(C=C, max_iter=3000)
                    clf.fit(enc.fit_transform(X[cal]), y_all[cal].astype(str), sample_weight=w[cal])
                    pr = clf.predict_proba(enc.transform(X))
                    M = np.zeros((len(df), len(options)))
                    for j, o in enumerate(options):
                        if o in clf.classes_:
                            M[:, j] = pr[:, list(clf.classes_).index(o)]
                    P[name] = M
            for g in groups:
                gm = np.ones(len(df), bool) if g == "ALL" else (df[g.split("=", 1)[0]].astype(str) == g.split("=", 1)[1]).to_numpy()
                hm = hold & gm
                if hm.sum() < min_n:
                    continue
                v = np.array([float(w[hm][(y_all[hm] == o).to_numpy()].sum()) for o in options])
                if v.sum() <= 0:
                    continue
                rep["truth"][(t, g)] = (v / v.sum()).tolist()
                cm = cal & gm
                if cm.sum() >= 5:
                    c = np.array([float(w[cm][(y_all[cm] == o).to_numpy()].sum()) for o in options])
                    if c.sum() > 0:
                        rep["crosstab"][(t, g)] = (c / c.sum()).tolist()
                for name, M in P.items():
                    u = (M[hm] * w[hm, None]).sum(axis=0)
                    if u.sum() > 0:
                        rep[name][(t, g)] = (u / u.sum()).tolist()
        out.append(rep)
    return out
