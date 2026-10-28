"""Public PAGA reference semantics, metadata-only layout reuse and deliberate cache writes."""

import inspect
import warnings

import numpy as np
import pandas as pd
import pytest

import genome_spy.integrations.scanpy as gsc
from tests.integrations.scanpy.helpers import leaf_marks
from tests.integrations.scanpy.paga_fixture import (
    POSITIONS,
    make_paga,
    paga_cases,
    paga_reference,
)


def test_signature_retains_scanpy_defaults_except_omitted_matplotlib_axes():
    import scanpy as sc

    actual = inspect.signature(gsc.pl.paga).parameters
    expected = inspect.signature(sc.pl.paga).parameters
    for key, param in expected.items():
        if key in {"ax", "cax"}:
            assert key not in actual
        else:
            assert actual[key].kind == param.kind
            assert actual[key].default == param.default
    assert actual.keys() - expected.keys() == {
        "hover",
        "zoom",
        "width",
        "height",
        "palette",
        "edge_slider",
        "show_node_labels",
        "kwargs",
    }


@pytest.mark.parametrize("case", paga_cases())
def test_nodes_edges_labels_bounds_and_cache_match_public_scanpy(case, monkeypatch):
    import matplotlib.pyplot as plt
    from matplotlib.colors import to_rgba
    from matplotlib.collections import LineCollection, PathCollection
    import scanpy as sc

    a = make_paga(case)
    options = paga_cases()[case]
    reference, reference_options = paga_reference(case)
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        ax = sc.pl.paga(reference, show=False, **reference_options)
        ax.figure.canvas.draw()
    point = next(c for c in ax.collections if isinstance(c, PathCollection))
    positions = np.asarray(point.get_offsets())
    areas = point.get_sizes()
    colors = point.get_facecolors()
    values = point.get_array()
    domain = [point.norm.vmin, point.norm.vmax]
    expected_edges = [
        (c.get_segments(), c.get_linewidths())
        for c in ax.collections
        if isinstance(c, LineCollection)
    ]
    labels = [t.get_text() for t in ax.texts]
    bounds = [ax.get_xlim(), ax.get_ylim()]
    plt.close("all")
    original = sc.pl.paga
    layout_calls = []

    def layout_only(data, **kwargs):
        assert data is not a and kwargs["plot"] is False
        layout_calls.append(kwargs)
        return original(data, **kwargs)

    monkeypatch.setattr(sc.pl, "paga", layout_only)
    monkeypatch.setattr(
        sc.tl, "paga", lambda *a, **k: pytest.fail("Reran PAGA analysis")
    )
    monkeypatch.setattr(
        plt, "figure", lambda *a, **k: pytest.fail("Created a Matplotlib figure")
    )
    monkeypatch.setattr(
        plt, "subplots", lambda *a, **k: pytest.fail("Created Matplotlib axes")
    )
    before = a.obs.copy(deep=True)
    stored = a.uns["paga"]["connectivities"].copy()
    old_pos = a.uns["paga"]["pos"].copy()
    spec = gsc.pl.paga(a, show=False, **options).to_dict()
    assert bool(layout_calls) == ("pos" not in options)
    mark = next(m for m in leaf_marks(spec) if m["mark"]["type"] == "point")
    rows = spec["datasets"][mark["data"]["name"]]
    np.testing.assert_allclose(
        [[r["_x"], r["_y"]] for r in rows], positions, atol=1e-10
    )
    np.testing.assert_allclose([r["_area"] for r in rows], areas)
    if values is None:
        np.testing.assert_allclose([to_rgba(r["_color"]) for r in rows], colors)
    else:
        np.testing.assert_allclose(
            [np.nan if r["_color"] is None else r["_color"] for r in rows],
            values.filled(np.nan),
            equal_nan=True,
        )
        fill = mark["encoding"]["fill"]
        assert bool(fill["legend"]) == (options.get("colorbar") is not False)
        if domain[0] == domain[1]:
            assert fill["scale"]["domain"][0] <= domain[0]
            assert fill["scale"]["domain"][1] > domain[1]
        else:
            np.testing.assert_allclose(fill["scale"]["domain"], domain)
        assert fill["scale"]["scheme"] == "viridis"
    assert [r["_label"] for r in rows] == labels
    for axis, domain in zip(("x", "y"), bounds, strict=True):
        np.testing.assert_allclose(mark["encoding"][axis]["scale"]["domain"], domain)
    rules = [m for m in leaf_marks(spec) if m["mark"]["type"] == "rule"]
    assert len(rules) == len(expected_edges)
    for rule, (segments, widths) in zip(rules, expected_edges, strict=True):
        edges = spec["datasets"][rule["data"]["name"]]
        np.testing.assert_allclose(
            [[[r["_x"], r["_y"]], [r["_x2"], r["_y2"]]] for r in edges], segments
        )
        np.testing.assert_allclose([r["_width"] for r in edges], widths)
    np.testing.assert_allclose(
        a.uns["paga"]["pos"],
        options.get("pos", positions) if options.get("add_pos", True) else old_pos,
    )
    pd.testing.assert_frame_equal(a.obs, before)
    assert (a.uns["paga"]["connectivities"] != stored).nnz == 0


