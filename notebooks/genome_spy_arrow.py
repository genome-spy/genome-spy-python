"""Minimal Polars-to-GenomeSpy Arrow IPC transport spike."""

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
def _(pl):
    signal = pl.DataFrame(
        {
            "position": [0, 1, 2, 3, 4, 5, 6, 7],
            "value": [0.2, 0.8, 1.4, 0.6, 1.1, 1.8, 1.2, 0.4],
        }
    )

    return (signal,)


@app.cell
def _(gs, signal):
    chart = (
        gs.Chart(
            data={
                "url": "arrow://signal",
                "format": {"type": "arrow"},
            }
        )
        .mark_point(size=100)
        .encode(x="position:Q", y="value:Q")
    )
    chart_widget = chart.widget(
        arrow_data={"signal": gs.to_arrow_ipc(signal)},
    )

    return (chart_widget,)


@app.cell
def _(chart_widget, mo):
    if chart_widget.error:
        output = mo.md(f"Arrow transport error: `{chart_widget.error}`")
    else:
        output = mo.vstack(
            [
                mo.md("Polars serialized this table as uncompressed Arrow IPC."),
                chart_widget,
            ]
        )
    output


if __name__ == "__main__":
    app.run()
