"""PCA variance ratios use stored scores and the shared rank-label renderer."""

import inspect

import anndata as ad
import numpy as np
import pytest
from scipy import sparse

import genome_spy.integrations.scanpy as gsc
from tests.integrations.scanpy.helpers import scanpy_rank_labels
from tests.integrations.scanpy.ranked_fixture import make_ranked_adata

sc = pytest.importorskip("scanpy")


def rows(spec):
    """Return the single variance panel's serialized scores and PC labels."""
    return spec["datasets"][spec["data"]["name"]]


def test_signature_preserves_scanpy_defaults_and_only_adds_keyword_controls():
    upstream = inspect.signature(sc.pl.pca_variance_ratio).parameters
    native = inspect.signature(gsc.pl.pca_variance_ratio).parameters
    for name, p in upstream.items():
        assert native[name].kind == p.kind and native[name].default == p.default
    assert set(native) - set(upstream) == {"hover", "width", "height"}
    assert all(
        native[k].kind is inspect.Parameter.KEYWORD_ONLY
        for k in set(native) - set(upstream)
    )


@pytest.mark.parametrize("log", [False, True])
@pytest.mark.parametrize("storage", [np.array, list, tuple])
def test_variance_is_the_existing_ranking_chart_without_analysis_or_expression(
    monkeypatch, log, storage
):
    a = make_ranked_adata()
    source = storage([0.2, 0.4, 0.1, 0.2, 0.05])
    a.uns["pca"]["variance_ratio"] = source
    for module, name in [
        (sc.pp, "pca"),
        (sc.tl, "pca"),
        (sc.pl, "ranking"),
        (sc.pl, "pca_variance_ratio"),
    ]:
        monkeypatch.setattr(
            module, name, lambda *a, **k: pytest.fail("Ran upstream analysis/plotting")
        )
    monkeypatch.setattr(
        ad.AnnData, "X", property(lambda _: pytest.fail("Read expression"))
    )
    options = {"log": log, "hover": False, "width": 240, "height": 210, "show": False}
    actual = gsc.pl.pca_variance_ratio(a, 2, **options)
    expected = gsc.pl.ranking(
        a, "uns", "variance_ratio", dictionary="pca", labels="PC", n_points=2, **options
    )
    reference = expected.to_dict()
    low, high = reference["encoding"]["y"]["scale"]["domain"]
    reference["encoding"]["y"]["scale"]["domain"] = [low, high + 0.3 * (high - low)]
    reference["padding"] = {"top": 0}
    assert actual.to_dict() == reference
    assert a.uns["pca"]["variance_ratio"] is source
    np.testing.assert_array_equal(source, [0.2, 0.4, 0.1, 0.2, 0.05])


@pytest.mark.reference
def test_tied_ratios_keep_original_pc_names_and_top_onlys_extra_label():
    spec = gsc.pl.pca_variance_ratio(make_ranked_adata(), 2, show=False).to_dict()
    actual = [(r["_rank"], r["_label"], r["_score"]) for r in rows(spec)]
    assert actual == scanpy_rank_labels("pca_variance_ratio", make_ranked_adata(), 2)[0]
    assert [(rank, score) for rank, _, score in actual] == [
        (0, 0.4),
        (1, 0.2),
        (2, 0.2),
    ]
    assert spec["title"] == "variance ratio"
    assert spec["encoding"]["x"]["scale"]["domain"] == [-0.9, 2.9]
    assert spec["encoding"]["x"]["axis"]["title"] == "ranking"
    np.testing.assert_allclose(spec["encoding"]["y"]["scale"]["domain"], [0.19, 0.489])


def test_log_is_a_natural_log_score_transform_before_ranking():
    a = make_ranked_adata()
    a.uns["pca"]["variance_ratio"] = np.exp([-3.0, -1.0, -2.0, -4.0])
    spec = gsc.pl.pca_variance_ratio(a, 1, log=True, show=False).to_dict()
    assert [r["_label"] for r in rows(spec)] == ["PC2", "PC3"]
    np.testing.assert_allclose([r["_score"] for r in rows(spec)], [-1, -2])
    np.testing.assert_allclose(spec["encoding"]["y"]["scale"]["domain"], [-2.1, -0.605])
    assert spec["encoding"]["y"]["scale"].get("type", "linear") == "linear"


