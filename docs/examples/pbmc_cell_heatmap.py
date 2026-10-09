"""PBMC cell heatmap.

Zoom through individual cells to inspect the same twelve markers within each cell type.
"""

import genome_spy as gs
from genome_spy.anndata import from_anndata
from genome_spy.datasets import _load_table_bundle as load_data
from genome_spy.datasets._pbmc import expression_table, pbmc_markers

META = {
    "category": "Single-cell expression",
    "order": 20,
    "height": 760,
    "max_width": 1050,
}

adata = pbmc_markers()
data = load_data("pbmc_markers", ("groups", "markers", "group_tree"))
genes = list(adata.var_names)
projection = from_anndata(
    adata, obs=["cell", "cell_type", "cell_order", "cell_end"], genes=genes
)
expression = expression_table(projection, genes)
cell_y = gs.Y("cell_order:Q").axis(None)

tiles = (
    gs.Chart(expression)
    .mark_rect(minHeight=0, minOpacity=1)
    .encode(
        x=gs.X("gene:O")
        .scale(domain=genes, padding=0, zoom=False)
        .axis(title=None, orient="top", labelAngle=-45, labelFontSize=11),
        y=cell_y,
        y2="cell_end:Q",
        color=gs.Color("expression:Q")
        .scale(domain=[0, data["expression_limit"]], scheme="viridis")
        .legend(title="log1p(counts)", orient="bottom", gradientLength=200),
        tooltip=[
            "cell:N",
            "cell_type:N",
            "gene:N",
            gs.Tooltip("expression:Q", format=".3f"),
        ],
    )
    .properties(width=gs.SizeDef(grow=1), height=560)
)
boundaries = (
    gs.Chart(data["groups"])
    .mark_rule(color="white", size=1, tooltip=None)
    .encode(y=gs.Y("start:Q").axis(None))
)
colors = gs.Scale(
    domain=data["groups"]["cell_type"].tolist(), range=data["groups"]["color"].tolist()
)
# Native AnnData inputs expose obs directly for the cell annotation rail.
rail = (
    gs.Chart(adata)
    .mark_rect(minHeight=0, minOpacity=1)
    .encode(
        y=cell_y,
        y2="cell_end:Q",
        color=gs.Color("cell_type:N")
        .scale(colors)
        .legend(title="Cell type", orient="bottom", columns=2),
        tooltip=["cell:N", "cell_type:N"],
    )
    .properties(width=14, height=560)
)
tree = (
    gs.Chart(data["group_tree"])
    .mark_rule(color="#667382", size=1, strokeCap="square", tooltip=None)
    .encode(
        x=gs.X("distance:Q")
        .scale(domain=[0, data["dendrogram"]["distance_limit"]])
        .axis(None),
        x2="distance_end:Q",
        y=gs.Y("cell:Q").axis(None),
        y2="cell_end:Q",
    )
    .properties(width=75, height=560)
)
chart = (
    (
        rail
        | (tiles + boundaries).properties(height=560, width=gs.SizeDef(grow=1))
        | tree
    )
    .properties(
        scales=gs.scales(
            y=gs.Scale(
                name="pbmc-cells",
                type="linear",
                domain=[0, len(adata)],
                reverse=True,
                nice=False,
                zoom=True,
            )
        ),
        title="PBMC marker expression in individual cells",
    )
    .resolve_scale(x="independent", y="shared", color="independent")
    .resolve_legend(default="collected")
    .configure_legend(direction="horizontal", titleOrient="top", columnPadding=20)
)
