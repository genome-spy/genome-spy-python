"""Time-series data semantics compared with the pinned public Scanpy helper."""

import inspect
import warnings

import numpy as np
import pandas as pd
import pytest
from scipy import sparse

import genome_spy.integrations.scanpy as gsc
from genome_spy.integrations.scanpy._timeseries_data import prepare_timeseries
from tests.integrations.scanpy.helpers import leaf_marks
from tests.integrations.scanpy.timeseries_fixture import timeseries_cases


@pytest.mark.parametrize("family", ["timeseries", "timeseries_subplot"])
@pytest.mark.parametrize("case", timeseries_cases())
def test_profiles_match_scanpy_positions_limits_colors_and_draw_order(
    family, case, monkeypatch
):
    import matplotlib.pyplot as plt
    import scanpy as sc

    X, options = timeseries_cases()[case]
    original = X.copy()
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        getattr(sc.pl, family)(X, **options)
    fig, ax = plt.gcf(), plt.gcf().axes[0]
    fig.canvas.draw()
    expected = np.ma.concatenate([c.get_offsets() for c in ax.collections])
    visible = ~np.ma.getmaskarray(expected).any(axis=1)
    expected = np.asarray(expected)[visible]
    domains = (ax.get_xlim(), ax.get_ylim())
    colors = np.concatenate(
        [
            np.repeat(c.get_facecolors(), len(c.get_offsets()), axis=0)
            if len(c.get_facecolors()) == 1
            else c.get_facecolors()
            for c in ax.collections
        ]
    )[visible]
    rule_limits = [line.get_ydata().tolist() for line in ax.lines]
    plt.close(fig)
    monkeypatch.setattr(
        sc.pl, family, lambda *a, **k: pytest.fail("Called upstream plot")
    )
    chart = getattr(gsc.pl, family)(X, show=False, **options)
    spec = chart.to_dict()
    points = next(
        m for m in leaf_marks(spec) if m.get("mark", {}).get("type") == "point"
    )
    records = spec["datasets"][points["data"]["name"]]
    actual = pd.DataFrame(records)
    valid = actual[["_time", "_value"]].notna().all(axis=1)
    if "_color" in actual:
        valid &= actual["_color"].notna()
    np.testing.assert_allclose(actual.loc[valid, ["_time", "_value"]], expected)
    for axis, domain in zip(("x", "y"), domains):
        scale = points["encoding"][axis]["scale"]
        np.testing.assert_allclose(scale["domain"], sorted(domain))
        assert scale.get("reverse", False) == (domain[0] > domain[1])
    if "_color" not in actual:
        from matplotlib.colors import to_rgba

        scale = points["encoding"]["fill"]["scale"]
        mapping = dict(zip(scale["domain"], scale["range"]))
        np.testing.assert_allclose(
            [to_rgba(mapping[s]) for s in actual.loc[valid, "_series"]], colors
        )
    rules = [m for m in leaf_marks(spec) if m.get("mark", {}).get("type") == "rule"]
    if rule_limits:
        assert len(rules) == 1
        np.testing.assert_allclose(
            [rules[0]["encoding"]["y"]["datum"], rules[0]["encoding"]["y2"]["datum"]],
            rule_limits[0],
        )
    else:
        assert not rules
    np.testing.assert_array_equal(X, original)


def test_forwarded_defaults_match_the_pinned_subplot_signature():
    import scanpy as sc
    from genome_spy.integrations.scanpy._timeseries_chart import build_timeseries

    native = inspect.signature(gsc.pl.timeseries).parameters
    assert native["X"].kind == inspect.Parameter.POSITIONAL_OR_KEYWORD
    assert native["kwargs"].kind == inspect.Parameter.VAR_KEYWORD
    assert all(
        p.kind == inspect.Parameter.KEYWORD_ONLY
        for name, p in native.items()
        if name not in {"X", "kwargs"}
    )
    actual = inspect.signature(build_timeseries).parameters
    for name, p in inspect.signature(sc.pl.timeseries_subplot).parameters.items():
        if name not in {"X", "ax"}:
            assert actual[name].default == p.default


def test_subplot_keeps_explicit_upstream_arguments_and_native_defaults():
    import matplotlib as mpl
    import matplotlib.pyplot as plt
    import scanpy as sc

    native = inspect.signature(gsc.pl.timeseries_subplot).parameters
    upstream = inspect.signature(sc.pl.timeseries_subplot).parameters
    for name, parameter in upstream.items():
        if name == "ax":
            assert name not in native
        else:
            assert native[name].kind == parameter.kind
            assert native[name].default == parameter.default
    assert set(native) - set(upstream) == {
        "show",
        "save",
        "hover",
        "zoom",
        "series_select",
        "ruler",
        "width",
        "height",
        "kwargs",
    }
    plt.close("all")
    with (
        mpl.rc_context({"figure.figsize": (6.4, 4.8), "figure.dpi": 100}),
        warnings.catch_warnings(),
    ):
        warnings.simplefilter("ignore")
        sc.pl.timeseries_subplot(np.array([[1, 2], [3, 4]]))
    fig = plt.gcf()
    fig.canvas.draw()
    bounds = fig.axes[0].get_window_extent()
    spec = gsc.pl.timeseries_subplot([[1, 2], [3, 4]], show=False).to_dict()
    np.testing.assert_allclose(
        [spec["width"], spec["height"]], [bounds.width, bounds.height]
    )
    plt.close(fig)


