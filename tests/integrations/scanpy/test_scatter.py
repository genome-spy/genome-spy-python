"""Scatter semantics independently exercise the existing native point pipeline."""

from copy import deepcopy
from hashlib import sha256
import inspect
import json
from pathlib import Path

import numpy as np
import pandas as pd
import pytest
from scipy import sparse

import genome_spy.integrations.scanpy as gsc
from tests.integrations.scanpy.helpers import points, units
from tests.integrations.scanpy.scatter_fixture import make_scatter_adata, scatter_cases

sc = pytest.importorskip("scanpy")


def records(spec):
    """Return the one shared table for a native scatter chart."""
    assert len(spec["datasets"]) == 1
    return next(iter(spec["datasets"].values()))


@pytest.mark.parametrize(
    "family,linked", [("scatter", False), ("umap", False), ("umap", True)]
)
def test_native_legend_configuration_overrides_shared_defaults_without_changing_points(
    family, linked
):
    import genome_spy as gs
    from genome_spy.integrations.scanpy._style import POINTS_TO_PIXELS

    options = {"basis": "umap"} if family == "scatter" else {}
    if linked:
        options["selection"] = gs.selection_interval("cells", encodings=["x", "y"])
    default = getattr(gsc.pl, family)(
        make_scatter_adata(), color=["cell_type", "score"], show=False, **options
    )
    compact = default.resolve_legend(default="collected").configure_legend(
        orient="bottom",
        direction="horizontal",
        columns=4,
        symbolSize=64,
        gradientLength=140,
    )
    original, updated = default.to_dict(), compact.to_dict()
    assert (
        original["config"]["legend"]["symbolSize"]
        == (300 if family == "scatter" else 36) * POINTS_TO_PIXELS**2
    )
    assert original["config"]["legend"]["orient"] == "right"
    assert updated["config"]["legend"]["symbolSize"] == 64
    assert updated["config"]["legend"]["orient"] == "bottom"
    assert updated["config"]["legend"]["gradientLength"] == 140
    assert updated["resolve"]["legend"] == {"default": "collected"}
    assert updated["datasets"] == original["datasets"]
    assert units(updated) == units(original)
    plot = units(updated["vconcat"][0]) if linked else units(updated)
    assert all(
        "orient" not in points(panel)["encoding"]["color"]["legend"] for panel in plot
    )
    assert "columns" not in points(plot[0])["encoding"]["color"]["legend"]


def test_many_categories_keep_scanpy_column_defaults():
    a = make_scatter_adata()
    a.obs["many"] = pd.Categorical(range(a.n_obs), categories=range(31))
    spec = gsc.pl.scatter(a, "x_value", "y_value", color="many", show=False).to_dict()
    assert spec["encoding"]["color"]["legend"]["columns"] == 3


@pytest.mark.parametrize("family", ["umap", "scatter"])
@pytest.mark.parametrize(
    "marker,shapes,factors",
    [
        ("s", ["square", "square"], [1, 1]),
        (["o", "s"], ["circle", "square"], [1, 1]),
        ("D", ["diamond", "diamond"], [2, 2]),
        (["s", "D"], ["square", "diamond"], [1, 2]),
    ],
)
def test_marker_shapes_reuse_embedding_data_and_units(family, marker, shapes, factors):
    data = make_scatter_adata()
    args = (data, "x_value", "y_value") if family == "scatter" else (data,)
    options = dict(color=["cell_type", "score"], show=False)
    plot = getattr(gsc.pl, family)
    plain = plot(*args, marker="o", **options).to_dict()
    marked = plot(*args, marker=marker, **options).to_dict()
    assert marked["datasets"] == plain["datasets"]
    assert "symbolType" not in marked["config"]["legend"]
    for panel, normal, shape, factor in zip(
        units(marked), units(plain), shapes, factors, strict=True
    ):
        encoding = points(panel)["encoding"]
        assert encoding.get("shape", {"value": "circle"}) == {"value": shape}
        original = points(normal)["encoding"]["size"]["scale"]
        assert encoding["size"]["scale"]["domain"] == original["domain"]
        np.testing.assert_allclose(
            encoding["size"]["scale"]["range"], np.array(original["range"]) * factor
        )


