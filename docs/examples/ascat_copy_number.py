"""ASCAT copy-number segmentation.

Aligned allele-specific copy-number, LogR, and B-allele-frequency tracks show
segment estimates over raw probe values for simulated sample S96.
"""

import genome_spy as gs

META = {
    "category": "Copy-number plots",
    "order": 22,
    "height": 500,
    "max_width": 980,
}

SEGMENTS_URL = "https://data.genomespy.app/sample-data/ASCAT/segments_S96.tsv"
RAW_URL = "https://data.genomespy.app/sample-data/ASCAT/raw_S96.tsv"
# Make individual measurements easier to see when zoomed in.
ZOOM_LEVEL = gs.Expression("zoomLevel")
POINT_SIZE = gs.expr(gs.expr.min(10 * gs.expr.pow(ZOOM_LEVEL, 1.5), 200))

# Draw the minor-allele copy count in green.
minor_copy_number = (
    gs.Chart()
    .mark_rule(minLength=2, yOffset=-3)
    .encode(
        y=gs.Y("nMinor:Q")
        .scale(domain=[0, 6], padding=0.04, clamp=True)
        .axis(tickMinStep=1),
        size=gs.value(5),
        color=gs.value("#88d27a"),
    )
    .properties(title="nMinor")
)

# Draw the major-allele copy count in red, offset slightly to keep both visible.
major_copy_number = (
    gs.Chart()
    .mark_rule(minLength=2, yOffset=3)
    .encode(
        y=gs.Y("nMajor:Q").scale(domain=[0, 6]),
        size=gs.value(5),
        color=gs.Color("nMajor:Q").scale(
            domain=[0, 6, 16], range=["#f06850", "#f06850", "#5F0F0F"]
        ),
    )
    .properties(title="nMajor")
)

# Combine both allele counts in the top track.
copy_number = (minor_copy_number + major_copy_number).properties(
    name="copyNumberTrack",
    title=gs.title("Allele-specific copy numbers", style="overlay"),
)

# Load individual LogR measurements and draw them as faint points.
raw_logr = (
    gs.Chart(gs.Data(url=RAW_URL))
    .mark_point(size=POINT_SIZE)
    .encode(
        x=gs.Locus("chr", "pos"),
        y=gs.Y("logR:Q").title(None),
        color=gs.value("#7090c0"),
        opacity=gs.value(0.25),
        strokeWidth=gs.value(0),
    )
    .properties(title="Single probe")
)

# Add a black line for each segment's mean LogR.
mean_logr = (
    gs.Chart()
    .mark_rule(minLength=3)
    .encode(
        y=gs.Y("logRMean:Q").title("LogR"),
        size=gs.value(3),
        color=gs.value("black"),
    )
    .properties(title="Mean LogR")
)

logr = (raw_logr + mean_logr).properties(name="logRTrack")

# Show individual B-allele frequencies, skipping missing measurements.
raw_baf = (
    gs.Chart(gs.Data(url=RAW_URL))
    .transform_filter(gs.datum.baf != None)  # noqa: E711
    .mark_point(size=POINT_SIZE)
    .encode(
        x=gs.Locus("chr", "pos"),
        y=gs.Y("baf:Q").title(None),
        color=gs.value("#7090c0"),
        opacity=gs.value(0.3),
        strokeWidth=gs.value(0),
    )
    .properties(title="Single probe")
)

# Add the segment's mean B-allele frequency.
mean_baf = (
    gs.Chart()
    .mark_rule(minLength=3)
    .encode(
        y=gs.Y("bafMean:Q").scale(domain=[0, 1]).title("B-allele frequency"),
        size=gs.value(3),
        color=gs.value("black"),
    )
    .properties(title="Mean BAF")
)

# Mirror the mean around 0.5 to show the complementary allele frequency.
mirrored_baf = (
    gs.Chart()
    .mark_rule(minLength=3)
    .encode(
        y=gs.Y(gs.expr(1 - gs.datum.bafMean), type="quantitative").title(None),
        size=gs.value(3),
        color=gs.value("black"),
    )
    .properties(title="Mean BAF")
)

baf = (raw_baf + mean_baf + mirrored_baf).properties(name="bafTrack")

# Load the segment estimates and stack the three tracks so they zoom together.
chart = (
    (copy_number & logr & baf)
    .properties(
        assembly="hg18",
        data=gs.Data(url=SEGMENTS_URL),
        background="#fafafa",
        description=(
            "ASCAT sample S96 with aligned allele-specific copy-number, LogR, "
            "and B-allele-frequency tracks."
        ),
    )
    .encode(
        x=gs.Locus("chr", "startpos").scale(type="locus"),
        x2=gs.Locus("chr", "endpos", offset=1),
    )
    .resolve_axis(x="shared")
    .configure_axis_x(grid=False, chromGrid=True, orient="bottom")
    .configure_axis_y(grid=True, gridColor="#f8f8f8")
    .configure_legend(disable=True)
    .configure_view(
        fill="white",
        stroke="#c8c8c8",
        shadowBlur=8,
        shadowColor="black",
        shadowOpacity=0.1,
    )
)
