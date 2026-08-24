"""Rainfall plot.

Inter-mutation distance across the genome for a single tumor sample. Point
color encodes substitution class and arrow annotations call out compact
kataegis-like clusters.
"""

from __future__ import annotations

import genome_spy as gs
from genome_spy.datasets._mutation import brca_rainfall_data
from genome_spy.schema import GenomeAxis, Legend, Scale

META = {
    "category": "Mutation position plots",
    "order": 18,
    "height": 420,
    "max_width": 980,
}

CONVERSION_ORDER = ["C>T", "C>G", "C>A", "T>C", "T>A", "T>G"]
CONVERSION_COLORS = ["#f64b3c", "#4f63c9", "#2891e8", "#f6b617", "#4caf50", "#f7931a"]


data = brca_rainfall_data()
points = data["points"]
change_points = data["change_points"]
y_domain = [0.0, data["y_max"]]
sample_name = data["sample"]
assembly = data["reference_build"]

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
        x=gs.Locus("chrom", "pos").scale(assembly=assembly).axis(axis),
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
        x=gs.Locus("chrom", "start").scale(assembly=assembly),
        y=gs.Y(gs.datum(0), type="quantitative")
        .scale(reverse=False, domain=y_domain)
        .title("log10 inter-event distance"),
        y2=gs.Y2("arrow_y:Q"),
    )
)

change_point_heads = (
    gs.Chart(change_points)
    .mark_point(shape="triangle-up", size=60, filled=True, color="#111111")
    .encode(
        x=gs.Locus("chrom", "start").scale(assembly=assembly),
        y=gs.Y("arrow_y:Q").scale(reverse=False, domain=y_domain),
    )
)

chart = (rainfall_points + change_point_stems + change_point_heads).properties(
    title=sample_name,
    description=(
        "A rainfall plot with substitution classes and arrowed change-point "
        "annotations for compact mutation clusters."
    ),
)
