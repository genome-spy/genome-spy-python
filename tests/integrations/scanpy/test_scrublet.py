"""Stored histogram semantics, upstream defaults and native Scrublet charts."""

from copy import deepcopy
import inspect

import anndata as ad
import numpy as np
import pandas as pd
import pytest

import genome_spy.integrations.scanpy as gsc
from genome_spy.integrations.scanpy._scrublet_data import prepare_scrublet
from tests.integrations.scanpy.helpers import units, leaf_marks
from tests.integrations.scanpy.scrublet_fixture import make_scrublet

sc = pytest.importorskip("scanpy")


def test_signature_preserves_scanpy_defaults_and_omits_matplotlib_return():
    actual = inspect.signature(gsc.pl.scrublet_score_distribution).parameters
    expected = inspect.signature(sc.pl.scrublet_score_distribution).parameters
    for name, p in expected.items():
        if name == "return_fig":
            assert name not in actual
        else:
            assert actual[name].kind == p.kind and actual[name].default == p.default
    assert set(actual) - set(expected) == {"hover", "zoom", "width", "height", "kwargs"}
    assert all(
        actual[name].kind == inspect.Parameter.KEYWORD_ONLY
        for name in ("hover", "zoom", "width", "height")
    )


@pytest.mark.parametrize("batched", [False, True])
@pytest.mark.parametrize(
    "observed_scale,simulated_scale",
    [("log", "linear"), ("linear", "log"), ("linear", "linear"), ("log", "log")],
)
def test_bins_densities_thresholds_titles_limits_and_batches_match_scanpy(
    batched, observed_scale, simulated_scale
):
    import matplotlib.pyplot as plt

    a = make_scrublet(batched)
    with plt.rc_context(plt.rcParamsDefault):
        axes = np.asarray(
            sc.pl.scrublet_score_distribution(
                a,
                scale_hist_obs=observed_scale,
                scale_hist_sim=simulated_scale,
                show=False,
            )
        ).ravel()
    table, thresholds = prepare_scrublet(a)
    spec = gsc.pl.scrublet_score_distribution(
        a, scale_hist_obs=observed_scale, scale_hist_sim=simulated_scale, show=False
    ).to_dict()
    assert len(units(spec)) == len(axes) == (4 if batched else 2)
    assert len(table) == len(axes) * 49
    for i, (panel, ax) in enumerate(zip(units(spec), axes, strict=True)):
        rows = table[table.panel == i]
        np.testing.assert_allclose(
            rows.start, [p.get_x() for p in ax.patches], atol=2e-16
        )
        np.testing.assert_allclose(
            rows.end - rows.start, [p.get_width() for p in ax.patches]
        )
        np.testing.assert_allclose(
            rows.density, [p.get_height() for p in ax.patches], rtol=1e-14
        )
        assert panel["title"]["text"] == ax.get_title()
        bars = leaf_marks(panel)[0]
        for axis in ("x", "y"):
            np.testing.assert_allclose(
                bars["encoding"][axis]["scale"]["domain"],
                getattr(ax, f"get_{axis}lim")(),
            )
            assert (
                bars["encoding"][axis]["axis"]["title"]
                == getattr(ax, f"get_{axis}label")()
            )
        assert len(ax.lines) == int(thresholds[i] is not None)
        if ax.lines:
            np.testing.assert_allclose(ax.lines[0].get_xdata(), thresholds[i])
            assert leaf_marks(panel)[-1]["mark"]["type"] == "rule"
    if batched:
        assert table.batch.unique().tolist() == ["B", "A"] and thresholds == [
            0.27,
            0.27,
            None,
            None,
        ]
    plt.close(axes[0].figure)


def test_denominator_ignores_missing_and_out_of_range_and_includes_right_edge():
    table, _ = prepare_scrublet(make_scrublet())
    rows = table[table.panel == 0]
    assert rows["count"].sum() == 10
    assert (
        rows.iloc[0]["count"] == 1
        and rows.iloc[1]["count"] == 1
        and rows.iloc[-1]["count"] == 1
    )
    np.testing.assert_allclose(np.sum(rows.density * (rows.end - rows.start)), 1)
    assert rows.density.max() == pytest.approx(3 * 49 / 10)


@pytest.mark.parametrize("threshold", [-0.2, 0, 1, 1.4, None])
def test_thresholds_preserve_expanded_x_limits_and_density_limits(threshold):
    import matplotlib.pyplot as plt

    a = make_scrublet()
    a.uns["scrublet"]["threshold"] = threshold
    axes = sc.pl.scrublet_score_distribution(a, show=False)
    spec = gsc.pl.scrublet_score_distribution(a, show=False).to_dict()
    for panel, ax in zip(units(spec), axes, strict=True):
        bars = leaf_marks(panel)[0]
        for axis in ("x", "y"):
            np.testing.assert_allclose(
                bars["encoding"][axis]["scale"]["domain"],
                getattr(ax, f"get_{axis}lim")(),
            )
    plt.close(axes[0].figure)


def test_constant_log_histogram_uses_shared_domain_helper():
    import matplotlib.pyplot as plt

    a = make_scrublet()
    a.obs["doublet_score"] = 0.5
    axes = sc.pl.scrublet_score_distribution(a, show=False)
    spec = gsc.pl.scrublet_score_distribution(a, show=False).to_dict()
    np.testing.assert_allclose(
        leaf_marks(units(spec)[0])[0]["encoding"]["y"]["scale"]["domain"],
        axes[0].get_ylim(),
    )
    plt.close(axes[0].figure)


