"""One method for every number on the scorecard: a small real survey, with or without AI, scored the same way.

For each country, question and survey size, a random sample of n respondents answers the question. Each group's
estimate is then one of:

  survey alone            the group's own answers in the sample (the overall sample answer if nobody in the group)
  + chatbot kind          the group's answers blended with the chatbot's estimate
  + record citizens       blended with record citizens' estimate, learned from past surveys
                          (Singapore: 61 other countries; United States: the same survey two years earlier)
  + record citizens (own) blended with record citizens learned from the sample itself (a brand-new question)
  + demographics (own)    blended with a model learned from the sample using demographics only
  + record + chatbot      blended with both past-survey record citizens and the chatbot

Blending: estimate = (worth x AI estimate + group's own answers) / (worth + people in the group), where each AI
source's "worth in respondents" is fitted on the other questions only (leave one question out), by survey size.
Truth: the people NOT in the sample (weighted). Error: points off per answer option. Scores are averaged over
draws for each group and question, then the middle result is taken across groups and questions.

Usage: one_method_experiment.py [singapore|us] [draws]
Writes docs/results/stress_test/one_method_<country>.md / .csv / _cells.csv.
"""
from __future__ import annotations

import json
import sys
import time
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.optimize import minimize
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import OneHotEncoder

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from digital_citizens.data import gss, wvs  # noqa: E402
from digital_citizens.evaluate.transfer import cross_country_transfer  # noqa: E402

OUT = Path("docs/results/stress_test")
SIZES = (150, 300, 600)
MIN_HOLD = 30
CONFIGS = {
    "survey alone": [],
    "+ chatbot kind": ["chat"],
    "+ record citizens": ["rec_past"],
    "+ record citizens (own survey)": ["rec_own"],
    "+ demographics only (own survey)": ["demo_own"],
    "+ record citizens + chatbot kind": ["rec_past", "chat"],
}


def _load(path: Path) -> dict:
    return {(r["question_id"], r["group"]): r["probs"] for r in json.load(open(path))}


def setup(country: str):
    if country == "us":
        packet = json.load(open(OUT / "packet_gss.json"))
        tg, groups = [q["id"] for q in packet["questions"]], [g for g in packet["groups"] if g != "ALL"]
        bench, b22 = gss.benchmark(2024), gss.benchmark(2022, segment_keys=["sex"])
        demo = ["age_band", "sex", "race_eth", "education", "region", "income4", "religion4"]
        rec = cross_country_transfer([b22], bench, tg, demo, groups + ["ALL"], C=0.3, min_n=30)
        chat = _load(OUT / "predictions_gss_claude_in_session.json")
        return "the United States", bench, tg, groups, demo, rec, chat
    packet = json.load(open(OUT / "packet_wvs_singapore.json"))
    tg, groups = [q["id"] for q in packet["questions"]], [g for g in packet["groups"] if g != "ALL"]
    bench = wvs.benchmark("Singapore")
    demo = ["sex", "age_band", "ethnic", "religion", "education3", "income3", "born_in_country"]
    rec = _load(OUT / "record_all_singapore_pred.json")
    chat = _load(OUT / "predictions_wvs_singapore_claude_in_session.json")
    return "Singapore", bench, tg, groups, demo, rec, chat


def _gmask(df: pd.DataFrame, g: str) -> np.ndarray:
    col, val = g.split("=", 1)
    return (df[col].astype(str) == val).to_numpy()


def _shares(y: pd.Series, w: np.ndarray, m: np.ndarray, options: list[str]) -> np.ndarray:
    v = np.array([float(w[m][(y[m] == o).to_numpy()].sum()) for o in options])
    return v / v.sum() if v.sum() > 0 else np.full(len(options), np.nan)


