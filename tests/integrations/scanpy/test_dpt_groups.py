"""Stored DPT group/pseudotime semantics and metadata-only access."""

import inspect
import warnings

import numpy as np
import pandas as pd
import pytest

import genome_spy.integrations.scanpy as gsc
from tests.integrations.scanpy.dpt_fixture import make_dpt, dpt_cases, dpt_reference
from tests.integrations.scanpy.helpers import leaf_marks


def test_signature_matches_scanpy_and_adds_only_native_options():
    import scanpy as sc

    actual = inspect.signature(gsc.pl.dpt_groups_pseudotime).parameters
    upstream = inspect.signature(sc.pl.dpt_groups_pseudotime).parameters
    for name, value in upstream.items():
        assert actual[name].kind == value.kind
        assert actual[name].default == value.default
    assert actual.keys() - upstream.keys() == {"hover", "zoom", "width", "height"}


@pytest.mark.parametrize("case", dpt_cases())
def test_panels_match_public_scanpy_values_bounds_colors_ticks_and_order(
    case, monkeypatch
):
    import matplotlib.pyplot as plt
    from matplotlib.colors import to_rgba
    import scanpy as sc

    adata, options = make_dpt(case), dpt_cases()[case]
    before = adata.obs.copy(deep=True)
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        fig = dpt_reference(adata, **options)
    fig.canvas.draw()
    expected = []
    for ax in fig.axes:
        expected.append(
            (
                np.ma.concatenate([c.get_offsets() for c in ax.collections]),
                ax.get_xlim(),
                ax.get_ylim(),
                ax.get_yticks(),
                ax.collections,
            )
        )
    plt.close(fig)
    for target, name in [
        (sc.pl, "dpt_groups_pseudotime"),
        (sc.tl, "dpt"),
        (sc.tl, "diffmap"),
        (sc.pp, "neighbors"),
    ]:
        monkeypatch.setattr(
            target, name, lambda *a, **k: pytest.fail("Ran upstream plotting/analysis")
        )
    spec = gsc.pl.dpt_groups_pseudotime(adata, show=False, **options).to_dict()
    assert len(spec["vconcat"]) == 2
    assert spec["resolve"]["scale"] == {"default": "independent"}
    for panel, (offsets, xlim, ylim, yticks, collections) in zip(
        spec["vconcat"], expected, strict=True
    ):
        point = next(m for m in leaf_marks(panel) if m["mark"]["type"] == "point")
        rows = spec["datasets"][point["data"]["name"]]
        valid = [
            r
            for r in rows
            if r["_value"] is not None and r.get("_color", 0) is not None
        ]
        np.testing.assert_allclose(
            [[r["_time"], r["_value"]] for r in valid],
            np.asarray(offsets)[~np.ma.getmaskarray(offsets).any(axis=1)],
        )
        assert len(rows) == adata.n_obs and len({r["_id"] for r in rows}) == adata.n_obs
        for axis, domain in [("x", xlim), ("y", ylim)]:
            np.testing.assert_allclose(
                point["encoding"][axis]["scale"]["domain"], domain
            )
        fill = point["encoding"]["fill"]
        if fill.get("field") == "_series":
            colors = dict(
                zip(fill["scale"]["domain"], fill["scale"]["range"], strict=True)
            )
            np.testing.assert_allclose(
                [to_rgba(colors[r["_series"]]) for r in valid],
                np.concatenate(
                    [
                        np.repeat(
                            c.get_facecolors()[:1],
                            (~np.ma.getmaskarray(c.get_offsets()).any(axis=1)).sum(),
                            axis=0,
                        )
                        for c in collections
                    ]
                ),
            )
        else:
            np.testing.assert_allclose(
                fill["scale"]["domain"], collections[0].get_clim()
            )
        if "values" in point["encoding"]["y"]["axis"]:
            np.testing.assert_array_equal(
                point["encoding"]["y"]["axis"]["values"], yticks
            )
        else:
            assert len(adata.obs["dpt_groups"].cat.categories) >= 5
    pd.testing.assert_frame_equal(adata.obs, before)


@pytest.mark.parametrize("backed", [False, True])
def test_views_and_backed_metadata_work_without_expression_or_analysis(
    tmp_path, monkeypatch, backed
):
    from anndata import AnnData, read_h5ad

    original = make_dpt()
    if backed:
        original.write_h5ad(tmp_path / "dpt.h5ad")
        adata = read_h5ad(tmp_path / "dpt.h5ad", backed="r")
    else:
        adata = original[[6, 1, 4, 3]]
    before = adata.obs.copy(deep=True)
    try:
        for name in ("X", "raw", "layers"):
            monkeypatch.setattr(
                AnnData, name, property(lambda self: pytest.fail("Read expression"))
            )
        chart = gsc.pl.dpt_groups_pseudotime(adata, show=False)
        assert len(chart.to_dict()["vconcat"]) == 2
        pd.testing.assert_frame_equal(adata.obs, before)
    finally:
        if backed:
            adata.file.close()


