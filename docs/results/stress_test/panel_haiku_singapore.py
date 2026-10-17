#!/usr/bin/env python3
"""Haiku 5.5 panel estimates for WVS wave 7, Singapore (blind forecasting test).

Writes haiku_singapore.json next to this file: one entry per question and group,
{"question_id", "group", "probs"}, with probs in the packet's option order.
Estimates come from general knowledge only; no survey results were consulted.
"""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
PACKET = os.path.join(HERE, "packet_singapore.json")
OUT = os.path.join(HERE, "haiku_singapore.json")

# Short group codes -> group names exactly as written in the packet.
CODES = {
    "ALL": "ALL",
    "CHN": "ethnic=Chinese",
    "MAL": "ethnic=Malay",
    "IND": "ethnic=Indian",
    "Y": "age_band=18-29",
    "O": "age_band=60+",
    "LOW": "education3=Lower",
    "HIGH": "education3=Higher",
    "MUS": "religion=Muslim",
    "NONE": "religion=No religion",
}
GROUP_TO_CODE = {v: k for k, v in CODES.items()}

# Share of each group choosing each option, in the packet's option order.
EST = {
    "Q3": {  # leisure time: very / rather / not very / not at all important
        "ALL": [0.30, 0.45, 0.20, 0.05],
        "CHN": [0.29, 0.46, 0.20, 0.05],
        "MAL": [0.32, 0.45, 0.18, 0.05],
        "IND": [0.30, 0.45, 0.20, 0.05],
        "Y": [0.34, 0.45, 0.17, 0.04],
        "O": [0.22, 0.44, 0.25, 0.09],
        "LOW": [0.30, 0.44, 0.21, 0.05],
        "HIGH": [0.30, 0.46, 0.19, 0.05],
        "MUS": [0.31, 0.45, 0.19, 0.05],
        "NONE": [0.33, 0.46, 0.16, 0.05],
    },
    "Q6": {  # religion importance: very / rather / not very / not at all
        "ALL": [0.35, 0.27, 0.18, 0.20],
        "CHN": [0.28, 0.28, 0.20, 0.24],
        "MAL": [0.75, 0.16, 0.06, 0.03],
        "IND": [0.45, 0.30, 0.14, 0.11],
        "Y": [0.25, 0.28, 0.22, 0.25],
        "O": [0.50, 0.27, 0.11, 0.12],
        "LOW": [0.42, 0.28, 0.14, 0.16],
        "HIGH": [0.27, 0.28, 0.20, 0.25],
        "MUS": [0.78, 0.15, 0.05, 0.02],
        "NONE": [0.05, 0.12, 0.30, 0.53],
    },
    "Q14": {  # determination/perseverance: important / not mentioned
        "ALL": [0.55, 0.45],
        "CHN": [0.55, 0.45],
        "MAL": [0.52, 0.48],
        "IND": [0.57, 0.43],
        "Y": [0.55, 0.45],
        "O": [0.56, 0.44],
        "LOW": [0.55, 0.45],
        "HIGH": [0.56, 0.44],
        "MUS": [0.52, 0.48],
        "NONE": [0.56, 0.44],
    },
    "Q18": {  # drug addicts as unwanted neighbours: mentioned / not mentioned
        "ALL": [0.55, 0.45],
        "CHN": [0.52, 0.48],
        "MAL": [0.68, 0.32],
        "IND": [0.55, 0.45],
        "Y": [0.42, 0.58],
        "O": [0.66, 0.34],
        "LOW": [0.61, 0.39],
        "HIGH": [0.48, 0.52],
        "MUS": [0.68, 0.32],
        "NONE": [0.42, 0.58],
    },
    "Q64": {  # confidence in churches/mosques/temples: great deal / quite a lot / not very much / none
        "ALL": [0.29, 0.41, 0.20, 0.10],
        "CHN": [0.24, 0.42, 0.22, 0.12],
        "MAL": [0.52, 0.36, 0.09, 0.03],
        "IND": [0.36, 0.40, 0.17, 0.07],
        "Y": [0.20, 0.40, 0.25, 0.15],
        "O": [0.36, 0.42, 0.15, 0.07],
        "LOW": [0.32, 0.42, 0.18, 0.08],
        "HIGH": [0.24, 0.42, 0.22, 0.12],
        "MUS": [0.56, 0.34, 0.08, 0.02],
        "NONE": [0.04, 0.16, 0.37, 0.43],
    },
    "Q66": {  # confidence in the press
        "ALL": [0.06, 0.40, 0.38, 0.16],
        "CHN": [0.05, 0.40, 0.39, 0.16],
        "MAL": [0.08, 0.44, 0.34, 0.14],
        "IND": [0.06, 0.40, 0.38, 0.16],
        "Y": [0.04, 0.34, 0.42, 0.20],
        "O": [0.08, 0.48, 0.31, 0.13],
        "LOW": [0.07, 0.43, 0.36, 0.14],
        "HIGH": [0.05, 0.37, 0.41, 0.17],
        "MUS": [0.08, 0.44, 0.34, 0.14],
        "NONE": [0.05, 0.36, 0.41, 0.18],
    },
    "Q70": {  # confidence in the courts
        "ALL": [0.27, 0.46, 0.19, 0.08],
        "CHN": [0.26, 0.46, 0.20, 0.08],
        "MAL": [0.25, 0.48, 0.19, 0.08],
        "IND": [0.28, 0.44, 0.20, 0.08],
        "Y": [0.22, 0.46, 0.22, 0.10],
        "O": [0.32, 0.45, 0.16, 0.07],
        "LOW": [0.27, 0.47, 0.18, 0.08],
        "HIGH": [0.27, 0.45, 0.20, 0.08],
        "MUS": [0.25, 0.48, 0.19, 0.08],
        "NONE": [0.22, 0.44, 0.24, 0.10],
    },
    "Q76": {  # confidence in elections
        "ALL": [0.19, 0.40, 0.28, 0.13],
        "CHN": [0.18, 0.40, 0.29, 0.13],
        "MAL": [0.22, 0.42, 0.24, 0.12],
        "IND": [0.19, 0.41, 0.27, 0.13],
        "Y": [0.14, 0.38, 0.32, 0.16],
        "O": [0.24, 0.42, 0.22, 0.12],
        "LOW": [0.20, 0.42, 0.26, 0.12],
        "HIGH": [0.18, 0.39, 0.30, 0.13],
        "MUS": [0.22, 0.42, 0.24, 0.12],
        "NONE": [0.15, 0.37, 0.31, 0.17],
    },
    "Q107": {  # 1 private ownership of business ... 10 government ownership
        "ALL": [0.12, 0.07, 0.09, 0.12, 0.22, 0.14, 0.10, 0.06, 0.03, 0.05],
        "CHN": [0.13, 0.07, 0.09, 0.12, 0.22, 0.14, 0.10, 0.06, 0.03, 0.04],
        "MAL": [0.07, 0.05, 0.07, 0.10, 0.20, 0.17, 0.13, 0.10, 0.06, 0.05],
        "IND": [0.12, 0.07, 0.09, 0.12, 0.22, 0.14, 0.10, 0.06, 0.03, 0.05],
        "Y": [0.10, 0.07, 0.09, 0.12, 0.22, 0.15, 0.11, 0.07, 0.04, 0.03],
        "O": [0.11, 0.07, 0.09, 0.12, 0.22, 0.14, 0.10, 0.07, 0.04, 0.04],
        "LOW": [0.09, 0.06, 0.08, 0.11, 0.21, 0.15, 0.12, 0.09, 0.04, 0.05],
        "HIGH": [0.14, 0.08, 0.10, 0.12, 0.22, 0.13, 0.09, 0.06, 0.03, 0.03],
        "MUS": [0.07, 0.05, 0.07, 0.10, 0.20, 0.17, 0.13, 0.10, 0.06, 0.05],
        "NONE": [0.13, 0.08, 0.09, 0.12, 0.22, 0.13, 0.10, 0.06, 0.03, 0.04],
    },
    "Q108": {  # 1 government should take more responsibility ... 10 people should provide for themselves
        "ALL": [0.05, 0.04, 0.06, 0.09, 0.15, 0.16, 0.14, 0.13, 0.07, 0.11],
        "CHN": [0.04, 0.04, 0.06, 0.09, 0.15, 0.16, 0.14, 0.13, 0.08, 0.11],
        "MAL": [0.09, 0.07, 0.09, 0.11, 0.15, 0.14, 0.12, 0.11, 0.06, 0.06],
        "IND": [0.06, 0.05, 0.07, 0.09, 0.15, 0.16, 0.14, 0.12, 0.07, 0.09],
        "Y": [0.05, 0.04, 0.06, 0.09, 0.15, 0.15, 0.14, 0.13, 0.08, 0.11],
        "O": [0.07, 0.06, 0.08, 0.10, 0.16, 0.16, 0.13, 0.11, 0.06, 0.07],
        "LOW": [0.07, 0.05, 0.07, 0.09, 0.15, 0.15, 0.13, 0.12, 0.07, 0.10],
        "HIGH": [0.04, 0.03, 0.05, 0.08, 0.14, 0.16, 0.15, 0.14, 0.08, 0.13],
        "MUS": [0.09, 0.07, 0.09, 0.11, 0.15, 0.14, 0.12, 0.11, 0.06, 0.06],
        "NONE": [0.04, 0.04, 0.06, 0.09, 0.15, 0.16, 0.14, 0.13, 0.08, 0.11],
    },
    "Q126": {  # immigrants increase terrorism risk: disagree / hard to say / agree
        "ALL": [0.43, 0.25, 0.32],
        "CHN": [0.44, 0.25, 0.31],
        "MAL": [0.40, 0.26, 0.34],
        "IND": [0.42, 0.26, 0.32],
        "Y": [0.50, 0.25, 0.25],
        "O": [0.36, 0.24, 0.40],
        "LOW": [0.38, 0.24, 0.38],
        "HIGH": [0.48, 0.25, 0.27],
        "MUS": [0.40, 0.26, 0.34],
        "NONE": [0.50, 0.25, 0.25],
    },
    "Q131": {  # feel secure in neighbourhood: very / quite / not very / not at all
        "ALL": [0.55, 0.38, 0.06, 0.01],
        "CHN": [0.56, 0.37, 0.06, 0.01],
        "MAL": [0.50, 0.40, 0.08, 0.02],
        "IND": [0.52, 0.39, 0.08, 0.01],
        "Y": [0.56, 0.37, 0.06, 0.01],
        "O": [0.52, 0.38, 0.08, 0.02],
        "LOW": [0.50, 0.40, 0.08, 0.02],
        "HIGH": [0.58, 0.36, 0.05, 0.01],
        "MUS": [0.50, 0.40, 0.08, 0.02],
        "NONE": [0.56, 0.37, 0.06, 0.01],
    },
    "Q142": {  # worried about losing job: very much / great deal / not much / not at all
        "ALL": [0.12, 0.20, 0.36, 0.32],
        "CHN": [0.11, 0.19, 0.37, 0.33],
        "MAL": [0.14, 0.22, 0.36, 0.28],
        "IND": [0.13, 0.21, 0.36, 0.30],
        "Y": [0.14, 0.22, 0.36, 0.28],
        "O": [0.08, 0.14, 0.33, 0.45],
        "LOW": [0.18, 0.24, 0.33, 0.25],
        "HIGH": [0.08, 0.18, 0.39, 0.35],
        "MUS": [0.14, 0.22, 0.36, 0.28],
        "NONE": [0.11, 0.19, 0.37, 0.33],
    },
    "Q177": {  # claiming benefits not entitled to: 1 never justifiable ... 10 always justifiable
        "ALL": [0.58, 0.08, 0.06, 0.05, 0.08, 0.03, 0.04, 0.03, 0.01, 0.04],
        "CHN": [0.60, 0.08, 0.06, 0.05, 0.07, 0.03, 0.04, 0.03, 0.01, 0.03],
        "MAL": [0.55, 0.08, 0.06, 0.05, 0.09, 0.03, 0.04, 0.04, 0.02, 0.04],
        "IND": [0.58, 0.08, 0.06, 0.05, 0.08, 0.03, 0.04, 0.03, 0.02, 0.03],
        "Y": [0.50, 0.09, 0.07, 0.06, 0.10, 0.04, 0.05, 0.04, 0.02, 0.03],
        "O": [0.66, 0.07, 0.05, 0.04, 0.06, 0.02, 0.03, 0.02, 0.01, 0.04],
        "LOW": [0.56, 0.09, 0.06, 0.05, 0.09, 0.03, 0.04, 0.03, 0.02, 0.03],
        "HIGH": [0.62, 0.08, 0.06, 0.05, 0.07, 0.03, 0.04, 0.03, 0.01, 0.01],
        "MUS": [0.55, 0.08, 0.06, 0.05, 0.09, 0.03, 0.04, 0.04, 0.02, 0.04],
        "NONE": [0.58, 0.08, 0.06, 0.05, 0.08, 0.03, 0.04, 0.03, 0.02, 0.03],
    },
    "Q184": {  # abortion: 1 never justifiable ... 10 always justifiable
        "ALL": [0.40, 0.06, 0.07, 0.07, 0.13, 0.07, 0.08, 0.06, 0.03, 0.03],
        "CHN": [0.37, 0.06, 0.07, 0.07, 0.14, 0.07, 0.08, 0.06, 0.04, 0.04],
        "MAL": [0.62, 0.09, 0.07, 0.05, 0.07, 0.03, 0.03, 0.02, 0.01, 0.01],
        "IND": [0.36, 0.07, 0.07, 0.07, 0.14, 0.07, 0.08, 0.06, 0.04, 0.04],
        "Y": [0.26, 0.05, 0.06, 0.07, 0.15, 0.09, 0.10, 0.10, 0.06, 0.06],
        "O": [0.52, 0.07, 0.07, 0.06, 0.12, 0.06, 0.04, 0.03, 0.02, 0.01],
        "LOW": [0.45, 0.07, 0.07, 0.06, 0.13, 0.06, 0.07, 0.04, 0.03, 0.02],
        "HIGH": [0.31, 0.06, 0.07, 0.07, 0.15, 0.08, 0.09, 0.08, 0.05, 0.04],
        "MUS": [0.62, 0.09, 0.07, 0.05, 0.07, 0.03, 0.03, 0.02, 0.01, 0.01],
        "NONE": [0.22, 0.05, 0.06, 0.07, 0.15, 0.09, 0.11, 0.11, 0.07, 0.07],
    },
    "Q209": {  # political action, signing a petition: have done / might do / would never do
        "ALL": [0.18, 0.38, 0.44],
        "CHN": [0.19, 0.39, 0.42],
        "MAL": [0.10, 0.30, 0.60],
        "IND": [0.24, 0.40, 0.36],
        "Y": [0.28, 0.44, 0.28],
        "O": [0.07, 0.28, 0.65],
        "LOW": [0.11, 0.32, 0.57],
        "HIGH": [0.29, 0.42, 0.29],
        "MUS": [0.10, 0.30, 0.60],
        "NONE": [0.24, 0.42, 0.34],
    },
    "Q237": {  # army rule: very good / fairly good / fairly bad / very bad
        "ALL": [0.05, 0.15, 0.33, 0.47],
        "CHN": [0.05, 0.15, 0.34, 0.46],
        "MAL": [0.06, 0.17, 0.35, 0.42],
        "IND": [0.05, 0.15, 0.33, 0.47],
        "Y": [0.03, 0.12, 0.33, 0.52],
        "O": [0.08, 0.20, 0.32, 0.40],
        "LOW": [0.07, 0.18, 0.33, 0.42],
        "HIGH": [0.03, 0.12, 0.33, 0.52],
        "MUS": [0.06, 0.17, 0.35, 0.42],
        "NONE": [0.04, 0.13, 0.34, 0.49],
    },
    "Q240": {  # left-right: 1 left ... 10 right
        "ALL": [0.03, 0.03, 0.05, 0.10, 0.20, 0.20, 0.15, 0.10, 0.06, 0.08],
        "CHN": [0.03, 0.03, 0.05, 0.10, 0.20, 0.20, 0.15, 0.10, 0.06, 0.08],
        "MAL": [0.04, 0.04, 0.06, 0.12, 0.20, 0.18, 0.14, 0.09, 0.06, 0.07],
        "IND": [0.04, 0.04, 0.06, 0.11, 0.20, 0.19, 0.15, 0.10, 0.05, 0.06],
        "Y": [0.05, 0.05, 0.07, 0.12, 0.19, 0.18, 0.14, 0.09, 0.05, 0.06],
        "O": [0.02, 0.02, 0.04, 0.09, 0.20, 0.21, 0.16, 0.12, 0.07, 0.07],
        "LOW": [0.03, 0.03, 0.05, 0.10, 0.20, 0.20, 0.15, 0.11, 0.06, 0.07],
        "HIGH": [0.04, 0.04, 0.06, 0.11, 0.19, 0.18, 0.15, 0.10, 0.07, 0.06],
        "MUS": [0.04, 0.04, 0.06, 0.12, 0.20, 0.18, 0.14, 0.09, 0.06, 0.07],
        "NONE": [0.04, 0.04, 0.06, 0.10, 0.19, 0.19, 0.15, 0.11, 0.06, 0.06],
    },
    "Q250": {  # importance of living in a democracy: 1 not at all ... 10 absolutely important
        "ALL": [0.03, 0.02, 0.03, 0.04, 0.09, 0.10, 0.14, 0.15, 0.12, 0.28],
        "CHN": [0.03, 0.02, 0.03, 0.04, 0.09, 0.10, 0.14, 0.15, 0.12, 0.28],
        "MAL": [0.03, 0.02, 0.03, 0.04, 0.10, 0.11, 0.14, 0.14, 0.12, 0.27],
        "IND": [0.02, 0.02, 0.03, 0.04, 0.09, 0.10, 0.14, 0.15, 0.13, 0.28],
        "Y": [0.02, 0.02, 0.03, 0.04, 0.08, 0.09, 0.13, 0.15, 0.13, 0.31],
        "O": [0.04, 0.03, 0.04, 0.05, 0.10, 0.11, 0.14, 0.14, 0.10, 0.25],
        "LOW": [0.04, 0.03, 0.04, 0.05, 0.10, 0.11, 0.14, 0.14, 0.11, 0.24],
        "HIGH": [0.02, 0.01, 0.02, 0.03, 0.07, 0.09, 0.14, 0.16, 0.14, 0.32],
        "MUS": [0.03, 0.02, 0.03, 0.04, 0.10, 0.11, 0.14, 0.14, 0.12, 0.27],
        "NONE": [0.02, 0.02, 0.03, 0.04, 0.08, 0.09, 0.13, 0.15, 0.13, 0.31],
    },
    "Q253": {  # respect for individual human rights: great deal / fairly much / not much / no respect at all
        "ALL": [0.12, 0.52, 0.28, 0.08],
        "CHN": [0.12, 0.52, 0.28, 0.08],
        "MAL": [0.14, 0.54, 0.26, 0.06],
        "IND": [0.12, 0.52, 0.28, 0.08],
        "Y": [0.08, 0.45, 0.35, 0.12],
        "O": [0.16, 0.56, 0.22, 0.06],
        "LOW": [0.13, 0.56, 0.25, 0.06],
        "HIGH": [0.10, 0.48, 0.31, 0.11],
        "MUS": [0.14, 0.54, 0.26, 0.06],
        "NONE": [0.10, 0.48, 0.31, 0.11],
    },
}


