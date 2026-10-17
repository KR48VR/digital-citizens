"""Blind group predictions from a small open model run locally (default: Qwen2.5-3B-Instruct, built by Alibaba).

For each question and group in an answer-free packet, the model is asked to answer as a member of the group, and
its probabilities for the option letters (A, B, ...) on the next token are read off and normalised. This is the
usual "answer as a group member" method for open models; it needs no API key. The model never sees any answers.

Usage: open_model_panel.py <packet.json> <survey description> <out.json> [model id]
Run it in an environment with torch and transformers (not the project's .venv).
"""
from __future__ import annotations

import json
import string
import sys
import time

import torch
from transformers import AutoModelForCausalLM, AutoTokenizer


def main() -> None:
    packet_path, survey, out_path = sys.argv[1], sys.argv[2], sys.argv[3]
    model_id = sys.argv[4] if len(sys.argv) > 4 else "Qwen/Qwen2.5-3B-Instruct"
    packet = json.load(open(packet_path))
    tok = AutoTokenizer.from_pretrained(model_id)
    model = AutoModelForCausalLM.from_pretrained(model_id, torch_dtype=torch.bfloat16)
    model.eval()
    letters = list(string.ascii_uppercase)
    out, t0 = [], time.time()
    for q in packet["questions"]:
        opts = q["options"]
        ids = [tok.encode(letters[i], add_special_tokens=False)[0] for i in range(len(opts))]
        for g in packet["groups"]:
            who = packet["group_descriptions"][g]
            msgs = [
                {"role": "system", "content": "You are taking part in a survey. Answer as the person described would, with a single letter."},
                {"role": "user", "content": f"Survey: {survey}.\nYou are one of the {who}.\n\nQuestion: {q['text']}\n\nOptions:\n"
                 + "\n".join(f"{letters[i]}. {o}" for i, o in enumerate(opts))
                 + "\n\nAnswer with the letter of the option you would choose."},
            ]
            text = tok.apply_chat_template(msgs, tokenize=False, add_generation_prompt=True)
            enc = tok(text, return_tensors="pt")
            with torch.no_grad():
                logits = model(**enc).logits[0, -1].float()
            p = torch.softmax(logits[ids], dim=0).tolist()
            out.append({"question_id": q["id"], "group": g, "probs": p})
        print(q["id"], f"{time.time() - t0:.0f}s", flush=True)
    json.dump(out, open(out_path, "w"))
    print("wrote", len(out), "predictions to", out_path)


if __name__ == "__main__":
    main()
