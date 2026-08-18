"""Executable snippets used by the notebook display and update guide."""

import genome_spy as gs


# notebooks-chart-start
initial_rows = [
    {"sample": "A", "value": 2.1, "group": "control"},
    {"sample": "B", "value": 3.4, "group": "control"},
    {"sample": "C", "value": 4.2, "group": "treated"},
]

chart = (
    gs.Chart(
        data={"name": "measurements"},
        datasets={"measurements": initial_rows},
    )
    .mark_point(filled=True, size=120)
    .encode(
        x=gs.X("sample:N").title("Sample"),
        y=gs.Y("value:Q").title("Measurement"),
        color=gs.Color("group:N"),
    )
    .properties(height=180, title="Notebook measurements")
)
# notebooks-chart-end


# notebooks-implicit-display-start
# Leave the chart as the final expression in a notebook cell.
chart
# notebooks-implicit-display-end


# notebooks-widget-start
view = chart.widget()

# Display this object once in the notebook.
view
# notebooks-widget-end


# notebooks-record-update-start
updated_rows = [
    {"sample": "A", "value": 2.8, "group": "control"},
    {"sample": "B", "value": 3.1, "group": "control"},
    {"sample": "C", "value": 4.7, "group": "treated"},
]

view.set_dataset("measurements", updated_rows, format="records")
# notebooks-record-update-end


CHARTS = {"chart": chart}