def draw_cells(bench, tg, groups, demo, ext, draws, seed=0) -> list[dict]:
    """One record per (draw, size, question, group): truth, the sample's group answers, and every AI estimate."""
    df = bench.respondents
    items = [q.id for q in bench.questions if q.id in df.columns]
    w = df["weight"].to_numpy() if "weight" in df.columns else np.ones(len(df))
    gm = {g: _gmask(df, g) for g in groups}
    rng = np.random.default_rng(seed)
    rows = []
    for d in range(draws):
        for n in SIZES:
            for t in tg:
                options = bench.qmap[t].options
                y = df[t]
                valid = y.notna().to_numpy()
                take = rng.choice(np.where(valid)[0], size=min(n, int(valid.sum())), replace=False)
                cal = np.zeros(len(df), bool); cal[take] = True
                hold = valid & ~cal
                overall = _shares(y, w, cal, options)
                own = {}
                if y[cal].nunique() >= 2:
                    others = [i for i in items if i != t]
                    feats = {"demo_own": df[demo].astype(str),
                             "rec_own": pd.concat([df[demo].astype(str), df[others].astype(str)], axis=1)}
                    for name, X in feats.items():
                        enc = OneHotEncoder(handle_unknown="ignore")
                        clf = LogisticRegression(C=0.3, max_iter=3000)
                        clf.fit(enc.fit_transform(X[cal]), y[cal].astype(str), sample_weight=w[cal])
                        pr = clf.predict_proba(enc.transform(X))
                        M = np.zeros((len(df), len(options)))
                        for j, o in enumerate(options):
                            if o in clf.classes_:
                                M[:, j] = pr[:, list(clf.classes_).index(o)]
                        own[name] = M
                for g in groups:
                    hm = hold & gm[g]
                    if hm.sum() < MIN_HOLD or (t, g) not in ext["rec_past"] or (t, g) not in ext["chat"]:
                        continue
                    truth = _shares(y, w, hm, options)
                    if np.isnan(truth).any():
                        continue
                    cm = cal & gm[g]
                    n_g = int(cm.sum())
                    sample = _shares(y, w, cm, options) if n_g > 0 else overall
                    src = {"rec_past": np.asarray(ext["rec_past"][(t, g)], float), "chat": np.asarray(ext["chat"][(t, g)], float)}
                    for name, M in own.items():
                        u = (M[hm] * w[hm, None]).sum(axis=0)
                        src[name] = u / u.sum()
                    if len(src) < 4:
                        continue
                    rows.append({"draw": d, "n": n, "question_id": t, "group": g, "n_group": n_g, "k": len(options),
                                 "truth": truth, "sample": np.nan_to_num(sample), "has_sample": n_g > 0,
                                 **{s: v / v.sum() for s, v in src.items()}})
    return rows


def _stack(rows, key, K):
    out = np.zeros((len(rows), K))
    for i, r in enumerate(rows):
        v = r[key]; out[i, :len(v)] = v
    return out


def _blend(alphas, P, C, nvec):
    num = C * nvec[:, None]
    den = nvec.copy()
    for a, p in zip(alphas, P):
        num = num + a * p
        den = den + a
    return num / den[:, None]


def _jsd(a, b, mask):
    a = np.where(mask, a, 0); b = np.where(mask, b, 0)
    m = 0.5 * (a + b)
    with np.errstate(divide="ignore", invalid="ignore"):
        ka = np.where(a > 0, a * np.log(a / m), 0).sum(1)
        kb = np.where(b > 0, b * np.log(b / m), 0).sum(1)
    return (0.5 * ka + 0.5 * kb) / np.log(2)


def fit_worth(P, C, nvec, T, mask):
    """Worth in respondents for each source, minimising mean JSD (as evaluate/bayes.py does), vectorised."""
    def loss(x):
        return float(_jsd(_blend(np.exp(x), P, C, nvec), T, mask).mean())
    res = minimize(loss, np.full(len(P), np.log(50.0)), method="Nelder-Mead", options={"maxiter": 400, "xatol": 1e-3, "fatol": 1e-7})
    return np.minimum(np.exp(res.x), 5000.0)


