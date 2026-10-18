"""Record-reading trial: does letting the chatbot read each person's survey record make it more accurate?

The chatbot kind on the scorecard is told only who a group is. Here it predicts how each of 100 real
Singaporeans (World Values Survey, 2019-20) answered 20 questions, two ways:
- "demographics": told only the person's age, sex, ethnicity, religion, education and similar;
- "record": told the same, plus the person's own answers to the survey's other questions.
Both arms use the same model and the same 20 questions as the one-method test (packet_wvs_singapore.json).

Scoring (`score`): for each person, how often the top choice matches what they said; for each group, points off
against what the rest of the survey said (median over group-question cells), next to the same 100 people's own
answers (a survey of 100 alone). 100 people is a pilot: it shows whether reading records is worth a full test.

Usage (run from the repository root; needs data/raw/wvs, see scripts/download_wvs.py):
  .venv/bin/python -I scripts/record_reading_trial.py plan    # no API calls: sample, prompt sizes, worst-case cost
  .venv/bin/python -I scripts/record_reading_trial.py run     # needs the key (below); one batch, refuses if over budget
  .venv/bin/python -I scripts/record_reading_trial.py score   # scores the saved predictions
Writes docs/results/record_reading_trial.{md,json} and docs/results/record_reading_trial_predictions.json.

The key: King adds it in the environment's settings as a network secret (header x-api-key, website
api.anthropic.com, path prefix /v1/messages/batches). The proxy attaches it, so the script never sees it; the
script sends its requests through the proxy on purpose, because the environment otherwise reaches the Claude API
directly. Running elsewhere, set DIGITAL_CITIZENS_API_KEY instead. Never ANTHROPIC_API_KEY: Claude Code itself
reads that name. Only batch endpoints are used, so the secret can be limited to them.
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

from digital_citizens.data import wvs

OUT = Path("docs/results")
PACKET = OUT / "stress_test" / "packet_wvs_singapore.json"
PRED = OUT / "record_reading_trial_predictions.json"
MODEL = "claude-opus-5-5"
EFFORT = "low"
MAX_TOKENS = 3000  # 20 short JSON answers plus brief thinking at low effort
BUDGET = 10.0  # dollars, worst case
PRICE_IN, PRICE_OUT = 4.0 / 1e6, 20.0 / 1e6  # per token, standard; the batch is charged half
BATCH_DISCOUNT = 0.5
PER_GROUP = {"Chinese": 34, "Malay": 33, "Indian": 33}
SEED = 7
DEMO = [("age", "Age"), ("sex", "Sex"), ("ethnic", "Ethnicity"), ("religion", "Religion"), ("education3", "Education"),
        ("income3", "Income"), ("born_in_country", "Born in Singapore or not"), ("marital", "Marital status"),
        ("employment", "Employment")]
GROUPS = ["ALL", "ethnic=Chinese", "ethnic=Malay", "ethnic=Indian", "age_band=18-29", "age_band=60+"]


def setup():
    packet = json.load(open(PACKET))
    targets = [q["id"] for q in packet["questions"]]
    df, qs = wvs.load_respondents("Singapore")
    record_items = [i for i in qs if i not in targets]
    rng = np.random.default_rng(SEED)
    ok = df[df[targets].notna().sum(axis=1) >= 15]
    pids = []
    for g, n in PER_GROUP.items():
        pool = ok[ok.ethnic == g].pid.tolist()
        pids += sorted(rng.choice(pool, size=n, replace=False).tolist())
    return df, qs, targets, record_items, pids


def system_prompt(qs, targets) -> str:
    lines = ["You predict how one real person answered a survey: the World Values Survey in Singapore, 2019-2020.",
             "For each question below, give the probability that this person chose each answer option, in the order listed.",
             "Reply with JSON only, one key per question id, each value a list of probabilities that sum to 1, for example",
             '{"' + targets[0] + '": [0.1, 0.6, 0.2, 0.1], ...}.', "", "Questions:"]
    for t in targets:
        q = qs[t]
        lines.append(f"{t}: {q.text}")
        lines += [f"  {i + 1}. {o}" for i, o in enumerate(q.options)]
    return "\n".join(lines)


def person_prompt(row, qs, record_items, arm: str) -> str:
    val = lambda c: int(row[c]) if c == "age" else row[c]
    who = [f"- {label}: {val(c)}" for c, label in DEMO if pd.notna(row[c]) and str(row[c]) not in ("NA", "nan")]
    text = ["About this person:", *who]
    if arm == "record":
        answered = [(i, row[i]) for i in record_items if row[i] is not None and pd.notna(row[i])]
        text += ["", f"Their own answers to {len(answered)} other questions in the same survey:"]
        text += [f"- {qs[i].text} -> {a}" for i, a in answered]
    text += ["", "Predict this person's answers to every question listed in your instructions. JSON only."]
    return "\n".join(text)


def requests(df, qs, targets, record_items, pids):
    system = [{"type": "text", "text": system_prompt(qs, targets), "cache_control": {"type": "ephemeral"}}]
    rows = df.set_index("pid")
    out = []
    for pid in pids:
        for arm in ("demographics", "record"):
            out.append({"custom_id": f"{arm}__{pid}", "params": {
                "model": MODEL, "max_tokens": MAX_TOKENS, "output_config": {"effort": EFFORT}, "system": system,
                "messages": [{"role": "user", "content": person_prompt(rows.loc[pid], qs, record_items, arm)}]}})
    return out


def worst_case(reqs) -> tuple[float, int]:
    """Dollars if every request used all its output tokens and nothing was cached; about 3.5 characters per token, rounded up."""
    n_in = sum(int(len(r["params"]["system"][0]["text"] + r["params"]["messages"][0]["content"]) / 3.5) + 50 for r in reqs)
    cost = BATCH_DISCOUNT * (n_in * PRICE_IN + len(reqs) * MAX_TOKENS * PRICE_OUT)
    return cost, n_in


def parse(text: str, qs, targets) -> dict[str, list[float]] | None:
    m = re.search(r"\{.*\}", text, flags=re.S)
    if not m:
        return None
    try:
        raw = json.loads(m.group(0))
    except json.JSONDecodeError:
        return None
    out = {}
    for t in targets:
        v = raw.get(t)
        if not isinstance(v, list) or len(v) != len(qs[t].options) or any(not isinstance(x, (int, float)) or x < 0 for x in v) or sum(v) <= 0:
            return None
        out[t] = [x / sum(v) for x in v]
    return out


def plan():
    df, qs, targets, record_items, pids = setup()
    reqs = requests(df, qs, targets, record_items, pids)
    cost, n_in = worst_case(reqs)
    print(f"{len(pids)} people ({PER_GROUP}), {len(targets)} questions, {len(record_items)} record questions available; "
          f"{len(reqs)} requests to {MODEL} (effort {EFFORT}, max {MAX_TOKENS} output tokens each).")
    print(f"Estimated input about {n_in:,} tokens; worst case ${cost:.2f} with the batch discount (budget ${BUDGET:.2f}).")
    print("\nExample record prompt (first 1,200 characters):\n" + reqs[1]["params"]["messages"][0]["content"][:1200])


def run():
    import anthropic
    key = os.environ.get("DIGITAL_CITIZENS_API_KEY")
    if key:
        client = anthropic.Anthropic(api_key=key)
    else:  # the network secret: through the proxy, with no key header of our own for it to replace
        http = anthropic.DefaultHttpxClient(proxy=os.environ["HTTPS_PROXY"], verify=os.environ.get("SSL_CERT_FILE", "/root/.ccr/ca-bundle.crt"))
        client = anthropic.Anthropic(api_key=None, default_headers={"X-Api-Key": anthropic.omit}, http_client=http)
    try:
        client.messages.batches.list(limit=1)
    except anthropic.AuthenticationError:
        sys.exit("The Claude API did not accept the key: check the network secret (header x-api-key, website "
                 "api.anthropic.com, path prefix /v1/messages/batches) and start a new session. Nothing was sent.")
    df, qs, targets, record_items, pids = setup()
    reqs = requests(df, qs, targets, record_items, pids)
    cost, n_in = worst_case(reqs)  # a conservative estimate from the prompts' length
    print(f"{len(reqs)} requests; input about {n_in:,} tokens; worst case ${cost:.2f} (budget ${BUDGET:.2f}).")
    if cost > BUDGET:
        sys.exit("Worst case is over budget: nothing was sent. Lower MAX_TOKENS or the number of people.")
    batch = client.messages.batches.create(requests=reqs)
    print("Batch", batch.id, "submitted; waiting (most finish within an hour).")
    while (batch := client.messages.batches.retrieve(batch.id)).processing_status != "ended":
        time.sleep(60)
    preds, failed, usage = {}, [], {"input": 0, "cache_read": 0, "cache_write": 0, "output": 0}
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
        p = parse(text, qs, targets) if msg.stop_reason not in ("refusal", "max_tokens") else None
        if p is None:
            failed.append([res.custom_id, msg.stop_reason]); continue
        preds.setdefault(arm, {})[pid] = p
    spent = BATCH_DISCOUNT * ((usage["input"] + 1.25 * usage["cache_write"] + 0.05 * usage["cache_read"]) * PRICE_IN + usage["output"] * PRICE_OUT)
    PRED.write_text(json.dumps({"batch": batch.id, "model": MODEL, "effort": EFFORT, "pids": pids, "targets": targets,
                                "usage": usage, "cost_estimate_usd": round(spent, 2), "failed": failed, "predictions": preds}, indent=1))
    print(f"Saved {sum(len(v) for v in preds.values())} predictions, {len(failed)} failed; about ${spent:.2f} spent. Now run: score")


def _shares(answers: pd.Series, weights: pd.Series, options: list[str]) -> np.ndarray:
    w = weights[answers.notna()]; a = answers[answers.notna()]
    return np.array([w[a == o].sum() for o in options]) / w.sum()


def score():
    df, qs, targets, record_items, _ = setup()
    P = json.load(open(PRED))
    pids, preds = P["pids"], P["predictions"]
    rows = df.set_index("pid")
    sample, rest = rows.loc[pids], rows.drop(index=pids)
    arms = [a for a in ("demographics", "record") if a in preds]
    lines = ["# Record-reading trial (pilot): Singapore, 100 people, 20 questions", "",
             f"Model {P['model']} (effort {P['effort']}), one batch ({P['batch']}); usage {P['usage']}; "
             f"about ${P['cost_estimate_usd']} spent; {len(P['failed'])} requests failed or could not be read.", "",
             "## Individual people: how often the most likely answer was the one they gave", "",
             "| arm | people | answers scored | top choice right | average probability on their real answer |", "|---|---|---|---|---|"]
    res = {"individual": {}, "groups": {}}
    for arm in arms:
        hit, prob, n = [], [], 0
        for pid, p in preds[arm].items():
            for t in targets:
                a = rows.at[pid, t]
                if a is None or pd.isna(a):
                    continue
                k = qs[t].options.index(a); n += 1
                hit.append(int(np.argmax(p[t]) == k)); prob.append(p[t][k])
        res["individual"][arm] = {"people": len(preds[arm]), "answers": n, "top_choice": float(np.mean(hit)), "prob_on_answer": float(np.mean(prob))}
        lines.append(f"| {arm} | {len(preds[arm])} | {n} | {np.mean(hit):.1%} | {np.mean(prob):.2f} |")
    lines += ["", "## Groups: points off against the rest of the survey (median over group-question cells)", "",
              "| group | people in the sample | the 100 people's own answers | " + " | ".join(arms) + " |", "|---|---|---|" + "---|" * len(arms)]
    cells = {k: [] for k in ["survey of 100", *arms]}
    for g in GROUPS:
        key, _, val = g.partition("=")
        members = sample.index if g == "ALL" else sample.index[sample[key] == val]
        truth_pool = rest if g == "ALL" else rest[rest[key] == val]
        # the sample is a third each by ethnicity: weight members back to the group's real ethnic mix
        mix = truth_pool.groupby("ethnic").weight.sum() / truth_pool.weight.sum()
        have_mix = sample.loc[members, "ethnic"].value_counts(normalize=True)
        wt = sample.loc[members, "ethnic"].map(lambda e: mix.get(e, 0) / have_mix[e])
        row = {k: [] for k in cells}
        for t in targets:
            opts = qs[t].options
            truth = _shares(truth_pool[t], truth_pool["weight"], opts)
            own = sample.loc[members, t]
            if own.notna().sum() >= 5:
                row["survey of 100"].append(100 * np.abs(_shares(own, wt, opts) - truth).mean())
            for arm in arms:
                have = [pid for pid in members if pid in preds[arm]]
                if have:
                    est = np.average([preds[arm][pid][t] for pid in have], axis=0, weights=wt[have].to_numpy())
                    row[arm].append(100 * np.abs(est - truth).mean())
        for k in cells:
            cells[k] += row[k]
        res["groups"][g] = {k: float(np.median(v)) for k, v in row.items() if v}
        lines.append(f"| {g} | {len(members)} | " + " | ".join(f"{np.median(row[k]):.1f}" if row[k] else "-" for k in cells) + " |")
    lines.append("| all groups | | " + " | ".join(f"{np.median(cells[k]):.1f}" for k in cells) + " |")
    res["groups"]["all"] = {k: float(np.median(v)) for k, v in cells.items()}
    lines += ["", "The sample is about a third each Chinese, Malay and Indian Singaporeans; within each group, people are weighted back to",
              "the group's real ethnic mix. The truth for each group is the weighted answers of everyone in the survey who is not in",
              "the sample. A pilot: read it as a signal, not a result.",
              "", "Generated by scripts/record_reading_trial.py."]
    (OUT / "record_reading_trial.md").write_text("\n".join(lines) + "\n")
    (OUT / "record_reading_trial.json").write_text(json.dumps(res, indent=1))
    print("\n".join(lines))


if __name__ == "__main__":
    {"plan": plan, "run": run, "score": score}[sys.argv[1] if len(sys.argv) > 1 else "plan"]()
