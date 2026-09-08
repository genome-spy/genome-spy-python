from __future__ import annotations

from copy import deepcopy
from datetime import date
import json

import genome_spy as gs
import pandas as pd
import polars as pl
import pyarrow as pa
import pytest

from genome_spy.data_transformers import _consolidate, _data_slots
from genome_spy.schema import InlineData


def test_equal_tables_are_stored_once_without_mutating_charts() -> None:
    rows = [{"x": i, "y": "abcdefghij" * 10} for i in range(100)]
    first = gs.Chart(rows).mark_point()
    second = gs.Chart(deepcopy(rows)).mark_rect()
    chart = gs.hconcat(first, second, first, second)
    spec = chart.to_dict()
    name, stored = next(iter(spec["datasets"].items()))
    assert stored == rows
    assert len(spec["datasets"]) == 1
    assert all(child["data"] == {"name": name} for child in spec["hconcat"])
    with gs.data_transformers.enable(consolidate_datasets=False):
        inline = chart.to_dict()
    assert "datasets" not in inline
    assert inline["hconcat"][0]["data"]["values"] == rows
    assert len(json.dumps(spec)) < len(json.dumps(inline)) / 3
    assert chart.to_dict() == spec
    assert gs.Chart.from_dict(spec).to_dict() == spec


def test_annotation_charts_share_data_and_render_transport() -> None:
    rows = pd.DataFrame({"x": [1, 2]})
    track = gs.Chart(rows).mark_point().encode(x="x:Q")
    annotation = gs.Chart(rows).mark_rule().encode(x="x:Q")
    chart = gs.vconcat(track, annotate=[annotation])
    spec = chart.to_dict()
    assert len(spec["datasets"]) == 1
    assert spec["vconcat"][0]["data"] == spec["annotate"][0]["data"]
    assert "$schema" not in spec["annotate"][0]
    prepared = chart._prepare_render()
    assert len(prepared.buffers) == 1
    assert prepared.spec["vconcat"][0]["data"] == prepared.spec["annotate"][0]["data"]
    assert prepared.spec["annotate"][0]["data"]["format"] == {"type": "arrow"}


@pytest.mark.parametrize(
    "table", [list, pd.DataFrame, pl.DataFrame, pa.Table.from_pylist]
)
def test_table_inputs_share_by_normalized_content(table) -> None:
    rows = [{"x": 1}]
    chart = gs.Chart(table(rows)).mark_point() + gs.Chart(rows).mark_point()
    assert len(chart.to_dict()["datasets"]) == 1


def test_content_order_and_changes_are_respected() -> None:
    a = gs.Chart([{"x": 1, "y": 2}, {"x": 3}]).mark_point()
    b = gs.Chart([{"y": 2, "x": 1}, {"x": 3}]).mark_point()
    c = gs.Chart([{"x": 3}, {"x": 1, "y": 2}]).mark_point()
    assert len((a + b + c).to_dict()["datasets"]) == 2
    a._kwds["data"][0]["x"] = 9
    assert len((a + b + c).to_dict()["datasets"]) == 3


def test_configuration_restores_after_nested_blocks_and_errors() -> None:
    settings = gs.data_transformers
    with pytest.raises(RuntimeError), settings.enable(consolidate_datasets=False):
        assert settings.consolidate_datasets is False
        with settings.enable():
            assert settings.consolidate_datasets is False
        with settings.enable(consolidate_datasets=True):
            assert settings.consolidate_datasets is True
        assert settings.consolidate_datasets is False
        raise RuntimeError
    assert settings.consolidate_datasets is True
    restore = settings.enable(consolidate_datasets=False)
    assert settings.consolidate_datasets is False
    with restore:
        pass
    assert settings.consolidate_datasets is True
    with pytest.raises(TypeError):
        settings.enable(consolidate_datasets="false")


@pytest.mark.parametrize("wrapper", [gs.Data, InlineData])
def test_schema_wrapped_records_use_same_normalization(wrapper) -> None:
    rows = [{"x": float("nan"), "day": date(2026, 9, 8)}]
    chart = gs.Chart(wrapper(values=rows)).mark_point() + gs.Chart(rows).mark_point()
    spec = chart.to_dict()
    assert list(spec["datasets"].values()) == [[{"x": None, "day": "2026-09-08"}]]
    json.dumps(spec, allow_nan=False)


