"""Single-source chart objects used by the Composition guide."""

# composition-data-start
import genome_spy as gs


measurements = [
    {"position": 1, "signal": 2.1, "quality": 0.72, "group": "control", "label": "C1"},
    {"position": 2, "signal": 2.8, "quality": 0.84, "group": "control", "label": "C2"},
    {"position": 3, "signal": 3.2, "quality": 0.66, "group": "control", "label": "C3"},
    {"position": 1, "signal": 2.4, "quality": 0.78, "group": "treated", "label": "T1"},
    {"position": 2, "signal": 3.5, "quality": 0.91, "group": "treated", "label": "T2"},
    {"position": 3, "signal": 4.3, "quality": 0.88, "group": "treated", "label": "T3"},
]
# composition-data-end


# composition-layer-start
points = gs.Chart().mark_point(filled=True, size=100)
labels = gs.Chart().mark_text(dy=-12).encode(text="label:N")

layered_chart = (
    (points + labels)
    .encode(
        x=gs.X("position:Q").title("Position"),
        y=gs.Y("signal:Q").scale(zero=False).title("Signal"),
        color=gs.Color("group:N").legend(title="Group"),
    )
    .properties(data=measurements, title="Points with labels")
)
# composition-layer-end


# composition-vertical-start
signal_track = (
    gs.Chart()
    .mark_point(filled=True, size=90)
    .encode(
        y=gs.Y("signal:Q").scale(zero=False).title("Signal"),
        color="group:N",
    )
    .properties(height=150)
    .with_view(stroke="lightgray")
)
quality_track = (
    gs.Chart()
    .mark_point(filled=True, size=90, color="#6f6f6f")
    .encode(y=gs.Y("quality:Q").scale(domain=[0, 1]).title("Quality"))
    .properties(height=90)
    .with_view(stroke="lightgray")
)

vertical_chart = (
    (signal_track & quality_track)
    .encode(x=gs.X("position:Q").scale(domain=[0.5, 3.5], zoom=True))
    .properties(data=measurements, spacing=20, title="Two aligned tracks")
    .resolve_scale(x="shared", y="independent")
    .resolve_axis(x="shared", y="independent")
)
# composition-vertical-end


# composition-horizontal-start
control_panel = (
    gs.Chart()
    .transform_filter("datum.group == 'control'")
    .mark_point(filled=True, size=100, color="#4c78a8")
    .encode(x="position:Q", y=gs.Y("signal:Q").scale(zero=False))
    .properties(title="Control")
    .with_view(stroke="lightgray")
)
treated_panel = (
    gs.Chart()
    .transform_filter("datum.group == 'treated'")
    .mark_point(filled=True, size=100, color="#e45756")
    .encode(x="position:Q", y=gs.Y("signal:Q").scale(zero=False))
    .properties(title="Treated")
    .with_view(stroke="lightgray")
)

horizontal_chart = (
    (control_panel | treated_panel)
    .properties(data=measurements, spacing=20)
    .resolve_scale(x="shared", y="shared")
    .resolve_axis(x="independent", y="shared")
)
# composition-horizontal-end


# composition-grid-start
memberships = [
    {"column": 0, "row": 0, "member": True, "columnTotal": 2, "rowTotal": 2},
    {"column": 0, "row": 1, "member": True, "columnTotal": 2, "rowTotal": 2},
    {"column": 0, "row": 2, "member": False, "columnTotal": 2, "rowTotal": 2},
    {"column": 1, "row": 0, "member": True, "columnTotal": 3, "rowTotal": 2},
    {"column": 1, "row": 1, "member": True, "columnTotal": 3, "rowTotal": 2},
    {"column": 1, "row": 2, "member": True, "columnTotal": 3, "rowTotal": 2},
    {"column": 2, "row": 0, "member": False, "columnTotal": 1, "rowTotal": 2},
    {"column": 2, "row": 1, "member": False, "columnTotal": 1, "rowTotal": 2},
    {"column": 2, "row": 2, "member": True, "columnTotal": 1, "rowTotal": 2},
]

column_bars = (
    gs.Chart()
    .mark_rect(color="#555")
    .encode(
        x=gs.X("column:I").axis(None),
        y=gs.Y("columnTotal:Q").axis(title="Column total", tickMinStep=1),
    )
)
column_labels = (
    gs.Chart()
    .mark_text(dy=-8)
    .encode(
        x="column:I",
        y="columnTotal:Q",
        text="columnTotal:Q",
    )
)
column_summary = (
    (column_bars + column_labels)
    .transform_filter("datum.row == 0")
    .properties(height=90)
    .resolve_scale(y="excluded")
)

row_bars = (
    gs.Chart()
    .mark_rect(color="#777")
    .encode(
        x=gs.X("rowTotal:Q").axis(title="Row total", tickMinStep=1),
        y=gs.Y("row:I").axis(None),
    )
)
row_labels = (
    gs.Chart()
    .mark_text(align="right", dx=-5, color="white")
    .encode(
        x="rowTotal:Q",
        y="row:I",
        text="rowTotal:Q",
    )
)
row_summary = (
    (row_bars + row_labels)
    .transform_filter("datum.column == 0")
    .properties(width=110)
    .resolve_scale(x="excluded")
)

matrix = (
    gs.Chart()
    .mark_point(filled=True, size=180)
    .encode(
        x=gs.X("column:I").axis(None),
        y=gs.Y("row:I").axis(None),
        color=gs.Color("member:N")
        .scale(domain=[False, True], range=["#d8d8d8", "#333333"])
        .legend(None),
    )
    .properties(width=gs.step(34), height=gs.step(34))
)

empty_cell = gs.Chart([]).mark_point().properties(width=0, height=0)

grid_chart = (
    gs.concat(
        empty_cell,
        column_summary,
        row_summary,
        matrix,
        columns=2,
    )
    .properties(data=memberships, spacing=4, title="Aligned summaries and matrix")
    .with_scales(
        x=gs.Scale(domain=[-0.5, 2.5], paddingInner=0.15, paddingOuter=0.1),
        y=gs.Scale(domain=[-0.5, 2.5], paddingInner=0.15, paddingOuter=0.1),
    )
    .resolve_scale(x="shared", y="shared")
)
# composition-grid-end


CHARTS = {
    "layered_chart": layered_chart,
    "vertical_chart": vertical_chart,
    "horizontal_chart": horizontal_chart,
    "grid_chart": grid_chart,
}
