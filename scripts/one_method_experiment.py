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

  + chatbot reading records  blended with the chatbot's guesses for each person in the group, made from that
                          person's answers to 57 other questions (scripts/record_reading_trial.py run full)

Usage: one_method_experiment.py [singapore|us] [draws] [standard|boost|reading]
       "boost" draws surveys with extra people from small groups (Singapore: Malay and Indian, 20% each; US: Black
       adults, 30%), weighted back to the population, and writes one_method_<country>_boost.*
       "reading" (Singapore) adds the chatbot reading records, and record citizens learned from the same 57
       questions it read, and writes one_method_singapore_reading.*
       one_method_experiment.py [singapore|us] compare [reading]   (recompute only the comparisons from saved cells)
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
BOTH_KEY = "+ record citizens (own survey) + chatbot kind"
# name -> (sources, mode): "blend" combines the sources with the group's survey answers; "alone" uses the source only
CONFIGS = {
    "survey alone": ([], "blend"),
    "+ chatbot kind": (["chat"], "blend"),
    "+ record citizens": (["rec_past"], "blend"),
    "+ record citizens (own survey)": (["rec_own"], "blend"),
    "+ demographics only (own survey)": (["demo_own"], "blend"),
    "+ record citizens + chatbot kind": (["rec_past", "chat"], "blend"),
    "+ record citizens (own survey) + chatbot kind": (["rec_own", "chat"], "blend"),
    "+ last round's answers": (["last"], "blend"),
    "+ chatbot (Opus)": (["chat_opus"], "blend"),
    "+ chatbot (Sonnet)": (["chat_sonnet"], "blend"),
    "+ chatbot (Haiku)": (["chat_haiku"], "blend"),
    "+ chatbot (Qwen, open, Asian-built)": (["chat_qwen"], "blend"),
    "+ chatbot panel, averaged": (["chat_avg"], "blend"),
    "+ chatbot panel, each weighted": (["chat", "chat_opus", "chat_sonnet", "chat_haiku", "chat_qwen"], "blend"),
    "+ record citizens (own survey) + chatbot panel, averaged": (["rec_own", "chat_avg"], "blend"),
    "+ record citizens (own survey) + chatbot panel, each weighted": (["rec_own", "chat", "chat_opus", "chat_sonnet", "chat_haiku", "chat_qwen"], "blend"),
    "+ record citizens + chatbot panel, each weighted": (["rec_past", "chat", "chat_opus", "chat_sonnet", "chat_haiku", "chat_qwen"], "blend"),
    "+ record citizens (own survey, 5 standard questions)": (["rec_own_k5"], "blend"),
    "+ record citizens (own survey, 10 standard questions)": (["rec_own_k10"], "blend"),
    "+ record citizens (own survey, 20 standard questions)": (["rec_own_k20"], "blend"),
    "+ record citizens (own survey, 10 standard questions) + chatbot kind": (["rec_own_k10", "chat"], "blend"),
    "+ record citizens (own survey, 20 standard questions) + chatbot kind": (["rec_own_k20", "chat"], "blend"),
    "+ chatbot reading records": (["chat_read"], "blend"),
    "+ record citizens (own survey, same 57 questions the chatbot read)": (["rec_own_57"], "blend"),
    "+ record citizens (own survey) + chatbot reading records": (["rec_own", "chat_read"], "blend"),
    "+ record citizens (own survey) + chatbot kind + chatbot reading records": (["rec_own", "chat", "chat_read"], "blend"),
    "chatbot kind alone, no survey": (["chat"], "alone"),
    "chatbot reading records alone, no survey": (["chat_read"], "alone"),
    "record citizens alone, no survey": (["rec_past"], "alone"),
    "last round's answers alone, no survey": (["last"], "alone"),
}
KEY_COMPARISONS = [  # (config A, size A, config B, size B): difference A - B in points off
    ("+ record citizens", 300, "survey alone", 600),
    ("+ record citizens (own survey)", 150, "survey alone", 300),
    ("+ record citizens (own survey)", 300, "survey alone", 600),
    ("+ chatbot kind", 150, "survey alone", 300),
    ("+ chatbot kind", 300, "survey alone", 600),
    ("+ chatbot kind", 150, "+ record citizens (own survey)", 150),
    ("+ chatbot kind", 300, "+ record citizens (own survey)", 300),
    ("+ chatbot kind", 600, "+ record citizens (own survey)", 600),
    ("+ record citizens (own survey) + chatbot kind", 150, "+ record citizens (own survey)", 150),
    ("+ record citizens (own survey) + chatbot kind", 300, "+ record citizens (own survey)", 300),
    ("+ record citizens (own survey) + chatbot kind", 600, "+ record citizens (own survey)", 600),
    ("+ record citizens (own survey) + chatbot kind", 150, "+ chatbot kind", 150),
    ("+ record citizens (own survey) + chatbot kind", 300, "+ chatbot kind", 300),
    ("+ record citizens (own survey) + chatbot kind", 600, "+ chatbot kind", 600),
    ("+ record citizens (own survey) + chatbot kind", 300, "survey alone", 600),
    ("+ record citizens + chatbot kind", 300, "+ record citizens", 300),
    ("+ chatbot panel, averaged", 300, "+ chatbot kind", 300),
    ("+ chatbot panel, each weighted", 300, "+ chatbot kind", 300),
    ("+ record citizens (own survey) + chatbot panel, averaged", 300, BOTH_KEY, 300),
    ("+ record citizens (own survey) + chatbot panel, each weighted", 300, BOTH_KEY, 300),
    ("+ record citizens (own survey, 5 standard questions)", 300, "+ record citizens (own survey)", 300),
    ("+ record citizens (own survey, 10 standard questions)", 300, "+ record citizens (own survey)", 300),
    ("+ record citizens (own survey, 20 standard questions)", 300, "+ record citizens (own survey)", 300),
    ("+ record citizens (own survey, 10 standard questions) + chatbot kind", 300, BOTH_KEY, 300),
    ("+ record citizens (own survey, 20 standard questions) + chatbot kind", 300, BOTH_KEY, 300),
    ("+ record citizens", 300, "+ chatbot kind", 300),  # asked before: record citizens beat the chatbot
    ("+ chatbot reading records", 150, "+ chatbot kind", 150),
    ("+ chatbot reading records", 300, "+ chatbot kind", 300),
    ("+ chatbot reading records", 300, "+ chatbot (Opus)", 300),  # the same make of chatbot, asked the usual way
    ("+ chatbot reading records", 150, "+ record citizens (own survey)", 150),
    ("+ chatbot reading records", 300, "+ record citizens (own survey)", 300),
    ("+ chatbot reading records", 300, "+ record citizens (own survey, same 57 questions the chatbot read)", 300),
    ("+ chatbot reading records", 300, "survey alone", 600),
    ("+ record citizens (own survey) + chatbot reading records", 150, BOTH_KEY, 150),
    ("+ record citizens (own survey) + chatbot reading records", 300, BOTH_KEY, 300),
    ("+ record citizens (own survey) + chatbot reading records", 600, BOTH_KEY, 600),
    ("+ record citizens (own survey) + chatbot kind + chatbot reading records", 300, BOTH_KEY, 300),
    ("+ record citizens (own survey) + chatbot kind + chatbot reading records", 300, "survey alone", 600),
]
PANEL = {"chat_opus": "opus", "chat_sonnet": "sonnet", "chat_haiku": "haiku", "chat_qwen": "qwen"}
KS = (5, 10, 20)


