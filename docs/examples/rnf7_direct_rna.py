"""ONT direct-RNA coverage and read alignments along RNF7.

An IGV-like browser connects condition-specific coverage and m6A site evidence
to reference sequence, alignment edits, and the individual wild-type and
METTL3-knockout molecules.
"""

from __future__ import annotations

import genome_spy as gs
from genome_spy.datasets._direct_rna import rnf7_direct_rna_data
from genome_spy.schema import Axis

META = {
    "category": "Read alignments and RNA splicing",
    "order": 18,
    "height": 820,
    "max_width": 980,
}

DISPLAY_DOMAIN = [0, 920]
WT_COLOR = "#6656c7"
KO_COLOR = "#e38335"
BASE_COLORS = gs.Scale(
    domain=["A", "C", "G", "T", "N"],
    range=["#4fbf45", "#4d96e8", "#e8b322", "#e85f78", "#bdbdbd"],
)

lane_height = gs.param(
    "laneHeight",
    value=6,
    bind=gs.binding_range(min=3, max=14, step=1, name="Read row height: "),
    transition={"type": "lerp", "halfLife": 30, "epsilon": 0.02},
)

# The whole-pileup overview controls the shared detail window.
brush = gs.param("transcriptWindow")
brush_update = gs.selection_interval(
    "transcriptWindow",
    encodings=["x"],
    push="outer",
    persist=False,
    mark=gs.BrushConfig(
        clip=False,
        fill="#4d70b8",
        fillOpacity=0.16,
        stroke="#355b9f",
        strokeWidth=1.2,
        measure="outside",
    ),
)
cursor = gs.ruler(
    "transcriptCursor",
    persist=False,
    encodings=["x"],
    extent="container",
    snap=False,
    mark=gs.RulerMarkConfig(stroke="#4d4d55", strokeWidth=1, opacity=0.35),
)


def coverage_bars(
    condition: str,
    color: str,
) -> gs.Chart:
    """Build one translucent per-base coverage layer in the shared panel."""

    return (
        gs.Chart(gs.Data(name="coverage"))
        .transform_filter(gs.datum.condition == condition)
        .transform_formula(expr=gs.datum.position + 1, as_="positionEnd")
        .mark_rect(clip="x", color=color, opacity=0.5, minWidth=0.5)
        .encode(
            x=gs.X("position:I"),
            x2=gs.X2("positionEnd"),
            y=gs.Y("coverage:Q")
            .scale(domain=[0, 160], nice=False, zero=True)
            .axis(title="Read depth", values=[0, 80, 160], grid=True),
            tooltip=[
                gs.Tooltip("conditionLabel:N").title("Condition"),
                gs.Tooltip("position:Q").title("Transcript position"),
                gs.Tooltip("coverage:Q").title("Read depth"),
                gs.Tooltip("coverageFraction:Q", format=".1%").title(
                    "Fraction of displayed reads"
                ),
            ],
        )
    )


# Draw the taller knockout profile first, then let the translucent WT bars mix
# with it wherever the two condition-specific coverages overlap.
coverage = gs.layer(
    coverage_bars("KO", KO_COLOR),
    coverage_bars("WT", WT_COLOR),
).properties(height=94)


# Keep the transcript model compact. Its genomic exon coordinates remain in
# tooltips, while the horizontal axis uses the BAM's transcript coordinates.
exon_blocks = (
    gs.Chart()
    .mark_rect(
        y=0.22,
        y2=0.78,
        cornerRadius=2,
        color="#55555f",
        stroke="white",
        strokeWidth=2,
    )
    .encode(
        x=gs.X("displayStart:I"),
        x2=gs.X2("displayEnd"),
        tooltip=[
            gs.Tooltip("exon:O").title("RNF7-201 exon"),
            gs.Tooltip("genomicStart:Q", format=",").title("GRCh38 start"),
            gs.Tooltip("genomicEnd:Q", format=",").title("GRCh38 end"),
        ],
    )
)
exon_labels = (
    gs.Chart()
    .transform_formula(expr="'Exon ' + datum.exon", as_="label")
    .mark_text(color="white", fontWeight=500, tooltip=None)
    .encode(
        x=gs.X("displayCenter:I"),
        y=gs.value(0.5),
        text=gs.Text("label:N"),
    )
)
transcript = gs.layer(exon_blocks, exon_labels).properties(
    name="transcript-model",
    data=gs.Data(name="exons"),
    height=32,
)


