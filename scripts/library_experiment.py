"""Does the 'library' work? A new question arrives; search the library for the closest previously asked
question; use that survey as the base; spread with record-anchored citizens; score against truth.

Test bed: the United States, where two different surveys of the same population exist on disk.
  * New questions = 31 World Values Survey (wave 7, US) items, with group-level truth.
  * Library       = General Social Survey 2022 and 2024 (real respondents, 84 items), hand-matched to the
                    WVS items at three levels of closeness (exact / close / loose).
  * Spread        = record-anchored citizens: each US WVS respondent's answer to the new question predicted
                    from their other answers, with the mapping learned on the other 61 WVS countries.
Everything is scored on common answer bins, for the population and for 20 harmonised groups.

Usage: .venv/bin/python -I scripts/library_experiment.py [--skip-record]  (record model is cached)
"""
from __future__ import annotations

import json
import sys
import time
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from digital_citizens.data import gss, wvs  # noqa: E402
from digital_citizens.evaluate import harness as H  # noqa: E402
from digital_citizens.data.benchmark import Benchmark  # noqa: E402
from digital_citizens.evaluate.transfer import cross_country_transfer, small_survey_holdout  # noqa: E402
from digital_citizens.library import crosswalk_us as X  # noqa: E402
from digital_citizens.library import harmonise as HM  # noqa: E402
from digital_citizens.library.search import match_questions  # noqa: E402

OUT = Path("docs/results/library_test")
CACHE = OUT / "record_all_us_pred.json"
DEMO = ["sex", "age_band", "education3", "income3", "religion", "born_in_country"]
MIN_GROUP_N = 50
SMALL_N = 300


def load_us():
    items = list(wvs.ITEMS) + X.EXTRA_WVS_ITEMS
    bench = wvs.benchmark("United States", items=items, segment_keys=["sex"])
    bench.respondents = HM.harmonise_wvs_us(bench.respondents)
    return bench, items


def record_model(bench, targets, groups, items):
    """Record-anchored citizens for the US: mapping learned on every other WVS7 country. Cached per question
    so an interrupted run resumes where it stopped."""
    pred: dict = {}
    if CACHE.exists():
        pred = {tuple(k.split("|")): v for k, v in json.load(open(CACHE)).items()}
    todo = [t for t in targets if not any(q == t for q, _ in pred)]
    if not todo:
        return pred
    t0 = time.time()
    train = []
    for name in sorted(wvs.available_countries()):
        if name == "United States":
            continue
        try:
            train.append(wvs.benchmark(name, items=items, segment_keys=["sex"]))
        except Exception as e:  # noqa: BLE001
            print("skip", name, type(e).__name__, str(e)[:80], flush=True)
    print(f"record model: training on {len(train)} countries, {sum(len(b.respondents) for b in train):,} people; {len(todo)} questions to do", flush=True)
    for i, t in enumerate(todo):
        pred.update(cross_country_transfer(train, bench, [t], DEMO, groups, C=0.3, min_n=MIN_GROUP_N))
        json.dump({"|".join(k): v for k, v in pred.items()}, open(CACHE, "w"))
        print(f"  {i+1}/{len(todo)} {t} done, {time.time()-t0:.0f}s elapsed", flush=True)
    print(f"record model done in {time.time()-t0:.0f}s, {len(pred)} cells", flush=True)
    return pred


def bench_like(template: Benchmark, real: dict) -> Benchmark:
    from digital_citizens.schema import Distribution
    return Benchmark(name=template.name, country=template.country, questions=template.questions, real={k: Distribution(question_id=k[0], group=k[1], probs=v, n=0) for k, v in real.items()}, segment_keys=template.segment_keys)


