"""PAGA comparison reuses native parents and honors stored embedding coordinates."""

import inspect
from copy import deepcopy

import numpy as np
import pandas as pd
import pytest
from anndata import AnnData

import genome_spy as gs
import genome_spy.integrations.scanpy as gsc
from tests.integrations.scanpy.helpers import leaf_marks, points
from tests.integrations.scanpy.paga_fixture import POSITIONS, make_compare

sc = pytest.importorskip("scanpy")


def test_default_on_data_bold_labels_keep_the_existing_explicit_font_restriction():
    with pytest.raises(NotImplementedError, match="legend_fontweight"):
        gsc.pl.paga_compare(make_compare(), show=False)


@pytest.mark.reference
@pytest.mark.parametrize(
    "palette",
    [
        ["#111111", "#222222", "#333333", "#444444"],
        {"D": "orange", "B": "blue", "A": "red", "C": "green"},
        ["red", "blue"],
    ],
)
def test_custom_palette_matches_scanpy_in_both_panels_without_changing_saved_colors(
    palette,
):
    import matplotlib.pyplot as plt
    from matplotlib.colors import to_rgba

    reference = make_compare()
    axes = sc.pl.paga_compare(
        reference, palette=palette, legend_fontweight="normal", show=False
    )
    expected = reference.uns["cluster_colors"]
    plt.close(axes[0].figure)
    a = make_compare()
    before = deepcopy(a.uns["cluster_colors"])
    spec = gsc.pl.paga_compare(
        a, palette=palette, legend_fontweight="normal", show=False
    ).to_dict()
    embedding, graph = spec["hconcat"]
    cells = points(embedding)["encoding"]["color"]["scale"]["range"]
    nodes = next(m for m in leaf_marks(graph) if m["mark"]["type"] == "point")
    graph_colors = nodes["encoding"]["fill"]["scale"]["range"]
    np.testing.assert_allclose(
        [to_rgba(c) for c in cells], [to_rgba(c) for c in expected]
    )
    np.testing.assert_allclose(
        [to_rgba(c) for c in graph_colors], [to_rgba(c) for c in expected]
    )
    assert a.uns["cluster_colors"] == before


def test_signature_preserves_every_upstream_parameter_and_default():
    upstream = inspect.signature(sc.pl.paga_compare).parameters
    native = inspect.signature(gsc.pl.paga_compare).parameters
    for name, parameter in upstream.items():
        assert native[name].kind == parameter.kind
        assert native[name].default == parameter.default
    assert set(native) - set(upstream) == {"hover", "zoom", "width", "height"}
    assert all(
        native[name].kind is inspect.Parameter.KEYWORD_ONLY
        for name in set(native) - set(upstream)
    )


@pytest.mark.parametrize("component", [False, True])
def test_native_named_palette_has_one_full_category_domain_in_both_panels(component):
    a = make_compare()
    before = deepcopy(a.uns["cluster_colors"])
    spec = gsc.pl.paga_compare(
        a,
        palette="set1",
        single_component=component,
        threshold=0.2,
        legend_fontweight="normal",
        show=False,
    ).to_dict()
    embedding, graph = spec["hconcat"]
    nodes = next(m for m in leaf_marks(graph) if m["mark"]["type"] == "point")
    assert points(embedding)["encoding"]["color"]["scale"]["scheme"] == "set1"
    assert nodes["encoding"]["fill"]["scale"] == {
        "type": "ordinal",
        "domain": ["A", "B", "C", "D"],
        "scheme": "set1",
    }
    assert nodes["encoding"]["fill"]["field"] == "_group"
    assert a.uns["cluster_colors"] == before


def test_explicit_palette_does_not_validate_or_replace_stale_saved_palette():
    a = make_compare()
    a.uns["cluster_colors"] = ["invalid"]
    spec = gsc.pl.paga_compare(
        a, palette="set1", legend_fontweight="normal", show=False
    ).to_dict()
    assert len(spec["hconcat"]) == 2
    assert a.uns["cluster_colors"] == ["invalid"]


