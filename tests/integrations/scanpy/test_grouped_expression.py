"""Grouped expression behavior and regressions."""

import json
import warnings
from dataclasses import asdict
from pathlib import Path

import numpy as np
import pandas as pd
import pytest
from scipy import sparse

import genome_spy.integrations.scanpy as gsc
from genome_spy.integrations.scanpy import pl
from genome_spy.integrations.scanpy._expression import grouped_data as _grouped_data
from genome_spy.integrations.scanpy._expression.grouped_data import (
    expression_fractions,
    group_means,
    grouped_expression,
    scale_values,
)
from tests.integrations.scanpy.expression_fixtures import (
    dotplot_cases,
    grouped_cases,
    make_grouped_adata,
    matrixplot_cases,
)
from tests.integrations.scanpy.helpers import points

sc = pytest.importorskip("scanpy")
GROUPED_DATA_FIXTURE = Path(__file__).with_name("fixtures") / "grouped.json"
GROUPED_DATA_REFERENCE = json.loads(GROUPED_DATA_FIXTURE.read_text())


class TestGroupedData:
    """Independent grouped-data semantics plus explicitly frozen upstream results."""

    @pytest.fixture
    def adata(self):
        with pytest.warns(UserWarning, match="Observation names are not unique"):
            a = make_grouped_adata()
        a.obs.index.name = "barcode"
        return a

    def test_means_fractions_and_scaling_have_independent_denominators(self, adata):
        table = grouped_expression(
            adata, ["g1", "g2", "g3"], "group", use_raw=False
        ).values
        means = group_means(table)
        assert list(means.index) == ["B", "A"]
        np.testing.assert_allclose(means, [[1, 1, 4], [0.5, 1.5, 4]])
        np.testing.assert_allclose(
            expression_fractions(table), [[1 / 3, 2 / 3, 1], [0.5, 0.5, 1]]
        )
        np.testing.assert_allclose(
            group_means(table, expression_cutoff=1), [[2, 2, 4], [0, 3, 4]]
        )
        np.testing.assert_allclose(
            expression_fractions(table, expression_cutoff=1),
            [[1 / 3, 1 / 3, 1], [0, 0.5, 1]],
        )
        np.testing.assert_allclose(
            expression_fractions(table, expression_cutoff=-0.5),
            [[2 / 3, 1, 1], [1, 1, 1]],
        )
        np.testing.assert_allclose(scale_values(means, "var"), [[1, 0, 0], [0, 1, 0]])
        np.testing.assert_allclose(
            scale_values(means, "group"), [[0, 0, 1], [0, 2 / 7, 1]]
        )
        np.testing.assert_allclose(means, [[1, 1, 4], [0.5, 1.5, 4]])

    def test_log_is_applied_to_observations_before_means_and_cutoffs(self, adata):
        table = grouped_expression(
            adata, ["g1", "g2", "g3"], "group", use_raw=False, log=True
        ).values
        np.testing.assert_allclose(
            group_means(table),
            [
                [np.log(3) / 2, (np.log(2) + np.log(3)) / 3, np.log(5)],
                [np.log(2) / 2, np.log(4) / 2, np.log(5)],
            ],
        )
        np.testing.assert_allclose(
            expression_fractions(table, expression_cutoff=1.5), [[0, 0, 1], [0, 0, 1]]
        )
        assert not np.allclose(
            group_means(table).iloc[:, :2], np.log1p([[1, 1], [0.5, 1.5]])
        )

    @pytest.mark.parametrize(
        "options,names,expected",
        [
            ({}, ["g1"], [3, 5, 7, 9, 11, 13]),
            ({"use_raw": False}, ["g1"], [0, 1, 2, 0, 9, np.nan]),
            ({"layer": "counts"}, ["g1"], [0, 10, 20, 0, 90, np.nan]),
            ({"gene_symbols": "symbol"}, ["ONE_RAW"], [3, 5, 7, 9, 11, 13]),
            (
                {"gene_symbols": "symbol", "use_raw": False},
                ["ONE"],
                [0, 1, 2, 0, 9, np.nan],
            ),
        ],
    )
    def test_selected_source_and_raw_symbols(self, adata, options, names, expected):
        table = grouped_expression(adata, names, "group", **options).values
        np.testing.assert_allclose(table.iloc[:, 0], expected, equal_nan=True)

    def test_repeated_slots_and_brackets_do_not_multiply_columns(self, adata):
        result = grouped_expression(
            adata, {"first": ["g2", "g1"], "again": "g2"}, "group", use_raw=False
        )
        assert list(result.values.columns) == ["g2", "g1", "g2"]
        assert [asdict(group) for group in result.feature_groups] == [
            {"label": "first", "start": 0, "end": 1},
            {"label": "again", "start": 2, "end": 2},
        ]
        np.testing.assert_allclose(
            group_means(result.values), [[1, 1, 1], [1.5, 0.5, 1.5]]
        )
        assert result.values.shape == (6, 3)

    def test_explicit_brackets_use_inclusive_slot_positions(self, adata):
        result = grouped_expression(
            adata,
            ["g1", "g2"],
            "group",
            var_group_labels=["markers"],
            var_group_positions=[(0, 1)],
        )
        assert [asdict(group) for group in result.feature_groups] == [
            {"label": "markers", "start": 0, "end": 1}
        ]

    def test_numeric_bin_edges_and_source_row_order_are_preserved(self, adata):
        table = grouped_expression(
            adata, "g1", "numeric", use_raw=False, num_categories=3
        ).values
        assert table.index.codes.tolist() == [0, 0, 1, 1, 2, 2]
        assert table.index.categories[0].left == -0.005
        assert [interval.right for interval in table.index.categories] == [
            1.667,
            3.333,
            5,
        ]
        np.testing.assert_allclose(
            table.iloc[:, 0], [0, 1, 2, 0, 9, np.nan], equal_nan=True
        )

    def test_string_sanitization_matches_anndata_without_mutating_annotations(
        self, adata
    ):
        before = adata.obs.copy(deep=True)
        table = grouped_expression(adata, "g1", "plain", use_raw=False).values
        assert table.index.categories.tolist() == ["2", "10"]
        pd.testing.assert_frame_equal(adata.obs, before)
        adata.obs["plain"] = ["10", "2", "30", "4", "50", "6"]
        unique = grouped_expression(adata, "g1", "plain", use_raw=False).values
        assert unique.index.categories.tolist() == ["10", "2", "30", "4", "50", "6"]

    def test_multi_key_groups_follow_category_product_order(self, adata):
        a = adata[adata.obs["group"].notna()]
        table = grouped_expression(a, "g1", ["group", "batch"], use_raw=False).values
        assert table.index.categories.tolist() == ["B_y", "B_x", "A_y", "A_x"]
        assert table.index.tolist() == ["B_x", "A_x", "B_y", "A_y", "B_x"]
        assert a.is_view

    def test_named_index_grouping_preserves_duplicate_observations(self, adata):
        table = grouped_expression(adata, "g2", "barcode", use_raw=False).values
        assert table.index.tolist() == adata.obs_names.tolist()
        assert table.index.name == "barcode"
        assert len(table) == 6
        assert group_means(table).loc["same", "g2"] == 0.5

    def test_supplied_category_order_is_validated_and_applied(self, adata):
        result = grouped_expression(
            adata, "g2", "group", use_raw=False, categories_order=["A", "B"]
        )
        assert result.values.index.categories.tolist() == ["A", "B"]
        assert list(group_means(result.values).index) == ["A", "B"]
        for invalid in (["A"], ["A", "A"], ["A", "B", "C"]):
            with pytest.raises(ValueError, match="categories"):
                grouped_expression(adata, "g2", "group", categories_order=invalid)

    def test_unused_categories_remain_metadata_without_invented_observations(
        self, adata
    ):
        adata.obs["group"] = adata.obs["group"].cat.add_categories(["unused"])
        table = grouped_expression(adata, "g2", "group", use_raw=False).values
        assert table.index.categories.tolist() == ["B", "A", "unused"]
        assert group_means(table).index.tolist() == ["B", "A"]
        assert expression_fractions(table).index.tolist() == ["B", "A"]

    def test_all_missing_groups_do_not_invent_statistics(self, adata):
        adata.obs["group"] = pd.Categorical([None] * 6, categories=["B", "A"])
        table = grouped_expression(adata, "g2", "group", use_raw=False).values
        assert table.index.categories.tolist() == ["B", "A"]
        assert group_means(table).shape == expression_fractions(table).shape == (0, 1)

    def test_nullable_metadata_preserves_its_comparison_denominator(self, adata):
        adata.obs["nullable"] = pd.array([0, 1, 2, 0, 9, None], dtype="Float64")
        table = grouped_expression(adata, "nullable", "group", use_raw=False).values
        assert expression_fractions(table).iloc[:, 0].tolist() == [0.5, 0.5]
        assert group_means(table).iloc[:, 0].tolist() == [1, 0.5]

    @pytest.mark.parametrize("format", ["csr_matrix", "csc_matrix"])
    def test_sparse_access_only_densifies_requested_unique_columns(
        self, adata, monkeypatch, format
    ):
        adata.X = getattr(sparse, format)(adata.X)
        dense_shapes = []
        cls = type(adata.X)
        original = cls.toarray

        def track(matrix, *args, **kwargs):
            dense_shapes.append(matrix.shape)
            return original(matrix, *args, **kwargs)

        monkeypatch.setattr(cls, "toarray", track)
        table = grouped_expression(
            adata, ["g2", "g1", "g2"], "group", use_raw=False
        ).values
        assert dense_shapes == [(6, 2)]
        assert list(table.columns) == ["g2", "g1", "g2"]
        np.testing.assert_allclose(group_means(table), [[1, 1, 1], [1.5, 0.5, 1.5]])

    @pytest.mark.parametrize("format", ["csr_array", "csc_array"])
    def test_sparse_array_limit_is_explicit_before_the_upstream_getter(
        self, adata, monkeypatch, format
    ):
        adata.X = getattr(sparse, format)(adata.X)
        monkeypatch.setattr(
            sc.get, "obs_df", lambda *args, **kwargs: pytest.fail("Getter ran")
        )
        with pytest.raises(NotImplementedError, match="does not support sparse arrays"):
            grouped_expression(adata, "g1", "group", use_raw=False)

    def test_view_reads_are_snapshots_without_analysis_or_cache_writes(
        self, adata, monkeypatch
    ):
        before_obs, before_var = (adata.obs.copy(deep=True), adata.var.copy(deep=True))
        adata.uns["group_colors"] = ["red", "blue"]
        for name in ("pca", "umap", "dendrogram", "rank_genes_groups"):
            monkeypatch.setattr(
                sc.tl, name, lambda *a, **k: pytest.fail("Analysis ran")
            )
        original = sc.get.obs_df
        calls = []

        def record(*args, **kwargs):
            calls.append(kwargs["keys"])
            return original(*args, **kwargs)

        monkeypatch.setattr(sc.get, "obs_df", record)
        view = adata[[3, 0, 5]]
        result = grouped_expression(view, ["g1", "g2", "g1"], "group", use_raw=False)
        assert calls == [["group", "g1", "g2"]]
        assert view.is_view
        np.testing.assert_allclose(
            result.values.iloc[:, 0], [0, 0, np.nan], equal_nan=True
        )
        adata.X[0, 0] = 100
        assert result.values.iloc[1, 0] == 0
        pd.testing.assert_frame_equal(adata.obs, before_obs)
        pd.testing.assert_frame_equal(adata.var, before_var)
        assert adata.uns == {"group_colors": ["red", "blue"]}

    def test_backed_expression_fails_without_reading_wide_x(
        self, adata, tmp_path, monkeypatch
    ):
        from anndata import AnnData, read_h5ad

        path = tmp_path / "backed.h5ad"
        adata.write_h5ad(path)
        backed = read_h5ad(path, backed="r")
        try:

            def forbidden(_):
                pytest.fail("Backed X was read")

            monkeypatch.setattr(AnnData, "X", property(forbidden))
            metadata = grouped_expression(
                backed, "score", "group", use_raw=False
            ).values
            assert group_means(metadata).iloc[:, 0].tolist() == [4, 1.5]
            with pytest.raises(TypeError, match="backed/lazy expression"):
                grouped_expression(backed, "g1", "group", use_raw=False)
        finally:
            backed.file.close()

    @pytest.mark.parametrize(
        "options,error,match",
        [
            ({"use_raw": True, "layer": "counts"}, ValueError, "incompatible"),
            ({"layer": "absent"}, ValueError, "layer.*missing"),
            ({"use_raw": "yes"}, TypeError, "use_raw"),
            ({"log": "yes"}, TypeError, "log"),
            ({"num_categories": 0, "groupby": "numeric"}, ValueError, "num_categories"),
            ({"groupby": "absent"}, ValueError, "groupby.*missing"),
            ({"groupby": ["group", "group"]}, ValueError, "distinct"),
            ({"groupby": ["group", "batch"]}, ValueError, "missing multi-key"),
            ({"var_names": []}, ValueError, "var_names"),
            ({"var_names": {"empty": []}}, ValueError, "nonempty"),
            (
                {"var_names": {"one": "g1"}, "var_group_labels": ["x"]},
                TypeError,
                "already defines",
            ),
            ({"var_group_labels": ["x"]}, ValueError, "both bracket"),
            (
                {"var_group_labels": ["x"], "var_group_positions": [(0, 3)]},
                ValueError,
                "inclusive slot",
            ),
        ],
    )
    def test_invalid_grouped_arguments_fail_clearly(self, adata, options, error, match):
        arguments = {"var_names": ["g1", "g2"], "groupby": "group", **options}
        with pytest.raises(error, match=match):
            grouped_expression(adata, **arguments)

    def test_ambiguous_gene_labels_follow_public_scanpy_lookup(self, adata):
        adata.var_names = ["duplicate", "duplicate", "g3"]
        with pytest.raises(ValueError, match="duplicated"):
            grouped_expression(adata, "g3", "group", use_raw=False)
        adata.raw = None
        with pytest.raises(ValueError, match="requires adata.raw"):
            grouped_expression(adata, "g3", "group", use_raw=True)

    def test_ambiguous_symbols_and_metadata_gene_collisions_are_rejected(self, adata):
        adata.var["symbol"] = ["duplicate", "duplicate", "CONST"]
        with pytest.raises(KeyError, match="duplicate entries"):
            grouped_expression(
                adata, "duplicate", "group", use_raw=False, gene_symbols="symbol"
            )
        adata.obs["g1"] = 1
        with pytest.raises(KeyError, match="both"):
            grouped_expression(adata, "g1", "group", use_raw=False)

    def test_index_column_group_ambiguity_is_rejected(self, adata):
        adata.obs.index.name = "group"
        with pytest.raises(ValueError, match="index name and a column"):
            grouped_expression(adata, "g1", "group")

    def test_multi_key_join_collisions_are_rejected(self, adata):
        adata.obs["left"] = pd.Categorical(["a_b", "a", "a_b", "a", "a_b", "a"])
        adata.obs["right"] = pd.Categorical(["c", "b_c", "c", "b_c", "c", "b_c"])
        with pytest.raises(ValueError, match="collide"):
            grouped_expression(adata, "g1", ["left", "right"])

    @pytest.mark.parametrize("cutoff", [np.nan, np.inf, True, "1"])
    def test_invalid_cutoffs_are_rejected(self, adata, cutoff):
        table = grouped_expression(adata, "g1", "group", use_raw=False).values
        with pytest.raises(ValueError, match="expression_cutoff"):
            expression_fractions(table, expression_cutoff=cutoff)
        with pytest.raises(ValueError, match="expression_cutoff"):
            group_means(table, expression_cutoff=cutoff)

    def test_nonfinite_values_and_undefined_logs_fail_clearly(self, adata):
        adata.X[0, 0] = np.inf
        with pytest.raises(ValueError, match="finite or missing"):
            grouped_expression(adata, "g1", "group", use_raw=False)
        adata.X[0, 0] = -1
        with pytest.raises(ValueError, match="greater than -1"):
            grouped_expression(adata, "g1", "group", use_raw=False, log=True)
        table = grouped_expression(adata, "g1", "group", use_raw=False).values
        with pytest.raises(ValueError, match="standard_scale"):
            scale_values(group_means(table), "invalid")

    def test_large_sparse_preparation_has_bounded_selected_column_memory(
        self, monkeypatch
    ):
        import tracemalloc

        from anndata import AnnData

        rng = np.random.default_rng(0)
        n_obs, n_vars = (100000, 20000)
        matrix = sparse.csr_matrix(
            (
                rng.random(n_obs * 4, dtype=np.float32),
                (np.repeat(np.arange(n_obs), 4), rng.integers(n_vars, size=n_obs * 4)),
            ),
            shape=(n_obs, n_vars),
        )
        adata = AnnData(matrix)
        adata.obs["group"] = pd.Categorical(np.arange(n_obs) % 10)
        densified = []
        original = sparse.csr_matrix.toarray

        def selected_only(values, *args, **kwargs):
            assert values.shape == (n_obs, 3), "Unrequested columns would be densified"
            densified.append(values.shape)
            return original(values, *args, **kwargs)

        monkeypatch.setattr(sparse.csr_matrix, "toarray", selected_only)
        tracemalloc.start()
        try:
            table = grouped_expression(
                adata, ["0", "50", "0", "19999"], "group", use_raw=False
            ).values
            means, fractions = (group_means(table), expression_fractions(table))
            _, peak = tracemalloc.get_traced_memory()
        finally:
            tracemalloc.stop()
        assert densified == [(n_obs, 3)]
        assert table.shape == (n_obs, 4)
        assert means.shape == fractions.shape == (10, 4)
        assert all((dtype == np.float32 for dtype in table.dtypes))
        assert peak < 64 * 1024**2

    @pytest.mark.parametrize("name,options", grouped_cases().items())
    def test_grouped_results_match_the_frozen_scanpy_1_11_5_oracle(
        self, adata, name, options
    ):
        if name == "multiple_groups":
            adata = adata[adata.obs["group"].notna()]
        options = options.copy()
        cutoff = options.pop("expression_cutoff", 0.0)
        only_expressed = options.pop("mean_only_expressed", False)
        scale = options.pop("standard_scale", None)
        arguments = {"var_names": ["g1", "g2", "g3"], "groupby": "group", **options}
        result = grouped_expression(adata, **arguments)
        means = scale_values(
            group_means(
                result.values, expression_cutoff=cutoff if only_expressed else None
            ),
            scale,
        )
        fractions = expression_fractions(result.values, expression_cutoff=cutoff)
        expected = GROUPED_DATA_REFERENCE["cases"][name]
        assert [str(value) for value in result.values.index.categories] == expected[
            "categories"
        ]
        assert [asdict(group) for group in result.feature_groups] == expected[
            "feature_groups"
        ]
        for frame, key in [
            (result.values, "table"),
            (means, "means"),
            (fractions, "fractions"),
        ]:
            assert list(frame.columns) == expected[key]["columns"]
            assert [str(value) for value in frame.index] == expected[key]["index"]
            np.testing.assert_allclose(
                frame.to_numpy(dtype=float),
                np.asarray(expected[key]["values"], dtype=float),
                rtol=1e-12,
                atol=1e-12,
                equal_nan=True,
            )


