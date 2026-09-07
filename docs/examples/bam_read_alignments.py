"""BAM read alignments.

An IGV-like alignment view with depth, mismatch, CIGAR, and read-level tracks.
"""

from __future__ import annotations

import genome_spy as gs

META = {
    "category": "Genome browser tracks",
    "order": 26,
    "height": 600,
    "max_width": 980,
}

# Choose the read details to show on hover.
read_tooltips = [
    gs.Tooltip("name").title("Read"),
    gs.Tooltip("strand").title("Strand"),
    gs.Tooltip("isPaired").title("Paired"),
    gs.Tooltip("isProperPair").title("Proper pair"),
    gs.Tooltip("isDuplicate").title("Duplicate"),
    gs.Tooltip("isQcFail").title("QC fail"),
    gs.Tooltip("isSecondary").title("Secondary"),
    gs.Tooltip("isSupplementary").title("Supplementary"),
    gs.Tooltip("mapq").title("Mapping quality"),
    gs.Tooltip("cigar").title("CIGAR"),
]

# Use the same base colors in the summary and individual reads.
base_colors = gs.Scale(
    domain=["A", "C", "T", "G", "N"],
    range=["#4FBF45", "#4D96E8", "#E85F78", "#E8B322", "#BDBDBD"],
)
# Let the reader adjust row height and filter out lower-quality reads or bases.
LANE_HEIGHT = gs.param(
    "laneHeight",
    value=12,
    bind=gs.binding_range(min=1, max=30, step=1),
    transition={"type": "lerp", "halfLife": 30, "epsilon": 0.02},
)
MIN_MAPQ = gs.param(
    "minMapq",
    value=0,
    bind=gs.binding_range(min=0, max=60, step=1, debounce=100),
)
MIN_BASE_QUALITY = gs.param(
    "minBaseQuality",
    value=0,
    bind=gs.binding_range(min=0, max=40, step=1, debounce=100),
)
# Load reads only when viewing a small enough region.
WINDOW_SIZE = gs.param("windowSize", value=15_000)
ZOOM_MESSAGE_STATE = gs.param(
    "zoomMessageState",
    expr=gs.expr.if_(
        gs.expr.abs(gs.expr.span(gs.expr.domain("x"))) > WINDOW_SIZE,
        1,
        0,
    ),
    transition={"type": "lerp", "halfLife": 60},
)

# Count how many reads cover each position, using the reads shown below.
depth = (
    gs.Chart()
    .transform_flatten_cigar(copyFields=["chrom"])
    .transform_filter(gs.datum.cigarType == "aligned")
    .transform_collect(sort=gs.compare(["chrom", "cigarStart"]))
    .transform_coverage(
        chrom="chrom",
        start="cigarStart",
        end="cigarEnd",
        as_="coverage",
        asStart="start",
        asEnd="end",
    )
    .mark_rect()
    .encode(
        x=gs.Locus("chrom", "start", band=0),
        x2=gs.Locus("chrom", "end", band=0),
        y=gs.Y("coverage:Q").axis(tickCount=2, title="Depth"),
        color=gs.value("#d0d0d0"),
    )
    .properties(name="depth", title="Depth")
)

# Add colored counts for bases that differ from the reference sequence.
mismatch_summary = (
    gs.Chart()
    .transform_filter(gs.datum.md != None)  # noqa: E711
    .transform_alignment_mismatches(copyFields=["chrom"])
    .transform_filter(
        (gs.datum.baseQuality == None)  # noqa: E711
        | (gs.datum.baseQuality >= MIN_BASE_QUALITY)
    )
    .transform_aggregate(groupby=["chrom", "mismatchStart", "base"])
    .transform_stack(
        field="count",
        groupby=["chrom", "mismatchStart"],
        sort=gs.compare("base", order="ascending"),
        as_=["mismatchCount0", "mismatchCount1"],
    )
    .transform_formula(expr=gs.datum.mismatchStart + 1, as_="mismatchEnd")
    .mark_rect()
    .encode(
        x=gs.Locus("chrom", "mismatchStart", band=0),
        x2=gs.Locus("chrom", "mismatchEnd", band=0),
        y=gs.Y("mismatchCount0:Q"),
        y2=gs.Y2("mismatchCount1"),
        color=gs.Color("base:N").scale(base_colors).legend(None),
    )
    .properties(name="mismatch-summary", title="Mismatch support")
)