# Color every reference base as a narrow tile. Letters fade in only when the
# selected interval is close enough to base-pair resolution.
sequence_rects = (
    gs.Chart()
    .transform_formula(expr=gs.datum.position + 1, as_="positionEnd")
    .mark_rect(y=0.28, y2=0.72, opacity=0.7)
    .encode(
        x=gs.X("position:I"),
        x2=gs.X2("positionEnd"),
        color=gs.Color("base:N").scale(BASE_COLORS).legend(None),
        tooltip=[
            gs.Tooltip("position:Q").title("Transcript position"),
            gs.Tooltip("base:N").title("Reference base"),
        ],
    )
)
sequence_labels = (
    gs.Chart()
    .transform_formula(expr=gs.datum.position + 0.5, as_="baseCenter")
    .mark_text(
        y=0.5,
        size=11,
        color="#111111",
        tooltip=None,
    )
    .encode(x=gs.X("baseCenter:I"), text=gs.Text("base:N"))
    .properties(opacity=gs.dynamic_opacity(unitsPerPixel=[0.2, 0.1], values=[0, 1]))
)


def m6a_site_markers(
    condition: str,
    color: str,
    y: float,
    shape: str,
) -> gs.Chart:
    """Place compact m6A probability markers around the reference sequence."""

    return (
        gs.Chart(gs.Data(name="sites"))
        .transform_filter(gs.datum.condition == condition)
        .mark_point(
            y=y,
            shape=shape,
            clip="x",
            filled=True,
            color=color,
            stroke="white",
            strokeWidth=0.8,
        )
        .encode(
            x=gs.X("position:I"),
            size=gs.Size("probability:Q")
            .scale(domain=[0, 1], range=[12, 72], clamp=True, nice=False)
            .legend(None),
            tooltip=[
                gs.Tooltip("conditionLabel:N").title("Condition"),
                gs.Tooltip("position:Q").title("Transcript position"),
                gs.Tooltip("genomicPosition:Q", format=",").title("GRCh38 position"),
                gs.Tooltip("kmer:N").title("5-mer context"),
                gs.Tooltip("probability:Q", format=".3f").title("m6Anet probability"),
                gs.Tooltip("difference:Q", format="+.3f").title("WT − KO"),
                gs.Tooltip("highConfidence:N").title("High confidence"),
            ],
        )
    )


sequence = gs.layer(
    sequence_rects,
    sequence_labels,
    m6a_site_markers("WT", WT_COLOR, 0.12, "triangle-down"),
    m6a_site_markers("KO", KO_COLOR, 0.88, "triangle-up"),
).properties(
    name="reference-sequence-m6a",
    data=gs.Data(name="sequence"),
    height=44,
)


