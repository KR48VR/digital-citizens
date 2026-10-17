"""Level-3 (individual) evaluation on Twin-2K-500 under a leakage-free protocol.

For each retest item: predict each person's wave-4 answer WITHOUT seeing their earlier answer to that
same item. Baselines: population modal answer, demographic-cell modal answer, k-NN on the other items.
Ceiling: the person's own wave 1-3 answer (test-retest). A digital twin should sit between the k-NN
floor and the retest ceiling; its score is reported as normalized accuracy = acc / retest_acc.
"""
from __future__ import annotations

import numpy as np
import pandas as pd

from ..data import twin2k
from . import baselines as B
from . import metrics as M


def evaluate_twin2k(k: int = 25, max_items: int | None = None, seed: int = 0, test_frac: float = 0.3, demo_cells: tuple[str, ...] = ("sex", "age", "education", "politics")) -> pd.DataFrame:
    w13, w4 = twin2k.load_responses()
    items = twin2k.retest_items(w13, w4)
    if max_items:
        items = items[:max_items]
    demo = twin2k.demographic_table(w13).set_index("pid")
    cat_cols = [c for c in twin2k.categorical_columns(w13) if c not in demo.columns]
    rng = np.random.default_rng(seed)
    pids = w13["pid"].to_numpy()
    test_mask = rng.random(len(pids)) < test_frac
    X = w13.set_index("pid")[cat_cols]
    rows = []
    for it in items:
        y4 = w4.set_index("pid")[it]
        y13 = w13.set_index("pid")[it]
        valid = y4.notna()
        test_ids = pids[test_mask & valid.loc[pids].to_numpy()]
        train_ids = pids[~test_mask & valid.loc[pids].to_numpy()]
        if len(test_ids) < 50 or len(train_ids) < 100:
            continue
        truth = y4.loc[test_ids].astype(str)
        # ceiling: the person's own earlier answer
        retest = float((y13.loc[test_ids].astype(str) == truth).mean())
        # floor 1: population modal answer (from training people's wave-4 answers)
        modal = B.modal_answer(y4.loc[train_ids])
        modal_acc = float((truth == str(modal)).mean())
        # floor 2: demographic-cell modal
        tr = demo.loc[train_ids].copy()
        tr[it] = y4.loc[train_ids].astype(str)
        te = demo.loc[test_ids].copy()
        cells = [c for c in demo_cells if c in demo.columns]
        demo_pred = B.demographic_cell_modal(tr, te, it, cells)
        demo_acc = float((demo_pred.astype(str).to_numpy() == truth.to_numpy()).mean())
        # floor 3: k-NN on the other items (target item's own earlier answer excluded)
        other = [c for c in cat_cols if c != it]
        knn_pred = B.knn_predict(X.loc[train_ids, other], y4.loc[train_ids], X.loc[test_ids, other], k=k)
        knn_acc = float((knn_pred.astype(str).to_numpy() == truth.to_numpy()).mean())
        rows.append({
            "item": it, "n_test": len(test_ids), "n_levels": int(y4.nunique()),
            "retest_ceiling": retest, "modal_acc": modal_acc, "demo_cell_acc": demo_acc, "knn_acc": knn_acc,
            "knn_normalized": M.normalized_accuracy(knn_acc, retest),
        })
    return pd.DataFrame(rows)