def evaluate(rows, tg):
    K = max(r["k"] for r in rows)
    T = _stack(rows, "truth", K); C = _stack(rows, "sample", K)
    mask = np.zeros_like(T, bool)
    for i, r in enumerate(rows):
        mask[i, :r["k"]] = True
    P = {s: _stack(rows, s, K) for s in ["rec_past", "chat", "rec_own", "demo_own"]}
    nvec = np.array([r["n_group"] for r in rows], float)
    has = np.array([r["has_sample"] for r in rows])
    qs = np.array([r["question_id"] for r in rows]); ns = np.array([r["n"] for r in rows])
    kvec = np.array([r["k"] for r in rows], float)
    est = {name: np.zeros_like(T) for name in CONFIGS}
    worth = []
    for name, srcs in CONFIGS.items():
        if not srcs:
            est[name] = C.copy()
            continue
        for n in SIZES:
            for q in tg:
                test = (ns == n) & (qs == q)
                if not test.any():
                    continue
                train = (ns == n) & (qs != q)
                a = fit_worth([P[s][train] for s in srcs], C[train], nvec[train] * has[train], T[train], mask[train])
                worth.append({"config": name, "n": n, "held_out": q, **{s: a[i] for i, s in enumerate(srcs)}})
                est[name][test] = _blend(a, [P[s][test] for s in srcs], C[test], nvec[test] * has[test])
    cells = []
    for name in CONFIGS:
        mae = 100 * (np.abs(est[name] - T) * mask).sum(1) / kvec
        cells.append(pd.DataFrame({"config": name, "draw": [r["draw"] for r in rows], "n": ns, "question_id": qs,
                                   "group": [r["group"] for r in rows], "n_group": nvec, "mae_pts": mae}))
    return pd.concat(cells, ignore_index=True), pd.DataFrame(worth)


def main() -> None:
    t0 = time.time()
    country = sys.argv[1] if len(sys.argv) > 1 else "singapore"
    draws = int(sys.argv[2]) if len(sys.argv) > 2 else 10
    title, bench, tg, groups, demo, rec, chat = setup(country)
    rows = draw_cells(bench, tg, groups, demo, {"rec_past": rec, "chat": chat}, draws)
    print(f"{len(rows)} cells drawn in {time.time() - t0:.0f}s", flush=True)
    cells, worth = evaluate(rows, tg)
    tag = "us" if country == "us" else "singapore"
    cells.to_csv(OUT / f"one_method_{tag}_cells.csv", index=False)
    per_cell = cells.groupby(["config", "n", "question_id", "group"], as_index=False).mae_pts.mean()
    summary = per_cell.groupby(["config", "n"]).mae_pts.agg(["median", "mean"]).reset_index()
    by_draw = cells.groupby(["config", "n", "draw"]).mae_pts.median().groupby(["config", "n"]).agg(["min", "max"]).reset_index()
    summary = summary.merge(by_draw, on=["config", "n"])
    summary.to_csv(OUT / f"one_method_{tag}.csv", index=False)
    w = worth.groupby(["config", "n"]).median(numeric_only=True).round(1).reset_index()
    sizes = cells[cells.config == "survey alone"].groupby(["n", "group"]).n_group.mean().unstack("n").round(0)
    lines = [f"# One method, {title}: a small real survey with and without AI", "",
             f"Generated {time.strftime('%Y-%m-%d %H:%M UTC', time.gmtime())}; runtime {time.time() - t0:.0f}s; "
             f"{draws} draws per survey size; {len(tg)} questions x {len(groups)} groups.", "",
             "Points off per answer option for each group: middle result over groups and questions (average in",
             "brackets; range of the middle result across single draws after it).", "",
             "| method | " + " | ".join(f"survey of {n}" for n in SIZES) + " |", "|---|" + "---|" * len(SIZES)]
    for name in CONFIGS:
        cells_txt = []
        for n in SIZES:
            r = summary[(summary.config == name) & (summary.n == n)].iloc[0]
            cells_txt.append(f"{r['median']:.2f} ({r['mean']:.2f}; {r['min']:.2f}-{r['max']:.2f})")
        lines.append(f"| {name} | " + " | ".join(cells_txt) + " |")
    lines += ["", "Worth of each AI source, in real respondents per group (middle of the leave-one-question-out fits):", "",
              H_table(w), "", "Average number of people from each group in a sample:", "", H_table(sizes.reset_index()), ""]
    (OUT / f"one_method_{tag}.md").write_text("\n".join(lines) + "\n")
    print("\n".join(lines))


def H_table(df: pd.DataFrame) -> str:
    cols = [str(c) for c in df.columns]
    out = ["| " + " | ".join(cols) + " |", "|" + "---|" * len(cols)]
    for r in df.itertuples(index=False):
        out.append("| " + " | ".join("" if (isinstance(v, float) and np.isnan(v)) else str(v) for v in r) + " |")
    return "\n".join(out)


if __name__ == "__main__":
    main()
