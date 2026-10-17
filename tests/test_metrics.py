import math

import numpy as np

from digital_citizens.evaluate import metrics as M


def test_jsd_bounds():
    assert M.jsd([1, 0], [1, 0]) == 0.0
    assert abs(M.jsd([1, 0], [0, 1]) - 1.0) < 1e-9
    assert 0 < M.jsd([0.6, 0.4], [0.4, 0.6]) < 1


def test_total_variation_and_wasserstein():
    assert abs(M.total_variation([0.5, 0.5], [1, 0]) - 0.5) < 1e-9
    assert abs(M.wasserstein_ordinal([1, 0, 0], [0, 0, 1]) - 2.0) < 1e-9
    assert abs(M.representativeness([1, 0, 0], [0, 0, 1]) - 0.0) < 1e-9
    assert abs(M.representativeness([0.2, 0.3, 0.5], [0.2, 0.3, 0.5]) - 1.0) < 1e-9


def test_entropy_ratio_detects_flattening_and_sharpening():
    real = [0.25, 0.25, 0.25, 0.25]
    assert M.entropy_ratio([0.7, 0.1, 0.1, 0.1], real) < 1
    assert abs(M.entropy_ratio(real, real) - 1) < 1e-9


def test_dispersion_ratio():
    real = [0.2, 0.4, 0.6, 0.8]
    assert abs(M.dispersion_ratio(real, real) - 1.0) < 1e-9
    assert M.dispersion_ratio(real, [0.5, 0.5, 0.5, 0.5]) == 0.0  # fully flattened
    assert M.dispersion_ratio(real, [0.1, 0.4, 0.6, 0.9]) > 1.0  # exaggerated
    assert math.isnan(M.dispersion_ratio([0.5, 0.5], [0.1, 0.9]))


def test_gap_recovery_slope():
    pop = [0.5, 0.5]
    real = {"a": [0.7, 0.3], "b": [0.3, 0.7], "c": [0.6, 0.4]}
    flat = {g: [0.55, 0.45] if g == "a" else [0.45, 0.55] if g == "b" else [0.53, 0.47] for g in real}
    out = M.gap_recovery(pop, real, pop, flat)
    assert out["r"] > 0.95 and 0 < out["slope"] < 0.5
    same = M.gap_recovery(pop, real, pop, real)
    assert abs(same["slope"] - 1) < 1e-9


def test_noise_floor_shrinks_with_n():
    p = [0.3, 0.3, 0.4]
    assert M.noise_floor_jsd(p, 50) > M.noise_floor_jsd(p, 5000)


def test_sign_agreement_and_normalized_accuracy():
    assert M.sign_agreement([1, -1, 2, 0], [0.5, -2, -1, 3]) == 2 / 3
    assert abs(M.normalized_accuracy(0.68, 0.8) - 0.85) < 1e-9
    assert math.isnan(M.normalized_accuracy(0.5, 0))
