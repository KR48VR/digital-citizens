"""Put two surveys of the same population on common segments and common answer bins."""
from __future__ import annotations

import numpy as np
import pandas as pd

from ..data.benchmark import Benchmark, Key
from ..schema import Distribution, Question

SEGMENTS = ["sex", "age_band4", "education3", "race_eth", "religion4", "region4"]

_NE = {"CT", "ME", "MA", "NH", "RI", "VT", "NJ", "NY", "PA"}
_MW = {"IL", "IN", "MI", "OH", "WI", "IA", "KS", "MN", "MO", "NE", "ND", "SD"}
_SO = {"DE", "FL", "GA", "MD", "NC", "SC", "VA", "DC", "WV", "AL", "KY", "MS", "TN", "AR", "LA", "OK", "TX"}
_WE = {"AZ", "CO", "ID", "MT", "NV", "NM", "UT", "WY", "AK", "CA", "HI", "OR", "WA"}


def age_band4(a: float) -> str:
    if pd.isna(a) or a < 0:
        return "NA"
    return "18-29" if a < 30 else "30-44" if a < 45 else "45-59" if a < 60 else "60+"


def _region4_from_state(label: str) -> str:
    if not isinstance(label, str) or not label.startswith("US: "):
        return "NA"
    code = label.split(" ")[1]
    return "Northeast" if code in _NE else "Midwest" if code in _MW else "South" if code in _SO else "West" if code in _WE else "NA"


def harmonise_gss(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()
    out["age_band4"] = out["age"].map(age_band4)
    out["education3"] = out["education"].map({"No high school diploma": "Lower", "High school": "Middle", "Some college / associate": "Middle", "Bachelor's or higher": "Higher"}).fillna("NA")
    out["region4"] = out["region"].fillna("NA")
    out["sex"] = out["sex"].fillna("NA")
    return out


def harmonise_wvs_us(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()
    out["age_band4"] = out["age"].map(age_band4)
    out["race_eth"] = out["ethnic"].map({"White, non-Hispanic": "White, non-Hispanic", "Hispanic": "Hispanic", "Black, Non-Hispanic": "Black, non-Hispanic", "Other, Non-Hispanic": "Other, non-Hispanic"}).fillna("NA")
    out["religion4"] = out["religion"].map(lambda r: r if r in {"Protestant", "Catholic", "No religion", "NA"} else "Other religion")
    out["region4"] = out["region"].map(_region4_from_state)
    return out


def collapse(probs, index_groups: list[list[int]]) -> list[float]:
    p = np.asarray(probs, dtype=float)
    v = np.array([p[idx].sum() for idx in index_groups])
    s = v.sum()
    return (v / s).tolist() if s > 0 else [1.0 / len(index_groups)] * len(index_groups)


def weighted_bins(answers: pd.Series, weights: pd.Series, options: list[str], index_groups: list[list[int]]) -> tuple[list[float], int]:
    m = answers.notna()
    if m.sum() == 0:
        return [float("nan")] * len(index_groups), 0
    w, a = weights[m], answers[m]
    counts = [sum(float(w[a == options[i]].sum()) for i in idx) for idx in index_groups]
    tot = sum(counts)
    n_used = int(sum(int((a == options[i]).sum()) for idx in index_groups for i in idx))
    return ([c / tot for c in counts] if tot > 0 else [1.0 / len(index_groups)] * len(index_groups)), n_used


def groups_of(df: pd.DataFrame, segments: list[str], min_n: int) -> list[str]:
    out = ["ALL"]
    for key in segments:
        for val, cnt in df[key].value_counts().items():
            if val != "NA" and cnt >= min_n:
                out.append(f"{key}={val}")
    return out


def _mask(df: pd.DataFrame, g: str) -> np.ndarray:
    if g == "ALL":
        return np.ones(len(df), bool)
    key, val = g.split("=", 1)
    return (df[key].astype(str) == val).to_numpy()


def truth_benchmark(wvs_df: pd.DataFrame, qmap: dict[str, Question], pairs: list[dict], groups: list[str], min_n: int = 50, name: str = "wvs7_us_on_common_bins") -> Benchmark:
    """Ground truth: WVS United States shares on the common bins, by harmonised group."""
    questions, real = [], {}
    for p in pairs:
        q = qmap[p["wvs"]]
        questions.append(Question(id=p["wvs"], text=f"{p['label']} [WVS wording: {q.text}]", options=p["bins"], ordinal=p["ordinal"], source="WVS7 United States", topic=p["label"]))
        for g in groups:
            m = _mask(wvs_df, g)
            probs, n = weighted_bins(wvs_df.loc[m, p["wvs"]], wvs_df.loc[m, "weight"], q.options, p["wvs_map"])
            if n >= min_n:
                real[(p["wvs"], g)] = Distribution(question_id=p["wvs"], group=g, probs=probs, n=n)
    return Benchmark(name=name, country="United States", questions=questions, real=real, respondents=wvs_df, segment_keys=SEGMENTS)


def library_predictions(gss_df: pd.DataFrame, gss_items: dict, pairs: list[dict], groups: list[str], min_n: int = 30) -> tuple[dict[Key, list[float]], dict[Key, int]]:
    """What the library says: the matched GSS item's shares (on common bins) for each harmonised group."""
    pred, ns = {}, {}
    for p in pairs:
        options = gss_items[p["gss"]][1]
        for g in groups:
            m = _mask(gss_df, g)
            probs, n = weighted_bins(gss_df.loc[m, p["gss"]], gss_df.loc[m, "weight"], options, p["gss_map"])
            if n >= min_n:
                pred[(p["wvs"], g)] = probs
                ns[(p["wvs"], g)] = n
    return pred, ns


def map_to_bins(pred: dict[Key, list[float]], pairs: list[dict]) -> dict[Key, list[float]]:
    """Collapse predictions made on the full WVS option list onto the common bins."""
    bw = {p["wvs"]: p for p in pairs}
    return {k: collapse(v, bw[k[0]]["wvs_map"]) for k, v in pred.items() if k[0] in bw}


def relevel(spread: dict[Key, list[float]], level: dict[Key, list[float]], groups: list[str]) -> dict[Key, list[float]]:
    """Take the overall level from ``level`` and the group-minus-population differences from ``spread``."""
    out = {}
    for (q, g), p in spread.items():
        if (q, "ALL") not in spread or (q, "ALL") not in level or g not in groups:
            continue
        v = np.asarray(level[(q, "ALL")]) + np.asarray(p) - np.asarray(spread[(q, "ALL")])
        v = np.clip(v, 1e-6, None)
        out[(q, g)] = (v / v.sum()).tolist()
    return out


def average(a: dict[Key, list[float]], b: dict[Key, list[float]]) -> dict[Key, list[float]]:
    return {k: ((np.asarray(a[k]) + np.asarray(b[k])) / 2).tolist() for k in a if k in b}


def mae_noise_floor(bench: Benchmark, draws: int = 200, seed: int = 0) -> pd.DataFrame:
    """Expected mean-absolute-error (points) between the truth and a fresh sample of the same size: the floor."""
    rng = np.random.default_rng(seed)
    rows = []
    for (q, g), d in bench.real.items():
        p = np.asarray(d.normalised())
        n = max(int(d.n), 1)
        sims = rng.multinomial(n, p, size=draws) / n
        rows.append({"question_id": q, "group": g, "n": n, "mae_floor": 100 * float(np.mean(np.abs(sims - p)))})
    return pd.DataFrame(rows)