def summarise(variants, truth, groups, floor):
    """``variants`` values are a prediction dict, or a list of (prediction dict, truth dict) pairs for methods
    that are repeated on fresh random samples: each repeat is scored against its own hold-out truth and the
    per-cell scores are averaged over repeats."""
    rows, cells = [], []
    for name, pred in variants.items():
        if isinstance(pred, list):
            ss, segs = [], []
            for p_rep, t_rep in pred:
                b = bench_like(truth, t_rep)
                ss.append(H.score(p_rep, b, name)); segs.append(H.segment_fidelity(p_rep, b, name))
            s = pd.concat(ss).groupby(["method", "question_id", "group"], as_index=False).agg({"k": "first", "ordinal": "first", "n_real": "first", "jsd": "mean", "tv": "mean", "mae_pts": "mean", "top_box_err": "mean", "max_abs_err": "mean", "entropy_ratio": "mean"})
            seg = pd.concat(segs).groupby(["method", "question_id"], as_index=False)[["gap_r", "gap_slope", "dispersion_ratio"]].mean()
        else:
            s = H.score(pred, truth, name)
            seg = H.segment_fidelity(pred, truth, name)
        s = s[s.group.isin(groups)]
        s = s.merge(floor[["question_id", "group", "mae_floor"]], on=["question_id", "group"], how="left")
        cells.append(s)
        pop, sg = s[s.group == "ALL"], s[s.group != "ALL"]
        rows.append({"method": name, "pop_mae_median": pop.mae_pts.median(), "pop_mae_mean": pop.mae_pts.mean(), "seg_mae_median": sg.mae_pts.median(), "seg_mae_mean": sg.mae_pts.mean(),
                     "seg_mae_over_floor": (sg.mae_pts - sg.mae_floor).median(), "gap_r": seg.gap_r.median(), "gap_slope": seg.gap_slope.median(), "n_items": pop.question_id.nunique(), "n_cells": len(s)})
    return pd.DataFrame(rows), pd.concat(cells, ignore_index=True)


