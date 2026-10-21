"""Callable embedding bounds preserve Scanpy's panel inputs and native charts."""

import numpy as np
import pytest

import genome_spy.integrations.scanpy as gsc
from tests.integrations.scanpy.embedding_fixture import make_embedding_adata
from tests.integrations.scanpy.helpers import points, units
from tests.integrations.scanpy.test_embedding import FAMILIES

sc = pytest.importorskip("scanpy")


@pytest.mark.parametrize("sort_order", [False, True])
@pytest.mark.parametrize("mask_obs", [None, "keep"])
@pytest.mark.parametrize("use_raw,layer", [(True, None), (False, "counts")])
def test_callable_inputs_and_domains_match_public_scanpy(
    sort_order, mask_obs, use_raw, layer
):
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    data = make_embedding_adata()
    captured = []

    def lower(values):
        captured.append(values.copy())
        return float(np.nanmin(values))

    def upper(values):
        captured.append(values.copy())
        return float(np.nanquantile(values, 0.8))

    options = dict(
        color=["score", "g1"],
        vmin=lower,
        vmax=[upper],
        sort_order=sort_order,
        mask_obs=mask_obs,
        use_raw=use_raw,
        layer=layer,
        show=False,
    )
    axes = sc.pl.umap(data, **options)
    expected = [
        (ax.collections[0].norm.vmin, ax.collections[0].norm.vmax) for ax in axes
    ]
    plt.close(axes[0].figure)
    upstream_inputs = captured.copy()
    captured.clear()
    spec = gsc.pl.umap(data, **options).to_dict()
    assert len(captured) == len(upstream_inputs) == 4
    for actual, reference in zip(captured, upstream_inputs, strict=True):
        np.testing.assert_array_equal(actual, reference)
        assert actual.dtype == reference.dtype
    for panel, domain in zip(units(spec), expected, strict=True):
        np.testing.assert_allclose(
            points(panel)["encoding"]["color"]["scale"]["domain"], domain
        )


@pytest.mark.parametrize("family", FAMILIES)
def test_shared_embeddings_resolve_callbacks_once_and_keep_complete_chart(family):
    data = make_embedding_adata()
    args = (data, "umap") if family == "embedding" else (data,)
    calls = []

    def upper(values):
        calls.append(values.copy())
        return float(np.nanmax(values))

    def categorical(values):
        pytest.fail("Categorical bounds must not be evaluated")

    options = dict(
        color=["cell_type", "score", "g1"],
        vmin=[categorical, "p10", None],
        vmax=[categorical, upper, upper],
        zoom=True,
        show=False,
    )
    chart = getattr(gsc.pl, family)(*args, **options)
    assert len(calls) == 2
    options.update(vmin=[None, "p10", None], vmax=[None, 4, 3])
    numeric = getattr(gsc.pl, family)(*args, **options)
    # Compare the entire chart, including axes, guides, points and interaction settings.
    assert chart.to_dict() == numeric.to_dict()
    chart.to_json()
    chart.to_html(inline=True, controls=False)
    assert len(calls) == 2


def test_callback_edits_cannot_change_other_bounds_plotted_values_or_anndata():
    data = make_embedding_adata()
    original = data.obs.score.to_numpy().copy()
    captured = []

    def lower(values):
        result = np.nanmin(values)
        values[:] = 1000
        return result

    def upper(values):
        captured.append(values.copy())
        return np.nanmax(values)

    chart = gsc.pl.umap(data, color="score", vmin=lower, vmax=upper, show=False)
    numeric = gsc.pl.umap(data, color="score", vmin=-1, vmax=4, show=False)
    np.testing.assert_array_equal(data.obs.score.to_numpy(), original)
    np.testing.assert_array_equal(captured[0], [np.nan, -1, 0, 0, 1, 1, 2, 4])
    assert chart.to_dict() == numeric.to_dict()


@pytest.mark.parametrize("name", ["vmin", "vmax"])
@pytest.mark.parametrize(
    "value", [None, True, "1", [1], np.array(1), complex(1), np.nan, np.inf]
)
def test_invalid_callable_results_fail_by_bound_and_panel(name, value):
    with pytest.raises(
        ValueError, match=rf"{name} callable for panel 1.*finite number"
    ):
        gsc.pl.umap(
            make_embedding_adata(),
            color="score",
            **{name: lambda values: value},
            show=False,
        )


def test_callback_exception_is_preserved():
    def fail(values):
        raise RuntimeError("user callback failed")

    with pytest.raises(RuntimeError, match="user callback failed"):
        gsc.pl.umap(make_embedding_adata(), color="score", vmin=fail, show=False)


@pytest.mark.parametrize("colorbar_loc,domain", [(None, [0, 1]), ("right", [1.8, 2.2])])
def test_constant_callable_bounds_reuse_existing_colorbar_expansion(
    colorbar_loc, domain
):
    spec = gsc.pl.umap(
        make_embedding_adata(),
        color="score",
        vmin=lambda values: 2,
        vmax=lambda values: np.float32(2),
        colorbar_loc=colorbar_loc,
        show=False,
    ).to_dict()
    np.testing.assert_allclose(
        points(spec)["encoding"]["color"]["scale"]["domain"], domain
    )


def test_callable_bounds_keep_existing_limit_order_validation():
    with pytest.raises(ValueError, match="vmin cannot exceed vmax"):
        gsc.pl.umap(
            make_embedding_adata(),
            color="score",
            vmin=np.nanmax,
            vmax=np.nanmin,
            show=False,
        )