@pytest.mark.parametrize("plot", [False, True])
@pytest.mark.parametrize("add_pos", [False, True])
@pytest.mark.parametrize("format", ["csr", "csc", "lil"])
def test_layout_never_reads_expression_or_creates_a_figure(
    plot, add_pos, format, monkeypatch
):
    from anndata import AnnData
    import scanpy as sc
    import matplotlib.pyplot as plt

    a = make_paga()
    a.uns["paga"]["connectivities"] = a.uns["paga"]["connectivities"].asformat(format)
    old = a.uns["paga"]["pos"].copy()
    for name in ("X", "raw", "layers"):
        original = inspect.getattr_static(AnnData, name)

        def guarded(self, _original=original):
            if self is a:
                pytest.fail("Read caller expression")
            return _original.__get__(self, type(self))

        monkeypatch.setattr(
            AnnData,
            name,
            property(guarded, original.__set__),
        )
    monkeypatch.setattr(sc.tl, "paga", lambda *a, **k: pytest.fail("Ran PAGA analysis"))
    monkeypatch.setattr(plt, "figure", lambda *a, **k: pytest.fail("Created figure"))
    result = gsc.pl.paga(a, plot=plot, add_pos=add_pos, show=False)
    assert (result is not None) == plot
    assert np.array_equal(a.uns["paga"]["pos"], old) is not add_pos


@pytest.mark.parametrize("add_pos", [False, True])
def test_layout_only_skips_chart_options_and_respects_position_cache(
    monkeypatch, add_pos
):
    from genome_spy.integrations.scanpy import _paga_chart

    a = make_paga()
    previous = a.uns["paga"]["pos"].copy()
    monkeypatch.setattr(
        _paga_chart,
        "build_paga",
        lambda *args, **kwargs: pytest.fail("Built a layout-only chart"),
    )
    result = gsc.pl.paga(
        a,
        pos=POSITIONS,
        plot=False,
        add_pos=add_pos,
        cmap="unsupported-scheme",
        labels=["short"],
        fontsize=-1,
        node_size_scale=-1,
        show=True,
    )
    assert result is None
    np.testing.assert_array_equal(
        a.uns["paga"]["pos"], POSITIONS if add_pos else previous
    )


def test_supplied_positions_skip_layout_and_failures_leave_caches_unchanged(
    monkeypatch,
):
    import scanpy as sc

    a = make_paga()
    old = a.uns["paga"]["pos"].copy()
    monkeypatch.setattr(sc.pl, "paga", lambda *a, **k: pytest.fail("Computed layout"))
    gsc.pl.paga(a, pos=POSITIONS, add_pos=False, show=False)
    np.testing.assert_array_equal(a.uns["paga"]["pos"], old)
    with pytest.raises(ValueError, match="labels"):
        gsc.pl.paga(a, pos=POSITIONS, labels=["short"], show=False)
    np.testing.assert_array_equal(a.uns["paga"]["pos"], old)


@pytest.mark.parametrize(
    "option",
    [
        {"transitions": "velocity"},
        {"export_to_gexf": True},
        {"fontoutline": 2},
        {"text_kwds": {"color": "red"}},
        {"left_margin": 0.2},
        {"cb_kwds": {"ticks": []}},
    ],
)
def test_unsupported_options_fail_before_imports_or_writes(option, monkeypatch):
    monkeypatch.setattr(
        gsc.pl, "_require_scanpy", lambda *a: pytest.fail("Imported Scanpy")
    )
    with pytest.raises(NotImplementedError, match="gsc.pl.paga:.*unsupported"):
        gsc.pl.paga(object(), **option)