def read_track(condition: str, color: str) -> gs.LayerChart:
    """Build a scrollable read track with mismatches and CIGAR events."""

    backbone = (
        gs.Chart(gs.Data(name="reads"))
        .transform_filter(gs.datum.condition == condition)
        .mark_arrow(
            style="arrow-block",
            minStemLength=8,
            fill=color,
            fillOpacity=0.38,
            stroke=color,
            strokeOpacity=0.62,
            strokeWidth=0.5,
        )
        .encode(
            x=gs.X("start:I"),
            x2=gs.X2("end"),
            opacity=gs.Opacity("mapq:Q")
            .scale(domain=[0, 60], range=[0.28, 1])
            .legend(None),
            direction=gs.value("forward"),
            tooltip=[
                gs.Tooltip("conditionLabel:N").title("Condition"),
                gs.Tooltip("read:N").title("Molecule"),
                gs.Tooltip("start:Q").title("Start"),
                gs.Tooltip("end:Q").title("End"),
                gs.Tooltip("queryLength:Q").title("Query length"),
                gs.Tooltip("mapq:Q").title("Mapping quality"),
            ],
        )
    )

    event_source = gs.Chart(gs.Data(name="events")).transform_filter(
        gs.datum.condition == condition
    )
    deletions = gs.layer(
        event_source.transform_filter(gs.datum.eventType == "deletion").mark_rect(
            color="white", minWidth=1, tooltip=None
        ),
        event_source.transform_filter(gs.datum.eventType == "deletion").mark_rule(
            color="#222222", minLength=1
        ),
    ).encode(
        x=gs.X("start:I", band=0),
        x2=gs.X2("end", band=0),
        tooltip=[
            gs.Tooltip("read:N").title("Molecule"),
            gs.Tooltip("start:Q").title("Deletion start"),
            gs.Tooltip("length:Q").title("Deleted bases"),
        ],
    )
    skips = (
        event_source.transform_filter(gs.datum.eventType == "skip")
        .mark_rule(color="#555555", strokeDash=[2, 2], minLength=1)
        .encode(
            x=gs.X("start:I"),
            x2=gs.X2("end"),
            tooltip=[
                gs.Tooltip("read:N").title("Molecule"),
                gs.Tooltip("start:Q").title("Skipped-region start"),
                gs.Tooltip("length:Q").title("Skipped bases"),
            ],
        )
    )
    insertions = (
        event_source.transform_filter(gs.datum.eventType == "insertion")
        .mark_text(text="I", color="#171717", size=gs.expr(lane_height * 0.9))
        .encode(
            x=gs.X("start:I"),
            tooltip=[
                gs.Tooltip("read:N").title("Molecule"),
                gs.Tooltip("start:Q").title("Insertion position"),
                gs.Tooltip("length:Q").title("Inserted bases"),
                gs.Tooltip("insertedSequence:N").title("Inserted sequence"),
            ],
        )
    )
    soft_clips = (
        event_source.transform_filter(gs.datum.eventType == "softClip")
        .mark_text(text="S", color="#555555", size=gs.expr(lane_height * 0.9))
        .encode(
            x=gs.X("start:I"),
            tooltip=[
                gs.Tooltip("read:N").title("Molecule"),
                gs.Tooltip("length:Q").title("Soft-clipped bases"),
            ],
        )
    )
    mismatch_rects = (
        event_source.transform_filter(gs.datum.eventType == "mismatch")
        .mark_rect(minWidth=1)
        .encode(
            x=gs.X("start:I"),
            x2=gs.X2("end"),
            color=gs.Color("base:N").scale(BASE_COLORS).legend(None),
            opacity=gs.Opacity("baseQuality:Q")
            .scale(domain=[5, 20], range=[0.2, 1], clamp=True, nice=False)
            .legend(None),
            tooltip=[
                gs.Tooltip("read:N").title("Molecule"),
                gs.Tooltip("start:Q").title("Mismatch position"),
                gs.Tooltip("refBase:N").title("Reference"),
                gs.Tooltip("base:N").title("Read base"),
                gs.Tooltip("baseQuality:Q").title("Base quality"),
            ],
        )
    )
    mismatch_labels = (
        event_source.transform_filter(gs.datum.eventType == "mismatch")
        .transform_formula(expr=gs.datum.start + 0.5, as_="baseCenter")
        .mark_text(
            color="#111111",
            size=gs.expr(lane_height * 0.72),
            tooltip=None,
        )
        .encode(x=gs.X("baseCenter:I"), text=gs.Text("base:N"))
        .properties(opacity=gs.dynamic_opacity(unitsPerPixel=[0.2, 0.1], values=[0, 1]))
    )

    return (
        gs.layer(
            backbone,
            deletions,
            skips,
            insertions,
            soft_clips,
            mismatch_rects,
            mismatch_labels,
        )
        .encode(
            y=gs.Y("lane:I")
            .scale(padding=0.18, reverse=True, zoom=False)
            .axis(labels=False, ticks=False, title=None)
        )
        .properties(
            height=gs.Step(step=lane_height),
            viewportHeight=190,
        )
        .resolve_scale(color="independent", opacity="independent")
    )


