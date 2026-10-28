"""Tracks retain Scanpy values and ordering while using native per-cell rects."""

import warnings

import numpy as np
import pandas as pd
import pytest
from scipy import sparse

import genome_spy.integrations.scanpy as gsc
from genome_spy.integrations.scanpy import pl
from tests.integrations.scanpy.expression_fixtures import make_grouped_adata
from tests.integrations.scanpy.expression_fixtures import make_heatmap_adata
from tests.integrations.scanpy.helpers import units

sc = pytest.importorskip("scanpy")


@pytest.fixture
def adata():
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", UserWarning)
        return make_heatmap_adata()


def plot(adata, **options):
    return gsc.pl.tracksplot(
        adata,
        options.pop("var_names", ["g1", "g2", "g3"]),
        options.pop("groupby", "group"),
        show=False,
        **options,
    )


def records(chart):
    spec = chart.to_dict()
    cells = pd.DataFrame(spec["datasets"][spec["data"]["name"]])
    tracks = []
    for panel in spec["vconcat"]:
        center = panel.get("spec", panel)
        if "layer" not in center:
            continue
        field = center["layer"][0]["encoding"]["y"]["field"]
        tracks.append(
            cells.assign(
                _track=len(tracks),
                _value=cells[field],
                _gene=panel["title"]["text"],
            )
        )
    return pd.concat(tracks, ignore_index=True)


@pytest.mark.parametrize("group_gap,spacing", [(0, 0), (3, 6), (7.5, 2.5)])
def test_spacing_preserves_values_ids_and_cell_order(adata, group_gap, spacing):
    reference = plot(adata, dendrogram=True).to_dict()
    actual = plot(
        adata, dendrogram=True, group_gap=group_gap, spacing=spacing
    ).to_dict()
    assert actual["datasets"] == reference["datasets"]
    assert reference["spacing"] == 0 and reference["scales"]["x"]["gapWidth"] == 0
    assert actual["spacing"] == spacing
    assert actual["scales"]["x"]["gapWidth"] == group_gap
    assert actual["scales"]["x"]["gapPositions"] == [3, 4, 7]
    assert actual["scales"]["x"]["domain"] == [0, adata.n_obs - 1]
    assert [panel.get("spec", panel)["height"] for panel in actual["vconcat"]] == [
        100,
        25,
        25,
        25,
        14,
    ]


@pytest.mark.parametrize("name", ["group_gap", "spacing"])
@pytest.mark.parametrize("value", [-1, True, "4", None, float("nan"), float("inf")])
def test_invalid_spacing_fails_before_loading_scanpy(monkeypatch, name, value):
    monkeypatch.setattr(pl, "_require_scanpy", lambda *a: pytest.fail("Loaded Scanpy"))
    with pytest.raises(ValueError, match=name):
        plot(object(), **{name: value})


def test_figsize_reserves_room_for_track_spacing(adata):
    plain = plot(adata, dendrogram=True, figsize=(6, 4)).to_dict()
    spaced = plot(adata, dendrogram=True, figsize=(6, 4), spacing=7).to_dict()

    def extent(spec):
        return sum(panel["height"] for panel in spec["vconcat"]) + spec["spacing"] * (
            len(spec["vconcat"]) - 1
        )

    assert extent(spaced) == pytest.approx(extent(plain))
    assert spaced["vconcat"][1]["height"] < plain["vconcat"][1]["height"]


