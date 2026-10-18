"""Memory check: has the chatbot already seen the published answers to our 20 Singapore questions?

The 20 questions (packet_wvs_singapore.json) come from the World Values Survey, whose results are published. A
chatbot that read them could look accurate by remembering rather than working the answer out. Two quick checks:

Test 1, ask it directly (`plan`, `run`, `score`; one batch to claude-opus-5-5, the model behind the chatbot reading
records; worst case under $1). For each question, two requests, with no person's record:
  - "named": what did the World Values Survey wave 7 find in Singapore? Use the published figures if you remember them.
  - "unnamed": how would adults in Singapore answer this question around 2020? (the survey is not named)
Each gives the percentage choosing each option, nationally and for the scorecard's nine groups, and is scored
against the whole survey's weighted answers.

Test 2, famous against little-known questions (`score`, free; reuses one_method_singapore_reading_cells.csv). If
memory helps, the chatbots should do better, compared with record citizens on the same question, on questions
whose results are widely published. Record citizens learned from other countries cannot remember Singapore's
answers, so they control for how hard each question is. Two ways to say which questions are well known:
  - FAMOUS below, fixed before any per-question result was looked at (judgement; reasons given);
  - how close the "named" recall in test 1 came, question by question.

Warning signs, set before running:
  - "named" recall within 2 points of the published national answer (exact recall of rounded figures would be
    under 1 point), or "named" at least 1 point closer than "unnamed" across the groups;
  - in test 2, the chatbots' edge over record citizens clearly larger on well-known questions.
Neither check proves memory or rules it out: a well-informed chatbot can also reason its way close. Disguising the
questions (the next test) and questions asked after the chatbot's knowledge was frozen are the stronger checks.

Usage (from the repository root; needs data/raw/wvs):
  .venv/bin/python -I scripts/memory_check.py plan | run | score
Writes docs/results/memory_check_predictions.json and docs/results/memory_check.{md,json}.
The key: as in scripts/record_reading_trial.py (DIGITAL_CITIZENS_API_KEY, or the network secret through the proxy).
"""
from __future__ import annotations

import json
import os
import re
import sys
import time
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from digital_citizens.data import wvs  # noqa: E402

OUT = Path("docs/results")
PACKET = OUT / "stress_test" / "packet_wvs_singapore.json"
CELLS = OUT / "stress_test" / "one_method_singapore_reading_cells.csv"
CHAT_KIND = OUT / "stress_test" / "predictions_wvs_singapore_claude_in_session.json"
PRED = OUT / "memory_check_predictions.json"
MODEL = "claude-opus-5-5"
EFFORT = "low"
MAX_TOKENS = 2000  # ten groups of up to ten percentages, plus brief thinking at low effort
BUDGET = 1.0  # dollars, worst case
PRICE_IN, PRICE_OUT = 4.0 / 1e6, 20.0 / 1e6  # per token, standard; the batch is charged half
BATCH_DISCOUNT = 0.5
ARMS = ("named", "unnamed")
# Well-known questions, chosen before any per-question result was seen (2026-10-18):
FAMOUS = {
    "Q6": "importance of religion, a headline World Values Survey item",
    "Q14": "determination, part of the autonomy index behind the Inglehart-Welzel cultural map",
    "Q184": "abortion, one of the items on the Inglehart-Welzel cultural map",
    "Q209": "signing a petition, one of the items on the Inglehart-Welzel cultural map",
    "Q237": "army rule, widely cited in the debate on support for democracy",
    "Q240": "left-right placement, a standard headline item",
    "Q250": "importance of democracy, widely cited",
}
ALONE = {"chatbot kind": "chatbot kind alone, no survey", "chatbot reading records": "chatbot reading records alone, no survey",
         "record citizens": "record citizens alone, no survey"}


def setup():
    packet = json.load(open(PACKET))
    return packet, list(packet["group_descriptions"])


def prompt(q: dict, packet: dict, arm: str) -> str:
    groups = packet["group_descriptions"]
    if arm == "named":
        head = ["The World Values Survey wave 7 interviewed about 2,000 adults in Singapore in 2020, and its results are",
                "published. For the question below, give the percentage of each group that chose each answer option, as the",
                "published results show. If you remember the published figures, use them; if not, give your best estimate."]
        reply = '{"recall": "remember" or "partly" or "estimate", "groups": {"ALL": [...], ...}}'
    else:
        head = ["Estimate how adults in Singapore would answer the survey question below, around 2020. For each group, give",
                "the percentage that would choose each answer option."]
        reply = '{"groups": {"ALL": [...], ...}}'
    lines = head + ["", f"Question: {q['text']}", "Answer options, in order:"]
    lines += [f"  {i + 1}. {o}" for i, o in enumerate(q["options"])]
    lines += ["", "Groups:"] + [f"  {g}: {d}" for g, d in groups.items()]
    lines += ["", f"Reply with JSON only, one list of {len(q['options'])} percentages per group, in option order: {reply}"]
    return "\n".join(lines)


