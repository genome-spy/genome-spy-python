"""PIK3CA mutation lollipop plot.

Recurrent TCGA-BRCA PIK3CA mutations are displaced just enough to keep dense
hotspots readable while connectors retain their true protein positions.
"""

import genome_spy as gs
from genome_spy.datasets._mutation import pik3ca_lollipop_data

META = {
    "category": "Mutation position plots",
    "order": 12,
    "height": 400,
    "max_width": 980,
}

LABEL_HEIGHT = 65
CONNECTOR_HEIGHT = 20
PROTEIN_HEIGHT = 50
DISPLACEMENT_LENGTH = 18

# Mutations, sample counts, and protein domains are prepared packaged data.
# GenomeSpy performs only the declarative sorting and collision displacement.
data = pik3ca_lollipop_data()

# Labels, stems, points, and counts use separate layers because each needs its
# own sizing and alignment.
mutation_labels = (
    gs.Chart()
    .mark_text(
        angle=-55,
        dx=4,
        size=10,
        align="left",
        baseline="middle",
        color="#303030",
        tooltip=None,
    )
    .encode(y=gs.value(0), text=gs.Text("mutation"))
    .properties(name="mutation-labels", height=LABEL_HEIGHT)
)
stems = (
    gs.Chart()
    .mark_rule(size=gs.expr("lineWidth"), color="#707070", tooltip=None)
    .encode(y2=gs.value(0))
)
upper_guides = (
    gs.Chart()
    .mark_rule(size=gs.expr("lineWidth"), color="#bbb", strokeDash=[3, 3], tooltip=None)
    .encode(y2=gs.value(1))
)
lollipops = (
    gs.Chart()
    .mark_point(size=260, filled=True, stroke="white", strokeWidth=1.5)
    .encode(
        color=gs.Color("variantClass:N").legend(title="Variant class", orient="top"),
        tooltip=[
            gs.Tooltip("mutation").title("Mutation"),
            gs.Tooltip("position").title("Residue"),
            gs.Tooltip("sampleCount").title("Distinct tumor samples"),
            gs.Tooltip("variantClass").title("Variant class"),
            gs.Tooltip("sourceProteinPosition").title("GDC protein position"),
        ],
    )
    .properties(name="lollipops")
)
sample_counts = (
    gs.Chart()
    .mark_text(size=8, align="center", baseline="middle", color="white", tooltip=None)
    .encode(text=gs.Text("sampleCount:Q"))
    .properties(name="sample-counts")
)
mutation_marks = gs.layer(stems, upper_guides, lollipops, sample_counts).properties(
    name="mutations"
)

# Dense hotspots are displaced for readability. These connectors still point
# back to each mutation's true residue position.
connectors = (
    gs.Chart()
    .mark_link(
        linkShape="diagonal",
        orient="vertical",
        x2Offset=0,
        size=gs.expr("lineWidth"),
        color="#707070",
        tooltip=None,
    )
    .encode(x2=gs.X2("position"), y=gs.value(1), y2=gs.value(0))
    .properties(name="lower-connectors")
)
anchors = (
    gs.Chart()
    .mark_rule(size=gs.expr("lineWidth"), color="#707070", tooltip=None, y2Offset=20)
    .encode(xOffset=gs.XOffset(gs.value(0)), y=gs.value(0), y2=gs.value(0))
    .properties(name="true-position-anchors")
)

# displace1d changes only the screen offset; the shared x value remains the real
# protein coordinate used by the domain track. The Python API serializes this
# transform and GenomeSpy executes it reactively in the browser.
mutation_view = (
    gs.vconcat(
        mutation_labels,
        mutation_marks,
        gs.layer(connectors, anchors).properties(height=CONNECTOR_HEIGHT),
        spacing=0,
    )
    .properties(
        data=gs.Data(name="mutations"),
    )
    .encode(
        x=gs.X("position:I").axis(None),
        xOffset=gs.XOffset("xDisplacement:Q").scale(None),
        y=gs.Y("sampleCount:Q")
        .scale(type="log", domainMin=1, nice=False, padding=0.08)
        .axis(title="Distinct tumor samples", grid=False),
    )
    .transform_collect(sort=gs.compare("position", order="ascending"))
    .transform_displace1d(
        pos="position",
        length=DISPLACEMENT_LENGTH,
        as_="xDisplacement",
        positionFactor=gs.expr("pixelsPerResidue"),
        extent=gs.expr("[0.5, proteinLength + 0.5 - 25 / max(1, pixelsPerResidue)]"),
    )
)

# The protein backbone and domains share the mutation view's x scale.
backbone = (
    gs.Chart([{"start": 1}])
    .transform_formula(expr=gs.Expression("proteinLength"), as_="end")
    .mark_rect(y=0.36, y2=0.64, color="#b9bdb8", tooltip=None)
    .properties(name="protein-backbone")
)
domain_blocks = (
    gs.Chart()
    .mark_rect(
        y=0.18,
        y2=0.82,
        cornerRadius=3,
        shadowColor="black",
        shadowOpacity=0.2,
        shadowBlur=4,
        shadowOffsetY=2,
    )
    .encode(
        color=gs.Color("label:N")
        .scale(
            domain=["ABD", "RBD", "C2", "Helical", "Kinase"],
            range=["#6f5bd3", "#4e79a7", "#59a14f", "#f28e2b", "#e15759"],
        )
        .legend(None),
        tooltip=[
            gs.Tooltip("description").title("Domain"),
            gs.Tooltip("start").title("Start"),
            gs.Tooltip("end").title("End"),
            gs.Tooltip(gs.value("UniProt P42336")).title("Source"),
        ],
    )
    .properties(name="domains")
)
domain_labels = (
    gs.Chart()
    .mark_text(color="white", paddingX=3, tooltip=None)
    .encode(text=gs.Text("label"))
    .properties(name="domain-labels")
)
protein = (
    gs.layer(backbone, domain_blocks, domain_labels)
    .properties(
        data=gs.Data(name="domains"),
        name="protein",
        height=PROTEIN_HEIGHT,
        padding=gs.Paddings(top=-5),
    )
    .encode(
        x=gs.X("start:I").axis(
            title="PIK3CA protein position (aa)", tickCount=10, extraValues=[1]
        ),
        x2=gs.X2("end"),
    )
)

# pixelsPerResidue lets the browser-side displacement adapt when the chart
# width changes.
chart = (
    gs.vconcat(mutation_view, protein, spacing=0)
    .properties(
        title="PIK3CA mutations in TCGA-BRCA",
        padding=10,
        description=(
            "Recurrent protein-altering PIK3CA mutations in TCGA-BRCA. "
            "Heights and labels show distinct tumor sample counts."
        ),
        datasets={"mutations": data["mutations"], "domains": data["domains"]},
        scales={"x": {"domainMin": 1, "nice": False}},
        params=[
            gs.param("proteinLength", value=data["proteinLength"]),
            gs.param("lineWidth", value=1),
            gs.param(
                "pixelsPerResidue", expr="width * (scale('x', 1) - scale('x', 0))"
            ),
        ],
    )
    .resolve_scale(x="shared", color="independent")
    .resolve_legend(color="collected")
)
