"""LAML oncoplot with clinical and pathway annotations.

Combine alterations, pathway summaries, clinical annotations, and gene-level
statistics for the 200 patients in the maftools TCGA LAML example.
"""

import genome_spy as gs
from genome_spy.datasets import _load_table_bundle as load_data
from genome_spy.schema import OverhangConfig

META = {
    "category": "Oncoprints and cohort summaries",
    "order": 26,
    "height": 750,
    "max_width": 1100,
}

MATRIX_HEIGHT = 360
TMB_HEIGHT = 70
SNV_TRACK_HEIGHT = 60
SNV_PANEL_HEIGHT = 130

# Load the prepared patient data and gene summaries.
data = load_data(
    "tcga_laml_combined_oncoplot",
    (
        "burden",
        "copy_number",
        "events",
        "genes",
        "matrix_rows",
        "pathway_bounds",
        "pathway_events",
        "samples",
        "spectrum",
    ),
)
# DataFrames let the gallery store shared tables in separate Arrow files.
# Keep gene rows in the same order across the matrix and side bars.
row_scale = gs.Scale(
    name="genes",
    domain=[0, len(data["matrix_rows"]) - 1],
    reverse=True,
    padding=0,
    zoom=False,
)
sample_x = gs.X("sample_order:I").axis(None).title(None)
row_y = gs.Y("row:I").scale(row_scale).axis(None).title(None)

mutation_colors = gs.Scale(
    domain=[
        "Frame_Shift_Del",
        "Nonsense_Mutation",
        "Frame_Shift_Ins",
        "Splice_Site",
        "In_Frame_Ins",
        "Missense_Mutation",
        "In_Frame_Del",
        "Del",
        "Amp",
        "Multi_Hit",
        "Pathway",
    ],
    range=[
        "#1f78b4",
        "#e31a1c",
        "#6a3d9a",
        "#ff7f00",
        "#df3b53",
        "#33a02c",
        "#ffff66",
        "#4363ee",
        "#ee6677",
        "#111111",
        "#535c68",
    ],
)

mutation_color = (
    gs.Color("class:N")
    .scale(mutation_colors)
    .legend(title="Variant classification", columns=3)
)

fab_colors = gs.Scale(
    domain=["M1", "M2", "M4", "M5", "M3", "M0", "M6", "M7", "Unknown"],
    range=[
        "#e41a1c",
        "#377eb8",
        "#4daf4a",
        "#984ea3",
        "#ff7f00",
        "#ffff33",
        "#a65628",
        "#f781bf",
        "#dddddd",
    ],
)
spectrum_colors = gs.Scale(
    domain=["C>T", "C>G", "C>A", "T>A", "T>C", "T>G"],
    range=["#ff4136", "#3d4db7", "#2499ed", "#4daf4a", "#ffcc00", "#ff9800"],
)

# Count alterations per patient, including copy-number changes.
# These are counts, not mutations per megabase.
burden = (
    gs.Chart(data["burden"])
    .transform_stack(field="count", groupby=["sample_order"], as_=["low", "high"])
    .mark_rect()
    .encode(
        x=sample_x,
        y=gs.Y("low:Q")
        .scale(domain=[0, data["burden_limit"]])
        .axis(values=[0, data["burden_limit"]], minExtent=0, maxExtent=1)
        .title(None),
        y2="high:Q",
        color=mutation_color,
        tooltip=["sample:N", "class:N", "count:Q"],
    )
    .properties(height=TMB_HEIGHT)
)

# Give empty cells a pale background; leave hover details to the colored cells.
background = (
    gs.Chart(data["matrix_rows"])
    .mark_rect(color="#edf0f2", tooltip=None)
    .encode(y=row_y)
)
# Show copy-number changes behind the sequence mutations.
copy_number = (
    gs.Chart(data["copy_number"])
    .mark_rect()
    .encode(
        x=sample_x,
        y=row_y,
        color=mutation_color,
        tooltip=["sample:N", "gene:N", "class:N"],
    )
)

# Color each mutation by its class.
mutations = (
    gs.Chart(data["events"])
    .mark_rect(yOffset=2, y2Offset=-2)
    .encode(
        x=sample_x,
        y=row_y,
        color=mutation_color,
        tooltip=["sample:N", "gene:N", "class:N"],
    )
)

# Fill the summary cell if any gene in the group is altered.
pathway_cells = (
    gs.Chart(data["pathway_events"])
    .mark_rect(yOffset=1, y2Offset=-1)
    .encode(
        x=sample_x,
        y=row_y,
        color=mutation_color,
        tooltip=["sample:N", "gene:N"],
    )
)

