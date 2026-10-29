"""Heatmaps behavior and regressions."""

import json
import warnings
from pathlib import Path

import numpy as np
import pandas as pd
import pytest
from scipy import sparse
from scipy.cluster import hierarchy

import genome_spy.integrations.scanpy as gsc
from genome_spy.integrations.scanpy import pl
from genome_spy.integrations.scanpy._expression import grouped_data as _grouped_data
from genome_spy.integrations.scanpy._expression.clustermap_data import (
    prepare_clustermap,
)
from tests.integrations.scanpy.expression_fixtures import (
    clustermap_cases,
    heatmap_cases,
    make_cluster_adata,
    make_grouped_adata,
    make_heatmap_adata,
    matrix_cases,
)
from tests.integrations.scanpy.helpers import leaf_marks, points, units

sc = pytest.importorskip("scanpy")
HEATMAP_FIXTURES = Path(__file__).with_name("fixtures")


def heatmap_plot(adata, **options):
    return gsc.pl.heatmap(
        adata,
        options.pop("var_names", ["g1", "g2", "g3"]),
        options.pop("groupby", "group"),
        show=False,
        **options,
    )


def heatmap_records(chart):
    spec = chart.to_dict()
    return pd.DataFrame(
        next((rows for rows in spec["datasets"].values() if "_value" in rows[0]))
    )


