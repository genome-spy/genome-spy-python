"""LUAD oncoprint.

A large cohort oncoprint adapted from the `pyoncoprint` TCGA LUAD notebook.
The shared sample axis ties together top burden and clinical tracks, the main
alteration matrix, and lower quantitative heatmaps.
"""

from __future__ import annotations

import genome_spy as gs
from genome_spy.datasets._oncoprint import luad_oncoprint_data
from genome_spy.schema import Scale

META = {
    "category": "Oncoprints and cohort summaries",
    "order": 35,
    "height": 720,
    "max_width": 1680,
}

CLASS_ORDER = [
    "Amplification",
    "Deep Deletion",
    "Splice Mutation (putative driver)",
    "Splice Mutation (putative passenger)",
    "Structural Variant (putative driver)",
    "Structural Variant (putative passenger)",
    "Inframe Mutation (putative driver)",
    "Missense Mutation (putative driver)",
    "Missense Mutation (putative passenger)",
    "Truncating mutation (putative driver)",
    "Truncating mutation (putative passenger)",
]

CLASS_COLORS = [
    "#ff2d2d",
    "#2846ff",
    "#d97706",
    "#f59e0b",
    "#7e22ce",
    "#d946ef",
    "#8b4513",
    "#19a34a",
    "#57ff33",
    "#111111",
    "#f3e21b",
]

SPECTRUM_ORDER = ["C>A", "C>G", "C>T", "T>A", "T>C", "T>G"]
SPECTRUM_COLORS = ["#2b59ff", "#00b3ff", "#29bf12", "#8dff3f", "#ff9f1c", "#d7263d"]

STAGE_ORDER = ["T1", "T1A", "T1B", "T2", "T2A", "T2B", "T3", "T4", "TX"]
STAGE_COLORS = [
    "#1d4ed8",
    "#4f46e5",
    "#06b6d4",
    "#10b981",
    "#84cc16",
    "#f59e0b",
    "#dc2626",
    "#7f1d1d",
    "#6b7280",
]

SAMPLE_TRACK_WIDTH = "container"
PERCENT_WIDTH = 32
COUNTS_WIDTH = 120
TMB_HEIGHT = 54
SPECTRUM_HEIGHT = 28
MSI_HEIGHT = 40
STAGE_HEIGHT = 24
MATRIX_HEIGHT = 430
MRNA_HEIGHT = 64
METHYLATION_HEIGHT = 64
MICROBIOME_HEIGHT = 28
SAMPLE_LABEL_HEIGHT = 80
TRACK_TICK_FONT_SIZE = 9
HEATMAP_LABEL_FONT_SIZE = 9
SUMMARY_WIDTH = PERCENT_WIDTH + COUNTS_WIDTH + 2
TOP_TRACKS_HEIGHT = TMB_HEIGHT + SPECTRUM_HEIGHT + MSI_HEIGHT + STAGE_HEIGHT + 16

MRNA_GROUP = "mRNA expression z-scores relative to diploid samples (RNA Seq V2 RSEM)"
METHYLATION_GROUP = "Methylation (HM27 and HM450 merge)"
MICROBIOME_GROUP = "Microbiome Signatures (log RNA Seq CPM)"


data = luad_oncoprint_data()

sample_domain = data["sample_domain"]
gene_order = data["gene_order"]
burden_limit = data["burden_limit"]
count_limit = data["count_limit"]
msi_limit = data["msi_limit"]

mutation_scale = Scale().domain(CLASS_ORDER).range(CLASS_COLORS)
spectrum_scale = Scale().domain(SPECTRUM_ORDER).range(SPECTRUM_COLORS)
stage_scale = Scale().domain(STAGE_ORDER).range(STAGE_COLORS)


def empty_panel(*, height: int) -> gs.Chart:
    """Create a placeholder that aligns the summary column with the matrix."""
    return (
        gs.Chart([])
        .mark_point()
        .properties(name="summary-placeholder", width=SUMMARY_WIDTH, height=height)
    )


def heatmap_panel(
    group_name: str,
    *,
    panel_height: int,
    domain: list[float],
    colors: list[str],
) -> gs.Chart:
    """Render one grouped quantitative heatmap block."""
    panel_data = data["heatmap_cells"][data["heatmap_cells"]["group"] == group_name]
    rows = data["heatmap_rows"][data["heatmap_rows"]["group"] == group_name]
    track_order = rows.sort_values("track_order")["track"].tolist()

    return (
        gs.Chart(panel_data)
        .mark_rect(stroke="white", strokeWidth=0.35)
        .encode(
            x=gs.X("sample_order:I").axis(None).title(None),
            y=gs.Y("track:N")
            .scale(domain=track_order, reverse=False, padding=0.02)
            .axis(title=None, labelFontSize=HEATMAP_LABEL_FONT_SIZE, labelLimit=74),
            color=gs.Color("value:Q").scale(domain=domain, range=colors).legend(None),
        )
        .properties(
            width=SAMPLE_TRACK_WIDTH,
            height=panel_height,
        )
    )


