"""Independent semantic and pinned-reference tests for UMAP."""

from copy import deepcopy
from io import BytesIO
import json
from pathlib import Path

import numpy as np
import pandas as pd
import pytest
from scipy import sparse

import genome_spy as gs
import genome_spy.scanpy as gsc
from tests.scanpy_fixtures import make_adata, reference_cases

sc = pytest.importorskip("scanpy")
mpl = pytest.importorskip("matplotlib")
REFERENCE = json.loads(
    (Path(__file__).with_name("fixtures") / "scanpy/umap.json").read_text()
)


@pytest.fixture
def adata():
    with pytest.warns(UserWarning, match="Observation names are not unique"):
        return make_adata()


def units(spec):
    for composition in ("concat", "hconcat", "vconcat"):
        if composition in spec:
            return [unit for child in spec[composition] for unit in units(child)]
    return [spec]


def rows(chart):
    spec = chart.to_dict()
    assert len(spec["datasets"]) == 1
    return next(iter(spec["datasets"].values()))


@pytest.mark.parametrize("case", reference_cases())
def test_complete_specs_match_frozen_reference_data_and_domains(adata, case):
    with mpl.rc_context({"figure.figsize": (3, 3), "figure.dpi": 100}):
        chart = gsc.pl.umap(
            adata, **reference_cases()[case], size=np.arange(8) * 7 + 25, show=False
        )
    spec = chart.to_dict()
    data = rows(chart)
    for i, (unit, expected) in enumerate(
        zip(units(spec), REFERENCE["cases"][case]["panels"], strict=True)
    ):
        encoding = unit.get("layer", [unit])[0]["encoding"]
        ordered = sorted(data, key=lambda r: r[f"_order_{i}"])
        assert [int(r["_obs_id"].removeprefix("row-")) for r in ordered] == expected[
            "order"
        ]
        np.testing.assert_array_equal(
            [[r["_coord_0"], r["_coord_1"]] for r in ordered], expected["coordinates"]
        )
        assert [r[f"_paint_{i}"] for r in ordered] == expected["colors"]
        np.testing.assert_allclose(
            [r[f"_size_{i}"] for r in ordered],
            np.array(expected["sizes"]) * (100 / 72 * 0.5) ** 2,
        )
        for coordinate in ["x", "y"]:
            np.testing.assert_allclose(
                encoding[coordinate]["scale"]["domain"],
                expected[f"{coordinate}_domain"],
            )
            assert (encoding[coordinate]["axis"] is not None) == expected["frameon"]
        np.testing.assert_allclose(
            [
                unit.get("layer", [unit])[0]["width"],
                unit.get("layer", [unit])[0]["height"],
            ],
            expected["plot_size"],
        )
        assert unit["title"]["text"] == expected["title"]
        if expected["legend"] is not None:
            assert (
                unit["layer"][1]["encoding"]["color"]["legend"]["values"]
                == expected["legend"]
            )
        if expected["color_domain"] is not None:
            assert (
                unit["layer"][1]["encoding"]["color"]["scale"]["domain"]
                == expected["color_domain"]
            )


def test_ties_and_duplicate_coordinates_keep_distinct_observations(adata):
    data = rows(gsc.pl.umap(adata, color="score", show=False))
    assert [r["_obs_id"] for r in sorted(data, key=lambda r: r["_order_0"])] == [
        f"row-{i}" for i in [2, 5, 6, 0, 3, 1, 7, 4]
    ]
    assert data[0]["_obs_label"] == data[2]["_obs_label"] == "duplicate"
    assert data[0]["_obs_id"] != data[2]["_obs_id"]
    assert data[0]["_value_0"] == 0 and data[2]["_value_0"] is None


@pytest.mark.parametrize(
    "options,expected",
    [
        ({"color": "g1"}, [i % 4 for i in range(8)]),
        ({"color": "g1", "use_raw": False}, [i % 3 for i in range(8)]),
        ({"color": "g1", "layer": "counts"}, [10 * (i % 3) for i in range(8)]),
        ({"color": "raw_only"}, list(range(20, 28))),
        ({"color": "G1", "gene_symbols": "symbol"}, [i % 4 for i in range(8)]),
    ],
)
def test_expression_source_and_embedding_symbol_lookup(adata, options, expected):
    assert [
        r["_value_0"] for r in rows(gsc.pl.umap(adata, **options, show=False))
    ] == expected


