"""PBMC UMAP panels.

Compare six marker genes, total counts, and cell types on one embedding.
"""

import genome_spy as gs
from genome_spy.anndata import from_anndata
from genome_spy.datasets import _load_table_bundle as load_data
from genome_spy.datasets._pbmc import pbmc_markers

META = {
    "category": "Single-cell expression",
    "order": 5,
    "height": 660,
    "max_width": 1050,
}

adata = pbmc_markers(umap_genes=True)
data = load_data("pbmc_markers", ("groups",))
genes = list(adata.var_names)
cells = from_anndata(
    adata,
    obs=["cell", "cell_type", "n_counts"],
    genes=genes,
    obsm_keys=[("X_umap", 0), ("X_umap", 1)],
)
zoom = gs.Expression("zoomLevel")
points = (
    gs.Chart()
    .mark_point(size=gs.expr(gs.expr.min(8 * gs.expr.pow(zoom, 0.6), 40)), opacity=0.9)
    .encode(
        x=gs.X("X_umap-0:Q")
        .scale(
            name="pbmc-umap-x",
            domain=data["umap_domains"]["x"],
            zero=False,
            nice=False,
            zoom=True,
        )
        .axis(None),
        y=gs.Y("X_umap-1:Q")
        .scale(
            name="pbmc-umap-y",
            domain=data["umap_domains"]["y"],
            zero=False,
            nice=False,
            zoom=True,
        )
        .axis(None),
    )
    .properties(width=gs.SizeDef(grow=1), height=210)
)
panels = [
    points.transform_collect(sort={"field": gene})
    .encode(
        color=gs.Color(f"{gene}:Q")
        .scale(
            domain=[0, data["umap_expression_limit"]],
            range=["#e8edf1", "#c9b2df", "#9976c4", "#70469c", "#48226f"],
        )
        .legend(
            gs.Legend(title="log1p(counts)", orient="bottom", gradientLength=180)
            if i == 0
            else None
        ),
        tooltip=["cell:N", "cell_type:N", gs.Tooltip(f"{gene}:Q", format=".3f")],
    )
    .properties(title=gs.title(gene, fontSize=13))
    for i, gene in enumerate(genes)
]
counts = (
    points.transform_collect(sort={"field": "n_counts"})
    .encode(
        color=gs.Color("n_counts:Q")
        .scale(domain=[0, data["n_counts_limit"]], scheme="blues")
        .legend(title="Total counts", orient="bottom", gradientLength=140),
        tooltip=["cell:N", "cell_type:N", gs.Tooltip("n_counts:Q", format=",.0f")],
    )
    .properties(title=gs.title("n_counts", fontSize=13))
)
labels = points.encode(
    color=gs.Color("cell_type:N")
    .scale(
        domain=data["groups"]["cell_type"].tolist(),
        range=data["groups"]["color"].tolist(),
    )
    .legend(title="Cell type", orient="bottom", columns=2),
    tooltip=["cell:N", "cell_type:N"],
).properties(title=gs.title("cell_type", fontSize=13))
chart = (
    gs.concat(*panels, counts, labels, columns=4, spacing=16)
    .properties(data=cells, title="PBMC markers and cell annotations")
    .resolve_scale(x="shared", y="shared", color="independent")
    .resolve_legend(default="collected")
    .configure_legend(direction="horizontal", titleOrient="top", columnPadding=20)
)
