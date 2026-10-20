"""Public authoring and transport for the Core 1.2 composition grammar."""

from copy import deepcopy
import inspect

import genome_spy as gs
import pandas as pd
import pytest

from genome_spy.schemapi import SchemaValidationError


@pytest.mark.parametrize("channel", [gs.X, gs.Color, gs.X2Offset, gs.Y2Offset])
def test_channel_fields_can_be_authored_with_named_arguments(channel) -> None:
    definition = channel(field="value").to_dict()
    assert definition == {"field": "value"}
    assert "field" in inspect.signature(channel).parameters


@pytest.mark.parametrize("name", ["x2Offset", "y2Offset"])
def test_secondary_offsets_do_not_infer_an_independent_field_type(name: str) -> None:
    chart = gs.Chart([{"offset": 0.5}]).mark_link(linkShape="orthogonal")
    spec = chart.encode(**{name: "offset:Q"}).to_dict()
    assert spec["encoding"][name] == {"field": "offset"}


def test_secondary_offset_expressions_keep_their_authored_type() -> None:
    spec = (
        gs.Chart([{"offset": 0.5}])
        .mark_link()
        .encode(x2Offset=gs.X2Offset(expr="datum.offset", type="quantitative"))
        .to_dict()
    )
    assert spec["encoding"]["x2Offset"] == {
        "expr": "datum.offset",
        "type": "quantitative",
    }


def test_facet_uses_named_mapping_and_header_options() -> None:
    points = gs.Chart().mark_point().encode(x="x:Q", y="y:Q")
    chart = gs.facet(
        points,
        facet=gs.FacetMapping().row(field="group", header=gs.FacetHeader(fontSize=14)),
        data=[{"x": 1, "y": 2, "group": "a"}],
        spacing=gs.FacetSpacing(row=8),
    ).configure_header(color="navy")
    spec = chart.to_dict()
    assert spec["facet"] == {"row": {"field": "group", "header": {"fontSize": 14}}}
    assert spec["spacing"] == {"row": 8}
    assert spec["config"]["header"] == {"color": "navy"}
    assert "$schema" not in spec["spec"]
    assert spec["spec"]["mark"] == "point"
    assert "facet" in inspect.signature(gs.facet).parameters


@pytest.mark.parametrize("wrapper", [gs.surround, gs.facet])
def test_single_plot_compositions_share_arrow_transport(wrapper) -> None:
    rows = pd.DataFrame({"x": [1, 2], "group": ["a", "b"]})
    center = gs.Chart(rows).mark_point().encode(x="x:Q")
    if wrapper is gs.surround:
        chart = wrapper(
            center,
            surround=gs.SurroundSides(
                top=gs.SurroundSideSpec(
                    views=[gs.Chart(rows).mark_tick().encode(x="x:Q")], spacing=3
                )
            ),
        )
    else:
        chart = wrapper(center, facet=gs.FacetFieldDef(field="group"))
    prepared = chart._prepare_render()
    assert len(prepared.buffers) == 1
    assert prepared.spec["spec"]["data"]["format"] == {"type": "arrow"}
    if wrapper is gs.surround:
        top = prepared.spec["surround"]["top"]["views"][0]
        assert top["data"] == prepared.spec["spec"]["data"]
        assert "$schema" not in top
    widget = chart._prepare_widget()
    assert widget.spec["spec"]["data"]["name"]


def test_surround_side_shared_encoding_serializes_named_channels() -> None:
    from genome_spy.schema import Encoding

    encoding = Encoding(
        y=gs.Y("row:I").axis(None),
        y2=gs.Y2("end:Q"),
        tooltip=[gs.Tooltip("label", title="Cell line")],
    )
    side = gs.SurroundSideSpec(encoding=encoding, views=[gs.Chart().mark_rect()])
    chart = gs.surround(gs.Chart().mark_rect(), surround=gs.SurroundSides(right=side))
    expected = {
        "y": {"field": "row", "type": "index", "axis": None},
        "y2": {"field": "end"},
        "tooltip": [{"field": "label", "title": "Cell line"}],
    }
    assert chart.to_dict()["surround"]["right"]["encoding"] == expected
    assert chart._prepare_render().spec["surround"]["right"]["encoding"] == expected
    assert isinstance(encoding._kwds["y"], gs.Y)


@pytest.mark.parametrize(
    ("spec", "chart_type"),
    [
        ({"facet": {"field": "group"}, "spec": {"mark": "point"}}, gs.FacetChart),
        (
            {"surround": {"top": [{"mark": "tick"}]}, "spec": {"mark": "point"}},
            gs.SurroundChart,
        ),
    ],
)
def test_new_compositions_round_trip_inside_concats(spec, chart_type) -> None:
    original = {
        "hconcat": [deepcopy(spec)],
        "$schema": "https://example.test/schema.json",
    }
    chart = gs.Chart.from_dict(original)
    child = chart._kwds["hconcat"][0]
    assert isinstance(child, chart_type)
    assert isinstance(child._kwds["spec"], gs.Chart)
    assert chart.to_dict() == original
    assert child.copy()._schema_url == original["$schema"]


@pytest.mark.parametrize("root", ["facet", "surround"])
def test_single_plot_compositions_reject_non_object_children(root: str) -> None:
    with pytest.raises(TypeError, match="spec must be a view specification"):
        gs.Chart.from_dict({root: {}, "spec": []}, validate=False)


def test_facet_properties_preserve_schema_validation() -> None:
    chart = gs.facet(
        gs.Chart().mark_point(),
        facet=gs.FacetMapping(row=gs.FacetFieldDef(field="group")),
    )
    with pytest.raises(SchemaValidationError):
        chart.properties(facet={"unknown": "group"}).to_dict()


def test_surround_signatures_omit_schema_forbidden_options() -> None:
    properties = inspect.signature(gs.SurroundChart.properties).parameters
    assert "viewportHeight" not in properties
    assert "viewportWidth" not in properties
    assert "axes" not in properties
    assert "height" not in inspect.signature(gs.SurroundSideSpec).parameters


def test_unit_views_support_named_resolution_arguments() -> None:
    chart = (
        gs.Chart()
        .mark_point()
        .resolve_scale(x="excluded")
        .resolve_axis(y="independent")
    )
    assert chart.to_dict()["resolve"] == {
        "scale": {"x": "excluded"},
        "axis": {"y": "independent"},
    }