@pytest.mark.parametrize("family", ["umap", "scatter"])
@pytest.mark.parametrize("marker", ["o", "s", "D"])
def test_category_legends_follow_panel_markers_in_native_units(family, marker):
    import matplotlib.pyplot as plt
    from matplotlib.markers import MarkerStyle

    data = make_scatter_adata()
    args = (data, "x_value", "y_value") if family == "scatter" else (data,)
    options = dict(color="cell_type", marker=marker, show=False)
    ax = getattr(sc.pl, family)(*args, **options)
    handle = ax.get_legend().legend_handles[0]
    # Embedding keys deliberately follow the points instead of Scanpy's circles.
    reference_marker = MarkerStyle(marker)
    path = (
        reference_marker.get_path().transformed(reference_marker.get_transform())
        if family == "umap"
        else handle.get_paths()[0]
    )
    width = path.get_extents().width
    expected_width = np.sqrt(handle.get_sizes()[0]) * width * 100 / 72
    plt.close(ax.figure)

    spec = getattr(gsc.pl, family)(*args, **options).to_dict()
    mark = points(spec)
    guide = mark["encoding"]["color"]["legend"]
    config = spec["config"]["legend"]
    shape = config.get(
        "symbolType", mark["encoding"].get("shape", {}).get("value", "circle")
    )
    native_marker = MarkerStyle({"circle": "o", "square": "s", "diamond": "D"}[shape])
    native_path = native_marker.get_path().transformed(native_marker.get_transform())
    np.testing.assert_allclose(
        native_path.vertices / native_path.get_extents().width,
        path.vertices / width,
        atol=1e-15,
    )
    np.testing.assert_allclose(
        np.sqrt(guide.get("symbolSize", config["symbolSize"])), expected_width
    )


def test_signature_preserves_scatter_defaults_and_adds_only_native_controls():
    actual = inspect.signature(gsc.pl.scatter).parameters
    upstream = inspect.signature(sc.pl.scatter).parameters
    for name, parameter in upstream.items():
        if name == "ax":
            assert name not in actual
        else:
            assert actual[name].default == parameter.default
            assert actual[name].kind == parameter.kind
    assert set(actual) - set(upstream) == {"hover", "zoom", "width", "height"}
    assert all(
        actual[name].kind == inspect.Parameter.KEYWORD_ONLY
        for name in set(actual) - set(upstream)
    )


@pytest.mark.parametrize("case", scatter_cases())
def test_complete_chart_matches_frozen_upstream_points_labels_palettes_and_limits(case):
    from matplotlib.colors import to_hex

    manifest = json.loads(
        (Path(__file__).with_name("fixtures") / "scatter.json").read_text()
    )
    assert (
        manifest["input_sha256"]
        == sha256(
            Path(__file__).with_name("scatter_fixture.py").read_bytes()
        ).hexdigest()
    )
    expected = manifest["cases"][case]
    spec = gsc.pl.scatter(
        make_scatter_adata(), **scatter_cases()[case], size=80, frameon=True, show=False
    ).to_dict()
    mark = points(spec)
    rows = sorted(records(spec), key=lambda r: r["_order_0"])
    if not expected["categorical"]:
        rows = [r for r in rows if r["_value_0"] is not None]
    coordinates = [[r["_coord_0"], r["_coord_1"]] for r in rows]
    if expected["categorical"]:
        np.testing.assert_array_equal(coordinates, expected["coordinates"])
    else:
        import matplotlib.pyplot as plt

        # Scanpy's draw order for tied colors depends on the local NumPy sort.
        options = scatter_cases()[case].copy()
        if "layers" in options:
            # New AnnData uses None for X instead of the legacy "X" layer alias.
            options["layers"] = tuple(
                None if v == "X" else v for v in options["layers"]
            )
        axis = sc.pl.scatter(
            make_scatter_adata(),
            **options,
            size=80,
            frameon=True,
            show=False,
        )
        try:
            artist = axis.collections[-1]
            offsets = artist.get_offsets()
            valid = ~np.ma.getmaskarray(offsets).any(axis=1)
            np.testing.assert_array_equal(coordinates, np.asarray(offsets)[valid])
            np.testing.assert_array_equal(
                [r["_value_0"] for r in rows], np.asarray(artist.get_array())[valid]
            )
        finally:
            plt.close(axis.figure)
        np.testing.assert_array_equal(
            sorted(coordinates), sorted(expected["coordinates"])
        )
    assert all(r["_size_0"] == 80 for r in rows)
    assert [mark["encoding"][axis]["axis"]["title"] for axis in ("x", "y")] == expected[
        "labels"
    ]
    assert spec.get("title", {}).get("text", "") == expected["title"]
    for axis in ("x", "y"):
        np.testing.assert_allclose(
            mark["encoding"][axis]["scale"]["domain"], expected[f"{axis}_domain"]
        )
    color = mark["encoding"]["color"]
    if expected["categorical"]:
        paints = dict(
            zip(color["scale"]["domain"], color["scale"]["range"], strict=True)
        )
        assert [
            to_hex(paints[r["_color_0"]], keep_alpha=True) for r in rows
        ] == expected["colors"]
        if color["legend"] is not None:
            assert color["legend"]["values"] == expected["legend"]
    else:
        assert color["scale"]["domain"] == expected["color_domain"]