def _load(path: Path) -> dict:
    return {(r["question_id"], r["group"]): r["probs"] for r in json.load(open(path))}


def _with_panel(ext: dict, tag: str) -> dict:
    """Add the other chatbots' blind predictions (docs/results/stress_test/panel_<model>_<country>.json) and their average."""
    chats = {"chat": ext["chat"]}
    for key, name in PANEL.items():
        f = OUT / f"panel_{name}_{tag}.json"
        if f.exists():
            ext[key] = chats[key] = _load(f)
    if len(chats) > 1:
        keys = set.intersection(*(set(c) for c in chats.values()))
        ext["chat_avg"] = {k: list(np.mean([np.asarray(c[k], float) / np.sum(c[k]) for c in chats.values()], axis=0)) for k in keys}
    return ext


def _ranking(tag: str) -> list[str] | None:
    f = OUT / f"standard_questions_{tag}.json"
    return json.load(open(f))["order"] if f.exists() else None


def setup(country: str):
    if country == "us":
        packet = json.load(open(OUT / "packet_gss.json"))
        tg, groups = [q["id"] for q in packet["questions"]], [g for g in packet["groups"] if g != "ALL"]
        bench, b22 = gss.benchmark(2024), gss.benchmark(2022, segment_keys=["sex"])
        demo = ["age_band", "sex", "race_eth", "education", "region", "income4", "religion4"]
        rec = cross_country_transfer([b22], bench, tg, demo, groups + ["ALL"], C=0.3, min_n=30)
        chat = _load(OUT / "predictions_gss_claude_in_session.json")
        last = {k: d.normalised() for k, d in gss.benchmark(2022).real.items()}  # same questions, asked two years earlier
        return "the United States", bench, tg, groups, demo, _with_panel({"rec_past": rec, "chat": chat, "last": last}, "us")
    packet = json.load(open(OUT / "packet_wvs_singapore.json"))
    tg, groups = [q["id"] for q in packet["questions"]], [g for g in packet["groups"] if g != "ALL"]
    bench = wvs.benchmark("Singapore")
    demo = ["sex", "age_band", "ethnic", "religion", "education3", "income3", "born_in_country"]
    rec = _load(OUT / "record_all_singapore_pred.json")
    chat = _load(OUT / "predictions_wvs_singapore_claude_in_session.json")
    return "Singapore", bench, tg, groups, demo, _with_panel({"rec_past": rec, "chat": chat}, "singapore")