def test_templates_keep_local_data_and_reserve_references() -> None:
    rows = [{"x": 1}]
    reserved = gs.Chart(rows).mark_point().to_dict()["data"]["name"]
    template = {
        "layer": [
            {"mark": "point", "data": {"values": rows}},
            {"mark": "point", "data": {"name": reserved}},
        ]
    }
    chart = gs.vconcat(
        gs.Chart(rows).mark_point(),
        gs.import_view(template="t"),
        gs.import_view(template="t"),
        templates={"t": template},
    )
    spec = chart.to_dict()
    assert reserved not in spec["datasets"]
    local = spec["templates"]["t"]
    assert reserved not in local["datasets"]
    local_name = local["layer"][0]["data"]["name"]
    assert local["datasets"][local_name] == rows
    assert local["layer"][1]["data"] == {"name": reserved}
    assert "datasets" not in template


def test_typed_mapping_sources_are_discovered() -> None:
    source = {"values": [{"x": 1}]}
    schema = {"additionalProperties": {"$ref": "#/definitions/Data"}}
    assert list(_data_slots({"future": source}, schema)) == [
        ("data", source, None, False)
    ]


@pytest.mark.parametrize("enabled", [True, False])
def test_widget_does_not_register_template_definitions_as_live_views(enabled) -> None:
    from genome_spy._render import _PreparedSpec, prepare_widget_spec

    reserved = "__genome_spy_python_data_0"
    template = {
        "mark": "point",
        "data": {"name": reserved},
        "datasets": {"local": [{"x": 2}]},
    }
    spec = {
        "vconcat": [
            {"mark": "point", "data": {"values": [{"x": 1}]}},
            {"import": {"template": "t"}},
        ],
        "templates": {"t": template},
    }
    prepared = prepare_widget_spec(_PreparedSpec(spec, {}, enabled))
    assert prepared.spec["templates"]["t"] == template
    assert reserved not in prepared.spec["datasets"]
    assert len(prepared.datasets) == 1
    assert prepared.datasets[0].name != "local"


def test_secondary_source_records_are_normalized() -> None:
    spec = {
        "mark": "point",
        "transform": [
            {
                "type": "cross",
                "from": {
                    "data": {
                        "values": [{"x": float("nan"), "day": date(2026, 9, 8)}],
                    }
                },
            }
        ],
    }
    _consolidate(spec)
    assert list(spec["datasets"].values()) == [[{"x": None, "day": "2026-09-08"}]]
    json.dumps(spec, allow_nan=False)


def test_authored_names_and_nested_shadowing_are_preserved() -> None:
    rows = [{"x": 1}]
    automatic = gs.Chart(rows).mark_point()
    reserved = next(iter(automatic.to_dict()["datasets"]))
    named = gs.Chart(gs.Data(name=reserved), datasets={reserved: rows}).mark_point()
    spec = (automatic & named).to_dict()
    generated = spec["vconcat"][0]["data"]["name"]
    assert generated != reserved
    assert spec["vconcat"][1]["datasets"] == {reserved: rows}
    assert spec["vconcat"][1]["data"] == {"name": reserved}
    assert spec["datasets"] == {generated: rows}


@pytest.mark.parametrize(
    "source",
    [
        {"values": [{"x": 1}], "name": "explicit"},
        {"values": [{"x": "1"}], "format": {"parse": {"x": "number"}}},
        {"values": "x\n1", "format": {"type": "csv"}},
        {"values": {"x": 1}},
        {"url": "https://example.org/data.json"},
    ],
)
def test_sources_requiring_original_semantics_are_unchanged(source) -> None:
    spec = gs.Chart(source).mark_point().to_dict()
    assert spec["data"] == source
    assert "datasets" not in spec


def test_rows_are_opaque_and_low_level_schema_serialization_is_literal() -> None:
    rows = [{"data": {"values": [{"x": 1}]}, "datasets": {"foo": []}}]
    data = InlineData(values=rows)
    assert data.to_dict() == {"values": rows}
    spec = gs.Chart(data).mark_point().to_dict()
    assert list(spec["datasets"].values()) == [rows]


def test_new_schema_declared_source_location_is_discovered() -> None:
    schema = {"properties": {"future": {"$ref": "#/definitions/Data"}}}
    source = {"values": [{"x": 1}]}
    assert list(_data_slots({"future": source}, schema)) == [
        ("data", source, None, False)
    ]


