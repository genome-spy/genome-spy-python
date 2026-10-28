"""Public Scanpy normalization, box statistics and native highest-expression contract."""

from copy import deepcopy
import inspect
import subprocess
import sys

import anndata as ad
import numpy as np
import pytest
from scipy import sparse

import genome_spy.integrations.scanpy as gsc
from genome_spy.integrations.scanpy._qc.highest_expr_data import (
    prepare_highest_expression,
)
from tests.integrations.scanpy.helpers import leaf_marks
from tests.integrations.scanpy.highest_expr_fixture import make_counts

sc = pytest.importorskip("scanpy")


def test_data_module_defers_the_optional_scanpy_import():
    subprocess.run(
        [
            sys.executable,
            "-c",
            "import sys; import genome_spy.integrations.scanpy._qc.highest_expr_data; assert 'scanpy' not in sys.modules",
        ],
        check=True,
    )


def test_signature_retains_scanpy_defaults_and_native_keyword_only_controls():
    actual = inspect.signature(gsc.pl.highest_expr_genes).parameters
    expected = inspect.signature(sc.pl.highest_expr_genes).parameters
    for name, parameter in expected.items():
        if name == "ax":
            assert name not in actual
        else:
            assert actual[name].kind == parameter.kind
            assert actual[name].default == parameter.default
    assert set(actual) - set(expected) == {"hover", "zoom", "width", "height"}
    assert all(
        actual[n].kind == inspect.Parameter.KEYWORD_ONLY
        for n in set(actual) - set(expected)
    )


@pytest.mark.parametrize("storage", ["dense", "csr", "csc"])
@pytest.mark.parametrize("log,symbols", [(False, None), (True, "symbol")])
def test_normalization_ranks_quartiles_whiskers_fliers_and_limits_match_scanpy(
    storage, log, symbols
):
    import matplotlib.pyplot as plt

    a = make_counts(storage)
    before = a.copy()
    reference = a.copy()
    with pytest.warns(UserWarning, match="zero counts"):
        ax = sc.pl.highest_expr_genes(
            reference, n_top=5, gene_symbols=symbols, log=log, show=False
        )
    with pytest.warns(UserWarning, match="zero counts"):
        boxes, fliers, limits = prepare_highest_expression(a, 5, None, symbols)
    assert boxes.gene.tolist() == [t.get_text() for t in ax.get_yticklabels()]
    for i, row in boxes.iterrows():
        vertices = ax.patches[i].get_path().vertices
        np.testing.assert_allclose(
            [row.q1, row.q3], [vertices[:, 0].min(), vertices[:, 0].max()]
        )
        lines = ax.lines[i * 6 : (i + 1) * 6]
        np.testing.assert_allclose(
            [row.lower, row.upper, row["median"]],
            [lines[j].get_xdata()[0] for j in (2, 3, 4)],
        )
        np.testing.assert_allclose(
            sorted(fliers.loc[fliers.gene == row.gene, "percent"]),
            sorted(lines[5].get_xdata()),
        )
    with pytest.warns(UserWarning, match="zero counts"):
        spec = gsc.pl.highest_expr_genes(
            a, n_top=5, gene_symbols=symbols, log=log, show=False
        ).to_dict()
    np.testing.assert_allclose(
        spec["layer"][0]["encoding"]["x"]["scale"]["domain"], ax.get_xlim()
    )
    assert spec["width"] == ax.get_window_extent().width
    plt.close(ax.figure)
    np.testing.assert_array_equal(
        a.X.toarray() if sparse.issparse(a.X) else a.X,
        before.X.toarray() if sparse.issparse(before.X) else before.X,
    )
    assert a.obs.equals(before.obs) and a.var.equals(before.var) and a.uns == before.uns


def test_one_public_normalization_uses_layer_ignores_raw_and_preserves_views(
    monkeypatch,
):
    a = make_counts("csr")
    a.layers["counts"] = a.X.copy()
    a.raw = ad.AnnData(sparse.csr_matrix(np.ones(a.shape)))
    a.X = sparse.csr_matrix(np.zeros(a.shape))
    view = a[1:, :]
    normalize, calls = sc.pp.normalize_total, []

    def observed(data, **options):
        calls.append(options)
        assert (
            data.X is view.layers["counts"]
            or (data.X != view.layers["counts"]).nnz == 0
        )
        return normalize(data, **options)

    monkeypatch.setattr(sc.pp, "normalize_total", observed)
    chart = gsc.pl.highest_expr_genes(view, n_top=2, layer="counts", show=False)
    assert view.is_view and calls == [{"target_sum": 100, "inplace": False}]
    rows = next(iter(chart.to_dict()["datasets"].values()))
    assert [r["gene"] for r in rows] == ["gene-4", "gene-2"]
    assert a.X.nnz == 0 and not a.uns


def test_sparse_access_only_densifies_one_selected_column(monkeypatch):
    a = make_counts("csr")
    dense, shapes = sparse.csr_matrix.toarray, []

    def observed(matrix, *args, **kwargs):
        shapes.append(matrix.shape)
        assert matrix.shape == (21, 1)
        return dense(matrix, *args, **kwargs)

    monkeypatch.setattr(sparse.csr_matrix, "toarray", observed)
    with pytest.warns(UserWarning, match="zero counts"):
        gsc.pl.highest_expr_genes(a, n_top=2, show=False)
    assert shapes == [(21, 1), (21, 1)]