# --- top sample-aligned tracks -------------------------------------------------

burden_track = (
    gs.Chart(data["sample_burden"])
    .transform_stack(
        field="count",
        groupby=["sample_order"],
        as_=["_y0", "_y1"],
    )
    .mark_rect()
    .encode(
        x=gs.X("sample_order:I").axis(None).title(None),
        y=gs.Y("_y0:Q")
        .scale(reverse=False, domain=[0, burden_limit], zero=True)
        .axis(labelFontSize=TRACK_TICK_FONT_SIZE, labelPadding=2, tickCount=3)
        .title(None),
        y2=gs.Y2("_y1"),
        color=gs.Color("class:N").scale(mutation_scale).legend(None),
    )
    .properties(
        width=SAMPLE_TRACK_WIDTH,
        height=TMB_HEIGHT,
        title=gs.Title(text="TMB", style="track-title"),
    )
)

mutation_spectrum_track = (
    gs.Chart(data["mutation_spectrum"])
    .transform_stack(
        field="count",
        groupby=["sample_order"],
        as_=["_y0", "_y1"],
        offset="normalize",
    )
    .mark_rect()
    .encode(
        x=gs.X("sample_order:I").axis(None).title(None),
        y=gs.Y("_y0:Q")
        .scale(reverse=False, domain=[0, 1], zero=True)
        .axis(domain=False, labels=False, ticks=False)
        .title(None),
        y2=gs.Y2("_y1"),
        color=gs.Color("class:N").scale(spectrum_scale).legend(None),
    )
    .properties(
        width=SAMPLE_TRACK_WIDTH,
        height=SPECTRUM_HEIGHT,
        title=gs.Title(text="Mutation spectrum", style="track-title"),
    )
)

msi_track = (
    gs.Chart(data["msi"])
    .mark_rect(color="#15803d")
    .encode(
        x=gs.X("sample_order:I").axis(None).title(None),
        y=gs.Y(gs.datum(0), type="quantitative")
        .scale(reverse=False, domain=[0, msi_limit], zero=True)
        .axis(labelFontSize=TRACK_TICK_FONT_SIZE, labelPadding=2, tickCount=3)
        .title(None),
        y2=gs.Y2("value"),
    )
    .properties(
        width=SAMPLE_TRACK_WIDTH,
        height=MSI_HEIGHT,
        title=gs.Title(text="MSI", style="track-title"),
    )
)

stage_track = (
    gs.Chart(data["stage"])
    .mark_rect()
    .encode(
        x=gs.X("sample_order:I").axis(None).title(None),
        y=gs.Y(gs.datum(0), type="quantitative")
        .scale(reverse=False, domain=[0, 1], zero=True)
        .axis(None),
        y2=gs.Y2(gs.datum(1)),
        color=gs.Color("stage:N").scale(stage_scale).legend(None),
    )
    .properties(
        width=SAMPLE_TRACK_WIDTH,
        height=STAGE_HEIGHT,
        title=gs.Title(text="AJCC Stage", style="track-title"),
    )
)

# --- main matrix ---------------------------------------------------------------
# Keep one event table in the data helper. Each layer selects the classes that
# need its visual mark, so the same normalized events remain easy to inspect.

matrix_grid = (
    gs.Chart(data["grid"])
    .mark_rect(color="#ebebeb", stroke="white", strokeWidth=0.35)
    .encode(
        x=gs.X("sample_order:I").axis(None).title(None),
        y=gs.Y("gene:N").title(None),
    )
)

full_rect_layer = (
    gs.Chart(data["events"])
    .transform_filter(
        (gs.datum["class"] == "Amplification") | (gs.datum["class"] == "Deep Deletion")
    )
    .mark_rect()
    .encode(
        x=gs.X("sample_order:I").axis(None),
        y=gs.Y("gene:N"),
        color=gs.Color("class:N").scale(mutation_scale).legend(None),
    )
)

putative_rect_layer = (
    gs.Chart(data["events"])
    .transform_filter(
        (gs.datum["class"] != "Amplification")
        & (gs.datum["class"] != "Deep Deletion")
        & (gs.datum["class"] != "Structural Variant (putative driver)")
        & (gs.datum["class"] != "Structural Variant (putative passenger)")
    )
    .mark_rect()
    .encode(
        x=gs.X("sample_order:I").axis(None),
        y=gs.Y("gene:N", band=0.5),
        color=gs.Color("class:N").scale(mutation_scale).legend(None),
    )
)

star_layer = (
    gs.Chart(data["events"])
    .transform_filter(
        (gs.datum["class"] == "Structural Variant (putative driver)")
        | (gs.datum["class"] == "Structural Variant (putative passenger)")
    )
    .mark_point(shape="cross", size=80, filled=True, strokeWidth=0)
    .encode(
        x=gs.X("sample_order:I").axis(None),
        y=gs.Y("gene:N"),
        color=gs.Color("class:N").scale(mutation_scale).legend(None),
    )
)

