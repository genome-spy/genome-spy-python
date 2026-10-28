"""Callable embedding bounds preserve Scanpy's panel inputs and native charts."""

import numpy as np
import pytest

import genome_spy.integrations.scanpy as gsc
from tests.integrations.scanpy.embedding_fixture import make_embedding_adata
from tests.integrations.scanpy.fixture_support import FAMILIES
from tests.integrations.scanpy.helpers import points, units

sc = pytest.importorskip("scanpy")


@pytest.mark.reference
@pytest.mark.parametrize("sort_order", [False, True])
@pytest.mark.parametrize("mask_obs", [None, "keep"])
@pytest.mark.parametrize("use_raw,layer", [(True, None), (False, "counts")])
@pytest.mark.parametrize("centered", [False, True])
def test_callable_inputs_and_domains_match_public_scanpy(
    sort_order, mask_obs, use_raw, layer, centered
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

    def center(values):
        captured.append(values.copy())
        return float(np.nanmean(values))

    options = dict(
        color=["score", "g1"],
        vmin=lower,
        vmax=[upper],
        sort_order=sort_order,
        mask_obs=mask_obs,
        use_raw=use_raw,
        layer=layer,
        vcenter=center if centered else None,
        show=False,
    )
    axes = sc.pl.umap(data, **options)
    expected = []
    for ax in axes:
        norm = ax.collections[0].norm
        expected.append(
            (norm.vmin, norm.vmax)
            if not centered
            else (norm.vmin, norm.vcenter, norm.vmax)
        )
    plt.close(axes[0].figure)
    upstream_inputs = captured.copy()
    captured.clear()
    spec = gsc.pl.umap(data, **options).to_dict()
    assert len(captured) == len(upstream_inputs) == (6 if centered else 4)
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
        vcenter=[categorical, "p50", None],
        zoom=True,
        show=False,
    )
    chart = getattr(gsc.pl, family)(*args, **options)
    assert len(calls) == 2
    options.update(vmin=[None, "p10", None], vmax=[None, 4, 3], vcenter=[None, 1, None])
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

    def center(values):
        captured.append(values.copy())
        values[:] = 1000
        return 0.5

    chart = gsc.pl.umap(
        data, color="score", vmin=lower, vmax=upper, vcenter=center, show=False
    )
    numeric = gsc.pl.umap(data, color="score", vmin=-1, vmax=4, vcenter=0.5, show=False)
    np.testing.assert_array_equal(data.obs.score.to_numpy(), original)
    np.testing.assert_array_equal(captured[0], [np.nan, -1, 0, 0, 1, 1, 2, 4])
    np.testing.assert_array_equal(captured[1], captured[0])
    assert chart.to_dict() == numeric.to_dict()


@pytest.mark.parametrize("name", ["vmin", "vmax", "vcenter"])
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


@pytest.mark.reference
@pytest.mark.parametrize(
    "center,bounds",
    [
        (-2, {}),
        (0, {}),
        (5, {}),
        (5, {"vmin": 4.5}),
        (-2, {"vmax": -1.5}),
        (0, {"vmin": -0.5, "vmax": 2}),
    ],
)
@pytest.mark.parametrize("colorbar_loc", [None, "right"])
def test_automatic_centered_limits_match_scanpy_without_changing_values(
    center, bounds, colorbar_loc
):
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    data = make_embedding_adata()
    options = dict(color="score", vcenter=center, colorbar_loc=colorbar_loc, show=False)
    options.update(bounds)
    ax = sc.pl.umap(data, **options)
    norm = ax.collections[0].norm
    expected = [norm.vmin, norm.vcenter, norm.vmax]
    spec = gsc.pl.umap(data, **options).to_dict()
    plt.close(ax.figure)
    assert points(spec)["encoding"]["color"]["scale"]["domain"] == expected
    assert (
        spec["datasets"]
        == gsc.pl.umap(data, color="score", show=False).to_dict()["datasets"]
    )


@pytest.mark.parametrize("bar", [None, "right"])
def test_constant_centered_colors_match_scanpy_with_and_without_a_guide(bar):
    data = make_embedding_adata()
    data.obs["score"] = 2.0
    spec = gsc.pl.umap(
        data, color="score", vcenter=2, colorbar_loc=bar, show=False
    ).to_dict()
    encoding = points(spec)["encoding"]["color"]
    assert encoding["scale"]["domain"] == ([0, 1] if bar is None else [1.8, 2, 2.2])
    if bar is None:
        assert encoding["datum"] == 1


@pytest.mark.parametrize(
    "bounds", [{"vmin": 0}, {"vmin": 1}, {"vmax": 0}, {"vmax": -1}]
)
def test_explicit_bounds_must_strictly_enclose_the_center(bounds):
    with pytest.raises(ValueError, match="vcenter"):
        gsc.pl.umap(
            make_embedding_adata(), color="score", vcenter=0, **bounds, show=False
        )


def test_integer_metadata_keeps_its_dtype_in_center_callbacks():
    data = make_embedding_adata()
    values = np.array([-3, -2, -1, 0, 1, 2, 4, 6], dtype=np.int64)
    data.obs["score"] = values
    calls = []

    def center(colors):
        calls.append(colors.copy())
        return float(np.mean(colors))

    spec = gsc.pl.umap(data, color="score", vcenter=center, show=False).to_dict()
    assert len(calls) == 1 and calls[0].dtype == values.dtype
    np.testing.assert_array_equal(calls[0], values)
    assert points(spec)["encoding"]["color"]["scale"]["domain"] == [-3, 0.875, 6]


def test_center_callback_resolves_once_per_panel_and_preserves_unsorted_masked_input():
    data = make_embedding_adata()
    calls = []

    def center(values):
        calls.append(values.copy())
        return float(np.nanmean(values))

    chart = gsc.pl.umap(
        data,
        color=["score", "g1"],
        mask_obs="keep",
        sort_order=False,
        vcenter=[center],
        show=False,
    )
    chart.to_json()
    chart.to_html(inline=True, controls=False)
    assert len(calls) == 2
    for values, source in zip(
        calls, [data.obs.score.to_numpy(), data.raw[:, "g1"].X.ravel()], strict=True
    ):
        np.testing.assert_array_equal(values, np.where(data.obs.keep, source, np.nan))
