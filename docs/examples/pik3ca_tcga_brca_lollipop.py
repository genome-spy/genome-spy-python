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

# Load prepared mutation counts and protein regions.
data = pik3ca_lollipop_data()
protein_length = gs.param("proteinLength", value=data["proteinLength"])
line_width = gs.param("lineWidth", value=1)
# Track the space available per protein position to keep nearby points apart.
pixels_per_residue = gs.param(
    "pixelsPerResidue", expr="width * (scale('x', 1) - scale('x', 0))"
)

# Tilt mutation names so neighboring labels take up less horizontal space.
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
# Draw a stem below each mutation point.
stems = (
    gs.Chart()
    .mark_rule(size=line_width, color="#707070", tooltip=None)
    .encode(y2=gs.value(0))
)
# Connect each point to its name with a faint dashed line.
upper_guides = (
    gs.Chart()
    .mark_rule(size=line_width, color="#bbb", strokeDash=[3, 3], tooltip=None)
    .encode(y2=gs.value(1))
)
# Color mutation points by class and show details on hover.
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
# Write the number of affected samples inside each point.
sample_counts = (
    gs.Chart()
    .mark_text(size=8, align="center", baseline="middle", color="white", tooltip=None)
    .encode(text=gs.Text("sampleCount:Q"))
    .properties(name="sample-counts")
)
mutation_marks = gs.layer(stems, upper_guides, lollipops, sample_counts).properties(
    name="mutations"
)

# Connect shifted points back to their true positions on the protein.
connectors = (
    gs.Chart()
    .mark_link(
        linkShape="diagonal",
        orient="vertical",
        x2Offset=0,
        size=line_width,
        color="#707070",
        tooltip=None,
    )
    .encode(x2=gs.X2("position"), y=gs.value(1), y2=gs.value(0))
    .properties(name="lower-connectors")
)
# Extend each connector down to the protein track.
anchors = (
    gs.Chart()
    .mark_rule(size=line_width, color="#707070", tooltip=None, y2Offset=20)
    .encode(xOffset=gs.XOffset(gs.value(0)), y=gs.value(0), y2=gs.value(0))
    .properties(name="true-position-anchors")
)

# Stack the names, lollipops, and connectors with no gaps between them.
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
    # Spread nearby mutations apart just enough to keep their points readable.
    .transform_displace1d(
        pos="position",
        length=DISPLACEMENT_LENGTH,
        as_="xDisplacement",
        positionFactor=pixels_per_residue,
        extent=gs.expr("[0.5, proteinLength + 0.5 - 25 / max(1, pixelsPerResidue)]"),
    )
)

# Draw a grey band spanning the protein.
backbone = (
    gs.Chart([{"start": 1}])
    .transform_formula(expr=protein_length, as_="end")
    .mark_rect(y=0.36, y2=0.64, color="#b9bdb8", tooltip=None)
    .properties(name="protein-backbone")
)
# Add colored blocks for the protein's named regions.
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
# Write the region names inside their blocks.
domain_labels = (
    gs.Chart()
    .mark_text(color="white", paddingX=3, tooltip=None)
    .encode(text=gs.Text("label"))
    .properties(name="domain-labels")
)
# Combine the protein band, blocks, and labels below the mutations.
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

# Join the mutation and protein tracks, keeping their positions aligned.
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
    )
    .add_params(protein_length, line_width, pixels_per_residue)
    .resolve_scale(x="shared", color="independent")
    .resolve_legend(color="collected")
)
