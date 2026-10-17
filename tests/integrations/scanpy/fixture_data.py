"""Original synthetic fixtures shared by tests and explicit oracle generation."""

from __future__ import annotations

from typing import Any


def make_adata() -> Any:
    import anndata as ad
    import numpy as np
    import pandas as pd

    obs = pd.DataFrame(
        {
            "cell_type": pd.Categorical(
                ["B", "A", None, "B", "C", "A", "B", "C"],
                categories=["C", "B", "A", "unused"],
                ordered=True,
            ),
            "score": np.array([0, 1, np.nan, 1, 4, -1, 0, 2], dtype=np.float32),
            "cell_id": [f"stable-{i}" for i in range(8)],
            "keep": [True, False, True, True, False, True, True, False],
        },
        index=["duplicate", "c1", "duplicate", "c3", "c4", "c5", "c6", "c7"],
    )
    matrix = np.array([[i, i % 3, -i] for i in range(8)], dtype=np.float32)
    a = ad.AnnData(
        matrix,
        obs=obs,
        var=pd.DataFrame({"symbol": ["G2", "G1", "J"]}, index=["g2", "g1", "junk"]),
    )
    a.raw = ad.AnnData(
        np.array([[i % 4, i + 20, i * 2, -i] for i in range(8)], dtype=np.float32),
        obs=obs.copy(),
        var=pd.DataFrame(
            {"symbol": ["RAW_G1", "RAW_ONLY", "G2", "J"]},
            index=["g1", "raw_only", "g2", "junk"],
        ),
    )
    a.layers["counts"] = matrix * 10
    a.obsm["X_umap"] = np.array(
        [
            [-2, -1, 0],
            [1, 0, 1],
            [-2, -1, 2],
            [2, 1, 3],
            [0, 3, 4],
            [-1, 2, 5],
            [0.5, -2, 6],
            [1.5, 2, 7],
        ],
        dtype=np.float32,
    )
    a.uns["cell_type_colors"] = ["#ff0000", "#00aa00", "#0000ff", "#888888"]
    return a


def reference_cases() -> dict[str, dict[str, Any]]:
    return {
        "categorical": {"color": "cell_type", "frameon": True},
        "continuous": {
            "color": "score",
            "vmin": "p10",
            "vmax": "p90",
            "frameon": False,
        },
        "raw": {"color": "g1", "frameon": True},
        "grid": {
            "color": [
                "g1",
                "g2",
                "raw_only",
                "score",
                "cell_type",
                "g1",
                "score",
                "g2",
            ],
            "frameon": False,
            "ncols": 4,
        },
    }
