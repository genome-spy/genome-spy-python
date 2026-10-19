"""Supplied matrix values, native API defaults and explicit unsupported forms."""

import inspect
import json
from pathlib import Path

import numpy as np
import pandas as pd
import pytest
from scipy import sparse

import genome_spy.integrations.scanpy as gsc
from tests.integrations.scanpy.matrix_fixture import matrix_cases

FIXTURES = Path(__file__).with_name("fixtures")


def test_matrix_keeps_scanpy_defaults_without_matplotlib_axes():
    upstream = json.loads((FIXTURES / "api.json").read_text())["entries"]["matrix"][
        "parameters"
    ]
    actual = inspect.signature(gsc.pl.matrix).parameters
    for parameter in upstream:
        if parameter["name"] == "ax":
            assert "ax" not in actual
            continue
        value = actual[parameter["name"]]
        assert value.kind.name == parameter["kind"]
        assert (
            None if value.default is inspect.Parameter.empty else repr(value.default)
        ) == parameter["default"]
    assert set(actual) - {p["name"] for p in upstream} == {
        "hover",
        "width",
        "height",
        "zoom",
        "show_values",
    }


@pytest.mark.parametrize("case", matrix_cases())
def test_supplied_matrix_matches_frozen_scanpy_without_plotting(monkeypatch, case):
    import scanpy as sc

    monkeypatch.setattr(
        sc.pl, "matrix", lambda *a, **k: pytest.fail("Called upstream plot")
    )
    values, options = matrix_cases()[case]
    original = values.copy()
    chart = gsc.pl.matrix(values, show=False, **options)
    spec = chart.to_dict()
    tiles = spec["layer"][0]
    records = spec["datasets"][tiles["data"]["name"]]
    actual = np.array([row["_value"] for row in records], dtype=float).reshape(
        values.shape
    )
    reference = json.loads((FIXTURES / "matrix.json").read_text())["cases"][case]
    np.testing.assert_allclose(
        actual, np.array(reference["values"], dtype=float), equal_nan=True
    )
    np.testing.assert_allclose(
        tiles["encoding"]["color"]["scale"]["domain"], reference["color_domain"]
    )
    assert tiles["encoding"]["color"]["legend"]["gradientLength"] == spec[
        "height"
    ] * options.get("colorbar_shrink", 0.5)
    np.testing.assert_array_equal(values, original)
    if np.ma.isMaskedArray(values):
        np.testing.assert_array_equal(values.mask, original.mask)


def test_dataframe_labels_are_used_only_when_explicitly_requested():
    values = pd.DataFrame(
        {"B": pd.array([1, None], dtype="Int64"), "A": [3, 5]}, index=["z", "a"]
    )
    for options, expected in (
        ({}, ["0", "1"]),
        ({"xticks": values.columns, "yticks": values.index}, ["B", "A"]),
    ):
        spec = gsc.pl.matrix(values, show=False, **options).to_dict()
        table = spec["datasets"][spec["layer"][0]["data"]["name"]]
        assert [row["_column"] for row in table[:2]] == expected
        assert table[2]["_value"] is None


@pytest.mark.parametrize(
    "values,options,error,match",
    [
        ([1, 2], {}, ValueError, "two nonempty"),
        ([], {}, ValueError, "two nonempty"),
        (np.zeros((2, 2, 3)), {}, ValueError, "two nonempty"),
        ([[1j]], {}, TypeError, "real numbers"),
        ([["abc"]], {}, TypeError, "real numbers"),
        ([[np.inf]], {}, ValueError, "finite or missing"),
        ([[np.nan]], {}, ValueError, "finite value"),
        (sparse.eye(2), {}, TypeError, "resident 2D"),
        ([[1, 2]], {"xticks": ["one"]}, ValueError, "2 labels"),
        ([[1, 2]], {"xticks": "AB"}, ValueError, "2 labels"),
        ([[1]], {"xlabel": 1}, TypeError, "xlabel"),
        ([[1]], {"color_map": "made-up"}, NotImplementedError, "color_map"),
        ([[1]], {"color_map": object()}, NotImplementedError, "color_map"),
        ([[1]], {"colorbar_shrink": 0}, ValueError, "positive"),
        ([[1]], {"width": 0}, ValueError, "positive"),
        ([[1]], {"hover": "yes"}, TypeError, "hover"),
        ([[1]], {"ax": None}, TypeError, "ax"),
        ([[1]], {"norm": object()}, TypeError, "norm"),
    ],
)
def test_unsupported_matrix_forms_fail_clearly(values, options, error, match):
    with pytest.raises(error, match=match):
        gsc.pl.matrix(values, show=False, **options)