def _gmask(df: pd.DataFrame, g: str) -> np.ndarray:
    col, val = g.split("=", 1)
    return (df[col].astype(str) == val).to_numpy()


def _shares(y: pd.Series, w: np.ndarray, m: np.ndarray, options: list[str]) -> np.ndarray:
    v = np.array([float(w[m][(y[m] == o).to_numpy()].sum()) for o in options])
    return v / v.sum() if v.sum() > 0 else np.full(len(options), np.nan)


def _boost_strata(df: pd.DataFrame, tag: str):
    """Small groups to over-sample and their share of the sample."""
    if tag == "us":
        return {"race_eth=Black, non-Hispanic": 0.30}
    return {"ethnic=Malay": 0.20, "ethnic=Indian": 0.20}


def _reading(df: pd.DataFrame, tg, bench) -> dict:
    """Per-person guesses of the chatbot reading records, as {question: array [person, option]}, NaN where not guessed."""
    P = json.load(open(Path("docs/results/record_reading_full_predictions.json")))["predictions"]["record"]
    out = {}
    for t in tg:
        M = np.full((len(df), len(bench.qmap[t].options)), np.nan)
        for i, pid in enumerate(df.pid):
            if pid in P:
                M[i] = P[pid][t]
        out[t] = M
    return out


