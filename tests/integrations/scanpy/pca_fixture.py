"""Stored PCA results for unit and browser composition checks."""

import numpy as np

from tests.integrations.scanpy.ranked_fixture import make_ranked_adata


def make_pca_adata():
    """Return stored coordinates and three loading columns for overview checks."""
    a = make_ranked_adata()
    a.varm["PCs"] = np.column_stack([a.varm["PCs"], [-3, 0, 2, 1]]).astype(float)
    a.obsm["X_pca"] = np.column_stack(
        [np.arange(a.n_obs), np.arange(a.n_obs) ** 2, -np.arange(a.n_obs)]
    ).astype(float)
    return a
