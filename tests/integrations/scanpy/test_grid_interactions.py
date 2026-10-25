"""Shared expression-grid options preserve prepared values and native styling."""

import inspect
import warnings

import numpy as np
import pytest

import genome_spy.integrations.scanpy as gsc
from tests.integrations.scanpy.helpers import leaf_marks
from tests.integrations.scanpy.heatmap_fixture import make_heatmap_adata
from tests.integrations.scanpy.clustermap_fixture import make_cluster_adata


@pytest.mark.parametrize(
    "family",
    [
        "matrix",
        "matrixplot",
        "MatrixPlot",
        "heatmap",
        "clustermap",
        "correlation_matrix",
        "rank_genes_groups_matrixplot",
        "rank_genes_groups_heatmap",
        "timeseries_as_heatmap",
        "sim",
        "dpt_timeseries",
        "paga_adjacency",
        "paga_path",
    ],
)
def test_every_matrix_family_exposes_keyword_only_value_labels(family):
    parameter = inspect.signature(getattr(gsc.pl, family)).parameters["show_values"]
    assert parameter.kind is inspect.Parameter.KEYWORD_ONLY
    assert parameter.default is (None if family == "correlation_matrix" else False)


def grid_chart(family, **options):
    """Build a small grid with real fixture values and optional interactions."""
    if family == "matrix":
        return gsc.pl.matrix([[0, np.nan, 1], [0.3, 0.8, 0]], show=False, **options)
    if family == "clustermap":
        return gsc.pl.clustermap(
            make_cluster_adata(), mask=np.eye(6, 4, dtype=bool), show=False, **options
        )
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", UserWarning)
        return getattr(gsc.pl, family)(
            make_heatmap_adata(), ["g1", "g2", "g1"], "group", show=False, **options
        )


@pytest.mark.parametrize(
    "family", ["dotplot", "matrixplot", "heatmap", "matrix", "clustermap"]
)
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
    field = "_mean" if family in ("dotplot", "matrixplot") else "_value"

    def records(s):
        return next(rows for rows in s["datasets"].values() if field in rows[0])

    assert records(plain) == records(active)
    plain_mark = next(m for m in leaf_marks(plain) if "color" in m.get("encoding", {}))
    active_mark = next(
        m for m in leaf_marks(active) if "color" in m.get("encoding", {})
    )
    for axis in ("x", "y"):
        assert (
            plain["scales"][axis]
            if "surround" in plain
            else plain_mark["encoding"][axis]["scale"]
        )["zoom"] is False
        assert (
            active["scales"][axis]
            if "surround" in active
            else active_mark["encoding"][axis]["scale"]
        )["zoom"] is (axis == "y")
    for channel in ("color", "size"):
        if channel in plain_mark["encoding"]:
            assert plain_mark["encoding"][channel] == active_mark["encoding"][channel]


@pytest.mark.parametrize(
    "family", ["dotplot", "matrixplot", "heatmap", "matrix", "clustermap"]
)
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
    arguments = (
        (object(),)
        if family in ("matrix", "clustermap")
        else (object(), ["g1"], "group")
    )
    with pytest.raises(TypeError, match=f"{option} must be"):
        getattr(gsc.pl, family)(*arguments, **{option: "yes"})


@pytest.mark.parametrize("family", ["matrixplot", "heatmap", "matrix", "clustermap"])
def test_value_marks_share_one_source_and_keep_plotted_values(family):
    options = {} if family in ("matrix", "clustermap") else {"standard_scale": "var"}
    spec = grid_chart(family, show_values=True, **options).to_dict()
    values = spec["spec"] if "surround" in spec else spec["layer"][0]
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
        6
        if family == "matrix"
        else 12
        if family == "matrixplot"
        else 24
        if family == "clustermap"
        else 27
    )


