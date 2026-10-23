"""Small stored PAGA graphs with threshold ties, unequal sizes and saved positions."""

import numpy as np
import pandas as pd
from anndata import AnnData
from scipy.sparse import csr_matrix

POSITIONS = np.array([[0.0, 0.0], [1.3, 0.2], [0.7, 1.4], [-0.4, 0.8]])


def make_paga(case="default"):
    """Return a stored graph; cached positions intentionally differ from requested layouts."""
    categories = ["A", "B", "C", "D"]
    sizes = [9, 4, 1, 6]
    a = AnnData(
        X=np.arange(sum(sizes) * 3, dtype=float).reshape(-1, 3)
        if case in paga_color_cases()
        else None,
        var=pd.DataFrame(index=["g1", "g2", "red"])
        if case in paga_color_cases()
        else None,
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
    if case in {"empty", "component_empty"}:
        a.uns["paga"]["connectivities"] = csr_matrix((4, 4))
    elif case in {"asymmetric", "asymmetric_csc"}:
        a.uns["paga"]["connectivities"][0, 1] = 0.7
        if case == "asymmetric_csc":
            a.uns["paga"]["connectivities"] = a.uns["paga"]["connectivities"].tocsc()
    elif case == "uniform_sizes":
        del a.uns["cluster_sizes"]
    elif case == "component_tie":
        a.uns["paga"]["connectivities"] = csr_matrix(
            [[0, 0.8, 0, 0], [0.8, 0, 0, 0], [0, 0, 0, 0.6], [0, 0, 0.6, 0]]
        )
    if case in paga_color_cases():
        a.obs["score"] = np.arange(a.n_obs, dtype=float) - 5
        if case == "obs_missing":
            a.obs.loc["cell-1", "score"] = np.nan
        if case == "gene_missing":
            a.X[1, 0] = np.nan
        if case.startswith("constant"):
            a.obs["score"] = 7.0
        a.raw = a.copy()
        a.X = a.X + 100
        if case == "degree_csc":
            a.uns["paga"]["connectivities"][0, 1] = 0.7
            a.uns["paga"]["connectivities"] = a.uns["paga"]["connectivities"].tocsc()
    return a


def paga_color_cases():
    """Cover annotation/gene means, thresholded degrees and Scanpy's guide choices."""
    return {
        "obs_score": {"color": "score"},
        "obs_missing": {"color": "score"},
        "gene_raw": {"color": "g1"},
        "gene_x": {"color": "g1", "use_raw": False},
        "gene_missing": {"color": "g1"},
        "degree_solid": {"color": "degree_solid", "threshold": 0.1},
        "degree_dashed": {
            "color": "degree_dashed",
            "dashed_edges": "weak",
            "threshold": 0.25,
        },
        "degree_csc": {"color": "degree_solid", "threshold": 0},
        "no_guide": {"color": "score", "colorbar": False},
        "colorbar_true": {"color": "score", "colorbar": True},
        "constant": {"color": "score"},
        "constant_no_guide": {"color": "score", "colorbar": False},
        "numeric_alias": {"color": "red", "colors": "score"},
        "component_score": {
            "color": "score",
            "single_component": True,
            "threshold": 0.2,
        },
        "component_gene": {"color": "g1", "single_component": True, "threshold": 0.2},
        "component_degree": {
            "color": "degree_solid",
            "single_component": True,
            "threshold": 0.2,
        },
    }


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
        "component": {"pos": POSITIONS, "threshold": 0.2, "single_component": True},
        "component_tie": {"pos": POSITIONS, "single_component": True},
        "component_empty": {"pos": POSITIONS, "single_component": True},
        "component_connected": {"pos": POSITIONS, "single_component": True},
        **{
            key: {"pos": POSITIONS, **options}
            for key, options in paga_color_cases().items()
        },
    }


def paga_reference(case):
    """Return a public Scanpy reference; explicitly subset disconnected component cases.

    Scanpy 1.11.5's direct single_component call keeps full positions and fails.
    """
    a, options = make_paga(case), paga_cases()[case].copy()
    if not case.startswith("component") or case == "component_connected":
        return a, options
    keep = (
        [0]
        if case == "component_empty"
        else [0, 1]
        if case == "component_tie"
        else [1, 2, 3]
    )
    labels = a.obs["cluster"].cat.categories[keep]
    subset = a[a.obs["cluster"].isin(labels)].copy()
    subset.uns["paga"]["connectivities"] = a.uns["paga"]["connectivities"][keep][
        :, keep
    ]
    subset.uns["cluster_sizes"] = a.uns["cluster_sizes"][keep]
    subset.uns["cluster_colors"] = [a.uns["cluster_colors"][i] for i in keep]
    options.update(pos=POSITIONS[keep], single_component=False)
    if case == "component_degree":
        options.update(color=[1, 5 / 7, 2 / 7], colorbar=False)
    return subset, options
