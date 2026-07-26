"""Oncoplot.

A cohort-level alteration matrix with per-sample burden bars above, recurrently
altered genes in the center, and per-gene summary bars at the side.
"""

from __future__ import annotations

import math

import genome_spy as gs
from genome_spy.datasets._oncoprint import laml_oncoplot_data
from genome_spy.schema import Legend, Scale

META = {
    "category": "Oncoprints and cohort summaries",
    "tags": ("rect", "cohort", "real-data", "hconcat", "vconcat"),
    "order": 25,
    "height": 660,
    "max_width": 760,
}

CLASS_ORDER = [
    "In_Frame_Ins",
    "Frame_Shift_Del",
    "Missense_Mutation",
    "In_Frame_Del",
    "Frame_Shift_Ins",
    "Nonsense_Mutation",
    "Splice_Site",
    "Multi_Hit",
]

data = laml_oncoplot_data()
DATA_PREVIEW = {
    "Samples": data.samples,
    "Mutation matrix": data.matrix,
}

class_colors = (
    Scale()
    .domain(CLASS_ORDER)
    .range(
        [
            "#d53e4f",
            "#377eb8",
            "#33a02c",
            "#fff176",
            "#6a3d9a",
            "#ff1f1f",
            "#ff9800",
            "#111111",
        ]
    )
)

matrix_width = 540
percent_width = 52
counts_width = 120
tmb_height = 70
matrix_height = 352
tmb_limit = data.tmb_limit
count_limit = data.count_limit
sample_domain = data.sample_domain

mutation_legend = (
    Legend()
    .title("Mutation class")
    .orient("bottom")
    .direction("horizontal")
    .columns(4)
    .symbolSize(90)
)

# --- Visualization -------------------------------------------------------------

tmb = (
    gs.Chart(data.sample_tmb)
    .mark_rect()
    .encode(
        x=gs.X("x0:Q")
        .scale(domain=sample_domain, zero=True, zoom=True)
        .axis(None)
        .title(None),
        x2=gs.X2("x1"),
        y=gs.Y("y0:Q").scale(reverse=False, domain=[0, tmb_limit]).title("TMB"),
        y2=gs.Y2("y1"),
        color=gs.Color("class:N").scale(class_colors).legend(None),
    )
    .properties(width=matrix_width, height=tmb_height)
)

grid = (
    gs.Chart(data.grid)
    .mark_rect(color="#f1f3f5", stroke="white", strokeWidth=0.5)
    .encode(
        x=gs.X("x0:Q")
        .scale(domain=sample_domain, zero=True, zoom=True)
        .axis(None)
        .title(None),
        x2=gs.X2("x1"),
        y=gs.Y("gene:N").scale(reverse=False, padding=0.08).title(None),
    )
)

matrix = (
    gs.Chart(data.matrix)
    .mark_rect(stroke="white", strokeWidth=0.5)
    .encode(
        x=gs.X("x0:Q")
        .scale(domain=sample_domain, zero=True, zoom=True)
        .axis(None)
        .title(None),
        x2=gs.X2("x1"),
        y=gs.Y("gene:N").scale(reverse=False, padding=0.08).title(None),
        color=gs.Color("class:N").scale(class_colors).legend(mutation_legend),
    )
)

matrix_panel = (grid + matrix).properties(width=matrix_width, height=matrix_height)

percent_panel = (
    gs.Chart(data.percent_labels)
    .mark_text(align="right", dx=-2, size=11)
    .encode(
        x=gs.X("x:Q").scale(domain=[0, 1]).axis(None).title(None),
        y=gs.Y("gene:N").scale(reverse=False, padding=0.08).axis(None).title(None),
        text=gs.Text("label:N"),
    )
    .properties(width=percent_width, height=matrix_height)
)

percent_header = (
    gs.Chart([{"x": 1, "label": ""}])
    .mark_text(opacity=0)
    .encode(
        x=gs.X("x:Q").scale(domain=[0, 1]).axis(None).title(None),
        text=gs.Text("label:N"),
    )
    .properties(width=percent_width, height=tmb_height)
)

count_title = (
    gs.Chart([{"x": math.floor(count_limit / 2), "label": "No. of samples"}])
    .mark_text(size=11)
    .encode(
        x=gs.X("x:Q")
        .scale(reverse=False, domain=[0, count_limit])
        .axis(None)
        .title(None),
        text=gs.Text("label:N"),
    )
    .properties(width=counts_width, height=tmb_height)
)

count_bars = (
    gs.Chart(data.gene_counts)
    .mark_rect()
    .encode(
        x=gs.X("x0:Q")
        .scale(reverse=False, domain=[0, count_limit], zero=True)
        .title(None),
        x2=gs.X2("x1"),
        y=gs.Y("gene:N").scale(reverse=False, padding=0.08).axis(None).title(None),
        color=gs.Color("class:N").scale(class_colors).legend(None),
    )
    .properties(width=counts_width, height=matrix_height)
)

count_grid = (
    gs.Chart(data.count_grid)
    .mark_rect(color="#f1f3f5", stroke="white", strokeWidth=0.5)
    .encode(
        x=gs.X("x0:Q").scale(reverse=False, domain=[0, count_limit], zero=True),
        x2=gs.X2("x1"),
        y=gs.Y("gene:N").scale(reverse=False, padding=0.08).axis(None).title(None),
    )
    .properties(width=counts_width, height=matrix_height)
)

counts_panel = (count_grid + count_bars).properties(
    width=counts_width, height=matrix_height
)
left_panel = gs.vconcat(tmb, matrix_panel, spacing=4).resolve_scale(x="shared")
right_panel = gs.vconcat(percent_header, percent_panel, spacing=4).resolve_scale(
    x="independent"
)
count_panel = gs.vconcat(count_title, counts_panel, spacing=4).resolve_scale(
    x="independent"
)

summary = f"Altered in {data.altered_samples} ({data.altered_samples / data.total_samples:.2%}) of {data.total_samples} samples."

chart = (
    gs.hconcat(left_panel, right_panel, count_panel, spacing=4)
    .resolve_scale(x="independent")
    .properties(
        title=summary,
        description="A TCGA LAML oncoplot styled after the canonical maftools example with top mutation-burden bars, recurrently altered genes, percent labels, and right-side per-gene sample counts.",
    )
)
