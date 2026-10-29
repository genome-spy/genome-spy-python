"""Small profile inputs shared by semantic and browser tests."""

from __future__ import annotations

import numpy as np
import pandas as pd
from anndata import AnnData


def timeseries_cases():
    """Return detached profiles/options with unsorted times, missing values and guides."""
    values = np.array([[0.5, 5], [1, 4], [4, 1], [7, -2]], dtype=float)
    time = np.array([3.0, 1.0, 1.0, -2.0])
    return {
        "multiple": (values, {"time": time, "var_names": ["A", "B"]}),
        "highlights": (
            values,
            {
                "time": time,
                "highlights_x": [-6.0, 8.0],
                "yticks": [-10.0, 10.0],
                "xlabel": "Time",
                "ylabel": "Supplied value",
            },
        ),
        "limits": (
            values,
            {
                "xlim": [4.0, -1.0],
                "highlights_x": [-6.0, 8.0],
                "marker": "o",
                "palette": ["red", "blue"],
            },
        ),
        "categorical": (
            values[:, 0],
            {
                "time": time,
                "color": np.array(["b", "a", "b", "a"]),
                "var_names": ["first", "second"],
                "marker": "s",
            },
        ),
        "integer_groups": (
            values[:, 0],
            {"color": np.array([2, 1, 2, 1]), "var_names": ["one", "two"]},
        ),
        "mixed_integer_first": (
            values[:, 0],
            {"color": [2, 1.0, 2.0, 1], "var_names": ["one", "two"]},
        ),
        "continuous": (
            values[:, 0],
            {
                "time": time,
                "color": np.array([0.1, 0.8, 0.5, 0.3]),
                "var_names": ["value"],
                "marker": "o",
            },
        ),
        "missing": (
            np.array([0.5, np.nan, 4.0, 7.0]),
            {"time": time, "color": np.array([0.1, 0.8, np.nan, 0.3])},
        ),
        "masked_legend_key": (
            np.array([np.nan, 1.0, 4.0, 7.0]),
            {"color": np.array([0.1, 0.8, 0.5, 0.3]), "var_names": ["masked first"]},
        ),
        "constant": (
            values[:, 0],
            {"color": np.full(4, 0.4), "var_names": ["constant"], "marker": "D"},
        ),
        "singleton": (
            np.array([[2.0, 3.0]]),
            {"time": np.array([4.0]), "var_names": ["A", "B"]},
        ),
    }


def make_sim():
    """Return seven samples and two named profiles, with three samples per run."""
    return AnnData(
        np.array([[1, 8], [2, 6], [4, 3], [7, 2], [5, 4], [3, 5], [2, 7]], dtype=float),
        obs=pd.DataFrame(index=[f"sample-{i}" for i in range(7)]),
        var=pd.DataFrame(index=["A", "B"]),
        uns={"tmax_write": 3.0},
    )


def sim_cases():
    """Cover precedence, partial runs, numeric ticks and the shuffled point branch."""
    return {
        "points": {},
        "heatmap": {"as_heatmap": True},
        "override": {"tmax_realization": 4},
        "fractional": {"as_heatmap": True, "tmax_realization": 2.5},
        "long": {"tmax_realization": 20},
        "shuffle": {"shuffle": True, "marker": "o"},
        "shuffle_heatmap": {"shuffle": True, "as_heatmap": True},
    }


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