def test_paga_coordinate_ownership_is_native_inheritance(monkeypatch):
    from genome_spy.integrations.scanpy import pl

    original = pl.paga
    captured = []

    def parent(*args, **kwargs):
        chart = original(*args, **kwargs)
        spec = chart.to_dict()
        assert set(spec["encoding"]) == {"x", "y"}
        assert all(not ({"x", "y"} & mark["encoding"].keys()) for mark in spec["layer"])
        captured.append(chart)
        return chart

    monkeypatch.setattr(pl, "paga", parent)
    comparison = pl.paga_compare(
        make_compare(), legend_fontweight="normal", show=False
    ).to_dict()
    expected = (
        captured[0]
        .encode(x=gs.X("_x:Q").axis(None), y=gs.Y("_y:Q").axis(None))
        .to_dict(include_schema=False)
    )
    expected.pop("datasets")
    assert comparison["hconcat"][1] == expected


@pytest.mark.reference
@pytest.mark.parametrize("components", [None, "2,3"])
@pytest.mark.parametrize("position_mode", ["median", "supplied", "cached"])
def test_positions_titles_and_limits_match_the_public_scanpy_call(
    components, position_mode
):
    import matplotlib.pyplot as plt

    options = {"components": components, "legend_fontweight": "normal"}
    if position_mode == "supplied":
        options["pos"] = POSITIONS
        options.update(title="Cells", title_graph="Graph")
    elif position_mode == "cached":
        options["color"] = "score"
    reference = make_compare()
    axes = sc.pl.paga_compare(reference, show=False, **options)
    expected_positions = reference.uns["paga"]["pos"].copy()
    expected_limits = [axes[0].get_xlim(), axes[0].get_ylim()]
    expected_titles = [ax.get_title() for ax in axes]
    common_title = axes[0].figure._suptitle
    common_title = common_title.get_text() if common_title is not None else None
    plt.close(axes[0].figure)
    a = make_compare()
    spec = gsc.pl.paga_compare(a, show=False, **options).to_dict()
    assert len(spec["hconcat"]) == 2
    np.testing.assert_allclose(a.uns["paga"]["pos"], expected_positions)
    embedding, graph = spec["hconcat"]
    for axis, limits in zip(("x", "y"), expected_limits, strict=True):
        np.testing.assert_allclose(
            points(embedding)["encoding"][axis]["scale"]["domain"], limits
        )
        assert all("scale" not in mark["encoding"][axis] for mark in leaf_marks(graph))
    assert spec.get("title") == common_title
    assert [
        embedding.get("title", {}).get("text", ""),
        graph["title"]["text"],
    ] == expected_titles
    nodes = next(
        rows for rows in spec["datasets"].values() if rows and "_cells" in rows[0]
    )
    np.testing.assert_allclose([[r["_x"], r["_y"]] for r in nodes], expected_positions)
    assert [r["_color"] for r in nodes] == (
        reference.obs.groupby("cluster", observed=True)["score"].mean().tolist()
        if position_mode == "cached"
        else reference.uns["cluster_colors"]
    )


@pytest.mark.parametrize(
    "preferred", ["draw_graph_fa", "umap", "tsne", "draw_graph_fr"]
)
def test_automatic_basis_precedence_and_explicit_basis(preferred):
    a = make_compare()
    a.obsm.clear()
    priority = ["draw_graph_fa", "umap", "tsne", "draw_graph_fr"]
    for i, basis in enumerate(priority[priority.index(preferred) :]):
        a.obsm[f"X_{basis}"] = np.column_stack(
            [np.arange(a.n_obs) + i * 100, np.arange(a.n_obs)]
        )
    spec = gsc.pl.paga_compare(a, legend_fontweight="normal", show=False).to_dict()
    cells = next(
        rows for rows in spec["datasets"].values() if rows and "_obs_id" in rows[0]
    )
    np.testing.assert_array_equal([r["_coord_0"] for r in cells], np.arange(a.n_obs))
    a.obsm["custom"] = a.obsm[f"X_{preferred}"] + 5
    gsc.pl.paga_compare(a, basis="custom", legend_fontweight="normal", show=False)
    np.testing.assert_allclose(a.uns["paga"]["pos"][0], [9, 9])


