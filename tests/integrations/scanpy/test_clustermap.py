"""Clustermap source selection, independent calculations, stored trees and limits."""

import inspect
import json
from pathlib import Path

import numpy as np
import pandas as pd
import pytest
from scipy import sparse
from scipy.cluster import hierarchy

import genome_spy.integrations.scanpy as gsc
from genome_spy.integrations.scanpy._expression.clustermap_data import (
    prepare_clustermap,
)
from tests.integrations.scanpy.clustermap_fixture import (
    make_cluster_adata,
    clustermap_cases,
)
from tests.integrations.scanpy.helpers import points, leaf_marks


def test_clustermap_signature_preserves_scanpy_contract():
    upstream = json.loads(
        (Path(__file__).with_name("fixtures") / "api.json").read_text()
    )["entries"]["clustermap"]["parameters"]
    actual = inspect.signature(gsc.pl.clustermap).parameters
    for parameter in upstream:
        native = actual[parameter["name"]]
        assert native.kind.name == parameter["kind"]
        assert (
            None if native.default is inspect.Parameter.empty else repr(native.default)
        ) == parameter["default"]
    assert set(actual) - {p["name"] for p in upstream} == {
        "hover",
        "zoom",
        "show_values",
        "highlight",
        "width",
        "height",
    }


def test_native_tracks_and_contiguous_scales_have_one_owner():
    spec = gsc.pl.clustermap(
        make_cluster_adata(),
        obs_keys="group",
        show=False,
    ).to_dict()
    assert spec["scales"]["x"]["gapPositions"] == []
    assert spec["scales"]["y"]["gapPositions"] == []
    assert spec["spacing"] == 0
    assert set(spec["surround"]) == {"top", "bottom", "left", "right"}
    for mark in leaf_marks(spec):
        assert mark["mark"].get("clip") != "never"
        for axis in ("x", "y"):
            assert "scale" not in mark.get("encoding", {}).get(axis, {}) or (
                mark["encoding"][axis]["type"] != "index"
            )


@pytest.mark.parametrize("case", clustermap_cases())
def test_ordered_values_and_geometry_match_frozen_upstream_without_plotting(
    monkeypatch, case
):
    import scanpy as sc
    import seaborn as sns

    monkeypatch.setattr(
        sc.pl, "clustermap", lambda *a, **k: pytest.fail("Called upstream plot")
    )
    monkeypatch.setattr(
        sns, "clustermap", lambda *a, **k: pytest.fail("Called Seaborn plot")
    )
    adata = make_cluster_adata()
    original = adata.copy()
    options = clustermap_cases()[case]
    obs_keys = options.get("obs_keys")
    data = prepare_clustermap(
        adata, obs_keys, None, **{k: v for k, v in options.items() if k != "obs_keys"}
    )
    reference = json.loads(
        (Path(__file__).with_name("fixtures") / "clustermap.json").read_text()
    )["cases"][case]
    assert list(data.row_order) == reference["row_order"]
    assert list(data.col_order) == reference["col_order"]
    np.testing.assert_allclose(data.values, reference["values"])
    np.testing.assert_array_equal(data.mask, reference["mask"])
    for name, tree in (("row", data.row_tree), ("col", data.col_tree)):
        expected = reference[name + "_tree"]
        if expected is None:
            assert tree is None
        else:
            np.testing.assert_allclose(tree.icoord, expected["icoord"])
            np.testing.assert_allclose(tree.dcoord, expected["dcoord"])
    chart = gsc.pl.clustermap(adata, show=False, cmap="viridis", **options)
    spec = chart.to_dict()
    tiles = points(spec)
    records = spec["datasets"][tiles["data"]["name"]]
    actual = np.array([r["_value"] for r in records], dtype=float).reshape(adata.shape)
    expected = data.values.to_numpy().copy()
    expected[data.mask] = np.nan
    np.testing.assert_allclose(actual, expected, equal_nan=True)
    np.testing.assert_array_equal(adata.X, original.X)
    pd.testing.assert_frame_equal(adata.obs, original.obs)
    assert set(adata.uns) == set(original.uns)


def test_scaling_precedes_distances_and_display_masks_do_not_change_trees():
    adata = make_cluster_adata()
    data = prepare_clustermap(adata, None, False, z_score=1)
    expected = (adata.X - adata.X.mean(axis=0)) / adata.X.std(axis=0, ddof=1)
    np.testing.assert_allclose(
        data.values, expected[np.ix_(data.row_order, data.col_order)]
    )
    assert abs(data.row_tree.order.index(0) - data.row_tree.order.index(2)) == 1
    positive = data.row_tree.dcoord[data.row_tree.dcoord > 0]
    assert positive.min() == pytest.approx(np.linalg.norm(expected[0] - expected[2]))
    masked = prepare_clustermap(
        adata, None, False, z_score=1, mask=np.ones(adata.shape, dtype=bool)
    )
    assert data.row_tree.order == masked.row_tree.order
    np.testing.assert_array_equal(data.row_tree.dcoord, masked.row_tree.dcoord)