@pytest.mark.parametrize("dtype", [np.int32, np.float32, np.float64])
def test_percentages_use_all_genes_and_include_zero_cells(dtype):
    a = ad.AnnData(np.array([[0, 0, 0], [1, 1, 8], [2, 2, 6]], dtype=dtype))
    with pytest.warns(UserWarning, match="zero counts"):
        boxes, _, _ = prepare_highest_expression(a, 1, None, None)
    assert boxes.gene.tolist() == ["2"]
    np.testing.assert_allclose(boxes["mean"], [140 / 3], rtol=1e-6)
    np.testing.assert_allclose(boxes["median"], [60])


@pytest.mark.parametrize(
    "options,error",
    [
        ({"ax": None}, TypeError),
        ({"return_fig": False}, TypeError),
        ({"color": "red"}, TypeError),
        ({"whis": 2}, TypeError),
        ({"n_top": 0}, ValueError),
        ({"n_top": True}, ValueError),
        ({"n_top": 1.5}, ValueError),
        ({"layer": 1}, TypeError),
        ({"gene_symbols": []}, TypeError),
        ({"log": 1}, TypeError),
        ({"hover": "yes"}, TypeError),
        ({"zoom": "xy"}, TypeError),
        ({"width": 0}, ValueError),
    ],
)
def test_invalid_options_fail_before_optional_imports(monkeypatch, options, error):
    monkeypatch.setattr(
        gsc.pl, "_require_scanpy", lambda *a: pytest.fail("Loaded Scanpy")
    )
    with pytest.raises(error, match="gsc.pl.highest_expr_genes"):
        gsc.pl.highest_expr_genes(object(), **options)


@pytest.mark.parametrize("bad", [-1, np.nan, np.inf, 1j])
def test_invalid_counts_fail_clearly(bad):
    a = ad.AnnData(np.array([[1, bad]]))
    with pytest.raises(ValueError, match="finite nonnegative"):
        gsc.pl.highest_expr_genes(a, show=False)


def test_labels_sources_empty_and_backed_are_explicit(tmp_path):
    a = make_counts()
    for options, error, match in [
        ({"layer": "missing"}, ValueError, "layer"),
        ({"gene_symbols": "missing"}, ValueError, "gene_symbols"),
    ]:
        with pytest.raises(error, match=match):
            gsc.pl.highest_expr_genes(a, show=False, **options)
    a.var["symbol"] = ["same"] * 5
    with (
        pytest.warns(UserWarning, match="zero counts"),
        pytest.raises(NotImplementedError, match="unique"),
    ):
        gsc.pl.highest_expr_genes(a, gene_symbols="symbol", show=False)
    a.var["symbol"] = [None] * 5
    with (
        pytest.warns(UserWarning, match="zero counts"),
        pytest.raises(NotImplementedError, match="nonmissing"),
    ):
        gsc.pl.highest_expr_genes(a, gene_symbols="symbol", show=False)
    with pytest.raises(ValueError, match="at least one"):
        gsc.pl.highest_expr_genes(a[:0], show=False)
    path = tmp_path / "counts.h5ad"
    make_counts().write_h5ad(path)
    backed = ad.read_h5ad(path, backed="r")
    try:
        with pytest.raises(TypeError, match="backed/lazy"):
            gsc.pl.highest_expr_genes(backed, show=False)
    finally:
        backed.file.close()


def test_all_zero_single_gene_large_n_top_and_snapshot():
    a = ad.AnnData(np.zeros((3, 1)))
    with pytest.warns(UserWarning, match="zero counts"):
        chart = gsc.pl.highest_expr_genes(a, show=False)
    spec = chart.to_dict()
    assert (
        len(spec["datasets"]) == 1 and len(next(iter(spec["datasets"].values()))) == 1
    )
    assert all(
        m["mark"]["tooltip"] is None
        for m in leaf_marks(
            gsc.pl.highest_expr_genes(a, hover=False, show=False).to_dict()
        )
    )
    snapshot = deepcopy(spec)
    a.X[:] = 10
    assert chart.to_dict() == snapshot
    a.X[:] = 0
    with (
        pytest.warns(UserWarning, match="zero counts"),
        pytest.raises(ValueError, match="positive percentages"),
    ):
        gsc.pl.highest_expr_genes(a, log=True, show=False)


@pytest.mark.parametrize("counts", [[[1], [2], [3]], [[1, 1], [2, 2]]])
@pytest.mark.parametrize("log", [False, True])
def test_constant_percentage_domains_match_public_scanpy(counts, log):
    import matplotlib.pyplot as plt

    a = ad.AnnData(np.array(counts, dtype=float))
    ax = sc.pl.highest_expr_genes(a, log=log, show=False)
    spec = gsc.pl.highest_expr_genes(a, log=log, show=False).to_dict()
    np.testing.assert_allclose(
        spec["layer"][0]["encoding"]["x"]["scale"]["domain"], ax.get_xlim()
    )
    plt.close(ax.figure)


def test_duplicate_cell_labels_keep_separate_outlier_ids():
    a = make_counts()
    a.obs_names = ["cell"] * a.n_obs
    with pytest.warns(UserWarning, match="zero counts"):
        _, fliers, _ = prepare_highest_expression(a, 5, None, None)
    assert fliers["cell"].unique().tolist() == ["cell"]
    assert set(fliers.cell_id) == {"row-0", "row-20"}