def test_native_color_names_match_css_and_reject_invalid_names_and_hex():
    from matplotlib.colors import CSS4_COLORS
    from genome_spy.integrations.scanpy._style import _CSS_NAMES, native_color

    assert _CSS_NAMES == CSS4_COLORS.keys()
    assert native_color("RebeccaPurple", "color") == "RebeccaPurple"
    for value in [
        "no_such_color",
        "notacolor",
        "#xyz",
        "#12345z",
        "transparent",
        "r",
        (1, 0, 0),
    ]:
        with pytest.raises(NotImplementedError, match="CSS color"):
            native_color(value, "color")


def test_raw_default_and_three_layers_preserve_selected_vectors_without_mutation():
    a = make_scatter_adata()
    before = deepcopy(a.uns), a.obs.copy(), a.var.copy(), a.X.copy()
    raw = records(gsc.pl.scatter(a, "g1", "g2", color="raw_only", show=False).to_dict())
    np.testing.assert_array_equal([r["_coord_0"] for r in raw], a.raw.obs_vector("g1"))
    np.testing.assert_array_equal([r["_coord_1"] for r in raw], a.raw.obs_vector("g2"))
    np.testing.assert_array_equal(
        [r["_value_0"] for r in raw], a.raw.obs_vector("raw_only")
    )
    layered = records(
        gsc.pl.scatter(
            a,
            "g1",
            "g2",
            color="g1",
            layers=("counts", "X", "X"),
            use_raw=False,
            show=False,
        ).to_dict()
    )
    np.testing.assert_array_equal(
        [r["_coord_0"] for r in layered], a.obs_vector("g1", layer="counts")
    )
    np.testing.assert_array_equal([r["_coord_1"] for r in layered], a.obs_vector("g2"))
    np.testing.assert_array_equal([r["_value_0"] for r in layered], a.obs_vector("g1"))
    pd.testing.assert_frame_equal(a.obs, before[1])
    pd.testing.assert_frame_equal(a.var, before[2])
    np.testing.assert_array_equal(a.X, before[3])
    for key in ("cell_type_colors", "gene_group_colors"):
        assert a.uns[key] == before[0][key]


def test_variables_use_public_row_vectors_without_transposing_or_copying_expression(
    monkeypatch,
):
    a = make_scatter_adata()
    getter, calls = type(a).var_vector, []

    def read(owner, key, *, layer=None):
        calls.append((key, layer))
        return getter(owner, key, layer=layer)

    monkeypatch.setattr(type(a), "var_vector", read)
    monkeypatch.setattr(
        type(a), "transpose", lambda *a: pytest.fail("Transposed the full AnnData")
    )
    spec = gsc.pl.scatter(
        a, "c1", "c3", color=["c1", "c4"], use_raw=False, layers="counts", show=False
    ).to_dict()
    assert calls == [("c1", "counts"), ("c3", "counts"), ("c4", "counts")]
    rows = records(spec)
    assert [r["_obs_id"] for r in rows] == list(a.var_names)
    np.testing.assert_array_equal([r["_coord_0"] for r in rows], a.layers["counts"][1])
    for panel in units(spec):
        assert [v["title"] for v in points(panel)["encoding"]["tooltip"][:2]] == [
            "Variable ID",
            "Variable",
        ]


@pytest.mark.parametrize("matrix_type", [sparse.csr_matrix, sparse.csc_matrix])
@pytest.mark.parametrize("axis", ["obs", "var"])
def test_sparse_and_views_only_densify_selected_vectors_and_read_repeated_fields_once(
    monkeypatch, matrix_type, axis
):
    a = make_scatter_adata()
    a.X = matrix_type(a.X)
    a = a[[5, 0, 4, 7], :]
    method, shapes = matrix_type.toarray, []

    def densify(value, *args, **kwargs):
        shapes.append(value.shape)
        return method(value, *args, **kwargs)

    monkeypatch.setattr(matrix_type, "toarray", densify)
    x, y = ("g1", "g2") if axis == "obs" else ("c5", "c4")
    spec = gsc.pl.scatter(a, x, y, color=[x, x], use_raw=False, show=False).to_dict()
    assert shapes == ([(4, 1), (4, 1)] if axis == "obs" else [(1, 3), (1, 3)])
    assert [r["_obs_label"] for r in records(spec)] == list(
        a.obs_names if axis == "obs" else a.var_names
    )
    assert len(units(spec)) == 2 and a.is_view


