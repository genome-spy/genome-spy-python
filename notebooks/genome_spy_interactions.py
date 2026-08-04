"""Minimal Marimo/GenomeSpy interaction spike."""

import marimo

__generated_with = "0.23.16"

app = marimo.App()


@app.cell
def _():
    import genome_spy as gs
    import marimo as mo

    return gs, mo


@app.cell
def _(gs):
    data = [
        {"x": index, "y": value, "group": "A" if index % 2 else "B"}
        for index, value in enumerate([2, 7, 4, 9, 5, 8, 3, 6])
    ]
    chart = (
        gs.Chart(data)
        .mark_point(size=100)
        .encode(x="x:Q", y="y:Q", color="group:N")
        .transform_filter("datum.y >= threshold")
        .properties(params=[gs.param("threshold", value=5)])
    )

    return (chart,)


@app.cell
def _(chart, mo):
    chart_widget = mo.ui.anywidget(
        chart.widget(
            parameter_names=("threshold",),
            parameter_values={"threshold": 5},
            enable_click_events=True,
        )
    )

    return (chart_widget,)


@app.cell
def _(mo):
    threshold = mo.ui.slider(
        start=0,
        stop=10,
        value=5,
        step=1,
        label="Minimum y",
    )

    return (threshold,)


@app.cell
def _(chart_widget, threshold):
    chart_widget.parameter_values = {"threshold": threshold.value}


@app.cell
def _(chart_widget, mo):
    if chart_widget.click_revision == 0:
        message = "Click a point to send its datum back to Python."
    else:
        message = f"Last clicked datum: {chart_widget.clicked_datum}"

    mo.vstack([chart_widget, mo.md(message)])


if __name__ == "__main__":
    app.run()
