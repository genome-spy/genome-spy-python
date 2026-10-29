"""Embeddings behavior and regressions."""

import json
from copy import deepcopy
from io import BytesIO
from pathlib import Path

import numpy as np
import pandas as pd
import pytest
from scipy import sparse

import genome_spy as gs
import genome_spy.integrations.scanpy as gsc
from tests.integrations.scanpy.embedding_fixtures import (
    FAMILIES,
    embedding_cases,
    make_adata,
    make_embedding_adata,
    make_scatter_adata,
    reference_cases,
    scatter_cases,
)
from tests.integrations.scanpy.helpers import leaf_marks, points, units

sc = pytest.importorskip("scanpy")
mpl = pytest.importorskip("matplotlib")
UMAP_REFERENCE = json.loads(
    (Path(__file__).with_name("fixtures") / "umap.json").read_text()
)


def umap_rows(chart):
    spec = chart.to_dict()
    assert len(spec["datasets"]) == 1
    return next(iter(spec["datasets"].values()))


class TestUmap:
    """Independent semantic and pinned-reference tests for UMAP."""

    @pytest.fixture
    def adata(self):
        with pytest.warns(UserWarning, match="Observation names are not unique"):
            return make_adata()

    @pytest.mark.parametrize("case", reference_cases())
    def test_complete_specs_match_frozen_reference_data_and_domains(self, adata, case):
        width, height = UMAP_REFERENCE["cases"][case]["panels"][0]["plot_size"]
        chart = gsc.pl.umap(
            adata,
            **reference_cases()[case],
            size=np.arange(8) * 7 + 25,
            width=width,
            height=height,
            show=False,
        )
        spec = chart.to_dict()
        data = umap_rows(chart)
        for i, (unit, expected) in enumerate(
            zip(units(spec), UMAP_REFERENCE["cases"][case]["panels"], strict=True)
        ):
            encoding = points(unit)["encoding"]
            ordered = sorted(data, key=lambda r: r[f"_order_{i}"])
            assert [
                int(r["_obs_id"].removeprefix("row-")) for r in ordered
            ] == expected["order"]
            np.testing.assert_array_equal(
                [[r["_coord_0"], r["_coord_1"]] for r in ordered],
                expected["coordinates"],
            )
            color = encoding["color"]
            if color["type"] == "nominal":
                palette = dict(
                    zip(color["scale"]["domain"], color["scale"]["range"], strict=True)
                )
                # Explicit CSS palettes retain the frozen Scanpy colors.
                from matplotlib.colors import to_hex

                assert [
                    to_hex(palette[r[f"_color_{i}"]], keep_alpha=True) for r in ordered
                ] == expected["colors"]
            else:
                assert color["scale"]["scheme"] == "viridis"
            np.testing.assert_allclose(
                [r[f"_size_{i}"] for r in ordered], np.array(expected["sizes"])
            )
            for coordinate in ["x", "y"]:
                np.testing.assert_allclose(
                    encoding[coordinate]["scale"]["domain"],
                    expected[f"{coordinate}_domain"],
                )
                assert (encoding[coordinate]["axis"] is not None) == expected["frameon"]
            np.testing.assert_allclose(
                [points(unit)["width"], points(unit)["height"]], expected["plot_size"]
            )
            assert unit["title"]["text"] == expected["title"]
            if expected["legend"] is not None:
                assert (
                    points(unit)["encoding"]["color"]["legend"]["values"]
                    == expected["legend"]
                )
            if expected["color_domain"] is not None:
                assert (
                    points(unit)["encoding"]["color"]["scale"]["domain"]
                    == expected["color_domain"]
                )

    def test_ties_and_duplicate_coordinates_keep_distinct_observations(self, adata):
        data = umap_rows(gsc.pl.umap(adata, color="score", show=False))
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
    def test_expression_source_and_embedding_symbol_lookup(
        self, adata, options, expected
    ):
        assert [
            r["_value_0"] for r in umap_rows(gsc.pl.umap(adata, **options, show=False))
        ] == expected

    @pytest.mark.parametrize(
        "kind",
        [sparse.csr_matrix, sparse.csc_matrix, sparse.csr_array, sparse.csc_array],
    )
    @pytest.mark.parametrize("view", [False, True])
    def test_sparse_expression_densifies_only_selected_columns(
        self, adata, monkeypatch, kind, view
    ):
        adata.X = kind(adata.X)
        source = adata[[7, 0, 3], :] if view else adata
        shapes = []

        def guard(original):

            def selected_only(self, *args, **kwargs):
                shapes.append(self.shape)
                assert self.shape in ((len(source), 1), (len(source),))
                return original(self, *args, **kwargs)

            return selected_only

        # Sparse-array column indexing can produce a one-dimensional COO vector.
        for cls in (
            sparse.csr_matrix,
            sparse.csc_matrix,
            sparse.csr_array,
            sparse.csc_array,
            sparse.coo_array,
        ):
            monkeypatch.setattr(cls, "toarray", guard(cls.toarray))
        data = umap_rows(
            gsc.pl.umap(source, color=["g1", "g1"], use_raw=False, show=False)
        )
        assert [r["_value_0"] for r in data] == (
            [1, 0, 0] if view else [i % 3 for i in range(8)]
        )
        assert len(shapes) == 1

    def test_observation_colors_never_read_expression(self, adata, monkeypatch):

        def forbidden(self):
            pytest.fail("Observation plot accessed expression")

        monkeypatch.setattr(type(adata), "X", property(forbidden))
        monkeypatch.setattr(type(adata.raw), "X", property(forbidden))
        assert len(umap_rows(gsc.pl.umap(adata, color="cell_type", show=False))) == 8

    @pytest.mark.parametrize(
        "options",
        [
            {"color": "cell_type", "groups": ["B"]},
            {"color": "score", "mask_obs": "keep"},
        ],
    )
    def test_groups_and_masks_recolor_instead_of_filtering(self, adata, options):
        data = umap_rows(gsc.pl.umap(adata, **options, show=False))
        assert len(data) == 8
        keep = (
            adata.obs.cell_type.eq("B").to_numpy()
            if "groups" in options
            else adata.obs.keep.to_numpy() & adata.obs.score.notna().to_numpy()
        )
        assert [r["_value_0"] is not None for r in data] == keep.tolist()
        if "groups" in options:
            assert {
                r["_color_0"]
                for r, retained in zip(data, keep, strict=True)
                if not retained
            } == {"NA"}

    def test_plotting_does_not_mutate_or_run_analysis(self, adata, monkeypatch):
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
        chart = gsc.pl.umap(
            adata,
            color=["cell_type", "g1"],
            palette=["red", "blue", "green", "grey"],
            show=False,
        )
        frozen = umap_rows(chart)
        pd.testing.assert_frame_equal(adata.obs, original.obs)
        np.testing.assert_array_equal(adata.X, original.X)
        np.testing.assert_array_equal(adata.raw.X, original.raw.X)
        assert adata.uns == uns
        adata.X[:] = -100
        adata.obsm["X_umap"][:] = -100
        adata.obs["cell_type"] = "changed"
        assert umap_rows(chart) == frozen

    def test_arrow_and_json_share_detached_records(self, adata):
        pa = pytest.importorskip("pyarrow")
        chart = gsc.pl.umap(
            adata, color=["cell_type", "score"], obs_id="cell_id", show=False
        )
        prepared = chart._prepare_render()
        assert len(prepared.buffers) == 1
        table = pa.ipc.open_file(
            BytesIO(next(iter(prepared.buffers.values())))
        ).read_all()
        assert table.to_pylist() == umap_rows(chart)
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
    def test_invalid_data_errors_are_contextual(self, adata, options, message):
        with pytest.raises((ValueError, TypeError), match=message):
            gsc.pl.umap(adata, **options, show=False)

    @pytest.mark.parametrize(
        "marker,factor", [(".", 0.25), ("o", 1), ("s", 1), ("D", 2)]
    )
    def test_sizes_include_physical_units_and_marker_path(self, adata, marker, factor):
        with mpl.rc_context({"figure.dpi": 150}):
            chart = gsc.pl.umap(adata, color="score", s=144, marker=marker, show=False)
        assert [r["_size_0"] for r in umap_rows(chart)] == [144] * 8
        scale = points(units(chart.to_dict())[0])["encoding"]["size"]["scale"]
        assert scale["range"][1] / scale["domain"][1] == pytest.approx(
            (100 / 72) ** 2 * factor
        )

    def test_backed_metadata_and_resident_embedding_work(
        self, adata, tmp_path, monkeypatch
    ):
        import anndata as ad

        path = tmp_path / "test.h5ad"
        adata.write_h5ad(path)
        backed = ad.read_h5ad(path, backed="r")
        try:

            def forbidden(self):
                pytest.fail("Plotting accessed backed expression before rejecting it")

            monkeypatch.setattr(type(backed), "X", property(forbidden))
            monkeypatch.setattr(type(backed.raw), "X", property(forbidden))
            assert (
                len(umap_rows(gsc.pl.umap(backed, color="cell_type", show=False))) == 8
            )
            for use_raw in [False, True]:
                with pytest.raises(TypeError, match="backed/lazy"):
                    gsc.pl.umap(
                        backed[[7, 0, 3]], color="g1", use_raw=use_raw, show=False
                    )
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
    def test_component_products_and_dimension_broadcasting(self, adata, options, count):
        chart = gsc.pl.umap(adata, **options, show=False)
        assert len(units(chart.to_dict())) == count
        assert len(umap_rows(chart)) == len(adata)

    def test_custom_palette_keeps_unused_order_and_masks(self, adata):
        palette = {"C": "purple", "B": "orange", "A": "cyan", "unused": "black"}
        chart = gsc.pl.umap(
            adata, color="cell_type", palette=palette, groups=["A", "C"], show=False
        )
        unit = units(chart.to_dict())[0]
        guide = points(unit)["encoding"]["color"]
        assert guide["scale"]["domain"] == ["C", "A", "NA"]
        assert guide["scale"]["range"] == ["purple", "cyan", "lightgray"]
        assert umap_rows(chart)[0]["_value_0"] is None
        assert adata.uns["cell_type_colors"] == [
            "#ff0000",
            "#00aa00",
            "#0000ff",
            "#888888",
        ]

    def test_hover_opt_out_keeps_point_style_and_disables_picking(self, adata):
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
        unit = points(units(chart.to_dict())[0])
        assert unit["mark"]["tooltip"] is None
        assert unit["mark"]["filled"] is True
        assert unit["mark"]["stroke"] == "red"
        assert unit["mark"]["strokeOpacity"] == 0.25
        assert "tooltip" not in unit["encoding"]
        assert unit["encoding"]["x"]["scale"]["zoom"] is False
        assert unit["mark"]["fillOpacity"] == 0.25
        assert {r["_size_0"] for r in umap_rows(chart)} == {0}

    @pytest.mark.parametrize(
        "palette", [[(1, 0, 0, 0.5)] * 4, ["#ff000080"] * 4, ["tab:blue"] * 4]
    )
    def test_matplotlib_color_forms_and_entry_alpha_fail_clearly(self, adata, palette):
        with pytest.raises(NotImplementedError, match="opaque CSS"):
            gsc.pl.umap(adata, color="cell_type", palette=palette, show=False)

    @pytest.mark.parametrize(
        "cmap", ["coolwarm", "viridis_r", mpl.colormaps["viridis"]]
    )
    def test_unsupported_colormaps_fail_clearly(self, adata, cmap):
        with pytest.raises(NotImplementedError, match="GenomeSpy scheme"):
            gsc.pl.umap(adata, color="score", cmap=cmap, show=False)

    def test_named_native_scheme_uses_full_category_order_with_groups(self, adata):
        with pytest.raises(NotImplementedError, match="missing-category legend"):
            gsc.pl.umap(adata, color="cell_type", palette="Set1", show=False)
        chart = gsc.pl.umap(
            adata,
            color="cell_type",
            palette="Set1",
            groups=["A"],
            na_in_legend=False,
            show=False,
        )
        scale = points(units(chart.to_dict())[0])["encoding"]["color"]["scale"]
        assert scale == {
            "type": "ordinal",
            "domain": ["C", "B", "A", "unused"],
            "nice": False,
            "scheme": "set1",
        }

    def test_on_data_labels_use_semantic_medians(self, adata):
        chart = gsc.pl.umap(
            adata,
            color="cell_type",
            legend_loc="on data",
            legend_fontweight="normal",
            show=False,
        )
        spec = chart.to_dict()
        labels = next(
            (values for values in spec["datasets"].values() if "label" in values[0])
        )
        assert [r["label"] for r in labels] == ["C", "B", "A", "NA"]
        assert labels[1] == {"label": "B", "x": 0.5, "y": -1.0}
        mark = next((m for m in leaf_marks(spec) if m["mark"]["type"] == "text"))
        measure = next((t for t in mark["transform"] if t["type"] == "measureText"))
        assert measure["fontSize"] == mark["mark"]["size"]
        assert measure["font"] == mark["mark"]["font"]
        displacement = next((t for t in mark["transform"] if t["type"] == "displace2d"))
        assert displacement["key"] == "label" and displacement["width"] == measure["as"]
        for axis, field in zip(("xOffset", "yOffset"), displacement["as"], strict=True):
            assert mark["encoding"][axis] == {
                "field": field,
                "type": "quantitative",
                "scale": None,
            }

    def test_missing_numeric_colors_and_ambiguous_genes_fail(self, adata):
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
        self, adata, dimensions
    ):
        before = (list(mpl.rcParams["figure.figsize"]), mpl.rcParams["figure.dpi"])
        default = gsc.pl.umap(adata, color=["cell_type", "score"], size=60, show=False)
        resized = gsc.pl.umap(
            adata, color=["cell_type", "score"], size=60, show=False, **dimensions
        )
        assert umap_rows(resized) == umap_rows(default)
        for original, panel in zip(
            units(default.to_dict()), units(resized.to_dict()), strict=True
        ):
            for name in ("width", "height"):
                expected = dimensions.get(name, original[name])
                assert panel[name] == expected
                assert all(
                    (layer[name] == expected for layer in panel.get("layer", [panel]))
                )
            assert (
                panel["config"]["legend"]["labelFontSize"]
                == original["config"]["legend"]["labelFontSize"]
            )
        numeric = units(resized.to_dict())[1]
        assert (
            resized.to_dict()["config"]["legend"]["gradientLength"] == numeric["height"]
        )
        assert before == (
            list(mpl.rcParams["figure.figsize"]),
            mpl.rcParams["figure.dpi"],
        )

    @pytest.mark.parametrize("color", ["cell_type", "score", ["cell_type", "score"]])
    @pytest.mark.parametrize("fontsize", [8, 20])
    @pytest.mark.parametrize("linked", [False, True])
    def test_legend_typography_survives_single_panel_composition(
        self, adata, color, fontsize, linked
    ):
        options = (
            {"selection": gs.selection_interval("cells", encodings=["x", "y"])}
            if linked
            else {}
        )
        spec = gsc.pl.umap(
            adata, color=color, legend_fontsize=fontsize, show=False, **options
        ).to_dict()
        panels = units(spec["vconcat"][0] if linked else spec)
        for panel in panels:
            categorical = points(panel)["encoding"]["color"]["type"] == "nominal"
            legend = panel["config"]["legend"]
            assert legend["labelFontSize"] == pytest.approx(
                (fontsize if categorical else 10) * 100 / 72
            )
            assert legend["rowPadding"] == pytest.approx(0.5 * fontsize * 100 / 72)
            assert legend["labelOffset"] == pytest.approx(0.8 * fontsize * 100 / 72)
            assert legend["layout"] == {"anchor": "middle", "wrap": False}

    def test_relative_panel_gaps_use_native_dimensions(self, adata):
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
        assert all((row["spacing"] == 60 for row in spec["vconcat"]))

    def test_brushing_has_one_owner_without_changing_prepared_data_or_guides(
        self, adata
    ):
        brush = gs.selection_interval(encodings=["x", "y"])
        options = dict(color=["cell_type", "score"], obs_id="cell_id", show=False)
        original = gsc.pl.umap(adata, **options)
        linked = gsc.pl.umap(adata, selection=brush, **options)
        spec = linked.to_dict()
        assert umap_rows(linked) == umap_rows(original)
        assert spec["params"] == [
            {
                "name": brush.name,
                "value": {"type": "interval", "intervals": {"x": None, "y": None}},
            }
        ]
        panels = units(spec["vconcat"][0])
        counter = spec["vconcat"][1]
        assert "data" not in counter
        assert spec["data"] == panels[0]["data"]
        assert counter["name"] == f"umap-count-{brush.name}"
        assert counter["transform"][-2] == {
            "type": "aggregate",
            "fields": ["selected"],
            "ops": ["sum"],
            "as": ["count"],
        }
        assert panels[0]["name"] == f"umap-brush-{brush.name}"
        assert panels[0]["params"] == [
            {
                "name": brush.name,
                "select": {"type": "interval", "encodings": ["x", "y"]},
                "push": "outer",
            }
        ]
        assert "params" not in panels[1]
        for panel, baseline in zip(panels, units(original.to_dict()), strict=True):
            point = points(panel)
            for key in ("encoding", "mark", "transform"):
                assert point.get(key) == points(baseline).get(key)

    @pytest.mark.parametrize("legend_loc", [None, "right margin"])
    def test_single_panel_brush_has_an_ancestor_value_without_empty_point_effects(
        self, adata, legend_loc
    ):
        brush = gs.selection_interval("cells", encodings=["x", "y"], empty=False)
        chart = gsc.pl.umap(
            adata, color="cell_type", selection=brush, legend_loc=legend_loc, show=False
        )
        spec = chart.to_dict()
        assert spec["params"][0]["value"]["intervals"] == {"x": None, "y": None}
        panel = units(spec["vconcat"][0])[0]
        assert panel["params"][0]["push"] == "outer"
        point = points(panel)
        assert "fillOpacity" not in point["encoding"]

    def test_brushing_rejects_different_projection_pairs(self, adata):
        with pytest.raises(NotImplementedError, match="same dimensions"):
            gsc.pl.umap(
                adata,
                dimensions=[(0, 1), (1, 2)],
                selection=gs.selection_interval(encodings=["x", "y"]),
                show=False,
            )

    def test_brushing_preserves_scalar_alpha_and_strokes(self, adata):
        options = dict(
            color="cell_type",
            palette=["red", "blue", "green", "grey"],
            legend_loc=None,
            selection=gs.selection_interval(encodings=["x", "y"]),
            show=False,
        )
        spec = gsc.pl.umap(
            adata, alpha=0.4, edgecolor="black", linewidth=1, **options
        ).to_dict()
        point = units(spec["vconcat"][0])[0]
        point = points(point)
        for channel in ("fillOpacity", "strokeOpacity"):
            assert channel not in point["encoding"]
            assert point["mark"][channel] == 0.4

    def test_native_defaults_ignore_matplotlib_global_style(self, adata):
        original = gsc.pl.umap(
            adata, color=["cell_type", "score"], show=False
        ).to_dict()
        with mpl.rc_context(
            {
                "figure.dpi": 150,
                "figure.figsize": (9, 2),
                "font.size": 22,
                "image.cmap": "plasma",
                "axes.xmargin": 0.3,
                "axes.ymargin": 0.2,
            }
        ):
            changed = gsc.pl.umap(
                adata, color=["cell_type", "score"], show=False
            ).to_dict()
        assert original == changed
        assert [(p["width"], p["height"]) for p in units(original)] == [(300, 300)] * 2

    def test_adapter_never_calls_matplotlib_color_utilities(self, adata, monkeypatch):

        def forbidden(*args, **kwargs):
            pytest.fail("Adapter used Matplotlib color conversion")

        monkeypatch.setattr(mpl.colors, "to_hex", forbidden)
        monkeypatch.setattr(mpl.colors, "to_rgba", forbidden)
        monkeypatch.setattr(mpl.colors, "Normalize", forbidden)
        chart = gsc.pl.umap(adata, color=["cell_type", "g1"], show=False)
        assert len(umap_rows(chart)) == adata.n_obs


