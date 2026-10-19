"""Original small cell/gene inputs for pinned clustermap references (MIT)."""

import numpy as np
import pandas as pd
from anndata import AnnData


def make_cluster_adata():
    return AnnData(
        np.array(
            [
                [1.0, 3, 7, 2],
                [8, 1, 2, 4],
                [1.1, 3.2, 7.3, 2.2],
                [7, 1.5, 3, 5],
                [4, 9, 1, 8],
                [4.5, 8, 1.3, 7],
            ]
        ),
        obs=pd.DataFrame(
            {
                "group": pd.Categorical(
                    ["B", "A", "B", "A", "C", "C"], categories=["C", "B", "A"]
                )
            },
            index=[f"cell-{i}" for i in range(6)],
        ),
        var=pd.DataFrame(index=["gene A", "gene B", "gene C", "gene D"]),
        uns={"group_colors": ["#009900", "#990000", "#000099"]},
    )


def clustermap_cases():
    return {
        "default": {},
        "row_annotation": {"obs_keys": "group"},
        "zscore_columns": {"z_score": 1},
        "scale_rows": {"standard_scale": 0},
        "columns_only": {
            "row_cluster": False,
            "metric": "cityblock",
            "method": "complete",
        },
        "no_clustering": {"row_cluster": False, "col_cluster": False},
        "masked": {"mask": np.eye(6, 4, dtype=bool)},
    }
