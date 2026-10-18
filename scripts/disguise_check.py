"""Disguise check: does the chatbot reading records get worse when the 20 questions are disguised?

If the chatbot reading records (scripts/record_reading_trial.py run full) is helped by remembering the World Values
Survey's published results, disguising the questions should make it worse. For 150 people drawn from the full test,
two versions go in one batch to claude-opus-5-5 at low effort:
  - "original": exactly the prompt of the full test, run again, to show how much guesses vary from run to run;
  - "disguised": the survey is not named, each of the 20 questions is reworded, and every list of answer options is
    flipped (for example 1 = always justifiable ... 10 = never justifiable). Guesses are flipped back before scoring.
The person's own answers to the 57 other questions are shown as before in both versions.

Warning sign, set before running: "disguised" clearly worse than "original" - top choice right at least 3 points
less often, or the 150 people's combined answer at least 1 point further from the whole survey - beyond the
difference between the two runs of the original. Flipping answer order can itself confuse a chatbot, so a drop is
not proof of memory; no drop is reassuring but not proof either. Questions asked after the chatbot's knowledge was
frozen remain the real test.

Usage (from the repository root; needs data/raw/wvs and docs/results/record_reading_full_predictions.json):
  .venv/bin/python -I scripts/disguise_check.py plan | run | score
Writes docs/results/disguise_check_predictions.json and docs/results/disguise_check.{md,json}.
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
import record_reading_trial as rr  # noqa: E402
from digital_citizens.data import wvs  # noqa: E402

OUT = Path("docs/results")
PRED = OUT / "disguise_check_predictions.json"
FULL = OUT / "record_reading_full_predictions.json"
MODEL, EFFORT = rr.MODEL, rr.EFFORT
MAX_TOKENS = 2000  # the full test averaged about 600 output tokens a person
BUDGET = 10.0  # dollars, worst case
N_PEOPLE, SEED = 150, 11
ARMS = ("original", "disguised")
L4 = ["Very important", "Quite important", "Not very important", "Not important at all"]
TRUST = ["A great deal", "Quite a lot", "Not very much", "None at all"]
SCALE = [str(i) for i in range(2, 10)]
# Reworded questions, answer options in the ORIGINAL order (they are shown flipped).
DISGUISE = {
    "Q3": ("How much does free time matter in your life?", L4),
    "Q6": ("How much does religion matter in your life?", L4),
    "Q14": ("Parents can try to teach children many qualities at home. Would you count determination and perseverance "
            "among the most important ones, if you could pick up to five qualities?", ["Picked", "Not picked"]),
    "Q18": ("Would you rather not have people who use drugs living next door to you?", ["Would rather not", "No objection"]),
    "Q64": ("How much do you trust religious organisations (churches, mosques, temples and so on)?", TRUST),
    "Q66": ("How much do you trust newspapers and the news media?", TRUST),
    "Q70": ("How much do you trust the law courts?", TRUST),
    "Q76": ("How much do you trust the way elections are run?", TRUST),
    "Q107": ("On a scale from 1 to 10, should more businesses be privately owned, or more be owned by the government?",
             ["More private ownership of business", *SCALE, "More government ownership of business"]),
    "Q108": ("On a scale from 1 to 10, who should do more to make sure people are provided for?",
             ["The government should do more", *SCALE, "Individuals should do more for themselves"]),
    "Q126": ("Do immigrants to Singapore raise the risk of terrorism?", ["Disagree", "Hard to say", "Agree"]),
    "Q131": ("How safe do you feel in your neighbourhood these days?", ["Very safe", "Quite safe", "Not very safe", "Not at all safe"]),
    "Q142": ("How much do you worry about losing your job, or not being able to find one?", ["Very much", "A great deal", "Not much", "Not at all"]),
    "Q177": ("On a scale from 1 to 10, can it ever be right to claim government benefits you are not entitled to?",
             ["Never justifiable", *SCALE, "Always justifiable"]),
    "Q184": ("On a scale from 1 to 10, can abortion ever be justified?", ["Never justifiable", *SCALE, "Always justifiable"]),
    "Q209": ("Signing a petition: have you done this, might you do it, or would you never do it?", ["Have done", "Might do", "Would never do"]),
    "Q237": ("Would it be a good or a bad way to run Singapore if the military governed the country?",
             ["Very good", "Fairly good", "Fairly bad", "Very bad"]),
    "Q240": ("People talk of the political left and right. Where would you put your own views on a scale from 1 to 10?",
             ["Left", *SCALE, "Right"]),
    "Q250": ("On a scale from 1 to 10, how much does it matter to you to live in a country run democratically?",
             ["Not at all important", *SCALE, "Absolutely important"]),
    "Q253": ("How much are individual human rights respected in Singapore today?",
             ["A great deal of respect", "Fairly much respect", "Not much respect", "No respect at all"]),
}


def setup():
    df, qs, targets, record_items, _ = rr.setup()  # rr.setup() without "full" also returns the pilot sample; unused
    pool = sorted(json.load(open(FULL))["predictions"]["record"])
    pids = sorted(np.random.default_rng(SEED).choice(pool, size=N_PEOPLE, replace=False).tolist())
    assert all(len(DISGUISE[t][1]) == len(qs[t].options) for t in targets)
    return df, qs, targets, record_items, pids


def disguised_system(targets) -> str:
    first = DISGUISE[targets[0]][1]
    lines = ["You predict how one real person answered a survey of adults in Singapore.",
             "For each question below, give the probability that this person chose each answer option, in the order listed.",
             "Reply with JSON only, one key per question id, each value a list of probabilities that sum to 1, for example",
             '{"' + targets[0] + '": [' + ", ".join(["0.25"] * len(first)) + '], ...}.', "", "Questions:"]
    for t in targets:
        text, opts = DISGUISE[t]
        lines.append(f"{t}: {text}")
        lines += [f"  {i + 1}. {o}" for i, o in enumerate(reversed(opts))]
    return "\n".join(lines)


def requests(df, qs, targets, record_items, pids):
    systems = {"original": rr.system_prompt(qs, targets), "disguised": disguised_system(targets)}
    rows = df.set_index("pid")
    return [{"custom_id": f"{arm}__{pid}", "params": {
        "model": MODEL, "max_tokens": MAX_TOKENS, "output_config": {"effort": EFFORT},
        "system": [{"type": "text", "text": systems[arm], "cache_control": {"type": "ephemeral"}}],
        "messages": [{"role": "user", "content": rr.person_prompt(rows.loc[pid], qs, record_items, "record")}]}}
        for pid in pids for arm in ARMS]


def worst_case(reqs) -> float:
    n_in = sum(int(len(r["params"]["system"][0]["text"] + r["params"]["messages"][0]["content"]) / 3.5) + 50 for r in reqs)
    return rr.BATCH_DISCOUNT * (n_in * rr.PRICE_IN + len(reqs) * MAX_TOKENS * rr.PRICE_OUT)


def plan():
    df, qs, targets, record_items, pids = setup()
    reqs = requests(df, qs, targets, record_items, pids)
    print(f"{len(pids)} people x {ARMS} = {len(reqs)} requests to {MODEL} (effort {EFFORT}, max {MAX_TOKENS} output tokens); "
          f"worst case ${worst_case(reqs):.2f} (budget ${BUDGET:.2f}).")
    print("\nDisguised questions as shown:\n" + disguised_system(targets))


def run():
    import anthropic
    key = os.environ.get("DIGITAL_CITIZENS_API_KEY")
    if key:
        client = anthropic.Anthropic(api_key=key)
    else:  # the network secret: through the proxy, with no key header of our own for it to replace
        http = anthropic.DefaultHttpxClient(proxy=os.environ["HTTPS_PROXY"], verify=os.environ.get("SSL_CERT_FILE", "/root/.ccr/ca-bundle.crt"))
        client = anthropic.Anthropic(api_key=None, default_headers={"X-Api-Key": anthropic.omit}, http_client=http)
    df, qs, targets, record_items, pids = setup()
    reqs = requests(df, qs, targets, record_items, pids)
    cost = worst_case(reqs)
    print(f"{len(reqs)} requests; worst case ${cost:.2f} (budget ${BUDGET:.2f}).")
    if cost > BUDGET:
        sys.exit("Worst case is over budget: nothing was sent.")
    batch = client.messages.batches.create(requests=reqs)
    print("Batch", batch.id, "submitted; waiting (most finish within an hour).", flush=True)
    while (batch := client.messages.batches.retrieve(batch.id)).processing_status != "ended":
        time.sleep(60)
    preds, failed, usage = {a: {} for a in ARMS}, [], {"input": 0, "cache_read": 0, "cache_write": 0, "output": 0}
    for res in client.messages.batches.results(batch.id):
        arm, pid = res.custom_id.split("__")
        if res.result.type != "succeeded":
            failed.append([res.custom_id, res.result.type]); continue
        msg = res.result.message
        u = msg.usage
        usage["input"] += u.input_tokens; usage["output"] += u.output_tokens
        usage["cache_read"] += getattr(u, "cache_read_input_tokens", 0) or 0
        usage["cache_write"] += getattr(u, "cache_creation_input_tokens", 0) or 0
        text = "".join(b.text for b in msg.content if b.type == "text")
        p = rr.parse(text, qs, targets) if msg.stop_reason not in ("refusal", "max_tokens") else None
        if p is None:
            failed.append([res.custom_id, msg.stop_reason]); continue
        if arm == "disguised":  # back to the original option order
            p = {t: v[::-1] for t, v in p.items()}
        preds[arm][pid] = p
    spent = rr.BATCH_DISCOUNT * ((usage["input"] + 1.25 * usage["cache_write"] + 0.05 * usage["cache_read"]) * rr.PRICE_IN + usage["output"] * rr.PRICE_OUT)
    PRED.write_text(json.dumps({"batch": batch.id, "model": MODEL, "effort": EFFORT, "pids": pids, "usage": usage,
                                "cost_estimate_usd": round(spent, 2), "failed": failed, "predictions": preds}, indent=1))
    print(f"Saved {sum(len(v) for v in preds.values())} predictions, {len(failed)} failed; about ${spent:.2f} spent. Now run: score")


def score():
    df, qs, targets, _, _ = setup()
    P = json.load(open(PRED))
    pids = P["pids"]
    first = json.load(open(FULL))["predictions"]["record"]
    runs = {"original, full test": {p: first[p] for p in pids}, **P["predictions"]}
    common = [p for p in pids if all(p in r for r in runs.values())]
    rows = df.set_index("pid")
    truth = {k: d.normalised() for k, d in wvs.benchmark("Singapore").real.items()}
    w = rows.loc[common, "weight"].to_numpy()
    lines = ["# Disguise check: does the chatbot reading records get worse when the questions are disguised?", "",
             f"{MODEL} (effort {EFFORT}), one batch ({P['batch']}); about ${P['cost_estimate_usd']} spent; "
             f"{len(P['failed'])} requests failed or could not be read; {len(common)} of {len(pids)} people have all three runs.", "",
             "| run | top choice right | average probability on their real answer | combined answer, points off the whole survey |",
             "|---|---|---|---|"]
    res = {}
    for name, r in runs.items():
        hit, prob = [], []
        for pid in common:
            for t in targets:
                a = rows.at[pid, t]
                if a is None or pd.isna(a):
                    continue
                k = qs[t].options.index(a)
                hit.append(int(np.argmax(r[pid][t]) == k)); prob.append(r[pid][t][k])
        nat = [100 * np.abs(np.average([r[p][t] for p in common], axis=0, weights=w) - truth[(t, "ALL")]).mean() for t in targets]
        res[name] = {"top_choice": float(np.mean(hit)), "prob_on_answer": float(np.mean(prob)), "national_points_off": float(np.median(nat)), "answers": len(hit)}
        lines.append(f"| {name} | {np.mean(hit):.1%} | {np.mean(prob):.2f} | {np.median(nat):.1f} |")
    own = [100 * np.abs(rr._shares(rows.loc[common, t], rows.loc[common, "weight"], qs[t].options) - truth[(t, "ALL")]).mean() for t in targets]
    res["the people's own answers"] = {"national_points_off": float(np.median(own))}
    lines += [f"| for comparison: the {len(common)} people's own answers | | | {np.median(own):.1f} |", "",
              "Combined answer: the people's guesses averaged (weighted) for each question, against everyone in the survey;",
              "median over the 20 questions. The two runs of the original show how much guesses vary by chance.", "",
              "Warning sign, set before running: the disguised run at least 3 points lower on top choice right, or at least",
              "1 point further off, than the original runs, beyond the gap between the two original runs.", "",
              "Generated by scripts/disguise_check.py."]
    (OUT / "disguise_check.md").write_text("\n".join(lines) + "\n")
    (OUT / "disguise_check.json").write_text(json.dumps(res, indent=1))
    print("\n".join(lines))


if __name__ == "__main__":
    {"plan": plan, "run": run, "score": score}[sys.argv[1] if len(sys.argv) > 1 else "plan"]()