def draw_cells(bench, tg, groups, demo, ext, draws, seed=0, design="standard", ranking=None, tag="singapore", reading=None) -> list[dict]:
    """One record per (draw, size, question, group): truth, the sample's group answers, and every AI estimate."""
    df = bench.respondents
    items = [q.id for q in bench.questions if q.id in df.columns]
    record_items = [i for i in items if i not in tg]  # the 57 questions the chatbot reading records was shown
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
                ws = w.copy()
                if design == "boost":
                    quotas = _boost_strata(df, tag)
                    rest = valid.copy()
                    take = []
                    for g_, share in quotas.items():
                        members = valid & _gmask(df, g_)
                        rest &= ~members
                        k = int(round(n * share))
                        take.append(rng.choice(np.where(members)[0], size=min(k, int(members.sum())), replace=False))
                        ws[members] = w[members] * (w[members].sum() / w[valid].sum()) / (k / n)  # weight back to the population
                    k_rest = n - sum(len(t_) for t_ in take)
                    take.append(rng.choice(np.where(rest)[0], size=k_rest, replace=False))
                    ws[rest] = w[rest] * (w[rest].sum() / w[valid].sum()) / (k_rest / n)
                    take = np.concatenate(take)
                else:
                    take = rng.choice(np.where(valid)[0], size=min(n, int(valid.sum())), replace=False)
                cal = np.zeros(len(df), bool); cal[take] = True
                hold = valid & ~cal
                overall = _shares(y, ws, cal, options)
                own = {}
                if y[cal].nunique() >= 2:
                    others = [i for i in items if i != t]
                    feats = {"demo_own": df[demo].astype(str),
                             "rec_own": pd.concat([df[demo].astype(str), df[others].astype(str)], axis=1)}
                    if ranking and design == "standard":
                        for k_ in KS:
                            short = [i for i in ranking if i != t and i in others][:k_]
                            feats[f"rec_own_k{k_}"] = pd.concat([df[demo].astype(str), df[short].astype(str)], axis=1)
                    if reading is not None:
                        feats["rec_own_57"] = pd.concat([df[demo].astype(str), df[record_items].astype(str)], axis=1)
                    for name, X in feats.items():
                        enc = OneHotEncoder(handle_unknown="ignore")
                        clf = LogisticRegression(C=0.3, max_iter=3000)
                        clf.fit(enc.fit_transform(X[cal]), y[cal].astype(str), sample_weight=ws[cal])
                        pr = clf.predict_proba(enc.transform(X))
                        M = np.zeros((len(df), len(options)))
                        for j, o in enumerate(options):
                            if o in clf.classes_:
                                M[:, j] = pr[:, list(clf.classes_).index(o)]
                        own[name] = M
                for g in groups:
                    hm = hold & gm[g]
                    if hm.sum() < MIN_HOLD:
                        continue
                    truth = _shares(y, w, hm, options)
                    if np.isnan(truth).any():
                        continue
                    cm = cal & gm[g]
                    n_g = int(cm.sum())
                    sample = _shares(y, ws, cm, options) if n_g > 0 else overall
                    if any((t, g) not in e for e in ext.values()):
                        continue
                    src = {name: np.asarray(e[(t, g)], float) for name, e in ext.items()}
                    for name, M in own.items():
                        u = (M[hm] * w[hm, None]).sum(axis=0)
                        src[name] = u / u.sum()
                    if reading is not None:  # the people being estimated, as the chatbot guessed each of them
                        rm = hm & ~np.isnan(reading[t][:, 0])
                        u = (reading[t][rm] * w[rm, None]).sum(axis=0)
                        src["chat_read"] = u / u.sum()
                    if "rec_own" not in src:
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


LOG_LO, LOG_HI = np.log(0.01), np.log(5000.0)


def fit_worth(P, C, nvec, T, mask):
    """Worth in respondents for each source, minimising mean JSD (as evaluate/bayes.py does), vectorised.

    Worths are limited to 0.01-5,000 respondents inside the search, so the balance between sources that is
    actually used is the one that was optimised (capping each source afterwards would distort it)."""
    def loss(x):
        return float(_jsd(_blend(np.exp(np.clip(x, LOG_LO, LOG_HI)), P, C, nvec), T, mask).mean())
    res = minimize(loss, np.full(len(P), np.log(50.0)), method="Nelder-Mead", options={"maxiter": 400 * len(P), "xatol": 1e-3, "fatol": 1e-7})
    return np.exp(np.clip(res.x, LOG_LO, LOG_HI))


