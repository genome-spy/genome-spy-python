"""Embedding style behavior and regressions."""

from copy import deepcopy

import anndata as ad
import numpy as np
import pytest
from scipy import sparse

import genome_spy as gs
import genome_spy.integrations.scanpy as gsc
from tests.integrations.scanpy.embedding_fixtures import (
    FAMILIES,
    graph_adata,
    make_density,
    make_embedding_adata,
)
from tests.integrations.scanpy.helpers import leaf_marks, points, units

sc = pytest.importorskip("scanpy")


class TestColorBounds:
    """Callable embedding bounds preserve Scanpy's panel inputs and native charts."""

    @pytest.mark.reference
    @pytest.mark.parametrize("sort_order", [False, True])
    @pytest.mark.parametrize("mask_obs", [None, "keep"])
    @pytest.mark.parametrize("use_raw,layer", [(True, None), (False, "counts")])
    @pytest.mark.parametrize("centered", [False, True])
    def test_callable_inputs_and_domains_match_public_scanpy(
        self, sort_order, mask_obs, use_raw, layer, centered
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
    def test_shared_embeddings_resolve_callbacks_once_and_keep_complete_chart(
        self, family
    ):
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
        options.update(
            vmin=[None, "p10", None], vmax=[None, 4, 3], vcenter=[None, 1, None]
        )
        numeric = getattr(gsc.pl, family)(*args, **options)
        # Compare the entire chart, including axes, guides, points and interaction settings.
        assert chart.to_dict() == numeric.to_dict()
        chart.to_json()
        chart.to_html(inline=True, controls=False)
        assert len(calls) == 2

    def test_callback_edits_cannot_change_other_bounds_plotted_values_or_anndata(self):
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
        numeric = gsc.pl.umap(
            data, color="score", vmin=-1, vmax=4, vcenter=0.5, show=False
        )
        np.testing.assert_array_equal(data.obs.score.to_numpy(), original)
        np.testing.assert_array_equal(captured[0], [np.nan, -1, 0, 0, 1, 1, 2, 4])
        np.testing.assert_array_equal(captured[1], captured[0])
        assert chart.to_dict() == numeric.to_dict()

    @pytest.mark.parametrize("name", ["vmin", "vmax", "vcenter"])
    @pytest.mark.parametrize(
        "value", [None, True, "1", [1], np.array(1), complex(1), np.nan, np.inf]
    )
    def test_invalid_callable_results_fail_by_bound_and_panel(self, name, value):
        with pytest.raises(
            ValueError, match=f"{name} callable for panel 1.*finite number"
        ):
            gsc.pl.umap(
                make_embedding_adata(),
                color="score",
                **{name: lambda values: value},
                show=False,
            )

    def test_callback_exception_is_preserved(self):

        def fail(values):
            raise RuntimeError("user callback failed")

        with pytest.raises(RuntimeError, match="user callback failed"):
            gsc.pl.umap(make_embedding_adata(), color="score", vmin=fail, show=False)

    @pytest.mark.parametrize(
        "colorbar_loc,domain", [(None, [0, 1]), ("right", [1.8, 2.2])]
    )
    def test_constant_callable_bounds_reuse_existing_colorbar_expansion(
        self, colorbar_loc, domain
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

    def test_callable_bounds_keep_existing_limit_order_validation(self):
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
        self, center, bounds, colorbar_loc
    ):
        import matplotlib

        matplotlib.use("Agg")
        import matplotlib.pyplot as plt

        data = make_embedding_adata()
        options = dict(
            color="score", vcenter=center, colorbar_loc=colorbar_loc, show=False
        )
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
    def test_constant_centered_colors_match_scanpy_with_and_without_a_guide(self, bar):
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
    def test_explicit_bounds_must_strictly_enclose_the_center(self, bounds):
        with pytest.raises(ValueError, match="vcenter"):
            gsc.pl.umap(
                make_embedding_adata(), color="score", vcenter=0, **bounds, show=False
            )

    def test_integer_metadata_keeps_its_dtype_in_center_callbacks(self):
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

    def test_center_callback_resolves_once_per_panel_and_preserves_unsorted_masked_input(
        self,
    ):
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
            np.testing.assert_array_equal(
                values, np.where(data.obs.keep, source, np.nan)
            )


pytest.importorskip("scanpy")


class TestColorbar:
    """Continuous guide placement through the shared native embedding pipeline."""

    @pytest.mark.parametrize(
        "family,options,location",
        [
            ("umap", {}, location)
            for location in (None, "right", "left", "top", "bottom")
        ]
        + [
            (family, options, "left")
            for family, options in [
                ("embedding", {"basis": "custom"}),
                ("tsne", {}),
                ("diffmap", {}),
                ("draw_graph", {}),
                ("pca", {}),
                ("pca_scatter", {}),
            ]
        ],
    )
    def test_embedding_colorbar_locations_preserve_records_and_categorical_guides(
        self, family, options, location
    ):
        adata = make_embedding_adata()
        options = dict(
            options, color=["cell_type", "score"], width=420, height=180, show=False
        )
        call = getattr(gsc.pl, family)
        original = call(adata, **options).to_dict()
        spec = call(adata, colorbar_loc=location, **options).to_dict()
        assert spec["datasets"] == original["datasets"]
        legend = spec["config"]["legend"]
        horizontal = location in ("top", "bottom")
        assert legend["orient"] == (location or "right")
        assert legend["direction"] == ("horizontal" if horizontal else "vertical")
        assert legend["gradientLength"] == (420 if horizontal else 180)
        assert legend["gradientThickness"] == legend["gradientLength"] / 30
        categorical, continuous = [points(panel)["encoding"] for panel in units(spec)]
        expected = deepcopy(points(units(original)[0])["encoding"])
        if location not in (None, "right"):
            expected["color"]["legend"].update(orient="right", direction="vertical")
        assert categorical == expected
        expected = deepcopy(points(units(original)[1])["encoding"])
        if location is None:
            expected["color"]["legend"] = None
        assert continuous == expected

    @pytest.mark.parametrize("linked", [False, True])
    def test_native_configuration_and_collection_override_numeric_guide_defaults(
        self, linked
    ):
        options = (
            {"selection": gs.selection_interval("cells", encodings=["x", "y"])}
            if linked
            else {}
        )
        chart = gsc.pl.umap(
            make_embedding_adata(),
            color=["score", "g1"],
            colorbar_loc="top",
            show=False,
            **options,
        )
        original = chart.to_dict()
        spec = (
            chart.resolve_legend(default="collected")
            .configure_legend(
                orient="left",
                direction="vertical",
                gradientLength=140,
                gradientThickness=8,
            )
            .to_dict()
        )
        assert spec["resolve"]["legend"] == {"default": "collected"}
        assert spec["config"]["legend"]["orient"] == "left"
        assert spec["config"]["legend"]["direction"] == "vertical"
        assert spec["config"]["legend"]["gradientLength"] == 140
        assert spec["datasets"] == original["datasets"]
        assert units(spec) == units(original)

    @pytest.mark.parametrize("location", ["none", "center", "RIGHT"])
    def test_unsupported_colorbar_locations_fail_before_reading_data(self, location):
        with pytest.raises(NotImplementedError, match="colorbar_loc"):
            gsc.pl.umap(None, colorbar_loc=location, show=False)


mpl = pytest.importorskip("matplotlib")
mpl.use("Agg")


class TestEmbeddingOutlines:
    """Outline sizes, order and opacity follow pinned Scanpy without new data reads."""

    @pytest.mark.reference
    @pytest.mark.parametrize(
        "options",
        [
            {},
            {"alpha": None},
            {"alpha": 0},
            {
                "alpha": 0.4,
                "outline_width": (0.2, 0.1),
                "outline_color": ("navy", "ivory"),
                "linewidths": 0,
            },
            {"edgecolor": "red", "linewidth": 2},
            {"edgecolor": "none"},
        ],
    )
    @pytest.mark.parametrize("marker", [".", "o", "s", "D"])
    def test_outline_geometry_and_opacity_match_scanpy(
        self, monkeypatch, options, marker
    ):
        import matplotlib.pyplot as plt

        a = make_embedding_adata()
        sizes = np.array([0, 36, 144, 324, 16, 4, 64, 100])
        with plt.rc_context({"figure.dpi": 100, "lines.linewidth": 1.5}):
            ax = sc.pl.umap(
                a,
                color="score",
                size=sizes,
                marker=marker,
                add_outline=True,
                show=False,
                **options,
            )
            reference = [
                (
                    artist.get_sizes().copy(),
                    artist.get_alpha(),
                    artist.get_linewidths().copy(),
                    artist.get_edgecolors().copy(),
                )
                for artist in ax.collections
            ]
            plt.close(ax.figure)
        monkeypatch.setattr(
            sc.pl, "umap", lambda *a, **k: pytest.fail("Called Scanpy plotting")
        )
        spec = gsc.pl.umap(
            a,
            color="score",
            size=sizes,
            marker=marker,
            add_outline=True,
            show=False,
            **options,
        ).to_dict()
        marks = leaf_marks(spec)
        # Numeric missing values add a separate foreground mark, never another outline.
        assert len(marks) == 4
        records = spec["datasets"][spec["data"]["name"]]
        ordered = sorted(records, key=lambda row: row["_order_0"])
        path = mpl.markers.MarkerStyle(marker)
        path_width = (
            path.get_path().transformed(path.get_transform()).get_extents().width
        )
        diameter = 100 / 72 * path_width
        for mark, (areas, alpha, widths, edges) in zip(
            [*marks[:2], marks[-1]], reference, strict=True
        ):
            if marker in ("s", "D"):
                assert mark["encoding"]["shape"] == {
                    "value": "square" if marker == "s" else "diamond"
                }
            scale = mark["encoding"]["size"]["scale"]
            native = (
                np.array([row["_size_0"] for row in ordered])
                * scale["range"][1]
                / scale["domain"][1]
            )
            np.testing.assert_allclose(native / diameter**2, areas)
            assert mark["mark"]["fillOpacity"] == (1 if alpha is None else alpha)
            if len(edges) and np.any(edges[:, 3]):
                np.testing.assert_allclose(
                    mark["mark"]["strokeWidth"], widths[0] * 100 / 72
                )
            else:
                assert mark["mark"]["strokeOpacity"] == 0
        assert marks[0]["mark"]["tooltip"] is None
        assert marks[1]["mark"]["tooltip"] is None
        assert marks[-1]["mark"]["tooltip"] == {"handler": "default"}

    @pytest.mark.parametrize("family", FAMILIES)
    def test_outlines_reuse_coordinates_ids_sizes_and_single_source(self, family):
        a = make_embedding_adata()
        original = deepcopy(a)
        args = (a, "umap") if family == "embedding" else (a,)
        options = dict(
            color=["cell_type", "g1"],
            size=np.arange(8) * 7,
            obs_id="cell_id",
            show=False,
            zoom=True,
        )
        plain = getattr(gsc.pl, family)(*args, **options).to_dict()
        outlined = getattr(gsc.pl, family)(*args, add_outline=True, **options).to_dict()
        assert outlined["datasets"] == plain["datasets"]
        assert len(outlined["datasets"]) == 1
        for panel, normal in zip(units(outlined), units(plain), strict=True):
            assert "data" in panel and "transform" in panel
            marks = leaf_marks(panel)
            assert len(marks) in (3, 4)
            assert all(("data" not in mark for mark in marks))
            assert not any(
                (
                    t["type"] == "collect"
                    for mark in marks
                    for t in mark.get("transform", [])
                )
            )
            assert panel["resolve"]["scale"]["size"] == "independent"
            foreground = points(panel)
            for axis in ("x", "y", "key", "size"):
                assert foreground["encoding"][axis] == points(normal)["encoding"][axis]
        np.testing.assert_array_equal(a.X, original.X)
        for key in a.obsm:
            np.testing.assert_array_equal(a.obsm[key], original.obsm[key])
        assert a.obs.equals(original.obs)

    @pytest.mark.parametrize(
        "options,error,match",
        [
            ({"add_outline": "yes"}, TypeError, "add_outline"),
            ({"outline_width": (0.1,)}, ValueError, "outline_width"),
            ({"outline_width": (-1, 0)}, ValueError, "outline_width"),
            ({"outline_width": (np.inf, 0)}, ValueError, "outline_width"),
            ({"outline_color": "red"}, ValueError, "outline_color"),
            ({"outline_color": ("r", "white")}, NotImplementedError, "outline_color"),
        ],
    )
    def test_invalid_outline_options_fail_clearly(self, options, error, match):
        with pytest.raises(error, match=match):
            gsc.pl.umap(
                make_embedding_adata(), show=False, **{"add_outline": True, **options}
            )

    def test_disabled_outline_settings_leave_the_chart_unchanged(self):
        data = make_embedding_adata()
        expected = gsc.pl.umap(data, show=False).to_dict()
        assert gsc.pl.umap(data, add_outline=None, show=False).to_dict() == expected
        assert (
            gsc.pl.umap(
                data,
                outline_width=(0.5, 0.2),
                outline_color=("navy", "ivory"),
                show=False,
            ).to_dict()
            == expected
        )
        with pytest.raises(ValueError, match="outline_width"):
            gsc.pl.umap(data, add_outline=True, outline_width=(1e200, 0), show=False)


class TestEmbeddingEdges:
    """Stored graph edges retain Scanpy ordering, source cells and native point layers."""

    @pytest.mark.reference
    @pytest.mark.parametrize(
        "storage", ["csr", "csc", "csr_array", "csc_array", "dense", "legacy_lil"]
    )
    @pytest.mark.parametrize("key", ["neighbors", "saved"])
    def test_graph_geometry_order_and_style_match_public_scanpy(self, storage, key):
        import matplotlib

        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
        from matplotlib.collections import LineCollection

        data = graph_adata(storage, key)
        data.obsm["X_umap"] = data.obsm["X_umap"][:, :2].copy()
        options = dict(
            color=["cell_type", "score"],
            edges=True,
            edges_width=0.7,
            edges_color="navy",
            neighbors_key=key,
            obs_id="cell_id",
            zoom=True,
            show=False,
        )
        reference_options = {
            k: v for k, v in options.items() if k not in {"obs_id", "zoom"}
        }
        # AnnData.copy() migrates legacy graphs to obsp, which rejects LIL storage.
        axes = sc.pl.umap(deepcopy(data), **reference_options)
        references = [
            next((c for c in ax.collections if isinstance(c, LineCollection)))
            for ax in axes
        ]
        spec = gsc.pl.umap(data, **options).to_dict()
        assert len(spec["datasets"]) == 2
        cell_rows = next(
            (rows for rows in spec["datasets"].values() if "_obs_id" in rows[0])
        )
        cells = {row["_obs_id"]: row for row in cell_rows}
        for panel, ax, reference in zip(units(spec), axes, references, strict=True):
            edge = leaf_marks(panel)[0]
            assert edge["mark"] == {
                "type": "rule",
                "color": "navy",
                "size": pytest.approx(0.7 * 100 / 72),
                "clip": True,
                "tooltip": None,
            }
            rows = spec["datasets"][edge["data"]["name"]]
            segments = [
                [
                    [cells[row[end]][axis] for axis in ["_coord_0", "_coord_1"]]
                    for end in ["_source", "_target"]
                ]
                for row in rows
            ]
            np.testing.assert_array_equal(segments, reference.get_segments())
            assert len(edge["transform"]) == 2
            assert all(
                (
                    t["from"]["name"] == points(panel)["data"]["name"]
                    for t in edge["transform"]
                )
            )
            assert reference.get_zorder() == -2
            for axis, expected in [("x", ax.get_xlim()), ("y", ax.get_ylim())]:
                np.testing.assert_allclose(
                    points(panel)["encoding"][axis]["scale"]["domain"], expected
                )
        plt.close(axes[0].figure)

    @pytest.mark.parametrize("family", FAMILIES)
    @pytest.mark.parametrize("outline", [False, True])
    def test_shared_embeddings_reuse_points_and_read_graph_without_analysis(
        self, family, outline, monkeypatch
    ):
        data = graph_adata()
        original = deepcopy(data)
        for module, name in [
            (sc.pp, "neighbors"),
            (sc.tl, "umap"),
            (sc.tl, "pca"),
            (sc.tl, "diffmap"),
            (sc.tl, "tsne"),
            (sc.pl, "embedding"),
        ]:
            monkeypatch.setattr(
                module,
                name,
                lambda *a, **k: pytest.fail("Ran analysis or Scanpy plotting"),
            )
        args = (data, "umap") if family == "embedding" else (data,)
        options = dict(
            color=["cell_type", "score"],
            dimensions=(0, 1),
            marker=["s", "D"],
            add_outline=outline,
            size=20,
            show=False,
        )
        plain = getattr(gsc.pl, family)(*args, **options).to_dict()
        chart = getattr(gsc.pl, family)(*args, edges=True, **options)
        spec = chart.to_dict()
        for panel, normal in zip(units(spec), units(plain), strict=True):
            assert leaf_marks(panel)[0]["mark"]["type"] == "rule"
            assert [m["mark"] for m in leaf_marks(panel)[1:]] == [
                m["mark"] for m in leaf_marks(normal)
            ]
        assert all(
            (
                mark["encoding"]["shape"] == {"value": "diamond"}
                for mark in leaf_marks(units(spec)[1])[1:]
            )
        )
        assert all(
            (rows in spec["datasets"].values() for rows in plain["datasets"].values())
        )
        np.testing.assert_array_equal(
            data.obsp["connectivities"].data, original.obsp["connectivities"].data
        )
        np.testing.assert_array_equal(data.obsm["X_umap"], original.obsm["X_umap"])
        assert data.uns["neighbors"] == original.uns["neighbors"]
        chart.to_html(inline=True, controls=False)

    def test_legacy_storage_and_current_storage_precedence(self):
        data = graph_adata()
        expected = gsc.pl.umap(data, edges=True, show=False).to_dict()
        matrix = data.obsp.pop("connectivities")
        data.uns["neighbors"]["connectivities"] = matrix
        assert gsc.pl.umap(data, edges=True, show=False).to_dict() == expected
        data.obsp["connectivities"] = matrix
        data.uns["neighbors"]["connectivities"] = sparse.eye(8)
        data.uns["neighbors"]["connectivities_key"] = "ignored_for_default_neighbors"
        assert gsc.pl.umap(data, edges=True, show=False).to_dict() == expected

    def test_disabled_edges_do_not_read_graph_or_change_chart(self):
        data = make_embedding_adata()
        plain = gsc.pl.umap(data, show=False).to_dict()
        assert (
            gsc.pl.umap(
                data,
                edges=False,
                neighbors_key="missing",
                edges_width=2,
                edges_color="navy",
                show=False,
            ).to_dict()
            == plain
        )

    @pytest.mark.parametrize(
        "options,error,message",
        [
            ({"neighbors_key": "missing"}, ValueError, "neighbors metadata"),
            ({"edges_width": -1}, ValueError, "edges_width"),
            ({"edges_width": np.inf}, ValueError, "edges_width"),
            ({"edges_color": ["red", "blue"]}, NotImplementedError, "edges_color"),
            ({"edges_color": "C0"}, NotImplementedError, "edges_color"),
            ({"dimensions": (1, 2)}, NotImplementedError, "first two"),
        ],
    )
    def test_invalid_or_unsupported_edge_options_fail_clearly(
        self, options, error, message
    ):
        with pytest.raises(error, match=message):
            gsc.pl.umap(graph_adata(), edges=True, show=False, **options)

    @pytest.mark.parametrize("problem", ["missing", "nonfinite", "shape", "loops"])
    def test_invalid_graphs_do_not_silently_disappear(self, problem):
        data = graph_adata()
        matrix = data.obsp.pop("connectivities")
        if problem == "nonfinite":
            matrix.data[0] = np.nan
        elif problem == "shape":
            matrix = sparse.csr_matrix((4, 4))
        elif problem == "loops":
            matrix = sparse.eye(8)
        if problem != "missing":
            data.uns["neighbors"]["connectivities"] = matrix
        error = NotImplementedError if problem == "loops" else ValueError
        with pytest.raises(error, match="self-loop|connectivities"):
            gsc.pl.umap(data, edges=True, show=False)

    def test_empty_graph_retains_points_without_an_edge_layer_failure(self):
        data = graph_adata()
        data.obsp["connectivities"] = sparse.csr_matrix((8, 8))
        spec = gsc.pl.umap(data, edges=True, show=False).to_dict()
        assert spec == gsc.pl.umap(data, show=False).to_dict()

    def test_nonfinite_legacy_lil_graph_is_rejected(self):
        data = graph_adata("legacy_lil")
        data.uns["neighbors"]["connectivities"][0, 1] = np.nan
        with pytest.raises(ValueError, match="finite real square matrix"):
            gsc.pl.umap(data, edges=True, show=False)

    def test_views_and_backed_graphs_keep_cell_identity_without_densifying(
        self, tmp_path, monkeypatch
    ):
        import anndata as ad

        data = graph_adata()
        path = tmp_path / "graph.h5ad"
        data.write_h5ad(path)
        backed = ad.read_h5ad(path, backed="r")
        monkeypatch.setattr(
            sparse.csr_matrix,
            "toarray",
            lambda *a, **k: pytest.fail("Densified a matrix"),
        )
        try:
            for candidate in [data[[7, 3, 0, 2, 1]], backed]:
                spec = gsc.pl.umap(
                    candidate, color="score", obs_id="cell_id", edges=True, show=False
                ).to_dict()
                cells = next(
                    (
                        rows
                        for rows in spec["datasets"].values()
                        if rows and "_obs_id" in rows[0]
                    )
                )
                assert [r["_obs_id"] for r in cells] == candidate.obs.cell_id.tolist()
                endpoints = next(
                    (
                        rows
                        for rows in spec["datasets"].values()
                        if rows and "_source" in rows[0]
                    )
                )
                assert {
                    r[end] for r in endpoints for end in ["_source", "_target"]
                } <= set(candidate.obs.cell_id)
        finally:
            backed.file.close()


EMBEDDING_DENSITY_CASES = [
    {},
    {"group": "A"},
    {"group": ["A", "B", "A"]},
    {"groupby": "condition"},
    {"title": "Density"},
    {"bg_dotsize": 3, "fg_dotsize": 8},
    {"vmin": None, "vmax": None},
    {"vmin": 0.2, "vmax": 0.7},
    {"vmin": "p10", "vmax": "p85"},
    {"vcenter": 0.3},
    {"vmin": lambda v: np.min(v), "vmax": lambda v: np.max(v)},
    {"basis": "PCA"},
    {"basis": "FA"},
    {"basis": "diffmap"},
    {"marker": "s"},
    {"marker": ["s"]},
    {"group": "unused"},
]


class TestEmbeddingDensity:
    """Stored density semantics and reuse of Scanpy-compatible embedding preparation."""

    @pytest.mark.reference
    @pytest.mark.parametrize("options", EMBEDDING_DENSITY_CASES)
    def test_coords_sizes_colors_bounds_order_and_titles_match_public_scanpy(
        self, options
    ):
        import matplotlib.pyplot as plt

        a = make_density()
        if options.get("group") == "unused":
            a.obs["condition"] = a.obs["condition"].cat.add_categories(["unused"])
        if options.get("basis") == "PCA":
            a.uns["scores_params"]["components"] = [2, 3]
        reference = a.copy()
        result = (
            sc.pl.embedding_density(reference, key="scores", show=False, **options)
            if "groupby" not in options
            else sc.pl.embedding_density(reference, show=False, **options)
        )
        axes = result if isinstance(result, list) else [result]
        spec = (
            gsc.pl.embedding_density(a, key="scores", show=False, **options).to_dict()
            if "groupby" not in options
            else gsc.pl.embedding_density(a, show=False, **options).to_dict()
        )
        assert len(units(spec)) == len(axes)
        assert len(spec["datasets"]) == 1
        data = next(iter(spec["datasets"].values()))
        for i, (panel, ax) in enumerate(zip(units(spec), axes, strict=True)):
            mark = points(panel)
            projection = panel["transform"][0]
            assert projection["type"] == "project"
            assert projection["fields"] == [
                "_obs_id",
                "_obs_label",
                *[mark["encoding"][axis]["field"] for axis in ("x", "y")],
                f"_value_{i}",
                f"_color_{i}",
                f"_size_{i}",
                f"_order_{i}",
            ]
            rows = sorted(data, key=lambda r: r[f"_order_{i}"])
            fields = [mark["encoding"][axis]["field"] for axis in ("x", "y")]
            np.testing.assert_array_equal(
                [[r[field] for field in fields] for r in rows],
                ax.collections[0].get_offsets(),
            )
            np.testing.assert_array_equal(
                [r[f"_size_{i}"] for r in rows], ax.collections[0].get_sizes()
            )
            np.testing.assert_array_equal(
                [r[f"_color_{i}"] for r in rows], ax.collections[0].get_array()
            )
            domain = [ax.collections[0].norm.vmin, ax.collections[0].norm.vmax]
            if options.get("vcenter") is not None:
                domain.insert(1, 0.3)
            np.testing.assert_allclose(
                mark["encoding"]["color"]["scale"]["domain"], domain
            )
            for axis in ("x", "y"):
                np.testing.assert_allclose(
                    mark["encoding"][axis]["scale"]["domain"],
                    getattr(ax, f"get_{axis}lim")(),
                )
                assert (
                    mark["encoding"][axis]["axis"]["title"]
                    == getattr(ax, f"get_{axis}label")()
                )
            assert panel.get("title", {}).get("text", "") == ax.get_title()
            assert "condition" not in mark["encoding"]["color"]
        plt.close(axes[0].figure)

    @pytest.mark.parametrize("group", [None, "all"])
    def test_ungrouped_result_defaults_to_one_panel(self, group):
        a = make_density(False)
        spec = gsc.pl.embedding_density(a, group=group, show=False).to_dict()
        assert len(units(spec)) == 1 and "title" not in spec
        rows = next(iter(spec["datasets"].values()))
        np.testing.assert_array_equal(
            [r["_color_0"] for r in rows], a.obs["umap_density"]
        )
        assert {r["_size_0"] for r in rows} == {180}

    def test_unsorted_points_keep_input_order_when_all_colors_are_in_range(self):
        a = make_density(False)
        spec = gsc.pl.embedding_density(a, sort_order=False, show=False).to_dict()
        rows = next(iter(spec["datasets"].values()))
        assert [r["_order_0"] for r in rows] == list(range(a.n_obs))

    @pytest.mark.parametrize(
        "options", [{}, {"group": "all", "vmin": 0.2, "vmax": 0.7}]
    )
    def test_unsorted_mixed_color_ranges_fail_instead_of_reordering_points(
        self, options
    ):
        with pytest.raises(
            NotImplementedError, match="sort_order=False.*overlap order"
        ):
            gsc.pl.embedding_density(
                make_density(), sort_order=False, show=False, **options
            )

    def test_multiple_markers_fail_clearly(self):
        with pytest.raises(NotImplementedError, match="one marker"):
            gsc.pl.embedding_density(make_density(), marker=["s", "."], show=False)

    def test_direct_basis_key_uses_the_shared_embedding_precedence(self):
        a = make_density()
        a.obsm["umap"] = a.obsm["X_umap"] + 10
        spec = gsc.pl.embedding_density(a, show=False).to_dict()
        rows = next(iter(spec["datasets"].values()))
        np.testing.assert_array_equal(
            [r["_coord_0"] for r in rows], a.obsm["umap"][:, 0]
        )

    def test_density_key_defaults_stay_pinned_for_other_bases_and_params_are_authoritative(
        self,
    ):
        a = make_density()
        a.uns["umap_density_condition_params"]["covariate"] = "condition"
        chart = gsc.pl.embedding_density(
            a, basis="tsne", groupby="condition", show=False
        )
        assert (
            points(units(chart.to_dict())[0])["encoding"]["x"]["axis"]["title"]
            == "tSNE1"
        )
        a.uns["scores_params"]["covariate"] = None
        with pytest.raises(ValueError, match="explicit groups require"):
            gsc.pl.embedding_density(a, key="scores", group="A", show=False)

    def test_no_density_analysis_expression_access_or_input_mutation(
        self, monkeypatch, tmp_path
    ):
        a = make_density()
        path = tmp_path / "stored.h5ad"
        a.write_h5ad(path)
        backed = ad.read_h5ad(path, backed="r")
        snapshot = a.obs.copy(deep=True)
        params = deepcopy(a.uns)
        view = a[:8]
        monkeypatch.setattr(
            sc.tl, "embedding_density", lambda *a, **k: pytest.fail("Reran KDE")
        )
        monkeypatch.setattr(
            ad.AnnData, "X", property(lambda *a: pytest.fail("Read expression"))
        )
        try:
            for data in (a, view, backed):
                chart = gsc.pl.embedding_density(
                    data, key="scores", zoom=True, show=False
                )
                assert chart.to_dict()["datasets"]
            assert view.is_view and a.obs.equals(snapshot) and (a.uns == params)
            assert not any((str(k).startswith("_tmp_") for k in a.obs))
        finally:
            backed.file.close()

    def test_shared_preparation_keeps_stable_ids_raw_hover_and_detached_values(self):
        a = make_density()
        a.obs_names = ["duplicate"] * 12
        chart = gsc.pl.embedding_density(a, key="scores", group="A", show=False)
        spec = chart.to_dict()
        snapshot = deepcopy(spec)
        rows = next(iter(spec["datasets"].values()))
        assert [r["_obs_id"] for r in rows] == [f"row-{i}" for i in range(12)]
        np.testing.assert_array_equal([r["_value_0"] for r in rows], a.obs.scores)
        assert rows[0]["_color_0"] == -1 and rows[0]["_value_0"] == 0
        a.obs["scores"] = 0
        a.obsm["X_umap"][:] = 0
        assert chart.to_dict() == snapshot

    @pytest.mark.parametrize(
        "options,error",
        [
            ({"components": "1,2"}, TypeError),
            ({"norm": object()}, NotImplementedError),
            ({"key": "scores", "groupby": "condition"}, ValueError),
            ({"basis": 3}, ValueError),
            ({"key": 4}, TypeError),
            ({"group": 1}, TypeError),
            ({"title": []}, TypeError),
            ({"bg_dotsize": None}, ValueError),
            ({"fg_dotsize": -1}, ValueError),
            ({"bg_dotsize": float("inf")}, ValueError),
            ({"zoom": "xy"}, TypeError),
            ({"ncols": None}, NotImplementedError),
            ({"hspace": None}, NotImplementedError),
            ({"colorbar_loc": "bad"}, NotImplementedError),
            ({"size": 5}, TypeError),
            ({"edgecolor": "red", "edgecolors": "blue"}, TypeError),
        ],
    )
    def test_invalid_options_fail_before_optional_dependencies(
        self, monkeypatch, options, error
    ):
        monkeypatch.setattr(
            gsc.pl, "_require_scanpy", lambda *a: pytest.fail("Loaded Scanpy")
        )
        with pytest.raises(error, match="gsc.pl.embedding_density"):
            gsc.pl.embedding_density(object(), **options)

    @pytest.mark.parametrize(
        "change,match",
        [
            (lambda a: a.uns.pop("scores_params"), "stored obs"),
            (lambda a: a.obs.pop("scores"), "stored obs"),
            (lambda a: a.uns["scores_params"].pop("components"), "components"),
            (lambda a: a.uns["scores_params"].update(components=[0, 2]), "valid 2D"),
            (lambda a: a.uns["scores_params"].update(components=[1, 99]), "valid 2D"),
            (lambda a: a.uns["scores_params"].update(components=[1.5, 2]), "one-based"),
            (
                lambda a: a.uns["scores_params"].update(covariate="absent"),
                "categorical obs",
            ),
            (
                lambda a: a.obs.__setitem__("condition", a.obs.condition.astype(str)),
                "categorical obs",
            ),
            (lambda a: a.obs.__setitem__("scores", np.nan), "finite values"),
            (lambda a: a.obs.__setitem__("scores", -1), "finite values"),
            (lambda a: a.obsm.pop("X_umap"), "missing obsm"),
        ],
    )
    def test_invalid_stored_results_fail_clearly(self, change, match):
        a = make_density()
        change(a)
        with pytest.raises(ValueError, match=match):
            gsc.pl.embedding_density(a, key="scores", show=False)

    @pytest.mark.parametrize("group", [None, [], ["missing"]])
    def test_invalid_group_selection(self, group):
        with pytest.raises(ValueError, match="group"):
            gsc.pl.embedding_density(
                make_density(), key="scores", group=group, show=False
            )