@pytest.mark.parametrize(
    "option",
    [
        {"ax": object()},
        {"cax": object()},
        {"plot": 1},
        {"add_pos": 1},
        {"zoom": "xy"},
        {"colorbar": 1},
    ],
)
def test_invalid_flags_and_axes_fail_clearly(option):
    with pytest.raises(TypeError, match="gsc.pl.paga:"):
        gsc.pl.paga(object(), **option)


@pytest.mark.parametrize(
    "change,error",
    [
        ("missing", ValueError),
        ("uncategorical", ValueError),
        ("shape", ValueError),
        ("nan", ValueError),
        ("loop", NotImplementedError),
    ],
)
def test_invalid_stored_graphs_are_not_recomputed(change, error):
    from scipy import sparse

    a = make_paga()
    if change == "missing":
        del a.uns["paga"]
    elif change == "uncategorical":
        a.obs["cluster"] = a.obs["cluster"].astype(str)
    elif change == "shape":
        a.uns["paga"]["connectivities"] = sparse.csr_matrix((3, 3))
    elif change == "nan":
        a.uns["paga"]["connectivities"].data[0] = np.nan
    elif change == "loop":
        graph = a.uns["paga"]["connectivities"].tolil()
        graph[0, 0] = 0.2
        a.uns["paga"]["connectivities"] = graph
    with pytest.raises(error, match="gsc.pl.paga:"):
        gsc.pl.paga(a, pos=POSITIONS, show=False)


@pytest.mark.parametrize("format", ["csr", "csc", "lil"])
@pytest.mark.parametrize("supplied_pos", [False, True])
@pytest.mark.parametrize("solid_edges", ["connectivities", "weak"])
def test_sparse_graph_validation_handles_storage_formats(
    format, supplied_pos, solid_edges
):
    import scanpy as sc

    a = make_paga()
    graph = a.uns["paga"][solid_edges].asformat(format)
    a.uns["paga"][solid_edges] = graph
    before = graph.copy()
    options = {"pos": POSITIONS} if supplied_pos else {}
    reference = a.copy()
    # Scanpy needs compressed storage for layout; keep the source object untouched.
    if format == "lil":
        reference.uns["paga"][solid_edges] = graph.tocsr()
    sc.pl.paga(reference, solid_edges=solid_edges, plot=False, show=False, **options)
    spec = gsc.pl.paga(a, solid_edges=solid_edges, show=False, **options).to_dict()
    mark = next(m for m in leaf_marks(spec) if m["mark"]["type"] == "point")
    rows = spec["datasets"][mark["data"]["name"]]
    np.testing.assert_allclose(
        [[r["_x"], r["_y"]] for r in rows], reference.uns["paga"]["pos"]
    )
    assert a.uns["paga"][solid_edges] is graph and graph.format == format
    assert (graph != before).nnz == 0
    graph[0, 1] = np.nan
    with pytest.raises(ValueError, match="graph weights must be finite"):
        gsc.pl.paga(a, solid_edges=solid_edges, show=False, **options)


@pytest.mark.parametrize("format", ["csr", "csc", "lil"])
def test_tree_layout_retains_the_unfiltered_source(format):
    import scanpy as sc
    from scipy.sparse.csgraph import minimum_spanning_tree

    a = make_paga()
    tree = minimum_spanning_tree(a.uns["paga"]["connectivities"])
    a.uns["paga"]["connectivities_tree"] = tree.asformat(format)
    reference = a.copy()
    reference.uns["paga"]["connectivities_tree"] = tree
    options = dict(
        solid_edges="connectivities_tree",
        layout="rt",
        threshold=0.02,
        plot=False,
        show=False,
    )
    sc.pl.paga(reference, **options)
    gsc.pl.paga(a, **options)
    np.testing.assert_allclose(a.uns["paga"]["pos"], reference.uns["paga"]["pos"])
    assert a.uns["paga"]["connectivities_tree"].format == format
    assert (a.uns["paga"]["connectivities_tree"] != tree).nnz == 0