@pytest.mark.reference
@pytest.mark.parametrize("log", [False, True])
@pytest.mark.parametrize("tree", [False, True])
def test_values_and_color_order_match_upstream_calls(adata, monkeypatch, log, tree):
    import matplotlib.pyplot as plt
    from matplotlib.axes import Axes

    sc.tl.dendrogram(adata, "group")
    calls = []
    original = Axes.fill_between

    def filled(axis, x, zero, values, **kwargs):
        calls.append((list(x), np.asarray(values).copy(), kwargs["color"]))
        return original(axis, x, zero, values, **kwargs)

    monkeypatch.setattr(Axes, "fill_between", filled)
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", UserWarning)
        reference = sc.pl.tracksplot(
            adata.copy(),
            ["g2", "g1", "g2"],
            "group",
            log=log,
            dendrogram=tree,
            show=False,
        )
    try:
        chart = plot(adata, var_names=["g2", "g1", "g2"], log=log, dendrogram=tree)
        data = records(chart)
        spec = chart.to_dict()
        color = units(spec)[1 if tree else 0]["layer"][0]["encoding"]["color"]["scale"]
        lookup = dict(zip(color["domain"], color["range"], strict=True))
        assert len(calls) == 12
        for slot in range(3):
            rows = data[data["_track"] == slot]
            expected = calls[slot * 4 : (slot + 1) * 4]
            np.testing.assert_allclose(
                rows["_value"],
                np.concatenate([part[1] for part in expected]),
                equal_nan=True,
            )
            assert rows["_cell"].tolist() == [x for part in expected for x in part[0]]
            assert [lookup[label] for label in rows["_group"]] == [
                color for part in expected for color in [part[2]] * len(part[0])
            ]
        assert len(data) == adata.n_obs * 3
        assert [axis.get_yscale() for axis in reference["track_axes"]] == [
            "log" if log else "linear"
        ] * 3
        assert [
            panel["layer"][0]["encoding"]["y"]["scale"]["type"]
            for panel in units(spec)[int(tree) : -1]
        ] == ["log" if log else "linear"] * 3
    finally:
        plt.close("all")


def test_raw_layer_symbols_and_one_getter_call(monkeypatch):
    a = make_grouped_adata()
    a = a[~a.obs["group"].isna()]
    original, calls = sc.get.obs_df, []

    def getter(*args, **kwargs):
        calls.append(kwargs)
        return original(*args, **kwargs)

    monkeypatch.setattr(sc.get, "obs_df", getter)
    raw = records(plot(a, var_names=["ONE_RAW"], gene_symbols="symbol"))
    np.testing.assert_array_equal(np.sort(raw["_value"]), [3, 5, 7, 9, 13])
    layer = records(plot(a, var_names=["ONE"], gene_symbols="symbol", layer="counts"))
    np.testing.assert_array_equal(np.sort(layer["_value"].dropna()), [0, 0, 10, 20])
    assert [call["use_raw"] for call in calls] == [True, False]
    assert calls[1]["layer"] == "counts"


def test_shared_tree_permutation_identity_and_detachment(adata, monkeypatch):
    adata.X = np.random.default_rng(42).random(adata.shape)
    sc.tl.dendrogram(adata, "group")
    before = adata.copy()

    def forbidden(*args, **kwargs):
        pytest.fail("Recomputed analysis or delegated rendering")

    for name in ("tracksplot", "heatmap"):
        monkeypatch.setattr(sc.pl, name, forbidden)
    for name in ("dendrogram", "pca", "umap", "rank_genes_groups"):
        monkeypatch.setattr(sc.tl, name, forbidden)
    markers = {"C": ["g1"], "A": ["g2"], "D": ["g3"], "B": ["g4", "g1"]}
    chart = plot(adata, var_names=markers, dendrogram=True)
    data = records(chart)
    order = list(adata.uns["dendrogram_group"]["categories_ordered"])
    assert order != list(adata.obs["group"].cat.categories)
    assert list(dict.fromkeys(data["_group"])) == order
    spec = chart.to_dict()
    palette = dict(
        zip(adata.obs["group"].cat.categories, adata.uns["group_colors"], strict=True)
    )
    marker_colors = [
        panel["surround"]["right"][0]["mark"]["color"]
        for panel in spec["vconcat"][1:-1]
    ]
    assert marker_colors == [palette[group] for group in order for _ in markers[group]]
    assert data["_obs_id"].nunique() == adata.n_obs
    for _, row in data.iterrows():
        position = int(row["_obs_id"].removeprefix("row-"))
        assert row["_obs_label"] == adata.obs_names[position]
        assert row["_value"] == adata[position, row["_gene"]].X[0, 0]
    pd.testing.assert_frame_equal(adata.obs, before.obs)
    np.testing.assert_array_equal(adata.X, before.X)
    np.testing.assert_array_equal(
        adata.uns["dendrogram_group"]["linkage"],
        before.uns["dendrogram_group"]["linkage"],
    )
    frozen = chart.to_dict()
    adata.X[:] = 99
    assert chart.to_dict() == frozen


