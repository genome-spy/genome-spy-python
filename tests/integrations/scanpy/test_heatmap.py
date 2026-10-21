"""Cell heatmap semantics, reuse, identity, resource policy and pinned references."""

import inspect
import json
from pathlib import Path
import warnings

import numpy as np
import pandas as pd
import pytest
from scipy import sparse

import genome_spy.integrations.scanpy as gsc
from genome_spy.integrations.scanpy import _grouped_data, pl
from tests.integrations.scanpy.heatmap_fixture import make_heatmap_adata, heatmap_cases
from tests.integrations.scanpy.grouped_fixture import make_grouped_adata
from tests.integrations.scanpy.helpers import leaf_marks, points

sc = pytest.importorskip("scanpy")
FIXTURES = Path(__file__).with_name("fixtures")


@pytest.fixture
def adata():
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", UserWarning)
        return make_heatmap_adata()


def plot(adata, **options):
    return gsc.pl.heatmap(
        adata,
        options.pop("var_names", ["g1", "g2", "g3"]),
        options.pop("groupby", "group"),
        show=False,
        **options,
    )


def records(chart):
    spec = chart.to_dict()
    return pd.DataFrame(
        next(rows for rows in spec["datasets"].values() if "_value" in rows[0])
    )


def test_signature_retains_upstream_defaults_and_native_additions():
    upstream = json.loads((FIXTURES / "api.json").read_text())["entries"]["heatmap"][
        "parameters"
    ]
    actual = inspect.signature(pl.heatmap).parameters
    for parameter in upstream:
        p = actual[parameter["name"]]
        assert p.kind.name == parameter["kind"]
        assert (
            None if p.default is inspect.Parameter.empty else repr(p.default)
        ) == parameter["default"]
    assert set(actual) - {p["name"] for p in upstream} == {
        "hover",
        "zoom",
        "show_values",
        "width",
        "height",
    }


@pytest.mark.parametrize("case", heatmap_cases())
def test_values_labels_and_bounds_match_frozen_scanpy(case):
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", UserWarning)
        a = make_heatmap_adata(case)
        chart = plot(a, **heatmap_cases()[case])
    reference = json.loads((FIXTURES / "heatmap.json").read_text())["cases"][case]
    data = records(chart)
    matrix = data.pivot(index="_y", columns="_x", values="_value").to_numpy()
    np.testing.assert_allclose(
        matrix, np.array(reference["values"], dtype=float), equal_nan=True
    )
    spec = chart.to_dict()
    np.testing.assert_allclose(
        points(spec)["encoding"]["color"]["scale"]["domain"],
        reference["color_domain"],
    )
    labels = (
        reference["y_labels"]
        if heatmap_cases()[case].get("swap_axes")
        else reference["x_labels"]
    )
    if labels:
        assert [
            row["label"]
            for row in spec["datasets"][
                next(m for m in leaf_marks(spec) if m.get("name") == "heatmap-genes")[
                    "data"
                ]["name"]
            ]
        ] == labels


@pytest.mark.parametrize("scale", [None, "obs", "var"])
def test_log_scaling_and_original_row_identity(adata, scale):
    original = np.log1p(adata.X[:, :3])
    if scale is not None:
        axis = 1 if scale == "obs" else 0
        original -= original.min(axis=axis, keepdims=True)
        maximum = original.max(axis=axis, keepdims=True)
        original = np.divide(
            original, maximum, out=np.zeros_like(original), where=maximum != 0
        )
    result = records(plot(adata, log=True, standard_scale=scale))
    for position in range(adata.n_obs):
        rows = result[result["_obs_id"] == f"row-{position}"]
        assert len(rows) == 3
        assert rows["_obs_label"].tolist() == [adata.obs_names[position]] * 3
        np.testing.assert_allclose(rows["_value"], original[position])


def test_raw_layer_symbols_and_single_getter_reuse(monkeypatch):
    a = make_grouped_adata()
    a = a[~a.obs["group"].isna()].copy()
    original = sc.get.obs_df
    calls = []

    def getter(*args, **kwargs):
        calls.append(kwargs)
        return original(*args, **kwargs)

    monkeypatch.setattr(sc.get, "obs_df", getter)
    raw = records(plot(a, var_names=["ONE_RAW"], gene_symbols="symbol"))
    assert len(calls) == 1 and calls[0]["use_raw"] is True
    assert sorted(raw["_value"]) == [3, 5, 7, 9, 13]
    layer = records(plot(a, var_names=["ONE"], gene_symbols="symbol", layer="counts"))
    assert len(calls) == 2 and calls[1]["use_raw"] is False
    assert sorted(layer["_value"].dropna()) == [0, 0, 10, 20]


