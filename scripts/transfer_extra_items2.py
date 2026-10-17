"""Record-anchored predictions (61-country mapping) for extra Singapore items so the ledger experiment can
cover more questions. Appends to docs/results/stress_test/record_all_singapore_pred.json."""
from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from digital_citizens.data import wvs  # noqa: E402
from digital_citizens.evaluate.transfer import cross_country_transfer  # noqa: E402

OUT = Path("docs/results/stress_test")
EXTRA = ["Q236", "Q62", "Q63", "Q70", "Q71", "Q123", "Q124", "Q128", "Q173", "Q237", "Q76", "Q131"]
GROUPS = ["ALL", "ethnic=Chinese", "ethnic=Malay", "ethnic=Indian", "age_band=18-29", "age_band=30-44", "age_band=45-59", "age_band=60+", "education3=Lower", "education3=Middle", "education3=Higher", "religion=Muslim", "religion=No religion", "religion=Buddhist", "religion=Protestant", "religion=Catholic", "religion=Hindu", "income3=Low", "income3=Medium", "income3=High", "sex=Male", "sex=Female"]
DEMO = ["sex", "age_band", "education3", "income3", "religion", "born_in_country"]

bench = wvs.benchmark("Singapore")
others = [wvs.benchmark(n, segment_keys=["sex"]) for n in sorted(wvs.available_countries()) if n != "Singapore"]
print(len(others), "training countries", flush=True)
cache = OUT / "record_all_singapore_pred_extra2.json"
have = json.loads(cache.read_text()) if cache.exists() else []
done = {(r["question_id"], r["group"]) for r in have}
targets = [q for q in EXTRA if q in bench.qmap]
rec = cross_country_transfer(others, bench, targets, DEMO, GROUPS)
have += [{"question_id": q, "group": g, "probs": p} for (q, g), p in rec.items() if (q, g) not in done]
cache.write_text(json.dumps(have))
print("cached", len(have), "cells", flush=True)
