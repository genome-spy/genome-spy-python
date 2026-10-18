"""Original group profiles and tree cases; no upstream dataset copies."""

from typing import Any


def make_tree_adata(case: str = "default") -> Any:
    import anndata as ad
    import numpy as np
    import pandas as pd

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
