"""Shared expression-grid options preserve prepared values and native styling."""

import inspect
import warnings

import numpy as np
import pytest

import genome_spy.integrations.scanpy as gsc
from tests.integrations.scanpy.helpers import leaf_marks
from tests.integrations.scanpy.heatmap_fixture import make_heatmap_adata


def grid_chart(family, **options):
    """Build a small grid with real fixture values and optional interactions."""
    if family == "matrix":
        return gsc.pl.matrix([[0, np.nan, 1], [0.3, 0.8, 0]], show=False, **options)
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", UserWarning)
        return getattr(gsc.pl, family)(
            make_heatmap_adata(), ["g1", "g2", "g1"], "group", show=False, **options
        )


@pytest.mark.parametrize("family", ["dotplot", "matrixplot", "heatmap", "matrix"])
def test_grid_options_are_keyword_only_and_off_by_default(family):
    parameters = inspect.signature(getattr(gsc.pl, family)).parameters
    for name in ("zoom", "highlight" if family == "dotplot" else "show_values"):
        assert parameters[name].kind is inspect.Parameter.KEYWORD_ONLY
        assert parameters[name].default is False
    plain = grid_chart(family).to_dict()
    active = grid_chart(
        family,
        zoom=True,
        **({"highlight": True} if family == "dotplot" else {"show_values": True}),
    ).to_dict()
    field = "_value" if family in ("matrix", "heatmap") else "_mean"

    def records(s):
        return next(rows for rows in s["datasets"].values() if field in rows[0])

    assert records(plain) == records(active)
    plain_mark = next(m for m in leaf_marks(plain) if "color" in m.get("encoding", {}))
    active_mark = next(
        m for m in leaf_marks(active) if "color" in m.get("encoding", {})
    )
    for axis in ("x", "y"):
        assert plain_mark["encoding"][axis]["scale"]["zoom"] is False
        assert active_mark["encoding"][axis]["scale"]["zoom"] is True
    for channel in ("color", "size"):
        if channel in plain_mark["encoding"]:
            assert plain_mark["encoding"][channel] == active_mark["encoding"][channel]


@pytest.mark.parametrize("family", ["dotplot", "matrixplot", "heatmap", "matrix"])
@pytest.mark.parametrize("option", ["zoom", "extra"])
def test_invalid_interaction_options_fail_before_loading_scanpy(
    monkeypatch, family, option
):
    option = (
        ("highlight" if family == "dotplot" else "show_values")
        if option == "extra"
        else option
    )
    monkeypatch.setattr(gsc.pl, "_require_scanpy", lambda: pytest.fail("Loaded Scanpy"))
    arguments = (object(),) if family == "matrix" else (object(), ["g1"], "group")
    with pytest.raises(TypeError, match=f"{option} must be boolean"):
        getattr(gsc.pl, family)(*arguments, **{option: "yes"})


@pytest.mark.parametrize("family", ["matrixplot", "heatmap", "matrix"])
def test_value_marks_share_one_source_and_keep_plotted_values(family):
    options = {} if family == "matrix" else {"standard_scale": "var"}
    spec = grid_chart(family, show_values=True, **options).to_dict()
    values = spec["layer"][0]
    tiles, text_group = values["layer"]
    text = text_group["layer"][0]
    assert "data" not in tiles and "data" not in text
    field = "_mean" if family == "matrixplot" else "_value"
    assert values["transform"][0] == {
        "type": "filter",
        "expr": f"isValid(datum.{field})",
    }
    assert text["encoding"]["text"] == {
        "field": field,
        "type": "quantitative",
        "format": ".2f",
    }
    assert text["mark"]["fitToBand"] is True
    assert text["mark"]["tooltip"] is None
    assert tiles["encoding"]["x"] == text["encoding"]["x"]
    assert tiles["encoding"]["y"] == text["encoding"]["y"]
    assert values["params"][0]["expr"].count("scale('color'") == 256
    source = values["data"]["name"]
    assert len(spec["datasets"][source]) == (
        6 if family == "matrix" else 12 if family == "matrixplot" else 27
    )


def test_highlight_uses_slots_and_remains_available_without_tooltips():
    spec = grid_chart("dotplot", highlight=True, hover=False).to_dict()
    dots = spec["layer"][2]
    assert dots["mark"]["type"] == "point" and dots["mark"]["tooltip"] is None
    assert dots["params"][0]["select"] == {
        "type": "point",
        "on": "mouseover",
        "clear": "mouseout",
        "toggle": False,
    }
    assert dots["params"][0]["push"] == "outer"
    assert "grid_hover.datum._x" in spec["layer"][0]["transform"][0]["expr"]
    assert "grid_hover.datum._y" in spec["layer"][1]["transform"][0]["expr"]
    assert all(layer["mark"]["tooltip"] is None for layer in spec["layer"][:2])
