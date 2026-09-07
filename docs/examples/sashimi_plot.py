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
# Add a slider to hide junctions supported by fewer reads.
min_uniquely_mapped_reads = gs.param(
    "minUniquelyMappedReads",
    value=1,
    bind=gs.binding_range(
        min=0,
        max=200,
        step=1,
        name="Min uniquely mapped reads",
    ),
)

DOMAIN = [
    {"chrom": "chr15", "pos": 92925000},
    {"chrom": "chr15", "pos": 92949000},
]

# Show read coverage in grey, loading only the region being viewed.
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

# Connect splice junctions with arcs: longer spans rise higher, and more reads
# make the lines thicker.
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

# Label each arc with its supporting read count.
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

# Load junction positions and apply the slider's minimum read count.
splice_junctions = (
    gs.layer(arc_layer, label_layer)
    .properties(
        name="splice-junctions",
        data=gs.Data(
            url="https://raw.githubusercontent.com/igvteam/igv-data/refs/heads/main/data/test/splice_junctions/splice_junction_track_test_cases_sampleA.chr15-92835700-93031800.SJ.out.bed",
            format=gs.data_format(type="bed"),
        ),
    )
    .transform_filter(gs.datum.score >= min_uniquely_mapped_reads)
    .transform_formula(expr=gs.datum.chromEnd - gs.datum.chromStart, as_="span")
    # Vary arc heights slightly to help separate nearby junctions.
    .transform_formula(
        expr=gs.datum.span + (gs.datum.span % 10 - 5) / 10 * gs.datum.span,
        as_="span",
    )
)

# Draw the arcs over the coverage and attach the slider.
chart = (
    gs.layer(coverage, splice_junctions)
    .properties(
        assembly="hg38",
        title="Sashimi plot",
        description=(
            "A sashimi-style splice junction view adapted from the GenomeSpy "
            "docs, using lazy BigWig coverage and splice-junction arcs."
        ),
        scales=gs.scales(x=gs.Scale(domain=DOMAIN)),
    )
    .add_params(min_uniquely_mapped_reads)
    .resolve_scale(y="independent")
    .resolve_axis(y="independent")
)