class TestEmbedding:
    """Shared stored-coordinate semantics and Scanpy-compatible embedding wrappers."""

    @pytest.mark.parametrize("family", FAMILIES)
    @pytest.mark.parametrize("marker", ["^", "v", "<", ">"])
    def test_triangular_markers_reject_until_native_geometry_matches(
        self, family, marker
    ):
        options = {"basis": "custom"} if family == "embedding" else {}
        with pytest.raises(NotImplementedError, match="marker"):
            getattr(gsc.pl, family)(
                make_embedding_adata(), marker=marker, show=False, **options
            )

    @pytest.mark.parametrize("case", embedding_cases())
    def test_complete_embedding_specs_match_pinned_reference_coordinates_and_labels(
        self, case
    ):
        from matplotlib.colors import to_hex

        manifest = json.loads(
            (Path(__file__).with_name("fixtures") / "embedding.json").read_text()
        )
        expected = manifest["cases"][case]
        family, options = embedding_cases()[case]
        spec = getattr(gsc.pl, family)(
            make_embedding_adata(),
            size=np.arange(8) * 7 + 25,
            frameon=True,
            show=False,
            **options,
        ).to_dict()
        mark = points(spec)
        data = sorted(
            next(iter(spec["datasets"].values())), key=lambda r: r["_order_0"]
        )
        fields = [mark["encoding"][axis]["field"] for axis in ("x", "y")]
        np.testing.assert_array_equal(
            [[row[field] for field in fields] for row in data], expected["coordinates"]
        )
        np.testing.assert_array_equal([r["_size_0"] for r in data], expected["sizes"])
        assert [
            mark["encoding"][axis]["axis"]["title"] for axis in ("x", "y")
        ] == expected["labels"]
        for axis in ("x", "y"):
            np.testing.assert_allclose(
                mark["encoding"][axis]["scale"]["domain"], expected[f"{axis}_domain"]
            )
        assert spec["title"]["text"] == expected["title"]
        color = mark["encoding"]["color"]
        if expected["legend"] is not None:
            assert color["legend"]["values"] == expected["legend"]
            paints = dict(
                zip(color["scale"]["domain"], color["scale"]["range"], strict=True)
            )
            assert [
                to_hex(paints[r["_color_0"]], keep_alpha=True) for r in data
            ] == expected["colors"]
        else:
            assert color["scale"]["domain"] == expected["color_domain"]

    @pytest.mark.parametrize(
        "family,basis",
        [
            ("umap", "umap"),
            ("tsne", "tsne"),
            ("diffmap", "diffmap"),
            ("draw_graph", "draw_graph_fa"),
            ("pca", "pca"),
            ("pca_scatter", "pca"),
        ],
    )
    def test_aliases_are_exactly_the_shared_embedding_chart(self, family, basis):
        a = make_embedding_adata()
        options = dict(
            color=["cell_type", "g1"],
            dimensions=(1, 2),
            obs_id="cell_id",
            zoom=True,
            show=False,
        )
        actual = getattr(gsc.pl, family)(a, **options).to_dict()
        expected = gsc.pl.embedding(a, basis, **options).to_dict()
        assert actual == expected

    def test_basis_precedence_and_dataframe_coordinates_retain_source_precision(self):
        a = make_embedding_adata()
        a.obsm["tsne"] = pd.DataFrame(a.obsm["X_tsne"] * 7, index=a.obs_names)
        chart = gsc.pl.tsne(a, dimensions=(2, 0), show=False).to_dict()
        records = next(iter(chart["datasets"].values()))
        np.testing.assert_array_equal(
            [[r["_coord_2"], r["_coord_0"]] for r in records],
            a.obsm["tsne"].iloc[:, [2, 0]],
        )
        assert {r["_obs_id"] for r in records} == {f"row-{i}" for i in range(8)}
        direct = gsc.pl.embedding(a, "X_tsne", show=False).to_dict()
        assert direct["encoding"]["x"]["axis"]["title"] == "X_tsne1"

    def test_component_broadcasting_uses_shared_panels_and_one_color_read(
        self, monkeypatch
    ):
        a = make_embedding_adata()
        getter, calls = (type(a.raw).obs_vector, [])

        def read(owner, key):
            calls.append(key)
            return getter(owner, key)

        monkeypatch.setattr(type(a.raw), "obs_vector", read)
        spec = gsc.pl.embedding(
            a, "custom", color="g1", components="all", show=False
        ).to_dict()
        assert (
            calls == ["g1"] and len(units(spec)) == 3 and (len(spec["datasets"]) == 1)
        )
        assert [
            [points(p)["encoding"][axis]["axis"]["title"] for axis in ("x", "y")]
            for p in units(spec)
        ] == [["custom1", "custom2"], ["custom1", "custom3"], ["custom2", "custom3"]]

    def test_diffmap_default_uses_first_two_stored_columns(self):
        a = make_embedding_adata()
        spec = gsc.pl.diffmap(a, show=False).to_dict()
        assert [spec["encoding"][axis]["axis"]["title"] for axis in ("x", "y")] == [
            "DC1",
            "DC2",
        ]
        data = next(iter(spec["datasets"].values()))
        np.testing.assert_array_equal(
            [[r["_coord_0"], r["_coord_1"]] for r in data], a.obsm["X_diffmap"][:, :2]
        )

    def test_pca_variance_labels_and_hover_use_the_same_stored_metadata(self):
        a = make_embedding_adata()
        before = deepcopy(a.uns["pca"])
        spec = gsc.pl.pca(
            a, dimensions=(2, 0), annotate_var_explained=True, show=False
        ).to_dict()
        expected = ["PC3 (12.5%)", "PC1 (50.0%)"]
        assert [
            spec["encoding"][axis]["axis"]["title"] for axis in ("x", "y")
        ] == expected
        assert [item["title"] for item in spec["encoding"]["tooltip"][-2:]] == expected
        np.testing.assert_array_equal(
            a.uns["pca"]["variance_ratio"], before["variance_ratio"]
        )
        a.uns["pca"]["variance_ratio"] = [0.5, 0.25]
        assert gsc.pl.pca(a, annotate_var_explained=True, show=False) is not None
        with pytest.raises(ValueError, match="variance_ratio"):
            gsc.pl.pca(a, components="2,3", annotate_var_explained=True, show=False)
        del a.uns["pca"]
        assert gsc.pl.pca(a, show=False) is not None

    def test_draw_graph_layout_is_explicit_or_comes_from_saved_params(self):
        a = make_embedding_adata()
        assert (
            gsc.pl.draw_graph(a, show=False).to_dict()
            == gsc.pl.draw_graph(a, layout="fa", show=False).to_dict()
        )
        del a.uns["draw_graph"]
        assert (
            gsc.pl.draw_graph(a, layout="fr", show=False).to_dict()["encoding"]["x"][
                "axis"
            ]["title"]
            == "FR1"
        )
        with pytest.raises(ValueError, match="layout"):
            gsc.pl.draw_graph(a, show=False)
        with pytest.raises(ValueError, match="X_draw_graph_missing"):
            gsc.pl.draw_graph(a, layout="missing", show=False)

    @pytest.mark.parametrize("stored", [None, [], {"params": None}])
    def test_malformed_embedding_metadata_fails_with_a_named_error(self, stored):
        a = make_embedding_adata()
        a.uns["draw_graph"] = stored
        with pytest.raises(ValueError, match="gsc.pl.draw_graph.*layout"):
            gsc.pl.draw_graph(a, show=False)
        a.uns["pca"] = stored
        with pytest.raises(ValueError, match="gsc.pl.pca.*variance_ratio"):
            gsc.pl.pca(a, annotate_var_explained=True, show=False)

    @pytest.mark.parametrize("family", FAMILIES)
    def test_plotting_and_python_selection_never_run_embedding_analysis(
        self, monkeypatch, family
    ):
        a = make_embedding_adata()
        before = {k: np.asarray(v).copy() for k, v in a.obsm.items()}
        for name in ("umap", "tsne", "diffmap", "draw_graph", "pca"):
            monkeypatch.setattr(
                sc.tl, name, lambda *a, **k: pytest.fail("Ran analysis")
            )
        monkeypatch.setattr(
            sc.pp, "neighbors", lambda *a, **k: pytest.fail("Ran neighbors")
        )
        options = {"basis": "custom"} if family == "embedding" else {}
        brush = gs.selection_interval("cells", encodings=["x", "y"])
        spec = getattr(gsc.pl, family)(
            a, color=["cell_type", "g1"], selection=brush, show=False, **options
        ).to_dict()
        assert len(spec["datasets"]) == 1
        for key, values in before.items():
            np.testing.assert_array_equal(a.obsm[key], values)
        basis = (
            "custom"
            if family == "embedding"
            else "draw_graph_fa"
            if family == "draw_graph"
            else "pca"
            if family == "pca_scatter"
            else family
        )
        key = basis if basis in a.obsm else f"X_{basis}"
        coordinates = np.asarray(a.obsm[key])
        low, high = np.quantile(coordinates[:, :2], [0.25, 0.75], axis=0)
        snapshot = {
            "type": "interval",
            "intervals": {"x": [low[0], high[0]], "y": [low[1], high[1]]},
        }
        expected = ((coordinates[:, :2] >= low) & (coordinates[:, :2] < high)).all(
            axis=1
        )
        np.testing.assert_array_equal(
            gsc.selection_mask(a, snapshot, basis=basis), expected
        )
        reordered = a[[7, 0, 3], :]
        np.testing.assert_array_equal(
            gsc.selection_mask(reordered, snapshot, basis=basis), expected[[7, 0, 3]]
        )

    def test_stored_bases_and_observation_colors_work_without_expression_even_backed(
        self, tmp_path, monkeypatch
    ):
        import anndata as ad

        a = make_embedding_adata()
        path = tmp_path / "embeddings.h5ad"
        a.write_h5ad(path)
        backed = ad.read_h5ad(path, backed="r")
        try:
            spec = gsc.pl.pca(backed, color="cell_type", show=False).to_dict()
            assert len(next(iter(spec["datasets"].values()))) == 8
            assert len(gsc.selection_mask(backed, None, basis="pca")) == 8
            with pytest.raises(TypeError, match="backed"):
                gsc.pl.pca(backed, color="g1", show=False)
        finally:
            backed.file.close()

    @pytest.mark.parametrize("basis", ["missing", None, ""])
    def test_missing_or_invalid_basis_fails_without_analysis(self, basis):
        with pytest.raises(ValueError, match="basis|missing"):
            gsc.pl.embedding(make_embedding_adata(), basis, show=False)

    def test_unsupported_internal_options_and_projection_fail_before_optional_imports(
        self, monkeypatch
    ):
        monkeypatch.setattr(
            gsc.pl, "_require_scanpy", lambda *a: pytest.fail("Imported Scanpy")
        )
        for options in [
            {"context": "test"},
            {"annotate_var_explained": True},
            {"projection": "3d"},
        ]:
            with pytest.raises((TypeError, NotImplementedError)):
                gsc.pl.embedding(object(), "pca", **options)


