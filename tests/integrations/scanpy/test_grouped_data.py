"""Independent grouped-data semantics plus explicitly frozen upstream results."""

from dataclasses import asdict
from hashlib import sha256
import json
from pathlib import Path

import numpy as np
import pandas as pd
import pytest
from scipy import sparse

from genome_spy.integrations.scanpy._expression.grouped_data import (
    expression_fractions,
    grouped_expression,
    group_means,
    scale_values,
)
from tests.integrations.scanpy.grouped_fixture import grouped_cases, make_grouped_adata

sc = pytest.importorskip("scanpy")
FIXTURE = Path(__file__).with_name("fixtures") / "grouped.json"
REFERENCE = json.loads(FIXTURE.read_text())


@pytest.fixture
def adata():
    with pytest.warns(UserWarning, match="Observation names are not unique"):
        a = make_grouped_adata()
    a.obs.index.name = "barcode"
    return a


def test_grouped_fixture_matches_its_frozen_provenance():
    source = Path(__file__).with_name("grouped_fixture.py")
    assert sha256(source.read_bytes()).hexdigest() == REFERENCE["fixture_sha256"]
    assert REFERENCE["versions"]["scanpy"] == "1.11.5"
    assert set(REFERENCE["cases"]) == set(grouped_cases())


def test_means_fractions_and_scaling_have_independent_denominators(adata):
    table = grouped_expression(adata, ["g1", "g2", "g3"], "group", use_raw=False).values
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
        expression_fractions(table, expression_cutoff=-0.5), [[2 / 3, 1, 1], [1, 1, 1]]
    )
    np.testing.assert_allclose(scale_values(means, "var"), [[1, 0, 0], [0, 1, 0]])
    np.testing.assert_allclose(scale_values(means, "group"), [[0, 0, 1], [0, 2 / 7, 1]])
    np.testing.assert_allclose(means, [[1, 1, 4], [0.5, 1.5, 4]])


def test_log_is_applied_to_observations_before_means_and_cutoffs(adata):
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
def test_selected_source_and_raw_symbols(adata, options, names, expected):
    table = grouped_expression(adata, names, "group", **options).values
    np.testing.assert_allclose(table.iloc[:, 0], expected, equal_nan=True)


def test_repeated_slots_and_brackets_do_not_multiply_columns(adata):
    result = grouped_expression(
        adata, {"first": ["g2", "g1"], "again": "g2"}, "group", use_raw=False
    )
    assert list(result.values.columns) == ["g2", "g1", "g2"]
    assert [asdict(group) for group in result.feature_groups] == [
        {"label": "first", "start": 0, "end": 1},
        {"label": "again", "start": 2, "end": 2},
    ]
    np.testing.assert_allclose(group_means(result.values), [[1, 1, 1], [1.5, 0.5, 1.5]])
    assert result.values.shape == (6, 3)


def test_explicit_brackets_use_inclusive_slot_positions(adata):
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


def test_numeric_bin_edges_and_source_row_order_are_preserved(adata):
    table = grouped_expression(
        adata, "g1", "numeric", use_raw=False, num_categories=3
    ).values
    assert table.index.codes.tolist() == [0, 0, 1, 1, 2, 2]
    assert table.index.categories[0].left == -0.005
    assert [interval.right for interval in table.index.categories] == [1.667, 3.333, 5]
    np.testing.assert_allclose(
        table.iloc[:, 0], [0, 1, 2, 0, 9, np.nan], equal_nan=True
    )


def test_string_sanitization_matches_anndata_without_mutating_annotations(adata):
    before = adata.obs.copy(deep=True)
    table = grouped_expression(adata, "g1", "plain", use_raw=False).values
    assert table.index.categories.tolist() == ["2", "10"]
    pd.testing.assert_frame_equal(adata.obs, before)
    adata.obs["plain"] = ["10", "2", "30", "4", "50", "6"]
    unique = grouped_expression(adata, "g1", "plain", use_raw=False).values
    assert unique.index.categories.tolist() == ["10", "2", "30", "4", "50", "6"]


def test_multi_key_groups_follow_category_product_order(adata):
    a = adata[adata.obs["group"].notna()]
    table = grouped_expression(a, "g1", ["group", "batch"], use_raw=False).values
    assert table.index.categories.tolist() == ["B_y", "B_x", "A_y", "A_x"]
    assert table.index.tolist() == ["B_x", "A_x", "B_y", "A_y", "B_x"]
    assert a.is_view


