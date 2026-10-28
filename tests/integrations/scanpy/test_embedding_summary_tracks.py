"""Linked tracks reuse detached values, cell identities and the existing renderer."""

import numpy as np
import pytest

import genome_spy.integrations.scanpy as gsc
from tests.integrations.scanpy.embedding_fixtures import adata as adata
from tests.integrations.scanpy.helpers import records
from tests.integrations.scanpy.helpers import leaf_marks, units


@pytest.mark.parametrize("palette", [None, "set1"])
def test_tracks_reuse_values_ids_colors_and_order_without_rereading(
    adata, monkeypatch, palette
):
    import scanpy as sc

    from genome_spy.integrations.scanpy._expression import (
        tracksplot_chart as _tracksplot_chart,
    )
    from genome_spy.integrations.scanpy._expression.grouped_data import heatmap_values

    adata.obs_names = ["duplicate"] * len(adata)
    plot = gsc.pl.EmbeddingSummary(
        adata,
        ["HLA-DRA", "missing.gene"],
        "type",
        categories_order=["B", "A"],
        palette=palette,
    )
    first = plot.to_chart()
    snapshot = first.to_json()
    source = records(first)
    expected_values = adata.to_df().iloc[:, [1, 0]]
    expected_values.index = adata.obs["type"].array.reorder_categories(["B", "A"])
    expected = heatmap_values(expected_values, standard_scale=None)
    original = _tracksplot_chart.build_tracksplot
    calls = []

    def renderer(*args, **kwargs):
        calls.append((args, kwargs))
        return original(*args, **kwargs)

    def forbidden(*args, **kwargs):
        pytest.fail("Adding tracks must not read AnnData or run analysis")

    monkeypatch.setattr(_tracksplot_chart, "build_tracksplot", renderer)
    monkeypatch.setattr(sc.get, "obs_df", forbidden)
    monkeypatch.setattr(sc.tl, "umap", forbidden)
    adata.X[:] = 999
    chart = plot.add_tracks(["missing.gene", "HLA-DRA"], group_gap=3).to_chart()
    assert len(calls) == 1
    prepared, kwargs = calls[0][0][0], calls[0][1]
    np.testing.assert_array_equal(
        prepared.observation_positions, expected.observation_positions
    )
    np.testing.assert_allclose(prepared.values, expected.values, equal_nan=True)
    assert kwargs["value_fields"] == ["_expr_1", "_expr_0"]
    assert kwargs["color_scale"].to_dict() == plot._observations["type"].color.to_dict()
    actual = records(chart)
    assert [row["_obs_id"] for row in actual] == [f"row-{i}" for i in range(len(adata))]
    assert [row["_obs_id"] for row in actual] == [row["_obs_id"] for row in source]
    assert [row["_cell"] for row in actual] == np.argsort(
        expected.observation_positions
    ).tolist()
    assert all(row["_obs_label"] == "duplicate" for row in actual)
    assert first.to_json() == snapshot
    assert (
        len(
            [
                rows
                for rows in chart.to_dict()["datasets"].values()
                if rows and "_obs_id" in rows[0]
            ]
        )
        == 1
    )
    leaves = [leaf for unit in units(chart.to_dict()) for leaf in leaf_marks(unit)]
    selected = [
        leaf for leaf in leaves if leaf.get("name", "").startswith("tracks-selected-")
    ]
    assert len(selected) == 2
    for leaf in selected:
        assert leaf["transform"][-1] == {
            "type": "filter",
            "param": "cells",
            "fields": {"x": "_coord_0", "y": "_coord_1"},
            "empty": True,
        }
    hidden = plot.add_tracks(show=False).to_chart()
    assert records(hidden) == source


@pytest.mark.parametrize(
    "option,value,error",
    [
        ("show", "yes", TypeError),
        ("zoom", 1, TypeError),
        ("width", 0, ValueError),
        ("height", -1, ValueError),
        ("group_gap", -1, ValueError),
        ("spacing", float("nan"), ValueError),
        ("position", "center", ValueError),
        ("var_names", ["other"], ValueError),
    ],
)
def test_tracks_reject_invalid_options(adata, option, value, error):
    plot = gsc.pl.EmbeddingSummary(adata, "HLA-DRA", "type")
    with pytest.raises(error):
        plot.add_tracks(**{option: value})


@pytest.mark.parametrize("missing", [False, True])
def test_tracks_reuse_group_validation(adata, missing):
    if missing:
        adata.obs.loc["cell-0", "type"] = None
    else:
        adata.obs["type"] = adata.obs["type"].cat.add_categories(["Unused"])
    plot = gsc.pl.EmbeddingSummary(adata, "HLA-DRA", "type").add_tracks()
    with pytest.raises(ValueError, match="missing groups|unused categories"):
        plot.to_chart()