# Mark positions where reads contain inserted bases.
insertion_summary = (
    gs.Chart()
    .transform_flatten_cigar(copyFields=["chrom"])
    .transform_filter(gs.datum.cigarType == "insertion")
    .transform_aggregate(groupby=["chrom", "cigarStart"])
    .mark_rule(color="black", size=1)
    .encode(
        x=gs.Locus("chrom", "cigarStart", band=0),
        y=gs.datum(0, type="quantitative"),
        y2=gs.Y2("count"),
    )
    .properties(name="insertion-summary", title="Insertion support")
)

# Combine the depth and variant counts into a compact summary track.
coverage = (
    (depth + mismatch_summary + insertion_summary)
    .properties(
        name="coverage",
        title=gs.Title(
            text="Depth and mismatch support",
            style="overlay-title",
            fontSize=11,
        ),
        height=40,
    )
    .resolve_scale(color="independent")
)

# Draw each read as a grey arrow; fade reads with lower mapping quality.
read_backbone = (
    gs.Chart()
    .mark_arrow(
        style="arrow-block",
        minStemLength=10,
        fill="#e0e0e0",
        stroke="#c4c4c4",
        strokeWidth=gs.expr(gs.expr.linearstep(3, 8, LANE_HEIGHT)),
    )
    .encode(
        x=gs.Locus("chrom", "start", band=0),
        x2=gs.Locus("chrom", "end", band=0),
        direction=gs.Direction("strand:N").scale(
            domain=["+", "-"], range=["forward", "reverse"]
        ),
        opacity=gs.Opacity("_mapqOrZero:Q")
        .scale(domain=[0, 60], range=[0.25, 1])
        .legend(
            title="Mapping quality",
            values=[0, 20, 40, 60],
        ),
        tooltip=read_tooltips,
    )
    .properties(name="read-backbone", title="Read alignment")
)

# Show deletions as white gaps crossed by a thin line.
deletions = gs.layer(
    gs.Chart()
    .transform_filter(gs.datum.cigarType == "deletion")
    .mark_rect(color="white", minWidth=1),
    gs.Chart()
    .transform_filter(gs.datum.cigarType == "deletion")
    .mark_rule(color="#222", minLength=1),
)

deletions = deletions.properties(name="deletions", title="Deletion").encode(
    x=gs.Locus("chrom", "cigarStart", band=0),
    x2=gs.Locus("chrom", "cigarEnd", band=0),
)

# Use dashed lines for regions skipped by the alignment.
skips = (
    gs.Chart()
    .transform_filter(gs.datum.cigarType == "skip")
    .mark_rule(color="#6b6b6b", strokeDash=[2, 2], minLength=1)
    .encode(
        x=gs.Locus("chrom", "cigarStart", band=0),
        x2=gs.Locus("chrom", "cigarEnd", band=0),
    )
    .properties(name="skips", title="Skipped region")
)

# Label insertions with "I" and show the inserted sequence on hover.
insertions = (
    gs.Chart()
    .transform_filter(gs.datum.cigarType == "insertion")
    .mark_text(
        text="I",
        color="black",
        size=gs.expr(LANE_HEIGHT * 0.90),
        font="Radley",
    )
    .encode(
        x=gs.Locus("chrom", "cigarStart", band=0),
        x2=None,
        tooltip=[
            gs.Tooltip(
                gs.expr(
                    gs.expr.slice(
                        gs.datum._seq,
                        gs.datum.readStart,
                        gs.datum.readEnd,
                    )
                )
            ).title("Inserted sequence")
        ],
    )
    .properties(name="insertions", title="Insertion")
)

# Label unaligned read ends with "S" for soft clipping.
soft_clips = (
    gs.Chart()
    .transform_filter(gs.datum.cigarType == "softClip")
    .mark_text(
        text="S",
        color="#555",
        size=gs.expr(LANE_HEIGHT * 0.90),
        font="Radley",
    )
    .encode(x=gs.Locus("chrom", "cigarStart", band=0), x2=None)
    .properties(name="soft-clips", title="Soft-clipped bases")
)

# Read the alignment instructions (CIGAR) to place these details on each read.
cigar_overlays = (
    gs.layer(deletions, skips, insertions, soft_clips)
    .transform_formula(expr=gs.datum.seq, as_="_seq")
    .transform_flatten_cigar(copyFields=["chrom", "_lane", "name", "cigar", "_seq"])
    .properties(name="cigar-overlays", title="CIGAR operation")
)