def test_reuses_parent_data_labels_aliases_and_independent_color_scales():
    a = make_compare()
    spec = gsc.pl.paga_compare(
        a,
        groups=["A"],
        groups_graph=["a", "b", "c", "d"],
        labels=["w", "x", "y", "z"],
        threshold=0.2,
        add_pos=False,
        legend_fontsize="large",
        legend_fontweight="normal",
        hover=False,
        zoom=True,
        show=False,
    ).to_dict()
    embedding, graph = spec["hconcat"]
    assert spec["resolve"]["scale"] == {
        "x": "shared",
        "y": "shared",
        "color": "independent",
        "fill": "independent",
        "stroke": "independent",
        "size": "independent",
    }
    assert spec["resolve"]["legend"] == {"default": "independent", "fill": "collected"}
    assert all(
        points(embedding)["encoding"][axis]["scale"]["zoom"] for axis in ("x", "y")
    )
    nodes = next(
        rows for rows in spec["datasets"].values() if rows and "_cells" in rows[0]
    )
    assert [r["_label"] for r in nodes] == ["w", "x", "y", "z"]
    assert all(
        m["mark"].get("tooltip") is None
        for m in leaf_marks(embedding) + leaf_marks(graph)
    )
    labels = [m for m in leaf_marks(embedding) if m["mark"]["type"] == "text"]
    assert labels[0]["mark"]["fontWeight"] == "normal"
    np.testing.assert_array_equal(a.uns["paga"]["pos"], POSITIONS + 99)


def test_no_analysis_expression_or_upstream_plotting_and_only_requested_cache_mutation(
    monkeypatch,
):
    a = make_compare()
    before = deepcopy(a)
    for owner, name in [
        (sc.tl, "paga"),
        (sc.tl, "umap"),
        (sc.pl, "paga"),
        (sc.pl, "embedding"),
        (sc.pl, "paga_compare"),
    ]:
        monkeypatch.setattr(
            owner,
            name,
            lambda *a, **k: pytest.fail("Ran analysis or upstream plotting"),
        )
    monkeypatch.setattr(
        AnnData, "X", property(lambda _: pytest.fail("Read expression"))
    )
    spec = gsc.pl.paga_compare(
        a, add_pos=False, legend_fontweight="normal", show=False
    ).to_dict()
    assert len(spec["hconcat"]) == 2
    assert a.obs.equals(before.obs) and a.var.equals(before.var)
    np.testing.assert_array_equal(a.obsm["X_umap"], before.obsm["X_umap"])
    np.testing.assert_array_equal(a.uns["paga"]["pos"], before.uns["paga"]["pos"])
    np.testing.assert_array_equal(
        a.uns["paga"]["connectivities"].data, before.uns["paga"]["connectivities"].data
    )
    assert a.uns.keys() == before.uns.keys()


@pytest.mark.parametrize(
    "options,error,match",
    [
        ({"color": ["cluster", "score"]}, NotImplementedError, "single"),
        ({"components": "all"}, NotImplementedError, "one coordinate pair"),
        ({"projection": "3d"}, NotImplementedError, "projection"),
        ({"legend_fontoutline": 2}, NotImplementedError, "legend_fontoutline"),
        ({"right_margin": 0.2}, NotImplementedError, "margins"),
        ({"plot": False}, NotImplementedError, "plot=False"),
        ({"transitions": "transitions_confidence"}, NotImplementedError, "transitions"),
        ({"ax": object()}, TypeError, "ax is omitted"),
        ({"hover": 1}, TypeError, "hover"),
        ({"width": 0}, ValueError, "width"),
        ({"title": 42}, TypeError, "title"),
        ({"title_graph": 42}, TypeError, "title_graph"),
    ],
)
def test_invalid_options_never_display_a_partial_comparison(
    monkeypatch, options, error, match
):
    monkeypatch.setattr(
        gs.TopLevelSpec,
        "display",
        lambda *a, **k: pytest.fail("Displayed a partial chart"),
    )
    a = make_compare()
    cached = a.uns["paga"]["pos"].copy()
    with pytest.raises(error, match=match):
        gsc.pl.paga_compare(a, legend_fontweight="normal", show=True, **options)
    np.testing.assert_array_equal(a.uns["paga"]["pos"], cached)


@pytest.mark.parametrize("missing", ["embedding", "paga", "cached", "unused_group"])
def test_missing_or_misaligned_results_fail_explicitly(missing):
    a, options = make_compare(), {}
    if missing == "embedding":
        a.obsm.clear()
    elif missing == "paga":
        del a.uns["paga"]
    elif missing == "cached":
        del a.uns["paga"]["pos"]
        options["color"] = "score"
    else:
        a = a[a.obs["cluster"] != "D"].copy()
        a.obs["cluster"] = pd.Categorical(
            a.obs["cluster"], categories=["A", "B", "C", "D"]
        )
    with pytest.raises(ValueError, match="embedding|PAGA|pos|shape|graph"):
        gsc.pl.paga_compare(a, legend_fontweight="normal", show=False, **options)