# Separate neighboring patients with thin white lines.
grid = (
    gs.Chart(data["samples"])
    .mark_rule(color="white", size=0.3, tooltip=None)
    .encode(x=gs.X("sample_order:I", band=0).axis(None).title(None))
)

# Add a grey dot to variants with alternate allele C.
alt_c = (
    gs.Chart(data["events"])
    .transform_filter(gs.datum.alt_c)
    # Make dots easier to see when zoomed in, up to 8 pixels across.
    .mark_point(
        filled=True,
        size=gs.expr(gs.expr.min(8 * gs.expr.pow(gs.Expression("zoomLevel"), 1.5), 64)),
        color="#aaaaaa",
    )
    .encode(
        x=sample_x,
        y=row_y,
        shape=gs.Shape("feature:N")
        .scale(domain=["Alternate allele C"], range=["circle"])
        .legend(title="Additional feature"),
        tooltip=["sample:N", "gene:N", "class:N", "feature:N"],
    )
)

# Outline each gene group, keeping both borders inside the chart.
outlines = (
    gs.Chart(data["pathway_bounds"])
    .mark_rect(
        fillOpacity=0,
        stroke="#535c68",
        strokeWidth=1,
        xOffset=0.5,
        x2Offset=-0.5,
        tooltip=None,
        clip=False,
    )
    .encode(y=gs.Y("start:I").scale(row_scale).axis(None), y2="end:I")
)

# Combine the cells, dots, and outlines into the gene matrix.
matrix = (
    background + copy_number + mutations + pathway_cells + grid + alt_c + outlines
).properties(height=MATRIX_HEIGHT)

# Add each patient's FAB classification below the matrix.
fab = (
    gs.Chart(data["samples"])
    .mark_rect()
    .encode(
        x=sample_x,
        color=gs.Color("FAB_classification:N")
        .scale(fab_colors)
        .legend(title="FAB classification", columns=3),
        tooltip=["sample:N", "FAB_classification:N"],
    )
    .properties(height=18)
)

# Show follow-up time with darker colors for longer follow-up.
followup = (
    gs.Chart(data["samples"])
    .transform_filter(gs.expr.isValid(gs.datum.days_to_last_followup))
    .mark_rect()
    .encode(
        x=sample_x,
        color=gs.Color("days_to_last_followup:Q")
        .scale(domain=[0, 2861], range=["#f7fcf0", "#7bccc4", "#084081"])
        .legend(title="Follow-up (days)", gradientLength=130, tickCount=3),
        tooltip=["sample:N", "days_to_last_followup:Q"],
    )
    .properties(height=18)
)

# Stack the six substitution types to show their proportions per patient.
spectrum = (
    gs.Chart(data["spectrum"])
    .transform_stack(field="percent", groupby=["sample_order"], as_=["low", "high"])
    .mark_rect()
    .encode(
        x=sample_x,
        y=gs.Y("low:Q").scale(domain=[0, 100]).axis(None),
        y2="high:Q",
        color=gs.Color("substitution:N")
        .scale(spectrum_colors)
        .legend(
            title="SNV substitutions", orient="right", direction="vertical", columns=2
        ),
        tooltip=["sample:N", "substitution:N", "percent:Q"],
    )
    .properties(height=SNV_TRACK_HEIGHT)
)

# Stack the patient tracks so their columns line up while zooming.
sample_column = (
    gs.vconcat(
        gs.layer(burden).resolve_scale(y="excluded").properties(height=TMB_HEIGHT),
        matrix,
        gs.layer(fab).resolve_scale(color="excluded").properties(height=18),
        gs.layer(followup).resolve_scale(color="excluded").properties(height=18),
        # Put the substitution legend beside this track, in the empty space.
        gs.layer(spectrum)
        .resolve_scale(y="excluded", color="excluded")
        .resolve_legend(default="excluded")
        .properties(
            height=SNV_PANEL_HEIGHT,
            overhang=OverhangConfig(left=False, right=False),
        ),
        spacing=8,
    )
    .properties(
        width=gs.SizeDef(grow=1),
        scales=gs.scales(
            x=gs.Scale(
                domain=data["sample_domain"], zoom=True, paddingInner=0, paddingOuter=0
            )
        ),
    )
    .resolve_scale(x="shared", y="shared", color="shared")
    .resolve_axis(x="independent", y="independent")
)

