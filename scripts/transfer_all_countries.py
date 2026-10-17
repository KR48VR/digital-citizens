"""Record-anchored citizens with the mapping learned from EVERY other WVS7 country available on disk.

Compares, for Singapore and China packets: Claude zero-shot; record-anchored trained on 2 countries;
record-anchored trained on all other countries; and both combined with the real population level.
Writes docs/results/stress_test/record_transfer_all_countries.md and .csv.
"""
from __future__ import annotations

import json
import sys
import time
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from digital_citizens.data import wvs  # noqa: E402
from digital_citizens.evaluate import harness as H  # noqa: E402
from digital_citizens.evaluate.calibrate import apply_gap_scale  # noqa: E402
from digital_citizens.evaluate.transfer import cross_country_transfer  # noqa: E402

OUT = Path("docs/results/stress_test")
DEMO = ["sex", "age_band", "education3", "income3", "religion", "born_in_country"]


def load_all(exclude: set[str]) -> list:
    benches = []
    for name in sorted(wvs.available_countries()):
        if name in exclude:
            continue
        try:
            benches.append(wvs.benchmark(name, segment_keys=["sex"]))
        except Exception as e:  # noqa: BLE001
            print("skip", name, type(e).__name__, str(e)[:80])
    return benches


def summarise(label: str, bench, variants: dict, groups: list[str]) -> pd.DataFrame:
    rows = []
    for name, v in variants.items():
        s = H.score(v, bench, name); s = s[s.group.isin(groups)]
        seg = H.segment_fidelity(v, bench, name)
        rows.append({"experiment": label, "method": name, "pop_mae": s[s.group == "ALL"].mae_pts.median(), "seg_mae_median": s[s.group != "ALL"].mae_pts.median(), "seg_mae_mean": s[s.group != "ALL"].mae_pts.mean(), "gap_r": seg.gap_r.median(), "gap_slope": seg.gap_slope.median(), "dispersion": seg.dispersion_ratio.median()})
    return pd.DataFrame(rows)


def main() -> None:
    t0 = time.time()
    results = []
    examples = []
    for country, packet_file, zs_file, two in [
        ("Singapore", "packet_wvs_singapore.json", "predictions_wvs_singapore_claude_in_session.json", ["United States", "China"]),
        ("China", "packet_wvs_china.json", "predictions_wvs_china_claude_in_session.json", ["United States", "Singapore"]),
    ]:
        bench = wvs.benchmark(country)
        packet = json.load(open(OUT / packet_file)); tg = [q["id"] for q in packet["questions"]]; groups = packet["groups"]
        zs = {(r["question_id"], r["group"]): r["probs"] for r in json.load(open(OUT / zs_file))}
        real = {k: d.normalised() for k, d in bench.real.items()}
        two_b = [wvs.benchmark(c, segment_keys=["sex"]) for c in two]
        all_b = load_all({country})
        n_all = sum(len(b.respondents) for b in all_b)
        print(f"{country}: training on {len(all_b)} countries, {n_all} respondents", flush=True)
        cc2 = cross_country_transfer(two_b, bench, tg, DEMO, groups)
        ccA = cross_country_transfer(all_b, bench, tg, DEMO, groups, C=0.3)
        variants = {
            "claude zero-shot": zs,
            f"record-anchored, trained on {len(two)} countries": cc2,
            f"record-anchored, trained on {len(all_b)} countries ({n_all:,} people)": ccA,
            "human level + record differences (2 countries)": apply_gap_scale(cc2, 1.0, tg, groups, base=real),
            f"human level + record differences ({len(all_b)} countries)": apply_gap_scale(ccA, 1.0, tg, groups, base=real),
            "everyone is average (human level only)": {(q, g): real[(q, "ALL")] for q in tg for g in groups if (q, g) in real},
        }
        results.append(summarise(country, bench, variants, groups))
        if country == "Singapore":
            for q, opt, label in [("Q142", 0, "job worry: very much"), ("Q209", 2, "petition: would never"), ("Q237", 3, "army rule: very bad")]:
                for g in ["ALL", "ethnic=Malay", "ethnic=Chinese", "education3=Lower", "education3=Higher", "age_band=60+"]:
                    if (q, g) in real:
                        examples.append({"item": label, "group": g, "real": 100 * real[(q, g)][opt], "claude": 100 * zs[(q, g)][opt] if (q, g) in zs else None,
                                         "record_2c": 100 * cc2[(q, g)][opt] if (q, g) in cc2 else None, "record_all": 100 * ccA[(q, g)][opt] if (q, g) in ccA else None,
                                         "human_level+record_all": 100 * variants[f"human level + record differences ({len(all_b)} countries)"][(q, g)][opt] if (q, g) in ccA else None})
    df = pd.concat(results, ignore_index=True).round(2)
    ex = pd.DataFrame(examples).round(1)
    df.to_csv(OUT / "record_transfer_all_countries.csv", index=False)
    lines = ["# Record-anchored citizens: does learning from more countries help?", "", f"Generated {time.strftime('%Y-%m-%d %H:%M')} UTC; runtime {time.time()-t0:.0f}s.", ""]
    for label, sub in df.groupby("experiment", sort=False):
        lines += [f"## {label}", "", H.to_markdown(sub.drop(columns=["experiment"])), ""]
    lines += ["## Singapore examples (share choosing the option, %)", "", H.to_markdown(ex, 1), ""]
    (OUT / "record_transfer_all_countries.md").write_text("\n".join(lines))
    print("\n".join(lines))


if __name__ == "__main__":
    main()
