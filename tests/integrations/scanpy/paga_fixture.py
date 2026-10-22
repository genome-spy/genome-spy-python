"""Small stored PAGA graphs with threshold ties, unequal sizes and saved positions."""

import numpy as np
import pandas as pd
from anndata import AnnData
from scipy.sparse import csr_matrix

POSITIONS = np.array([[0.0, 0.0], [1.3, 0.2], [0.7, 1.4], [-0.4, 0.8]])


def make_paga(case="default"):
    """Return a metadata-only graph; a cached position intentionally differs from requested layouts."""
    categories = ["A", "B", "C", "D"]
    sizes = [9, 4, 1, 6]
    a = AnnData(
        obs=pd.DataFrame(
            {
                "cluster": pd.Categorical(
                    np.repeat(categories, sizes), categories=categories
                )
            },
            index=[f"cell-{i}" for i in range(sum(sizes))],
        ),
        uns={
            "paga": {
                "groups": "cluster",
                "connectivities": csr_matrix(
                    [
                        [0, 0.009, 0.01, 0],
                        [0.009, 0, 0.5, 0.2],
                        [0.01, 0.5, 0, 0.05],
                        [0, 0.2, 0.05, 0],
                    ]
                ),
                "weak": csr_matrix(
                    [[0, 0.6, 0, 0.2], [0.6, 0, 0, 0], [0, 0, 0, 0.3], [0.2, 0, 0.3, 0]]
                ),
                "pos": POSITIONS + 99,
            },
            "cluster_colors": ["#e41a1c", "#377eb8", "#4daf4a", "#ff7f00"],
            "cluster_sizes": np.array(sizes),
        },
    )
    if case == "empty":
        a.uns["paga"]["connectivities"] = csr_matrix((4, 4))
    elif case in {"asymmetric", "asymmetric_csc"}:
        a.uns["paga"]["connectivities"][0, 1] = 0.7
        if case == "asymmetric_csc":
            a.uns["paga"]["connectivities"] = a.uns["paga"]["connectivities"].tocsc()
    elif case == "uniform_sizes":
        del a.uns["cluster_sizes"]
    return a


def paga_cases():
    """Cover computed/supplied layouts, threshold inclusion, aliases and edge/node scaling."""
    return {
        "default": {},
        "supplied": {"pos": POSITIONS},
        "all_edges": {"pos": POSITIONS, "threshold": 0},
        "boundary": {"pos": POSITIONS, "threshold": 0.01},
        "dashed": {
            "pos": POSITIONS,
            "dashed_edges": "weak",
            "min_edge_width": 0.6,
            "max_edge_width": 0.9,
        },
        "sizing": {
            "pos": POSITIONS,
            "node_size_scale": 2.0,
            "node_size_power": 1.0,
            "fontsize": 14,
            "fontweight": "normal",
            "frameon": False,
            "title": "Stored graph",
        },
        "aliases": {
            "pos": POSITIONS,
            "colors": ["red", "blue", "green", "orange"],
            "colorbar": False,
            "groups": ["one", "two", "three", "four"],
            "add_pos": False,
        },
        "circle": {"layout": "circle"},
        "initialized": {
            "init_pos": POSITIONS,
            "random_state": 17,
            "layout_kwds": {"niter": 100},
        },
        "empty": {"pos": POSITIONS},
        "asymmetric": {"pos": POSITIONS, "threshold": 0},
        "asymmetric_csc": {"pos": POSITIONS, "threshold": 0},
        "uniform_sizes": {"pos": POSITIONS, "color": "purple"},
        "zero_sizes": {"pos": POSITIONS, "node_size_scale": 0},
    }
