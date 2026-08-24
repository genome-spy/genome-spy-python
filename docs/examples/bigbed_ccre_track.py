"""BigBed cCRE track.

A regulatory-annotation track built from BigBed intervals. Candidate elements
are drawn as locus spans and colored by their annotation class.
"""

from __future__ import annotations

import genome_spy as gs

META = {
    "category": "Reference annotation tracks",
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
            "A regulatory annotation track showing candidate cis-regulatory "
            "elements over a focused locus."
        ),
        scales=gs.scales(
            x=gs.Scale(
                domain=[
                    {"chrom": "chr7", "pos": 66600000},
                    {"chrom": "chr7", "pos": 66800000},
                ]
            )
        ),
    )
    .configure_view(stroke="lightgray")
)
