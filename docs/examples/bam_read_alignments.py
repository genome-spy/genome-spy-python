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

base_colors = gs.Scale(
    domain=["A", "C", "T", "G", "N"],
    range=["#4FBF45", "#4D96E8", "#E85F78", "#E8B322", "#BDBDBD"],
)

depth = (
    gs.Chart()
    .transform_flatten_cigar(copyFields=["chrom"])
    .transform_filter("datum.cigarType == 'aligned'")
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

mismatch_summary = (
    gs.Chart()
    .transform_filter("datum.md != null")
    .transform_alignment_mismatches(copyFields=["chrom"])
    .transform_filter(
        "datum.baseQuality == null || datum.baseQuality >= minBaseQuality"
    )
    .transform_aggregate(groupby=["chrom", "mismatchStart", "base"])
    .transform_stack(
        field="count",
        groupby=["chrom", "mismatchStart"],
        sort=gs.compare("base", order="ascending"),
        as_=["mismatchCount0", "mismatchCount1"],
    )
    .transform_formula(expr="datum.mismatchStart + 1", as_="mismatchEnd")
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

insertion_summary = (
    gs.Chart()
    .transform_flatten_cigar(copyFields=["chrom"])
    .transform_filter("datum.cigarType == 'insertion'")
    .transform_aggregate(groupby=["chrom", "cigarStart"])
    .mark_rule(color="black", size=1)
    .encode(
        x=gs.Locus("chrom", "cigarStart", band=0),
        y=gs.datum(0, type="quantitative"),
        y2=gs.Y2("count"),
    )
    .properties(name="insertion-summary", title="Insertion support")
)

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

read_backbone = (
    gs.Chart()
    .mark_arrow(
        style="arrow-block",
        minStemLength=10,
        fill="#e0e0e0",
        stroke="#c4c4c4",
        strokeWidth=gs.expr("linearstep(3, 8, laneHeight)"),
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

deletions = gs.layer(
    gs.Chart()
    .transform_filter("datum.cigarType == 'deletion'")
    .mark_rect(color="white", minWidth=1),
    gs.Chart()
    .transform_filter("datum.cigarType == 'deletion'")
    .mark_rule(color="#222", minLength=1),
)

deletions = deletions.properties(name="deletions", title="Deletion").encode(
    x=gs.Locus("chrom", "cigarStart", band=0),
    x2=gs.Locus("chrom", "cigarEnd", band=0),
)

skips = (
    gs.Chart()
    .transform_filter("datum.cigarType == 'skip'")
    .mark_rule(color="#6b6b6b", strokeDash=[2, 2], minLength=1)
    .encode(
        x=gs.Locus("chrom", "cigarStart", band=0),
        x2=gs.Locus("chrom", "cigarEnd", band=0),
    )
    .properties(name="skips", title="Skipped region")
)

insertions = (
    gs.Chart()
    .transform_filter("datum.cigarType == 'insertion'")
    .mark_text(
        text="I",
        color="black",
        size=gs.expr("laneHeight * 0.90"),
        font="Radley",
    )
    .encode(
        x=gs.Locus("chrom", "cigarStart", band=0),
        x2=None,
        tooltip=[
            gs.Tooltip(
                gs.expr("slice(datum._seq, datum.readStart, datum.readEnd)")
            ).title("Inserted sequence")
        ],
    )
    .properties(name="insertions", title="Insertion")
)

soft_clips = (
    gs.Chart()
    .transform_filter("datum.cigarType == 'softClip'")
    .mark_text(
        text="S",
        color="#555",
        size=gs.expr("laneHeight * 0.90"),
        font="Radley",
    )
    .encode(x=gs.Locus("chrom", "cigarStart", band=0), x2=None)
    .properties(name="soft-clips", title="Soft-clipped bases")
)

cigar_overlays = (
    gs.layer(deletions, skips, insertions, soft_clips)
    .transform_formula(expr="datum.seq", as_="_seq")
    .transform_flatten_cigar(copyFields=["chrom", "_lane", "name", "cigar", "_seq"])
    .properties(name="cigar-overlays", title="CIGAR operation")
)

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

mismatch_labels = (
    gs.Chart()
    .mark_text(color="black", size=gs.expr("laneHeight * 0.75"), tooltip=None)
    .encode(text=gs.Text("base:N"))
    .properties(name="mismatch-labels", title="Mismatch base")
)

mismatches = (
    (mismatch_rects + mismatch_labels)
    .transform_filter("datum.md != null")
    .transform_alignment_mismatches(
        copyFields=["chrom", "_lane", "name", "cigar", "mapq", "strand"]
    )
    .transform_formula(
        expr="datum.baseQuality == null ? 20 : datum.baseQuality",
        as_="_baseQualityForOpacity",
    )
    .transform_filter(
        "datum.baseQuality == null || datum.baseQuality >= minBaseQuality"
    )
    .properties(name="mismatches", title="Mismatch")
    .encode(
        x=gs.Locus("chrom", "mismatchStart", band=0),
        x2=gs.Locus("chrom", "mismatchEnd", band=0),
    )
)

read_layers = (
    gs.layer(read_backbone, cigar_overlays, mismatches)
    .properties(name="read-layers", title="Read alignments")
    .encode(y=gs.Y("_lane:I").scale(padding=0.25, reverse=True, zoom=False))
    .resolve_scale(opacity="independent")
)

zoom_message = gs.layer(
    gs.Chart().mark_rect(fill="white", opacity=0.7),
    gs.Chart()
    .mark_text(text="Zoom in closer to load data.", color="#333", size=13, yOffset=20)
    .encode(x=gs.value(0.5), y=gs.value(1)),
    data=[{}],
    name="zoom-message",
    params=[
        gs.param(
            "zoomMessageState",
            expr="abs(span(domain('x'))) > windowSize ? 1 : 0",
            transition={"type": "lerp", "halfLife": 60},
        )
    ],
    opacity=gs.expr("zoomMessageState"),
)

read_alignments = (
    gs.layer(read_layers, zoom_message)
    .properties(
        name="read-alignments",
        title=gs.Title(text="Read alignments", orient="none"),
        height=gs.Step(step=gs.expr("laneHeight")),
        viewportHeight="container",
        params=[
            gs.param(
                "laneHeight",
                value=12,
                bind={"input": "range", "min": 1, "max": 30, "step": 1},
                transition={"type": "lerp", "halfLife": 30, "epsilon": 0.02},
            )
        ],
    )
    .resolve_scale(color="independent", opacity="independent")
)

chart = (
    (coverage & read_alignments)
    .properties(
        assembly="hg38",
        data=gs.lazy.bam(
            "https://data.genomespy.app/sample-data/NIST-HG002/"
            "HG002.GRCh38.chr20_9950000_10100000.downsample33pct.bam",
            windowSize=gs.expr("windowSize"),
        ),
        params=[
            gs.param(
                "minMapq",
                value=0,
                bind={
                    "input": "range",
                    "min": 0,
                    "max": 60,
                    "step": 1,
                    "debounce": 100,
                },
            ),
            gs.param(
                "minBaseQuality",
                value=0,
                bind={
                    "input": "range",
                    "min": 0,
                    "max": 40,
                    "step": 1,
                    "debounce": 100,
                },
            ),
            gs.param("windowSize", value=15_000),
        ],
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
    .transform_filter("datum.mapq == null || datum.mapq >= minMapq")
    .transform_formula(
        expr="datum.mapq == null ? 0 : datum.mapq",
        as_="_mapqOrZero",
    )
    .transform_pileup(start="start", end="end", as_="_lane")
    .resolve_axis(x="shared")
    .configure_view(stroke="lightgray")
    .configure_legend()
)