@pytest.mark.parametrize("axis", [0, 1])
def test_standard_scaling_preserves_missing_constant_profiles(axis):
    from anndata import AnnData

    profiles = np.array([[4.0, 4, 4], [2, 3, 6]])
    original = profiles if axis == 0 else profiles.T
    adata = AnnData(original.copy())

    data = prepare_clustermap(
        adata, None, False, standard_scale=axis, row_cluster=False, col_cluster=False
    )

    expected = np.array([[np.nan, np.nan, np.nan], [0, 0.25, 1]])
    if axis == 1:
        expected = expected.T
    np.testing.assert_allclose(data.values, expected, equal_nan=True)
    np.testing.assert_array_equal(data.mask, np.isnan(expected))
    np.testing.assert_array_equal(adata.X, original)


def test_observation_strip_owns_category_legend_with_saved_order_and_colors():
    adata = make_cluster_adata()
    adata.obs["group"] = adata.obs["group"].cat.add_categories(["unused"])
    adata.obs.iloc[0, 0] = np.nan
    adata.uns["group_colors"] = ["green", "green", "navy", "gold"]
    original = adata.obs.copy()
    data = prepare_clustermap(adata, "group", False)
    pd.testing.assert_series_equal(
        data.obs_labels, original["group"].iloc[list(data.row_order)]
    )
    spec = gsc.pl.clustermap(adata, obs_keys="group", zoom=True, show=False).to_dict()
    strips = [
        mark
        for mark in leaf_marks(spec)
        if mark.get("encoding", {}).get("color", {}).get("legend", {}) is not None
        and mark.get("encoding", {}).get("color", {}).get("legend", {}).get("title")
        == "group"
    ]
    assert len(strips) == 1
    strip = strips[0]
    assert strip["mark"]["type"] == "rect"
    color = strip["encoding"]["color"]
    assert color["scale"] == {
        "type": "ordinal",
        "domain": ["C", "B", "A", "unused"],
        "range": ["green", "green", "navy", "gold"],
    }
    assert color["legend"]["symbolType"] == "square"
    assert {"type": "filter", "expr": "isValid(datum._color)"} in strip["transform"]
    rows = spec["datasets"][strip["data"]["name"]]
    assert [row["_color"] for row in rows] == [
        None if pd.isna(label) else label for label in data.obs_labels
    ]
    pd.testing.assert_frame_equal(adata.obs, original)
    # Explicit CSS tracks do not invent category names or a second mark layer.
    explicit = gsc.pl.clustermap(
        adata,
        row_colors=pd.Series(["green"] * 6, index=adata.obs_names, name="group"),
        zoom=True,
        show=False,
    ).to_dict()
    assert len(leaf_marks(explicit)) == len(leaf_marks(spec))


def test_supplied_linkage_is_authoritative_and_annotations_follow_both_orders(
    monkeypatch,
):
    adata = make_cluster_adata()
    row = hierarchy.linkage(adata.X[::-1], method="single")
    col = hierarchy.linkage(adata.X.T[::-1], method="complete")
    expected_rows = tuple(hierarchy.leaves_list(row))
    expected_cols = tuple(hierarchy.leaves_list(col))
    monkeypatch.setattr(
        hierarchy, "linkage", lambda *a, **k: pytest.fail("Recomputed linkage")
    )
    colors = pd.DataFrame(
        {
            "first": ["red", "blue", "green", "gold", "black", "purple"],
            "second": ["white"] * 6,
        },
        index=adata.obs_names,
    ).iloc[::-1]
    data = prepare_clustermap(
        adata,
        None,
        False,
        row_linkage=row,
        col_linkage=col,
        row_colors=colors,
        col_colors=["red", "green", "blue", "black"],
    )
    assert data.row_order == expected_rows and data.col_order == expected_cols
    pd.testing.assert_frame_equal(
        data.row_colors, colors.reindex(adata.obs_names).iloc[list(expected_rows)]
    )
    assert data.col_colors.iloc[:, 0].tolist() == [
        ["red", "green", "blue", "black"][i] for i in expected_cols
    ]


@pytest.mark.parametrize("storage", ["dense", "csr", "csc", "view"])
def test_raw_selection_and_resident_storage_use_only_supplied_matrix(storage):
    adata = make_cluster_adata()
    raw = adata.copy()
    raw.X = raw.X + 100
    adata.raw = raw
    if storage in ("csr", "csc"):
        adata.X = getattr(sparse, storage + "_matrix")(adata.X)
    if storage == "view":
        adata = adata[[3, 2, 1], :]
        raw = raw[[3, 2, 1], :].copy()
        assert adata.is_view
    for option, expected in ((None, raw.X), (False, adata.X)):
        data = prepare_clustermap(
            adata, None, option, row_cluster=False, col_cluster=False
        )
        np.testing.assert_allclose(
            data.values, expected.toarray() if sparse.issparse(expected) else expected
        )


