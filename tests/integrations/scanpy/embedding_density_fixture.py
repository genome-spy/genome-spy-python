"""Original stored densities on distinct supplied embedding coordinates."""

import anndata as ad
import numpy as np
import pandas as pd
from scipy import sparse


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
