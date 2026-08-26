"""PIK3CA mutation lollipop plot.

Recurrent TCGA-BRCA PIK3CA mutations are displaced just enough to keep dense
hotspots readable while connectors retain their true protein positions.
"""

import genome_spy as gs

META = {
    "category": "Mutation position plots",
    "order": 12,
    "height": 400,
    "max_width": 980,
}

PROTEIN_LENGTH = 1068
LABEL_HEIGHT = 65
CONNECTOR_HEIGHT = 20
PROTEIN_HEIGHT = 50
DISPLACEMENT_LENGTH = 18

MUTATIONS = [
    {
        "position": 81,
        "mutation": "E81K",
        "sampleCount": 2,
        "variantClass": "Missense_Mutation",
        "sourceProteinPosition": "81/1068",
    },
    {
        "position": 88,
        "mutation": "R88Q",
        "sampleCount": 2,
        "variantClass": "Missense_Mutation",
        "sourceProteinPosition": "88/1068",
    },
    {
        "position": 108,
        "mutation": "R108H",
        "sampleCount": 2,
        "variantClass": "Missense_Mutation",
        "sourceProteinPosition": "108/1068",
    },
    {
        "position": 110,
        "mutation": "E110del",
        "sampleCount": 2,
        "variantClass": "In_Frame_Del",
        "sourceProteinPosition": "109/1068",
    },
    {
        "position": 111,
        "mutation": "K111del",
        "sampleCount": 2,
        "variantClass": "In_Frame_Del",
        "sourceProteinPosition": "111/1068",
    },
    {
        "position": 118,
        "mutation": "G118D",
        "sampleCount": 5,
        "variantClass": "Missense_Mutation",
        "sourceProteinPosition": "118/1068",
    },
    {
        "position": 345,
        "mutation": "N345K",
        "sampleCount": 17,
        "variantClass": "Missense_Mutation",
        "sourceProteinPosition": "345/1068",
    },
    {
        "position": 366,
        "mutation": "P366R",
        "sampleCount": 2,
        "variantClass": "Missense_Mutation",
        "sourceProteinPosition": "366/1068",
    },
    {
        "position": 420,
        "mutation": "C420R",
        "sampleCount": 4,
        "variantClass": "Missense_Mutation",
        "sourceProteinPosition": "420/1068",
    },
    {
        "position": 447,
        "mutation": "P447_L455del",
        "sampleCount": 3,
        "variantClass": "In_Frame_Del",
        "sourceProteinPosition": "446-455/1068",
    },
    {
        "position": 453,
        "mutation": "E453K",
        "sampleCount": 7,
        "variantClass": "Missense_Mutation",
        "sourceProteinPosition": "453/1068",
    },
    {
        "position": 542,
        "mutation": "E542K",
        "sampleCount": 41,
        "variantClass": "Missense_Mutation",
        "sourceProteinPosition": "542/1068",
    },
    {
        "position": 545,
        "mutation": "E545A",
        "sampleCount": 5,
        "variantClass": "Missense_Mutation",
        "sourceProteinPosition": "545/1068",
    },
    {
        "position": 545,
        "mutation": "E545K",
        "sampleCount": 67,
        "variantClass": "Missense_Mutation",
        "sourceProteinPosition": "545/1068",
    },
    {
        "position": 546,
        "mutation": "Q546K",
        "sampleCount": 4,
        "variantClass": "Missense_Mutation",
        "sourceProteinPosition": "546/1068",
    },
    {
        "position": 546,
        "mutation": "Q546R",
        "sampleCount": 6,
        "variantClass": "Missense_Mutation",
        "sourceProteinPosition": "546/1068",
    },
    {
        "position": 726,
        "mutation": "E726K",
        "sampleCount": 8,
        "variantClass": "Missense_Mutation",
        "sourceProteinPosition": "726/1068",
    },
    {
        "position": 939,
        "mutation": "D939G",
        "sampleCount": 2,
        "variantClass": "Missense_Mutation",
        "sourceProteinPosition": "939/1068",
    },
    {
        "position": 1004,
        "mutation": "M1004I",
        "sampleCount": 3,
        "variantClass": "Missense_Mutation",
        "sourceProteinPosition": "1004/1068",
    },
    {
        "position": 1007,
        "mutation": "G1007R",
        "sampleCount": 2,
        "variantClass": "Missense_Mutation",
        "sourceProteinPosition": "1007/1068",
    },
    {
        "position": 1043,
        "mutation": "M1043I",
        "sampleCount": 2,
        "variantClass": "Missense_Mutation",
        "sourceProteinPosition": "1043/1068",
    },
    {
        "position": 1044,
        "mutation": "N1044Y",
        "sampleCount": 2,
        "variantClass": "Missense_Mutation",
        "sourceProteinPosition": "1044/1068",
    },
    {
        "position": 1047,
        "mutation": "H1047L",
        "sampleCount": 13,
        "variantClass": "Missense_Mutation",
        "sourceProteinPosition": "1047/1068",
    },
    {
        "position": 1047,
        "mutation": "H1047R",
        "sampleCount": 120,
        "variantClass": "Missense_Mutation",
        "sourceProteinPosition": "1047/1068",
    },
    {
        "position": 1047,
        "mutation": "H1047Y",
        "sampleCount": 2,
        "variantClass": "Missense_Mutation",
        "sourceProteinPosition": "1047/1068",
    },
    {
        "position": 1049,
        "mutation": "G1049R",
        "sampleCount": 2,
        "variantClass": "Missense_Mutation",
        "sourceProteinPosition": "1049/1068",
    },
]
DOMAINS = [
    {"start": 16, "end": 105, "label": "ABD", "description": "PI3K-ABD"},
    {"start": 187, "end": 289, "label": "RBD", "description": "PI3K-RBD"},
    {"start": 330, "end": 487, "label": "C2", "description": "C2 PI3K-type"},
    {"start": 517, "end": 694, "label": "Helical", "description": "PIK helical"},
    {
        "start": 765,
        "end": 1051,
        "label": "Kinase",
        "description": "PI3K/PI4K catalytic",
    },
]

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
# protein coordinate used by the domain track.
mutation_view = (
    gs.vconcat(
        mutation_labels,
        mutation_marks,
        gs.layer(connectors, anchors).properties(height=CONNECTOR_HEIGHT),
        spacing=0,
    )
    .properties(
        data=gs.Data(name="mutations"),
        resolve={"scale": {"color": "shared"}, "legend": {"color": "shared"}},
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
    .transform_formula(expr="proteinLength", as_="end")
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

# pixelsPerResidue lets the displacement transform adapt when the chart width
# changes.
chart = (
    gs.vconcat(mutation_view, protein, spacing=0)
    .properties(
        title="PIK3CA mutations in TCGA-BRCA",
        padding=10,
        description="Recurrent protein-altering PIK3CA mutations in TCGA-BRCA. Heights and labels show distinct tumor sample counts.",
        datasets={"mutations": MUTATIONS, "domains": DOMAINS},
        scales={"x": {"domainMin": 1, "nice": False}},
        params=[
            gs.param("proteinLength", value=PROTEIN_LENGTH),
            gs.param("lineWidth", value=1),
            gs.param(
                "pixelsPerResidue", expr="width * (scale('x', 1) - scale('x', 0))"
            ),
        ],
    )
    .resolve_scale(x="shared")
)
