"""Stored DPT expression ordering against public Scanpy, without analysis or mutation."""

import warnings

import numpy as np
import pandas as pd
import pytest
from scipy import sparse

import genome_spy.integrations.scanpy as gsc
from tests.integrations.scanpy.profile_fixtures import (
    dpt_profile_cases,
    make_dpt_profiles,
)
from tests.integrations.scanpy.helpers import leaf_marks

pytest.importorskip("scanpy")


@pytest.mark.reference
@pytest.mark.parametrize("case", dpt_profile_cases())
def test_profiles_order_limits_labels_and_boundaries_match_public_scanpy(
    case, monkeypatch
):
    import matplotlib.pyplot as plt
    import scanpy as sc

    adata, options = make_dpt_profiles(case), dpt_profile_cases()[case]
    before, obs = adata.X.copy(), adata.obs.copy(deep=True)
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        sc.pl.dpt_timeseries(adata, show=False, **options)
    ax = plt.gcf().axes[0]
    heatmap = bool(ax.images)
    expected = (
        np.asarray(ax.images[0].get_array())
        if heatmap
        else np.ma.concatenate([c.get_offsets() for c in ax.collections])
    )
    limits = [ax.get_xlim(), ax.get_ylim()]
    boundaries = [line.get_xdata()[0] for line in ax.lines]
    xlabel = ax.get_xlabel()
    plt.close("all")
    for owner, name in [
        (sc.pl, "dpt_timeseries"),
        (sc.tl, "dpt"),
        (sc.tl, "diffmap"),
        (sc.pp, "neighbors"),
    ]:
        monkeypatch.setattr(
            owner, name, lambda *a, **k: pytest.fail("Ran upstream plotting/analysis")
        )
    spec = gsc.pl.dpt_timeseries(adata, show=False, **options).to_dict()
    mark = next(
        m
        for m in leaf_marks(spec)
        if m["mark"]["type"] == ("rect" if heatmap else "point")
    )
    table = spec["datasets"][mark["data"]["name"]]
    actual = (
        np.array([r["_value"] for r in table]).reshape(adata.n_vars, -1)
        if heatmap
        else np.array([[r["_time"], r["_value"]] for r in table])
    )
    np.testing.assert_array_equal(actual, expected)
    scales = (
        spec["scales"]
        if heatmap
        else {a: mark["encoding"][a]["scale"] for a in ("x", "y")}
    )
    for axis, domain in zip(("x", "y"), limits, strict=True):
        np.testing.assert_allclose(scales[axis]["domain"], domain)
    rules = [m for m in leaf_marks(spec) if m["mark"]["type"] == "rule"]
    highlights = spec["datasets"][rules[0]["data"]["name"]] if rules else []
    assert [row["position"] for row in highlights] == boundaries
    if heatmap:
        assert any(
            m.get("encoding", {}).get("x", {}).get("axis", {}).get("title") == xlabel
            for m in leaf_marks(spec)
        )
    else:
        assert mark["encoding"]["x"]["axis"]["title"] == xlabel
    np.testing.assert_array_equal(adata.X, before)
    pd.testing.assert_frame_equal(adata.obs, obs)
    assert adata.uns["dpt_changepoints"] == boundaries


def test_gene_view_uses_x_and_saved_indices_without_raw_layers_or_other_dpt_fields(
    monkeypatch,
):
    from anndata import AnnData

    source = make_dpt_profiles()
    source.raw = source
    adata = source[:, [1, 0]]
    expected = source.X[source.obs["dpt_order_indices"].to_numpy()][:, [1, 0]]
    monkeypatch.setattr(AnnData, "raw", property(lambda self: pytest.fail("Read raw")))

    # AnnData 0.13 stores X under layers[None]; named layers must remain unread.
    def guard(getitem):
        def read(self, key):
            assert key is None, "Read a named layer"
            return getitem(self, key)

        return read

    for layer_type in {type(source.layers), type(adata.layers)}:
        monkeypatch.setattr(layer_type, "__getitem__", guard(layer_type.__getitem__))
    spec = gsc.pl.dpt_timeseries(adata, show=False).to_dict()
    mark = next(m for m in leaf_marks(spec) if m["mark"]["type"] == "rect")
    rows = spec["datasets"][mark["data"]["name"]]
    np.testing.assert_array_equal(
        np.array([r["_value"] for r in rows]).reshape(2, -1), expected.T
    )
    assert adata.is_view


@pytest.mark.parametrize("field", ["dpt_order_indices", "dpt_changepoints"])
def test_missing_metadata_errors_before_expression_access(field, monkeypatch):
    from anndata import AnnData

    adata = make_dpt_profiles()
    del (adata.obs if field == "dpt_order_indices" else adata.uns)[field]
    monkeypatch.setattr(
        AnnData, "X", property(lambda self: pytest.fail("Read expression"))
    )
    with pytest.raises(ValueError, match="run sc.tl.dpt"):
        gsc.pl.dpt_timeseries(adata, show=False)


@pytest.mark.parametrize("indices", [[0.5] * 7, ["0"] * 7, [7] * 7, [-8] * 7])
def test_invalid_indices_fail_without_reconstructing_an_order(indices):
    adata = make_dpt_profiles()
    adata.obs["dpt_order_indices"] = indices
    with pytest.raises(ValueError, match="gsc.pl.dpt_timeseries:.*valid row indices"):
        gsc.pl.dpt_timeseries(adata, show=False)


def test_backed_and_sparse_sources_fail_without_loading_or_densifying(
    tmp_path, monkeypatch
):
    from anndata import AnnData, read_h5ad

    adata = make_dpt_profiles()
    adata.write_h5ad(tmp_path / "dpt.h5ad")
    backed = read_h5ad(tmp_path / "dpt.h5ad", backed="r")
    try:
        with monkeypatch.context() as guarded:
            guarded.setattr(
                AnnData, "X", property(lambda self: pytest.fail("Read backed X"))
            )
            with pytest.raises(TypeError, match="backed/lazy"):
                gsc.pl.dpt_timeseries(backed, show=False)
    finally:
        backed.file.close()
    adata.X = sparse.csr_matrix(adata.X)
    monkeypatch.setattr(
        sparse.csr_matrix, "toarray", lambda *a, **k: pytest.fail("Densified X")
    )
    with pytest.raises(TypeError, match="resident"):
        gsc.pl.dpt_timeseries(adata, show=False)


@pytest.mark.parametrize(
    "options,error",
    [
        ({"as_heatmap": 1}, TypeError),
        ({"show_values": 1}, TypeError),
        ({"zoom": "x"}, TypeError),
        ({"as_heatmap": False, "show_values": True}, NotImplementedError),
    ],
)
def test_invalid_flags_precede_optional_imports(options, error, monkeypatch):
    monkeypatch.setattr(
        gsc.pl, "_require_scanpy", lambda *a: pytest.fail("Imported Scanpy")
    )
    with pytest.raises(error, match=r"gsc\.pl\.dpt_timeseries:"):
        gsc.pl.dpt_timeseries(object(), **options)


def test_single_gene_points_keep_the_parent_color_requirement():
    with pytest.raises(ValueError, match="one variable requires color"):
        gsc.pl.dpt_timeseries(
            make_dpt_profiles("single_gene"), as_heatmap=False, show=False
        )