def test_named_index_grouping_preserves_duplicate_observations(adata):
    table = grouped_expression(adata, "g2", "barcode", use_raw=False).values
    assert table.index.tolist() == adata.obs_names.tolist()
    assert table.index.name == "barcode"
    assert len(table) == 6
    assert group_means(table).loc["same", "g2"] == 0.5


def test_supplied_category_order_is_validated_and_applied(adata):
    result = grouped_expression(
        adata, "g2", "group", use_raw=False, categories_order=["A", "B"]
    )
    assert result.values.index.categories.tolist() == ["A", "B"]
    assert list(group_means(result.values).index) == ["A", "B"]
    for invalid in (["A"], ["A", "A"], ["A", "B", "C"]):
        with pytest.raises(ValueError, match="categories"):
            grouped_expression(adata, "g2", "group", categories_order=invalid)


def test_unused_categories_remain_metadata_without_invented_observations(adata):
    adata.obs["group"] = adata.obs["group"].cat.add_categories(["unused"])
    table = grouped_expression(adata, "g2", "group", use_raw=False).values
    assert table.index.categories.tolist() == ["B", "A", "unused"]
    assert group_means(table).index.tolist() == ["B", "A"]
    assert expression_fractions(table).index.tolist() == ["B", "A"]


def test_all_missing_groups_do_not_invent_statistics(adata):
    adata.obs["group"] = pd.Categorical([None] * 6, categories=["B", "A"])
    table = grouped_expression(adata, "g2", "group", use_raw=False).values
    assert table.index.categories.tolist() == ["B", "A"]
    assert group_means(table).shape == expression_fractions(table).shape == (0, 1)


def test_nullable_metadata_preserves_its_comparison_denominator(adata):
    adata.obs["nullable"] = pd.array([0, 1, 2, 0, 9, None], dtype="Float64")
    table = grouped_expression(adata, "nullable", "group", use_raw=False).values
    assert expression_fractions(table).iloc[:, 0].tolist() == [0.5, 0.5]
    assert group_means(table).iloc[:, 0].tolist() == [1, 0.5]


@pytest.mark.parametrize("format", ["csr_matrix", "csc_matrix"])
def test_sparse_access_only_densifies_requested_unique_columns(
    adata, monkeypatch, format
):
    adata.X = getattr(sparse, format)(adata.X)
    dense_shapes = []
    cls = type(adata.X)
    original = cls.toarray

    def track(matrix, *args, **kwargs):
        dense_shapes.append(matrix.shape)
        return original(matrix, *args, **kwargs)

    monkeypatch.setattr(cls, "toarray", track)
    table = grouped_expression(adata, ["g2", "g1", "g2"], "group", use_raw=False).values
    assert dense_shapes == [(6, 2)]
    assert list(table.columns) == ["g2", "g1", "g2"]
    np.testing.assert_allclose(group_means(table), [[1, 1, 1], [1.5, 0.5, 1.5]])


@pytest.mark.parametrize("format", ["csr_array", "csc_array"])
def test_sparse_array_limit_is_explicit_before_the_upstream_getter(
    adata, monkeypatch, format
):
    adata.X = getattr(sparse, format)(adata.X)
    monkeypatch.setattr(
        sc.get, "obs_df", lambda *args, **kwargs: pytest.fail("Getter ran")
    )
    with pytest.raises(NotImplementedError, match="does not support sparse arrays"):
        grouped_expression(adata, "g1", "group", use_raw=False)


def test_view_reads_are_snapshots_without_analysis_or_cache_writes(adata, monkeypatch):
    before_obs, before_var = adata.obs.copy(deep=True), adata.var.copy(deep=True)
    adata.uns["group_colors"] = ["red", "blue"]
    for name in ("pca", "umap", "dendrogram", "rank_genes_groups"):
        monkeypatch.setattr(sc.tl, name, lambda *a, **k: pytest.fail("Analysis ran"))
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
    np.testing.assert_allclose(result.values.iloc[:, 0], [0, 0, np.nan], equal_nan=True)
    adata.X[0, 0] = 100
    assert result.values.iloc[1, 0] == 0
    pd.testing.assert_frame_equal(adata.obs, before_obs)
    pd.testing.assert_frame_equal(adata.var, before_var)
    assert adata.uns == {"group_colors": ["red", "blue"]}


