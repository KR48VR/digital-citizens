import numpy as np
import pandas as pd

from digital_citizens.population.synth import ipf, margin_error, margins, rake, sample_population


def test_ipf_matches_margins():
    seed = np.ones((3, 2))
    out = ipf(seed, [np.array([50, 30, 20]), np.array([60, 40])])
    assert np.allclose(out.sum(axis=1), [50, 30, 20])
    assert np.allclose(out.sum(axis=0), [60, 40])


def test_rake_hits_targets_and_sampling_preserves_them():
    rng = np.random.default_rng(0)
    df = pd.DataFrame({"sex": rng.choice(["F", "M"], 2000, p=[0.7, 0.3]), "age": rng.choice(["young", "old"], 2000, p=[0.8, 0.2])})
    targets = {"sex": {"F": 0.5, "M": 0.5}, "age": {"young": 0.4, "old": 0.6}}
    w = rake(df, targets)
    err = margin_error(df, targets, w)
    assert max(err.values()) < 1e-4
    samp = sample_population(df, 20000, w, seed=1)
    assert abs(margins(samp, "sex")["F"] - 0.5) < 0.02
    assert abs(margins(samp, "age")["old"] - 0.6) < 0.02
