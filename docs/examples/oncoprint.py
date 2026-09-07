"""Oncoplot.

A cohort-level alteration matrix with per-sample burden bars above, recurrently
altered genes in the center, and per-gene summary bars at the side.
"""

from __future__ import annotations

import genome_spy as gs
from genome_spy.datasets._oncoprint import laml_oncoplot_data
from genome_spy.schema import Legend, RulerMarkConfig, Scale

META = {
    "category": "Oncoprints and cohort summaries",
    "order": 25,
    "height": 530,
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

# Load the prepared mutation matrix and sample and gene summaries.
data = laml_oncoplot_data()
# Follow the mouse with a line to help identify the current sample column.
sample_ruler = gs.ruler(
    "sampleRuler",
    persist=False,
    encodings=["x"],
    snap=False,
    mark=RulerMarkConfig(opacity=0.3),
)

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

# Set the space reserved for the matrix and its surrounding summaries.
matrix_width = 400
percent_width = 52
counts_width = 120
tmb_height = 70
matrix_height = 352
tmb_limit = data["tmb_limit"]
count_limit = data["count_limit"]
sample_domain = data["sample_domain"]
gene_order = data["genes"].sort_values("gene_order")["gene"].tolist()
gene_scale = {"domain": gene_order, "reverse": True, "padding": 0.08}

mutation_legend = (
    Legend()
    .title("Mutation class")
    .orient("bottom")
    .direction("horizontal")
    .columns(3)
    .symbolSize(90)
)

# Stack mutation counts by class above each sample.
tmb = (
    gs.Chart(data["sample_tmb"])
    .transform_stack(
        field="count",
        groupby=["sample_order"],
        as_=["_y0", "_y1"],
    )
    .mark_rect()
    .encode(
        x=gs.X("sample_order:I").axis(None).title(None),
        y=gs.Y("_y0:Q").scale(reverse=False, domain=[0, tmb_limit]).title("TMB"),
        y2=gs.Y2("_y1"),
        color=gs.Color("class:N").scale(class_colors).legend(None),
    )
    .properties(width=matrix_width, height=tmb_height)
)

# Give every sample–gene cell a pale background.
grid = (
    gs.Chart(data["grid"])
    .mark_rect(color="#f1f3f5", stroke="white", strokeWidth=0.5)
    .encode(
        x=gs.X("sample_order:I").axis(None).title(None),
        y=gs.Y("gene:N").title(None),
    )
)

# Fill altered cells with their mutation-class colors.
matrix = (
    gs.Chart(data["events"])
    .mark_rect(stroke="white", strokeWidth=0.5)
    .encode(
        x=gs.X("sample_order:I").axis(None).title(None),
        y=gs.Y("gene:N").title(None),
        color=gs.Color("class:N").scale(class_colors).legend(mutation_legend),
    )
)

# Combine the background and mutations, then add the hover line.
matrix_panel = (
    (grid + matrix)
    .properties(
        width=matrix_width,
        height=matrix_height,
        scales={"y": gene_scale},
    )
    .add_params(sample_ruler)
)

# Show the percentage of samples with an alteration in each gene.
percent_panel = (
    gs.Chart(data["genes"])
    .mark_text(align="right", dx=-2, size=11)
    .encode(
        x=gs.value(1),
        y=gs.Y("gene:N").axis(None).title(None),
        text=gs.Text("label:N"),
    )
    .properties(width=percent_width, height=matrix_height, scales={"y": gene_scale})
)

# Leave space above the percentages to line them up with the matrix rows.
percent_header = (
    gs.Chart([{}])
    .mark_text(opacity=0)
    .properties(width=percent_width, height=tmb_height)
)

# Label the gene-count bars on the right.
count_title = (
    gs.Chart([{"label": "No. of samples"}])
    .mark_text(size=11)
    .encode(
        x=gs.value(0.5),
        text=gs.Text("label:N"),
    )
    .properties(width=counts_width, height=tmb_height)
)

# Stack the number of affected samples by mutation class for each gene.
count_bars = (
    gs.Chart(data["gene_counts"])
    .transform_stack(field="count", groupby=["gene"], as_=["_x0", "_x1"])
    .mark_rect()
    .encode(
        x=gs.X("_x0:Q")
        .scale(reverse=False, domain=[0, count_limit], zero=True)
        .title(None),
        x2=gs.X2("_x1"),
        y=gs.Y("gene:N").axis(None).title(None),
        color=gs.Color("class:N").scale(class_colors).legend(None),
    )
    .properties(width=counts_width, height=matrix_height)
)

# Add pale row backgrounds behind the gene-count bars.
count_grid = (
    gs.Chart(data["genes"][["gene"]])
    .mark_rect(color="#f1f3f5", stroke="white", strokeWidth=0.5)
    .encode(
        y=gs.Y("gene:N").axis(None).title(None),
    )
    .properties(width=counts_width, height=matrix_height)
)

counts_panel = (count_grid + count_bars).properties(
    width=counts_width, height=matrix_height, scales={"y": gene_scale}
)

# Keep the top bars and matrix columns aligned while zooming through samples.
sample_column = (
    gs.concat(tmb, matrix_panel, columns=1, spacing=4)
    .properties(
        scales={
            "x": {
                "domain": sample_domain,
                "paddingInner": 0,
                "paddingOuter": 0,
                "zoom": True,
            }
        }
    )
    .resolve_scale(x="shared", y="independent")
)
percent_column = gs.concat(percent_header, percent_panel, columns=1, spacing=4)
counts_column = gs.concat(count_title, counts_panel, columns=1, spacing=4)

summary = f"Altered in {data['altered_samples']} ({data['altered_samples'] / data['total_samples']:.2%}) of {data['total_samples']} samples."

# Place the matrix beside its percentages and counts, and add the cohort total.
chart = (
    gs.concat(sample_column, percent_column, counts_column, columns=3, spacing=4)
    .resolve_scale(x="independent", y="independent")
    .resolve_axis(y="independent")
    .properties(
        title=summary,
        description="A TCGA LAML oncoplot styled after the canonical maftools example with top mutation-burden bars, recurrently altered genes, percent labels, and right-side per-gene sample counts.",
    )
)