def test_trees_reorder_cells_markers_and_ids_together_without_analysis(
    adata, monkeypatch
):
    sc.tl.dendrogram(adata, "group")
    order = list(adata.uns["dendrogram_group"]["categories_ordered"])

    def forbidden(*args, **kwargs):
        pytest.fail("Plotting recomputed analysis or group means")

    for name in ("heatmap", "umap", "MatrixPlot"):
        monkeypatch.setattr(sc.pl, name, forbidden)
    for name in ("dendrogram", "umap", "pca", "rank_genes_groups"):
        monkeypatch.setattr(sc.tl, name, forbidden)
    monkeypatch.setattr(_grouped_data, "group_means", forbidden)
    before = adata.copy()
    result = plot(adata, **heatmap_cases()["matched_blocks"])
    data = records(result)
    assert list(dict.fromkeys(data["_group"])) == order
    assert len(data) == adata.n_obs * 5
    assert data["_obs_id"].nunique() == adata.n_obs
    pd.testing.assert_frame_equal(adata.obs, before.obs)
    np.testing.assert_array_equal(adata.X, before.X)
    np.testing.assert_array_equal(
        adata.uns["dendrogram_group"]["linkage"],
        before.uns["dendrogram_group"]["linkage"],
    )
    frozen = result.to_dict()
    adata.X[:] = 99
    assert result.to_dict() == frozen


@pytest.mark.parametrize("swapped", [False, True])
def test_unequal_group_spans_and_tree_centers(adata, swapped):
    chart = plot(adata, dendrogram=True, swap_axes=swapped)
    spec = chart.to_dict()
    tree = spec["surround"]["top" if swapped else "right"][0]
    branches = spec["datasets"][tree["data"]["name"]]
    data = records(chart).drop_duplicates("_obs_id")
    counts = data.groupby("_group", sort=False).size().to_numpy()
    centers = counts.cumsum() - counts / 2 - 0.5
    leaf_positions = sorted(
        {
            row[field] + row[f"{field}_offset"]
            for row in branches
            for field, distance in [("leaf", "distance"), ("leaf2", "distance2")]
            if row[distance] == 0
        }
    )
    np.testing.assert_allclose(leaf_positions, centers)


@pytest.mark.parametrize("swapped", [False, True])
def test_native_tracks_share_authoritative_gapped_slot_scales(adata, swapped):
    spec = plot(
        adata,
        var_names={"First": ["g2", "g2"], "Last": ["g1"]},
        dendrogram=True,
        swap_axes=swapped,
        zoom="xy",
        show_values=True,
    ).to_dict()
    data = records(plot(adata, dendrogram=True))
    stops = (
        data.drop_duplicates("_obs_id").groupby("_group", sort=False).size().cumsum()
    )
    cell, gene = ("x", "y") if swapped else ("y", "x")
    assert spec["scales"][cell]["gapPositions"] == stops.iloc[:-1].tolist()
    assert spec["scales"][gene]["gapPositions"] == [2]
    assert spec["scales"][cell]["domain"] == [0, adata.n_obs - 1]
    assert spec["spec"]["width"] == (1000 if swapped else 90)
    marks = leaf_marks(spec)
    assert all(mark["mark"].get("clip") != "never" for mark in marks)
    for mark in marks:
        for axis in (cell, gene):
            encoding = mark.get("encoding", {}).get(axis, {})
            if encoding.get("type") == "index":
                assert "scale" not in encoding
    strip = next(mark for mark in marks if mark.get("name") == "heatmap-category-strip")
    assert len(spec["datasets"][strip["data"]["name"]]) == adata.n_obs
    assert (
        sum(len(rows) for rows in spec["datasets"].values() if "_value" in rows[0])
        == adata.n_obs * 3
    )


@pytest.mark.parametrize(
    "spans,cuts",
    [
        ([(0, 1), (2, 2)], [2]),
        ([(0, 0)], []),
        ([(0, 1), (1, 2)], []),
        ([(np.int64(0), np.int64(1)), (np.int64(2), np.int64(2))], [2]),
    ],
)
def test_only_partitioned_marker_spans_create_gaps(adata, spans, cuts):
    spec = json.loads(
        plot(
            adata, var_group_labels=["block"] * len(spans), var_group_positions=spans
        ).to_json()
    )
    assert spec["scales"]["x"]["gapPositions"] == cuts


def test_single_group_keeps_all_slots_without_a_group_gap():
    spec = plot(make_heatmap_adata("one_group")).to_dict()
    assert spec["scales"]["y"]["gapPositions"] == []
    assert len(records(plot(make_heatmap_adata("one_group")))) == 27
    assert not any(
        mark.get("name") == "heatmap-category-strip" for mark in leaf_marks(spec)
    )


@pytest.mark.parametrize("storage", [sparse.csr_matrix, sparse.csc_matrix])
def test_sparse_views_densify_only_selected_genes(adata, monkeypatch, storage):
    adata.X = storage(adata.X)
    original = storage.toarray
    shapes = []

    def selected(matrix, *args, **kwargs):
        shapes.append(matrix.shape)
        assert matrix.shape[1] == 2
        return original(matrix, *args, **kwargs)

    monkeypatch.setattr(storage, "toarray", selected)
    chart = plot(adata[:5], var_names=["g1", "g2", "g1"])
    assert shapes == [(5, 2)]
    assert len(records(chart)) == 15


