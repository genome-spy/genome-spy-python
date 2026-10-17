"""Original, hand-sized inputs for grouped plotting semantics."""

from __future__ import annotations

from typing import Any


def make_grouped_adata() -> Any:
    import anndata as ad
    import numpy as np
    import pandas as pd

    obs = pd.DataFrame(
        {
            "group": pd.Categorical(
                ["B", "A", "B", "A", None, "B"], categories=["B", "A"]
            ),
            "batch": pd.Categorical(
                ["x", "x", "y", "y", "x", "x"], categories=["y", "x"]
            ),
            "plain": ["10", "2", "10", "2", "10", "2"],
            "numeric": [0.0, 1.0, 2.0, 3.0, 4.0, 5.0],
            "score": [4.0, 1.0, 0.0, 2.0, 6.0, 8.0],
        },
        index=["same", "a", "same", "c", "d", "e"],
    )
    a = ad.AnnData(
        np.array(
            [[0, 1, 4], [1, 3, 4], [2, 0, 4], [0, 0, 4], [9, 9, 4], [np.nan, 2, 4]],
            dtype=float,
        ),
        obs=obs,
        var=pd.DataFrame({"symbol": ["ONE", "TWO", "CONST"]}, index=["g1", "g2", "g3"]),
    )
    a.layers["counts"] = a.X * 10
    a.raw = ad.AnnData(
        np.array([[10 * (i + 1), 3 + 2 * i, 5 + i] for i in range(6)], dtype=float),
        obs=obs.copy(),
        var=pd.DataFrame(
            {"symbol": ["TWO_RAW", "ONE_RAW", "RAW_ONLY"]},
            index=["g2", "g1", "raw_only"],
        ),
    )
    return a


def grouped_cases() -> dict[str, dict[str, Any]]:
    return {
        "default_raw": {"var_names": ["g1", "g2"]},
        "x": {"use_raw": False},
        "layer": {"var_names": ["g1", "g2"], "layer": "counts"},
        "raw_symbols": {"var_names": ["ONE_RAW", "RAW_ONLY"], "gene_symbols": "symbol"},
        "x_symbols": {
            "var_names": ["TWO", "ONE"],
            "gene_symbols": "symbol",
            "use_raw": False,
        },
        "numeric_bins": {"groupby": "numeric", "num_categories": 3, "use_raw": False},
        "natural_strings": {"groupby": "plain", "use_raw": False},
        "named_index": {"groupby": "barcode", "use_raw": False},
        "multiple_groups": {"groupby": ["group", "batch"], "use_raw": False},
        "reordered": {"categories_order": ["A", "B"], "use_raw": False},
        "repeated_slots": {
            "var_names": {"first": ["g2", "g1"], "again": "g2"},
            "use_raw": False,
        },
        "log_before_cutoff": {"log": True, "expression_cutoff": 1.5, "use_raw": False},
        "strict_cutoff": {"expression_cutoff": 1.0, "use_raw": False},
        "negative_cutoff": {"expression_cutoff": -0.5, "use_raw": False},
        "expressed_only": {
            "mean_only_expressed": True,
            "expression_cutoff": 1.0,
            "use_raw": False,
        },
        "scale_var": {"standard_scale": "var", "use_raw": False},
        "scale_group": {"standard_scale": "group", "use_raw": False},
    }
