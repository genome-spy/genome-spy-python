"""PBMC UMAP panels.

Compare six marker genes, total counts, and cell types on one embedding.
Hover over a cell to outline it in every panel.
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
hovered = gs.selection_point(
    "cell_hover",
    on="pointerover",
    clear="mouseleave",
    toggle=False,
    persist=False,
    empty=False,
)
cell_types = gs.selection_point("cell_types", encodings=["color"], bind="legend")
gene_range = gs.selection_interval("gene_range", encodings=["color"], bind="legend")
counts_range = gs.selection_interval("counts_range", encodings=["color"], bind="legend")

# Test the same cell fields before splitting the data into panels.
selected = ~gs.expr.selectionActive(gs.Expression(cell_types.name)) | (
    gs.expr.selectionContains(
        gs.Expression(cell_types.name), "color", gs.datum.cell_type
    )
)
for selection, field in ((gene_range, genes[0]), (counts_range, "n_counts")):
    reference = gs.Expression(selection.name)
    bounds = gs.expr.selectionBounds(reference, "color")
    selected = selected & (
        ~gs.expr.selectionActive(reference)
        | ((gs.datum[field] >= bounds[0]) & (gs.datum[field] < bounds[1]))
    )

points = (
    gs.Chart()
    .mark_point(size=gs.expr(gs.expr.min(8 * gs.expr.pow(zoom, 0.6), 40)), opacity=0.9)
    .add_params(hovered.copy(push="outer"))
    .encode(
        key=gs.Key("cell"),
        opacity=gs.Opacity("legend_opacity:Q").scale(None).legend(None),
        stroke=gs.value("#111827"),
        strokeWidth=gs.when(hovered).then(gs.value(2)).otherwise(gs.value(0)),
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
    points.add_params(*([gene_range.copy(push="outer")] if i == 0 else []))
    .transform_collect(sort=gs.compare(field=gene))
    .encode(
        color=gs.Color(f"{gene}:Q")
        .scale(
            domain=[0, data["umap_expression_limit"]],
            range=["#e8edf1", "#c9b2df", "#9976c4", "#70469c", "#48226f"],
        )
        .legend(
            gs.Legend(title=f"{gene} expression", orient="bottom", gradientLength=180)
            if i == 0
            else None
        ),
        tooltip=["cell:N", "cell_type:N", gs.Tooltip(f"{gene}:Q", format=".3f")],
    )
    .properties(title=gs.title(gene, fontSize=13))
    for i, gene in enumerate(genes)
]
counts = (
    points.add_params(counts_range.copy(push="outer"))
    .transform_collect(sort=gs.compare(field="n_counts"))
    .encode(
        color=gs.Color("n_counts:Q")
        .scale(domain=[0, data["n_counts_limit"]], scheme="blues")
        .legend(title="Total counts", orient="bottom", gradientLength=140),
        tooltip=["cell:N", "cell_type:N", gs.Tooltip("n_counts:Q", format=",.0f")],
    )
    .properties(title=gs.title("n_counts", fontSize=13))
)
labels = (
    points.add_params(cell_types.copy(push="outer"))
    .encode(
        color=gs.Color("cell_type:N")
        .scale(
            domain=data["groups"]["cell_type"].tolist(),
            range=data["groups"]["color"].tolist(),
        )
        .legend(title="Cell type", orient="bottom", columns=2),
        tooltip=["cell:N", "cell_type:N"],
    )
    .properties(title=gs.title("cell_type", fontSize=13))
)
chart = (
    gs.concat(*panels, counts, labels, columns=4, spacing=16)
    .properties(data=cells, title="PBMC markers and cell annotations")
    .transform_identifier()
    .add_params(
        gs.param("cell_hover", value=None),
        gs.param(cell_types.name, value=None),
        gs.param(gene_range.name, value=None),
        gs.param(counts_range.name, value=None),
    )
    .transform_calculate(legend_opacity=gs.expr.if_(selected, 0.9, 0.04))
    .resolve_scale(x="shared", y="shared", color="independent")
    .resolve_legend(default="collected")
    .configure_legend(
        selectionLabel=False,
        direction="horizontal",
        titleOrient="top",
        columnPadding=20,
    )
)
