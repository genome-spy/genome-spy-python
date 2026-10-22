"""Supplied profile order, cropped limits and the pinned heatmap contract."""

import inspect
import json
from pathlib import Path

import numpy as np
import pandas as pd
import pytest
from scipy import sparse

import genome_spy.integrations.scanpy as gsc
from tests.integrations.scanpy.helpers import leaf_marks, points


def test_signature_preserves_upstream_defaults_and_adds_only_native_options():
    upstream = json.loads(
        Path(__file__).with_name("fixtures").joinpath("api.json").read_text()
    )["entries"]["timeseries_as_heatmap"]["parameters"]
    actual = inspect.signature(gsc.pl.timeseries_as_heatmap).parameters
    for parameter in upstream:
        value = actual[parameter["name"]]
        assert value.kind.name == parameter["kind"]
        assert (
            None if value.default is inspect.Parameter.empty else repr(value.default)
        ) == parameter["default"]
    assert set(actual) - {p["name"] for p in upstream} == {
        "show",
        "save",
        "hover",
        "zoom",
        "show_values",
        "width",
        "height",
    }


@pytest.mark.parametrize("shape", [(5, 3), (1, 3), (5, 1), (1, 1)])
def test_values_limits_labels_and_highlights_match_scanpy_without_analysis(
    shape, monkeypatch
):
    import matplotlib.pyplot as plt
    import scanpy as sc

    values = np.arange(np.prod(shape), dtype=float).reshape(shape)
    original = values.copy()
    labels = np.array([f"v{i}" for i in range(shape[1])])
    # Read the upstream reference only in tests; runtime never calls its renderer.
    sc.pl.timeseries_as_heatmap(values, var_names=labels, highlights_x=[-1, 0.25, 20])
    ax = plt.gcf().axes[0]
    expected = np.asarray(ax.images[0].get_array())
    limits = {"x": ax.get_xlim(), "y": ax.get_ylim()}
    plt.close("all")
    monkeypatch.setattr(
        sc.pl,
        "timeseries_as_heatmap",
        lambda *a, **k: pytest.fail("Called upstream plot"),
    )
    spec = gsc.pl.timeseries_as_heatmap(
        values,
        var_names=labels,
        highlights_x=[-1, 0.25, 20],
        show_values=True,
        zoom="xy",
        show=False,
    ).to_dict()
    tables = [rows for rows in spec["datasets"].values() if "_value" in rows[0]]
    assert len(tables) == 1
    np.testing.assert_array_equal(
        np.array([r["_value"] for r in tables[0]]).reshape(shape[::-1]), expected
    )
    np.testing.assert_array_equal(values, original)
    assert [r["_row"] for r in tables[0][:: shape[0]]] == list(labels)
    assert [r["_column"] for r in tables[0][: shape[0]]] == [
        str(i) for i in range(shape[0])
    ]
    for axis in ("x", "y"):
        np.testing.assert_allclose(spec["scales"][axis]["domain"], limits[axis])
        assert spec["scales"][axis]["type"] == "linear"
        assert spec["scales"][axis]["zoom"] is True
    assert spec["scales"]["y"]["reverse"] is False
    tile = points(spec)
    assert tile["encoding"]["x"]["field"] == "_x0"
    assert tile["encoding"]["x2"]["field"] == "_x1"
    assert {
        step.get("as"): step.get("expr")
        for step in spec["spec"]["layer"][0]["transform"]
        if step["type"] == "formula"
    } == {
        "_x0": "datum._x - 0.5",
        "_x1": "datum._x + 0.5",
        "_y0": "datum._y - 0.5",
        "_y1": "datum._y + 0.5",
    }
    rule = next(mark for mark in leaf_marks(spec) if mark["mark"]["type"] == "rule")
    assert spec["datasets"][rule["data"]["name"]] == [
        {"position": h} for h in (-1, 0.25, 20)
    ]
    assert rule["encoding"]["y"]["datum"] == 0
    assert rule["encoding"]["y2"]["datum"] == shape[1]
    assert rule["mark"]["clip"] is True