def requests(packet):
    return [{"custom_id": f"{arm}__{q['id']}", "params": {
        "model": MODEL, "max_tokens": MAX_TOKENS, "output_config": {"effort": EFFORT},
        "messages": [{"role": "user", "content": prompt(q, packet, arm)}]}}
        for q in packet["questions"] for arm in ARMS]


def worst_case(reqs) -> float:
    n_in = sum(int(len(r["params"]["messages"][0]["content"]) / 3.5) + 50 for r in reqs)
    return BATCH_DISCOUNT * (n_in * PRICE_IN + len(reqs) * MAX_TOKENS * PRICE_OUT)


def parse(text: str, q: dict, groups: list[str]):
    m = re.search(r"\{.*\}", text, flags=re.S)
    if not m:
        return None
    try:
        raw = json.loads(m.group(0))
    except json.JSONDecodeError:
        return None
    out = {}
    for g in groups:
        v = (raw.get("groups") or {}).get(g)
        if not isinstance(v, list) or len(v) != len(q["options"]) or any(not isinstance(x, (int, float)) or x < 0 for x in v) or sum(v) <= 0:
            return None
        out[g] = [x / sum(v) for x in v]
    return {"recall": raw.get("recall"), "groups": out}


def plan():
    packet, _ = setup()
    reqs = requests(packet)
    print(f"{len(reqs)} requests ({len(packet['questions'])} questions x {ARMS}) to {MODEL} (effort {EFFORT}, max {MAX_TOKENS} output tokens); "
          f"worst case ${worst_case(reqs):.2f} (budget ${BUDGET:.2f}).")
    print("\nExample named prompt:\n" + reqs[0]["params"]["messages"][0]["content"])


def run():
    import anthropic
    key = os.environ.get("DIGITAL_CITIZENS_API_KEY")
    if key:
        client = anthropic.Anthropic(api_key=key)
    else:  # the network secret: through the proxy, with no key header of our own for it to replace
        http = anthropic.DefaultHttpxClient(proxy=os.environ["HTTPS_PROXY"], verify=os.environ.get("SSL_CERT_FILE", "/root/.ccr/ca-bundle.crt"))
        client = anthropic.Anthropic(api_key=None, default_headers={"X-Api-Key": anthropic.omit}, http_client=http)
    packet, groups = setup()
    reqs = requests(packet)
    cost = worst_case(reqs)
    print(f"{len(reqs)} requests; worst case ${cost:.2f} (budget ${BUDGET:.2f}).")
    if cost > BUDGET:
        sys.exit("Worst case is over budget: nothing was sent.")
    batch = client.messages.batches.create(requests=reqs)
    print("Batch", batch.id, "submitted; waiting.", flush=True)
    while (batch := client.messages.batches.retrieve(batch.id)).processing_status != "ended":
        time.sleep(30)
    qmap = {q["id"]: q for q in packet["questions"]}
    preds, failed, usage = {a: {} for a in ARMS}, [], {"input": 0, "output": 0}
    for res in client.messages.batches.results(batch.id):
        arm, qid = res.custom_id.split("__")
        if res.result.type != "succeeded":
            failed.append([res.custom_id, res.result.type]); continue
        msg = res.result.message
        usage["input"] += msg.usage.input_tokens; usage["output"] += msg.usage.output_tokens
        text = "".join(b.text for b in msg.content if b.type == "text")
        p = parse(text, qmap[qid], groups) if msg.stop_reason not in ("refusal", "max_tokens") else None
        if p is None:
            failed.append([res.custom_id, msg.stop_reason]); continue
        preds[arm][qid] = p
    spent = BATCH_DISCOUNT * (usage["input"] * PRICE_IN + usage["output"] * PRICE_OUT)
    PRED.write_text(json.dumps({"batch": batch.id, "model": MODEL, "effort": EFFORT, "usage": usage,
                                "cost_estimate_usd": round(spent, 2), "failed": failed, "predictions": preds}, indent=1))
    print(f"Saved {sum(len(v) for v in preds.values())} answers, {len(failed)} failed; about ${spent:.2f} spent. Now run: score")


def _err(p, t) -> float:
    return float(100 * np.abs(np.asarray(p, float) - np.asarray(t, float)).mean())


