"""Original observation/variable scatter inputs with distinct raw and layer values."""

from tests.integrations.scanpy.embedding_fixture import make_embedding_adata


def make_scatter_adata():
    """Add finite annotations to the shared stored-coordinate fixture for either axis."""
    import numpy as np
    import pandas as pd

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