@pytest.mark.parametrize(
    "field", ["dpt_groups", "dpt_order", "dpt_pseudotime", "dpt_changepoints"]
)
def test_missing_analysis_is_an_error(field):
    adata = make_dpt()
    del (adata.uns if field == "dpt_changepoints" else adata.obs)[field]
    with pytest.raises(ValueError, match="run sc.tl.dpt"):
        gsc.pl.dpt_groups_pseudotime(adata, show=False)


@pytest.mark.parametrize(
    "field,value,error",
    [
        ("dpt_groups", ["a"] * 8, TypeError),
        ("dpt_groups", pd.Categorical([None] + ["a"] * 7), ValueError),
        ("dpt_order", ["bad"] * 8, TypeError),
        ("dpt_order", [np.inf] + list(range(7)), ValueError),
        ("dpt_pseudotime", [np.nan] * 8, ValueError),
        ("dpt_pseudotime", ["bad"] * 8, TypeError),
        ("dpt_changepoints", [np.inf], ValueError),
    ],
)
def test_invalid_stored_metadata_fails_clearly(field, value, error):
    adata = make_dpt()
    if field == "dpt_changepoints":
        adata.uns[field] = value
    else:
        adata.obs[field] = value
    with pytest.raises(error, match=r"gsc\.pl\.dpt_groups_pseudotime:"):
        gsc.pl.dpt_groups_pseudotime(adata, show=False)


@pytest.mark.parametrize(
    "options,error",
    [
        ({"hover": 1}, TypeError),
        ({"zoom": "xy"}, TypeError),
        ({"width": 0}, ValueError),
        ({"save": True}, NotImplementedError),
    ],
)
def test_invalid_options_precede_optional_imports(options, error, monkeypatch):
    monkeypatch.setattr(
        gsc.pl, "_require_scanpy", lambda *a: pytest.fail("Loaded Scanpy")
    )
    with pytest.raises(error, match=r"gsc\.pl\.dpt_groups_pseudotime:"):
        gsc.pl.dpt_groups_pseudotime(object(), **options)


def test_native_group_guide_uses_observed_names_and_time_guide_uses_visible_range():
    a = make_dpt()
    a.obs.loc["cell-0", "dpt_order"] = np.nan
    a.obs.loc["cell-0", "dpt_pseudotime"] = -100
    spec = gsc.pl.dpt_groups_pseudotime(a, show=False).to_dict()
    group, time = [
        next(m for m in leaf_marks(p) if m["mark"]["type"] == "point")
        for p in spec["vconcat"]
    ]
    assert group["encoding"]["fill"]["scale"]["domain"] == ["alpha", "beta"]
    guide = group["encoding"]["fill"]["legend"]
    assert guide["title"] == "DPT group" and guide["orient"] == "right"
    assert guide["symbolSize"] == 49
    assert time["encoding"]["fill"]["legend"]["title"] == "pseudotime"
    assert time["encoding"]["fill"]["scale"]["domain"] == [0.2, 1.0]


def test_constant_pseudotime_uses_the_shared_expanded_native_guide():
    a = make_dpt()
    a.obs["dpt_pseudotime"] = 0.5
    spec = gsc.pl.dpt_groups_pseudotime(a, show=False).to_dict()
    fill = next(
        m for m in leaf_marks(spec["vconcat"][1]) if m["mark"]["type"] == "point"
    )["encoding"]["fill"]
    assert fill["field"] == "_color" and fill["legend"]["title"] == "pseudotime"
    np.testing.assert_allclose(fill["scale"]["domain"], [0.45, 0.55])


@pytest.mark.parametrize(
    "marker,shape", [(".", "circle"), ("o", "circle"), ("s", "square")]
)
def test_group_key_keeps_the_native_marker_shape(marker, shape):
    spec = gsc.pl.dpt_groups_pseudotime(make_dpt(), marker=marker, show=False).to_dict()
    points = next(
        m for m in leaf_marks(spec["vconcat"][0]) if m["mark"]["type"] == "point"
    )
    guide = points["encoding"]["fill"]["legend"]
    assert guide["symbolType"] == shape
    assert guide["symbolStrokeWidth"] == 0