def main() -> None:
    t0 = time.time()
    OUT.mkdir(parents=True, exist_ok=True)
    skip_record = "--skip-record" in sys.argv
    pairs = X.PAIRS
    targets = [p["wvs"] for p in pairs]
    quality = {p["wvs"]: p["quality"] for p in pairs}
    label = {p["wvs"]: p["label"] for p in pairs}
    gss_of = {p["wvs"]: p["gss"] for p in pairs}

    # --- the new questions and their truth (WVS US, on common bins)
    us, items = load_us()
    groups = HM.groups_of(us.respondents, HM.SEGMENTS, MIN_GROUP_N)
    truth = HM.truth_benchmark(us.respondents, us.qmap, pairs, groups, min_n=MIN_GROUP_N)
    floor = HM.mae_noise_floor(truth)
    real = {k: d.normalised() for k, d in truth.real.items()}
    print(f"truth: {len(truth.real)} cells, groups={groups}", flush=True)

    # --- the library: GSS 2024 and 2022
    g24 = HM.harmonise_gss(gss.load_respondents(2024))
    g22 = HM.harmonise_gss(gss.load_respondents(2022))
    lib24, n24 = HM.library_predictions(g24, gss.ITEMS, pairs, groups)
    lib22, _ = HM.library_predictions(g22, gss.ITEMS, pairs, groups)
    headline24 = {(q, g): lib24[(q, "ALL")] for q in targets for g in groups if (q, "ALL") in lib24}

    # --- step 1 test: can wording search find the right library question?
    wvs_texts = {q.id: q.text for q in us.questions}
    gss_texts = {k: v[0] for k, v in gss.ITEMS.items()}
    mrows = []
    for method in ("tfidf", "semantic"):
        for qid, ranked in match_questions(wvs_texts, gss_texts, top=3, method=method).items():
            truth_gss = gss_of.get(qid)
            rank = next((i + 1 for i, (g, _) in enumerate(ranked) if g == truth_gss), None) if truth_gss else None
            mrows.append({"matcher": method, "wvs_item": qid, "in_crosswalk": qid in gss_of, "quality": quality.get(qid, "-"), "hand_match": truth_gss or "-", "top1": ranked[0][0], "top1_sim": ranked[0][1], "rank_of_hand_match": rank})
    mdf_all = pd.DataFrame(mrows)
    mdf_all.to_csv(OUT / "search_matches.csv", index=False)
    msum = mdf_all.groupby("matcher").apply(lambda d: pd.Series({"items_with_a_match": int(d.in_crosswalk.sum()), "right_match_first": int((d.rank_of_hand_match == 1).sum()), "right_match_in_top3": int(d.rank_of_hand_match.notna().sum()),
                                                                "median_sim_when_match_exists": d[d.in_crosswalk].top1_sim.median(), "median_sim_when_no_match": d[~d.in_crosswalk].top1_sim.median(),
                                                                "no-match_items_scoring_above_median_matched": int((d[~d.in_crosswalk].top1_sim > d[d.in_crosswalk].top1_sim.median()).sum()), "no-match_items": int((~d.in_crosswalk).sum())}), include_groups=False).reset_index()
    mdf = mdf_all[mdf_all.matcher == "semantic"]

    # --- step 2/3: record-anchored spread (cached) and small fresh survey
    variants = {
        "uniform": {k: [1 / len(v)] * len(v) for k, v in real.items()},
        "everyone is average (true level, no spread) [oracle]": {(q, g): real[(q, "ALL")] for (q, g) in real},
        "library 2024: matched GSS question, used as is": lib24,
        "library 2022: matched GSS question, used as is": lib22,
        "library 2024: headline only, no spread": headline24,
    }
    if not skip_record:
        rec_full = record_model(us, targets, groups, items)
        rec = HM.map_to_bins(rec_full, pairs)
        variants["record citizens alone (61-country model, no library)"] = rec
        variants["library 2024 headline + record spread"] = HM.relevel(rec, headline24, groups)
        variants["library 2024 as is, averaged with headline + record spread"] = HM.average(lib24, HM.relevel(rec, headline24, groups))
        variants["true level + record spread [oracle level]"] = HM.relevel(rec, real, groups)
        reps = small_survey_holdout(us, targets, DEMO, groups, n_cal=SMALL_N, reps=5, min_n=MIN_GROUP_N)
        tr = [HM.map_to_bins(r["truth"], pairs) for r in reps]
        variants[f"fresh small survey (n={SMALL_N}): crosstab only"] = [(HM.map_to_bins(r["crosstab"], pairs), t) for r, t in zip(reps, tr)]
        variants[f"fresh small survey (n={SMALL_N}) + record spread"] = [(HM.map_to_bins(r["demographics + record model"], pairs), t) for r, t in zip(reps, tr)]
        variants[f"fresh small survey (n={SMALL_N}) + demographics-only spread"] = [(HM.map_to_bins(r["demographics model"], pairs), t) for r, t in zip(reps, tr)]
        variants[f"library 2024 as is, averaged with small survey (n={SMALL_N}) + record spread"] = [(HM.average(lib24, HM.map_to_bins(r["demographics + record model"], pairs)), t) for r, t in zip(reps, tr)]

    conf = [p["wvs"] for p in pairs if p["label"].startswith("Confidence")]
    anchored = {}
    for q in conf:
        others = [o for o in conf if o != q and (o, "ALL") in real and (o, "ALL") in lib24]
        shift = np.mean([np.asarray(real[(o, "ALL")]) - np.asarray(lib24[(o, "ALL")]) for o in others], axis=0)
        for g in groups:
            if (q, g) in lib24:
                v = np.clip(np.asarray(lib24[(q, g)]) + shift, 1e-6, None)
                anchored[(q, g)] = (v / v.sum()).tolist()
    variants["library 2024 + survey-difference shift learned from the other 9 confidence questions (anchors) [confidence items only]"] = anchored

    summ, cells = summarise(variants, truth, groups, floor)
    cells["quality"] = cells.question_id.map(quality)
    cells["label"] = cells.question_id.map(label)
    cells.to_csv(OUT / "library_test_us_cells.csv", index=False)
    summ.round(2).to_csv(OUT / "library_test_us.csv", index=False)

    # by match quality
    byq = cells[cells.group != "ALL"].groupby(["method", "quality"]).mae_pts.median().unstack("quality").reindex(columns=["exact", "close", "loose"])
    byq_pop = cells[cells.group == "ALL"].groupby(["method", "quality"]).mae_pts.median().unstack("quality").reindex(columns=["exact", "close", "loose"])
    # per item
    key_methods = [m for m in variants if m.startswith("library 2024: matched") or m.startswith("library 2024 headline + record") or m.startswith("record citizens") or m.startswith("fresh small survey (n=300) +") or m.startswith("library 2024 as is, averaged with small")]
    per_item = cells[cells.group != "ALL"].groupby(["question_id", "method"]).mae_pts.median().unstack("method")[key_methods]
    per_item.insert(0, "quality", per_item.index.map(quality)); per_item.insert(0, "gss_match", per_item.index.map(gss_of)); per_item.insert(0, "question", per_item.index.map(label))
    per_item_pop = cells[cells.group == "ALL"].set_index(["question_id", "method"]).mae_pts.unstack("method")[key_methods]
    # by group
    by_group = cells[cells.group != "ALL"].groupby(["group", "method"]).mae_pts.median().unstack("method")[key_methods]
    by_group.insert(0, "n_truth", cells[cells.group != "ALL"].groupby("group").n_real.median().astype(int))
    by_group.insert(1, "n_gss2024", pd.Series({g: int(np.median([n for (q, gg), n in n24.items() if gg == g])) for g in by_group.index}))
    # worked examples
    ex = []
    for q, bin_i in [("Q57", 0), ("Q182", 2), ("Q73", 0), ("Q171", 0), ("Q184", 1)]:
        for g in ["ALL", "age_band4=18-29", "age_band4=60+", "race_eth=Black, non-Hispanic", "race_eth=Hispanic", "religion4=No religion", "religion4=Protestant", "region4=South"]:
            if (q, g) in real:
                row = {"question": f"{label[q]}: {truth.qmap[q].options[bin_i]}", "group": g, "real": 100 * real[(q, g)][bin_i]}
                for m in key_methods:
                    v = variants[m][0][0] if isinstance(variants[m], list) else variants[m]
                    row[m] = 100 * v[(q, g)][bin_i] if (q, g) in v else None
                ex.append(row)
    exdf = pd.DataFrame(ex)

    lines = ["# Library test: United States (GSS as the library, WVS as the new questions)", "", f"Generated {time.strftime('%Y-%m-%d %H:%M')} UTC; runtime {time.time()-t0:.0f}s.", "",
             f"New questions: {len(targets)} WVS-7 US items (exact {sum(v=='exact' for v in quality.values())}, close {sum(v=='close' for v in quality.values())}, loose {sum(v=='loose' for v in quality.values())} matches). "
             f"Truth: WVS US (n={len(us.respondents):,}, fielded 2017) on common bins, {len(groups)} groups ({len(groups)-1} segments, min n={MIN_GROUP_N}). Library: GSS 2024 (n={len(g24):,}) and GSS 2022 (n={len(g22):,}). "
             f"Noise floor: median {floor[floor.group=='ALL'].mae_floor.median():.1f} pts (population), {floor[floor.group!='ALL'].mae_floor.median():.1f} pts (segments). All errors are mean absolute error per bin, in percentage points. "
             f"'Fresh small survey' rows: {SMALL_N} random respondents answer the question; scored against the other respondents (no overlap), 5 repeats, scores averaged.", "",
             "## Step 1: can a wording search find the right library question?", "",
             f"Two automatic matchers, scored against the hand-checked crosswalk over all {len(wvs_texts)} WVS items ({len(gss_of)} have a GSS match, {len(wvs_texts)-len(gss_of)} do not):", "",
             H.to_markdown(msum, 2), "",
             "The last two columns matter: a no-match item that scores as high as a matched one would be given a wrong 'closest question' by an unattended search.", "",
             "Semantic matcher, item by item:", "", H.to_markdown(mdf[mdf.in_crosswalk].drop(columns=["in_crosswalk", "matcher"]), 2), "",
             "## Steps 2-3: how good is the answer, by method", "", H.to_markdown(summ, 2), "",
             "`seg_mae_over_floor` is the median segment error minus what survey sampling noise alone would produce; `gap_r`/`gap_slope` say whether group differences are reproduced (1 = perfectly).", "",
             "## By how close the library match is (segment error, median points)", "", H.to_markdown(byq.reset_index(), 2), "",
             "### Population level, by match quality", "", H.to_markdown(byq_pop.reset_index(), 2), "",
             "## Per question (segment error, median points)", "", H.to_markdown(per_item.reset_index(), 1), "",
             "### Per question, population level", "", H.to_markdown(per_item_pop.reset_index(), 1), "",
             "## Per group (median over questions)", "", H.to_markdown(by_group.reset_index(), 1), "",
             "## Worked examples (share choosing the option, %)", "", H.to_markdown(exdf, 1), ""]
    (OUT / "library_test_us.md").write_text("\n".join(lines))
    print("\n".join(lines))


if __name__ == "__main__":
    main()
