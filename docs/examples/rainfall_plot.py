"""Rainfall plot.

Inter-mutation distance across the genome for a single tumor sample. Point
color encodes substitution class and arrow annotations call out compact
kataegis-like clusters.
"""

from __future__ import annotations

import genome_spy as gs
from genome_spy.datasets._annotations import refseq_gene_bodies
from genome_spy.datasets._mutation import brca_rainfall_data
from genome_spy.schema import GenomeAxis, Legend, Scale

META = {
    "category": "Mutation position plots",
    "order": 18,
    "height": 500,
}

CONVERSION_ORDER = ["C>T", "C>G", "C>A", "T>C", "T>A", "T>G"]
CONVERSION_COLORS = ["#f64b3c", "#4f63c9", "#2891e8", "#f6b617", "#4caf50", "#f7931a"]
REGION = [
    {"chrom": "chr8", "pos": 97_900_000},
    {"chrom": "chr8", "pos": 99_000_000},
]


data = brca_rainfall_data()
points = data["points"]
change_points = data["change_points"]
y_domain = [0.0, data["y_max"]]
sample_name = data["sample"]
assembly = data["reference_build"]
genes = refseq_gene_bodies(assembly)

axis = (
    GenomeAxis()
    .title("Genomic position")
    .chromGrid(True)
    .chromGridOpacity(0.16)
    .chromGridFillEven("#f5f7fb")
    .chromGridFillOdd("#ffffff")
    .chromLabels(True)
    .chromLabelFontSize(11)
    .chromTicks(True)
    .grid(False)
)

mutation_scale = Scale().domain(CONVERSION_ORDER).range(CONVERSION_COLORS)
mutation_legend = (
    Legend()
    .orient("bottom")
    .direction("horizontal")
    .columns(3)
    .symbolSize(80)
    .title("Substitution class")
)

# --- Visualization -------------------------------------------------------------

rainfall_points = (
    gs.Chart(points)
    .mark_point(size=18, filled=True, opacity=0.95)
    .encode(
        x=gs.Locus("chrom", "pos", offset=1),
        y=gs.Y("log10_distance:Q")
        .scale(reverse=False, domain=y_domain)
        .title("log10 inter-event distance"),
        color=gs.Color("con_class:N").scale(mutation_scale).legend(mutation_legend),
    )
)

change_point_stems = (
    gs.Chart(change_points)
    .mark_rule(color="#111111", size=1.2)
    .encode(
        x=gs.Locus("chrom", "start", offset=1),
        y=gs.Y(gs.datum(0), type="quantitative")
        .scale(reverse=False, domain=y_domain)
        .title("log10 inter-event distance"),
        y2=gs.Y2("arrow_y"),
    )
)

change_point_heads = (
    gs.Chart(change_points)
    .mark_point(shape="triangle-up", size=60, filled=True, color="#111111")
    .encode(
        x=gs.Locus("chrom", "start", offset=1),
        y=gs.Y("arrow_y:Q").scale(reverse=False, domain=y_domain),
    )
)

rainfall_track = (rainfall_points + change_point_stems + change_point_heads).properties(
    name="rainfall-track",
    title=sample_name,
    height=300,
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

gene_track = (
    (gene_bodies + gene_labels)
    .properties(
        name="refseq-genes",
        data=genes,
        title=gs.title("RefSeq genes", orient="left", offset=8),
        height=gs.step(24),
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

chart = (
    (rainfall_track & gene_track)
    .properties(
        assembly=assembly,
        width="container",
        scales=gs.scales(x=gs.Scale(domain=REGION)),
        axes=gs.axes(x=axis),
        spacing=8,
        description=(
            "A regional rainfall plot with substitution classes, arrowed "
            "change-point annotations, and aligned RefSeq gene bodies."
        ),
    )
    .resolve_scale(x="shared", y="independent")
    .resolve_axis(x="shared", y="independent")
    .configure_view(stroke="lightgray")
)
