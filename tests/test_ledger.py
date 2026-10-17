import numpy as np
import pandas as pd

from digital_citizens.data import ledger as L


def _row(**kw):
    base = dict(ledger_id="t1", country="Singapore", source_org="X", title="T", year="2024", url="", fieldwork="", population="", n=1000, sampling="probability", question_text="q", options="worried|not worried", group="ethnic=Malay", shares="60|40", maps_to="Q142", option_map="0+1|2+3", confidence=1.0, notes="")
    base.update(kw)
    return pd.Series(base)


def test_pseudocounts_respect_shares_and_reference_split():
    counts = L.to_pseudocounts(_row(), k=4, reference=np.array([0.3, 0.1, 0.4, 0.2]))
    assert abs(counts.sum() - 1000) < 1e-9
    assert abs(counts[:2].sum() - 600) < 1e-9 and abs(counts[2:].sum() - 400) < 1e-9
    assert abs(counts[0] / counts[1] - 3.0) < 1e-9  # split within the block follows the reference 0.3:0.1


def test_confidence_scales_evidence_and_missing_dk_leaves_mass_out():
    counts = L.to_pseudocounts(_row(confidence=0.5, shares="50|30"), k=4)
    assert abs(counts.sum() - 400) < 1e-9  # 1000 * 0.5 * 80%


def test_mean_rows_discretise_and_reverse():
    r = _row(shares="mean=3.5;sd=0.8", option_map="identity")
    c = L.to_pseudocounts(r, k=4)
    assert c.argmax() in (2, 3) and abs(c.sum() - 1000) < 1e-9
    rr = L.to_pseudocounts(_row(shares="mean=3.5;sd=0.8", option_map="reverse"), k=4)
    assert rr.argmax() in (0, 1)
