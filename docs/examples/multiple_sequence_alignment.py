"""Multiple sequence alignment.

An alignment view combines a sequence-logo summary with a zoomable row for
each aligned sequence.
"""

import genome_spy as gs
from genome_spy.schema import Scale

META = {
    "category": "Reference annotation tracks",
    "order": 28,
    "height": 440,
    "max_width": 980,
}

BASE_COLORS = Scale(
    domain=["A", "C", "T", "G", "N", "-"],
    range=["#4FBF45", "#4D96E8", "#E85F78", "#E8B322", "#BDBDBD", "#f5f5f5"],
)

logo = (
    gs.Chart()
    .transform_aggregate(groupby=["pos", "sequence"])
    .transform_formula(
        expr=gs.expr.if_(gs.datum.sequence == "-", None, gs.datum.sequence),
        as_="base",
    )
    .transform_stack(
        field="count",
        groupby=["pos"],
        offset="information",
        as_=["_y0", "_y1"],
        baseField="base",
        sort=gs.compare("count", order="ascending"),
    )
    .mark_text(
        font="Source Sans Pro",
        fontWeight=700,
        size=90,
        squeeze=True,
        fitToBand=True,
        logoLetters=True,
        paddingX=0,
        paddingY=0,
    )
    .encode(
        x=gs.X("pos:I").axis(None),
        y=gs.Y("_y0:Q").scale(domain=[0, 2], zoom=True).title("Information"),
        y2=gs.Y2("_y1"),
        text=gs.Text("base:N"),
        color=gs.Color("base:N").scale(BASE_COLORS).legend(None),
    )
    .properties(height=70, title="Sequence logo")
)

alignment = (
    gs.layer(
        gs.Chart().mark_rect(),
        gs.Chart()
        .mark_text(size=11, fitToBand=True, opacity=0.7, tooltip=None)
        .encode(color=gs.value("black"), text=gs.Text("sequence:N")),
    )
    .encode(
        x=gs.X("pos:I"),
        y=gs.Y("identifier:N").title(None),
        color=gs.Color("sequence:N").scale(BASE_COLORS).legend(None),
    )
    .properties(height=gs.step(14), viewportHeight="container", title="Alignment")
)

chart = (
    gs.vconcat(logo, alignment, spacing=8)
    .properties(
        assembly="hg38",
        data=gs.Data(
            url="https://data.genomespy.app/sample-data/16SRNA_Deino_87seq.aln",
            format=gs.data_format(type="fasta"),
        ),
        scales=gs.scales(x=gs.Scale(domain=[190, 230], zoom={"extent": "data"})),
        description="A multiple sequence alignment with a sequence-logo overview.",
    )
    .transform_flatten_sequence()
    .resolve_scale(x="shared")
    .resolve_axis(x="independent")
)