@pytest.mark.parametrize(
    "kind", [sparse.csr_matrix, sparse.csc_matrix, sparse.csr_array, sparse.csc_array]
)
@pytest.mark.parametrize("view", [False, True])
def test_sparse_expression_densifies_only_selected_columns(
    adata, monkeypatch, kind, view
):
    adata.X = kind(adata.X)
    source = adata[[7, 0, 3], :] if view else adata
    original = kind.toarray
    shapes = []

    def selected_only(self, *args, **kwargs):
        shapes.append(self.shape)
        assert self.shape == (len(source), 1)
        return original(self, *args, **kwargs)

    monkeypatch.setattr(kind, "toarray", selected_only)
    data = rows(gsc.pl.umap(source, color=["g1", "g1"], use_raw=False, show=False))
    assert [r["_value_0"] for r in data] == (
        [1, 0, 0] if view else [i % 3 for i in range(8)]
    )
    assert shapes == [(len(source), 1)]


def test_observation_colors_never_read_expression(adata, monkeypatch):
    def forbidden(self):
        pytest.fail("Observation plot accessed expression")

    monkeypatch.setattr(type(adata), "X", property(forbidden))
    monkeypatch.setattr(type(adata.raw), "X", property(forbidden))
    assert len(rows(gsc.pl.umap(adata, color="cell_type", show=False))) == 8


@pytest.mark.parametrize(
    "options",
    [{"color": "cell_type", "groups": ["B"]}, {"color": "score", "mask_obs": "keep"}],
)
def test_groups_and_masks_recolor_instead_of_filtering(adata, options):
    data = rows(gsc.pl.umap(adata, **options, show=False))
    assert len(data) == 8
    keep = (
        adata.obs.cell_type.eq("B").to_numpy()
        if "groups" in options
        else adata.obs.keep.to_numpy() & adata.obs.score.notna().to_numpy()
    )
    assert [r["_value_0"] is not None for r in data] == keep.tolist()
    assert {
        r["_paint_0"] for r, retained in zip(data, keep, strict=True) if not retained
    } == {"#d3d3d3ff"}


def test_plotting_does_not_mutate_or_run_analysis(adata, monkeypatch):
    original = adata.copy()
    uns = deepcopy(adata.uns)
    for module, name in [
        (sc.tl, "umap"),
        (sc.tl, "rank_genes_groups"),
        (sc.tl, "dendrogram"),
        (sc.pl, "umap"),
        (sc.pp, "pca"),
    ]:
        monkeypatch.setattr(
            module,
            name,
            lambda *a, **k: pytest.fail(
                "Plotting ran analysis or an upstream plotting function"
            ),
        )
    monkeypatch.setattr(
        mpl.pyplot,
        "figure",
        lambda *a, **k: pytest.fail("Production constructed an artist"),
    )
    chart = gsc.pl.umap(adata, color=["cell_type", "g1"], palette="Set1", show=False)
    frozen = rows(chart)
    pd.testing.assert_frame_equal(adata.obs, original.obs)
    np.testing.assert_array_equal(adata.X, original.X)
    np.testing.assert_array_equal(adata.raw.X, original.raw.X)
    assert adata.uns == uns
    adata.X[:] = -100
    adata.obsm["X_umap"][:] = -100
    adata.obs["cell_type"] = "changed"
    assert rows(chart) == frozen


def test_arrow_and_json_share_detached_records(adata):
    pa = pytest.importorskip("pyarrow")
    chart = gsc.pl.umap(
        adata, color=["cell_type", "score"], obs_id="cell_id", show=False
    )
    prepared = chart._prepare_render()
    assert len(prepared.buffers) == 1
    table = pa.ipc.open_file(BytesIO(next(iter(prepared.buffers.values())))).read_all()
    assert table.to_pylist() == rows(chart)
    assert table.column("_obs_id").to_pylist() == adata.obs.cell_id.tolist()


