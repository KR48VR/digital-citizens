"""Command-line entry points.

  dc baselines gss        -> docs/results/baselines_gss2024.md
  dc baselines goqa       -> docs/results/baselines_globalopinionqa.md
  dc baselines twin2k     -> docs/results/baselines_twin2k.md
  dc personas singapore   -> demographic report on the Nemotron Singapore persona bank
  dc simulate gss --mode distribution --model claude-sonnet-5-5 --limit 20   (needs ANTHROPIC_API_KEY; --mock for a dry run)
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd

from .data import globalopinionqa, gss, nemotron, wvs
from .evaluate import baselines as B
from .evaluate import harness as H
from .evaluate.individual import evaluate_twin2k

RESULTS = Path("docs/results")
GOQA_COUNTRIES = ["United States", "China", "Singapore", "Japan", "Germany", "Britain", "India (Current national sample)", "Indonesia", "Malaysia", "S. Korea", "Vietnam", "Taiwan ROC"]


def _write(name: str, text: str) -> Path:
    RESULTS.mkdir(parents=True, exist_ok=True)
    p = RESULTS / name
    p.write_text(text)
    print(f"wrote {p}")
    return p


def baselines_gss(args: argparse.Namespace) -> None:
    b24, b22 = gss.benchmark(2024), gss.benchmark(2022)
    preds = {
        "uniform": B.uniform(b24),
        "population_marginal_for_segments": B.population_marginal(b24),
        "previous_wave_2022": B.previous_wave(b24, b22),
    }
    reg: dict = {}
    for q in b24.questions:
        if q.id in b22.respondents.columns:
            reg.update(B.demographic_regression(b22.respondents, b24.respondents, q.id, q.options, ["age_band", "sex", "race_eth", "education", "region", "party3", "ideology3", "income4", "religion4", "urbanicity"], b24.segment_keys))
    preds["demographic_regression_2022->2024"] = reg
    scored = pd.concat([H.score(p, b24, name) for name, p in preds.items()], ignore_index=True)
    scored["level"] = np.where(scored["group"] == "ALL", "population", "segment")
    floor = H.noise_floor(b24)
    floor["level"] = np.where(floor["group"] == "ALL", "population", "segment")
    seg = pd.concat([H.segment_fidelity(p, b24, name) for name, p in preds.items() if name != "population_marginal_for_segments"], ignore_index=True)
    lines = [
        "# Baselines on GSS 2024 (United States)", "",
        f"Questions: {len(b24.questions)}; respondents: {len(b24.respondents)}; cells (question x group): {len(b24.real)}; segments: {', '.join(b24.segment_keys)}.", "",
        "These are the free, no-LLM predictions a digital-citizen simulator has to beat. Lower JSD/TV is better; entropy_ratio and dispersion_ratio should be near 1.", "",
        "## Population level (group = ALL)", "",
        H.to_markdown(H.summarise(scored[scored.level == "population"], ("method",))), "",
        f"Survey sampling-noise floor (expected JSD of a perfect simulator vs this survey's own sample): median {floor[floor.level=='population'].jsd_noise_floor.median():.4f}", "",
        "## Segment level (all question x segment cells)", "",
        H.to_markdown(H.summarise(scored[scored.level == "segment"], ("method",))), "",
        f"Sampling-noise floor at segment level: median JSD {floor[floor.level=='segment'].jsd_noise_floor.median():.4f}", "",
        "## Does the prediction reproduce how segments differ? (per question, averaged)", "",
        H.to_markdown(seg.groupby("method")[["gap_r", "gap_slope", "dispersion_ratio"]].median().reset_index()), "",
        "## Segment level by segment type (median JSD)", "",
    ]
    scored["segment_type"] = scored["group"].str.split("=").str[0]
    piv = scored[scored.level == "segment"].pivot_table(index="segment_type", columns="method", values="jsd", aggfunc="median").reset_index()
    lines += [H.to_markdown(piv), ""]
    _write("baselines_gss2024.md", "\n".join(lines))
    scored.to_csv(RESULTS / "baselines_gss2024_cells.csv", index=False)


def baselines_wvs(args: argparse.Namespace) -> None:
    country = (args.countries or ["Singapore"])[0]
    b = wvs.benchmark(country)
    preds = {"uniform": B.uniform(b), "population_marginal_for_segments": B.population_marginal(b)}
    scored = pd.concat([H.score(p, b, name) for name, p in preds.items()], ignore_index=True)
    scored["level"] = np.where(scored["group"] == "ALL", "population", "segment")
    scored["segment_type"] = scored["group"].str.split("=").str[0]
    floor = H.noise_floor(b)
    floor["level"] = np.where(floor["group"] == "ALL", "population", "segment")
    tag = wvs.COUNTRY_FILES[country].lower()
    lines = [f"# Baselines on WVS wave 7, {country}", "",
             f"Questions: {len(b.questions)}; respondents: {len(b.respondents)}; cells: {len(b.real)}; segments: {', '.join(b.segment_keys)}.", "",
             "## Population level", "", H.to_markdown(H.summarise(scored[scored.level == 'population'], ('method',))), "",
             f"Sampling-noise floor: median JSD {floor[floor.level=='population'].jsd_noise_floor.median():.4f}", "",
             "## Segment level", "", H.to_markdown(H.summarise(scored[scored.level == 'segment'], ('method',))), "",
             f"Sampling-noise floor at segment level: median JSD {floor[floor.level=='segment'].jsd_noise_floor.median():.4f}", "",
             "## 'Everyone is average' error by segment type (median mae_pts): how much segments actually differ", "",
             H.to_markdown(scored[(scored.level == 'segment') & (scored.method == 'population_marginal_for_segments')].groupby('segment_type')[['mae_pts', 'jsd']].median().reset_index()), "",
             "## Segment groups available", "", ", ".join(b.groups()), ""]
    _write(f"baselines_wvs7_{tag}.md", "\n".join(lines))
    scored.to_csv(RESULTS / f"baselines_wvs7_{tag}_cells.csv", index=False)


def baselines_goqa(args: argparse.Namespace) -> None:
    countries = args.countries or GOQA_COUNTRIES
    b = globalopinionqa.benchmark(countries, min_countries=2)
    preds = {"uniform": B.uniform(b), "other_countries_mean": B.leave_one_group_out_mean(b)}
    scored = pd.concat([H.score(p, b, name) for name, p in preds.items()], ignore_index=True)
    scored["country"] = scored["group"].str.replace("country=", "", regex=False)
    floor = H.noise_floor(b, default_n=1000)
    lines = [
        "# Baselines on GlobalOpinionQA (WVS wave 7 + Pew Global Attitudes)", "",
        f"Questions used: {len(b.questions)} (answered by at least 2 of the selected countries); countries: {', '.join(countries)}.", "",
        "The 'other countries' mean' baseline predicts a country's answer shares as the average of every other country that was asked the same question. Prior work found LLMs struggle to beat it on country means.", "",
        "## By country (median over questions)", "",
        H.to_markdown(scored.pivot_table(index="country", columns="method", values="jsd", aggfunc="median").reset_index().rename(columns=lambda c: c if c in {"country"} else f"jsd_{c}")), "",
        H.to_markdown(scored.groupby(["country", "method"]).size().unstack().reset_index().rename(columns=lambda c: c if c == "country" else f"n_{c}")), "",
        f"Sampling-noise floor assuming n=1,000 per country: median JSD {floor.jsd_noise_floor.median():.4f}", "",
        "## Overall", "",
        H.to_markdown(H.summarise(scored, ("method",))), "",
    ]
    _write("baselines_globalopinionqa.md", "\n".join(lines))
    scored.to_csv(RESULTS / "baselines_globalopinionqa_cells.csv", index=False)


def baselines_twin2k(args: argparse.Namespace) -> None:
    df = evaluate_twin2k(k=args.k, max_items=args.limit)
    summ = df[["retest_ceiling", "modal_acc", "demo_cell_acc", "knn_acc", "knn_normalized"]].mean().to_frame("mean").T
    lines = [
        "# Individual-level baselines on Twin-2K-500 (United States, 2,058 panelists)", "",
        f"Retest items with a small categorical answer set: {len(df)}; each evaluated on a random 30% test split of people.", "",
        "Protocol: predict a person's wave-4 answer without seeing their earlier answer to that item. The retest ceiling is how often people agree with themselves two weeks later. A digital twin is only useful if it beats k-NN (people who answered the other items similarly) and approaches the ceiling.", "",
        "## Averages over items", "",
        H.to_markdown(summ), "",
        "## Per item", "",
        H.to_markdown(df.sort_values("retest_ceiling", ascending=False)), "",
    ]
    _write("baselines_twin2k.md", "\n".join(lines))
    df.to_csv(RESULTS / "baselines_twin2k_items.csv", index=False)


def personas_report(args: argparse.Namespace) -> None:
    df = nemotron.load(columns=["sex", "age", "marital_status", "education_level", "industry", "planning_area", "cultural_background"])
    rep = nemotron.demographic_report(df)
    eth = rep.get("ethnicity_inferred", {})
    lines = ["# Nemotron-Personas-Singapore: demographic skeleton check", "", f"Records: {len(df)} (first shard).", ""]
    for k, v in rep.items():
        lines += [f"## {k}", "", H.to_markdown(pd.DataFrame({k: list(v.keys()), "share": list(v.values())})), ""]
    lines += ["## Ethnicity inferred from narrative vs official 2024 resident shares (approx.)", "", H.to_markdown(pd.DataFrame({"group": list(nemotron.SG_ETHNIC_TARGET_2024), "official": list(nemotron.SG_ETHNIC_TARGET_2024.values()), "persona_bank": [eth.get(g, 0.0) for g in nemotron.SG_ETHNIC_TARGET_2024]})), ""]
    _write("personas_singapore.md", "\n".join(lines))


def simulate(args: argparse.Namespace) -> None:
    from .simulate.llm import AnthropicLLM, MockLLM
    from .simulate.prompts import segment_description
    from .simulate.runner import SimConfig, aggregate, simulate_distribution, simulate_roleplay

    if args.benchmark == "gss":
        b = gss.benchmark(2024)
    elif args.benchmark == "goqa":
        b = globalopinionqa.benchmark(args.countries or ["United States", "China", "Singapore"], min_countries=1)
    else:
        raise SystemExit("benchmark must be gss or goqa")
    qs = b.questions[: args.limit] if args.limit else b.questions
    b = b.subset([q.id for q in qs])
    llm = MockLLM() if args.mock else AnthropicLLM(model=args.model)
    cfg = SimConfig(persona_style=args.persona_style, temperature=args.temperature, n_samples=1, workers=args.workers)
    if args.mode == "distribution":
        groups = {}
        for g in b.groups():
            if g == "ALL":
                groups[g] = segment_description({}, b.country)
            else:
                key, val = g.split("=", 1)
                groups[g] = f"adults living in {val}" if key == "country" else segment_description({key: val}, b.country)
        dists = simulate_distribution(qs, groups, llm, cfg, n_repeats=args.repeats)
    else:
        if args.benchmark != "gss":
            raise SystemExit("role-play mode needs respondent-level personas; use --benchmark gss")
        rng = np.random.default_rng(0)
        df = b.respondents.sample(n=min(args.personas, len(b.respondents)), random_state=0)
        record_items = [c for c in gss.ITEMS if c in df.columns and c not in {q.id for q in qs}]
        personas = gss.to_personas(df, record_items)
        resp = simulate_roleplay(personas, qs, llm, cfg)
        dists = aggregate(resp, personas, qs, segment_keys=b.segment_keys, min_n=10)
    pred = {(d.question_id, d.group): d.probs for d in dists}
    name = f"{llm.name}:{args.mode}:{args.persona_style}"
    scored = H.score(pred, b, name)
    scored["level"] = np.where(scored["group"] == "ALL", "population", "segment")
    seg = H.segment_fidelity(pred, b, name)
    out = {"benchmark": b.name, "method": name, "n_questions": len(qs), "summary": H.summarise(scored, ("method", "level")).to_dict("records"), "segment_fidelity_median": seg[["gap_r", "gap_slope", "dispersion_ratio"]].median().to_dict() if len(seg) else {}}
    print(json.dumps(out, indent=2, default=float))
    tag = f"{args.benchmark}_{args.mode}_{args.persona_style}_{llm.name}".replace("/", "_")
    RESULTS.mkdir(parents=True, exist_ok=True)
    scored.to_csv(RESULTS / f"sim_{tag}_cells.csv", index=False)
    (RESULTS / f"sim_{tag}.json").write_text(json.dumps(out, indent=2, default=float))


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(prog="dc", description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("baselines"); p.add_argument("benchmark", choices=["gss", "goqa", "twin2k", "wvs"]); p.add_argument("--countries", nargs="*"); p.add_argument("--k", type=int, default=25); p.add_argument("--limit", type=int)
    p = sub.add_parser("personas"); p.add_argument("country", choices=["singapore"])
    p = sub.add_parser("simulate"); p.add_argument("benchmark", choices=["gss", "goqa"]); p.add_argument("--mode", choices=["distribution", "roleplay"], default="distribution"); p.add_argument("--model", default="claude-sonnet-5-5"); p.add_argument("--mock", action="store_true"); p.add_argument("--limit", type=int, default=20); p.add_argument("--personas", type=int, default=200); p.add_argument("--persona-style", default="full"); p.add_argument("--temperature", type=float, default=1.0); p.add_argument("--repeats", type=int, default=1); p.add_argument("--workers", type=int, default=8); p.add_argument("--countries", nargs="*")
    _extend_parser(ap)
    args = ap.parse_args(argv)
    if args.cmd == "packet":
        make_packet(args)
        return 0
    if args.cmd == "score-packet":
        score_packet(args)
        return 0
    if args.cmd == "baselines":
        {"gss": baselines_gss, "goqa": baselines_goqa, "twin2k": baselines_twin2k, "wvs": baselines_wvs}[args.benchmark](args)
    elif args.cmd == "personas":
        personas_report(args)
    elif args.cmd == "simulate":
        simulate(args)
    return 0



# ---- "packet" workflow: export questions without answers, let any predictor (a person, an in-session model,
# ---- an external script) fill in shares, then score them against the hidden ground truth.

GSS_PACKET_GROUPS = ["ALL", "party3=Democrat (incl. leaners)", "party3=Republican (incl. leaners)", "age_band=18-29", "age_band=65+", "race_eth=Black, non-Hispanic", "education=Bachelor's or higher"]


def make_packet(args: argparse.Namespace) -> None:
    rng = np.random.default_rng(args.seed)
    exclude = set(args.exclude or [])
    if args.benchmark == "gss":
        b = gss.benchmark(2024)
        qids = [q.id for q in b.questions if q.id not in exclude and all((q.id, g) in b.real for g in GSS_PACKET_GROUPS)]
        pick = sorted(rng.choice(qids, size=min(args.n, len(qids)), replace=False).tolist())
        packet = {"benchmark": "gss", "groups": GSS_PACKET_GROUPS, "group_descriptions": {g: ("all adults in the United States" if g == "ALL" else f"US adults with {g.split('=')[0].replace('_', ' ')}: {g.split('=', 1)[1]}") for g in GSS_PACKET_GROUPS},
                  "questions": [{"id": q.id, "text": q.text, "options": q.options} for q in b.questions if q.id in pick]}
    elif args.benchmark == "wvs":
        country = (args.countries or ["Singapore"])[0]
        b = wvs.benchmark(country)
        groups = args.groups or ["ALL", "ethnic=Chinese", "ethnic=Malay", "ethnic=Indian", "age_band=18-29", "age_band=60+", "education3=Lower", "education3=Higher", "religion=Muslim", "religion=No religion"]
        qids = [q.id for q in b.questions if q.id not in exclude and all((q.id, g) in b.real for g in groups)]
        pick = sorted(rng.choice(qids, size=min(args.n, len(qids)), replace=False).tolist())
        packet = {"benchmark": "wvs", "country": country, "groups": groups, "group_descriptions": {g: (f"all adults in {country}" if g == "ALL" else f"adults in {country} with {g.split('=')[0].replace('_', ' ').replace('3', '')}: {g.split('=', 1)[1]}") for g in groups},
                  "questions": [{"id": q.id, "text": q.text, "options": q.options} for q in b.questions if q.id in pick]}
    else:
        countries = args.countries or ["United States", "China", "Singapore"]
        b = globalopinionqa.benchmark(countries, min_countries=len(countries))
        qids = [q.id for q in b.questions if q.id not in exclude]
        pick = set(rng.choice(qids, size=min(args.n, len(qids)), replace=False).tolist())
        packet = {"benchmark": "goqa", "groups": [f"country={c}" for c in countries], "group_descriptions": {f"country={c}": f"adults living in {c}" for c in countries},
                  "questions": [{"id": q.id, "text": q.text, "options": q.options, "source": q.source} for q in b.questions if q.id in pick]}
    Path(args.out).write_text(json.dumps(packet, indent=1))
    print(f"wrote {args.out}: {len(packet['questions'])} questions x {len(packet['groups'])} groups (no answers included)")


def score_packet(args: argparse.Namespace) -> None:
    packet = json.loads(Path(args.packet).read_text())
    preds_raw = json.loads(Path(args.predictions).read_text())
    pred: dict = {}
    for row in preds_raw:
        pred[(row["question_id"], row["group"])] = [float(x) for x in row["probs"]]
    qids = [q["id"] for q in packet["questions"]]
    if packet["benchmark"] == "gss":
        b24, b22 = gss.benchmark(2024), gss.benchmark(2022)
        b = b24.subset(qids)
        cells = {k for k in b.real if k[1] in packet["groups"]}
        b.real = {k: v for k, v in b.real.items() if k in cells}
        methods = {args.name: pred, "previous_wave_2022": B.previous_wave(b, b22), "population_marginal_for_segments": B.population_marginal(b)}
        reg: dict = {}
        for q in b.questions:
            reg.update(B.demographic_regression(b22.respondents, b24.respondents, q.id, q.options, ["age_band", "sex", "race_eth", "education", "region", "party3", "ideology3", "income4", "religion4", "urbanicity"], b24.segment_keys))
        methods["demographic_regression_2022->2024"] = {k: v for k, v in reg.items() if k in cells}
    elif packet["benchmark"] == "wvs":
        b = wvs.benchmark(packet["country"]).subset(qids)
        cells = {k for k in b.real if k[1] in packet["groups"]}
        b.real = {k: v for k, v in b.real.items() if k in cells}
        methods = {args.name: pred, "population_marginal_for_segments": B.population_marginal(b), "uniform": B.uniform(b)}
    else:
        countries = [g.split("=", 1)[1] for g in packet["groups"]]
        bfull = globalopinionqa.benchmark(GOQA_COUNTRIES + [c for c in countries if c not in GOQA_COUNTRIES], min_countries=2)
        b = bfull.subset(qids)
        lo = B.leave_one_group_out_mean(b)  # uses all 12+ countries as "others"
        cells = {k for k in b.real if k[1] in packet["groups"]}
        b.real = {k: v for k, v in b.real.items() if k in cells}
        methods = {args.name: pred, "other_countries_mean": {k: v for k, v in lo.items() if k in cells}, "uniform": B.uniform(b)}
    scored = pd.concat([H.score(p, b, name) for name, p in methods.items()], ignore_index=True)
    scored["level"] = np.where(scored["group"] == "ALL", "population", "segment") if packet["benchmark"] in {"gss", "wvs"} else "country"
    lines = [f"# Stress test: {args.name} on {packet['benchmark']} packet `{Path(args.packet).name}`", "",
             f"{len(qids)} questions x {len(packet['groups'])} groups; predictions written without access to the answers; scored against the real shares. Lower is better for jsd/tv/mae_pts.", ""]
    for lvl, sub in scored.groupby("level"):
        lines += [f"## {lvl}", "", H.to_markdown(H.summarise(sub, ("method",))), ""]
    if packet["benchmark"] in {"gss", "wvs"}:
        seg = pd.concat([H.segment_fidelity(p, b, name) for name, p in methods.items() if name != "population_marginal_for_segments"], ignore_index=True)
        lines += ["## Segment differences (gap recovery; dispersion ratio ideal = 1)", "", H.to_markdown(seg.groupby("method")[["gap_r", "gap_slope", "dispersion_ratio"]].median().reset_index()), ""]
        lines += ["## By group (median mae_pts)", "", H.to_markdown(scored.pivot_table(index="group", columns="method", values="mae_pts", aggfunc="median").reset_index()), ""]
    else:
        lines += ["## By country (median)", "", H.to_markdown(scored.pivot_table(index="group", columns="method", values=["jsd", "mae_pts"], aggfunc="median").reset_index()), ""]
    lines += ["## Worst 10 cells for " + args.name, "", H.to_markdown(scored[scored.method == args.name].sort_values("jsd", ascending=False).head(10)[["question_id", "group", "k", "jsd", "mae_pts", "max_abs_err"]]), ""]
    out = Path(args.out)
    out.write_text("\n".join(lines))
    scored.to_csv(out.with_suffix(".csv"), index=False)
    print("\n".join(lines[:40]))
    print(f"wrote {out}")


def _extend_parser(ap: argparse.ArgumentParser) -> None:
    sub = ap._subparsers._group_actions[0]  # type: ignore[attr-defined]
    p = sub.add_parser("packet"); p.add_argument("benchmark", choices=["gss", "goqa", "wvs"]); p.add_argument("--groups", nargs="*"); p.add_argument("--n", type=int, default=30); p.add_argument("--seed", type=int, default=7); p.add_argument("--out", required=True); p.add_argument("--exclude", nargs="*"); p.add_argument("--countries", nargs="*")
    p = sub.add_parser("score-packet"); p.add_argument("--packet", required=True); p.add_argument("--predictions", required=True); p.add_argument("--name", required=True); p.add_argument("--out", required=True)


if __name__ == "__main__":
    sys.exit(main())