def evaluate(rows, tg):
    K = max(r["k"] for r in rows)
    T = _stack(rows, "truth", K); C = _stack(rows, "sample", K)
    mask = np.zeros_like(T, bool)
    for i, r in enumerate(rows):
        mask[i, :r["k"]] = True
    skip = {"draw", "n", "question_id", "group", "n_group", "k", "truth", "sample", "has_sample"}
    P = {s: _stack(rows, s, K) for s in rows[0] if s not in skip}
    nvec = np.array([r["n_group"] for r in rows], float)
    has = np.array([r["has_sample"] for r in rows])
    qs = np.array([r["question_id"] for r in rows]); ns = np.array([r["n"] for r in rows])
    kvec = np.array([r["k"] for r in rows], float)
    configs = {k: v for k, v in CONFIGS.items() if all(s in P for s in v[0])}
    est = {name: np.zeros_like(T) for name in configs}
    worth = []
    for name, (srcs, mode) in configs.items():
        if not srcs:
            est[name] = C.copy()
            continue
        if mode == "alone":
            est[name] = P[srcs[0]].copy()
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
    for name in configs:
        mae = 100 * (np.abs(est[name] - T) * mask).sum(1) / kvec
        cells.append(pd.DataFrame({"config": name, "draw": [r["draw"] for r in rows], "n": ns, "question_id": qs,
                                   "group": [r["group"] for r in rows], "n_group": nvec, "mae_pts": mae}))
    return pd.concat(cells, ignore_index=True), pd.DataFrame(worth)


def _cube(cells, config, n):
    """mae as an array [question, group, draw] for one method and survey size."""
    c = cells[(cells.config == config) & (cells.n == n)]
    return c.pivot_table(index=["question_id", "group"], columns="draw", values="mae_pts")


def bootstrap(cells, B=1000, seed=1):
    """95% intervals for each middle result, and for the key differences, resampling questions and draws."""
    rng = np.random.default_rng(seed)
    qs = sorted(cells.question_id.unique())
    cubes = {(c, n): _cube(cells, c, n) for c in cells.config.unique() for n in SIZES}
    q_draws = [rng.integers(0, len(qs), len(qs)) for _ in range(B)]

    arrays = {key: (cube.to_numpy(), {q: np.where(cube.index.get_level_values(0) == q)[0] for q in qs}) for key, cube in cubes.items()}

    def resample(key, qi, di):
        arr, qpos = arrays[key]
        rows_ = np.concatenate([qpos[qs[i]] for i in qi])
        return np.median(arr[rows_][:, di].mean(axis=1))

    ci, diffs = {}, []
    d_draws = {key: [rng.integers(0, cube.shape[1], cube.shape[1]) for _ in range(B)] for key, cube in cubes.items()}
    boot = {key: np.array([resample(key, q_draws[b], d_draws[key][b]) for b in range(B)]) for key in cubes}
    for key, v in boot.items():
        ci[key] = (np.percentile(v, 2.5), np.percentile(v, 97.5))
    for a, na, b_, nb in KEY_COMPARISONS:
        if (a, na) in boot and (b_, nb) in boot:
            point = np.median(cubes[(a, na)].mean(axis=1)) - np.median(cubes[(b_, nb)].mean(axis=1))
            dv = boot[(a, na)] - boot[(b_, nb)]
            diffs.append({"a": a, "n_a": na, "b": b_, "n_b": nb, "difference": point,
                          "low": np.percentile(dv, 2.5), "high": np.percentile(dv, 97.5)})
    return ci, pd.DataFrame(diffs)


def compare_only(tag: str) -> None:
    """Recompute the key comparisons from the saved cells (same bootstrap draws) and update the .md section."""
    cells = pd.read_csv(OUT / f"one_method_{tag}_cells.csv")
    _, diffs = bootstrap(cells)
    diffs.to_csv(OUT / f"one_method_{tag}_comparisons.csv", index=False)
    md = (OUT / f"one_method_{tag}.md").read_text()
    head, rest = md.split("Key comparisons", 1)
    tail = rest[rest.index("Worth of each AI source"):]
    block = ["Key comparisons (difference in points off, A minus B; negative means A is closer; 95% interval):", "",
             "| A | B | difference | 95% interval |", "|---|---|---|---|"]
    for r in diffs.itertuples():
        block.append(f"| {r.a}, survey of {r.n_a} | {r.b}, survey of {r.n_b} | {r.difference:+.2f} | {r.low:+.2f} to {r.high:+.2f} |")
    (OUT / f"one_method_{tag}.md").write_text(head + "\n".join(block) + "\n\n" + tail)
    print("\n".join(block))