matrix_panel = (
    matrix_grid + full_rect_layer + putative_rect_layer + star_layer
).properties(
    width=SAMPLE_TRACK_WIDTH,
    height=MATRIX_HEIGHT,
    scales={"y": {"domain": gene_order, "reverse": True, "padding": 0.03}},
)

percent_panel = (
    gs.Chart(data["genes"])
    .mark_text(align="right", dx=-3, size=10, color="#4b5563", clip="never")
    .encode(
        x=gs.value(1),
        y=gs.Y("gene:N").axis(None).title(None),
        text=gs.Text("label:N"),
    )
    .properties(width=PERCENT_WIDTH, height=MATRIX_HEIGHT)
)

count_grid = (
    gs.Chart(data["genes"][["gene"]])
    .mark_rect(color="#ebebeb", stroke="white", strokeWidth=0.35)
    .encode(
        y=gs.Y("gene:N").axis(None).title(None),
    )
)

count_bars = (
    gs.Chart(data["gene_counts"])
    .transform_stack(field="count", groupby=["gene"], as_=["_x0", "_x1"])
    .mark_rect()
    .encode(
        x=gs.X("_x0:Q")
        .scale(domain=[0, count_limit], zero=True)
        .title("Altered samples"),
        x2=gs.X2("_x1"),
        y=gs.Y("gene:N").axis(None).title(None),
        color=gs.Color("class:N").scale(mutation_scale).legend(None),
    )
)

gene_count_panel = (
    (count_grid + count_bars)
    .properties(width=COUNTS_WIDTH, height=MATRIX_HEIGHT)
    .resolve_scale(x="excluded")
)

matrix_summary = (
    gs.concat(percent_panel, gene_count_panel, columns=2, spacing=2)
    .properties(scales={"y": {"domain": gene_order, "reverse": True, "padding": 0.03}})
    .resolve_scale(x="excluded", y="shared")
)

# --- lower grouped heatmaps ----------------------------------------------------

mrna_panel = heatmap_panel(
    MRNA_GROUP,
    panel_height=MRNA_HEIGHT,
    domain=[-3.0, 0.0, 3.0],
    colors=["#2166ac", "#f7f7f7", "#b2182b"],
)

methylation_panel = heatmap_panel(
    METHYLATION_GROUP,
    panel_height=METHYLATION_HEIGHT,
    domain=[0.0, 0.5, 1.0],
    colors=["#eff6ff", "#60a5fa", "#1d4ed8"],
)

microbiome_panel = heatmap_panel(
    MICROBIOME_GROUP,
    panel_height=MICROBIOME_HEIGHT,
    domain=[1.4, 4.6, 7.8],
    colors=["#f6e3c4", "#c08457", "#7c3f00"],
)

sample_label_track = (
    gs.Chart(data["samples"])
    .mark_text(align="center", baseline="top", angle=90, size=9, paddingX=1)
    .encode(
        x=gs.X("sample_order:I", band=0).axis(None).title(None),
        x2=gs.X2("sample_order", band=1),
        y=gs.value(0.5),
        text=gs.Text("sample:N"),
    )
    .properties(width=SAMPLE_TRACK_WIDTH, height=SAMPLE_LABEL_HEIGHT)
)

sample_tracks = (
    gs.vconcat(
        burden_track,
        mutation_spectrum_track,
        msi_track,
        stage_track,
        matrix_panel,
        mrna_panel,
        methylation_panel,
        microbiome_panel,
        spacing=4,
    )
    .properties(
        scales={
            "x": {
                "domain": sample_domain,
                "paddingInner": 0,
                "paddingOuter": 0,
                "zoom": True,
            }
        },
        params=[
            gs.param(
                "sampleRuler",
                persist=False,
                ruler={
                    "encodings": ["x"],
                    "extent": "container",
                    "snap": False,
                    "mark": {"opacity": 0.3},
                },
            )
        ],
    )
    .resolve_scale(x="shared", y="independent")
    .resolve_axis(y="independent")
    .properties(width=SAMPLE_TRACK_WIDTH)
)

center_column = gs.vconcat(sample_tracks, sample_label_track, spacing=4).resolve_scale(
    x="shared", y="independent"
)

summary_column = gs.concat(
    empty_panel(height=TOP_TRACKS_HEIGHT),
    matrix_summary,
    columns=1,
    spacing=4,
)

chart = (
    gs.concat(center_column, summary_column, columns=2, spacing=2)
    .resolve_scale(x="shared", y="independent")
    .properties(width=SAMPLE_TRACK_WIDTH)
    .properties(
        title="TCGA Lung Adenocarcinoma (PanCancer Atlas), default sort method",
        width="container",
        viewportHeight="container",
        description=(
            "A TCGA LUAD oncoprint adapted from the pyoncoprint notebook, with "
            "sample-level burden tracks above, the sorted alteration matrix in the "
            "middle, and grouped quantitative heatmaps below."
        ),
    )
)
