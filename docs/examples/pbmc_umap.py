"""PBMC UMAP.

Explore cell types in a zoomable single-cell embedding.
"""

import genome_spy as gs
from genome_spy.anndata import from_anndata
from genome_spy.datasets import _load_table_bundle as load_data
from genome_spy.datasets._pbmc import pbmc_markers

META = {
    "category": "Single-cell expression",
    "order": 0,
    "height": 660,
    "max_width": 850,
}

adata = pbmc_markers()
data = load_data("pbmc_markers", ("groups",))
cells = from_anndata(
    adata, obs=["cell", "cell_type"], obsm_keys=[("X_umap", 0), ("X_umap", 1)]
)
colors = gs.Scale(
    domain=data["groups"]["cell_type"].tolist(),
    range=data["groups"]["color"].tolist(),
)
zoom = gs.Expression("zoomLevel")
chart = (
    gs.Chart(cells)
    .mark_point(
        size=gs.expr(gs.expr.min(18 * gs.expr.pow(zoom, 0.6), 90)), opacity=0.85
    )
    .encode(
        x=gs.X("X_umap-0:Q")
        .scale(
            name="pbmc-umap-x",
            domain=data["umap_domains"]["x"],
            zero=False,
            nice=False,
            zoom=True,
        )
        .axis(title="UMAP 1", labels=False, ticks=False, domain=False, grid=False),
        y=gs.Y("X_umap-1:Q")
        .scale(
            name="pbmc-umap-y",
            domain=data["umap_domains"]["y"],
            zero=False,
            nice=False,
            zoom=True,
        )
        .axis(title="UMAP 2", labels=False, ticks=False, domain=False, grid=False),
        color=gs.Color("cell_type:N")
        .scale(colors)
        .legend(title="Cell type", orient="bottom", columns=4),
        tooltip=["cell:N", "cell_type:N"],
    )
    .properties(height=520, title="PBMC cell types")
)