# Color mismatched bases, fading those with lower base quality.
mismatch_rects = (
    gs.Chart()
    .mark_rect(minWidth=1)
    .encode(
        color=gs.Color("base:N").scale(base_colors).legend(title="Base"),
        opacity=gs.Opacity("_baseQualityForOpacity:Q")
        .scale(domain=[5, 20], range=[0.1, 1], clamp=True, nice=False)
        .legend(title="Base quality", values=[6, 10, 15, 20]),
    )
    .properties(name="mismatch-rects", title="Mismatch")
)

# Draw the base letters over their colored blocks.
mismatch_labels = (
    gs.Chart()
    .mark_text(color="black", size=gs.expr(LANE_HEIGHT * 0.75), tooltip=None)
    .encode(text=gs.Text("base:N"))
    .properties(name="mismatch-labels", title="Mismatch base")
)

# Find mismatches from the read's MD tag and apply the base-quality slider.
mismatches = (
    (mismatch_rects + mismatch_labels)
    .transform_filter(gs.datum.md != None)  # noqa: E711
    .transform_alignment_mismatches(
        copyFields=["chrom", "_lane", "name", "cigar", "mapq", "strand"]
    )
    .transform_formula(
        expr=gs.expr.if_(gs.datum.baseQuality == None, 20, gs.datum.baseQuality),  # noqa: E711
        as_="_baseQualityForOpacity",
    )
    .transform_filter(
        (gs.datum.baseQuality == None)  # noqa: E711
        | (gs.datum.baseQuality >= MIN_BASE_QUALITY)
    )
    .properties(name="mismatches", title="Mismatch")
    .encode(
        x=gs.Locus("chrom", "mismatchStart", band=0),
        x2=gs.Locus("chrom", "mismatchEnd", band=0),
    )
)

# Put the read arrows, alignment details, and mismatches on the same rows.
read_layers = (
    gs.layer(read_backbone, cigar_overlays, mismatches)
    .properties(name="read-layers", title="Read alignments")
    .encode(y=gs.Y("_lane:I").scale(padding=0.25, reverse=True, zoom=False))
    .resolve_scale(opacity="independent")
)

# Ask the reader to zoom in when the region is too wide to load reads.
zoom_message = gs.layer(
    gs.Chart().mark_rect(fill="white", opacity=0.7),
    gs.Chart()
    .mark_text(text="Zoom in closer to load data.", color="#333", size=13, yOffset=20)
    .encode(x=gs.value(0.5), y=gs.value(1)),
    data=[{}],
    name="zoom-message",
    opacity=ZOOM_MESSAGE_STATE,
).add_params(ZOOM_MESSAGE_STATE)

# Make the read rows scrollable and connect their height to the slider.
read_alignments = (
    gs.layer(read_layers, zoom_message)
    .properties(
        name="read-alignments",
        title=gs.Title(text="Read alignments", orient="none"),
        height=gs.Step(step=LANE_HEIGHT),
        viewportHeight="container",
    )
    .add_params(LANE_HEIGHT)
    .resolve_scale(color="independent", opacity="independent")
)

# Load the visible reads and place the summary above the scrollable read track.
chart = (
    (coverage & read_alignments)
    .properties(
        assembly="hg38",
        data=gs.lazy.bam(
            "https://data.genomespy.app/sample-data/NIST-HG002/"
            "HG002.GRCh38.chr20_9950000_10100000.downsample33pct.bam",
            windowSize=WINDOW_SIZE,
        ),
        scales=gs.scales(
            x=gs.Scale(
                domain=[
                    {"chrom": "chr20", "pos": 10031817},
                    {"chrom": "chr20", "pos": 10031936},
                ]
            )
        ),
        spacing=5,
        description="BAM depth, alignments, CIGAR operations, and mismatches.",
    )
    .add_params(MIN_MAPQ, MIN_BASE_QUALITY, WINDOW_SIZE)
    # Apply the mapping-quality cutoff, keeping reads with unknown quality.
    .transform_filter((gs.datum.mapq == None) | (gs.datum.mapq >= MIN_MAPQ))  # noqa: E711
    .transform_formula(
        expr=gs.expr.if_(gs.datum.mapq == None, 0, gs.datum.mapq),  # noqa: E711
        as_="_mapqOrZero",
    )
    # Put overlapping reads on separate rows.
    .transform_pileup(start="start", end="end", as_="_lane")
    .resolve_axis(x="shared")
    .configure_view(stroke="lightgray")
    .configure_legend()
)
