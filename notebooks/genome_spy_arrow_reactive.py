"""Live Polars-to-GenomeSpy updates in Marimo without widget reconstruction."""

import marimo

__generated_with = "0.23.16"
app = marimo.App()


@app.cell
def _():
    import genome_spy as gs
    import marimo as mo
    import polars as pl

    return gs, mo, pl


@app.cell
def _(mo):
    amplitude = mo.ui.slider(
        start=50,
        stop=200,
        value=100,
        step=10,
        label="Signal amplitude (%)",
    )
    return (amplitude,)


@app.cell
def _(gs, mo, pl):
    initial_signal = pl.DataFrame(
        {
            "position": list(range(8)),
            "value": [0.2, 0.8, 1.4, 0.6, 1.1, 1.8, 1.2, 0.4],
            "group": ["A", "A", "A", "A", "B", "B", "B", "B"],
        }
    )
    chart = (
        gs.Chart(data={"name": "table"}, datasets={"table": []})
        .mark_point(size=110, filled=True)
        .encode(
            x=gs.X("position:Q").title("Position"),
            y=gs.Y("value:Q").title("Scaled value"),
            color=gs.Color("group:N"),
            tooltip=[
                gs.Tooltip("position:Q"),
                gs.Tooltip("value:Q"),
                gs.Tooltip("group:N"),
            ],
        )
        .properties(width=620, height=320)
    )
    view = chart.widget()
    view.set_dataset("table", initial_signal)
    chart_widget = mo.ui.anywidget(view)
    return chart_widget, view


@app.cell
def _(amplitude, mo, pl, view):
    filtered_dataframe = pl.DataFrame(
        {
            "position": list(range(8)),
            "value": [0.2, 0.8, 1.4, 0.6, 1.1, 1.8, 1.2, 0.4],
            "group": ["A", "A", "A", "A", "B", "B", "B", "B"],
        }
    ).with_columns((pl.col("value") * amplitude.value / 100).alias("value"))
    view.set_dataset("table", filtered_dataframe)
    transport_summary = mo.md(
        "**Live Arrow update:** the stable widget model received a new binary "
        'dataset through `view.set_dataset("table", filtered_dataframe)`; '
        "the chart was not reconstructed."
    )
    return (transport_summary,)


@app.cell
def _(amplitude, chart_widget, mo, transport_summary):
    mo.vstack(
        [
            amplitude,
            transport_summary,
            chart_widget,
        ]
    )
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
