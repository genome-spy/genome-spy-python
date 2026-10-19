"""Stored coordinate cases over the existing original observation fixture."""

import warnings

import numpy as np

from tests.integrations.scanpy.fixture_data import make_adata


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
