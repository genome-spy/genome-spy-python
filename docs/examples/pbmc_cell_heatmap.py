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
cell_types = gs.selection_point("cell_types", encodings=["color"], bind="legend")
cell_type_match = ~gs.expr.selectionActive(gs.Expression(cell_types.name)) | (
    gs.expr.selectionContains(
        gs.Expression(cell_types.name), "color", gs.datum.cell_type
    )
)
expression_range = gs.selection_interval(
    "expression_range", encodings=["color"], bind="legend"
)
expression_bounds = gs.expr.selectionBounds(
    gs.Expression(expression_range.name), "color"
)
expression_match = ~gs.expr.selectionActive(gs.Expression(expression_range.name)) | (
    (gs.datum.expression >= expression_bounds[0])
    & (gs.datum.expression < expression_bounds[1])
)


tiles = (
    gs.Chart(expression)
    .add_params(expression_range)
    .transform_calculate(
        legend_opacity=gs.expr.if_(cell_type_match & expression_match, 1, 0.08)
    )
    .mark_rect(minHeight=0, minOpacity=1)
    .encode(
        opacity=gs.Opacity("legend_opacity:Q").scale(None).legend(None),
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
    .properties(name="expressionCells", width=gs.SizeDef(grow=1), height=560)
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
    .add_params(cell_types.copy(push="outer"))
    .mark_rect(minHeight=0, minOpacity=1)
    .encode(
        opacity=gs.when(cell_types).then(gs.value(1)).otherwise(gs.value(0.15)),
        y=cell_y,
        y2="cell_end:Q",
        color=gs.Color("cell_type:N")
        .scale(colors)
        .legend(title="Cell type", orient="bottom", columns=2),
        tooltip=["cell:N", "cell_type:N"],
    )
    .properties(width=14)
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
    .properties(width=75)
)
chart = (
    gs.surround(
        (tiles + boundaries).properties(height=560, width=gs.SizeDef(grow=1)),
        surround=gs.SurroundSides(left=[rail], right=[tree]),
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
    .add_params(gs.param(cell_types.name, value=None))
    .resolve_legend(default="collected")
    .configure_legend(
        selectionLabel=False,
        direction="horizontal",
        titleOrient="top",
        columnPadding=20,
    )
)
