import numpy as np
import pandas as pd

from digital_citizens.library import crosswalk_us as X
from digital_citizens.library import harmonise as HM
from digital_citizens.library.search import match_questions, strip_shared_stems


def test_crosswalk_shapes():
    seen = set()
    for p in X.PAIRS:
        assert p["wvs"] not in seen, "duplicate wvs item"
        seen.add(p["wvs"])
        assert len(p["bins"]) == len(p["wvs_map"]) == len(p["gss_map"]) >= 2
        assert p["quality"] in {"exact", "close", "loose"}
        for m in (p["wvs_map"], p["gss_map"]):
            flat = [i for idx in m for i in idx]
            assert len(flat) == len(set(flat)), "an option mapped to two bins"


def test_collapse_and_relevel():
    assert np.allclose(HM.collapse([0.1, 0.2, 0.3, 0.4], [[0, 1], [2, 3]]), [0.3, 0.7])
    assert np.allclose(HM.collapse([0.5, 0.5, 0.0], [[0], [1]]), [0.5, 0.5])  # dropped option renormalised
    spread = {("q", "ALL"): [0.5, 0.5], ("q", "g=a"): [0.7, 0.3]}
    level = {("q", "ALL"): [0.2, 0.8]}
    out = HM.relevel(spread, level, ["ALL", "g=a"])
    assert np.allclose(out[("q", "g=a")], [0.4, 0.6])
    assert np.allclose(out[("q", "ALL")], [0.2, 0.8])


def test_weighted_bins_and_groups():
    df = pd.DataFrame({"a": ["x", "y", "z", None, "x"], "w": [1, 1, 2, 1, 1], "sex": ["Male", "Female", "Male", "Male", "NA"]})
    probs, n = HM.weighted_bins(df["a"], df["w"], ["x", "y", "z"], [[0], [1, 2]])
    assert n == 4 and np.allclose(probs, [2 / 5, 3 / 5])
    assert HM.groups_of(df, ["sex"], min_n=2) == ["ALL", "sex=Male"]


def test_harmonise_region_and_age():
    assert HM._region4_from_state("US: CA California") == "West"
    assert HM._region4_from_state("US: TX Texas") == "South"
    assert HM.age_band4(29) == "18-29" and HM.age_band4(60) == "60+" and HM.age_band4(float("nan")) == "NA"


def test_tfidf_matcher_and_stem_stripping():
    lib = {"a": "how often do you attend religious services", "b": "do you favor or oppose the death penalty"}
    q = {"x": "about how often do you attend religious services these days", "y": "is the death penalty ever justified"}
    m = match_questions(q, lib, top=1)
    assert m["x"][0][0] == "a" and m["y"][0][0] == "b"
    stripped = strip_shared_stems({"1": "confidence in the press", "2": "confidence in the army", "3": "confidence in banks"}, max_share=0.5)
    assert stripped["1"] == "press" and stripped["3"] == "banks"
