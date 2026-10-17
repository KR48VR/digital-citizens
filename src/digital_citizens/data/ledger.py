"""Evidence ledger: published survey findings (toplines and crosstabs) turned into priors.

A ledger row is one published number: "IPS 2024, n=4,000, Malay respondents, 'worried about job
security', 54% agree". Rows live in a CSV per country (``data/ledger/<country>.csv``) with these columns:

    ledger_id, country, source_org, title, year, url, fieldwork, population, n, sampling,
    question_text, options, group, shares, maps_to, option_map, confidence, notes

- ``options`` and ``shares``: '|'-separated, aligned (shares in percent; may sum to <100 if DK omitted).
- ``group``: 'ALL' or a benchmark segment key such as 'ethnic=Malay', 'age_band=18-29'.
- ``maps_to``: the benchmark question id the finding speaks to (e.g. WVS 'Q142').
- ``option_map``: for each ledger option, the benchmark option index(es) it covers, '|'-separated,
  with several indices joined by '+' (e.g. '0+1|2+3' maps a yes/no item onto a 4-point scale).
- ``confidence``: 0-1 multiplier on n for how comparable the wording/population/time is.
- ``sampling``: probability | online_panel | opt_in | social_media (used to set a default confidence).

``to_pseudocounts`` converts a row into pseudo-counts on the benchmark's option list: the row's
effective sample size (n * confidence) is spread over its options by the published shares, and within
a merged block it is split in the proportions of a reference distribution (e.g. the pooled prior), so a
coarse published number never invents detail it does not have.
"""
from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd

from .benchmark import Benchmark, Key

DEFAULT_CONFIDENCE = {"probability": 1.0, "online_panel": 0.5, "opt_in": 0.25, "social_media": 0.1}
COLUMNS = ["ledger_id", "country", "source_org", "title", "year", "url", "fieldwork", "population", "n", "sampling", "question_text", "options", "group", "shares", "maps_to", "option_map", "confidence", "notes"]


def load(path: str | Path) -> pd.DataFrame:
    df = pd.read_csv(path, dtype=str).fillna("")
    missing = [c for c in COLUMNS if c not in df.columns]
    if missing:
        raise ValueError(f"ledger missing columns: {missing}")
    df["n"] = pd.to_numeric(df["n"], errors="coerce")
    df["confidence"] = df.apply(lambda r: float(r["confidence"]) if r["confidence"] else DEFAULT_CONFIDENCE.get(r["sampling"], 0.5), axis=1)
    return df


def _parse_map(option_map: str, n_options: int) -> list[list[int]]:
    blocks = []
    for part in option_map.split("|"):
        idx = [int(x) for x in part.split("+") if x.strip() != ""]
        if any(i < 0 or i >= n_options for i in idx):
            raise ValueError(f"option_map index out of range: {option_map}")
        blocks.append(idx)
    return blocks


def to_pseudocounts(row: pd.Series, k: int, reference: np.ndarray | None = None) -> np.ndarray:
    """Pseudo-counts over the benchmark's k options for one ledger row."""
    shares = np.array([float(x) for x in str(row["shares"]).split("|")], dtype=float)
    blocks = _parse_map(str(row["option_map"]), k)
    if len(blocks) != len(shares):
        raise ValueError(f"{row['ledger_id']}: {len(shares)} shares vs {len(blocks)} option_map blocks")
    eff_n = float(row["n"]) * float(row["confidence"]) if pd.notna(row["n"]) else 0.0
    total_share = shares.sum()
    counts = np.zeros(k)
    ref = np.full(k, 1.0 / k) if reference is None else np.clip(np.asarray(reference, float), 1e-6, None)
    for share, idx in zip(shares, blocks):
        mass = eff_n * share / 100.0
        w = ref[idx] / ref[idx].sum()
        counts[idx] += mass * w
    # shares that sum to less than 100 (DK omitted) leave the remainder unallocated: that is intended
    return counts


def ledger_counts(df: pd.DataFrame, bench: Benchmark, reference: dict[Key, list[float]] | None = None) -> dict[Key, np.ndarray]:
    """Sum pseudo-counts of all ledger rows that map onto each (question, group) cell of the benchmark."""
    out: dict[Key, np.ndarray] = {}
    for _, r in df.iterrows():
        q = str(r["maps_to"]).strip()
        if not q or q not in bench.qmap:
            continue
        key = (q, str(r["group"]).strip() or "ALL")
        ref = np.asarray(reference[key]) if reference and key in reference else None
        c = to_pseudocounts(r, bench.qmap[q].k, ref)
        out[key] = out.get(key, np.zeros(bench.qmap[q].k)) + c
    return out


def coverage(df: pd.DataFrame, bench: Benchmark, groups: list[str]) -> pd.DataFrame:
    rows = []
    for q in bench.questions:
        sub = df[df["maps_to"] == q.id]
        rows.append({"question_id": q.id, "rows": len(sub), "groups_covered": sorted(set(sub["group"]) & set(groups)), "effective_n": float((sub["n"] * sub["confidence"]).sum()) if len(sub) else 0.0})
    return pd.DataFrame(rows)
