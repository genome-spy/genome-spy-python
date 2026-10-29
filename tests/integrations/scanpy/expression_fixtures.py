"""Small expression inputs shared by semantic and browser tests."""

from __future__ import annotations

from typing import Any

import numpy as np
import pandas as pd
from anndata import AnnData


def make_grouped_adata() -> Any:
    import anndata as ad

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


def dotplot_cases() -> dict[str, dict[str, Any]]:
    cases = {
        "default": {},
        "reordered": {"categories_order": ["A", "B"]},
        "log": {"log": True, "expression_cutoff": 0.8},
        "expressed": {"mean_only_expressed": True, "expression_cutoff": 1},
        "scaled": {"standard_scale": "var"},
        "swapped_scaled": {"swap_axes": True, "standard_scale": "group"},
        "supplied": {
            "dot_color_df": pd.DataFrame(
                [[4, 8, 2], [8, 2, 6]], index=["A", "B"], columns=["g3", "g1", "g2"]
            )
        },
        "supplied_scaled": {
            "standard_scale": "var",
            "dot_color_df": pd.DataFrame(
                [[4, 8, 2], [8, 2, 6]], index=["A", "B"], columns=["g3", "g1", "g2"]
            ),
        },
        "clipped": {"dot_min": 0.4, "dot_max": 0.8, "smallest_dot": 10},
        "repeated": {"var_names": {"first": ["g2", "g1"], "again": "g2"}},
        "constant_colors": {
            "dot_color_df": pd.DataFrame(
                4.0, index=["B", "A"], columns=["g1", "g2", "g3"]
            )
        },
    }
    # Viridis shares a published palette; native reds uses different Vega stops.
    return {name: {"cmap": "viridis", **options} for name, options in cases.items()}


def matrixplot_cases() -> dict[str, dict[str, Any]]:
    supplied = pd.DataFrame(
        [[4, 8, 2], [8, 2, 6]], index=["A", "B"], columns=["g3", "g1", "g2"]
    )
    return {
        "default": {},
        "reordered": {"categories_order": ["A", "B"]},
        "log": {"log": True},
        "scaled_var": {"standard_scale": "var"},
        "scaled_group": {"standard_scale": "group"},
        "swapped_scaled": {"swap_axes": True, "standard_scale": "var"},
        "supplied": {"values_df": supplied},
        "supplied_scaled": {
            "values_df": supplied,
            "standard_scale": "var",
            "log": True,
        },
        "supplied_reordered": {
            "values_df": supplied,
            "categories_order": ["B", "A"],
            "swap_axes": True,
        },
        "repeated": {"var_names": {"first": ["g2", "g1"], "again": "g2"}},
        "constant": {
            "values_df": pd.DataFrame(4.0, index=["B", "A"], columns=["g1", "g2", "g3"])
        },
        "missing": {"values_df": supplied.mask(supplied == 8)},
        "bounds_edges": {
            "vmin": 1,
            "vmax": 3,
            "edgecolor": "black",
            "linewidth": 1.5,
        },
    }


def make_heatmap_adata(case: str = "default") -> Any:
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


def matrix_cases():
    base = np.array([[-2.0, 0, 2], [1, 3, 5]])
    labels = {
        "xticks": ["gene A", "B", "B"],
        "yticks": ["group 2", "group 1"],
        "xlabel": "Genes",
        "ylabel": "Groups",
        "title": "Supplied values",
    }
    return {
        "default": (base, {}),
        "labels": (base, labels),
        "constant": (np.full((2, 3), 7.0), labels),
        "zero": (np.zeros((2, 3)), {}),
        "missing": (np.array([[np.nan, 0, 2], [1, 3, 5]]), labels),
        "masked": (np.ma.array(base, mask=[[0, 1, 0], [1, 0, 0]]), labels),
        "row": (base[:1], {"colorbar_shrink": 0.8}),
        "column": (base[:, :1], {"colorbar_shrink": 0.25}),
    }


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


def make_tree_adata(case: str = "default") -> Any:
    import anndata as ad

    profiles = np.array(
        [[0, 1, 4, 2], [1, 0, 4, 2], [4, 2, 0, 1], [2, 4, 1, 0]], dtype=float
    )
    if case == "ties":
        profiles[1] = profiles[0]
    if case == "identical":
        profiles[:] = profiles[0]
    obs = pd.DataFrame(
        {
            "group": pd.Categorical(
                ["C", "A", "D", "B"] * 2, categories=["C", "A", "D", "B"]
            ),
            "batch": pd.Categorical(["z"] * 4 + ["y"] * 4, categories=["z", "y"]),
        },
        index=[f"cell{i}" for i in range(8)],
    )
    if case == "missing_group":
        obs.loc["cell7", "group"] = None
    a = ad.AnnData(np.tile(profiles, (2, 1)), obs=obs)
    a.var_names = ["g1", "g2", "g3", "g4"]
    a.obsm["custom"] = np.log1p(a.X * [1, 3, 2, 5])
    if case == "pca":
        a = ad.AnnData(np.pad(a.X, ((0, 0), (0, 60))), obs=obs.copy())
        a.var_names = [f"g{i + 1}" for i in range(64)]
        a.obsm["X_pca"] = np.tile(profiles, (2, 1))
    return a


def tree_cases() -> dict[str, dict[str, Any]]:
    return {
        "default": {},
        "missing_group": {},
        "multi": {"groupby": ["group", "batch"]},
        "pca": {},
        "custom": {
            "use_rep": "custom",
            "cor_method": "spearman",
            "linkage_method": "average",
        },
        "optimal": {"optimal_ordering": True},
        "ties": {},
        "identical": {},
    }


def tree_plot_cases() -> dict[str, tuple[str, dict[str, Any]]]:
    markers = {"first": ["g2", "g1"], "rest": ["g3", "g4"]}
    matched = {"C": ["g1", "g2"], "A": ["g2"], "D": ["g3"], "B": ["g4", "g1"]}
    return {
        **{
            f"standalone_{side}": ("dendrogram", {"orientation": side})
            for side in ("top", "bottom", "left", "right")
        },
        "dotplot": (
            "dotplot",
            {"var_names": markers, "dendrogram": True, "cmap": "viridis"},
        ),
        "dotplot_swapped": (
            "dotplot",
            {
                "var_names": markers,
                "dendrogram": True,
                "swap_axes": True,
                "cmap": "viridis",
            },
        ),
        "matrixplot": ("matrixplot", {"var_names": markers, "dendrogram": True}),
        "matrixplot_swapped": (
            "matrixplot",
            {"var_names": markers, "dendrogram": True, "swap_axes": True},
        ),
        "marker_blocks": (
            "matrixplot",
            {"var_names": matched, "dendrogram": True, "standard_scale": "var"},
        ),
        "correlation": ("correlation_matrix", {"cmap": "viridis"}),
        "correlation_no_tree": (
            "correlation_matrix",
            {"dendrogram": False, "cmap": "viridis"},
        ),
        "correlation_numbers": (
            "correlation_matrix",
            {"show_correlation_numbers": True, "cmap": "viridis"},
        ),
    }
