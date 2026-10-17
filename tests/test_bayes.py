import numpy as np

from digital_citizens.evaluate import bayes as Bz


def test_pool_weights_sources_and_counts():
    src = {"a": [0.9, 0.1], "b": [0.1, 0.9]}
    p = Bz.pool(src, {"a": 10, "b": 10})
    assert np.allclose(p, [0.5, 0.5])
    p = Bz.pool(src, {"a": 10, "b": 0}, counts=[0, 90])  # 90 real answers overwhelm a 10-respondent-worth prior
    assert p[1] > 0.85
    p = Bz.pool(src, {"a": 0, "b": 0})
    assert np.allclose(p, [0.5, 0.5])


def test_fit_alphas_prefers_the_accurate_source():
    rng = np.random.default_rng(0)
    cells = []
    for _ in range(40):
        real = rng.dirichlet([2, 2, 2])
        good = np.clip(real + rng.normal(0, 0.02, 3), 0.01, None)
        bad = rng.dirichlet([1, 1, 1])
        cells.append(({"good": good / good.sum(), "bad": bad}, real, None))
    al = Bz.fit_alphas(cells, ["good", "bad"])
    assert al["good"] > 5 * al["bad"]
