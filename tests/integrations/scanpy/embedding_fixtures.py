"""Small embedding inputs shared by semantic and browser tests."""

from __future__ import annotations

import warnings
from typing import Any

import anndata as ad
import numpy as np
import pandas as pd
import pytest
from scipy import sparse

from tests.integrations.scanpy.ranked_fixture import make_ranked_adata


def make_adata() -> Any:
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


def make_embedding_adata():
    """Return distinct stored bases without fitting an embedding or copying a dataset."""
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", UserWarning)
        a = make_adata()
    coordinates = a.obsm["X_umap"]
    for i, basis in enumerate(
        ("tsne", "diffmap", "pca", "draw_graph_fa", "draw_graph_fr")
    ):
        a.obsm[f"X_{basis}"] = coordinates * (i + 2) + np.array(
            [3, -2, 4], dtype=np.float32
        )
    a.obsm["custom"] = coordinates * 2
    a.uns["draw_graph"] = {"params": {"layout": "fa"}}
    a.uns["pca"] = {"variance_ratio": np.array([0.5, 0.25, 0.125])}
    return a


def embedding_cases():
    """Return basis, component and label variations for complete chart references."""
    return {
        "custom": (
            "embedding",
            {"basis": "custom", "dimensions": (2, 0), "color": "score"},
        ),
        "tsne": ("tsne", {"color": "cell_type"}),
        "diffmap_default": ("diffmap", {"color": "score"}),
        "diffmap_components": ("diffmap", {"components": "2,3", "color": "g1"}),
        "draw_graph_default": ("draw_graph", {"color": "cell_type"}),
        "draw_graph_fr": ("draw_graph", {"layout": "fr", "color": "score"}),
        "pca_variance": (
            "pca",
            {"annotate_var_explained": True, "components": "2,3", "color": "score"},
        ),
        "pca_alias": ("pca_scatter", {"color": "g1"}),
    }


def make_scatter_adata():
    """Add finite annotations to the shared stored-coordinate fixture for either axis."""

    a = make_embedding_adata()
    a.obs["x_value"] = np.array([0, 1, 0, 2, 4, -1, 0.5, 1.5], dtype=np.float32)
    a.obs["y_value"] = np.array([-1, 0, -1, 1, 3, 2, -2, 2], dtype=np.float32)
    a.var["mean_value"] = np.array([0.2, 1.7, 0.8], dtype=np.float32)
    a.var["dispersion"] = np.array([2.3, 0.5, 1.1], dtype=np.float32)
    a.var["gene_group"] = pd.Categorical(
        ["signal", "marker", "signal"], categories=["marker", "signal"]
    )
    a.uns["gene_group_colors"] = ["#440099", "#ee9900"]
    return a


def scatter_cases():
    """Return complete cases covering the separate scatter lookups and coordinate labels."""
    return {
        "observations": dict(x="x_value", y="y_value", color="cell_type"),
        "continuous": dict(x="x_value", y="y_value", color="score"),
        "raw": dict(x="g1", y="g2", color="raw_only"),
        "layers": dict(
            x="g1", y="g2", color="g1", use_raw=False, layers=("counts", "X", "X")
        ),
        "variables": dict(x="mean_value", y="dispersion", color="gene_group"),
        "variable_expression": dict(
            x="c1", y="c3", color="c4", use_raw=False, layers=("counts", "X", "counts")
        ),
        "diffmap": dict(basis="diffmap", color="g1"),
        "literal": dict(basis="pca", components="2,3", color="#3478ab"),
    }