def test_subplot_errors_name_the_requested_entry():
    for options, error in [
        ({"time": [1]}, ValueError),
        ({"marker": "^"}, NotImplementedError),
        ({"ax": None}, TypeError),
        ({"return_fig": True}, TypeError),
    ]:
        with pytest.raises(error, match=r"gsc\.pl\.timeseries_subplot:"):
            gsc.pl.timeseries_subplot([[1, 2], [3, 4]], show=False, **options)


@pytest.mark.parametrize("family", ["timeseries", "timeseries_subplot"])
def test_numeric_colors_do_not_read_a_series_palette(family):
    plot = getattr(gsc.pl, family)
    options = {"color": [0.2, 0.8], "show": False}
    expected = plot([1, 2], palette=None, **options).to_dict()
    actual = plot([1, 2], palette=object(), **options).to_dict()
    assert actual == expected


def test_numeric_tables_masks_missingness_and_ids_are_preserved():
    frame = pd.DataFrame(
        {"B": pd.array([1, None, 3], dtype="Int64"), "A": [True, False, True]}
    )
    before = frame.copy(deep=True)
    result, _ = prepare_timeseries(
        frame,
        time=None,
        color=None,
        var_names=["B", "A"],
        highlights_x=(),
        xlim=None,
        yticks=None,
        palette=None,
        legend=True,
    )
    assert result.table["_id"].tolist() == [0, 2, 4, 1, 3, 5]
    np.testing.assert_allclose(
        result.table["_value"], [1, np.nan, 3, 1, 0, 1], equal_nan=True
    )
    pd.testing.assert_frame_equal(frame, before)
    masked = np.ma.array([[1, 2], [3, 4]], mask=[[False, True], [False, False]])
    spec = gsc.pl.timeseries(masked, show=False).to_dict()
    records = next(iter(spec["datasets"].values()))
    assert [r["_value"] for r in records] == [1, 3, None, 4]


@pytest.mark.parametrize("family", ["timeseries", "timeseries_subplot"])
@pytest.mark.parametrize(
    "values,options,error,match",
    [
        ([], {}, ValueError, "nonempty"),
        (sparse.eye(2), {}, TypeError, "resident"),
        ([[1j]], {}, TypeError, "real numbers"),
        ([["1"]], {}, TypeError, "real numbers"),
        ([[np.inf]], {}, ValueError, "finite"),
        ([1, 2], {}, ValueError, "requires color"),
        ([[1, 2], [3, 4]], {"time": [1]}, ValueError, "time"),
        ([[1, 2], [3, 4]], {"time": [np.inf, 0]}, ValueError, "finite"),
        ([1, 2], {"color": ["A"]}, ValueError, "color"),
        ([1, 2], {"color": ["A", None]}, ValueError, "missing"),
        ([[1, 2], [3, 4]], {"var_names": ["A"]}, ValueError, "var_names"),
        ([[1, 2], [3, 4]], {"var_names": ["A", "A"]}, NotImplementedError, "repeated"),
        ([[1, 2]], {"palette": ["red"]}, ValueError, "palette"),
        ([[1, 2]], {"palette": object()}, NotImplementedError, "palette"),
        ([[1, 2]], {"color_map": object()}, NotImplementedError, "color_map"),
        ([[1, 2]], {"marker": "^"}, NotImplementedError, "marker"),
        ([[1, 2]], {"marker": ["o", "s"]}, NotImplementedError, "marker"),
        ([[1, 2]], {"marker": ["o", "o", "o"]}, ValueError, "marker"),
        ([[1, 2]], {"xlim": [0]}, ValueError, "xlim"),
        ([[1, 2]], {"highlights_x": [np.nan]}, ValueError, "highlights_x"),
        ([[1, 2]], {"yticks": [np.inf]}, ValueError, "yticks"),
        ([[1, 2]], {"xlabel": 1}, TypeError, "xlabel"),
        ([[1, 2]], {"legend": "yes"}, TypeError, "legend"),
        ([[1, 2]], {"zoom": "xy"}, TypeError, "zoom"),
        ([[1, 2]], {"hover": "yes"}, TypeError, "hover"),
        ([[1, 2]], {"width": 0}, ValueError, "positive"),
        ([[1, 2]], {"ax": None}, TypeError, "ax"),
        ([[1, 2]], {"unknown": True}, TypeError, "unknown"),
    ],
)
def test_unsupported_profiles_and_options_fail_clearly(
    family, values, options, error, match
):
    with pytest.raises(error, match=match):
        getattr(gsc.pl, family)(values, show=False, **options)