def test_rank_limits_preserve_default_extra_label_and_empty_space_for_short_results():
    a = make_ranked_adata()
    a.uns["pca"]["variance_ratio"] = np.linspace(0.9, 0.01, 50)
    default = gsc.pl.pca_variance_ratio(a, show=False).to_dict()
    assert len(rows(default)) == 31
    assert rows(default)[-1]["_label"] == "PC31"
    short = gsc.pl.pca_variance_ratio(a, 80, show=False).to_dict()
    assert len(rows(short)) == 50
    assert short["encoding"]["x"]["scale"]["domain"] == [-0.9, 80.9]


def test_float32_log_scores_retain_scanpys_input_precision():
    a = make_ranked_adata()
    source = np.array([0.1, 0.4, 0.2], dtype=np.float32)
    a.uns["pca"]["variance_ratio"] = source
    spec = gsc.pl.pca_variance_ratio(a, log=True, show=False).to_dict()
    np.testing.assert_array_equal(
        [r["_score"] for r in rows(spec)], np.log(source)[[1, 2, 0]]
    )


def test_linear_scores_are_never_renormalized_and_zero_is_allowed():
    a = make_ranked_adata()
    a.uns["pca"]["variance_ratio"] = np.array([-0.2, 0, 2.0])
    spec = gsc.pl.pca_variance_ratio(a, show=False).to_dict()
    assert [r["_score"] for r in rows(spec)] == [2, 0, -0.2]
    a.uns["pca"]["variance_ratio"] = [0.0]
    single = gsc.pl.pca_variance_ratio(a, show=False).to_dict()
    assert len(rows(single)) == 1 and rows(single)[0]["_label"] == "PC1"
    assert single["encoding"]["y"]["scale"]["domain"] == [-0.05, 0.05]


@pytest.mark.parametrize("count", [0, -1, True, 1.5, None])
def test_invalid_rank_counts_name_n_pcs(count):
    with pytest.raises(ValueError, match="gsc.pl.pca_variance_ratio: n_pcs"):
        gsc.pl.pca_variance_ratio(make_ranked_adata(), count, show=False)


@pytest.mark.parametrize("pca", [None, {}, {"variance": np.array([1.0])}])
def test_missing_results_require_explicit_scanpy_pca(pca):
    a = make_ranked_adata()
    a.uns["pca"] = pca
    with pytest.raises(
        ValueError, match=r"gsc.pl.pca_variance_ratio: missing.*sc.pp.pca explicitly"
    ):
        gsc.pl.pca_variance_ratio(a, show=False)


@pytest.mark.parametrize(
    "values,log,error,message",
    [
        ([], False, ValueError, "nonempty"),
        (np.array([[0.2, 0.4]]), False, TypeError, "one-dimensional"),
        ("0.2", False, TypeError, "one-dimensional"),
        ([[0.2], [0.4, 0.1]], False, TypeError, "real numbers"),
        ([float("nan")], False, ValueError, "finite"),
        ([float("inf")], False, ValueError, "finite"),
        ([1j], False, TypeError, "real numbers"),
        ([0.4, 0], True, ValueError, "positive"),
        ([0.4, -0.1], True, ValueError, "positive"),
    ],
)
def test_invalid_stored_vectors_fail_with_context(values, log, error, message):
    a = make_ranked_adata()
    a.uns["pca"]["variance_ratio"] = values
    with pytest.raises(error, match=f"gsc.pl.pca_variance_ratio:.*{message}"):
        gsc.pl.pca_variance_ratio(a, log=log, show=False)


def test_lazy_vectors_reject_without_materialization():
    class Lazy:
        def __array__(self, *args):
            pytest.fail("Materialized lazy ratios")

    a = make_ranked_adata()
    a.uns["pca"]["variance_ratio"] = Lazy()
    with pytest.raises(TypeError, match="gsc.pl.pca_variance_ratio:.*resident"):
        gsc.pl.pca_variance_ratio(a, show=False)


def test_backed_data_and_views_read_the_stored_snapshot_without_reconstruction(
    tmp_path,
):
    a = ad.AnnData(sparse.csr_matrix((10, 100)))
    a.uns["pca"] = {"variance_ratio": np.array([0.2, 0.4, 0.1])}
    path = tmp_path / "variance.h5ad"
    a.write_h5ad(path)
    backed = ad.read_h5ad(path, backed="r")
    try:
        for data in (backed, backed[:2, :3]):
            spec = gsc.pl.pca_variance_ratio(data, 1, show=False).to_dict()
            assert [r["_label"] for r in rows(spec)] == ["PC2", "PC1"]
            np.testing.assert_array_equal(
                data.uns["pca"]["variance_ratio"], [0.2, 0.4, 0.1]
            )
    finally:
        backed.file.close()
