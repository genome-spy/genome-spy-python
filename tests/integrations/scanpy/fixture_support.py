"""Small embedding and summary inputs shared without importing test modules."""

import warnings

import numpy as np
import pandas as pd
import pytest
from scipy import sparse

from tests.integrations.scanpy.embedding_fixture import make_embedding_adata
from tests.integrations.scanpy.fixture_data import make_adata


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


def records(chart):
    """Return the shared table of a single-source chart."""
    spec = chart.to_dict()
    return spec["datasets"][spec["data"]["name"]]


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
