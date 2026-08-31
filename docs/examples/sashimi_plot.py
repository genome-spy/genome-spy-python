"""Sashimi plot.

A splice-junction view with coverage in the background and arc links connecting
junction endpoints. Labels on the arcs show junction support while the signal
track keeps local expression context visible.
"""

from __future__ import annotations

import genome_spy as gs

META = {
    "category": "Genome browser tracks",
    "order": 20,
    "height": 360,
    "max_width": 920,
}

DOMAIN = [
    {"chrom": "chr15", "pos": 92925000},
    {"chrom": "chr15", "pos": 92949000},
]

# Coverage is a standard signal track; the BigWig stays lazy so the same pattern
# works for larger loci too.
coverage = (
    gs.Chart(
        gs.lazy.bigwig(
            "https://raw.githubusercontent.com/igvteam/igv-data/refs/heads/main/data/test/splice_junctions/splice_junction_track_test_cases_sampleA.chr15-92835700-93031800.bigWig",
            pixelsPerBin=1,
        )
    )
    .mark_rect(color="lightgray", minWidth=0.5, minOpacity=1, tooltip=None)
    .transform_filter(gs.datum.score > 0)
    .encode(
        x=gs.Locus("chrom", "start"),
        x2=gs.Locus("chrom", "end"),
        y=gs.Y("score:Q").scale(nice=True, zero=False, reverse=False).title("Coverage"),
    )
    .properties(name="coverage")
)

# Junction arcs and their count labels share a derived span metric so the arc
# height reflects intron length while stroke width reflects read support.
arc_layer = (
    gs.Chart()
    .mark_link(linkShape="dome", maxChordLength=100000000)
    .encode(
        x=gs.Locus("chrom", "chromStart", band=0),
        x2=gs.Locus("chrom", "chromEnd", band=0),
        y=gs.Y("span:Q")
        .scale(
            type="sqrt",
            domain=gs.expr("[0, span(domain('x')) * height / width * 5]"),
            reverse=False,
        )
        .axis(None),
        size=gs.Size("score:Q").scale(type="sqrt", range=[0.1, 2.0]),
    )
    .properties(name="arcs")
)

label_layer = (
    gs.Chart()
    .mark_text(dy=-8, tooltip=False)
    .transform_formula(
        expr=(gs.datum.chromEnd + gs.datum.chromStart) / 2,
        as_="center",
    )
    .encode(
        x=gs.Locus("chrom", "center"),
        y=gs.Y("span:Q").scale(reverse=False),
        text=gs.Text("score:Q"),
    )
    .properties(name="labels")
)

# The BED-based splice junctions are filtered by a bound parameter so the reader
# can interactively remove low-support junctions.
splice_junctions = (
    gs.layer(arc_layer, label_layer)
    .properties(
        name="splice-junctions",
        data=gs.Data(
            url="https://raw.githubusercontent.com/igvteam/igv-data/refs/heads/main/data/test/splice_junctions/splice_junction_track_test_cases_sampleA.chr15-92835700-93031800.SJ.out.bed",
            format=gs.data_format(type="bed"),
        ),
    )
    .transform_filter("datum.score >= minUniquelyMappedReads")
    .transform_formula(expr=gs.datum.chromEnd - gs.datum.chromStart, as_="span")
    .transform_formula(
        expr=gs.datum.span + (gs.datum.span % 10 - 5) / 10 * gs.datum.span,
        as_="span",
    )
)

# Overlay the coverage signal with splice-junction arcs on the same locus window.
chart = (
    gs.layer(coverage, splice_junctions)
    .properties(
        assembly="hg38",
        title="Sashimi plot",
        description=(
            "A sashimi-style splice junction view adapted from the GenomeSpy "
            "docs, using lazy BigWig coverage and splice-junction arcs."
        ),
        params=[
            gs.param(
                "minUniquelyMappedReads",
                value=1,
                bind={
                    "input": "range",
                    "min": 0,
                    "max": 200,
                    "step": 1,
                    "name": "Min uniquely mapped reads",
                },
            )
        ],
        scales=gs.scales(x=gs.Scale(domain=DOMAIN)),
    )
    .resolve_scale(y="independent")
    .resolve_axis(y="independent")
)