def main():
    with open(PACKET, encoding="utf-8") as f:
        packet = json.load(f)

    groups = packet["groups"]
    if set(groups) != set(CODES.values()):
        raise SystemExit("group list in the packet does not match CODES")

    questions = packet["questions"]
    if {q["id"] for q in questions} != set(EST):
        raise SystemExit("question ids in the packet do not match EST")

    entries = []
    for q in questions:
        qid = q["id"]
        n_opts = len(q["options"])
        for group in groups:
            probs = EST[qid][GROUP_TO_CODE[group]]
            if len(probs) != n_opts:
                raise SystemExit(f"{qid} / {group}: {len(probs)} values for {n_opts} options")
            total = sum(probs)
            probs = [round(p / total, 6) for p in probs]
            entries.append({"question_id": qid, "group": group, "probs": probs})

    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(entries, f, indent=2)

    # Self-check on the file just written.
    with open(OUT, encoding="utf-8") as f:
        written = json.load(f)
    option_counts = {q["id"]: len(q["options"]) for q in questions}
    assert len(written) == len(questions) * len(groups) == 200, len(written)
    for e in written:
        assert e["group"] in groups
        assert len(e["probs"]) == option_counts[e["question_id"]], e["question_id"]
        assert all(p >= 0 for p in e["probs"])
        assert abs(sum(e["probs"]) - 1.0) < 1e-4, (e["question_id"], e["group"], sum(e["probs"]))
    keys = {(e["question_id"], e["group"]) for e in written}
    assert len(keys) == 200

    print(f"wrote {len(written)} entries to {OUT}")


if __name__ == "__main__":
    main()