@pytest.mark.parametrize(
    "options,message",
    [
        ({"use_raw": True, "layer": "counts"}, "incompatible"),
        ({"color": "missing"}, "missing or ambiguous"),
        ({"color": "g1", "layer": "missing"}, "layer"),
        ({"mask_obs": [True]}, "boolean vector"),
        ({"size": [-1] * 8}, "nonnegative"),
        ({"size": [1]}, "one per observation"),
        ({"dimensions": (0, 9)}, "components"),
        ({"components": "1,2", "dimensions": (0, 1)}, "mutually exclusive"),
        ({"obs_id": "cell_type"}, "unique and nonmissing"),
        ({"color": "score", "vmin": 8, "vmax": 0}, "vmin"),
    ],
)
def test_invalid_data_errors_are_contextual(adata, options, message):
    with pytest.raises((ValueError, TypeError), match=message):
        gsc.pl.umap(adata, **options, show=False)


@pytest.mark.parametrize("marker,factor", [(".", 0.25), ("o", 1)])
def test_sizes_include_physical_units_and_marker_path(adata, marker, factor):
    with mpl.rc_context({"figure.dpi": 150}):
        data = rows(gsc.pl.umap(adata, color="score", s=144, marker=marker, show=False))
    assert [r["_size_0"] for r in data] == pytest.approx(
        [144 * (150 / 72) ** 2 * factor] * 8
    )


def test_show_obeys_autoshow_and_displays_once(adata, monkeypatch):
    displayed = []
    monkeypatch.setattr(gs.TopLevelSpec, "display", lambda self: displayed.append(self))
    monkeypatch.setattr(sc.settings, "_autoshow", True)
    assert gsc.pl.umap(adata) is None
    assert len(displayed) == 1
    assert isinstance(gsc.pl.umap(adata, show=False), gs.TopLevelSpec)
    assert len(displayed) == 1


def test_backed_metadata_and_resident_embedding_work(adata, tmp_path, monkeypatch):
    import anndata as ad

    path = tmp_path / "test.h5ad"
    adata.write_h5ad(path)
    backed = ad.read_h5ad(path, backed="r")
    try:

        def forbidden(self):
            pytest.fail("Plotting accessed backed expression before rejecting it")

        monkeypatch.setattr(type(backed), "X", property(forbidden))
        monkeypatch.setattr(type(backed.raw), "X", property(forbidden))
        assert len(rows(gsc.pl.umap(backed, color="cell_type", show=False))) == 8
        for use_raw in [False, True]:
            with pytest.raises(TypeError, match="backed/lazy"):
                gsc.pl.umap(backed[[7, 0, 3]], color="g1", use_raw=use_raw, show=False)
    finally:
        backed.file.close()


@pytest.mark.parametrize(
    "options,count",
    [
        ({"components": "all"}, 3),
        ({"color": ["score", "g1"], "components": ["1,2", "2,3"]}, 4),
        ({"color": ["score", "g1"], "dimensions": [(0, 1), (1, 2)]}, 2),
    ],
)
def test_component_products_and_dimension_broadcasting(adata, options, count):
    chart = gsc.pl.umap(adata, **options, show=False)
    assert len(units(chart.to_dict())) == count
    assert len(rows(chart)) == len(adata)


def test_custom_palette_keeps_unused_order_and_masks(adata):
    palette = {"C": "purple", "B": "orange", "A": "cyan", "unused": "black"}
    chart = gsc.pl.umap(
        adata, color="cell_type", palette=palette, groups=["A", "C"], show=False
    )
    unit = units(chart.to_dict())[0]
    guide = unit["layer"][1]["encoding"]["color"]
    assert guide["scale"]["domain"] == ["C", "A", "NA"]
    assert guide["scale"]["range"] == ["#800080", "#00ffff", "#d3d3d3"]
    assert rows(chart)[0]["_value_0"] is None
    assert adata.uns["cell_type_colors"] == ["#ff0000", "#00aa00", "#0000ff", "#888888"]


