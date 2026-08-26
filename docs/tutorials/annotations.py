"""Single-source chart objects used by the annotations guide."""

import genome_spy as gs
from genome_spy.datasets._annotations import refseq_gene_bodies


# annotations-points-start
points = [
    {"gene": "A", "effect": -1.8, "significance": 2.1},
    {"gene": "B", "effect": -0.7, "significance": 1.2},
    {"gene": "C", "effect": 0.2, "significance": 0.7},
    {"gene": "D", "effect": 1.1, "significance": 1.5},
    {"gene": "E", "effect": 2.0, "significance": 2.8},
]

annotations = [
    {
        "gene": "A",
        "effect": -1.8,
        "significance": 2.1,
        "label_x": -2.15,
        "label_y": 2.65,
    },
    {
        "gene": "E",
        "effect": 2.0,
        "significance": 2.8,
        "label_x": 1.55,
        "label_y": 3.35,
    },
]

point_marks = (
    gs.Chart(points)
    .mark_point(filled=True, size=80)
    .encode(
        x=gs.X("effect:Q").title("Effect"),
        y=gs.Y("significance:Q").title("Significance"),
    )
)

leader_lines = (
    gs.Chart(annotations)
    .mark_rule(color="#555", size=1)
    .encode(
        x=gs.X("effect:Q").title("Effect"),
        x2="label_x",
        y=gs.Y("significance:Q").title("Significance"),
        y2="label_y",
    )
)

point_labels = (
    gs.Chart(annotations)
    .mark_text(baseline="bottom", yOffset=-3, fontWeight="bold")
    .encode(
        x=gs.X("label_x:Q").title("Effect"),
        y=gs.Y("label_y:Q").title("Significance"),
        text="gene:N",
    )
)

point_annotation_chart = (point_marks + leader_lines + point_labels).properties(
    title="Selected observations with leader-line labels"
)
# annotations-points-end


# annotations-genes-start
GENE_REGION = [
    {"chrom": "chr8", "pos": 97_850_000},
    {"chrom": "chr8", "pos": 99_000_000},
]
genes = refseq_gene_bodies("hg19")

gene_tooltip = [
    gs.Tooltip("symbol:N").title("Gene"),
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
        clip=False,
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

gene_annotation_track = (
    (gene_bodies + gene_labels)
    .properties(
        assembly="hg19",
        data=genes,
        scales=gs.scales(x=gs.Scale(domain=GENE_REGION)),
        title=gs.title("RefSeq gene annotations", orient="left"),
        height=gs.step(24),
        axes=gs.axes(x=gs.GenomeAxis(title="Genomic position")),
    )
    .encode(
        y=gs.Y("lane:O")
        .scale(
            type="index",
            domain=[0, 3],
            reverse=True,
            align=0,
            paddingInner=0.4,
            paddingOuter=0.2,
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
    .transform_filter("datum.lane < 3")
)
# annotations-genes-end


CHARTS = {
    "point_annotation_chart": point_annotation_chart,
    "gene_annotation_track": gene_annotation_track,
}
