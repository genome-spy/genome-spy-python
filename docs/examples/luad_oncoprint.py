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
    "tags": ("oncoprint", "cohort", "heatmap", "real-data", "zoom"),
    "order": 35,
    "height": 1160,
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

MATRIX_WIDTH = 1180
SUMMARY_WIDTH = 220
PERCENT_WIDTH = 44
COUNTS_WIDTH = 120
TMB_HEIGHT = 54
SPECTRUM_HEIGHT = 54
MSI_HEIGHT = 40
STAGE_HEIGHT = 24
MATRIX_HEIGHT = 430
MRNA_HEIGHT = 64
METHYLATION_HEIGHT = 64
MICROBIOME_HEIGHT = 28
TRACK_TICK_FONT_SIZE = 9
HEATMAP_LABEL_FONT_SIZE = 9

MRNA_GROUP = "mRNA expression z-scores relative to diploid samples (RNA Seq V2 RSEM)"
METHYLATION_GROUP = "Methylation (HM27 and HM450 merge)"
MICROBIOME_GROUP = "Microbiome Signatures (log RNA Seq CPM)"


data = luad_oncoprint_data()

DATA_PREVIEW = {
    "Samples": data.samples,
    "Mutation matrix": data.full_rect_events,
}

sample_domain = data.sample_domain
gene_order = data.gene_order
burden_limit = data.burden_limit
spectrum_limit = data.spectrum_limit
count_limit = data.count_limit
msi_limit = data.msi_limit

mutation_scale = Scale().domain(CLASS_ORDER).range(CLASS_COLORS)
spectrum_scale = Scale().domain(SPECTRUM_ORDER).range(SPECTRUM_COLORS)
stage_scale = Scale().domain(STAGE_ORDER).range(STAGE_COLORS)


def blank_panel(*, width: int, height: int) -> gs.Chart:
    """Invisible spacer panel used to align the right summary column."""
    return (
        gs.Chart([{"x0": 0, "x1": 1, "y0": 0, "y1": 1}])
        .mark_rect(opacity=0)
        .encode(
            x=gs.X("x0:Q").scale(domain=[0, 1], zero=True).axis(None).title(None),
            x2=gs.X2("x1"),
            y=gs.Y("y0:Q").scale(reverse=False, domain=[0, 1], zero=True).axis(None),
            y2=gs.Y2("y1"),
        )
        .properties(width=width, height=height)
    )


def heatmap_panel(
    group_name: str,
    *,
    panel_height: int,
    domain: list[float],
    colors: list[str],
) -> gs.Chart:
    """Render one grouped quantitative heatmap block."""
    panel_data = data.heatmap_cells[data.heatmap_cells["group"] == group_name]
    rows = data.heatmap_rows[data.heatmap_rows["group"] == group_name]
    track_order = rows.sort_values("track_order")["track"].tolist()

    return (
        gs.Chart(panel_data)
        .mark_rect(stroke="white", strokeWidth=0.35)
        .encode(
            x=gs.X("x0:Q")
            .scale(domain=data.sample_domain, zero=True, zoom=True)
            .axis(None)
            .title(None),
            x2=gs.X2("x1"),
            y=gs.Y("track:N")
            .scale(domain=track_order, reverse=False, padding=0.02)
            .axis(title=None, labelFontSize=HEATMAP_LABEL_FONT_SIZE, labelLimit=74),
            color=gs.Color("value:Q").scale(domain=domain, range=colors).legend(None),
        )
        .properties(
            width=MATRIX_WIDTH,
            height=panel_height,
        )
    )


# --- top sample-aligned tracks -------------------------------------------------