def test_hover_opt_out_keeps_point_style_and_disables_picking(adata):
    chart = gsc.pl.umap(
        adata,
        color="score",
        size=0,
        hover=False,
        alpha=0.25,
        edgecolor="red",
        linewidth=2,
        show=False,
    )
    unit = units(chart.to_dict())[0]["layer"][0]
    assert unit["mark"]["tooltip"] is None
    assert unit["mark"]["filled"] is True
    assert unit["mark"]["stroke"] == "#ff0000"
    assert unit["mark"]["strokeOpacity"] == 0.25
    assert "tooltip" not in unit["encoding"]
    assert unit["encoding"]["x"]["scale"]["zoom"] is False
    assert {r["_opacity_0"] for r in rows(chart)} == {0.25}
    assert {r["_size_0"] for r in rows(chart)} == {0}


def test_palette_alpha_has_an_explicit_native_opacity_channel(adata):
    chart = gsc.pl.umap(
        adata,
        color="cell_type",
        palette=[(1, 0, 0, 0.5)] * 4,
        legend_loc=None,
        show=False,
    )
    assert rows(chart)[0]["_opacity_0"] == pytest.approx(128 / 255)
    root = units(chart.to_dict())[0]
    unit = root.get("layer", [root])[0]
    assert unit["encoding"]["fill"]["scale"]["range"][0] == "#ff0000"
    assert unit["mark"]["strokeOpacity"] == 0


def test_on_data_labels_use_semantic_medians(adata):
    chart = gsc.pl.umap(
        adata,
        color="cell_type",
        legend_loc="on data",
        legend_fontweight="normal",
        show=False,
    )
    spec = chart.to_dict()
    labels = next(
        values for values in spec["datasets"].values() if "label" in values[0]
    )
    assert [r["label"] for r in labels] == ["C", "B", "A", "NA"]
    assert labels[1] == {"label": "B", "x": 0.5, "y": -1.0}


def test_missing_numeric_colors_and_ambiguous_genes_fail(adata):
    adata.obs["score"] = np.nan
    with pytest.raises(ValueError, match="at least one nonmissing"):
        gsc.pl.umap(adata, color="score", show=False)
    adata.var_names = ["g1", "g1", "junk"]
    with pytest.raises(ValueError, match="ambiguous"):
        gsc.pl.umap(adata, color="g1", use_raw=False, show=False)


@pytest.mark.parametrize(
    "dimensions", [{"width": 300}, {"height": 240}, {"width": 300, "height": 240}]
)
def test_native_dimensions_override_panel_areas_without_changing_data_or_settings(
    adata, dimensions
):
    before = (list(mpl.rcParams["figure.figsize"]), mpl.rcParams["figure.dpi"])
    default = gsc.pl.umap(adata, color=["cell_type", "score"], size=60, show=False)
    resized = gsc.pl.umap(
        adata, color=["cell_type", "score"], size=60, show=False, **dimensions
    )
    assert rows(resized) == rows(default)
    for original, panel in zip(
        units(default.to_dict()), units(resized.to_dict()), strict=True
    ):
        for name in ("width", "height"):
            expected = dimensions.get(name, original[name])
            assert panel[name] == expected
            assert all(layer[name] == expected for layer in panel["layer"])
        assert (
            panel["config"]["legend"]["labelFontSize"]
            == original["config"]["legend"]["labelFontSize"]
        )
    numeric = units(resized.to_dict())[1]
    assert (
        numeric["layer"][1]["encoding"]["color"]["legend"]["gradientLength"]
        == numeric["height"]
    )
    assert before == (list(mpl.rcParams["figure.figsize"]), mpl.rcParams["figure.dpi"])


def test_relative_panel_gaps_use_native_dimensions(adata):
    chart = gsc.pl.umap(
        adata,
        color=["cell_type", "score"],
        width=300,
        height=240,
        ncols=1,
        wspace=0.2,
        hspace=0.1,
        show=False,
    )
    spec = chart.to_dict()
    assert spec["spacing"] == 24
    assert len(spec["vconcat"]) == 2
    assert all(row["spacing"] == 60 for row in spec["vconcat"])