def test_backed_data_rejects_before_expression_reads(tmp_path, monkeypatch):
    import anndata as ad

    path = tmp_path / "cells.h5ad"
    make_cluster_adata().write_h5ad(path)
    backed = ad.read_h5ad(path, backed="r")
    try:
        monkeypatch.setattr(
            ad.AnnData,
            "X",
            property(lambda self: pytest.fail("Read backed expression")),
        )
        with pytest.raises(TypeError, match="clustermap.*backed/lazy"):
            prepare_clustermap(backed, None, False)
    finally:
        backed.file.close()


def test_sparse_view_densifies_only_the_supplied_columns(monkeypatch):
    from anndata import AnnData
    import tracemalloc

    adata = AnnData(sparse.csr_matrix((1000, 20_000), dtype=np.float32))
    selected = adata[:, [2, 100, 700]]
    shapes = []
    original = sparse.csr_matrix.toarray

    def bounded(matrix, *args, **kwargs):
        shapes.append(matrix.shape)
        assert matrix.shape == (1000, 3)
        return original(matrix, *args, **kwargs)

    monkeypatch.setattr(sparse.csr_matrix, "toarray", bounded)
    tracemalloc.start()
    try:
        result = prepare_clustermap(
            selected, None, False, row_cluster=False, col_cluster=False
        )
        _, peak = tracemalloc.get_traced_memory()
    finally:
        tracemalloc.stop()
    assert shapes == [(1000, 3)]
    assert result.values.shape == (1000, 3)
    assert peak < 16 * 1024 * 1024


def test_missing_values_colors_duplicates_and_raw_vocabulary_are_explicit():
    adata = make_cluster_adata()
    adata.obs_names = ["repeat"] * 6
    adata.var_names = ["same", "same", "C", "D"]
    adata.X[0, 0] = np.nan
    colors = pd.Series(["red", "blue"], index=["same", "C"], name="annotation")
    data = prepare_clustermap(
        adata, None, False, row_cluster=False, col_cluster=False, col_colors=colors
    )
    assert data.row_order == tuple(range(6)) and data.col_order == tuple(range(4))
    assert data.col_colors.iloc[:, 0].tolist() == ["red", "red", "blue", "white"]
    assert data.mask[0, 0] and data.mask.sum() == 1
    with pytest.raises(ValueError, match="clustermap.*finite"):
        prepare_clustermap(adata, None, False)
    adata = make_cluster_adata()
    adata.raw = adata.copy()
    subset = adata[:, :2]
    with pytest.raises(ValueError, match="raw and X"):
        prepare_clustermap(subset, None, None)


@pytest.mark.parametrize("shape", [(501, 501), (1500, 2)])
def test_large_clustermaps_use_requested_clustering_without_size_caps(shape):
    from anndata import AnnData

    a = AnnData(np.random.default_rng(0).normal(size=shape))
    cluster_rows = shape[0] == 1500
    prepared = prepare_clustermap(
        a, None, False, row_cluster=cluster_rows, col_cluster=False
    )
    assert prepared.values.shape == shape
    if cluster_rows:
        assert prepared.row_tree is not None
        assert set(prepared.row_tree.order) == set(range(shape[0]))
    else:
        np.testing.assert_array_equal(prepared.values, a.X)


@pytest.mark.parametrize(
    "options,error,match",
    [
        ({"norm": object()}, TypeError, "norm"),
        ({"tree_kws": {}}, TypeError, "tree_kws"),
        ({"ax": None}, TypeError, "ax is omitted"),
        ({"hover": 1}, TypeError, "hover"),
        ({"obs_keys": ["group"]}, TypeError, "obs_keys"),
        ({"obs_keys": "missing"}, ValueError, "obs_keys"),
        ({"z_score": 0, "standard_scale": 1}, ValueError, "cannot be combined"),
        ({"row_cluster": "False"}, TypeError, "row_cluster"),
        ({"row_linkage": [[0, 1, 1, 2]]}, ValueError, "axis length"),
        ({"mask": [[True]]}, ValueError, "mask"),
        ({"row_colors": ["red"]}, ValueError, "row_colors"),
        ({"cmap": "rocket"}, NotImplementedError, "GenomeSpy scheme"),
        ({"cbar_kws": {"ticks": [0, 1]}}, TypeError, "cbar_kws"),
        ({"cbar_pos": (0, 0, 1, 1)}, NotImplementedError, "cbar_pos"),
        ({"dendrogram_ratio": 1}, ValueError, "ratio"),
    ],
)
def test_unsupported_options_fail_clearly(options, error, match):
    with pytest.raises(error, match=match):
        gsc.pl.clustermap(make_cluster_adata(), show=False, **options)