def test_backed_expression_fails_without_reading_wide_x(adata, tmp_path, monkeypatch):
    from anndata import read_h5ad, AnnData

    path = tmp_path / "backed.h5ad"
    adata.write_h5ad(path)
    backed = read_h5ad(path, backed="r")
    try:

        def forbidden(_):
            pytest.fail("Backed X was read")

        monkeypatch.setattr(AnnData, "X", property(forbidden))
        metadata = grouped_expression(backed, "score", "group", use_raw=False).values
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
def test_invalid_grouped_arguments_fail_clearly(adata, options, error, match):
    arguments = {"var_names": ["g1", "g2"], "groupby": "group", **options}
    with pytest.raises(error, match=match):
        grouped_expression(adata, **arguments)


def test_ambiguous_gene_labels_follow_public_scanpy_lookup(adata):
    adata.var_names = ["duplicate", "duplicate", "g3"]
    with pytest.raises(ValueError, match="duplicated"):
        grouped_expression(adata, "g3", "group", use_raw=False)
    adata.raw = None
    with pytest.raises(ValueError, match="requires adata.raw"):
        grouped_expression(adata, "g3", "group", use_raw=True)


def test_ambiguous_symbols_and_metadata_gene_collisions_are_rejected(adata):
    adata.var["symbol"] = ["duplicate", "duplicate", "CONST"]
    with pytest.raises(KeyError, match="duplicate entries"):
        grouped_expression(
            adata, "duplicate", "group", use_raw=False, gene_symbols="symbol"
        )
    adata.obs["g1"] = 1
    with pytest.raises(KeyError, match="both"):
        grouped_expression(adata, "g1", "group", use_raw=False)


def test_index_column_group_ambiguity_is_rejected(adata):
    adata.obs.index.name = "group"
    with pytest.raises(ValueError, match="index name and a column"):
        grouped_expression(adata, "g1", "group")


def test_multi_key_join_collisions_are_rejected(adata):
    adata.obs["left"] = pd.Categorical(["a_b", "a", "a_b", "a", "a_b", "a"])
    adata.obs["right"] = pd.Categorical(["c", "b_c", "c", "b_c", "c", "b_c"])
    with pytest.raises(ValueError, match="collide"):
        grouped_expression(adata, "g1", ["left", "right"])


@pytest.mark.parametrize("cutoff", [np.nan, np.inf, True, "1"])
def test_invalid_cutoffs_are_rejected(adata, cutoff):
    table = grouped_expression(adata, "g1", "group", use_raw=False).values
    with pytest.raises(ValueError, match="expression_cutoff"):
        expression_fractions(table, expression_cutoff=cutoff)
    with pytest.raises(ValueError, match="expression_cutoff"):
        group_means(table, expression_cutoff=cutoff)


def test_nonfinite_values_and_undefined_logs_fail_clearly(adata):
    adata.X[0, 0] = np.inf
    with pytest.raises(ValueError, match="finite or missing"):
        grouped_expression(adata, "g1", "group", use_raw=False)
    adata.X[0, 0] = -1
    with pytest.raises(ValueError, match="greater than -1"):
        grouped_expression(adata, "g1", "group", use_raw=False, log=True)
    table = grouped_expression(adata, "g1", "group", use_raw=False).values
    with pytest.raises(ValueError, match="standard_scale"):
        scale_values(group_means(table), "invalid")


def test_large_sparse_preparation_has_bounded_selected_column_memory(monkeypatch):
    from anndata import AnnData
    import tracemalloc

    rng = np.random.default_rng(0)
    n_obs, n_vars = 100_000, 20_000
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
        means, fractions = group_means(table), expression_fractions(table)
        _, peak = tracemalloc.get_traced_memory()
    finally:
        tracemalloc.stop()
    assert densified == [(n_obs, 3)]
    assert table.shape == (n_obs, 4)
    assert means.shape == fractions.shape == (10, 4)
    assert all(dtype == np.float32 for dtype in table.dtypes)
    assert peak < 64 * 1024**2


@pytest.mark.parametrize("name,options", grouped_cases().items())
def test_grouped_results_match_the_frozen_scanpy_1_11_5_oracle(adata, name, options):
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
    expected = REFERENCE["cases"][name]
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
