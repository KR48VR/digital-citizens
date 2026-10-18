"""Memory checks 1 and 3 for the chatbot used on the scorecard (Claude Fable 5.1), which so far had only check 2.

The scorecard's chatbot kind answers for whole groups, so both checks ask it for every group's answer shares, one
request per question, as scripts/memory_check.py does for the chatbot reading records. Four versions of each of
the 20 Singapore questions go in one batch to claude-fable-5-1 at low effort:
  - "named": the survey is named and its published figures are asked for (check 1);
  - "unnamed": the same question, the survey not named (check 1's comparison, and check 3's original);
  - "unnamed, again": the same as "unnamed", to show how much answers vary from run to run;
  - "disguised": the question reworded, its answer options in reverse order and the survey not named (check 3;
    wording from scripts/disguise_check.py). Answers are flipped back before scoring.
Everything is scored against the whole survey's weighted answers (points off per answer option).

Warning signs, set before running:
  - check 1: "named" within 2 points of the national answers (exact recall of rounded figures would be under 1),
    or at least 1 point closer than "unnamed" across all group-question cells;
  - check 3: "disguised" at least 1 point further off than "unnamed" (median over group-question cells), beyond
    the gap between the two unnamed runs.
Neither check proves memory or rules it out; questions asked after the chatbot was built are the real test.

Usage (from the repository root; needs data/raw/wvs):
  .venv/bin/python -I scripts/memory_check_chatbot.py plan | run | score
Writes docs/results/memory_check_chatbot_predictions.json and docs/results/memory_check_chatbot.{md,json}.
The key: as in scripts/record_reading_trial.py.
"""
from __future__ import annotations

import json
import os
import sys
import time
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
sys.path.insert(0, str(Path(__file__).resolve().parent))
import memory_check as mc  # noqa: E402
from disguise_check import DISGUISE  # noqa: E402
from digital_citizens.data import wvs  # noqa: E402

OUT = Path("docs/results")
PRED = OUT / "memory_check_chatbot_predictions.json"
MODEL = "claude-fable-5-1"  # the scorecard's chatbot kind (its predictions there were written in-session)
EFFORT = "low"
MAX_TOKENS = 2000
BUDGET = 5.0  # dollars, worst case
PRICE_IN, PRICE_OUT = 10.0 / 1e6, 50.0 / 1e6  # per token, standard; the batch is charged half
BATCH_DISCOUNT = 0.5
ARMS = ("named", "unnamed", "unnamed, again", "disguised")


def disguised_question(q: dict) -> dict:
    text, opts = DISGUISE[q["id"]]
    return {**q, "text": text, "options": list(reversed(opts))}


def prompt(q: dict, packet: dict, arm: str) -> str:
    if arm == "named":
        return mc.prompt(q, packet, "named")
    return mc.prompt(disguised_question(q) if arm == "disguised" else q, packet, "unnamed")


def requests(packet):
    return [{"custom_id": f"{i}__{q['id']}", "params": {
        "model": MODEL, "max_tokens": MAX_TOKENS, "output_config": {"effort": EFFORT},
        "messages": [{"role": "user", "content": prompt(q, packet, arm)}]}}
        for q in packet["questions"] for i, arm in enumerate(ARMS)]


def worst_case(reqs) -> float:
    n_in = sum(int(len(r["params"]["messages"][0]["content"]) / 3.5) + 50 for r in reqs)
    return BATCH_DISCOUNT * (n_in * PRICE_IN + len(reqs) * MAX_TOKENS * PRICE_OUT)


def plan():
    packet, _ = mc.setup()
    reqs = requests(packet)
    print(f"{len(reqs)} requests ({len(packet['questions'])} questions x {ARMS}) to {MODEL} (effort {EFFORT}, max {MAX_TOKENS} output tokens); "
          f"worst case ${worst_case(reqs):.2f} (budget ${BUDGET:.2f}).")
    print("\nExample disguised prompt:\n" + reqs[3]["params"]["messages"][0]["content"])