def test_variable_layer_default_ignores_raw_as_scanpy_transpose_does():
    a = make_scatter_adata()
    spec = gsc.pl.scatter(
        a, "c1", "c3", color="c1", layers="counts", show=False
    ).to_dict()
    rows = records(spec)
    np.testing.assert_array_equal([r["_coord_0"] for r in rows], a.layers["counts"][1])
    np.testing.assert_array_equal([r["_value_0"] for r in rows], a.layers["counts"][1])
    assert len(rows) == a.n_vars


def test_palettes_follow_categorical_panels_and_reject_upstream_flat_list_truncation():
    a = make_scatter_adata()
    spec = gsc.pl.scatter(
        a,
        "x_value",
        "y_value",
        color=["score", "cell_type"],
        palette=[["red", "blue", "green", "gray"]],
        show=False,
    ).to_dict()
    categorical = points(units(spec)[1])["encoding"]["color"]
    assert categorical["scale"]["range"] == [
        "red",
        "blue",
        "green",
        "gray",
        "lightgrey",
    ]
    with pytest.raises(NotImplementedError, match="nested palettes"):
        gsc.pl.scatter(
            a,
            "x_value",
            "y_value",
            color=["cell_type", "cell_type"],
            palette=["red", "blue", "green", "gray"],
            show=False,
        )


def test_scatter_basis_is_exact_X_key_and_diffmap_skips_first_column():
    a = make_scatter_adata()
    a.obsm["diffmap"] = a.obsm["X_diffmap"] * 50
    spec = gsc.pl.scatter(a, basis="diffmap", show=False).to_dict()
    np.testing.assert_array_equal(
        [[r["_coord_0"], r["_coord_1"]] for r in records(spec)],
        a.obsm["X_diffmap"][:, [1, 2]],
    )
    assert [spec["encoding"][axis]["axis"]["title"] for axis in ("x", "y")] == [
        "DC1",
        "DC2",
    ]
    del a.obsm["X_diffmap"]
    with pytest.raises(ValueError, match="X_diffmap"):
        gsc.pl.scatter(a, basis="diffmap", show=False)


def test_category_order_groups_missing_and_per_panel_palettes_stay_consistent():
    a = make_scatter_adata()
    spec = gsc.pl.scatter(
        a,
        "x_value",
        "y_value",
        color=["cell_type", "cell_type"],
        groups=["A", "B"],
        palette=[
            ["red", "blue", "green", "gray"],
            ["purple", "orange", "navy", "gray"],
        ],
        show=False,
    ).to_dict()
    for index, panel in enumerate(units(spec)):
        color = points(panel)["encoding"]["color"]
        assert color["legend"]["values"] == ["A", "B"]
        assert color["scale"]["domain"] == ["B", "A", "NA"]
        expected = (
            ["blue", "green", "lightgrey"]
            if index == 0
            else ["orange", "navy", "lightgrey"]
        )
        assert color["scale"]["range"] == expected
        order = sorted(records(spec), key=lambda r: r[f"_order_{index}"])
        assert [r[f"_color_{index}"] for r in order] == [
            "NA",
            "NA",
            "NA",
            "A",
            "A",
            "B",
            "B",
            "B",
        ]


def test_scatter_keeps_pinned_numeric_sort_flag_behavior_and_filters_missing_colors():
    a = make_scatter_adata()
    spec = gsc.pl.scatter(
        a, "x_value", "y_value", color="score", sort_order=False, show=False
    ).to_dict()
    rows = sorted(records(spec), key=lambda r: r["_order_0"])
    assert [r["_obs_label"] for r in rows] == list(
        a.obs_names[np.argsort(a.obs["score"].to_numpy())]
    )
    assert spec["transform"][-1] == {
        "type": "filter",
        "expr": "isValid(datum._value_0)",
    }
    assert "layer" not in spec
    assert spec["encoding"]["x"]["axis"]["labels"] is True
    assert spec["title"]["text"] == "score"


def test_missing_numeric_color_does_not_expand_coordinate_limits():
    a = make_scatter_adata()
    a.obs.loc["c4", "x_value"] = 100000
    a.obs.loc["c4", "score"] = np.nan
    spec = gsc.pl.scatter(a, "x_value", "y_value", color="score", show=False).to_dict()
    np.testing.assert_allclose(spec["encoding"]["x"]["scale"]["domain"], [-1.15, 2.15])
    assert len(records(spec)) == a.n_obs
    assert spec["transform"][-1]["expr"] == "isValid(datum._value_0)"


