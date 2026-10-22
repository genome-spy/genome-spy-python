"""Stored DPT metadata/profiles with distinct rank, row-index and category orders."""

import numpy as np
import pandas as pd
from anndata import AnnData
from tests.integrations.scanpy.sim_fixture import make_sim


def make_dpt(case="default"):
    """Return stored DPT metadata, optionally filtered without renumbering ranks."""
    adata = AnnData(
        np.zeros((8, 2)),
        obs=pd.DataFrame(
            {
                "dpt_groups": pd.Categorical(
                    ["beta", "alpha"] * 4, categories=["beta", "unused", "alpha"]
                ),
                "dpt_order": [4, 0, 6, 2, 7, 1, 5, 3],
                "dpt_pseudotime": np.array(
                    [0, 0.2, 0.4, 0.6, 0.8, 1, 0.5, 0.3], dtype=float
                ),
            },
            index=[f"cell-{i}" for i in range(8)],
        ),
        uns={"dpt_changepoints": np.array([3, 6])},
    )
    if case == "many_groups":
        adata.obs["dpt_groups"] = pd.Categorical(
            ["a", "b", "c", "d", "e", "f", "a", "b"]
        )
    elif case == "missing":
        adata.obs["dpt_pseudotime"] = [np.inf, 0.2, np.nan, 0.6, 0.8, 1, -np.inf, 0.3]
    elif case == "integer_time":
        adata.obs["dpt_pseudotime"] = np.arange(8) % 2
    elif case == "single_group":
        adata.obs["dpt_groups"] = pd.Categorical(["only"] * 8)
        adata.uns["dpt_changepoints"] = np.array([], dtype=int)
    elif case == "filtered_view":
        return adata[[6, 1, 4, 3]]
    return adata


def dpt_cases():
    """Cover categorical ticks, colors, masked times, markers and filtered ranks."""
    return {
        "default": {},
        "many_groups": {"marker": "o"},
        "missing": {"marker": "o"},
        "integer_time": {},
        "single_group": {},
        "filtered_view": {},
        "custom_colors": {
            "palette": ["red", "blue"],
            "color_map": "plasma",
            "marker": "s",
        },
    }


def dpt_reference(adata, *, color_map=None, palette=None, marker="."):
    """Render Scanpy's two public component calls; its parent entry fails on pandas Series indexing."""
    import matplotlib.pyplot as plt
    import scanpy as sc

    fig, (group_ax, time_ax) = plt.subplots(2, 1)
    groups = adata.obs["dpt_groups"]
    sc.pl.timeseries_subplot(
        groups.cat.codes.to_numpy(),
        time=adata.obs["dpt_order"].to_numpy(),
        color=np.asarray(groups),
        highlights_x=adata.uns["dpt_changepoints"],
        ylabel="dpt groups",
        yticks=np.arange(len(groups.cat.categories))
        if len(groups.cat.categories) < 5
        else None,
        palette=palette,
        ax=group_ax,
        marker=marker,
    )
    sc.pl.timeseries_subplot(
        adata.obs["dpt_pseudotime"].to_numpy(),
        time=adata.obs["dpt_order"].to_numpy(),
        color=adata.obs["dpt_pseudotime"].to_numpy(),
        highlights_x=adata.uns["dpt_changepoints"],
        xlabel="dpt order",
        ylabel="pseudotime",
        yticks=[0, 1],
        color_map=color_map,
        ax=time_ax,
        marker=marker,
    )
    return fig


def make_dpt_profiles(case="heatmap"):
    """Return two nonconstant genes with a saved, non-self-inverse DPT ordering."""
    adata = make_sim()
    adata.obs["dpt_order_indices"] = [4, 0, 6, 2, 5, 1, 3]
    adata.uns["dpt_changepoints"] = [2, 5]
    if case == "repeated_indices":
        adata.obs["dpt_order_indices"] = [4, 0, 4, -1, 2, 2, 3]
    elif case == "single_gene":
        adata = adata[:, :1]
    elif case == "single_sample":
        adata = adata[:1].copy()
        adata.obs["dpt_order_indices"] = [0]
        adata.uns["dpt_changepoints"] = []
    return adata


def dpt_profile_cases():
    """Cover both renderers, inactive options, native schemes and NumPy row indexing."""
    return {
        "heatmap": {},
        "points": {"as_heatmap": False, "marker": "o"},
        "plasma": {"color_map": "plasma", "marker": "unused"},
        "point_inactive_color": {"as_heatmap": False, "color_map": "unused"},
        "repeated_indices": {},
        "single_gene": {},
        "single_sample": {},
    }
