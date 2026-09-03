"""TCGA ovarian cancer GISTIC landscape.

Recurrent copy-number scores and their amplification and deletion peaks are
shown over a shared hg19 genomic axis.
"""

import genome_spy as gs
from genome_spy.datasets._annotations import refseq_gene_bodies
from genome_spy.datasets._gistic import tcga_ov_gistic_data

META = {
    "category": "Copy-number plots",
    "order": 36,
    "height": 400,
    "max_width": 980,
}

GENOME_DOMAIN = [{"chrom": "chr1"}, {"chrom": "chrY"}]

event_colors = gs.Scale(
    domain=["Amp", "Del"],
    range=["#e45756", "#4c78a8"],
)

data = tcga_ov_gistic_data()
genes = refseq_gene_bodies("hg19")

# Negating deletion scores places amplifications and deletions on opposite sides
# of the shared zero line.
zero_line = (
    gs.Chart([{"value": 0}])
    .mark_rule(color="black", opacity=0.3)
    .encode(y=gs.Y("value:Q").title(None))
    .properties(name="zero-line")
)

q_values = (
    gs.Chart(data["scores"])
    .transform_formula(
        expr=gs.datum["-log10(q-value)"] * gs.expr.if_(gs.datum.Type == "Del", -1, 1),
        as_="-log10(q-value)",
    )
    .mark_rect(minOpacity=1)
    .encode(
        x=gs.Locus("Chromosome", "Start"),
        x2=gs.Locus("Chromosome", "End"),
        y=gs.Y("-log10(q-value):Q"),
        color=gs.Color("Type:N").scale(event_colors),
    )
    .properties(name="q-value-rects")
)

thresholds = (
    gs.Chart([{"value": 0.602}, {"value": -0.602}])
    .mark_rule(strokeDash=[3, 1], color="black", opacity=0.3)
    .encode(y=gs.Y("value:Q").title(None))
    .properties(name="q-value-thresholds")
)

score_track = gs.layer(zero_line, q_values, thresholds).properties(
    name="gistic-q-value",
    title=gs.Title(
        text="GISTIC q-values from the TCGA OV-TP cohort",
        style="overlay-title",
    ),
)

# GISTIC stores wide peak, peak, and region limits in separate columns. Fold
# them into rows so one rule layer can draw all three interval types.
lesion_track = (
    gs.Chart(data["lesions"])
    .transform_regex_extract(
        field="Unique Name",
        regex=r"^(Amplification|Deletion) Peak[ ]+\d+$",
        as_=["Type"],
        skipInvalidInput=True,
    )
    .transform_filter(gs.datum.Type)
    .transform_regex_fold(
        columnRegex=[r"^(.*) Limits$"],
        asValue=["limits"],
        asKey="Segment type",
    )
    .transform_regex_extract(
        field="limits",
        regex=r"^(chr[^:]+):(\d+)-(\d+)",
        as_=["Chrom", "Start", "End"],
    )
    .transform_project(
        fields=[
            "Segment type",
            "Chrom",
            "Start",
            "End",
            "Type",
            "Descriptor",
            "q values",
        ]
    )
    .mark_rule(minLength=2)
    .encode(
        x=gs.Locus("Chrom", "Start"),
        x2=gs.Locus("Chrom", "End"),
        y=gs.Y("Type:N")
        .scale(domain=["Amplification", "Deletion"], padding=0.2)
        .title(None),
        color=gs.Color("Type:N").scale(
            domain=["Amplification", "Deletion"],
            range=["#e45756", "#4c78a8"],
        ),
        opacity=gs.Opacity("Segment type:N").scale(
            type="ordinal",
            domain=["Wide Peak", "Peak", "Region"],
            range=[0.3, 1, 0.3],
        ),
        size=gs.Size("Segment type:N").scale(
            type="ordinal",
            domain=["Wide Peak", "Peak", "Region"],
            range=[11, 15, 2],
        ),
    )
    .properties(
        name="gistic-all-lesions",
        title=gs.Title(text="Regions and peaks", orient="none"),
        height=gs.step(20),
    )
)