class TestHeatmap:
    """Cell heatmap semantics, reuse, identity, resource policy and pinned references."""

    @pytest.fixture
    def adata(self):
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", UserWarning)
            return make_heatmap_adata()

    @pytest.mark.parametrize("case", heatmap_cases())
    def test_values_labels_and_bounds_match_frozen_scanpy(self, case):
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", UserWarning)
            a = make_heatmap_adata(case)
            chart = heatmap_plot(a, **heatmap_cases()[case])
        reference = json.loads((HEATMAP_FIXTURES / "heatmap.json").read_text())[
            "cases"
        ][case]
        data = heatmap_records(chart)
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
                    next(
                        (
                            m
                            for m in leaf_marks(spec)
                            if m.get("name") == "heatmap-genes"
                        )
                    )["data"]["name"]
                ]
            ] == labels

    @pytest.mark.parametrize("scale", [None, "obs", "var"])
    def test_log_scaling_and_original_row_identity(self, adata, scale):
        original = np.log1p(adata.X[:, :3])
        if scale is not None:
            axis = 1 if scale == "obs" else 0
            original -= original.min(axis=axis, keepdims=True)
            maximum = original.max(axis=axis, keepdims=True)
            original = np.divide(
                original, maximum, out=np.zeros_like(original), where=maximum != 0
            )
        result = heatmap_records(heatmap_plot(adata, log=True, standard_scale=scale))
        for position in range(adata.n_obs):
            rows = result[result["_obs_id"] == f"row-{position}"]
            assert len(rows) == 3
            assert rows["_obs_label"].tolist() == [adata.obs_names[position]] * 3
            np.testing.assert_allclose(rows["_value"], original[position])

    def test_raw_layer_symbols_and_single_getter_reuse(self, monkeypatch):
        a = make_grouped_adata()
        a = a[~a.obs["group"].isna()].copy()
        original = sc.get.obs_df
        calls = []

        def getter(*args, **kwargs):
            calls.append(kwargs)
            return original(*args, **kwargs)

        monkeypatch.setattr(sc.get, "obs_df", getter)
        raw = heatmap_records(
            heatmap_plot(a, var_names=["ONE_RAW"], gene_symbols="symbol")
        )
        assert len(calls) == 1 and calls[0]["use_raw"] is True
        assert sorted(raw["_value"]) == [3, 5, 7, 9, 13]
        layer = heatmap_records(
            heatmap_plot(a, var_names=["ONE"], gene_symbols="symbol", layer="counts")
        )
        assert len(calls) == 2 and calls[1]["use_raw"] is False
        assert sorted(layer["_value"].dropna()) == [0, 0, 10, 20]

    def test_trees_reorder_cells_markers_and_ids_together_without_analysis(
        self, adata, monkeypatch
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
        result = heatmap_plot(adata, **heatmap_cases()["matched_blocks"])
        data = heatmap_records(result)
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
    def test_unequal_group_spans_and_tree_centers(self, adata, swapped):
        chart = heatmap_plot(adata, dendrogram=True, swap_axes=swapped)
        spec = chart.to_dict()
        tree = spec["surround"]["top" if swapped else "right"][0]
        branches = spec["datasets"][tree["data"]["name"]]
        data = heatmap_records(chart).drop_duplicates("_obs_id")
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
    def test_native_tracks_share_authoritative_gapped_slot_scales(self, adata, swapped):
        spec = heatmap_plot(
            adata,
            var_names={"First": ["g2", "g2"], "Last": ["g1"]},
            dendrogram=True,
            swap_axes=swapped,
            zoom="xy",
            show_values=True,
        ).to_dict()
        data = heatmap_records(heatmap_plot(adata, dendrogram=True))
        stops = (
            data.drop_duplicates("_obs_id")
            .groupby("_group", sort=False)
            .size()
            .cumsum()
        )
        cell, gene = ("x", "y") if swapped else ("y", "x")
        assert spec["scales"][cell]["gapPositions"] == stops.iloc[:-1].tolist()
        assert spec["scales"][gene]["gapPositions"] == [2]
        assert spec["scales"][cell]["domain"] == [0, adata.n_obs - 1]
        assert spec["spec"]["width"] == (1000 if swapped else 90)
        marks = leaf_marks(spec)
        assert all((mark["mark"].get("clip") != "never" for mark in marks))
        for mark in marks:
            for axis in (cell, gene):
                encoding = mark.get("encoding", {}).get(axis, {})
                if encoding.get("type") == "index":
                    assert "scale" not in encoding
        strip = next(
            (mark for mark in marks if mark.get("name") == "heatmap-category-strip")
        )
        labels = next((mark for mark in marks if mark.get("name") == "heatmap-groups"))
        assert "title" not in labels
        assert labels["mark"]["clip"] == ("y" if swapped else "x")
        assert labels["mark"]["cullByVisibleRange"] == cell
        assert len(spec["datasets"][strip["data"]["name"]]) == adata.n_obs
        assert (
            sum(
                (len(rows) for rows in spec["datasets"].values() if "_value" in rows[0])
            )
            == adata.n_obs * 3
        )

    @pytest.mark.parametrize("swapped", [False, True])
    @pytest.mark.parametrize("group_gap", [0, 2.5, 8])
    def test_group_gap_changes_only_shared_scale_widths(
        self, adata, swapped, group_gap
    ):
        options = {
            "var_names": {"First": ["g2", "g2"], "Last": ["g1"]},
            "dendrogram": True,
            "swap_axes": swapped,
            "zoom": "xy",
        }
        expected = heatmap_plot(adata, **options).to_dict()
        assert all((expected["scales"][axis]["gapWidth"] == 0 for axis in ("x", "y")))
        for axis in ("x", "y"):
            expected["scales"][axis]["gapWidth"] = group_gap
        assert heatmap_plot(adata, group_gap=group_gap, **options).to_dict() == expected

    @pytest.mark.parametrize(
        "spans,cuts",
        [
            ([(0, 1), (2, 2)], [2]),
            ([(0, 0)], []),
            ([(0, 1), (1, 2)], []),
            ([(np.int64(0), np.int64(1)), (np.int64(2), np.int64(2))], [2]),
        ],
    )
    def test_only_partitioned_marker_spans_create_gaps(self, adata, spans, cuts):
        spec = json.loads(
            heatmap_plot(
                adata,
                var_group_labels=["block"] * len(spans),
                var_group_positions=spans,
            ).to_json()
        )
        assert spec["scales"]["x"]["gapPositions"] == cuts

    def test_single_group_keeps_all_slots_without_a_group_gap(self):
        spec = heatmap_plot(make_heatmap_adata("one_group")).to_dict()
        assert spec["scales"]["y"]["gapPositions"] == []
        assert len(heatmap_records(heatmap_plot(make_heatmap_adata("one_group")))) == 27
        assert not any(
            (mark.get("name") == "heatmap-category-strip" for mark in leaf_marks(spec))
        )

    @pytest.mark.parametrize("storage", [sparse.csr_matrix, sparse.csc_matrix])
    def test_sparse_views_densify_only_selected_genes(
        self, adata, monkeypatch, storage
    ):
        adata.X = storage(adata.X)
        original = storage.toarray
        shapes = []

        def selected(matrix, *args, **kwargs):
            shapes.append(matrix.shape)
            assert matrix.shape[1] == 2
            return original(matrix, *args, **kwargs)

        monkeypatch.setattr(storage, "toarray", selected)
        chart = heatmap_plot(adata[:5], var_names=["g1", "g2", "g1"])
        assert shapes == [(5, 2)]
        assert len(heatmap_records(chart)) == 15

    @pytest.mark.parametrize("family", ["heatmap", "tracksplot"])
    def test_large_cell_plots_read_only_requested_columns(self, monkeypatch, family):
        import anndata as ad

        import genome_spy as gs
        from genome_spy.integrations.scanpy._expression import (
            heatmap_chart,
            tracksplot_chart,
        )

        a = ad.AnnData(
            sparse.csr_matrix((100000, 20000)),
            obs=pd.DataFrame({"group": pd.Categorical(["A"] * 100000)}),
        )
        a.var_names = [f"g{i}" for i in range(20000)]
        original, shapes, displayed = (sparse.csr_matrix.toarray, [], [])

        def selected(matrix, *args, **kwargs):
            shapes.append(matrix.shape)
            assert matrix.shape == (100000, 3), "Densified unrequested genes"
            return original(matrix, *args, **kwargs)

        def render(prepared, *args, **kwargs):
            displayed.append(prepared.values.shape)
            return gs.Chart().mark_rect()

        monkeypatch.setattr(sparse.csr_matrix, "toarray", selected)
        module = heatmap_chart if family == "heatmap" else tracksplot_chart
        monkeypatch.setattr(module, f"build_{family}", render)
        getattr(gsc.pl, family)(
            a, ["g0", "g1", "g2"], "group", use_raw=False, show=False
        )
        assert shapes == displayed == [(100000, 3)]

    def test_two_groups_get_a_tree_and_many_genes_hide_labels(self, adata):
        a = adata[adata.obs["group"].isin(["C", "A"])].copy()
        a.obs["group"] = a.obs["group"].cat.remove_unused_categories()
        spec = heatmap_plot(a, dendrogram=True).to_dict()
        tree = spec["surround"]["right"][0]
        assert len(spec["datasets"][tree["data"]["name"]]) == 2
        hidden = heatmap_plot(adata, var_names=["g1"] * 51).to_dict()
        shown = heatmap_plot(
            adata, var_names=["g1"] * 51, show_gene_labels=True
        ).to_dict()
        assert len(leaf_marks(hidden)) + 1 == len(leaf_marks(shown))
        labels = shown["datasets"][shown["surround"]["bottom"][0]["data"]["name"]]
        assert [row["label"] for row in labels] == ["g1"] * 51

    def test_partial_marker_labels_use_palette_positions_when_swapped(self, adata):
        spec = heatmap_plot(
            adata, var_names={"A": ["g1"], "other": ["g2"]}, swap_axes=True
        ).to_dict()
        strip = spec["surround"]["right"][0]
        rows = spec["datasets"][strip["data"]["name"]]
        assert [row["label"] for row in rows] == ["C", "A"]

    def test_cell_scaling_precedes_tree_marker_subset(self, adata):
        expected = adata.X[:, :3].copy()
        expected -= expected.min(axis=1, keepdims=True)
        expected /= expected.max(axis=1, keepdims=True)
        data = heatmap_records(
            heatmap_plot(
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

    def test_backed_expression_is_rejected_before_getter(
        self, adata, monkeypatch, tmp_path
    ):
        import anndata as ad

        path = tmp_path / "heatmap.h5ad"
        adata.write_h5ad(path)
        backed = ad.read_h5ad(path, backed="r")
        monkeypatch.setattr(
            sc.get, "obs_df", lambda *a, **kw: pytest.fail("Read backed expression")
        )
        try:
            with pytest.raises(TypeError, match="backed/lazy expression"):
                heatmap_plot(backed)
        finally:
            backed.file.close()

    @pytest.mark.parametrize("swapped", [False, True])
    def test_gene_ticks_and_disabled_hover(self, adata, swapped):
        spec = heatmap_plot(adata, swap_axes=swapped, hover=False).to_dict()
        tiles = points(spec)
        gene, cell = ("y", "x") if swapped else ("x", "y")
        assert tiles["encoding"][gene]["axis"]["values"] == [0, 1, 2]
        assert tiles["encoding"][cell]["axis"] is None
        assert tiles["mark"]["tooltip"] is None
        assert "tooltip" not in tiles["encoding"]

    @pytest.mark.parametrize("kind", ["missing", "unused"])
    def test_invalid_groups_fail_explicitly(self, adata, kind):
        if kind == "missing":
            adata.obs.iloc[0, adata.obs.columns.get_loc("group")] = None
        else:
            adata.obs["group"] = adata.obs["group"].cat.add_categories(["empty"])
        with pytest.raises(ValueError, match="missing groups|unused categories"):
            heatmap_plot(adata)

    @pytest.mark.parametrize(
        "options,error,match",
        [
            ({"norm": object()}, NotImplementedError, "norm"),
            ({"vcenter": 0}, NotImplementedError, "vcenter"),
            ({"interpolation": "bilinear"}, NotImplementedError, "interpolation"),
            ({"standard_scale": "group"}, ValueError, "standard_scale"),
            ({"show_gene_labels": 1}, TypeError, "show_gene_labels"),
            ({"dendrogram": ""}, TypeError, "dendrogram"),
            ({"zoom": "yes"}, TypeError, "zoom"),
            ({"group_gap": -1}, ValueError, "group_gap"),
            ({"group_gap": float("nan")}, ValueError, "group_gap"),
            ({"group_gap": float("inf")}, ValueError, "group_gap"),
            ({"group_gap": True}, ValueError, "group_gap"),
            ({"group_gap": "4"}, ValueError, "group_gap"),
            ({"group_gap": None}, ValueError, "group_gap"),
        ],
    )
    def test_bad_options_fail_before_optional_import(
        self, monkeypatch, options, error, match
    ):
        monkeypatch.setattr(
            pl, "_require_scanpy", lambda *a: pytest.fail("Loaded Scanpy")
        )
        with pytest.raises(error, match=match):
            heatmap_plot(object(), **options)


pytest.importorskip("scanpy")
MATRIX_FIXTURES = Path(__file__).with_name("fixtures")


class TestMatrix:
    """Supplied matrix values, native API defaults and explicit unsupported forms."""

    def test_matrix_tracks_share_contiguous_scales_without_copying_values(self):
        spec = gsc.pl.matrix(
            [[1, np.nan, 3], [4, 5, 6]],
            xticks=["same", "same", "last"],
            yticks=["first", "last"],
            xlabel="Genes",
            ylabel="Groups",
            zoom="xy",
            show_values=True,
            show=False,
        ).to_dict()
        assert set(spec["surround"]) == {"bottom", "left"}
        assert spec["spec"]["width"] == 400
        assert "padding" not in spec and "params" not in spec
        for axis, count in (("x", 3), ("y", 2)):
            assert spec["scales"][axis]["domain"] == [0, count - 1]
            assert spec["scales"][axis]["gapPositions"] == []
            assert spec["scales"][axis]["zoom"] is True
            assert "name" not in spec["scales"][axis]
        for mark in leaf_marks(spec):
            for axis in ("x", "y"):
                assert "scale" not in mark.get("encoding", {}).get(axis, {})
        assert sum(("_value" in rows[0] for rows in spec["datasets"].values())) == 1
        labels = spec["datasets"][spec["surround"]["bottom"][0]["data"]["name"]]
        assert labels == [
            {"slot": 0, "label": "same"},
            {"slot": 1, "label": "same"},
            {"slot": 2, "label": "last"},
        ]

    @pytest.mark.parametrize("case", matrix_cases())
    def test_supplied_matrix_matches_frozen_scanpy_without_plotting(
        self, monkeypatch, case
    ):
        import scanpy as sc

        monkeypatch.setattr(
            sc.pl, "matrix", lambda *a, **k: pytest.fail("Called upstream plot")
        )
        values, options = matrix_cases()[case]
        original = values.copy()
        chart = gsc.pl.matrix(values, show=False, **options)
        spec = chart.to_dict()
        tiles = spec["spec"]
        records = spec["datasets"][tiles["data"]["name"]]
        actual = np.array([row["_value"] for row in records], dtype=float).reshape(
            values.shape
        )
        reference = json.loads((MATRIX_FIXTURES / "matrix.json").read_text())["cases"][
            case
        ]
        np.testing.assert_allclose(
            actual, np.array(reference["values"], dtype=float), equal_nan=True
        )
        np.testing.assert_allclose(
            tiles["encoding"]["color"]["scale"]["domain"], reference["color_domain"]
        )
        assert tiles["encoding"]["color"]["legend"]["gradientLength"] == spec["spec"][
            "height"
        ] * options.get("colorbar_shrink", 0.5)
        np.testing.assert_array_equal(values, original)
        if np.ma.isMaskedArray(values):
            np.testing.assert_array_equal(values.mask, original.mask)

    def test_dataframe_labels_are_used_only_when_explicitly_requested(self):
        values = pd.DataFrame(
            {"B": pd.array([1, None], dtype="Int64"), "A": [3, 5]}, index=["z", "a"]
        )
        for options, expected in (
            ({}, ["0", "1"]),
            ({"xticks": values.columns, "yticks": values.index}, ["B", "A"]),
        ):
            spec = gsc.pl.matrix(values, show=False, **options).to_dict()
            table = spec["datasets"][spec["spec"]["data"]["name"]]
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
    def test_unsupported_matrix_forms_fail_clearly(self, values, options, error, match):
        with pytest.raises(error, match=match):
            gsc.pl.matrix(values, show=False, **options)


class TestClustermap:
    """Clustermap source selection, independent calculations, stored trees and limits."""

    def test_native_tracks_and_contiguous_scales_have_one_owner(self):
        spec = gsc.pl.clustermap(
            make_cluster_adata(), obs_keys="group", show=False
        ).to_dict()
        assert spec["scales"]["x"]["gapPositions"] == []
        assert spec["scales"]["y"]["gapPositions"] == []
        assert spec["spacing"] == 0
        assert set(spec["surround"]) == {"top", "bottom", "left", "right"}
        for mark in leaf_marks(spec):
            assert mark["mark"].get("clip") != "never"
            for axis in ("x", "y"):
                assert (
                    "scale" not in mark.get("encoding", {}).get(axis, {})
                    or mark["encoding"][axis]["type"] != "index"
                )

    @pytest.mark.parametrize("case", clustermap_cases())
    def test_ordered_values_and_geometry_match_frozen_upstream_without_plotting(
        self, monkeypatch, case
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
            adata,
            obs_keys,
            None,
            **{k: v for k, v in options.items() if k != "obs_keys"},
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
        actual = np.array([r["_value"] for r in records], dtype=float).reshape(
            adata.shape
        )
        expected = data.values.to_numpy().copy()
        expected[data.mask] = np.nan
        np.testing.assert_allclose(actual, expected, equal_nan=True)
        np.testing.assert_array_equal(adata.X, original.X)
        pd.testing.assert_frame_equal(adata.obs, original.obs)
        assert set(adata.uns) == set(original.uns)

    def test_scaling_precedes_distances_and_display_masks_do_not_change_trees(self):
        adata = make_cluster_adata()
        data = prepare_clustermap(adata, None, False, z_score=1)
        expected = (adata.X - adata.X.mean(axis=0)) / adata.X.std(axis=0, ddof=1)
        np.testing.assert_allclose(
            data.values, expected[np.ix_(data.row_order, data.col_order)]
        )
        assert abs(data.row_tree.order.index(0) - data.row_tree.order.index(2)) == 1
        positive = data.row_tree.dcoord[data.row_tree.dcoord > 0]
        assert positive.min() == pytest.approx(
            np.linalg.norm(expected[0] - expected[2])
        )
        masked = prepare_clustermap(
            adata, None, False, z_score=1, mask=np.ones(adata.shape, dtype=bool)
        )
        assert data.row_tree.order == masked.row_tree.order
        np.testing.assert_array_equal(data.row_tree.dcoord, masked.row_tree.dcoord)

    @pytest.mark.parametrize("axis", [0, 1])
    def test_standard_scaling_preserves_missing_constant_profiles(self, axis):
        from anndata import AnnData

        profiles = np.array([[4.0, 4, 4], [2, 3, 6]])
        original = profiles if axis == 0 else profiles.T
        adata = AnnData(original.copy())
        data = prepare_clustermap(
            adata,
            None,
            False,
            standard_scale=axis,
            row_cluster=False,
            col_cluster=False,
        )
        expected = np.array([[np.nan, np.nan, np.nan], [0, 0.25, 1]])
        if axis == 1:
            expected = expected.T
        np.testing.assert_allclose(data.values, expected, equal_nan=True)
        np.testing.assert_array_equal(data.mask, np.isnan(expected))
        np.testing.assert_array_equal(adata.X, original)

    def test_observation_strip_owns_category_legend_with_saved_order_and_colors(self):
        adata = make_cluster_adata()
        adata.obs["group"] = adata.obs["group"].cat.add_categories(["unused"])
        adata.obs.iloc[0, 0] = np.nan
        adata.uns["group_colors"] = ["green", "green", "navy", "gold"]
        original = adata.obs.copy()
        data = prepare_clustermap(adata, "group", False)
        pd.testing.assert_series_equal(
            data.obs_labels, original["group"].iloc[list(data.row_order)]
        )
        spec = gsc.pl.clustermap(
            adata, obs_keys="group", zoom=True, show=False
        ).to_dict()
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
        self, monkeypatch
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
    def test_raw_selection_and_resident_storage_use_only_supplied_matrix(self, storage):
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
                data.values,
                expected.toarray() if sparse.issparse(expected) else expected,
            )

    def test_backed_data_rejects_before_expression_reads(self, tmp_path, monkeypatch):
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

    def test_sparse_view_densifies_only_the_supplied_columns(self, monkeypatch):
        import tracemalloc

        from anndata import AnnData

        adata = AnnData(sparse.csr_matrix((1000, 20000), dtype=np.float32))
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

    def test_missing_values_colors_duplicates_and_raw_vocabulary_are_explicit(self):
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
    def test_large_clustermaps_use_requested_clustering_without_size_caps(self, shape):
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
    def test_unsupported_options_fail_clearly(self, options, error, match):
        with pytest.raises(error, match=match):
            gsc.pl.clustermap(make_cluster_adata(), show=False, **options)


def tracksplot_plot(adata, **options):
    return gsc.pl.tracksplot(
        adata,
        options.pop("var_names", ["g1", "g2", "g3"]),
        options.pop("groupby", "group"),
        show=False,
        **options,
    )


def tracksplot_records(chart):
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
                _track=len(tracks), _value=cells[field], _gene=panel["title"]["text"]
            )
        )
    return pd.concat(tracks, ignore_index=True)


class TestTracksplot:
    """Tracks retain Scanpy values and ordering while using native per-cell rects."""

    @pytest.fixture
    def adata(self):
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", UserWarning)
            return make_heatmap_adata()

    @pytest.mark.parametrize("group_gap,spacing", [(0, 0), (3, 6), (7.5, 2.5)])
    def test_spacing_preserves_values_ids_and_cell_order(
        self, adata, group_gap, spacing
    ):
        reference = tracksplot_plot(adata, dendrogram=True).to_dict()
        actual = tracksplot_plot(
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
    def test_invalid_spacing_fails_before_loading_scanpy(
        self, monkeypatch, name, value
    ):
        monkeypatch.setattr(
            pl, "_require_scanpy", lambda *a: pytest.fail("Loaded Scanpy")
        )
        with pytest.raises(ValueError, match=name):
            tracksplot_plot(object(), **{name: value})

    def test_figsize_reserves_room_for_track_spacing(self, adata):
        plain = tracksplot_plot(adata, dendrogram=True, figsize=(6, 4)).to_dict()
        spaced = tracksplot_plot(
            adata, dendrogram=True, figsize=(6, 4), spacing=7
        ).to_dict()

        def extent(spec):
            return sum((panel["height"] for panel in spec["vconcat"])) + spec[
                "spacing"
            ] * (len(spec["vconcat"]) - 1)

        assert extent(spaced) == pytest.approx(extent(plain))
        assert spaced["vconcat"][1]["height"] < plain["vconcat"][1]["height"]

    @pytest.mark.reference
    @pytest.mark.parametrize("log", [False, True])
    @pytest.mark.parametrize("tree", [False, True])
    def test_values_and_color_order_match_upstream_calls(
        self, adata, monkeypatch, log, tree
    ):
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
            chart = tracksplot_plot(
                adata, var_names=["g2", "g1", "g2"], log=log, dendrogram=tree
            )
            data = tracksplot_records(chart)
            spec = chart.to_dict()
            color = units(spec)[1 if tree else 0]["layer"][0]["encoding"]["color"][
                "scale"
            ]
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
                assert rows["_cell"].tolist() == [
                    x for part in expected for x in part[0]
                ]
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

    def test_raw_layer_symbols_and_one_getter_call(self, monkeypatch):
        a = make_grouped_adata()
        a = a[~a.obs["group"].isna()]
        original, calls = (sc.get.obs_df, [])

        def getter(*args, **kwargs):
            calls.append(kwargs)
            return original(*args, **kwargs)

        monkeypatch.setattr(sc.get, "obs_df", getter)
        raw = tracksplot_records(
            tracksplot_plot(a, var_names=["ONE_RAW"], gene_symbols="symbol")
        )
        np.testing.assert_array_equal(np.sort(raw["_value"]), [3, 5, 7, 9, 13])
        layer = tracksplot_records(
            tracksplot_plot(a, var_names=["ONE"], gene_symbols="symbol", layer="counts")
        )
        np.testing.assert_array_equal(np.sort(layer["_value"].dropna()), [0, 0, 10, 20])
        assert [call["use_raw"] for call in calls] == [True, False]
        assert calls[1]["layer"] == "counts"

    def test_shared_tree_permutation_identity_and_detachment(self, adata, monkeypatch):
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
        chart = tracksplot_plot(adata, var_names=markers, dendrogram=True)
        data = tracksplot_records(chart)
        order = list(adata.uns["dendrogram_group"]["categories_ordered"])
        assert order != list(adata.obs["group"].cat.categories)
        assert list(dict.fromkeys(data["_group"])) == order
        spec = chart.to_dict()
        palette = dict(
            zip(
                adata.obs["group"].cat.categories,
                adata.uns["group_colors"],
                strict=True,
            )
        )
        marker_colors = [
            panel["surround"]["right"][0]["mark"]["color"]
            for panel in spec["vconcat"][1:-1]
        ]
        assert marker_colors == [
            palette[group] for group in order for _ in markers[group]
        ]
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
    def test_sparse_view_reads_only_selected_columns(self, adata, monkeypatch, storage):
        adata.X = storage(adata.X)
        original, shapes = (storage.toarray, [])

        def selected(matrix, *args, **kwargs):
            shapes.append(matrix.shape)
            assert matrix.shape[1] == 2
            return original(matrix, *args, **kwargs)

        monkeypatch.setattr(storage, "toarray", selected)
        a = adata[:5]
        assert (
            len(tracksplot_records(tracksplot_plot(a, var_names=["g1", "g2", "g1"])))
            == 15
        )
        assert shapes == [(5, 2)]

    def test_zero_negative_missing_singletons_and_repeated_tracks(self, adata):
        adata.X[:, 0] = 0
        adata.X[0, 1] = -0.5
        adata.X[1, 1] = np.nan
        chart = tracksplot_plot(adata, var_names=["g1", "g2", "g1"])
        data = tracksplot_records(chart)
        assert data["_value"].isna().sum() == 1
        assert len(data) == 27 and (data["_value"] < 0).sum() == 1
        log = tracksplot_plot(adata, log=True).to_dict()
        assert units(log)[0]["layer"][0]["encoding"]["y"]["scale"]["domain"][0] > 0
        assert (
            "datum._value_1 > 0" in units(log)[1]["layer"][0]["transform"][-1]["expr"]
        )
        single = adata[adata.obs["group"] == "A"]
        assert len(tracksplot_records(tracksplot_plot(single))) == 3

    @pytest.mark.parametrize("kind", ["numeric", "missing", "unused"])
    def test_invalid_groups_fail(self, adata, kind):
        if kind == "numeric":
            adata.obs["group"] = np.arange(adata.n_obs)
        elif kind == "missing":
            adata.obs.iloc[0, 0] = None
        else:
            adata.obs["group"] = adata.obs["group"].cat.add_categories(["empty"])
        with pytest.raises(
            ValueError, match="categorical observation|missing groups|unused categories"
        ):
            tracksplot_plot(adata)

    def test_backed_rejection_precedes_expression_access(
        self, adata, monkeypatch, tmp_path
    ):
        import anndata as ad

        monkeypatch.setattr(
            sc.get, "obs_df", lambda *a, **k: pytest.fail("Read expression")
        )
        path = tmp_path / "tracks.h5ad"
        adata.write_h5ad(path)
        backed = ad.read_h5ad(path, backed="r")
        try:
            with pytest.raises(TypeError, match="backed/lazy"):
                tracksplot_plot(backed)
        finally:
            backed.file.close()

    @pytest.mark.parametrize(
        "options,error",
        [
            ({"cmap": "viridis"}, TypeError),
            ({"alpha": 0.5}, TypeError),
            ({"log": 1}, TypeError),
            ({"zoom": "xy"}, TypeError),
            ({"dendrogram": ""}, TypeError),
        ],
    )
    def test_options_fail_before_optional_import(self, monkeypatch, options, error):
        monkeypatch.setattr(
            pl, "_require_scanpy", lambda *a: pytest.fail("Loaded Scanpy")
        )
        with pytest.raises(error, match="gsc.pl.tracksplot"):
            tracksplot_plot(object(), **options)

    @pytest.mark.parametrize(
        "options,error",
        [
            ({"figsize": (4, 4), "width": 300}, TypeError),
            (
                {"var_group_positions": [(0, 0)], "var_group_labels": ["partial"]},
                NotImplementedError,
            ),
        ],
    )
    def test_invalid_dimensions_and_partial_marker_spans_fail(
        self, adata, options, error
    ):
        with pytest.raises(error, match="gsc.pl.tracksplot"):
            tracksplot_plot(adata, **options)
