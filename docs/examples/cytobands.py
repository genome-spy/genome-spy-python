"""Chromosome ideogram.

A whole-genome cytoband ideogram with band labels and chromosome separators.
Intervals are colored by stain to show familiar light, dark, centromeric, and
other structural band types.
"""

from __future__ import annotations

import genome_spy as gs

META = {
    "category": "Reference annotation tracks",
    "tags": ("cytobands", "ideogram", "locus", "layer", "real-data"),
    "order": 5,
    "height": 120,
    "max_width": 920,
}

stain_domain = [
    "gneg",
    "gpos25",
    "gpos50",
    "gpos75",
    "gpos100",
    "acen",
    "stalk",
    "gvar",
]

# The ideogram itself is just a whole-genome interval track colored by cytoband stain.
band_layer = (
    gs.Chart()
    .mark_rect()
    .encode(
        color=gs.Color("gieStain:N")
        .scale(
            domain=stain_domain,
            range=[
                "#f0f0f0",
                "#e0e0e0",
                "#d0d0d0",
                "#c0c0c0",
                "#a0a0a0",
                "#cc4444",
                "#338833",
                "#000000",
            ],
        )
        .legend(None)
    )
    .properties(title="Cytoband")
)

label_layer = (
    gs.Chart()
    .mark_text(
        align="center",
        baseline="middle",
        paddingX=4,
        tooltip=None,
    )
    .encode(
        color=gs.Color("gieStain:N")
        .scale(
            domain=stain_domain,
            range=[
                "black",
                "black",
                "black",
                "black",
                "black",
                "black",
                "white",
                "white",
            ],
        )
        .legend(None),
        text=gs.Text("name:N"),
    )
)

# Add dashed separators at chromosome starts to make whole-genome navigation easier.
separator_layer = (
    gs.Chart()
    .encode(x2=None)
    .mark_rule(color="#a0a0a0", strokeDash=[3, 3], strokeDashOffset=2)
    .transform_filter("datum.chromStart == 0 && datum.chrom != 'chr1'")
)

# The shared encoding lives on the layered root so each sublayer inherits the
# same genome-wide interval coordinates.
chart = (
    gs.layer(band_layer, label_layer, separator_layer)
    .properties(
        assembly="hg38",
        name="ideogram-track",
        title=gs.title("Chromosome Ideogram", style="track-title"),
        description=(
            "A whole-genome ideogram showing hg38 cytobands and chromosome boundaries."
        ),
        height=24,
        data=gs.Data(
            url="https://data.genomespy.app/genomes/hg38/cytoBand.txt.gz",
            format=gs.data_format(
                type="tsv",
                columns=["chrom", "chromStart", "chromEnd", "name", "gieStain"],
            ),
        ),
    )
    .encode(
        x=gs.Locus("chrom", "chromStart"),
        x2=gs.Locus("chrom", "chromEnd"),
    )
    .transform_filter("!test(/_/, datum.chrom)")
    .resolve_scale(color="independent")
    .configure_view(stroke="black")
)