burden_track = (
    gs.Chart(data.sample_burden)
    .mark_rect()
    .encode(
        x=gs.X("x0:Q")
        .scale(domain=sample_domain, zero=True, zoom=True)
        .axis(None)
        .title(None),
        x2=gs.X2("x1"),
        y=gs.Y("y0:Q")
        .scale(reverse=False, domain=[0, burden_limit], zero=True)
        .axis(labelFontSize=TRACK_TICK_FONT_SIZE, labelPadding=2, tickCount=3)
        .title("TMB"),
        y2=gs.Y2("y1"),
        color=gs.Color("class:N").scale(mutation_scale).legend(None),
    )
    .properties(width=MATRIX_WIDTH, height=TMB_HEIGHT)
)

mutation_spectrum_track = (
    gs.Chart(data.mutation_spectrum)
    .mark_rect()
    .encode(
        x=gs.X("x0:Q")
        .scale(domain=sample_domain, zero=True, zoom=True)
        .axis(None)
        .title(None),
        x2=gs.X2("x1"),
        y=gs.Y("y0:Q")
        .scale(reverse=False, domain=[0, spectrum_limit], zero=True)
        .axis(labelFontSize=TRACK_TICK_FONT_SIZE, labelPadding=2, tickCount=3)
        .title("Mutation spectrum"),
        y2=gs.Y2("y1"),
        color=gs.Color("class:N").scale(spectrum_scale).legend(None),
    )
    .properties(width=MATRIX_WIDTH, height=SPECTRUM_HEIGHT)
)

msi_track = (
    gs.Chart(data.msi)
    .mark_rect(color="#15803d")
    .encode(
        x=gs.X("x0:Q")
        .scale(domain=sample_domain, zero=True, zoom=True)
        .axis(None)
        .title(None),
        x2=gs.X2("x1"),
        y=gs.Y("y0:Q")
        .scale(reverse=False, domain=[0, msi_limit], zero=True)
        .axis(labelFontSize=TRACK_TICK_FONT_SIZE, labelPadding=2, tickCount=3)
        .title("MSI"),
        y2=gs.Y2("value"),
    )
    .properties(width=MATRIX_WIDTH, height=MSI_HEIGHT)
)

stage_track = (
    gs.Chart(data.stage)
    .mark_rect()
    .encode(
        x=gs.X("x0:Q")
        .scale(domain=sample_domain, zero=True, zoom=True)
        .axis(None)
        .title(None),
        x2=gs.X2("x1"),
        y=gs.Y("y0:Q").scale(reverse=False, domain=[0, 1], zero=True).axis(None),
        y2=gs.Y2("y1"),
        color=gs.Color("stage:N").scale(stage_scale).legend(None),
    )
    .properties(width=MATRIX_WIDTH, height=STAGE_HEIGHT)
)

# --- main matrix ---------------------------------------------------------------

matrix_grid = (
    gs.Chart(data.grid)
    .mark_rect(color="#ebebeb", stroke="white", strokeWidth=0.35)
    .encode(
        x=gs.X("x0:Q")
        .scale(domain=sample_domain, zero=True, zoom=True)
        .axis(None)
        .title(None),
        x2=gs.X2("x1"),
        y=gs.Y("gene:N").scale(reverse=False, padding=0.03).title(None),
    )
)

full_rect_layer = (
    gs.Chart(data.full_rect_events)
    .mark_rect()
    .encode(
        x=gs.X("x0:Q").scale(domain=sample_domain, zero=True, zoom=True).axis(None),
        x2=gs.X2("x1"),
        y=gs.Y("gene:N").scale(reverse=False, padding=0.03),
        color=gs.Color("class:N").scale(mutation_scale).legend(None),
    )
)

half_rect_layer = (
    gs.Chart(data.half_rect_events)
    .mark_rect()
    .encode(
        x=gs.X("x0:Q").scale(domain=sample_domain, zero=True, zoom=True).axis(None),
        x2=gs.X2("x1"),
        y=gs.Y("gene:N").scale(reverse=False, padding=0.03),
        color=gs.Color("class:N").scale(mutation_scale).legend(None),
    )
)

