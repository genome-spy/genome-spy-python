"""Stored groups and shuffled pseudotime for direct PAGA path references."""

import numpy as np
import pandas as pd
from anndata import AnnData
from scipy import sparse


def make_path(storage="dense", case="default"):
    """Return asymmetric raw/X profiles, with category order distinct from path and cell order."""
    values = np.array(
        [[2, 9, 3], [6, 1, 5], [4, 7, 2], [8, 2, 1], [3, 8, 6], [7, 4, 9]], dtype=float
    )
    a = AnnData(
        values,
        obs=pd.DataFrame(
            {
                "cluster": pd.Categorical(
                    ["beta", "alpha", "gamma", "beta", "alpha", "gamma"],
                    categories=["gamma", "unused", "beta", "alpha"],
                ),
                "dpt_pseudotime": [0.7, 0.4, 0.9, 0.1, 0.2, 0.5],
                "score": [10.0, 20.0, 15.0, 5.0, 0.0, 25.0],
            },
            index=[f"cell-{i}" for i in range(6)],
        ),
        var=pd.DataFrame(index=["g1", "g2", "g3"]),
        uns={
            "paga": {"groups": "cluster"},
            "cluster_colors": ["red", "gray", "blue", "green"],
        },
    )
    if case == "missing":
        a.X[0, 0] = np.nan
    if storage != "dense":
        a.X = getattr(sparse, storage + "_matrix")(a.X)
    if case != "raw_fallback":
        a.raw = a
        a.X = a.X * 3
    if case == "filtered":
        return a[[0, 1, 3, 4]]
    return a


def path_cases():
    """Cover path names/indices/repeats, window order, raw access and annotations."""
    return {
        "default": {},
        "smoothed": {"n_avg": 3},
        "normalized": {"n_avg": 2, "normalize_to_zero_one": True},
        "indices": {"nodes": [2, 3]},
        "repeated": {"nodes": ["beta", "alpha", "beta"]},
        "x": {"use_raw": False},
        "raw_fallback": {},
        "filtered": {"nodes": ["alpha", "beta"]},
        "no_annotations": {"annotations": ()},
        "annotation": {"annotations": ("score",)},
        "obs_key": {"keys": ["g1", "score"], "n_avg": 2},
        "missing": {},
        "missing_smoothed": {"n_avg": 2},
        "labels_off": {
            "show_node_names": False,
            "show_yticks": False,
            "show_colorbar": False,
        },
        "custom": {
            "color_map": "plasma",
            "color_maps_annotations": {"dpt_pseudotime": "Blues"},
            "palette_groups": ["orange", "gray", "purple", "cyan"],
            "title": "Stored path",
            "ytick_fontsize": 12,
            "title_fontsize": 14,
        },
        "inactive": {
            "xlim": (1, 3),
            "legend_fontsize": "large",
            "legend_fontweight": "bold",
        },
    }
