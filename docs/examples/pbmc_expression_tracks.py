"""PBMC expression tracks.

Inspect individual marker values in twelve tracks that zoom together.
"""

import genome_spy as gs
from genome_spy.anndata import from_anndata
from genome_spy.datasets import _load_table_bundle as load_data
from genome_spy.datasets._pbmc import expression_table, pbmc_markers

META = {
    "category": "Single-cell expression",
    "order": 30,
    "height": 830,
    "max_width": 1050,
}

adata = pbmc_markers()
data = load_data("pbmc_markers", ("groups", "markers", "group_tree"))
genes = list(adata.var_names)
projection = from_anndata(
    adata, obs=["cell", "cell_type", "cell_order", "cell_end"], genes=genes
)
expression = expression_table(projection, genes)
colors = gs.Scale(
    domain=data["groups"]["cell_type"].tolist(), range=data["groups"]["color"].tolist()
)
cell_x = gs.X("cell_order:Q").axis(None)
tracks = []

for marker in data["markers"].to_dict("records"):
    # Each adjacent rect spans one cell, from zero to its expression value.
    bars = (
        gs.Chart()
        .transform_filter(gs.datum.gene == marker["gene"])
        .mark_rect(minWidth=0, minOpacity=1)
        .encode(
            x=cell_x,
            x2="cell_end:Q",
            y=gs.Y("expression:Q")
            .scale(domain=[0, marker["expression_limit"]], zoom=False)
            .axis(
                title=None,
                values=[0, marker["expression_limit"]],
                labelFontSize=9,
                labelFlush=True,
                minExtent=24,
                maxExtent=24,
            ),
            y2=gs.datum(0),
            color=gs.Color("cell_type:N").scale(colors).legend(None),
            tooltip=[
                "cell:N",
                "cell_type:N",
                "gene:N",
                gs.Tooltip("expression:Q", format=".3f"),
            ],
        )
    )
    baseline = (
        gs.Chart([{}])
        .mark_rule(color="#d9dfe4", size=0.5, tooltip=None)
        .encode(y=gs.value(0))
    )
    tracks.append(
        (bars + baseline).properties(
            height=40,
            title=gs.title(
                marker["gene"],
                orient="left",
                angle=0,
                align="right",
                fontSize=11,
                offset=35,
            ),
        )
    )

strip = (
    gs.Chart(data["groups"])
    .mark_rect()
    .encode(
        x=gs.X("start:Q").axis(title="Cells grouped by type", tickCount=5),
        x2="end:Q",
        color=gs.Color("cell_type:N")
        .scale(colors)
        .legend(title="Cell type", orient="bottom", columns=2),
        tooltip=["cell_type:N", "count:Q"],
    )
    .properties(height=10)
)
# One shared table and x scale serve every track; each y scale stays independent.
tree = (
    gs.Chart(data["group_tree"])
    .mark_rule(color="#667382", size=1, strokeCap="square", tooltip=None)
    .encode(
        x=gs.X("cell:Q").axis(None),
        x2="cell_end:Q",
        y=gs.Y("distance:Q")
        .scale(domain=[0, data["dendrogram"]["distance_limit"]], zoom=False)
        .axis(None),
        y2="distance_end:Q",
    )
    .properties(height=65)
)
chart = (
    gs.vconcat(tree, *tracks, strip, spacing=8)
    .properties(
        data=expression,
        scales=gs.scales(
            x=gs.Scale(
                name="pbmc-cells",
                type="linear",
                domain=[0, len(adata)],
                nice=False,
                zoom=True,
            )
        ),
        title="PBMC marker expression tracks: log1p(counts)",
    )
    .resolve_scale(x="shared", y="independent", color="shared")
    .resolve_axis(x="independent", y="independent")
    .resolve_legend(default="collected")
)
