"""Oncoplot.

A cohort-level alteration matrix with per-sample burden bars above, recurrently
altered genes in the center, and per-gene summary bars at the side.
"""

from __future__ import annotations

import genome_spy as gs
from genome_spy.datasets._oncoprint import laml_oncoplot_data
from genome_spy.schema import Legend, Scale

META = {
    "category": "Oncoprints and cohort summaries",
    "order": 25,
    "height": 480,
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

matrix_width = 400
percent_width = 52
counts_width = 120
tmb_height = 70
matrix_height = 352
tmb_limit = data["tmb_limit"]
count_limit = data["count_limit"]
sample_domain = data["sample_domain"]
gene_order = data["genes"].sort_values("gene_order")["gene"].tolist()

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

grid = (
    gs.Chart(data["grid"])
    .mark_rect(color="#f1f3f5", stroke="white", strokeWidth=0.5)
    .encode(
        x=gs.X("sample_order:I").axis(None).title(None),
        y=gs.Y("gene:N").title(None),
    )
)

matrix = (
    gs.Chart(data["events"])
    .mark_rect(stroke="white", strokeWidth=0.5)
    .encode(
        x=gs.X("sample_order:I").axis(None).title(None),
        y=gs.Y("gene:N").title(None),
        color=gs.Color("class:N").scale(class_colors).legend(mutation_legend),
    )
)

matrix_panel = (grid + matrix).properties(
    width=matrix_width,
    height=matrix_height,
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
                "snap": False,
                "mark": {"opacity": 0.3},
            },
        )
    ],
)

percent_panel = (
    gs.Chart(data["genes"])
    .mark_text(align="right", dx=-2, size=11)
    .encode(
        x=gs.value(1),
        y=gs.Y("gene:N").axis(None).title(None),
        text=gs.Text("label:N"),
    )
    .properties(width=percent_width, height=matrix_height)
)

percent_header = (
    gs.Chart([{}])
    .mark_text(opacity=0)
    .properties(width=percent_width, height=tmb_height)
)

count_title = (
    gs.Chart([{"label": "No. of samples"}])
    .mark_text(size=11)
    .encode(
        x=gs.value(0.5),
        text=gs.Text("label:N"),
    )
    .properties(width=counts_width, height=tmb_height)
)

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

count_grid = (
    gs.Chart(data["genes"][["gene"]])
    .mark_rect(color="#f1f3f5", stroke="white", strokeWidth=0.5)
    .encode(
        y=gs.Y("gene:N").axis(None).title(None),
    )
    .properties(width=counts_width, height=matrix_height)
)

counts_panel = (
    (count_grid + count_bars)
    .properties(width=counts_width, height=matrix_height)
    .resolve_scale(x="excluded")
)

matrix_row = (
    gs.concat(matrix_panel, percent_panel, counts_panel, columns=3, spacing=4)
    .properties(scales={"y": {"domain": gene_order, "reverse": True, "padding": 0.08}})
    .resolve_scale(x="excluded", y="shared")
)

summary = f"Altered in {data['altered_samples']} ({data['altered_samples'] / data['total_samples']:.2%}) of {data['total_samples']} samples."

chart = (
    gs.concat(
        gs.concat(tmb, percent_header, count_title, columns=3, spacing=4),
        matrix_row,
        columns=1,
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
    )
    .resolve_scale(x="shared", y="independent")
    .resolve_axis(y="independent")
    .properties(
        title=summary,
        description="A TCGA LAML oncoplot styled after the canonical maftools example with top mutation-burden bars, recurrently altered genes, percent labels, and right-side per-gene sample counts.",
    )
)
