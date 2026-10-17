"""Download the public datasets used by the v0 benchmarks into data/raw/.

Everything here is downloadable without a login. Run:  .venv/bin/python -I scripts/download_data.py
"""
from __future__ import annotations

import sys
import urllib.request
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data" / "raw"

FILES = {
    # US General Social Survey, single-year public-use files (NORC). Stata format.
    "gss/2024_stata.zip": "https://gss.norc.org/content/dam/gss/get-the-data/documents/stata/2024_stata.zip",
    "gss/2022_stata.zip": "https://gss.norc.org/content/dam/gss/get-the-data/documents/stata/2022_stata.zip",
    # GlobalOpinionQA (Anthropic): WVS + Pew Global Attitudes questions with per-country answer shares.
    "globalopinionqa/llm_global_opinions.parquet": "https://huggingface.co/datasets/Anthropic/llm_global_opinions/resolve/refs%2Fconvert%2Fparquet/default/train/0000.parquet",
    # Twin-2K-500 (Columbia): 2,058 US panelists, ~500 questions, with a retest wave.
    "twin2k/question_catalog.json": "https://huggingface.co/datasets/LLM-Digital-Twin/Twin-2K-500/resolve/main/question_catalog_and_human_response_csv/question_catalog.json",
    "twin2k/wave1_3_response_label.csv": "https://huggingface.co/datasets/LLM-Digital-Twin/Twin-2K-500/resolve/main/question_catalog_and_human_response_csv/wave1_3_response_label.csv",
    "twin2k/wave4_response_label.csv": "https://huggingface.co/datasets/LLM-Digital-Twin/Twin-2K-500/resolve/main/question_catalog_and_human_response_csv/wave4_response_label.csv",
    # NVIDIA Nemotron-Personas-Singapore (first of two shards, 74k records).
    "nemotron/Nemotron-Personas-Singapore-train-00000-of-00002.parquet": "https://huggingface.co/datasets/nvidia/Nemotron-Personas-Singapore/resolve/main/data/train-00000-of-00002.parquet",
}


def main() -> int:
    for rel, url in FILES.items():
        dest = RAW / rel
        dest.parent.mkdir(parents=True, exist_ok=True)
        if dest.exists():
            print(f"skip (exists) {rel}")
            continue
        print(f"download {rel}")
        urllib.request.urlretrieve(url, dest)
        if dest.suffix == ".zip":
            with zipfile.ZipFile(dest) as z:
                for m in z.namelist():
                    if m.lower().endswith(".dta"):
                        z.extract(m, dest.parent)
                        (dest.parent / m).rename(dest.parent / Path(m).name)
    print("done")
    return 0


if __name__ == "__main__":
    sys.exit(main())
