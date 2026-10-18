"""Original cell-level heatmap cases with unequal groups and repeated names."""

from typing import Any

from tests.integrations.scanpy.dendrogram_fixture import make_tree_adata


def make_heatmap_adata(case: str = "default") -> Any:
    import numpy as np
    import pandas as pd

    adata = make_tree_adata()[[0, 1, 2, 3, 0, 2, 2, 0, 3]].copy()
    adata.obs_names = ["same", "a", "b", "c", "same", "d", "e", "f", "g"]
    adata.obs["numeric"] = np.arange(9)
    adata.X[:, 0] += np.arange(9) / 20
    adata.var["symbol"] = ["ONE", "TWO", "THREE", "FOUR"]
    adata.uns["group_colors"] = ["#e41a1c", "#377eb8", "#4daf4a", "#984ea3"]
    if case == "missing":
        adata.X[0, 0] = np.nan
    if case == "constant":
        adata.X[:] = 4
    if case == "one_group":
        adata.obs["group"] = pd.Categorical(["C"] * 9)
    return adata


def heatmap_cases() -> dict[str, dict[str, Any]]:
    markers = {"first": ["g2", "g1"], "again": ["g2"]}
    matched = {"C": ["g1"], "A": ["g2"], "D": ["g3"], "B": ["g4", "g1"]}
    return {
        "default": {},
        "log": {"log": True},
        "scaled_var": {"standard_scale": "var"},
        "scaled_obs": {"standard_scale": "obs"},
        "swapped": {"swap_axes": True},
        "markers": {"var_names": markers},
        "swapped_markers": {"var_names": markers, "swap_axes": True},
        "tree": {"dendrogram": True},
        "swapped_tree": {"dendrogram": True, "swap_axes": True},
        "matched_blocks": {"var_names": matched, "dendrogram": True},
        "missing": {},
        "constant": {},
        "one_group": {},
        "hidden_labels": {"show_gene_labels": False},
        "numeric_bins": {"groupby": "numeric", "num_categories": 3},
        "multi_key": {"groupby": ["group", "batch"]},
    }