@pytest.mark.parametrize("storage", ["csr", "csc"])
@pytest.mark.parametrize("use_raw", [True, False])
def test_gene_colors_read_one_sparse_column_without_changing_sources(
    storage, use_raw, monkeypatch
):
    from scipy import sparse
    import scanpy as sc

    a = make_paga("gene_raw")
    a.X = getattr(sparse, f"{storage}_matrix")(a.X)
    raw = a.raw.to_adata()
    raw.X = getattr(sparse, f"{storage}_matrix")(raw.X)
    a.raw = raw
    # Exercise a view while keeping the existing graph's group order and slots.
    a = a[:18]
    before = (a.X.copy(), a.raw.X.copy())
    read, dense = sc.get.obs_df, []
    reads = []

    def getter(*args, **kwargs):
        reads.append(kwargs)
        return read(*args, **kwargs)

    def toarray(self, *args, **kwargs):
        dense.append(self.shape)
        assert self.shape[1] == 1
        return original(self, *args, **kwargs)

    cls = getattr(sparse, f"{storage}_matrix")
    original = cls.toarray
    monkeypatch.setattr(cls, "toarray", toarray)
    monkeypatch.setattr(sc.get, "obs_df", getter)
    spec = gsc.pl.paga(
        a, color="g1", use_raw=use_raw, pos=POSITIONS, add_pos=False, show=False
    ).to_dict()
    assert len(reads) == 1 and reads[0]["keys"] == ["cluster", "g1"]
    assert reads[0]["use_raw"] is use_raw and dense == [(a.n_obs, 1)]
    rows = next(rows for rows in spec["datasets"].values() if "_cells" in rows[0])
    expected = np.arange(0, 54, 3, dtype=float) + (0 if use_raw else 100)
    for row in rows:
        np.testing.assert_allclose(
            row["_color"], expected[a.obs["cluster"] == row["_group"]].mean()
        )
    assert (a.X != before[0]).nnz == 0 and (a.raw.X != before[1]).nnz == 0


def test_gene_colors_fall_back_to_x_without_raw_and_keep_missing_group_labels():
    a = make_paga("gene_missing")
    a.raw = None
    spec = gsc.pl.paga(a, color="g1", pos=POSITIONS, show=False).to_dict()
    nodes = next(rows for rows in spec["datasets"].values() if "_cells" in rows[0])
    assert nodes[0]["_color"] is None
    np.testing.assert_allclose(
        [row["_color"] for row in nodes[1:]], [131.5, 139, 149.5]
    )
    marks = leaf_marks(spec)
    assert any(
        mark["encoding"].get("text", {}).get("field") == "_label" for mark in marks
    )
    point = next(mark for mark in marks if mark["mark"]["type"] == "point")
    assert "isValid(datum._color)" in point["transform"][0]["expr"]


@pytest.mark.parametrize(
    "color,options,match",
    [
        ("degree_dashed", {}, "requires dashed_edges"),
        ("degree_unknown", {}, "degree_solid.*degree_dashed"),
        ("missing", {}, "not a gene"),
        ("score", {}, "at least one finite"),
        ("degree_solid", {"threshold": 1}, "equal weighted degrees"),
    ],
)
def test_invalid_color_inputs_never_write_positions(color, options, match):
    a = make_paga("obs_score")
    a.obs["score"] = np.nan
    before = a.uns["paga"]["pos"].copy()
    with pytest.raises(ValueError, match=match):
        gsc.pl.paga(a, color=color, pos=POSITIONS, show=False, **options)
    np.testing.assert_array_equal(a.uns["paga"]["pos"], before)


@pytest.mark.parametrize("color", ["score", "degree_solid", "degree_dashed"])
def test_numeric_metadata_and_degrees_do_not_read_expression_or_draw_figures(
    color, monkeypatch
):
    from anndata import AnnData
    import matplotlib.pyplot as plt
    import scanpy as sc

    a = make_paga("obs_score")
    original = inspect.getattr_static(AnnData, "X")

    def forbidden(*args, **kwargs):
        pytest.fail("Read expression, drew a figure or reran analysis")

    monkeypatch.setattr(AnnData, "X", property(forbidden, original.__set__))
    raw = type(a.raw)
    monkeypatch.setattr(raw, "X", property(forbidden))
    monkeypatch.setattr(plt, "figure", forbidden)
    monkeypatch.setattr(sc.tl, "paga", forbidden)
    monkeypatch.setattr(sc.pl, "paga", forbidden)
    assert (
        gsc.pl.paga(a, color=color, dashed_edges="weak", pos=POSITIONS, show=False)
        is not None
    )


