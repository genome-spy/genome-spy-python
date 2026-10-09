"""PBMC marker matrix.

Compare mean marker expression across eight cell types, with aligned cell counts.
"""

import genome_spy as gs
from genome_spy.datasets import _load_table_bundle as load_data

META = {
    "category": "Single-cell expression",
    "order": 10,
    "height": 660,
    "max_width": 1050,
}

data = load_data(
    "pbmc_markers", ("groups", "markers", "means", "group_tree", "marker_groups")
)
genes = data["markers"]["gene"].tolist()
row_y = (
    gs.Y("group_order:Q")
    .scale(
        domain=data["group_domain"], reverse=True, nice=False, zero=False, zoom=False
    )
    .axis(None)
)
gene_x = (
    gs.X("gene:O")
    .scale(domain=genes, padding=0, zoom=False)
    .axis(
        title=None,
        orient="top",
        labelAngle=-45,
        labelFontSize=11,
        minExtent=40,
        maxExtent=40,
    )
)

# Prepared means include cells with zero expression.
matrix = (
    gs.Chart(data["means"])
    .mark_rect(xOffset=1, x2Offset=-1, yOffset=1, y2Offset=-1)
    .encode(
        x=gene_x,
        y=row_y.field("row_start"),
        y2="row_end:Q",
        color=gs.Color("mean_expression:Q")
        .scale(domain=[0, data["mean_expression_limit"]], scheme="blues")
        .legend(title="Mean log1p(counts)", orient="bottom", gradientLength=220),
        tooltip=[
            "cell_type:N",
            "gene:N",
            gs.Tooltip("mean_expression:Q", format=".3f"),
        ],
    )
    .properties(height=320, width=gs.SizeDef(grow=1))
)

labels = (
    gs.Chart(data["groups"])
    .mark_text(align="right", size=12)
    .encode(x=gs.value(1), y=row_y, text="cell_type:N")
    .properties(width=155, height=320)
)
counts = (
    gs.Chart(data["groups"])
    .mark_rect(color="#9aa8b4", yOffset=12, y2Offset=-12)
    .encode(
        x=gs.X("count:Q")
        .scale(domain=[0, data["count_limit"]], reverse=True)
        .axis(
            title="Cell count",
            values=[0, data["count_limit"]],
            labelFontSize=9,
            titleFontSize=10,
        ),
        x2=gs.datum(0),
        y=row_y.field("row_start"),
        y2="row_end:Q",
        tooltip=["cell_type:N", "count:Q"],
    )
    .properties(width=80, height=320)
)
count_labels = (
    gs.Chart(data["groups"])
    .mark_text(align="right", size=10, dx=-3)
    .encode(x=gs.value(1), y=row_y, text="count:Q")
)
# Draw the prepared group tree with the same row scale as the expression matrix.
tree = (
    gs.Chart(data["group_tree"])
    .mark_rule(color="#667382", size=1, strokeCap="square", tooltip=None)
    .encode(
        x=gs.X("distance:Q")
        .scale(domain=[0, data["dendrogram"]["distance_limit"]])
        .axis(None),
        x2="distance_end:Q",
        y=row_y.field("row"),
        y2="row_end:Q",
    )
    .properties(width=75, height=320)
)
colors = gs.Scale(
    domain=data["groups"]["cell_type"].tolist(),
    range=data["groups"]["color"].tolist(),
)
header_x = (
    gs.X("start:Q")
    .scale(domain=data["marker_domain"], nice=False, zero=False, zoom=False)
    .axis(None)
)
# Marker-group blocks span all genes associated with that cell type.
marker_blocks = (
    gs.Chart(data["marker_groups"])
    .mark_rect(xOffset=1, x2Offset=-1)
    .encode(
        x=header_x,
        x2="end:Q",
        color=gs.Color("cell_type:N").scale(colors).legend(None),
        tooltip="cell_type:N",
    )
)
marker_labels = (
    gs.Chart(data["marker_groups"])
    .mark_text(angle=-90, size=10.5, color="white", squeeze=False, tooltip=None)
    .encode(
        x=header_x.field("center"),
        y=gs.value(0.5),
        text="cell_type:N",
    )
)
marker_header = (
    (
        marker_blocks
        + marker_labels.transform_filter(gs.datum.label_color == "white")
        + marker_labels.mark_text(
            angle=-90, size=10.5, color="#173238", squeeze=False, tooltip=None
        ).transform_filter(gs.datum.label_color == "#173238")
    )
    .properties(height=120)
    .resolve_scale(x="excluded", y="excluded", color="excluded")
)
# The matrix's top gene axis occupies 40 px below the colored header.
spacer = (
    gs.layer(gs.Chart([{}]).mark_point(opacity=0, tooltip=None))
    .properties(height=160)
    .resolve_scale(y="excluded")
)
expression_column = (
    (marker_header & matrix)
    .properties(width=gs.SizeDef(grow=1))
    .resolve_scale(x="shared")
)
label_column = (spacer & labels).properties(width=155).resolve_scale(x="independent")
count_column = (
    (spacer & (counts + count_labels).properties(width=80, height=320))
    .properties(width=80)
    .resolve_scale(x="independent")
)
tree_column = (spacer & tree).properties(width=75).resolve_scale(x="independent")
chart = (
    gs.hconcat(
        label_column,
        count_column,
        expression_column,
        tree_column,
        spacing=12,
    )
    .resolve_scale(x="independent", y="shared", color="independent")
    .resolve_legend(default="collected")
    .configure_legend(direction="horizontal", titleOrient="top")
    .properties(title="PBMC marker expression by cell type")
)
