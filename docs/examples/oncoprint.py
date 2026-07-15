"""Oncoplot.

A cohort-level alteration matrix with per-sample burden bars above, recurrently
altered genes in the center, and per-gene summary bars at the side.
"""

from __future__ import annotations

import math

import pandas as pd

import genome_spy as gs
from genome_spy.datasets import load_dataset
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


def curated_laml_oncoplot() -> dict[str, pd.DataFrame | int]:
    """Load the curated TCGA LAML oncoplot payload."""
    payload = load_dataset("tcga_laml_oncoprint", as_format="json")

    samples = pd.DataFrame(payload["samples"]).sort_values("sample_order").copy()
    genes = pd.DataFrame(payload["genes"]).sort_values("gene_order").copy()
    matrix = pd.DataFrame(payload["matrix"]).copy()
    grid = pd.DataFrame(payload["grid"]).copy()
    sample_tmb = pd.DataFrame(payload["sample_tmb"]).copy()
    gene_counts = pd.DataFrame(payload["gene_counts"]).copy()
    percent_labels = pd.DataFrame(payload["percent_labels"]).copy()

    sample_order = samples["sample"].tolist()
    gene_order = genes["gene"].tolist()

    for frame in [samples, matrix, grid, sample_tmb]:
        frame["sample"] = pd.Categorical(
            frame["sample"], categories=sample_order, ordered=True
        )
    for frame in [genes, matrix, grid, gene_counts, percent_labels]:
        frame["gene"] = pd.Categorical(
            frame["gene"], categories=gene_order, ordered=True
        )

    genes["zero"] = 0
    percent_labels["x"] = 0

    return {
        "samples": samples,
        "genes": genes,
        "matrix": matrix,
        "grid": grid,
        "sample_tmb": sample_tmb,
        "gene_counts": gene_counts,
        "percent_labels": percent_labels,
        "total_samples": int(payload["total_samples"]),
        "altered_samples": int(payload["altered_samples"]),
    }


loaded = curated_laml_oncoplot()
sample_data = loaded["samples"]
gene_data = loaded["genes"]
matrix_data = loaded["matrix"]
grid_data = loaded["grid"]
sample_tmb_data = loaded["sample_tmb"]
gene_count_data = loaded["gene_counts"]
percent_data = loaded["percent_labels"]
total_samples = loaded["total_samples"]
altered_samples = loaded["altered_samples"]

percent_data = percent_data.copy()
percent_data["x"] = 1

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
tmb_limit = int(sample_data["tmb_total"].max())
count_limit = int(gene_data["altered_samples"].max())

mutation_legend = (
    Legend()
    .title("Mutation class")
    .orient("bottom")
    .direction("horizontal")
    .columns(4)
    .symbolSize(90)
)

count_grid_data = gene_data[["gene"]].copy()
count_grid_data["x0"] = 0
count_grid_data["x1"] = count_limit

# --- Visualization -------------------------------------------------------------

tmb = (
    gs.Chart(sample_tmb_data)
    .mark_rect()
    .encode(
        x=gs.X("sample:N").axis(None).title(None),
        y=gs.Y("y0:Q").scale(reverse=False, domain=[0, tmb_limit]).title("TMB"),
        y2=gs.Y2("y1"),
        color=gs.Color("class:N").scale(class_colors).legend(None),
    )
    .properties(width=matrix_width, height=tmb_height)
)

grid = (
    gs.Chart(grid_data)
    .mark_rect(color="#f1f3f5", stroke="white", strokeWidth=0.5)
    .encode(
        x=gs.X("sample:N").axis(None).title(None),
        y=gs.Y("gene:N").scale(reverse=False, padding=0.08).title(None),
    )
)

matrix = (
    gs.Chart(matrix_data)
    .mark_rect(stroke="white", strokeWidth=0.5)
    .encode(
        x=gs.X("sample:N").axis(None).title(None),
        y=gs.Y("gene:N").scale(reverse=False, padding=0.08).title(None),
        color=gs.Color("class:N").scale(class_colors).legend(mutation_legend),
    )
)

matrix_panel = (grid + matrix).properties(width=matrix_width, height=matrix_height)

percent_panel = (
    gs.Chart(percent_data)
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
    gs.Chart(gene_count_data)
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
    gs.Chart(count_grid_data)
    .mark_rect(color="#f1f3f5", stroke="white", strokeWidth=0.5)
    .encode(
        x=gs.X("x0:Q").scale(reverse=False, domain=[0, count_limit], zero=True),
        x2=gs.X2("x1"),
        y=gs.Y("gene:N").scale(reverse=False, padding=0.08).axis(None).title(None),
    )
    .properties(width=counts_width, height=matrix_height)
)

top_row = gs.hconcat(tmb, percent_header, count_title, spacing=4).resolve_scale(
    x="independent"
)
counts_panel = (count_grid + count_bars).properties(
    width=counts_width, height=matrix_height
)
middle_row = gs.hconcat(
    matrix_panel, percent_panel, counts_panel, spacing=4
).resolve_scale(x="independent")

summary = f"Altered in {altered_samples} ({altered_samples / total_samples:.2%}) of {total_samples} samples."

chart = (
    gs.vconcat(
        top_row,
        middle_row,
    )
    .resolve_scale(x="independent")
    .properties(
        title=summary,
        description="A TCGA LAML oncoplot styled after the canonical maftools example with top mutation-burden bars, recurrently altered genes, percent labels, and right-side per-gene sample counts.",
    )
)