# Show mean variant allele frequency to the left of each gene.
vaf = (
    gs.Chart(data["genes"])
    .mark_rect(color="#535c68", yOffset=1, y2Offset=-1)
    .encode(
        x=gs.X("vaf:Q").scale(domain=[0, 100], reverse=True).axis(None),
        x2=gs.datum(0),
        y=row_y,
        tooltip=["gene:N", "vaf:Q"],
    )
    .properties(width=85, height=MATRIX_HEIGHT)
)
# Label the genes and pathway summaries.
row_labels = (
    gs.Chart(data["matrix_rows"])
    .mark_text(align="right", size=11, fontStyle="italic")
    .encode(
        x=gs.value(1),
        y=row_y,
        text="gene:N",
    )
    .properties(width=60, height=MATRIX_HEIGHT)
)

# Show the percentage of patients affected in each row.
percentages = (
    gs.Chart(data["matrix_rows"])
    .mark_text(align="left", size=10)
    .encode(
        x=gs.value(0),
        y=row_y,
        text="percent_label:N",
        tooltip=["gene:N", "altered_percent:Q"],
    )
    .properties(width=32, height=MATRIX_HEIGHT)
)

# Show each gene's MutSig result on the right; leave missing values blank.
qvalues = (
    gs.Chart(data["genes"])
    .transform_filter(gs.expr.isValid(gs.datum.neglog_q))
    .mark_rect(color="#535c68", yOffset=1, y2Offset=-1)
    .encode(
        x=gs.X("neglog_q:Q").scale(domain=[0, 12.64176]).axis(None),
        x2=gs.datum(0),
        y=row_y,
        tooltip=["gene:N", "neglog_q:Q"],
    )
    .properties(width=100, height=MATRIX_HEIGHT)
)
blank = gs.Chart([{}]).mark_point(opacity=0).properties(width=0, height=100)


def bar_header(title: str, left: str, right: str, width: int) -> gs.LayerChart:
    """Keep side-bar headings inside the common top-track height."""
    labels = (
        gs.Chart(
            [
                {"x": 0.5, "y": 0.27, "label": title},
                {"x": 0.06, "y": 0.09, "label": left},
                {"x": 0.92, "y": 0.09, "label": right},
            ]
        )
        .mark_text(size=10)
        .encode(
            x=gs.X("x:Q").scale(domain=[0, 1]).axis(None),
            y=gs.Y("y:Q").scale(domain=[0, 1]).axis(None),
            text="label:N",
        )
    )
    line = gs.Chart([{}]).mark_rule(color="#535c68", size=1).encode(y=gs.value(0))
    return (
        (line + labels)
        .properties(width=width, height=TMB_HEIGHT)
        .resolve_scale(y="excluded")
    )


def track_label(label: str) -> gs.Chart:
    """Place a clinical track label in the right-hand column."""
    return (
        gs.Chart([{"label": label}])
        .mark_text(align="left", size=10)
        .encode(
            x=gs.value(0),
            text="label:N",
        )
        .properties(width=150, height=18)
    )


# Put the headings above the side bars, alongside the top patient track.
left_column = gs.vconcat(
    bar_header("VAF (%)", "100", "0", 85)
    | blank.mark_text(angle=-90, size=11)
    .encode(text=gs.value("TMB"), x=gs.value(0.8), y=gs.value(0.5))
    .properties(width=60, height=TMB_HEIGHT),
    (vaf | row_labels).resolve_scale(x="independent"),
    spacing=8,
).resolve_scale(x="independent", y="shared")

right_column = gs.vconcat(
    blank.properties(width=32, height=TMB_HEIGHT)
    | bar_header("−log10 q", "0", "12.64", 100),
    (percentages | qvalues).resolve_scale(x="independent"),
    track_label("FAB classification"),
    track_label("Follow-up (days)"),
    spacing=8,
).resolve_scale(x="independent", y="shared", color="independent")

# Place the side bars around the matrix, keeping every gene row aligned.
panels = gs.hconcat(left_column, sample_column, right_column, spacing=8).resolve_scale(
    x="independent", y="shared", color="independent"
)

# Put the remaining legends below the chart and add the patient-count title.
chart = (
    panels.resolve_legend(default="collected")
    .configure_legend(
        orient="bottom",
        direction="horizontal",
        titleOrient="top",
        labelFontSize=10,
        symbolSize=65,
        layout={"right": {"anchor": "end"}},
    )
    .properties(
        title=f"Altered in {data['altered_samples']} ({100 * data['altered_samples'] / len(data['samples']):.1f}%) of {len(data['samples'])} samples",
        description="TCGA LAML: 18 genes, five pathway summary rows, all 200 patients, and maftools-style clinical and burden tracks.",
    )
)
