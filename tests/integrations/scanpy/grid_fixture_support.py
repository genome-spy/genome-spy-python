"""Grid and builder examples shared by structural and browser checks."""

import warnings

import numpy as np

import genome_spy.integrations.scanpy as gsc
from tests.integrations.scanpy.expression_fixtures import (
    make_cluster_adata,
    make_heatmap_adata,
    make_tree_adata,
)

FAMILIES = ["dotplot", "matrixplot", "heatmap", "matrix", "clustermap"]


def make_chart(family, **options):
    """Build a small grid through its public function or builder."""
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", UserWarning)
        common = dict(width=320, height=260, **options)
        if family == "matrix":
            return gsc.pl.matrix(np.arange(1, 13).reshape(4, 3), show=False, **common)
        if family == "clustermap":
            return gsc.pl.clustermap(make_cluster_adata(), show=False, **common)
        if family in ("DotPlot", "MatrixPlot"):
            return getattr(gsc.pl, family)(
                make_heatmap_adata(), ["g1", "g2", "g1"], "group", **common
            ).to_chart()
        return getattr(gsc.pl, family)(
            make_heatmap_adata(), ["g1", "g2", "g1"], "group", show=False, **common
        )


def builder(family="DotPlot"):
    """Build a styled grouped plot with repeated marker slots."""
    plot = getattr(gsc.pl, family)(
        make_tree_adata(),
        {"First": ["g2", "g1"], "Again": "g2"},
        "group",
        zoom="xy",
        hover=True,
        width=360,
        height=260,
    )
    if family == "MatrixPlot":
        return plot.style(cmap="viridis", edge_color="navy", edge_lw=0.7)
    return plot.style(
        cmap="viridis",
        dot_edge_color="navy",
        dot_edge_lw=0.7,
        largest_dot=120,
        size_exponent=2,
        grid=True,
    )
