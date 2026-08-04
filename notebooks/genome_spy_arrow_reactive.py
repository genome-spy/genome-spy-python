"""Reactive Polars-to-GenomeSpy Arrow IPC transport spike."""

import marimo

__generated_with = "0.23.16"

app = marimo.App()


@app.cell
def _():
    import json
    import time

    import genome_spy as gs
    import marimo as mo
    import polars as pl

    return gs, json, mo, pl, time


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
def _(gs):
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
    chart_widget = chart.widget()

    return (chart_widget,)


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
def _(amplitude, chart_widget, gs, json, pl, signal, time):
    scaled_signal = signal.with_columns(
        (pl.col("value") * amplitude.value / 100).alias("value")
    )
    started = time.perf_counter()
    arrow_payload = gs.to_arrow_ipc(scaled_signal)
    arrow_encode_ms = (time.perf_counter() - started) * 1_000
    json_payload_size = len(json.dumps(scaled_signal.to_dicts()).encode())
    chart_widget.arrow_data = {"signal": arrow_payload}
    transport_summary = (
        f"Arrow IPC: {len(arrow_payload):,} bytes, "
        f"{arrow_encode_ms:.2f} ms encode; "
        f"JSON rows: {json_payload_size:,} bytes"
    )

    return (transport_summary,)


@app.cell
def _(amplitude, chart_widget, mo, transport_summary):
    if chart_widget.error:
        output = mo.md(f"Arrow transport error: `{chart_widget.error}`")
    else:
        output = mo.vstack(
            [
                amplitude,
                mo.md(
                    "Move the control to replace the Arrow payload and "
                    "re-embed the chart."
                ),
                mo.md(transport_summary),
                chart_widget,
            ]
        )
    output


if __name__ == "__main__":
    app.run()