def test_transform_secondary_data_is_consolidated() -> None:
    spec = {
        "mark": "point",
        "transform": [{"type": "cross", "from": {"data": {"values": [{"x": 1}]}}}],
    }
    _consolidate(spec)
    name = spec["transform"][0]["from"]["data"]["name"]
    assert spec["datasets"][name] == [{"x": 1}]


@pytest.mark.parametrize("arrow", [False, True])
def test_widget_sharing_and_independent_bindings_when_disabled(arrow) -> None:
    rows = [{"x": 1}]
    data = pl.DataFrame(rows) if arrow else rows
    chart = gs.Chart(data).mark_point() & gs.Chart(data).mark_point()
    widget = chart.widget()
    assert len(widget.dataset_names) == 1
    assert widget.spec["vconcat"][0]["data"] == widget.spec["vconcat"][1]["data"]
    widget.set_dataset(widget.dataset_names[0], [{"x": 2}], format="records")
    with gs.data_transformers.enable(consolidate_datasets=False):
        independent = chart.widget()
    assert len(independent.dataset_names) == 2
    assert (
        independent.spec["vconcat"][0]["data"] != independent.spec["vconcat"][1]["data"]
    )


def test_raw_widget_spec_shares_records() -> None:
    chart = {
        "layer": [
            {"mark": "point", "data": {"values": [{"x": 1}]}},
            {"mark": "rect", "data": {"values": [{"x": 1}]}},
        ]
    }
    original = deepcopy(chart)
    widget = gs.JupyterChart(chart)
    assert len(widget.dataset_names) == 1
    assert chart == original
    gs.Chart.from_dict(widget.spec)  # The consolidated raw spec is valid GenomeSpy.


def test_explicit_equal_widget_datasets_update_independently() -> None:
    chart = gs.vconcat(
        gs.Chart(gs.Data(name="first")).mark_point(),
        gs.Chart(gs.Data(name="second")).mark_point(),
        datasets={"first": [{"x": 1}], "second": [{"x": 1}]},
    )
    widget = chart.widget()
    first, second = widget.dataset_manifest
    before = getattr(widget, second["revision_trait"])
    widget.set_dataset("first", [{"x": 2}], format="records")
    assert getattr(widget, first["revision_trait"]) == 1
    assert getattr(widget, second["revision_trait"]) == before
    assert widget.dataset_names == ("first", "second")


def test_widget_does_not_rewrite_data_inside_parameter_values() -> None:
    value = {"data": {"values": [{"x": 1}]}, "datasets": {"private": []}}
    chart = gs.Chart().mark_point().add_params(gs.param("settings", value=value))
    widget = chart.widget()
    assert widget.spec["params"][0]["value"] == value
    assert widget.dataset_names == ()


def test_empty_inline_array_is_consolidated() -> None:
    spec = gs.Chart([]).mark_point().to_dict(include_schema=False)
    assert "$schema" not in spec
    assert spec["datasets"][spec["data"]["name"]] == []


def test_reserved_unresolved_reference_is_not_captured() -> None:
    chart = gs.Chart([{"x": 1}]).mark_point()
    name = chart.to_dict()["data"]["name"]
    spec = (chart + gs.Chart(gs.Data(name=name)).mark_point()).to_dict()
    assert name not in spec["datasets"]
    assert spec["layer"][1]["data"]["name"] == name


def test_shared_arrow_buffer_has_independent_disabled_widget_updates() -> None:
    data = pl.DataFrame({"x": [1]})
    chart = gs.Chart(data).mark_point() & gs.Chart(data).mark_point()
    with gs.data_transformers.enable(consolidate_datasets=False):
        prepared = chart._prepare_render()
        widget = chart.widget()
    assert len(prepared.buffers) == 1
    assert len(widget.dataset_names) == 2
    first, second = widget.dataset_manifest
    initial_second = getattr(widget, second["revision_trait"])
    widget.set_dataset(widget.dataset_names[0], pl.DataFrame({"x": [2]}))
    assert getattr(widget, first["revision_trait"]) == 2
    assert getattr(widget, second["revision_trait"]) == initial_second


def test_json_html_and_file_export_share_the_policy(tmp_path) -> None:
    chart = gs.Chart([{"x": 1}]).mark_point()
    assert "datasets" in json.loads(chart.to_json())
    assert '"datasets"' in chart.to_html()
    path = tmp_path / "chart.json"
    chart.save(path)
    assert json.loads(path.read_text()) == chart.to_dict()
    with gs.data_transformers.enable(consolidate_datasets=False):
        assert '"datasets"' not in chart.to_html()