def test_metadata_only_views_backed_and_no_analysis_fallback(monkeypatch, tmp_path):
    a = make_scrublet()
    path = tmp_path / "stored.h5ad"
    a.write_h5ad(path)
    backed = ad.read_h5ad(path, backed="r")
    view = a[:10]
    monkeypatch.setattr(
        sc.pp, "scrublet", lambda *a, **k: pytest.fail("Reran Scrublet")
    )
    monkeypatch.setattr(
        ad.AnnData, "X", property(lambda *a: pytest.fail("Read expression"))
    )
    try:
        for data in (a, view, backed):
            assert gsc.pl.scrublet_score_distribution(data, show=False).to_dict()[
                "datasets"
            ]
        assert view.is_view
        del a.uns["scrublet"]
        with pytest.raises(ValueError, match="run sc.pp.scrublet explicitly"):
            gsc.pl.scrublet_score_distribution(a, show=False)
    finally:
        backed.file.close()


@pytest.mark.parametrize(
    "options,error",
    [
        ({"ax": None}, TypeError),
        ({"return_fig": False}, TypeError),
        ({"bins": 20}, TypeError),
        ({"scale_hist_obs": "symlog"}, NotImplementedError),
        ({"scale_hist_sim": "logit"}, NotImplementedError),
        ({"scale_hist_sim": 1}, NotImplementedError),
        ({"figsize": None}, TypeError),
        ({"figsize": (1, 1)}, ValueError),
        ({"figsize": (8, float("nan"))}, ValueError),
        ({"figsize": (10, 4), "width": 200}, TypeError),
        ({"hover": 1}, TypeError),
        ({"zoom": "xy"}, TypeError),
        ({"width": 0}, ValueError),
    ],
)
def test_unsupported_options_fail_before_dependencies(monkeypatch, options, error):
    monkeypatch.setattr(
        gsc.pl, "_require_scanpy", lambda *a: pytest.fail("Loaded Scanpy")
    )
    with pytest.raises(error, match="gsc.pl.scrublet_score_distribution"):
        gsc.pl.scrublet_score_distribution(object(), **options)


@pytest.mark.parametrize(
    "change,error,match",
    [
        (lambda a: a.uns.clear(), ValueError, "stored scrublet"),
        (lambda a: a.obs.pop("doublet_score"), ValueError, "doublet_score"),
        (
            lambda a: a.uns["scrublet"].pop("doublet_scores_sim"),
            ValueError,
            "doublet_scores_sim",
        ),
        (
            lambda a: a.uns["scrublet"].update(threshold=float("nan")),
            ValueError,
            "threshold",
        ),
        (
            lambda a: a.uns["scrublet"].update(doublet_scores_sim=[np.nan, 2, -1]),
            ValueError,
            "at least one score",
        ),
        (
            lambda a: a.uns["scrublet"].update(doublet_scores_sim=[[0.1, 0.2]]),
            TypeError,
            "one-dimensional",
        ),
        (
            lambda a: a.uns["scrublet"].update(doublet_scores_sim=[float("inf")]),
            ValueError,
            "finite",
        ),
        (
            lambda a: a.uns["scrublet"].update(doublet_scores_sim=["bad"]),
            TypeError,
            "real numbers",
        ),
        (
            lambda a: a.uns["scrublet"].update(batched_by="missing"),
            ValueError,
            "batched_by",
        ),
    ],
)
def test_invalid_results_fail_clearly(change, error, match):
    a = make_scrublet()
    change(a)
    with pytest.raises(error, match=match):
        gsc.pl.scrublet_score_distribution(a, show=False)


def test_batch_order_missing_values_unused_categories_and_missing_results():
    a = make_scrublet(True)
    a.obs["sample"] = a.obs["sample"].astype(str)
    table, _ = prepare_scrublet(a)
    assert table.batch.unique().tolist() == ["A", "B"]
    a.obs.iloc[0, a.obs.columns.get_loc("sample")] = None
    table, _ = prepare_scrublet(a)
    assert table[table.panel == 0]["count"].sum() == 9
    a.obs["sample"] = pd.Categorical(a.obs["sample"], categories=["A", "B", "unused"])
    with pytest.raises(NotImplementedError, match="unused batch"):
        prepare_scrublet(a)
    a = make_scrublet(True)
    del a.uns["scrublet"]["batches"]["A"]
    with pytest.raises(ValueError, match="batch 'A'"):
        prepare_scrublet(a)


def test_native_dimensions_hover_and_chart_snapshot():
    a = make_scrublet()
    chart = gsc.pl.scrublet_score_distribution(
        a, figsize=(10, 4), hover=False, show=False
    )
    spec = chart.to_dict()
    assert all(
        panel["width"] == 440 and panel["height"] == 310 for panel in units(spec)
    )
    assert all(
        mark["mark"]["tooltip"] is None
        for panel in units(spec)
        for mark in leaf_marks(panel)
    )
    snapshot = deepcopy(spec)
    a.uns["scrublet"]["doublet_scores_sim"][:] = 0
    a.obs["doublet_score"] = 0
    assert chart.to_dict() == snapshot


def test_duplicate_metadata_columns_fail_with_plot_context():
    a = make_scrublet()
    a.obs = pd.concat([a.obs, a.obs], axis=1)
    with pytest.raises(
        ValueError,
        match="gsc.pl.scrublet_score_distribution: obs column names must be unique",
    ):
        gsc.pl.scrublet_score_distribution(a, show=False)