gene_tooltip = [
    gs.Tooltip("symbol:N").title("Gene"),
    gs.Tooltip("identifier:N").title("RefSeq locus"),
    gs.Tooltip("chrom:N").title("Chromosome"),
    gs.Tooltip("start:Q").title("Start").format(",d"),
    gs.Tooltip("end:Q").title("End").format(",d"),
    gs.Tooltip("strand:N").title("Strand"),
]

gene_bodies = (
    gs.Chart()
    .mark_arrow(
        style="arrow-block",
        fill="#d5d9de",
        stroke="#59636e",
        strokeWidth=1,
        yOffset=5,
        size=7,
        tooltip=gs.HandledTooltip(handler="default"),
    )
    .encode(
        x=gs.Locus("chrom", "start"),
        x2=gs.Locus("chrom", "end"),
        direction=gs.Direction("strand:N").scale(
            domain=["+", "-"], range=["forward", "reverse"]
        ),
        tooltip=gene_tooltip,
    )
    .properties(
        opacity=gs.dynamic_opacity(unitsPerPixel=[100000, 40000], values=[0, 1])
    )
)

# Label scores only decide which colliding names survive; they do not filter the
# gene bodies themselves.
gene_labels = (
    gs.Chart()
    .transform_measure_text(field="symbol", as_="label_width", fontSize=11)
    .transform_filter_scored_labels(
        pos="linear_start",
        pos2="linear_end",
        asMidpoint="label_position",
        score="score",
        width="label_width",
        lane="lane",
        padding=5,
    )
    .mark_text(
        baseline="middle",
        align="center",
        # Clip labels at the genomic window while keeping the vertical offset
        # free to extend above the gene body.
        clip="x",
        yOffset=-5,
        size=11,
        color="#20262d",
        tooltip=gs.HandledTooltip(handler="default"),
    )
    .encode(
        x=gs.X("label_position:L"),
        text="symbol:N",
        tooltip=gene_tooltip,
    )
)

gene_track = (
    (gene_bodies + gene_labels)
    .properties(
        name="refseq-genes",
        data=genes,
        title=gs.title("RefSeq genes", orient="left"),
        height=gs.step(24),
        padding=gs.Paddings(top=10),
    )
    .encode(
        y=gs.Y("lane:O")
        .scale(
            type="index",
            domain=[0, 3],
            reverse=True,
            align=0,
            paddingInner=0.4,
            paddingOuter=0.5,
            zoom=False,
        )
        .axis(None)
    )
    .transform_linearize_genomic_coordinate(
        chrom="chrom",
        pos=["start", "end"],
        as_=["linear_start", "linear_end"],
    )
    .transform_collect(sort=gs.compare(field=["linear_start", "linear_end"]))
    .transform_pileup(
        start="linear_start",
        end="linear_end",
        as_="lane",
        preference="strand",
        preferredOrder=["-", "+"],
    )
    .transform_filter(gs.datum.lane < 3)
)

# All three tracks share genomic zooming but keep independent vertical scales.
chart = (
    gs.vconcat(score_track, lesion_track, gene_track)
    .properties(
        assembly="hg19",
        name="gistic-track",
        width="container",
        scales=gs.scales(x=gs.Scale(domain=GENOME_DOMAIN)),
        axes=gs.axes(x=gs.GenomeAxis(title="Genomic position")),
        spacing=8,
        description=(
            "TCGA OV-TP GISTIC2 copy-number scores, recurrent lesions, and "
            "aligned RefSeq gene bodies across the hg19 genome."
        ),
    )
    .resolve_scale(x="shared", y="independent")
    .resolve_axis(x="shared", y="independent")
    .configure_legend(disable=True)
    .configure_view(stroke="lightgray")
)