wild_type_reads = read_track("WT", WT_COLOR)
knockout_reads = read_track("KO", KO_COLOR)

# Compress all WT and knockout lanes into one fixed-height navigation track.
read_overview = (
    gs.layer(
        gs.Chart(gs.Data(name="reads"))
        .mark_rule(size=1, opacity=0.58)
        .encode(
            x=gs.X("start:I")
            .scale(domain=DISPLAY_DOMAIN, nice=False, zoom=False)
            .axis(title="RNF7-201 transcript position (nt)", tickCount=10),
            x2=gs.X2("end"),
            y=gs.Y("overviewY:Q")
            .scale(domain=[0, 1], reverse=True, zoom=False)
            .axis(labels=False, ticks=False, title="All reads"),
            color=gs.Color("conditionLabel:N")
            .scale(
                domain=["Wild type", "METTL3 knockout"],
                range=[WT_COLOR, KO_COLOR],
            )
            .legend(
                title=None,
                orient="bottom",
                direction="horizontal",
            ),
            tooltip=[
                gs.Tooltip("conditionLabel:N").title("Condition"),
                gs.Tooltip("read:N").title("Molecule"),
                gs.Tooltip("start:Q").title("Start"),
                gs.Tooltip("end:Q").title("End"),
            ],
        ),
    )
    .properties(height=78)
    .add_params(brush_update)
)
overview = gs.vconcat(read_overview).resolve_scale(x="excluded")

# Every detail track shares the brush-controlled transcript scale and ruler.
details = (
    gs.vconcat(
        coverage,
        transcript,
        sequence,
        wild_type_reads,
        knockout_reads,
        spacing=3,
    )
    .properties(
        scales=gs.scales(
            x=gs.Scale(
                domain=gs.SelectionDomainRef(
                    param=brush.name,
                    initial=DISPLAY_DOMAIN,
                ),
                nice=False,
                zoom=True,
            )
        ),
        axes=gs.axes(
            x=Axis(
                orient="top",
                title="RNF7-201 transcript position (nt)",
                tickCount=10,
                grid=False,
            )
        ),
    )
    .add_params(cursor)
    .resolve_scale(x="shared", y="independent")
    .resolve_axis(x="shared", y="independent")
)

data = rnf7_direct_rna_data()
event_records = (
    data["events"]
    .astype(object)
    .where(data["events"].notna(), None)
    .to_dict(orient="records")
)
chart = (
    gs.vconcat(details, overview, spacing=6)
    .properties(
        title="RNF7 ONT direct-RNA coverage, m6A evidence, and alignments",
        description=(
            "Condition-specific aggregate coverage and published m6Anet site "
            "probabilities above RNF7-201 reference sequence and separate "
            "wild-type and METTL3-knockout long-read alignments with real "
            "mismatch and CIGAR-event overlays."
        ),
        datasets={
            "coverage": data["coverage"].to_dict(orient="records"),
            "reads": data["reads"].to_dict(orient="records"),
            "events": event_records,
            "sequence": data["sequence"].to_dict(orient="records"),
            "sites": data["sites"].to_dict(orient="records"),
            "exons": data["exons"].to_dict(orient="records"),
        },
        padding=28,
    )
    .add_params(brush, lane_height)
    .resolve_scale(x="independent", y="independent", color="independent")
    .resolve_axis(x="independent", y="independent")
    .configure_view(stroke="#dedee5")
)