def test_highlight_uses_native_ruler_without_extra_marks_or_data():
    plain = grid_chart("dotplot", hover=False).to_dict()
    spec = grid_chart("dotplot", highlight=True, hover=False).to_dict()
    dots = spec["spec"]["layer"][0]
    assert dots["mark"]["type"] == "point" and dots["mark"]["tooltip"] is None
    assert spec["spec"]["params"] == [
        {
            "name": "grid_cursor",
            "persist": False,
            "ruler": {
                "encodings": ["x", "y"],
                "display": "center",
                "extent": "view",
                "mark": {
                    "stroke": "#4682b4",
                    "opacity": 0.55,
                    "strokeWidth": 1,
                    "zindex": 0,
                },
            },
        }
    ]
    assert spec["datasets"] == plain["datasets"]
    del spec["spec"]["params"]
    assert spec == plain


@pytest.mark.parametrize(
    "family", ["dotplot", "matrixplot", "heatmap", "matrix", "clustermap"]
)
def test_grid_can_explicitly_enable_both_axes(family):
    spec = grid_chart(family, zoom="xy").to_dict()
    mark = next(m for m in leaf_marks(spec) if "color" in m.get("encoding", {}))
    for axis in ("x", "y"):
        assert (
            spec["scales"][axis]
            if "surround" in spec
            else mark["encoding"][axis]["scale"]
        )["zoom"] is True


@pytest.mark.parametrize(
    "family,field", [("heatmap", "label"), ("clustermap", "_color")]
)
@pytest.mark.parametrize("hover", [False, True])
def test_category_strip_uses_native_tooltip_and_respects_hover(family, field, hover):
    spec = (
        grid_chart(family, hover=hover).to_dict()
        if family == "heatmap"
        else gsc.pl.clustermap(
            make_cluster_adata(), obs_keys="group", hover=hover, show=False
        ).to_dict()
    )
    strip = next(
        mark
        for mark in leaf_marks(spec)
        if mark.get("encoding", {}).get("color", {}).get("field") == field
    )
    assert strip["mark"]["clip"] is True
    assert "xOffset" not in strip["mark"] and "x2Offset" not in strip["mark"]
    if hover:
        assert strip["mark"]["tooltip"] == {"handler": "default"}
        assert strip["encoding"]["tooltip"] == [
            {"field": field, "type": "nominal", "title": "group"}
        ]
    else:
        assert strip["mark"]["tooltip"] is None
        assert "tooltip" not in strip["encoding"]


@pytest.mark.parametrize("invalid", [None, 0, 1, "x", "y", [], {}])
def test_zoom_rejects_other_modes_before_optional_dependencies(monkeypatch, invalid):
    monkeypatch.setattr(gsc.pl, "_require_scanpy", lambda: pytest.fail("Loaded Scanpy"))
    with pytest.raises(TypeError, match="zoom must be False, True.*or 'xy'"):
        gsc.pl.matrix(object(), zoom=invalid)


@pytest.mark.parametrize("family", ["dotplot", "matrixplot"])
@pytest.mark.parametrize("swapped", [False, True])
def test_summary_tracks_share_positions_without_copying_measurements(family, swapped):
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", UserWarning)
        spec = getattr(gsc.pl, family)(
            make_heatmap_adata(),
            {"First": ["g2", "g1"], "Again": ["g2"]},
            "group",
            dendrogram=True,
            swap_axes=swapped,
            zoom="xy",
            show=False,
        ).to_dict()
    gene_axis = "y" if swapped else "x"
    assert spec["scales"][gene_axis]["gapPositions"] == (
        [2] if family == "dotplot" else []
    )
    assert spec["scales"]["x" if swapped else "y"]["gapPositions"] == []
    assert all(
        spec["scales"][axis]["gapWidth"] == (0 if family == "dotplot" else 4)
        for axis in ("x", "y")
    )
    assert set(spec["surround"]) == {"top", "bottom", "left", "right"}
    assert "padding" not in spec and spec["spacing"] == 0
    assert "params" not in spec
    measurements = [rows for rows in spec["datasets"].values() if "_mean" in rows[0]]
    assert len(measurements) == 1 and len(measurements[0]) == 12
    for mark in leaf_marks(spec):
        for axis in ("x", "y"):
            encoding = mark.get("encoding", {}).get(axis, {})
            if encoding.get("type") == "index":
                assert "scale" not in encoding
        if mark.get("mark", {}).get("type") == "link":
            assert mark["mark"]["clip"] is True