def dotplot_chart(a, **options):
    return gsc.pl.dotplot(
        a,
        options.pop("var_names", ["g1", "g2", "g3"]),
        "group",
        use_raw=False,
        show=False,
        **options,
    )


def dotplot_table(result):
    spec = result.to_dict()
    return pd.DataFrame(spec["datasets"][points(spec)["data"]["name"]])


class TestDotplot:
    """Dotplot contract, displayed statistics, sizing and detached native output."""

    @pytest.fixture
    def adata(self):
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", UserWarning)
            return make_grouped_adata()

    @pytest.mark.parametrize("swapped", [False, True])
    @pytest.mark.parametrize("gap", [0, 2.5, 8])
    def test_group_gap_only_changes_native_slot_spacing(self, adata, swapped, gap):
        options = {
            "var_names": {"First": ["g1", "g2"], "Last": ["g3"]},
            "swap_axes": swapped,
        }
        expected = dotplot_chart(adata, **options).to_dict()
        assert all((expected["scales"][axis]["gapWidth"] == 0 for axis in ("x", "y")))
        for axis in ("x", "y"):
            expected["scales"][axis]["gapWidth"] = gap
        assert dotplot_chart(adata, group_gap=gap, **options).to_dict() == expected

    @pytest.mark.parametrize("gap", [-1, float("nan"), float("inf"), True, "4", None])
    def test_group_gap_rejects_invalid_widths(self, adata, gap):
        with pytest.raises(ValueError, match="group_gap"):
            dotplot_chart(adata, group_gap=gap)

    @pytest.mark.parametrize("case", dotplot_cases())
    def test_displayed_geometry_matches_frozen_scanpy_exports(self, adata, case):
        reference = json.loads(
            Path(__file__).with_name("fixtures").joinpath("dotplot.json").read_text()
        )["cases"][case]
        result = dotplot_chart(adata, **dotplot_cases()[case])
        spec, data = (result.to_dict(), dotplot_table(result))
        assert spec["spec"]["view"] == {
            "stroke": "black",
            "strokeWidth": pytest.approx(1.5 * 100 / 72),
        }
        assert spec["config"]["view"] == {"stroke": "transparent", "strokeWidth": 0}
        unit = points(spec)
        np.testing.assert_allclose(data[["_x", "_y"]] + 0.5, reference["positions"])
        size = unit["encoding"]["size"]["scale"]
        area_map = dict(zip(size["domain"], size["range"], strict=True))
        np.testing.assert_allclose(
            [area_map[p] for p in data["_percent"]],
            np.array(reference["sizes"]) * (100 / 72) ** 2,
        )
        for channel, padding in [("x", 0.3), ("y", 0.5)]:
            encoding = unit["encoding"][channel]
            assert encoding["type"] == "index"
            assert spec["scales"][channel]["domain"] == [
                0,
                int(data[f"_{channel}"].max()),
            ]
            assert spec["scales"][channel]["paddingOuter"] == pytest.approx(padding)
            assert spec["scales"][channel]["zoom"] is False
        assert spec["scales"]["y"]["reverse"] is True
        size_labels = [
            str(round(value)) for value in unit["encoding"]["size"]["legend"]["values"]
        ]
        assert size_labels == reference["size_labels"]

    def test_hand_calculated_means_fractions_and_exact_area_mapping(self, adata):
        result = dotplot_chart(adata)
        data = dotplot_table(result)
        np.testing.assert_allclose(data["_mean"], [1, 1, 4, 0.5, 1.5, 4])
        np.testing.assert_allclose(
            data["_percent"], [100 / 3, 200 / 3, 100, 50, 50, 100]
        )
        unit = points(result.to_dict())
        scale = unit["encoding"]["size"]["scale"]
        for percent, area in zip(scale["domain"], scale["range"], strict=True):
            assert area == pytest.approx((percent / 100) ** 1.5 * 200 * (100 / 72) ** 2)
        assert unit["mark"]["stroke"] == "black"
        assert unit["mark"]["strokeWidth"] == pytest.approx(0.2 * 100 / 72)
        assert unit["mark"]["tooltip"] == {"handler": "default"}

    @pytest.mark.parametrize(
        "installed,expected",
        [
            ("1.11.5", [0, 1 / 6, 1, 0, 0, 1, 0, 1, 0]),
            ("1.12.0", [0, 1 / 3, 1, 0, 1 / 5, 1, 0, 1, 5 / 6]),
            ("1.12.4", [0, 1 / 3, 1, 0, 1 / 5, 1, 0, 1, 5 / 6]),
        ],
    )
    def test_swapped_scaling_preserves_both_scanpy_scaling_passes(
        self, adata, monkeypatch, installed, expected
    ):
        from genome_spy.integrations.scanpy._expression import dotplot_builder

        monkeypatch.setattr(dotplot_builder, "version", lambda _: installed)
        adata.obs["group"] = pd.Categorical(["A", "A", "B", "B", None, "C"])
        adata.X = np.array(
            [[1, 2, 3], [1, 2, 3], [2, 3, 9], [2, 3, 9], [99, 99, 99], [4, 7, 8]],
            dtype=float,
        )
        data = dotplot_table(dotplot_chart(adata, standard_scale="var", swap_axes=True))
        np.testing.assert_allclose(data["_mean"], expected)
        np.testing.assert_allclose(data["_percent"], [100] * 9)

    def test_supplied_colors_align_labels_scale_once_and_do_not_mutate(self, adata):
        supplied = pd.DataFrame(
            [[4, 8, 2], [8, 2, 6]], index=["A", "B"], columns=["g3", "g1", "g2"]
        )
        original = supplied.copy(deep=True)
        np.testing.assert_allclose(
            dotplot_table(dotplot_chart(adata, dot_color_df=supplied))["_mean"],
            [2, 6, 8, 8, 2, 4],
        )
        scaled = dotplot_table(
            dotplot_chart(adata, dot_color_df=supplied, standard_scale="group")
        )
        np.testing.assert_allclose(scaled["_mean"], [0, 2 / 3, 1, 1, 0, 1 / 3])
        pd.testing.assert_frame_equal(supplied, original)

    def test_repeated_feature_slots_keep_distinct_coordinates_and_labels(self, adata):
        result = dotplot_chart(adata, var_names={"first": ["g2", "g1"], "again": "g2"})
        data = dotplot_table(result)
        assert data["_x"].tolist() == [0, 1, 2] * 2
        np.testing.assert_allclose(data["_mean"], [1, 1, 1, 1.5, 0.5, 1.5])
        spec = result.to_dict()
        labels = spec["datasets"][spec["surround"]["bottom"][0]["data"]["name"]]
        assert [v["label"] for v in labels] == ["g2", "g1", "g2"]
        assert spec["surround"]["top"][0]["layer"][0]["mark"]["type"] == "rule"

    @pytest.mark.parametrize("swapped", [False, True])
    def test_hover_preserves_gene_group_and_unclipped_fraction(self, adata, swapped):
        result = dotplot_chart(
            adata,
            var_names=["g2", "g1", "g2"],
            swap_axes=swapped,
            dot_min=0.4,
            dot_max=0.8,
        )
        data = dotplot_table(result)
        assert data["_gene"].tolist() == (
            ["g2", "g2", "g1", "g1", "g2", "g2"] if swapped else ["g2", "g1", "g2"] * 2
        )
        assert data["_group"].tolist() == (
            ["B", "A"] * 3 if swapped else ["B"] * 3 + ["A"] * 3
        )
        np.testing.assert_allclose(
            data["_percent"],
            [200 / 3, 50, 100 / 3, 50, 200 / 3, 50]
            if swapped
            else [200 / 3, 100 / 3, 200 / 3, 50, 50, 50],
        )
        tooltip = points(result.to_dict())["encoding"]["tooltip"]
        assert [item["field"] for item in tooltip] == [
            "_gene",
            "_group",
            "_mean",
            "_percent",
        ]
        assert tooltip[2]["title"] == "Mean expression"

    @pytest.mark.parametrize(
        "supplied,scaled", [(False, True), (True, False), (True, True)]
    )
    def test_hover_names_displayed_color_values(self, adata, supplied, scaled):
        options = {"standard_scale": "var"} if scaled else {}
        if supplied:
            options["dot_color_df"] = pd.DataFrame(
                4.0, index=["B", "A"], columns=["g1", "g2", "g3"]
            )
        tooltip = points(dotplot_chart(adata, **options).to_dict())["encoding"][
            "tooltip"
        ]
        assert tooltip[2]["title"] == (
            "Color value" if supplied else "Mean expression"
        ) + (" (scaled)" if scaled else "")

    def test_hover_can_be_disabled_without_changing_geometry(self, adata):
        enabled = points(dotplot_chart(adata).to_dict())
        disabled = points(dotplot_chart(adata, hover=False).to_dict())
        assert disabled["mark"]["tooltip"] is None
        assert "tooltip" not in disabled["encoding"]
        assert {
            k: v for k, v in enabled["encoding"].items() if k != "tooltip"
        } == disabled["encoding"]

    def test_dot_limits_clip_then_power_and_guides_use_percentages(self, adata):
        spec = dotplot_chart(adata, dot_min=0.4, dot_max=0.8, smallest_dot=10).to_dict()
        size = points(spec)["encoding"]["size"]
        for percent, area in zip(
            size["scale"]["domain"], size["scale"]["range"], strict=True
        ):
            fraction = np.clip(percent / 100, 0.4, 0.8)
            assert area == pytest.approx(
                (10 + ((fraction - 0.4) / 0.4) ** 1.5 * 190) * (100 / 72) ** 2
            )
        np.testing.assert_allclose(size["legend"]["values"], [50, 60, 70, 80])

    def test_no_analysis_or_mutation_and_chart_is_a_snapshot(self, adata, monkeypatch):

        def forbidden(*args, **kwargs):
            pytest.fail("Upstream plotting/analysis ran")

        monkeypatch.setattr(sc.pl, "dotplot", forbidden)
        monkeypatch.setattr(sc.pl, "DotPlot", forbidden)
        for name in ("umap", "pca", "dendrogram", "rank_genes_groups"):
            monkeypatch.setattr(sc.tl, name, forbidden)
        before = adata.copy()
        result = dotplot_chart(adata)
        frozen = result.to_dict()
        pd.testing.assert_frame_equal(adata.obs, before.obs)
        np.testing.assert_allclose(adata.X, before.X)
        assert adata.uns == before.uns
        adata.X[:] = 9
        assert result.to_dict() == frozen

    @pytest.mark.parametrize(
        "options,error,match",
        [
            ({"norm": object()}, NotImplementedError, "norm"),
            ({"vcenter": 0}, NotImplementedError, "vcenter"),
            ({"color_on": "square"}, TypeError, "color_on"),
            ({"dot_size_df": object()}, TypeError, "dot_size_df"),
            ({"cmap": "coolwarm"}, NotImplementedError, "cmap"),
            ({"dot_min": 0.8, "dot_max": 0.2}, ValueError, "dot_min"),
            ({"dot_max": 2}, ValueError, "dot_max"),
            ({"smallest_dot": 201}, ValueError, "smallest_dot"),
            ({"figsize": (5, 4), "width": 200}, TypeError, "figsize"),
            ({"standard_scale": "obs"}, ValueError, "standard_scale"),
            ({"mean_only_expressed": "yes"}, TypeError, "mean_only_expressed"),
        ],
    )
    def test_unsupported_or_invalid_options_are_named(
        self, adata, options, error, match
    ):
        with pytest.raises(error, match=match):
            dotplot_chart(adata, **options)

    def test_empty_groups_zero_fractions_and_constant_colors(self, adata):
        adata.obs["group"] = adata.obs["group"].cat.add_categories(["unused"])
        with pytest.raises(ValueError, match="unused categories"):
            dotplot_chart(adata)
        adata.obs["group"] = adata.obs["group"].cat.remove_unused_categories()
        adata.X[:] = 0
        with pytest.raises(ValueError, match="dot_max=1"):
            dotplot_chart(adata)
        spec = dotplot_chart(adata, dot_max=1).to_dict()
        size = points(spec)["encoding"]["size"]["scale"]
        assert size["range"][size["domain"].index(0)] == 0
        assert points(spec)["encoding"]["color"]["scale"]["domain"] == [-0.1, 0.1]

    def test_nullable_missing_group_statistic_retains_its_slot(self, adata):
        adata.obs["nullable"] = pd.array([None, 1, None, 0, 2, None], dtype="Float64")
        result = dotplot_chart(adata, var_names="nullable")
        data = dotplot_table(result)
        assert data["_x"].tolist() == [0, 0]
        assert data["_y"].tolist() == [0, 1]
        assert pd.isna(data["_mean"].iloc[0]) and pd.isna(data["_percent"].iloc[0])
        assert data["_mean"].iloc[1] == 0.5 and data["_percent"].iloc[1] == 50

    def test_native_dimensions_and_figsize(self, adata):
        for options, expected in [
            ({}, (111, 70)),
            ({"width": 400, "height": 200}, (400, 200)),
            ({"figsize": (6, 3)}, (450, 300)),
        ]:
            spec = dotplot_chart(adata, **options).to_dict()
            assert (spec["spec"]["width"], spec["spec"]["height"]) == expected

    def test_default_raw_lookup_and_selected_sparse_columns(self, adata, monkeypatch):
        from scipy import sparse

        result = gsc.pl.dotplot(adata, ["g1", "g2"], "group", show=False)
        np.testing.assert_allclose(
            dotplot_table(result)["_mean"], [23 / 3, 100 / 3, 7, 30]
        )
        assert dotplot_table(result)["_percent"].tolist() == [100] * 4
        adata.X = sparse.csr_matrix(adata.X)
        original, shapes = (sparse.csr_matrix.toarray, [])

        def selected(matrix, *args, **kwargs):
            shapes.append(matrix.shape)
            return original(matrix, *args, **kwargs)

        monkeypatch.setattr(sparse.csr_matrix, "toarray", selected)
        dotplot_chart(adata, var_names=["g1", "g2", "g1"])
        assert shapes == [(6, 2)]

    @pytest.mark.parametrize("kind", ["missing", "duplicates", "nonnumeric"])
    def test_supplied_color_tables_reject_ambiguous_inputs(self, adata, kind):
        colors = pd.DataFrame(
            [[1, 2, 3], [4, 5, 6]], index=["B", "A"], columns=["g1", "g2", "g3"]
        )
        if kind == "missing":
            colors = colors.drop(columns="g1")
        elif kind == "duplicates":
            colors.index = ["A", "A"]
        else:
            colors = colors.astype(str)
        with pytest.raises((ValueError, TypeError), match="dot_color_df"):
            dotplot_chart(adata, dot_color_df=colors)