def main() -> None:
    t0 = time.time()
    country = sys.argv[1] if len(sys.argv) > 1 else "singapore"
    if len(sys.argv) > 2 and sys.argv[2] == "compare":
        compare_only(("us" if country == "us" else "singapore") + ("_reading" if sys.argv[3:4] == ["reading"] else ""))
        return
    draws = int(sys.argv[2]) if len(sys.argv) > 2 else 10
    design = sys.argv[3] if len(sys.argv) > 3 else "standard"
    title, bench, tg, groups, demo, ext = setup(country)
    reading = _reading(bench.respondents, tg, bench) if design == "reading" else None
    tag0 = "us" if country == "us" else "singapore"
    cache = Path("data/cache") / f"one_method_{tag0}_{design}_{draws}_rows.pkl"
    if cache.exists():
        rows = pd.read_pickle(cache)
        print(f"reused {len(rows)} cached cells from {cache}", flush=True)
    else:
        rows = draw_cells(bench, tg, groups, demo, ext, draws, design="standard" if reading else design,
                          ranking=_ranking(tag0), tag=tag0, reading=reading)
        cache.parent.mkdir(parents=True, exist_ok=True)
        pd.to_pickle(rows, cache)
    print(f"{len(rows)} cells drawn in {time.time() - t0:.0f}s", flush=True)
    cells, worth = evaluate(rows, tg)
    tag = tag0 + ("_" + design if design in ("boost", "reading") else "")
    cells.to_csv(OUT / f"one_method_{tag}_cells.csv", index=False)
    per_cell = cells.groupby(["config", "n", "question_id", "group"], as_index=False).mae_pts.mean()
    summary = per_cell.groupby(["config", "n"]).mae_pts.agg(["median", "mean"]).reset_index()
    ci, diffs = bootstrap(cells)
    summary["low"] = [ci[(r.config, r.n)][0] for r in summary.itertuples()]
    summary["high"] = [ci[(r.config, r.n)][1] for r in summary.itertuples()]
    summary.to_csv(OUT / f"one_method_{tag}.csv", index=False)
    diffs.to_csv(OUT / f"one_method_{tag}_comparisons.csv", index=False)
    w = worth.groupby(["config", "n"]).median(numeric_only=True).round(1).reset_index()
    sizes = cells[cells.config == "survey alone"].groupby(["n", "group"]).n_group.mean().unstack("n").round(0)
    lines = [f"# One method, {title}: a small real survey with and without AI" + {"boost": " (small groups boosted)", "reading": " (with the chatbot reading records)"}.get(design, ""), "",
             f"Generated {time.strftime('%Y-%m-%d %H:%M UTC', time.gmtime())}; runtime {time.time() - t0:.0f}s; "
             f"{draws} draws per survey size; {len(tg)} questions x {len(groups)} groups.", "",
             "Points off per answer option for each group: middle result over groups and questions of the",
             "per-cell average across draws (average in brackets; 95% interval from resampling questions and",
             "draws after it). Part of every score is chance in the people the estimate is checked against.", "",
             "| method | " + " | ".join(f"survey of {n}" for n in SIZES) + " |", "|---|" + "---|" * len(SIZES)]
    for name in [c for c in CONFIGS if c in set(summary.config)]:
        cells_txt = []
        for n in SIZES:
            r = summary[(summary.config == name) & (summary.n == n)].iloc[0]
            cells_txt.append(f"{r['median']:.2f} ({r['mean']:.2f}; {r['low']:.2f}-{r['high']:.2f})")
        lines.append(f"| {name} | " + " | ".join(cells_txt) + " |")
    lines += ["", "Key comparisons (difference in points off, A minus B; negative means A is closer; 95% interval):", "",
              "| A | B | difference | 95% interval |", "|---|---|---|---|"]
    for r in diffs.itertuples():
        lines.append(f"| {r.a}, survey of {r.n_a} | {r.b}, survey of {r.n_b} | {r.difference:+.2f} | {r.low:+.2f} to {r.high:+.2f} |")
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
