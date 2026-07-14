"""BigBed cCRE track.

A lazy BigBed annotation track adapted from the GenomeSpy docs, showing ENCODE
candidate cis-regulatory elements over an hg38 locus.
"""

from __future__ import annotations

import genome_spy as gs

META = {
    "category": "Reference annotation tracks",
    "tags": ("bigbed", "ccre", "lazy", "rect", "real-data"),
    "order": 18,
    "height": 180,
    "max_width": 920,
}

# This is the minimal lazy-annotation pattern: load a BigBed source and color
# intervals by their regulatory label over a fixed locus.
chart = (
    gs.Chart(
        gs.lazy.bigbed(
            "https://data.genomespy.app/sample-data/encodeCcreCombined.hg38.bb"
        )
    )
    .mark_rect()
    .encode(
        x=gs.Locus("chrom", "chromStart"),
        x2=gs.Locus("chrom", "chromEnd"),
        color=gs.Color("ucscLabel:N").scale(
            domain=["prom", "enhP", "enhD", "K4m3", "CTCF"],
            range=["#FF0000", "#FFA700", "#FFCD00", "#FFAAAA", "#00B0F0"],
        ),
    )
    .properties(
        assembly="hg38",
        title="BigBed cCRE track",
        description=(
            "An ENCODE candidate cis-regulatory element track adapted from the "
            "GenomeSpy docs."
        ),
        view={"stroke": "lightgray"},
        scales={
            "x": {
                "domain": [
                    {"chrom": "chr7", "pos": 66600000},
                    {"chrom": "chr7", "pos": 66800000},
                ]
            }
        },
    )
)
