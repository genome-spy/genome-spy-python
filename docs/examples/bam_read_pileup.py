"""BAM coverage and read pileup.

Load a genomic window from an indexed BAM file and stack its reads by strand.
"""

import genome_spy as gs

META = {"category": "Read alignments and RNA splicing", "order": 25, "height": 520}

# Change the space between read rows without reloading the data.
lane_height = gs.param(
    "laneHeight",
    value=12,
    bind=gs.binding_range(min=2, max=30, step=1, name="Row height: "),
)

# Count overlapping read spans at each position.
coverage = (
    gs.Chart()
    .transform_coverage(start="start", end="end", chrom="chrom", as_="coverage")
    .mark_rect()
    .encode(
        x=gs.Locus("chrom", "start"),
        x2=gs.Locus("chrom", "end"),
        y=gs.Y("coverage:Q").axis(tickCount=2),
    )
    .properties(height=40)
)

# Put overlapping reads on separate rows and show their direction with arrows.
reads = (
    gs.Chart()
    .transform_pileup(start="start", end="end", as_="_lane")
    .mark_arrow(style="arrow-block", minStemLength=10)
    .encode(
        x=gs.Locus("chrom", "start").axis(),
        x2=gs.Locus("chrom", "end"),
        y=gs.Y("_lane:I").scale(padding=0.2, reverse=True, zoom=False),
        color=gs.Color("strand:N").scale(
            domain=["+", "-"], range=["crimson", "orange"]
        ),
        direction=gs.Direction("strand:N").scale(
            domain=["+", "-"], range=["forward", "reverse"]
        ),
    )
    # Scroll through the pileup when the rows exceed the available space.
    .properties(height=gs.Step(step=lane_height), viewportHeight="container")
)

# Both tracks share the visible region and the same lazily loaded reads.
chart = (
    (coverage & reads)
    .properties(
        assembly="hg18",
        data=gs.lazy.bam(
            "https://data.genomespy.app/sample-data/bamExample.bam", windowSize=30000
        ),
        scales=gs.scales(
            x=gs.Scale(
                domain=[
                    {"chrom": "chr21", "pos": 33037317},
                    {"chrom": "chr21", "pos": 33039137},
                ]
            )
        ),
        spacing=5,
    )
    .add_params(lane_height)
    .resolve_axis(x="shared")
    .configure_view(stroke="lightgray")
)
