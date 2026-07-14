"""BAM read alignments.

A lazy BAM alignment example adapted from the GenomeSpy docs, combining a
coverage track with piled-up read rectangles over a small hg18 locus.
"""

from __future__ import annotations

import genome_spy as gs

META = {
    "category": "Genome browser tracks",
    "tags": ("bam", "coverage", "pileup", "lazy", "vconcat", "real-data"),
    "order": 26,
    "height": 360,
    "max_width": 920,
}

domain = [
    {"chrom": "chr21", "pos": 33037317},
    {"chrom": "chr21", "pos": 33039137},
]

# The upper panel derives a simple coverage histogram directly from the BAM reads.
coverage = (
    gs.Chart()
    .mark_rect()
    .transform(
        {
            "type": "coverage",
            "start": "start",
            "end": "end",
            "as": "coverage",
            "chrom": "chrom",
        }
    )
    .encode(
        x=gs.Locus("chrom", "start", axis=None),
        x2=gs.Locus("chrom", "end"),
        y=gs.Y("coverage:Q").scale(reverse=False),
    )
    .properties(height=40)
)

# The lower panel piles reads into lanes and colors them by strand.
alignments = (
    gs.Chart()
    .mark_rect()
    .transform_pileup(start="start", end="end", as_="_lane")
    .encode(
        x=gs.Locus("chrom", "start", axis={}),
        x2=gs.Locus("chrom", "end"),
        y=gs.Y("_lane", type="index").scale(
            domain=[0, 60], padding=0.3, reverse=True, zoom=False
        ),
        color=gs.Color("strand:N").scale(
            domain=["+", "-"], range=["crimson", "orange"]
        ),
    )
)

# A shared lazy BAM source drives both panels, giving the example the familiar
# browser pattern of coverage above per-read alignments.
chart = gs.vconcat(coverage, alignments, spacing=5).properties(
    assembly="hg18",
    title="BAM read alignments",
    description=(
        "A lazy BAM alignment example adapted from the GenomeSpy docs, with "
        "coverage above piled-up reads."
    ),
    data=gs.lazy.bam(
        "https://data.genomespy.app/sample-data/bamExample.bam",
        windowSize=30000,
    ),
    scales={"x": {"domain": domain}},
    resolve={"scale": {"x": "shared"}},
    config={"view": {"stroke": "lightgray"}},
)
