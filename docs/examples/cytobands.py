"""Chromosome ideogram.

A whole-genome cytoband ideogram with band labels and chromosome separators.
Intervals are colored by stain to show familiar light, dark, centromeric, and
other structural band types.
"""

from __future__ import annotations

import genome_spy as gs

META = {
    "category": "Reference annotation tracks",
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

# Draw chromosome bands in colors matching their stain type.
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

# Label bands, using white text on the darkest backgrounds.
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

# Separate neighboring chromosomes with dashed lines.
separator_layer = (
    gs.Chart()
    .encode(x2=None)
    .mark_rule(color="#a0a0a0", strokeDash=[3, 3], strokeDashOffset=2)
    .transform_filter((gs.datum.chromStart == 0) & (gs.datum.chrom != "chr1"))
)

# Load band positions and combine the colored bands, names, and separators.
chart = (
    gs.layer(band_layer, label_layer, separator_layer)
    .properties(
        assembly="hg38",
        name="ideogram-track",
        title=gs.title("Chromosome Ideogram", style="track-title"),
        description=(
            "A whole-genome ideogram showing hg38 cytobands and chromosome boundaries."
        ),
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
    .transform_filter(~gs.expr.test(gs.expr.regexp("_"), gs.datum.chrom))
    .resolve_scale(color="independent")
    .configure_view(stroke="black")
)