def scatter_records(spec):
    """Return the one shared table for a native scatter chart."""
    assert len(spec["datasets"]) == 1
    return next(iter(spec["datasets"].values()))


class TestScatter:
    """Scatter semantics independently exercise the existing native point pipeline."""

    @pytest.mark.parametrize(
        "family,linked", [("scatter", False), ("umap", False), ("umap", True)]
    )
    def test_native_legend_configuration_overrides_shared_defaults_without_changing_points(
        self, family, linked
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
        original, updated = (default.to_dict(), compact.to_dict())
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
            (
                "orient" not in points(panel)["encoding"]["color"]["legend"]
                for panel in plot
            )
        )
        assert "columns" not in points(plot[0])["encoding"]["color"]["legend"]

    def test_many_categories_keep_scanpy_column_defaults(self):
        a = make_scatter_adata()
        a.obs["many"] = pd.Categorical(range(a.n_obs), categories=range(31))
        spec = gsc.pl.scatter(
            a, "x_value", "y_value", color="many", show=False
        ).to_dict()
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
    def test_marker_shapes_reuse_embedding_data_and_units(
        self, family, marker, shapes, factors
    ):
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

    @pytest.mark.reference
    @pytest.mark.parametrize("family", ["umap", "scatter"])
    @pytest.mark.parametrize("marker", ["o", "s", "D"])
    def test_category_legends_follow_panel_markers_in_native_units(
        self, family, marker
    ):
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
        native_marker = MarkerStyle(
            {"circle": "o", "square": "s", "diamond": "D"}[shape]
        )
        native_path = native_marker.get_path().transformed(
            native_marker.get_transform()
        )
        np.testing.assert_allclose(
            native_path.vertices / native_path.get_extents().width,
            path.vertices / width,
            atol=1e-15,
        )
        np.testing.assert_allclose(
            np.sqrt(guide.get("symbolSize", config["symbolSize"])), expected_width
        )

    @pytest.mark.reference
    @pytest.mark.parametrize("case", scatter_cases())
    def test_complete_chart_matches_frozen_upstream_points_labels_palettes_and_limits(
        self, case
    ):
        from matplotlib.colors import to_hex

        manifest = json.loads(
            (Path(__file__).with_name("fixtures") / "scatter.json").read_text()
        )
        expected = manifest["cases"][case]
        spec = gsc.pl.scatter(
            make_scatter_adata(),
            **scatter_cases()[case],
            size=80,
            frameon=True,
            show=False,
        ).to_dict()
        mark = points(spec)
        rows = sorted(scatter_records(spec), key=lambda r: r["_order_0"])
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
                    (None if v == "X" else v for v in options["layers"])
                )
            axis = sc.pl.scatter(
                make_scatter_adata(), **options, size=80, frameon=True, show=False
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
        assert all((r["_size_0"] == 80 for r in rows))
        assert [
            mark["encoding"][axis]["axis"]["title"] for axis in ("x", "y")
        ] == expected["labels"]
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

    def test_native_color_names_match_css_and_reject_invalid_names_and_hex(self):
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

    def test_raw_default_and_three_layers_preserve_selected_vectors_without_mutation(
        self,
    ):
        a = make_scatter_adata()
        before = (deepcopy(a.uns), a.obs.copy(), a.var.copy(), a.X.copy())
        raw = scatter_records(
            gsc.pl.scatter(a, "g1", "g2", color="raw_only", show=False).to_dict()
        )
        np.testing.assert_array_equal(
            [r["_coord_0"] for r in raw], a.raw.obs_vector("g1")
        )
        np.testing.assert_array_equal(
            [r["_coord_1"] for r in raw], a.raw.obs_vector("g2")
        )
        np.testing.assert_array_equal(
            [r["_value_0"] for r in raw], a.raw.obs_vector("raw_only")
        )
        layered = scatter_records(
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
        np.testing.assert_array_equal(
            [r["_coord_1"] for r in layered], a.obs_vector("g2")
        )
        np.testing.assert_array_equal(
            [r["_value_0"] for r in layered], a.obs_vector("g1")
        )
        pd.testing.assert_frame_equal(a.obs, before[1])
        pd.testing.assert_frame_equal(a.var, before[2])
        np.testing.assert_array_equal(a.X, before[3])
        for key in ("cell_type_colors", "gene_group_colors"):
            assert a.uns[key] == before[0][key]

    def test_variables_use_public_row_vectors_without_transposing_or_copying_expression(
        self, monkeypatch
    ):
        a = make_scatter_adata()
        getter, calls = (type(a).var_vector, [])

        def read(owner, key, *, layer=None):
            calls.append((key, layer))
            return getter(owner, key, layer=layer)

        monkeypatch.setattr(type(a), "var_vector", read)
        monkeypatch.setattr(
            type(a), "transpose", lambda *a: pytest.fail("Transposed the full AnnData")
        )
        spec = gsc.pl.scatter(
            a,
            "c1",
            "c3",
            color=["c1", "c4"],
            use_raw=False,
            layers="counts",
            show=False,
        ).to_dict()
        assert calls == [("c1", "counts"), ("c3", "counts"), ("c4", "counts")]
        rows = scatter_records(spec)
        assert [r["_obs_id"] for r in rows] == list(a.var_names)
        np.testing.assert_array_equal(
            [r["_coord_0"] for r in rows], a.layers["counts"][1]
        )
        for panel in units(spec):
            assert [v["title"] for v in points(panel)["encoding"]["tooltip"][:2]] == [
                "Variable ID",
                "Variable",
            ]

    @pytest.mark.parametrize("matrix_type", [sparse.csr_matrix, sparse.csc_matrix])
    @pytest.mark.parametrize("axis", ["obs", "var"])
    def test_sparse_and_views_only_densify_selected_vectors_and_read_repeated_fields_once(
        self, monkeypatch, matrix_type, axis
    ):
        a = make_scatter_adata()
        a.X = matrix_type(a.X)
        a = a[[5, 0, 4, 7], :]
        method, shapes = (matrix_type.toarray, [])

        def densify(value, *args, **kwargs):
            shapes.append(value.shape)
            return method(value, *args, **kwargs)

        monkeypatch.setattr(matrix_type, "toarray", densify)
        x, y = ("g1", "g2") if axis == "obs" else ("c5", "c4")
        spec = gsc.pl.scatter(
            a, x, y, color=[x, x], use_raw=False, show=False
        ).to_dict()
        assert shapes == ([(4, 1), (4, 1)] if axis == "obs" else [(1, 3), (1, 3)])
        assert [r["_obs_label"] for r in scatter_records(spec)] == list(
            a.obs_names if axis == "obs" else a.var_names
        )
        assert len(units(spec)) == 2 and a.is_view

    def test_variable_layer_default_ignores_raw_as_scanpy_transpose_does(self):
        a = make_scatter_adata()
        spec = gsc.pl.scatter(
            a, "c1", "c3", color="c1", layers="counts", show=False
        ).to_dict()
        rows = scatter_records(spec)
        np.testing.assert_array_equal(
            [r["_coord_0"] for r in rows], a.layers["counts"][1]
        )
        np.testing.assert_array_equal(
            [r["_value_0"] for r in rows], a.layers["counts"][1]
        )
        assert len(rows) == a.n_vars

    def test_palettes_follow_categorical_panels_and_reject_upstream_flat_list_truncation(
        self,
    ):
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

    def test_scatter_basis_is_exact_X_key_and_diffmap_skips_first_column(self):
        a = make_scatter_adata()
        a.obsm["diffmap"] = a.obsm["X_diffmap"] * 50
        spec = gsc.pl.scatter(a, basis="diffmap", show=False).to_dict()
        np.testing.assert_array_equal(
            [[r["_coord_0"], r["_coord_1"]] for r in scatter_records(spec)],
            a.obsm["X_diffmap"][:, [1, 2]],
        )
        assert [spec["encoding"][axis]["axis"]["title"] for axis in ("x", "y")] == [
            "DC1",
            "DC2",
        ]
        del a.obsm["X_diffmap"]
        with pytest.raises(ValueError, match="X_diffmap"):
            gsc.pl.scatter(a, basis="diffmap", show=False)

    def test_category_order_groups_missing_and_per_panel_palettes_stay_consistent(self):
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
            order = sorted(scatter_records(spec), key=lambda r: r[f"_order_{index}"])
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

    def test_scatter_keeps_pinned_numeric_sort_flag_behavior_and_filters_missing_colors(
        self,
    ):
        a = make_scatter_adata()
        spec = gsc.pl.scatter(
            a, "x_value", "y_value", color="score", sort_order=False, show=False
        ).to_dict()
        rows = sorted(scatter_records(spec), key=lambda r: r["_order_0"])
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

    def test_missing_numeric_color_does_not_expand_coordinate_limits(self):
        a = make_scatter_adata()
        a.obs.loc["c4", "x_value"] = 100000
        a.obs.loc["c4", "score"] = np.nan
        spec = gsc.pl.scatter(
            a, "x_value", "y_value", color="score", show=False
        ).to_dict()
        np.testing.assert_allclose(
            spec["encoding"]["x"]["scale"]["domain"], [-1.15, 2.15]
        )
        assert len(scatter_records(spec)) == a.n_obs
        assert spec["transform"][-1]["expr"] == "isValid(datum._value_0)"

    def test_duplicate_names_get_distinct_point_ids_without_changing_display_labels(
        self,
    ):
        a = make_scatter_adata()
        rows = scatter_records(
            gsc.pl.scatter(a, "x_value", "y_value", show=False).to_dict()
        )
        assert len({r["_obs_id"] for r in rows}) == a.n_obs
        assert [r["_obs_label"] for r in rows] == list(a.obs_names)

    def test_plotting_calls_no_analysis_or_scanpy_plotting(self, monkeypatch):
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
            (
                {"x": "x_value", "y": "dispersion"},
                ValueError,
                "observations.*variables",
            ),
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
    def test_invalid_and_unsupported_cases_fail_clearly(self, options, error, match):
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
    def test_omitted_and_unknown_options_are_not_silently_ignored(self, options):
        with pytest.raises(TypeError, match=next(iter(options))):
            gsc.pl.scatter(object(), **options)

    @pytest.mark.parametrize("value", [float("nan"), float("inf"), -float("inf")])
    def test_nonfinite_axis_values_fail_before_rendering(self, value):
        a = make_scatter_adata()
        a.obs.loc["c1", "x_value"] = value
        with pytest.raises(ValueError, match="finite"):
            gsc.pl.scatter(a, "x_value", "y_value", show=False)

    def test_backed_metadata_is_supported_but_backed_expression_fails_early(
        self, tmp_path
    ):
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