@pytest.mark.parametrize("color", ["red", "other_category"])
def test_unsupported_color_collisions_and_categorical_mixtures_fail_clearly(color):
    a = make_paga("obs_score")
    a.obs["other_category"] = a.obs["cluster"]
    with pytest.raises(NotImplementedError, match="gsc.pl.paga:.*unsupported"):
        gsc.pl.paga(a, color=color, pos=POSITIONS, show=False)


@pytest.mark.xfail(
    strict=True,
    raises=ValueError,
    reason="Scanpy 1.11.5 trims component colors but keeps full coordinates; recheck on an upstream fix.",
)
def test_direct_scanpy_component_entry_detects_an_upstream_fix():
    import scanpy as sc
    import matplotlib.pyplot as plt
    from matplotlib.collections import PathCollection

    a = make_paga("component")
    try:
        ax = sc.pl.paga(
            a, pos=POSITIONS, threshold=0.2, single_component=True, show=False
        )
    except ValueError as error:
        assert (
            str(error)
            == "'c' argument has 3 elements, which is inconsistent with 'x' and 'y' with size 4."
        )
        raise
    else:
        point = next(c for c in ax.collections if isinstance(c, PathCollection))
        assert len(point.get_offsets()) == 3
    finally:
        plt.close("all")


@pytest.mark.parametrize("storage", ["csr", "csc", "lil"])
@pytest.mark.parametrize("supplied", [False, True])
def test_component_preserves_ids_sources_and_full_coordinate_cache(
    storage, supplied, monkeypatch
):
    import scanpy as sc
    import matplotlib.pyplot as plt

    a = make_paga("component_score")
    matrix = a.uns["paga"]["connectivities"].asformat(storage)
    a.uns["paga"]["connectivities"] = matrix
    before = matrix.copy()
    obs = a.obs.copy(deep=True)
    reference = a.copy()
    reference.uns["paga"]["connectivities"] = matrix.tocsr()
    options = {"pos": POSITIONS} if supplied else {}
    sc.pl.paga(reference, threshold=0.2, plot=False, show=False, **options)
    monkeypatch.setattr(sc.tl, "paga", lambda *a, **k: pytest.fail("Reran PAGA"))
    monkeypatch.setattr(plt, "figure", lambda *a, **k: pytest.fail("Created figure"))
    spec = gsc.pl.paga(
        a, single_component=True, threshold=0.2, color="score", show=False, **options
    ).to_dict()
    rows = next(rows for rows in spec["datasets"].values() if "_cells" in rows[0])
    assert [r["_id"] for r in rows] == [1, 2, 3]
    assert [r["_group"] for r in rows] == ["B", "C", "D"]
    np.testing.assert_allclose(
        [[r["_x"], r["_y"]] for r in rows], reference.uns["paga"]["pos"][[1, 2, 3]]
    )
    assert a.uns["paga"]["pos"].shape == (4, 2)
    np.testing.assert_allclose(a.uns["paga"]["pos"], reference.uns["paga"]["pos"])
    assert a.uns["paga"]["connectivities"] is matrix and (matrix != before).nnz == 0
    pd.testing.assert_frame_equal(a.obs, obs)


@pytest.mark.parametrize("plot", [True, False])
def test_dashed_component_restriction_only_applies_when_plotting_a_disconnected_graph(
    plot,
):
    a = make_paga()
    kwargs = dict(
        single_component=True, dashed_edges="weak", pos=POSITIONS, show=False, plot=plot
    )
    before = a.uns["paga"]["pos"].copy()
    # Connected graphs and no-plot layout still use the ordinary public behavior.
    assert (gsc.pl.paga(a, **kwargs) is not None) is plot
    if plot:
        a.uns["paga"]["pos"] = before
        with pytest.raises(ValueError, match="single_component.*dashed_edges=None"):
            gsc.pl.paga(a, threshold=0.2, **kwargs)
        np.testing.assert_array_equal(a.uns["paga"]["pos"], before)
    else:
        assert gsc.pl.paga(a, threshold=0.2, **kwargs) is None


