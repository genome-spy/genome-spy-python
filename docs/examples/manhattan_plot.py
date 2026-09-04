"""Manhattan plot.

Genome-wide association hits on a locus-aware chromosome axis. Alternating
chromosome colors separate the blocks, dashed rules mark significance
thresholds, and the strongest peaks are outlined for emphasis.
"""

import genome_spy as gs
from genome_spy.datasets._hapmap import hapmap_manhattan_data
from genome_spy.schema import GenomeAxis, Scale

META = {
    "category": "Association plots",
    "order": 10,
    "height": 500,
    "max_width": 980,
}

GENOME_WIDE_P = 5e-8
SUGGESTIVE_P = 1e-5


data, _top_hits, domains = hapmap_manhattan_data(
    genome_wide_p=GENOME_WIDE_P,
    suggestive_p=SUGGESTIVE_P,
)

# --- Visualization -------------------------------------------------------------

chrom_colors = Scale().range(["#5b8fd6", "#8f98a3"])

axis = (
    GenomeAxis()
    .title("Genomic position")
    .chromGrid(True)
    .chromGridOpacity(0.14)
    .chromGridFillEven("#f4f6fb")
    .chromGridFillOdd("#ffffff")
    .chromLabels(True)
    .chromLabelFontSize(11)
    .chromTicks(True)
    .chromTickSize(10)
    .labelFontSize(10)
    .grid(False)
)

points = (
    gs.Chart()
    .mark_point(size=20, filled=True, opacity=0.82)
    .encode(
        x=gs.Locus("chrom", "BP").scale(assembly="hg18").axis(axis),
        y=gs.Y("neglog:Q")
        .scale(reverse=False, domain=domains["y_domain"])
        .title("−log10 p"),
        color=gs.Color("chrom_group:N")
        .scale(chrom_colors)
        .legend(title="Chromosome group"),
    )
)

genome_wide_rule = (
    gs.Chart([{}])
    .transform_formula(
        expr=gs.Expression("manhattanSignificanceCutoff"), as_="threshold"
    )
    .mark_rule(strokeDash=[6, 4], size=1.4, color="#c53b2c")
    .encode(
        y=gs.Y("threshold:Q")
        .scale(reverse=False, domain=domains["y_domain"])
        .title("−log10 p")
    )
)

suggestive_rule = (
    gs.Chart([{"threshold": domains["suggestive_y"]}])
    .mark_rule(strokeDash=[2, 4], size=1.2, color="#d48b31")
    .encode(
        y=gs.Y("threshold:Q")
        .scale(reverse=False, domain=domains["y_domain"])
        .title("−log10 p")
    )
)

highlight_points = (
    gs.Chart()
    .transform_filter(gs.Expression("datum.neglog >= manhattanSignificanceCutoff"))
    .mark_point(
        size=48,
        filled=True,
        color="#c53b2c",
        stroke="black",
        strokeWidth=0.5,
    )
    .encode(
        x=gs.Locus("chrom", "BP").scale(assembly="hg18"),
        y=gs.Y("neglog:Q")
        .scale(reverse=False, domain=domains["y_domain"])
        .title("−log10 p"),
    )
)

association_track = genome_wide_rule + suggestive_rule + points + highlight_points

chart = association_track.properties(
    assembly="hg18",
    title="HapMap genome-wide association scan",
    data=data,
    params=[
        gs.param(
            "manhattanSignificanceCutoff",
            value=round(domains["genome_wide_y"], 1),
            bind={
                "input": "range",
                "min": 3,
                "max": domains["y_domain"][1],
                "step": 0.1,
                "name": "−log10 p cutoff: ",
            },
        )
    ],
    description=(
        "A Manhattan plot with a locus-aware chromosome axis and an "
        "interactive significance threshold."
    ),
)