@pytest.mark.parametrize(
    "labels", [(), ["same", "same"], np.array([["A", "unused"], ["B", "unused"]])]
)
def test_repeated_default_and_two_dimensional_labels_preserve_slots(labels):
    spec = gsc.pl.timeseries_as_heatmap(
        [[1, 2], [3, 4]], var_names=labels, show=False
    ).to_dict()
    expected = (
        ["0", "1"]
        if not len(labels)
        else ["A", "B"]
        if isinstance(labels, np.ndarray)
        else labels
    )
    table = next(rows for rows in spec["datasets"].values() if "_value" in rows[0])
    assert [r["_row"] for r in table[::2]] == list(expected)


def test_nan_and_masked_inputs_follow_scanpy_conversion_without_mutation():
    values = np.ma.array(
        [[1.0, np.nan], [3.0, 4.0]], mask=[[True, False], [False, False]]
    )
    before = values.copy()
    spec = gsc.pl.timeseries_as_heatmap(values, hover=False, show=False).to_dict()
    table = next(rows for rows in spec["datasets"].values() if "_value" in rows[0])
    assert [row["_value"] for row in table] == [1.0, 3.0, None, 4.0]
    assert points(spec)["mark"]["tooltip"] is None
    np.testing.assert_array_equal(values.data, before.data)
    np.testing.assert_array_equal(values.mask, before.mask)
    assert spec["spec"]["width"] == 372 and spec["spec"]["height"] == 616


@pytest.mark.parametrize(
    "values,options,error,match",
    [
        ([1, 2], {}, ValueError, "two nonempty"),
        ([], {}, ValueError, "two nonempty"),
        (sparse.eye(2), {}, TypeError, "resident 2D"),
        ([[1j]], {}, TypeError, "real numbers"),
        ([["abc"]], {}, TypeError, "real numbers"),
        ([[np.inf]], {}, ValueError, "finite or missing"),
        ([[np.nan]], {}, ValueError, "finite value"),
        ([[1, 2]], {"var_names": ["one"]}, ValueError, "2 labels"),
        ([[1, 2]], {"var_names": "AB"}, TypeError, "var_names"),
        ([[1]], {"var_names": np.zeros((1, 0))}, ValueError, "var_names"),
        ([[1]], {"highlights_x": [np.inf]}, ValueError, "highlights_x"),
        ([[1]], {"highlights_x": [True]}, ValueError, "highlights_x"),
        ([[1]], {"highlights_x": "1"}, TypeError, "highlights_x"),
        ([[1]], {"color_map": object()}, NotImplementedError, "color_map"),
        ([[1]], {"width": 0}, ValueError, "positive"),
        ([[1]], {"hover": "yes"}, TypeError, "hover"),
        ([[1]], {"show_values": "yes"}, TypeError, "show_values"),
        ([[1]], {"zoom": "x"}, TypeError, "zoom"),
        ([[1]], {"ax": None}, TypeError, "ax"),
    ],
)
def test_invalid_inputs_fail_clearly(values, options, error, match):
    with pytest.raises(error, match=match):
        gsc.pl.timeseries_as_heatmap(values, show=False, **options)


def test_dataframe_metadata_does_not_implicitly_supply_labels():
    frame = pd.DataFrame({"B": [1, 2], "A": [3, 4]}, index=["z", "a"])
    spec = gsc.pl.timeseries_as_heatmap(frame, show=False).to_dict()
    table = next(rows for rows in spec["datasets"].values() if "_value" in rows[0])
    assert [r["_row"] for r in table] == ["0", "0", "1", "1"]
    assert [r["_value"] for r in table] == [1, 2, 3, 4]


def test_readonly_noncontiguous_view_keeps_supplied_order_and_data():
    base = np.arange(24).reshape(6, 4)
    values = base[::2, ::-1]
    values.setflags(write=False)
    spec = gsc.pl.timeseries_as_heatmap(values, show=False).to_dict()
    table = next(rows for rows in spec["datasets"].values() if "_value" in rows[0])
    np.testing.assert_array_equal(
        np.array([row["_value"] for row in table]).reshape(4, 3), values.T
    )
    np.testing.assert_array_equal(base, np.arange(24).reshape(6, 4))


def test_lazy_matrix_is_rejected_before_materializing():
    class LazyMatrix:
        def __array__(self, *args, **kwargs):
            pytest.fail("Materialized lazy input")

    with pytest.raises(TypeError, match="resident 2D"):
        gsc.pl.timeseries_as_heatmap(LazyMatrix(), show=False)