def make_density(grouped=True):
    """Return supplied densities and metadata; no expression or density analysis is needed."""
    xy = np.array(
        [
            [-3, -2],
            [-2, -1],
            [-1, -2],
            [0, -1],
            [1, -2],
            [2, -1],
            [-3, 1],
            [-2, 2],
            [-1, 1],
            [0, 2],
            [1, 1],
            [2, 2],
        ],
        dtype=float,
    )
    density = np.array([0, 0.2, 0.4, 0.6, 0.8, 1, 0.15, 0.3, 0.45, 0.6, 0.75, 0.9])
    a = ad.AnnData(
        sparse.csr_matrix((12, 20000)),
        obs=pd.DataFrame(
            {
                "condition": pd.Categorical(["B", "A"] * 6, categories=["B", "A"]),
                "cell_id": [f"id-{i}" for i in range(12)],
            },
            index=[f"cell-{i}" for i in range(12)],
        ),
    )
    a.obsm["X_umap"] = np.column_stack([xy, xy[:, 0] + xy[:, 1]])
    for basis in ("pca", "diffmap", "tsne", "draw_graph_fa"):
        a.obsm["X_" + basis] = a.obsm["X_umap"] * 2 + 5
    for key in ("scores", "umap_density", "umap_density_condition"):
        a.obs[key] = density.copy()
        a.uns[key + "_params"] = {
            "covariate": "condition" if grouped else None,
            "components": [1, 2],
        }
    return a


def make_pca_adata():
    """Return stored coordinates and three loading columns for overview checks."""
    a = make_ranked_adata()
    a.varm["PCs"] = np.column_stack([a.varm["PCs"], [-3, 0, 2, 1]]).astype(float)
    a.obsm["X_pca"] = np.column_stack(
        [np.arange(a.n_obs), np.arange(a.n_obs) ** 2, -np.arange(a.n_obs)]
    ).astype(float)
    return a


@pytest.fixture
def adata():
    """Return six cells with missing expression for linked-summary checks."""
    from anndata import AnnData

    a = AnnData(
        np.array(
            [
                [-1, np.nan],
                [0, np.nan],
                [0.5, np.nan],
                [1, np.nan],
                [2, np.nan],
                [np.nan, np.nan],
            ]
        ),
        obs=pd.DataFrame(
            {"type": pd.Categorical(["A", "A", "B", "B", "B", "A"])},
            index=[f"cell-{i}" for i in range(6)],
        ),
        var=pd.DataFrame(index=["HLA-DRA", "missing.gene"]),
    )
    a.obsm["X_umap"] = np.array(
        [[0, 0], [1, 0], [2, 1], [3, 1], [4, 2], [5, 2]], dtype=float
    )
    return a


@pytest.fixture
def metadata_adata(adata):
    """Add missing categories and numeric observations to the summary fixture."""
    adata.obs["sample.label"] = pd.Categorical(
        ["D1", "D1", "D2", None, "D2", "D3"], categories=["D3", "D2", "D1", "Unused"]
    )
    adata.uns["sample.label_colors"] = ["purple", "orange", "teal", "pink"]
    adata.obs["qc.score"] = [0.0, np.nan, -0.5, 0.5, 1.0, np.nan]
    return adata


def graph_adata(storage="csr", key="neighbors"):
    """Return an original stored graph with asymmetric, negative and sparse-zero entries."""
    data = make_embedding_adata()
    matrix = sparse.coo_matrix(
        (
            [1, 0.5, 0.8, 0.9, 0, -0.3, 0.2, 0.1],
            ([0, 1, 2, 3, 3, 5, 0, 0], [1, 0, 3, 2, 7, 4, 6, 2]),
        ),
        shape=(8, 8),
    )
    if storage == "dense":
        matrix = matrix.toarray()
    else:
        matrix = {
            "csr": sparse.csr_matrix,
            "csc": sparse.csc_matrix,
            "csr_array": sparse.csr_array,
            "csc_array": sparse.csc_array,
            "legacy_lil": sparse.lil_matrix,
        }[storage](matrix)
    name = "connectivities" if key == "neighbors" else "saved_connectivities"
    data.uns[key] = {"connectivities_key": name, "distances_key": "unused_distances"}
    if storage == "legacy_lil":
        data.uns[key][name] = matrix
    else:
        data.obsp[name] = matrix
    return data


FAMILIES = ["embedding", "umap", "tsne", "diffmap", "draw_graph", "pca", "pca_scatter"]


def umap_data():
    """Return the small UMAP fixture without duplicate-name warning noise."""
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", UserWarning)
        return make_adata()