@pytest.mark.parametrize("storage", [sparse.csr_matrix, sparse.csc_matrix])
def test_sparse_view_reads_only_selected_columns(adata, monkeypatch, storage):
    adata.X = storage(adata.X)
    original, shapes = storage.toarray, []

    def selected(matrix, *args, **kwargs):
        shapes.append(matrix.shape)
        assert matrix.shape[1] == 2
        return original(matrix, *args, **kwargs)

    monkeypatch.setattr(storage, "toarray", selected)
    a = adata[:5]
    assert len(records(plot(a, var_names=["g1", "g2", "g1"]))) == 15
    assert shapes == [(5, 2)]


def test_zero_negative_missing_singletons_and_repeated_tracks(adata):
    adata.X[:, 0] = 0
    adata.X[0, 1] = -0.5
    adata.X[1, 1] = np.nan
    chart = plot(adata, var_names=["g1", "g2", "g1"])
    data = records(chart)
    assert data["_value"].isna().sum() == 1
    assert len(data) == 27 and (data["_value"] < 0).sum() == 1
    log = plot(adata, log=True).to_dict()
    assert units(log)[0]["layer"][0]["encoding"]["y"]["scale"]["domain"][0] > 0
    assert "datum._value_1 > 0" in units(log)[1]["layer"][0]["transform"][-1]["expr"]
    single = adata[adata.obs["group"] == "A"]
    assert len(records(plot(single))) == 3


@pytest.mark.parametrize("kind", ["numeric", "missing", "unused"])
def test_invalid_groups_fail(adata, kind):
    if kind == "numeric":
        adata.obs["group"] = np.arange(adata.n_obs)
    elif kind == "missing":
        adata.obs.iloc[0, 0] = None
    else:
        adata.obs["group"] = adata.obs["group"].cat.add_categories(["empty"])
    with pytest.raises(
        ValueError, match="categorical observation|missing groups|unused categories"
    ):
        plot(adata)


def test_backed_rejection_precedes_expression_access(adata, monkeypatch, tmp_path):
    import anndata as ad

    monkeypatch.setattr(
        sc.get, "obs_df", lambda *a, **k: pytest.fail("Read expression")
    )
    path = tmp_path / "tracks.h5ad"
    adata.write_h5ad(path)
    backed = ad.read_h5ad(path, backed="r")
    try:
        with pytest.raises(TypeError, match="backed/lazy"):
            plot(backed)
    finally:
        backed.file.close()


@pytest.mark.parametrize(
    "options,error",
    [
        ({"ax": None}, TypeError),
        ({"return_fig": True}, TypeError),
        ({"cmap": "viridis"}, TypeError),
        ({"alpha": 0.5}, TypeError),
        ({"log": 1}, TypeError),
        ({"hover": "yes"}, TypeError),
        ({"zoom": "xy"}, TypeError),
        ({"dendrogram": ""}, TypeError),
    ],
)
def test_options_fail_before_optional_import(monkeypatch, options, error):
    monkeypatch.setattr(pl, "_require_scanpy", lambda *a: pytest.fail("Loaded Scanpy"))
    with pytest.raises(error, match="gsc.pl.tracksplot"):
        plot(object(), **options)


@pytest.mark.parametrize(
    "options,error",
    [
        ({"width": 0}, ValueError),
        ({"height": -1}, ValueError),
        ({"figsize": (4, 4), "width": 300}, TypeError),
        (
            {"var_group_positions": [(0, 0)], "var_group_labels": ["partial"]},
            NotImplementedError,
        ),
    ],
)
def test_invalid_dimensions_and_partial_marker_spans_fail(adata, options, error):
    with pytest.raises(error, match="gsc.pl.tracksplot"):
        plot(adata, **options)