def test_tied_components_use_node_count_and_original_order_not_cell_counts():
    a = make_paga("component_tie")
    a.uns["cluster_sizes"] = np.array([1, 1, 100, 100])
    spec = gsc.pl.paga(a, pos=POSITIONS, single_component=True, show=False).to_dict()
    rows = next(rows for rows in spec["datasets"].values() if "_cells" in rows[0])
    assert [r["_id"] for r in rows] == [0, 1]
    assert [r["_area"] for r in rows] == pytest.approx([2000 / (np.sqrt(2) + 10)] * 2)


@pytest.mark.parametrize("palette", [None, "set1"])
def test_group_legend_uses_displayed_names_without_changing_palette_positions(palette):
    a = make_paga("component")
    spec = gsc.pl.paga(
        a,
        pos=POSITIONS,
        single_component=True,
        threshold=0.2,
        palette=palette,
        show=False,
    ).to_dict()
    mark = next(m for m in leaf_marks(spec) if m["mark"]["type"] == "point")
    fill = mark["encoding"]["fill"]
    rows = spec["datasets"][mark["data"]["name"]]
    assert fill["field"] == "_group"
    assert fill["legend"]["title"] == "cluster"
    assert fill["legend"]["values"] == [r["_group"] for r in rows] == ["B", "C", "D"]
    if palette:
        assert fill["scale"]["domain"] == ["A", "B", "C", "D"]
    else:
        assert fill["scale"]["range"] == [a.uns["cluster_colors"][i] for i in [1, 2, 3]]


@pytest.mark.parametrize("color", ["score", "g1", "degree_solid"])
@pytest.mark.parametrize("colorbar", [None, True, False])
def test_numeric_node_guides_are_native_and_can_be_hidden(color, colorbar):
    spec = gsc.pl.paga(
        make_paga("obs_score"),
        pos=POSITIONS,
        color=color,
        colorbar=colorbar,
        show=False,
    ).to_dict()
    fill = next(m for m in leaf_marks(spec) if m["mark"]["type"] == "point")[
        "encoding"
    ]["fill"]
    assert fill["field"] == "_color"
    if colorbar is False:
        assert fill["legend"] is None
    else:
        assert fill["legend"]["title"] == color
        assert fill["legend"]["titleOrient"] == "right"
        assert "gradientLength" not in fill["legend"]
        assert fill["legend"]["gradientThickness"] == 15


def test_node_legend_rejects_colliding_group_names_before_cache_write():
    a = make_paga()
    a.obs["cluster"] = a.obs["cluster"].cat.rename_categories([1, "1", "C", "D"])
    original = a.uns["paga"]["pos"].copy()
    with pytest.raises(ValueError, match="labels collide when serialized"):
        gsc.pl.paga(a, pos=POSITIONS, show=False)
    np.testing.assert_array_equal(a.uns["paga"]["pos"], original)


@pytest.mark.parametrize("fontweight", ["normal", "bold"])
def test_node_labels_use_native_measurement_and_stable_ids_without_changing_nodes(
    fontweight,
):
    a = make_paga()
    options = dict(
        pos=POSITIONS,
        labels=["Same label"] * 4,
        fontsize=12,
        fontweight=fontweight,
        add_pos=False,
        show=False,
    )
    spec = gsc.pl.paga(a, **options).to_dict()
    hidden = gsc.pl.paga(a, show_node_labels=False, **options).to_dict()
    assert spec["datasets"] == hidden["datasets"]
    labels = next(m for m in leaf_marks(spec) if m["mark"]["type"] == "text")
    measure = next(t for t in labels["transform"] if t["type"] == "measureText")
    displacement = next(t for t in labels["transform"] if t["type"] == "displace2d")
    assert displacement["key"] == "_id"
    assert displacement["x"] == "_x" and displacement["y"] == "_y"
    assert displacement["anchorWidth"] == displacement["anchorHeight"] == "_node_extent"
    assert measure["fontSize"] == labels["mark"]["size"] == pytest.approx(12 * 100 / 72)
    assert measure["fontWeight"] == labels["mark"]["fontWeight"] == fontweight
    assert labels["mark"]["baseline"] == "middle"
    assert "yOffset" not in labels["mark"]
    assert labels["encoding"]["xOffset"]["scale"] is None
    assert labels["encoding"]["yOffset"]["scale"] is None
    assert not any(m["mark"]["type"] == "text" for m in leaf_marks(hidden))
    np.testing.assert_array_equal(a.uns["paga"]["pos"], make_paga().uns["paga"]["pos"])