def test_duplicate_names_get_distinct_point_ids_without_changing_display_labels():
    a = make_scatter_adata()
    rows = records(gsc.pl.scatter(a, "x_value", "y_value", show=False).to_dict())
    assert len({r["_obs_id"] for r in rows}) == a.n_obs
    assert [r["_obs_label"] for r in rows] == list(a.obs_names)


def test_plotting_calls_no_analysis_or_scanpy_plotting(monkeypatch):
    a = make_scatter_adata()
    for module, name in [
        (sc.pl, "scatter"),
        (sc.pl, "embedding"),
        (sc.tl, "pca"),
        (sc.tl, "umap"),
        (sc.tl, "tsne"),
        (sc.pp, "neighbors"),
    ]:
        monkeypatch.setattr(
            module,
            name,
            lambda *a, **kw: pytest.fail("Ran upstream plotting or analysis"),
        )
    for options in scatter_cases().values():
        assert gsc.pl.scatter(a, **options, show=False) is not None


@pytest.mark.parametrize(
    "options,error,match",
    [
        ({}, ValueError, "x and y"),
        ({"x": "x_value", "y": "dispersion"}, ValueError, "observations.*variables"),
        ({"color": "missing_annotation"}, ValueError, "observations.*variables"),
        ({"color": "notacolor"}, ValueError, "observations.*variables"),
        ({"layers": "counts"}, ValueError, "use_raw"),
        ({"layers": ["X", None]}, ValueError, "layers"),
        ({"layers": "missing"}, ValueError, "layers"),
        ({"groups": "unknown", "color": "cell_type"}, ValueError, "groups"),
        ({"size": [10] * 8}, NotImplementedError, "scalar"),
        ({"marker": "^"}, NotImplementedError, "marker"),
        ({"marker": "v"}, NotImplementedError, "marker"),
        ({"marker": "<"}, NotImplementedError, "marker"),
        ({"marker": ">"}, NotImplementedError, "marker"),
        ({"basis": "umap", "components": "1,5"}, ValueError, "components"),
        ({"projection": "3d"}, NotImplementedError, "projection"),
        ({"right_margin": 0.5}, NotImplementedError, "right_margin"),
        ({"left_margin": 0.1}, NotImplementedError, "left_margin"),
        ({"legend_loc": "on data"}, NotImplementedError, "legend_loc"),
        ({"legend_fontoutline": 1}, NotImplementedError, "legend_fontoutline"),
        ({"color": (1, 0, 0)}, TypeError, "CSS color"),
        ({"color_map": object(), "color": "g1"}, NotImplementedError, "scheme"),
    ],
)
def test_invalid_and_unsupported_cases_fail_clearly(options, error, match):
    args = {"x": "x_value", "y": "y_value", "show": False} | options
    if not options:
        args.pop("x")
    with pytest.raises(error, match=match):
        gsc.pl.scatter(make_scatter_adata(), **args)


@pytest.mark.parametrize(
    "options",
    [
        {"ax": None},
        {"return_fig": True},
        {"cmap": "viridis"},
        {"layer": "counts"},
        {"gene_symbols": "symbol"},
    ],
)
def test_omitted_and_unknown_options_are_not_silently_ignored(options):
    with pytest.raises(TypeError, match=next(iter(options))):
        gsc.pl.scatter(object(), **options)


@pytest.mark.parametrize("value", [float("nan"), float("inf"), -float("inf")])
def test_nonfinite_axis_values_fail_before_rendering(value):
    a = make_scatter_adata()
    a.obs.loc["c1", "x_value"] = value
    with pytest.raises(ValueError, match="finite"):
        gsc.pl.scatter(a, "x_value", "y_value", show=False)


def test_backed_metadata_is_supported_but_backed_expression_fails_early(tmp_path):
    import anndata as ad

    path = tmp_path / "scatter.h5ad"
    make_scatter_adata().write_h5ad(path)
    a = ad.read_h5ad(path, backed="r")
    try:
        assert (
            gsc.pl.scatter(a, "x_value", "y_value", color="cell_type", show=False)
            is not None
        )
        assert (
            gsc.pl.scatter(
                a, "mean_value", "dispersion", color="gene_group", show=False
            )
            is not None
        )
        with pytest.raises(TypeError, match="backed"):
            gsc.pl.scatter(a, "g1", "g2", show=False)
        with pytest.raises(TypeError, match="backed"):
            gsc.pl.scatter(a, "c1", "c3", use_raw=False, show=False)
    finally:
        a.file.close()