def run():
    import anthropic
    key = os.environ.get("DIGITAL_CITIZENS_API_KEY")
    if key:
        client = anthropic.Anthropic(api_key=key)
    else:  # the network secret: through the proxy, with no key header of our own for it to replace
        http = anthropic.DefaultHttpxClient(proxy=os.environ["HTTPS_PROXY"], verify=os.environ.get("SSL_CERT_FILE", "/root/.ccr/ca-bundle.crt"))
        client = anthropic.Anthropic(api_key=None, default_headers={"X-Api-Key": anthropic.omit}, http_client=http)
    packet, groups = mc.setup()
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
        i, qid = res.custom_id.split("__")
        arm = ARMS[int(i)]
        if res.result.type != "succeeded":
            failed.append([res.custom_id, res.result.type]); continue
        msg = res.result.message
        usage["input"] += msg.usage.input_tokens; usage["output"] += msg.usage.output_tokens
        text = "".join(b.text for b in msg.content if b.type == "text")
        q = disguised_question(qmap[qid]) if arm == "disguised" else qmap[qid]
        p = mc.parse(text, q, groups) if msg.stop_reason not in ("refusal", "max_tokens") else None
        if p is None:
            failed.append([res.custom_id, msg.stop_reason]); continue
        if arm == "disguised":  # back to the original option order
            p["groups"] = {g: v[::-1] for g, v in p["groups"].items()}
        preds[arm][qid] = p
    spent = BATCH_DISCOUNT * (usage["input"] * PRICE_IN + usage["output"] * PRICE_OUT)
    PRED.write_text(json.dumps({"batch": batch.id, "model": MODEL, "effort": EFFORT, "usage": usage,
                                "cost_estimate_usd": round(spent, 2), "failed": failed, "predictions": preds}, indent=1))
    print(f"Saved {sum(len(v) for v in preds.values())} answers, {len(failed)} failed; about ${spent:.2f} spent. Now run: score")


def score():
    packet, groups = mc.setup()
    targets = [q["id"] for q in packet["questions"]]
    truth = {k: d.normalised() for k, d in wvs.benchmark("Singapore").real.items()}
    P = json.load(open(PRED))
    err = {}
    for arm in ARMS:
        err[arm] = {(q, g): mc._err(v, truth[(q, g)]) for q, d in P["predictions"][arm].items() for g, v in d["groups"].items()
                    if (q, g) in truth and q in targets and g in groups}
    common = set.intersection(*(set(e) for e in err.values()))
    res = {"arms": {}}
    lines = ["# Memory checks 1 and 3 for the scorecard's chatbot (Claude Fable 5.1)", "",
             f"{MODEL} (effort {EFFORT}), one batch ({P['batch']}); about ${P['cost_estimate_usd']} spent; "
             f"{len(P['failed'])} requests failed or could not be read; {len(common)} group-question cells in every version.", "",
             "Points off per answer option against the whole survey (median; lower is closer).", "",
             "| version | national answer (median over questions) | all group-question cells |", "|---|---|---|"]
    for arm in ARMS:
        nat = [err[arm][k] for k in common if k[1] == "ALL"]
        allc = [err[arm][k] for k in common]
        res["arms"][arm] = {"national": float(np.median(nat)), "national_average": float(np.mean(nat)), "cells": float(np.median(allc))}
        lines.append(f"| {arm} | {np.median(nat):.1f} | {np.median(allc):.1f} |")
    d = lambda a, b: float(np.median([err[a][k] - err[b][k] for k in common]))
    res["named_minus_unnamed"] = d("named", "unnamed")
    res["disguised_minus_unnamed"] = d("disguised", "unnamed")
    res["again_minus_unnamed"] = d("unnamed, again", "unnamed")
    res["disguised_minus_again"] = d("disguised", "unnamed, again")
    res["said"] = pd.Series([v.get("recall") for v in P["predictions"]["named"].values()]).value_counts().to_dict()
    lines += ["", "Differences, median over the same group-question cells (negative: the first is closer):", "",
              f"- named minus unnamed: {res['named_minus_unnamed']:+.2f}",
              f"- disguised minus unnamed: {res['disguised_minus_unnamed']:+.2f}; disguised minus unnamed, again: {res['disguised_minus_again']:+.2f}",
              f"- unnamed, again minus unnamed (run-to-run): {res['again_minus_unnamed']:+.2f}", "",
              f"Asked whether it remembered the published figures, it said: {res['said']}.", "",
              "Warning signs, set before running: check 1, named within 2 points nationally, or at least 1 point closer than",
              "unnamed; check 3, disguised at least 1 point further off than unnamed, beyond the run-to-run gap.", "",
              "Generated by scripts/memory_check_chatbot.py."]
    (OUT / "memory_check_chatbot.md").write_text("\n".join(lines) + "\n")
    (OUT / "memory_check_chatbot.json").write_text(json.dumps(res, indent=1))
    print("\n".join(lines))


if __name__ == "__main__":
    {"plan": plan, "run": run, "score": score}[sys.argv[1] if len(sys.argv) > 1 else "plan"]()