def score():
    packet, groups = setup()
    bench = wvs.benchmark("Singapore")
    truth = {k: d.normalised() for k, d in bench.real.items()}
    P = json.load(open(PRED))
    targets = [q["id"] for q in packet["questions"]]
    # every source's estimate of each group's answer, against the whole survey
    src = {arm: {(q, g): v for q, d in P["predictions"][arm].items() for g, v in d["groups"].items()} for arm in ARMS}
    src["chatbot kind (Fable 5.1, scorecard)"] = {(r["question_id"], r["group"]): list(np.asarray(r["probs"], float) / np.sum(r["probs"]))
                                                  for r in json.load(open(CHAT_KIND))}
    reading = json.load(open(OUT / "record_reading_full_predictions.json"))["predictions"]["record"]
    df = bench.respondents.set_index("pid")
    est = {}
    for g in groups:
        members = df.index if g == "ALL" else df.index[df[g.split("=")[0]].astype(str) == g.split("=")[1]]
        have = [p for p in members if p in reading]
        w = df.loc[have, "weight"].to_numpy()
        for q in targets:
            est[(q, g)] = list(np.average([reading[p][q] for p in have], axis=0, weights=w))
    src["chatbot reading records (Opus 5.5)"] = est
    err = {s: {k: _err(v, truth[k]) for k, v in e.items() if k in truth and k[0] in targets and k[1] in groups} for s, e in src.items()}

    lines = ["# Memory check: has the chatbot already seen the published answers?", "",
             f"Test 1: {MODEL} (effort {EFFORT}), one batch ({P['batch']}); about ${P['cost_estimate_usd']} spent; "
             f"{len(P['failed'])} requests failed or could not be read. Test 2 reuses the full record-reading test.", "",
             "## Test 1: asked directly, scored against the whole survey", "",
             "Points off per answer option (median over questions; lower is closer). Exact recall of rounded published",
             "figures would be under 1 point off.", "",
             "| source | national answer | all ten groups |", "|---|---|---|"]
    res = {"test1": {}, "test2": {}}
    for s, e in err.items():
        nat = [v for k, v in e.items() if k[1] == "ALL"]
        res["test1"][s] = {"national": float(np.median(nat)), "groups": float(np.median(list(e.values()))), "cells": len(e)}
        lines.append(f"| {s} | {np.median(nat):.1f} | {np.median(list(e.values())):.1f} |")
    diff = [err["named"][k] - err["unnamed"][k] for k in err["named"] if k in err["unnamed"]]
    recall = pd.Series([d.get("recall") for d in P["predictions"]["named"].values()]).value_counts().to_dict()
    res["test1"]["named_minus_unnamed"] = float(np.median(diff))
    res["test1"]["said"] = recall
    lines += ["", f"Naming the survey changed the guesses by {np.median(diff):+.1f} points at the median (negative: closer when named).",
              f"Asked whether it remembered the published figures, it said: {recall}.", ""]

    # Test 2: the chatbots' edge over record citizens, question by question (alone, survey of 300, averaged over draws)
    cells = pd.read_csv(CELLS)
    cells = cells[(cells.n == 300) & cells.config.isin(ALONE.values())]
    per = cells.groupby(["config", "question_id", "group"]).mae_pts.mean().groupby(["config", "question_id"]).median().unstack("config")
    per = per.rename(columns={v: k for k, v in ALONE.items()})
    recall_err = pd.Series({q: err["named"][(q, "ALL")] for q in targets if (q, "ALL") in err["named"]})
    tab = pd.DataFrame({"famous": [q in FAMOUS for q in per.index], "named recall, national": recall_err.reindex(per.index)}, index=per.index)
    lines += ["## Test 2: famous against little-known questions", "",
              "Edge = chatbot's points off minus record citizens' points off on the same question (each alone, no survey;",
              "median over groups). Negative means the chatbot did better than record citizens.", "",
              "| chatbot | edge, famous questions | edge, other questions | link between edge and how well test 1 recalled it |", "|---|---|---|---|"]
    for c in ("chatbot kind", "chatbot reading records"):
        edge = per[c] - per["record citizens"]
        tab[f"edge: {c}"] = edge
        f, o = edge[tab.famous].median(), edge[~tab.famous].median()
        rho = float(pd.Series(edge).corr(tab["named recall, national"], method="spearman"))
        res["test2"][c] = {"famous": float(f), "other": float(o), "spearman_with_recall_error": rho}
        lines.append(f"| {c} | {f:+.1f} ({tab.famous.sum()} questions) | {o:+.1f} ({(~tab.famous).sum()} questions) | {rho:+.2f} |")
    lines += ["", "The last column is a rank correlation across the 20 questions (from -1 to +1). If memory helps, it is",
              "positive: the better a question is recalled (smaller recall error), the bigger the chatbot's edge.", "",
              "Question by question:", "", "| question | famous | named recall, national | edge: chatbot kind | edge: chatbot reading records |",
              "|---|---|---|---|---|"]
    for q, r in tab.iterrows():
        lines.append(f"| {q} | {'yes' if r.famous else ''} | {r['named recall, national']:.1f} | {r['edge: chatbot kind']:+.1f} | {r['edge: chatbot reading records']:+.1f} |")
    lines += ["", "Famous questions, chosen before any per-question result was seen: " +
              "; ".join(f"{q} ({why})" for q, why in FAMOUS.items()) + ".", "",
              "Neither test proves memory or rules it out: a well-informed chatbot can also reason its way close. With 20",
              "questions, differences in test 2 of a point or so can be chance.", "", "Generated by scripts/memory_check.py."]
    (OUT / "memory_check.md").write_text("\n".join(lines) + "\n")
    (OUT / "memory_check.json").write_text(json.dumps(res, indent=1))
    print("\n".join(lines))


if __name__ == "__main__":
    {"plan": plan, "run": run, "score": score}[sys.argv[1] if len(sys.argv) > 1 else "plan"]()