def test_large_request_fails_before_extraction(monkeypatch):
    import anndata as ad

    a = ad.AnnData(
        sparse.csr_matrix((100_000, 20_000)),
        obs=pd.DataFrame({"group": pd.Categorical(["A"] * 100_000)}),
    )
    a.var_names = [f"g{i}" for i in range(20_000)]
    monkeypatch.setattr(
        sc.get, "obs_df", lambda *a, **kw: pytest.fail("Read expression")
    )
    with pytest.raises(ValueError, match="250,000.*subset cells or genes"):
        plot(a, var_names=[f"g{i}" for i in range(50)])


def test_two_groups_get_a_tree_and_many_genes_hide_labels(adata):
    a = adata[adata.obs["group"].isin(["C", "A"])].copy()
    a.obs["group"] = a.obs["group"].cat.remove_unused_categories()
    spec = plot(a, dendrogram=True).to_dict()
    tree = spec["surround"]["right"][0]
    assert len(spec["datasets"][tree["data"]["name"]]) == 2
    hidden = plot(adata, var_names=["g1"] * 51).to_dict()
    shown = plot(adata, var_names=["g1"] * 51, show_gene_labels=True).to_dict()
    assert len(leaf_marks(hidden)) + 1 == len(leaf_marks(shown))
    labels = shown["datasets"][shown["surround"]["bottom"][0]["data"]["name"]]
    assert [row["label"] for row in labels] == ["g1"] * 51


def test_partial_marker_labels_use_palette_positions_when_swapped(adata):
    spec = plot(
        adata, var_names={"A": ["g1"], "other": ["g2"]}, swap_axes=True
    ).to_dict()
    strip = spec["surround"]["right"][0]
    rows = spec["datasets"][strip["data"]["name"]]
    assert [row["label"] for row in rows] == ["C", "A"]


def test_cell_scaling_precedes_tree_marker_subset(adata):
    expected = adata.X[:, :3].copy()
    expected -= expected.min(axis=1, keepdims=True)
    expected /= expected.max(axis=1, keepdims=True)
    data = records(
        plot(
            adata,
            dendrogram=True,
            standard_scale="obs",
            var_group_labels=["C", "A", "D", "B"],
            var_group_positions=[(0, 0)] * 4,
        )
    )
    assert set(data["_gene"]) == {"g1"}
    for position in range(adata.n_obs):
        rows = data[data["_obs_id"] == f"row-{position}"]
        np.testing.assert_allclose(rows["_value"], [expected[position, 0]] * 4)


def test_backed_expression_is_rejected_before_getter(adata, monkeypatch, tmp_path):
    import anndata as ad

    path = tmp_path / "heatmap.h5ad"
    adata.write_h5ad(path)
    backed = ad.read_h5ad(path, backed="r")
    monkeypatch.setattr(
        sc.get, "obs_df", lambda *a, **kw: pytest.fail("Read backed expression")
    )
    try:
        with pytest.raises(TypeError, match="backed/lazy expression"):
            plot(backed)
    finally:
        backed.file.close()


@pytest.mark.parametrize("swapped", [False, True])
def test_gene_ticks_and_disabled_hover(adata, swapped):
    spec = plot(adata, swap_axes=swapped, hover=False).to_dict()
    tiles = points(spec)
    gene, cell = ("y", "x") if swapped else ("x", "y")
    assert tiles["encoding"][gene]["axis"]["values"] == [0, 1, 2]
    assert tiles["encoding"][cell]["axis"] is None
    assert tiles["mark"]["tooltip"] is None
    assert "tooltip" not in tiles["encoding"]


@pytest.mark.parametrize("kind", ["missing", "unused"])
def test_invalid_groups_fail_explicitly(adata, kind):
    if kind == "missing":
        adata.obs.iloc[0, adata.obs.columns.get_loc("group")] = None
    else:
        adata.obs["group"] = adata.obs["group"].cat.add_categories(["empty"])
    with pytest.raises(ValueError, match="missing groups|unused categories"):
        plot(adata)


@pytest.mark.parametrize(
    "options,error,match",
    [
        ({"ax": None}, TypeError, "ax"),
        ({"return_fig": True}, TypeError, "return_fig"),
        ({"norm": object()}, NotImplementedError, "norm"),
        ({"vcenter": 0}, NotImplementedError, "vcenter"),
        ({"interpolation": "bilinear"}, NotImplementedError, "interpolation"),
        ({"standard_scale": "group"}, ValueError, "standard_scale"),
        ({"show_gene_labels": 1}, TypeError, "show_gene_labels"),
        ({"dendrogram": ""}, TypeError, "dendrogram"),
        ({"hover": "yes"}, TypeError, "hover"),
        ({"zoom": "yes"}, TypeError, "zoom"),
    ],
)
def test_bad_options_fail_before_optional_import(monkeypatch, options, error, match):
    monkeypatch.setattr(pl, "_require_scanpy", lambda *a: pytest.fail("Loaded Scanpy"))
    with pytest.raises(error, match=match):
        plot(object(), **options)
