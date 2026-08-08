from __future__ import annotations

import genome_spy as gs
import polars as pl


def test_widget_uses_chart_spec() -> None:
    chart = gs.Chart(data=[{"x": 1, "y": 2}]).mark_point().encode(x="x:Q", y="y:Q")

    widget = chart.widget()

    assert widget.spec == chart.to_dict()
    assert "import(moduleUrl)" in widget._esm


def test_jupyter_chart_accepts_raw_spec_dict() -> None:
    spec = {
        "$schema": "https://cdn.jsdelivr.net/npm/@genome-spy/core/dist/schema.json",
        "mark": "point",
        "data": {"values": [{"x": 1}]},
        "encoding": {"x": {"field": "x", "type": "quantitative"}},
    }

    widget = gs.JupyterChart(spec)

    assert widget.spec == spec


def test_widget_automatically_exposes_binary_arrow_payloads() -> None:
    chart = (
        gs.Chart(pl.DataFrame({"position": [1, 2], "value": [3.0, 4.0]}))
        .mark_point()
        .encode(x="position:Q", y="value:Q")
    )

    widget = chart.widget()

    identifier = next(iter(widget.arrow_data))
    assert widget.spec["data"] == {
        "url": f"arrow://{identifier}",
        "format": {"type": "arrow"},
    }
    assert widget.arrow_data[identifier][:6] == b"ARROW1"
    assert "arrow_data" in widget._esm
    assert "createObjectURL" in widget._esm
    assert "revokeObjectURL" in widget._esm
    assert "renderRevision" in widget._esm
    assert "toUint8Array" in widget._esm
    assert "nextApi?.finalize?.()" in widget._esm


def test_widget_exposes_explicit_interaction_state() -> None:
    chart = (
        gs.Chart([{"x": 1, "y": 2}])
        .mark_point()
        .encode(x="x:Q", y="y:Q")
        .properties(params=[gs.param("threshold", value=1)])
    )

    widget = chart.widget(
        parameter_names=("threshold",),
        parameter_values={"threshold": 2},
        enable_click_events=True,
    )

    assert widget.parameter_names == ["threshold"]
    assert widget.parameter_values == {"threshold": 2}
    assert widget.enable_click_events is True
    assert widget.clicked_datum == {}
    assert widget.click_revision == 0
    assert widget.error == ""
    assert "getParam" in widget._esm
    assert "clicked_datum" in widget._esm
