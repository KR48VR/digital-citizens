"""Smoke tests on the real data files; skipped when data/raw is not populated (run scripts/download_data.py)."""
from pathlib import Path

import pytest

from digital_citizens.data import globalopinionqa, gss, nemotron, twin2k
from digital_citizens.evaluate import baselines as B
from digital_citizens.evaluate import harness as H

HAVE_GSS = Path("data/raw/gss/GSS2024.dta").exists() and Path("data/raw/gss/GSS2022.dta").exists()
HAVE_GOQA = globalopinionqa.DEFAULT_PATH.exists()
HAVE_TWIN = (twin2k.DIR / "wave4_response_label.csv").exists()
HAVE_SG = nemotron.SG_PATH.exists()


@pytest.mark.skipif(not HAVE_GSS, reason="GSS files not downloaded")
def test_gss_benchmark_shapes_and_baselines():
    b = gss.benchmark(2024, items=["happy", "cappun", "polviews"])
    assert {q.id for q in b.questions} == {"happy", "cappun", "polviews"}
    assert ("happy", "ALL") in b.real and abs(sum(b.real[("happy", "ALL")].probs) - 1) < 1e-9
    assert b.real[("happy", "ALL")].n > 3000
    assert ("cappun", "party3=Republican (incl. leaners)") in b.real
    prev = gss.benchmark(2022, items=["happy", "cappun", "polviews"])
    pred = B.previous_wave(b, prev)
    scored = H.score(pred, b, "prev")
    assert scored.jsd.median() < 0.01  # last wave is a strong predictor of this wave
    personas = gss.to_personas(b.respondents.head(5), ["happy", "cappun"])
    assert personas[0].country == "United States" and personas[0].record


@pytest.mark.skipif(not HAVE_GOQA, reason="GlobalOpinionQA parquet not downloaded")
def test_goqa_benchmark_has_target_countries():
    b = globalopinionqa.benchmark(["United States", "China", "Singapore"], min_countries=1)
    groups = b.groups()
    assert {"country=United States", "country=China", "country=Singapore"} <= set(groups)
    for d in list(b.real.values())[:50]:
        assert len(d.probs) == b.qmap[d.question_id].k
    lo = B.leave_one_group_out_mean(b)
    assert len(lo) > 100


@pytest.mark.skipif(not HAVE_TWIN, reason="Twin-2K-500 files not downloaded")
def test_twin2k_retest_items():
    w13, w4 = twin2k.load_responses()
    items = twin2k.retest_items(w13, w4)
    assert 50 < len(items) < 130
    acc = twin2k.test_retest_accuracy(w13, w4, items[:5])
    assert acc.between(0, 1).all()


@pytest.mark.skipif(not HAVE_SG, reason="Nemotron Singapore shard not downloaded")
def test_nemotron_personas():
    df = nemotron.load(columns=["uuid", "sex", "age", "marital_status", "education_level", "occupation", "industry", "planning_area", "persona", "cultural_background"]).head(20)
    ps = nemotron.to_personas(df)
    assert len(ps) == 20 and ps[0].attributes["planning_area"] and ps[0].narrative
    assert nemotron.infer_ethnicity("grew up in a Malay household in Bedok") == "Malay"