triangle_layer = (
    gs.Chart(data.triangle_events)
    .mark_point(shape="triangle-right", size=105, filled=True, strokeWidth=0)
    .encode(
        x=gs.X("x:Q").scale(domain=sample_domain, zero=True, zoom=True).axis(None),
        y=gs.Y("gene:N").scale(reverse=False, padding=0.03),
        color=gs.Color("class:N").scale(mutation_scale).legend(None),
    )
)

star_layer = (
    gs.Chart(data.star_events)
    .mark_point(shape="star", size=80, filled=True, strokeWidth=0)
    .encode(
        x=gs.X("x:Q").scale(domain=sample_domain, zero=True, zoom=True).axis(None),
        y=gs.Y("gene:N").scale(reverse=False, padding=0.03),
        color=gs.Color("class:N").scale(mutation_scale).legend(None),
    )
)

matrix_panel = (
    matrix_grid + full_rect_layer + half_rect_layer + triangle_layer + star_layer
).properties(width=MATRIX_WIDTH, height=MATRIX_HEIGHT)

percent_panel = (
    gs.Chart(data.percent_labels)
    .mark_text(align="right", dx=-3, size=10, color="#4b5563")
    .encode(
        x=gs.X("x:Q").scale(domain=[0, 1]).axis(None).title(None),
        y=gs.Y("gene:N")
        .scale(domain=gene_order, reverse=False, padding=0.03)
        .axis(None)
        .title(None),
        text=gs.Text("label:N"),
    )
    .properties(width=PERCENT_WIDTH, height=MATRIX_HEIGHT)
)

count_grid = (
    gs.Chart(data.count_grid)
    .mark_rect(color="#ebebeb", stroke="white", strokeWidth=0.35)
    .encode(
        x=gs.X("x0:Q")
        .scale(domain=[0, count_limit], zero=True)
        .title("Altered samples"),
        x2=gs.X2("x1"),
        y=gs.Y("gene:N")
        .scale(domain=gene_order, reverse=False, padding=0.03)
        .axis(None)
        .title(None),
    )
)

count_bars = (
    gs.Chart(data.gene_counts)
    .mark_rect()
    .encode(
        x=gs.X("x0:Q")
        .scale(domain=[0, count_limit], zero=True)
        .title("Altered samples"),
        x2=gs.X2("x1"),
        y=gs.Y("gene:N")
        .scale(domain=gene_order, reverse=False, padding=0.03)
        .axis(None)
        .title(None),
        color=gs.Color("class:N").scale(mutation_scale).legend(None),
    )
)

gene_count_panel = (count_grid + count_bars).properties(
    width=COUNTS_WIDTH, height=MATRIX_HEIGHT
)

matrix_summary_row = gs.hconcat(
    percent_panel,
    gene_count_panel,
    spacing=4,
).resolve_scale(y="shared", x="independent")

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

summary_width = PERCENT_WIDTH + COUNTS_WIDTH + 4

center_column = (
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
    .resolve_scale(x="shared", y="independent")
    .resolve_axis(y="independent")
    .properties(width=MATRIX_WIDTH)
)

right_column = gs.vconcat(
    blank_panel(width=summary_width, height=TMB_HEIGHT),
    blank_panel(width=summary_width, height=SPECTRUM_HEIGHT),
    blank_panel(width=summary_width, height=MSI_HEIGHT),
    blank_panel(width=summary_width, height=STAGE_HEIGHT),
    matrix_summary_row,
    blank_panel(width=summary_width, height=MRNA_HEIGHT),
    blank_panel(width=summary_width, height=METHYLATION_HEIGHT),
    blank_panel(width=summary_width, height=MICROBIOME_HEIGHT),
    spacing=4,
)

chart = (
    gs.hconcat(
        center_column,
        right_column,
        spacing=4,
    )
    .resolve_scale(x="independent", y="independent")
    .properties(
        title=data.title,
        description=(
            "A TCGA LUAD oncoprint adapted from the pyoncoprint notebook, with "
            "sample-level burden tracks above, the sorted alteration matrix in the "
            "middle, and grouped quantitative heatmaps below."
        ),
    )
)
