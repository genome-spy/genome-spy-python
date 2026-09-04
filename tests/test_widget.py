from __future__ import annotations

from copy import deepcopy

import genome_spy as gs
import pandas as pd
import polars as pl
import pyarrow as pa
import pytest


def _entry(widget: gs.JupyterChart, name: str) -> dict[str, object]:
    return next(entry for entry in widget.dataset_manifest if entry["name"] == name)


def _declared_chart() -> gs.Chart:
    return (
        gs.Chart(data={"name": "table"}, datasets={"table": []})
        .mark_point()
        .encode(x="x:Q", y="y:Q")
    )


def test_widget_rewrites_eager_records_as_a_named_dataset() -> None:
    chart = gs.Chart(data=[{"x": 1, "y": 2}]).mark_point().encode(x="x:Q", y="y:Q")

    widget = chart.widget()

    assert widget.spec["data"] == {"name": "__genome_spy_python_data_0"}
    assert widget.spec["datasets"] == {"__genome_spy_python_data_0": [{"x": 1, "y": 2}]}
    assert widget.dataset_names == ("__genome_spy_python_data_0",)
    assert "import(moduleUrl)" in widget._esm
    assert widget.controls == ["svg", "png", "inspector"]
    assert widget._control_definitions["png"] == {
        "module": "core",
        "export": "pngButton",
    }


def test_widget_accepts_selected_or_disabled_controls() -> None:
    chart = gs.Chart().mark_point()

    selected = chart.widget(controls=["png", "full-window"])
    disabled = chart.widget(controls=False)

    assert selected.controls == ["png", "full-window"]
    assert disabled.controls == []


def test_jupyter_chart_rewrites_raw_eager_spec_dict() -> None:
    spec = {
        "$schema": "https://cdn.jsdelivr.net/npm/@genome-spy/core/dist/schema.json",
        "mark": "point",
        "data": {"values": [{"x": 1}]},
        "encoding": {"x": {"field": "x", "type": "quantitative"}},
    }

    widget = gs.JupyterChart(spec)

    assert widget.spec["data"] == {"name": "__genome_spy_python_data_0"}
    assert widget.spec["datasets"] == {"__genome_spy_python_data_0": [{"x": 1}]}


def test_widget_generated_dataset_names_skip_existing_declarations() -> None:
    chart = (
        gs.Chart(data=[{"x": 1}], datasets={"__genome_spy_python_data_0": []})
        .mark_point()
        .encode(x="x:Q")
    )

    widget = chart.widget()

    assert widget.spec["data"] == {"name": "__genome_spy_python_data_1"}
    assert set(widget.spec["datasets"]) == {
        "__genome_spy_python_data_0",
        "__genome_spy_python_data_1",
    }


def test_widget_records_a_named_scoped_dataset_owner() -> None:
    child = (
        gs.Chart(data={"name": "table"}, datasets={"table": []})
        .mark_point()
        .encode(x="x:Q")
        .properties(name="child")
    )

    widget = gs.vconcat(child).widget()

    entry = _entry(widget, "table")
    assert entry["owner"] == "child"
    assert entry["scoped"] is True


def test_widget_exposes_initial_arrow_payload_in_a_private_trait() -> None:
    chart = (
        gs.Chart(pl.DataFrame({"position": [1, 2], "value": [3.0, 4.0]}))
        .mark_point()
        .encode(x="position:Q", y="value:Q")
    )

    widget = chart.widget()
    entry = _entry(widget, "__genome_spy_python_data_0")

    assert widget.spec["data"] == {"name": "__genome_spy_python_data_0"}
    assert widget.spec["datasets"] == {"__genome_spy_python_data_0": []}
    assert getattr(widget, entry["format_trait"]) == "arrow"
    assert getattr(widget, entry["revision_trait"]) == 1
    assert getattr(widget, entry["payload_trait"])[:6] == b"ARROW1"
    assert "datasets.load" in widget._esm
    assert "createObjectURL" not in widget._esm


@pytest.mark.parametrize(
    "table",
    [
        pl.DataFrame({"x": [1, 2], "y": [3, 4]}),
        pd.DataFrame({"x": [1, 2], "y": [3, 4]}),
        pa.table({"x": [1, 2], "y": [3, 4]}),
        pa.record_batch([[1, 2], [3, 4]], names=["x", "y"]),
    ],
)
def test_set_dataset_serializes_supported_tables_without_rewriting_spec(
    table: object,
) -> None:
    widget = _declared_chart().widget()
    entry = _entry(widget, "table")
    original_spec = deepcopy(widget.spec)

    widget.set_dataset("table", table)

    assert widget.spec == original_spec
    assert getattr(widget, entry["format_trait"]) == "arrow"
    assert getattr(widget, entry["revision_trait"]) == 1
    assert getattr(widget, entry["payload_trait"])[:6] == b"ARROW1"


def test_set_dataset_changes_only_the_targeted_dataset_traits() -> None:
    chart = (
        gs.Chart(
            data={"name": "table"},
            datasets={"table": [], "reference": [{"x": 0, "y": 0}]},
        )
        .mark_point()
        .encode(x="x:Q", y="y:Q")
    )
    widget = chart.widget()
    table = _entry(widget, "table")
    reference = _entry(widget, "reference")
    reference_state = {
        trait: getattr(widget, reference[trait])
        for trait in ("payload_trait", "format_trait", "revision_trait")
    }

    widget.set_dataset("table", pl.DataFrame({"x": [1], "y": [2]}))

    assert getattr(widget, table["revision_trait"]) == 1
    assert {
        trait: getattr(widget, reference[trait])
        for trait in ("payload_trait", "format_trait", "revision_trait")
    } == reference_state


def test_set_dataset_records_is_an_explicit_fallback() -> None:
    widget = _declared_chart().widget()
    entry = _entry(widget, "table")

    widget.set_dataset("table", [{"x": 1, "y": 2}], format="records")

    assert getattr(widget, entry["format_trait"]) == "records"
    assert getattr(widget, entry["payload_trait"]) == [{"x": 1, "y": 2}]
    assert getattr(widget, entry["revision_trait"]) == 1


def test_set_dataset_keeps_previous_state_when_serialization_fails() -> None:
    widget = _declared_chart().widget()
    entry = _entry(widget, "table")
    widget.set_dataset("table", pl.DataFrame({"x": [1]}))
    before = tuple(
        getattr(widget, entry[trait])
        for trait in ("payload_trait", "format_trait", "revision_trait")
    )

    with pytest.raises(TypeError, match="write_ipc"):
        widget.set_dataset("table", object())

    assert (
        tuple(
            getattr(widget, entry[trait])
            for trait in ("payload_trait", "format_trait", "revision_trait")
        )
        == before
    )


def test_set_data_requires_one_live_dataset() -> None:
    widget = _declared_chart().widget()

    widget.set_data(pl.DataFrame({"x": [1], "y": [2]}))

    assert getattr(widget, _entry(widget, "table")["revision_trait"]) == 1


def test_set_data_reports_ambiguous_dataset_names() -> None:
    widget = (
        gs.Chart(data={"name": "first"}, datasets={"first": [], "second": []})
        .mark_point()
        .encode(x="x:Q")
        .widget()
    )

    with pytest.raises(ValueError, match="exactly one"):
        widget.set_data(pl.DataFrame({"x": [1]}))


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