def matrixplot_chart(adata, **options):
    return gsc.pl.matrixplot(
        adata,
        options.pop("var_names", ["g1", "g2", "g3"]),
        "group",
        use_raw=False,
        show=False,
        **options,
    )


def matrixplot_table(chart):
    spec = chart.to_dict()
    return pd.DataFrame(spec["datasets"][points(spec)["data"]["name"]])


class TestMatrixplot:
    """Matrixplot statistics, authoritative tables, contract and detached native tiles."""

    @pytest.fixture
    def adata(self):
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", UserWarning)
            return make_grouped_adata()

    @pytest.mark.parametrize("case", matrixplot_cases())
    def test_displayed_table_and_labels_match_frozen_scanpy(self, adata, case):
        reference = json.loads(
            Path(__file__).with_name("fixtures").joinpath("matrixplot.json").read_text()
        )["cases"][case]
        spec = matrixplot_chart(adata, **matrixplot_cases()[case]).to_dict()
        data = pd.DataFrame(spec["datasets"][points(spec)["data"]["name"]])
        np.testing.assert_allclose(
            data["_mean"].to_numpy(dtype=float),
            np.array(reference["values"], dtype=float).ravel(),
            equal_nan=True,
        )
        for side, axis in [("bottom", "x"), ("left", "y")]:
            labels = spec["datasets"][spec["surround"][side][0]["data"]["name"]]
            assert [row["label"] for row in labels] == reference[f"{axis}_labels"]
        np.testing.assert_allclose(
            points(spec)["encoding"]["color"]["scale"]["domain"],
            reference["color_domain"],
        )

    @pytest.mark.parametrize(
        "options,expected",
        [
            ({}, [1, 1, 4, 0.5, 1.5, 4]),
            ({"standard_scale": "var"}, [1, 0, 0, 0, 1, 0]),
            ({"standard_scale": "group"}, [0, 0, 1, 0, 2 / 7, 1]),
            ({"standard_scale": "var", "swap_axes": True}, [1, 0, 0, 1, 0, 0]),
            (
                {"log": True},
                [
                    np.log(3) / 2,
                    np.log(6) / 3,
                    np.log(5),
                    np.log(2) / 2,
                    np.log(4) / 2,
                    np.log(5),
                ],
            ),
        ],
    )
    def test_hand_calculated_means_and_one_scaling_pass(self, adata, options, expected):
        np.testing.assert_allclose(
            matrixplot_table(matrixplot_chart(adata, **options))["_mean"], expected
        )

    def test_supplied_table_preserves_values_and_order_without_aggregation(
        self, adata, monkeypatch
    ):
        supplied = matrixplot_cases()["supplied"]["values_df"]
        original = supplied.copy(deep=True)
        monkeypatch.setattr(
            _grouped_data,
            "group_means",
            lambda *a, **kw: pytest.fail("Supplied table was recomputed"),
        )
        adata.X[:] = -2
        result = matrixplot_chart(
            adata, values_df=supplied, log=True, standard_scale="group"
        )
        data = matrixplot_table(result)
        assert data["_group"].tolist() == ["A"] * 3 + ["B"] * 3
        assert data["_gene"].tolist() == ["g3", "g1", "g2"] * 2
        np.testing.assert_array_equal(data["_mean"], [4, 8, 2, 8, 2, 6])
        reordered = matrixplot_table(
            matrixplot_chart(adata, values_df=supplied, categories_order=["B", "A"])
        )
        np.testing.assert_array_equal(reordered["_mean"], [8, 2, 6, 4, 8, 2])
        frozen = result.to_dict()
        pd.testing.assert_frame_equal(supplied, original)
        supplied.iloc[:, :] = 99
        assert result.to_dict() == frozen

    def test_repeated_supplied_feature_slots_keep_distinct_values(self, adata):
        values = pd.DataFrame(
            [[1, 2, 3], [4, 5, 6]], index=["B", "A"], columns=["g2", "g1", "g2"]
        )
        data = matrixplot_table(
            matrixplot_chart(adata, var_names=["g2", "g1", "g2"], values_df=values)
        )
        assert data["_gene"].tolist() == ["g2", "g1", "g2"] * 2
        assert data["_mean"].tolist() == [1, 2, 3, 4, 5, 6]

    def test_no_plotting_analysis_mutation_or_fraction_computation(
        self, adata, monkeypatch
    ):

        def forbidden(*a, **kw):
            pytest.fail("Unneeded upstream plotting/analysis/statistics ran")

        for name in ("matrixplot", "MatrixPlot"):
            monkeypatch.setattr(sc.pl, name, forbidden)
        for name in ("umap", "pca", "dendrogram", "rank_genes_groups"):
            monkeypatch.setattr(sc.tl, name, forbidden)
        monkeypatch.setattr(_grouped_data, "expression_fractions", forbidden)
        obs, values, uns = (adata.obs.copy(deep=True), adata.X.copy(), adata.uns.copy())
        result = matrixplot_chart(adata)
        frozen = result.to_dict()
        pd.testing.assert_frame_equal(adata.obs, obs)
        np.testing.assert_allclose(adata.X, values)
        assert adata.uns == uns
        adata.X[:] = 99
        assert result.to_dict() == frozen

    @pytest.mark.parametrize(
        "options,error,match",
        [
            ({"norm": object()}, NotImplementedError, "norm"),
            ({"vcenter": 0}, NotImplementedError, "vcenter"),
            ({"shading": "auto"}, TypeError, "shading"),
            ({"edgecolor": "red", "edgecolors": "blue"}, TypeError, "edgecolor"),
            ({"linewidth": 1, "linewidths": 2}, TypeError, "linewidth"),
            ({"standard_scale": "obs"}, ValueError, "standard_scale"),
            ({"log": "yes"}, TypeError, "log"),
            ({"swap_axes": None}, TypeError, "swap_axes"),
        ],
    )
    def test_unsupported_options_fail_before_dependencies(
        self, options, error, match, monkeypatch
    ):
        monkeypatch.setattr(
            pl, "_require_scanpy", lambda *a: pytest.fail("Validation loaded Scanpy")
        )
        with pytest.raises(error, match=match):
            matrixplot_chart(object(), **options)

    @pytest.mark.parametrize(
        "options,error,match",
        [
            ({"cmap": "coolwarm"}, NotImplementedError, "cmap"),
            ({"edgecolor": (1, 0, 0)}, NotImplementedError, "edgecolor"),
            ({"linewidth": -1}, ValueError, "linewidth"),
            ({"figsize": (5, 4), "width": 200}, TypeError, "figsize"),
            ({"vmin": 2, "vmax": 1}, ValueError, "vmin"),
        ],
    )
    def test_invalid_native_style_is_named(self, adata, options, error, match):
        with pytest.raises(error, match=match):
            matrixplot_chart(adata, **options)

    @pytest.mark.parametrize(
        "kind",
        [
            "missing_group",
            "missing_gene",
            "extra_gene",
            "duplicate_group",
            "duplicate_gene",
            "nonnumeric",
            "infinite",
        ],
    )
    def test_supplied_tables_reject_ambiguous_or_invalid_inputs(self, adata, kind):
        values = matrixplot_cases()["supplied"]["values_df"].astype(float)
        if kind == "missing_group":
            values = values.iloc[:1]
        elif kind == "missing_gene":
            values = values.iloc[:, :2]
        elif kind == "extra_gene":
            values["extra"] = 1
        elif kind == "duplicate_group":
            values.index = ["B", "B"]
        elif kind == "duplicate_gene":
            values.columns = ["g1", "g1", "g2"]
        elif kind == "nonnumeric":
            values = values.astype(str)
        else:
            values.iloc[0, 0] = np.inf
        with pytest.raises((ValueError, TypeError), match="values_df"):
            matrixplot_chart(adata, values_df=values)

    def test_raw_default_sparse_selected_columns_and_view(self, adata, monkeypatch):
        from scipy import sparse

        raw = gsc.pl.matrixplot(adata, ["g1", "g2"], "group", show=False)
        np.testing.assert_allclose(
            matrixplot_table(raw)["_mean"], [23 / 3, 100 / 3, 7, 30]
        )
        adata.X = sparse.csr_matrix(adata.X)
        original, shapes = (sparse.csr_matrix.toarray, [])

        def selected(matrix, *a, **kw):
            shapes.append(matrix.shape)
            return original(matrix, *a, **kw)

        monkeypatch.setattr(sparse.csr_matrix, "toarray", selected)
        np.testing.assert_allclose(
            matrixplot_table(
                matrixplot_chart(adata[:, :], var_names=["g1", "g2", "g1"])
            )["_mean"],
            [1, 1, 1, 0.5, 1.5, 0.5],
        )
        assert shapes == [(6, 2)]

    def test_missing_cells_constant_color_and_unused_categories(self, adata):
        values = pd.DataFrame(
            [[4, np.nan, 4], [4, 4, 4]], index=["B", "A"], columns=["g1", "g2", "g3"]
        )
        spec = matrixplot_chart(adata, values_df=values).to_dict()
        assert pd.isna(
            matrixplot_table(matrixplot_chart(adata, values_df=values))["_mean"].iloc[1]
        )
        assert points(spec)["encoding"]["color"]["scale"]["domain"] == [3.6, 4.4]
        assert "_paint" not in matrixplot_table(
            matrixplot_chart(adata, values_df=values)
        )
        adata.obs["group"] = adata.obs["group"].cat.add_categories(["unused"])
        with pytest.raises(ValueError, match="unused categories"):
            matrixplot_chart(adata)

    def test_dimensions_edges_and_hover(self, adata):
        for options, expected in [
            ({}, (111, 70)),
            ({"swap_axes": True}, (70, 111)),
            ({"width": 400, "height": 200}, (400, 200)),
            ({"figsize": (6, 3)}, (450, 300)),
        ]:
            spec = matrixplot_chart(adata, **options).to_dict()
            assert (spec["spec"]["width"], spec["spec"]["height"]) == expected
        spec = matrixplot_chart(
            adata, edgecolor="none", linewidth=2, hover=False
        ).to_dict()
        tiles = points(spec)
        assert tiles["mark"]["strokeOpacity"] == 0
        assert tiles["mark"]["strokeWidth"] == pytest.approx(2 * 100 / 72)
        assert tiles["mark"]["tooltip"] is None and "tooltip" not in tiles["encoding"]
