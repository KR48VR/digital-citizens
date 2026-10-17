import numpy as np

from digital_citizens.evaluate import calibrate as C


def _dists():
    # two questions, population + 3 groups; simulated gaps are exactly half the real gaps
    real = {("q1", "ALL"): [0.5, 0.5], ("q1", "a"): [0.7, 0.3], ("q1", "b"): [0.3, 0.7], ("q1", "c"): [0.6, 0.4],
            ("q2", "ALL"): [0.2, 0.8], ("q2", "a"): [0.4, 0.6], ("q2", "b"): [0.1, 0.9], ("q2", "c"): [0.2, 0.8]}
    pred = {}
    for (q, g), p in real.items():
        pop = np.array(real[(q, "ALL")])
        pred[(q, g)] = (pop + 0.5 * (np.array(p) - pop)).tolist()
    return real, pred


def test_gap_scale_recovers_known_factor_and_applies():
    real, pred = _dists()
    a = C.fit_gap_scale(pred, real, ["q1", "q2"], ["ALL", "a", "b", "c"])
    assert abs(a - 2.0) < 1e-9
    fixed = C.apply_gap_scale(pred, a, ["q1"], ["ALL", "a", "b", "c"])
    assert np.allclose(fixed[("q1", "a")], real[("q1", "a")])
    anchored = C.apply_gap_scale(pred, a, ["q2"], ["ALL", "a"], base=real)
    assert np.allclose(anchored[("q2", "ALL")], real[("q2", "ALL")])


def test_power_calibration_prefers_identity_when_already_right():
    real, _ = _dists()
    t = C.fit_power(real, real, list(real))
    assert abs(t - 1.0) < 1e-9
    softened = C.apply_power({("q", "g"): [0.9, 0.1]}, 0.5)[("q", "g")]
    assert softened[0] < 0.9 and abs(sum(softened) - 1) < 1e-9
