"""Paga behavior and regressions."""

import inspect
import warnings
from copy import deepcopy

import numpy as np
import pandas as pd
import pytest
from anndata import AnnData

import genome_spy as gs
import genome_spy.integrations.scanpy as gsc
from tests.integrations.scanpy.helpers import leaf_marks, points
from tests.integrations.scanpy.paga_fixtures import (
    POSITIONS,
    make_compare,
    make_paga,
    paga_cases,
    paga_reference,
)

pytest.importorskip("scanpy")


class TestPaga:
    """Public PAGA reference semantics, metadata-only layout reuse and deliberate cache writes."""

    @pytest.mark.reference
    @pytest.mark.parametrize("case", paga_cases())
    def test_nodes_edges_labels_bounds_and_cache_match_public_scanpy(
        self, case, monkeypatch
    ):
        import matplotlib.pyplot as plt
        import scanpy as sc
        from matplotlib.collections import LineCollection, PathCollection
        from matplotlib.colors import to_rgba

        a = make_paga(case)
        options = paga_cases()[case]
        reference, reference_options = paga_reference(case)
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            ax = sc.pl.paga(reference, show=False, **reference_options)
            ax.figure.canvas.draw()
        point = next((c for c in ax.collections if isinstance(c, PathCollection)))
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
        mark = next((m for m in leaf_marks(spec) if m["mark"]["type"] == "point"))
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
            np.testing.assert_allclose(
                mark["encoding"][axis]["scale"]["domain"], domain
            )
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
        self, plot, add_pos, format, monkeypatch
    ):
        import matplotlib.pyplot as plt
        import scanpy as sc
        from anndata import AnnData

        a = make_paga()
        a.uns["paga"]["connectivities"] = a.uns["paga"]["connectivities"].asformat(
            format
        )
        old = a.uns["paga"]["pos"].copy()
        for name in ("X", "raw", "layers"):
            original = inspect.getattr_static(AnnData, name)

            def guarded(self, _original=original):
                if self is a:
                    pytest.fail("Read caller expression")
                return _original.__get__(self, type(self))

            monkeypatch.setattr(AnnData, name, property(guarded, original.__set__))
        monkeypatch.setattr(
            sc.tl, "paga", lambda *a, **k: pytest.fail("Ran PAGA analysis")
        )
        monkeypatch.setattr(
            plt, "figure", lambda *a, **k: pytest.fail("Created figure")
        )
        result = gsc.pl.paga(a, plot=plot, add_pos=add_pos, show=False)
        assert (result is not None) == plot
        assert np.array_equal(a.uns["paga"]["pos"], old) is not add_pos

    @pytest.mark.parametrize("add_pos", [False, True])
    def test_layout_only_skips_chart_options_and_respects_position_cache(
        self, monkeypatch, add_pos
    ):
        from genome_spy.integrations.scanpy._paga import chart as _paga_chart

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
        self, monkeypatch
    ):
        import scanpy as sc

        a = make_paga()
        old = a.uns["paga"]["pos"].copy()
        monkeypatch.setattr(
            sc.pl, "paga", lambda *a, **k: pytest.fail("Computed layout")
        )
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
    def test_unsupported_options_fail_before_imports_or_writes(
        self, option, monkeypatch
    ):
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
    def test_invalid_flags_and_axes_fail_clearly(self, option):
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
    def test_invalid_stored_graphs_are_not_recomputed(self, change, error):
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
        self, format, supplied_pos, solid_edges
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
        sc.pl.paga(
            reference, solid_edges=solid_edges, plot=False, show=False, **options
        )
        spec = gsc.pl.paga(a, solid_edges=solid_edges, show=False, **options).to_dict()
        mark = next((m for m in leaf_marks(spec) if m["mark"]["type"] == "point"))
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
    def test_tree_layout_retains_the_unfiltered_source(self, format):
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
        try:
            sc.pl.paga(reference, **options)
        except TypeError as error:
            if "required keyword-only argument: 'directed'" not in str(error):
                raise
            with pytest.raises(
                NotImplementedError, match="Scanpy version cannot compute tree layouts"
            ):
                gsc.pl.paga(a, **options)
            assert a.uns["paga"]["connectivities_tree"].format == format
            assert (a.uns["paga"]["connectivities_tree"] != tree).nnz == 0
            pytest.xfail(
                "Installed Scanpy tree layout omits the required directed argument."
            )
        gsc.pl.paga(a, **options)
        np.testing.assert_allclose(a.uns["paga"]["pos"], reference.uns["paga"]["pos"])
        assert a.uns["paga"]["connectivities_tree"].format == format
        assert (a.uns["paga"]["connectivities_tree"] != tree).nnz == 0

    @pytest.mark.parametrize("layout", ["rt", "rt_circular", "fr"])
    def test_layout_errors_do_not_fall_back_or_mask_unrelated_errors(
        self, monkeypatch, layout
    ):
        import scanpy as sc

        def unavailable(*args, **kwargs):
            raise TypeError(
                "get_igraph_from_adjacency() missing 1 required keyword-only argument: 'directed'"
            )

        monkeypatch.setattr(sc.pl, "paga", unavailable)
        expected = NotImplementedError if layout != "fr" else TypeError
        with pytest.raises(
            expected, match="tree layouts" if layout != "fr" else "directed"
        ):
            gsc.pl.paga(make_paga(), layout=layout, show=False)

        def invalid(*args, **kwargs):
            raise TypeError("invalid layout option")

        monkeypatch.setattr(sc.pl, "paga", invalid)
        with pytest.raises(TypeError, match="invalid layout option"):
            gsc.pl.paga(make_paga(), layout=layout, show=False)

    @pytest.mark.parametrize("storage", ["csr", "csc"])
    @pytest.mark.parametrize("use_raw", [True, False])
    def test_gene_colors_read_one_sparse_column_without_changing_sources(
        self, storage, use_raw, monkeypatch
    ):
        import scanpy as sc
        from scipy import sparse

        a = make_paga("gene_raw")
        a.X = getattr(sparse, f"{storage}_matrix")(a.X)
        raw = a.raw.to_adata()
        raw.X = getattr(sparse, f"{storage}_matrix")(raw.X)
        a.raw = raw
        # Exercise a view while keeping the existing graph's group order and slots.
        a = a[:18]
        before = (a.X.copy(), a.raw.X.copy())
        read, dense = (sc.get.obs_df, [])
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
        rows = next((rows for rows in spec["datasets"].values() if "_cells" in rows[0]))
        expected = np.arange(0, 54, 3, dtype=float) + (0 if use_raw else 100)
        for row in rows:
            np.testing.assert_allclose(
                row["_color"], expected[a.obs["cluster"] == row["_group"]].mean()
            )
        assert (a.X != before[0]).nnz == 0 and (a.raw.X != before[1]).nnz == 0

    def test_gene_colors_fall_back_to_x_without_raw_and_keep_missing_group_labels(self):
        a = make_paga("gene_missing")
        a.raw = None
        spec = gsc.pl.paga(a, color="g1", pos=POSITIONS, show=False).to_dict()
        nodes = next(
            (rows for rows in spec["datasets"].values() if "_cells" in rows[0])
        )
        assert nodes[0]["_color"] is None
        np.testing.assert_allclose(
            [row["_color"] for row in nodes[1:]], [131.5, 139, 149.5]
        )
        marks = leaf_marks(spec)
        assert any(
            (
                mark["encoding"].get("text", {}).get("field") == "_label"
                for mark in marks
            )
        )
        point = next((mark for mark in marks if mark["mark"]["type"] == "point"))
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
    def test_invalid_color_inputs_never_write_positions(self, color, options, match):
        a = make_paga("obs_score")
        a.obs["score"] = np.nan
        before = a.uns["paga"]["pos"].copy()
        with pytest.raises(ValueError, match=match):
            gsc.pl.paga(a, color=color, pos=POSITIONS, show=False, **options)
        np.testing.assert_array_equal(a.uns["paga"]["pos"], before)

    @pytest.mark.parametrize("color", ["score", "degree_solid", "degree_dashed"])
    def test_numeric_metadata_and_degrees_do_not_read_expression_or_draw_figures(
        self, color, monkeypatch
    ):
        import matplotlib.pyplot as plt
        import scanpy as sc
        from anndata import AnnData

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
    def test_unsupported_color_collisions_and_categorical_mixtures_fail_clearly(
        self, color
    ):
        a = make_paga("obs_score")
        a.obs["other_category"] = a.obs["cluster"]
        with pytest.raises(NotImplementedError, match="gsc.pl.paga:.*unsupported"):
            gsc.pl.paga(a, color=color, pos=POSITIONS, show=False)

    @pytest.mark.reference
    @pytest.mark.xfail(
        strict=True,
        raises=ValueError,
        reason="Scanpy 1.11.5 trims component colors but keeps full coordinates; recheck on an upstream fix.",
    )
    def test_direct_scanpy_component_entry_detects_an_upstream_fix(self):
        import matplotlib.pyplot as plt
        import scanpy as sc
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
            point = next((c for c in ax.collections if isinstance(c, PathCollection)))
            assert len(point.get_offsets()) == 3
        finally:
            plt.close("all")

    @pytest.mark.parametrize("storage", ["csr", "csc", "lil"])
    @pytest.mark.parametrize("supplied", [False, True])
    def test_component_preserves_ids_sources_and_full_coordinate_cache(
        self, storage, supplied, monkeypatch
    ):
        import matplotlib.pyplot as plt
        import scanpy as sc

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
        monkeypatch.setattr(
            plt, "figure", lambda *a, **k: pytest.fail("Created figure")
        )
        spec = gsc.pl.paga(
            a,
            single_component=True,
            threshold=0.2,
            color="score",
            show=False,
            **options,
        ).to_dict()
        rows = next((rows for rows in spec["datasets"].values() if "_cells" in rows[0]))
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
        self, plot
    ):
        a = make_paga()
        kwargs = dict(
            single_component=True,
            dashed_edges="weak",
            pos=POSITIONS,
            show=False,
            plot=plot,
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

    def test_tied_components_use_node_count_and_original_order_not_cell_counts(self):
        a = make_paga("component_tie")
        a.uns["cluster_sizes"] = np.array([1, 1, 100, 100])
        spec = gsc.pl.paga(
            a, pos=POSITIONS, single_component=True, show=False
        ).to_dict()
        rows = next((rows for rows in spec["datasets"].values() if "_cells" in rows[0]))
        assert [r["_id"] for r in rows] == [0, 1]
        assert [r["_area"] for r in rows] == pytest.approx(
            [2000 / (np.sqrt(2) + 10)] * 2
        )

    @pytest.mark.parametrize("palette", [None, "set1"])
    def test_group_legend_uses_displayed_names_without_changing_palette_positions(
        self, palette
    ):
        a = make_paga("component")
        spec = gsc.pl.paga(
            a,
            pos=POSITIONS,
            single_component=True,
            threshold=0.2,
            palette=palette,
            show=False,
        ).to_dict()
        mark = next((m for m in leaf_marks(spec) if m["mark"]["type"] == "point"))
        fill = mark["encoding"]["fill"]
        rows = spec["datasets"][mark["data"]["name"]]
        assert fill["field"] == "_group"
        assert fill["legend"]["title"] == "cluster"
        assert (
            fill["legend"]["values"] == [r["_group"] for r in rows] == ["B", "C", "D"]
        )
        if palette:
            assert fill["scale"]["domain"] == ["A", "B", "C", "D"]
        else:
            assert fill["scale"]["range"] == [
                a.uns["cluster_colors"][i] for i in [1, 2, 3]
            ]

    @pytest.mark.parametrize("color", ["score", "g1", "degree_solid"])
    @pytest.mark.parametrize("colorbar", [None, True, False])
    def test_numeric_node_guides_are_native_and_can_be_hidden(self, color, colorbar):
        spec = gsc.pl.paga(
            make_paga("obs_score"),
            pos=POSITIONS,
            color=color,
            colorbar=colorbar,
            show=False,
        ).to_dict()
        fill = next((m for m in leaf_marks(spec) if m["mark"]["type"] == "point"))[
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

    def test_node_legend_rejects_colliding_group_names_before_cache_write(self):
        a = make_paga()
        a.obs["cluster"] = a.obs["cluster"].cat.rename_categories([1, "1", "C", "D"])
        original = a.uns["paga"]["pos"].copy()
        with pytest.raises(ValueError, match="labels collide when serialized"):
            gsc.pl.paga(a, pos=POSITIONS, show=False)
        np.testing.assert_array_equal(a.uns["paga"]["pos"], original)

    @pytest.mark.parametrize("fontweight", ["normal", "bold"])
    def test_node_labels_use_native_measurement_and_stable_ids_without_changing_nodes(
        self, fontweight
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
        labels = next((m for m in leaf_marks(spec) if m["mark"]["type"] == "text"))
        measure = next((t for t in labels["transform"] if t["type"] == "measureText"))
        displacement = next(
            (t for t in labels["transform"] if t["type"] == "displace2d")
        )
        assert displacement["key"] == "_id"
        assert displacement["x"] == "_x" and displacement["y"] == "_y"
        assert (
            displacement["anchorWidth"]
            == displacement["anchorHeight"]
            == "_node_extent"
        )
        assert (
            measure["fontSize"]
            == labels["mark"]["size"]
            == pytest.approx(12 * 100 / 72)
        )
        assert measure["fontWeight"] == labels["mark"]["fontWeight"] == fontweight
        assert labels["mark"]["baseline"] == "middle"
        assert "yOffset" not in labels["mark"]
        assert labels["encoding"]["xOffset"]["scale"] is None
        assert labels["encoding"]["yOffset"]["scale"] is None
        assert not any((m["mark"]["type"] == "text" for m in leaf_marks(hidden)))
        np.testing.assert_array_equal(
            a.uns["paga"]["pos"], make_paga().uns["paga"]["pos"]
        )


sc = pytest.importorskip("scanpy")


class TestPagaCompare:
    """PAGA comparison reuses native parents and honors stored embedding coordinates."""

    def test_default_on_data_bold_labels_keep_the_existing_explicit_font_restriction(
        self,
    ):
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
        self, palette
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
        nodes = next((m for m in leaf_marks(graph) if m["mark"]["type"] == "point"))
        graph_colors = nodes["encoding"]["fill"]["scale"]["range"]
        np.testing.assert_allclose(
            [to_rgba(c) for c in cells], [to_rgba(c) for c in expected]
        )
        np.testing.assert_allclose(
            [to_rgba(c) for c in graph_colors], [to_rgba(c) for c in expected]
        )
        assert a.uns["cluster_colors"] == before

    @pytest.mark.parametrize("component", [False, True])
    def test_native_named_palette_has_one_full_category_domain_in_both_panels(
        self, component
    ):
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
        nodes = next((m for m in leaf_marks(graph) if m["mark"]["type"] == "point"))
        assert points(embedding)["encoding"]["color"]["scale"]["scheme"] == "set1"
        assert nodes["encoding"]["fill"]["scale"] == {
            "type": "ordinal",
            "domain": ["A", "B", "C", "D"],
            "scheme": "set1",
        }
        assert nodes["encoding"]["fill"]["field"] == "_group"
        assert a.uns["cluster_colors"] == before

    def test_explicit_palette_does_not_validate_or_replace_stale_saved_palette(self):
        a = make_compare()
        a.uns["cluster_colors"] = ["invalid"]
        spec = gsc.pl.paga_compare(
            a, palette="set1", legend_fontweight="normal", show=False
        ).to_dict()
        assert len(spec["hconcat"]) == 2
        assert a.uns["cluster_colors"] == ["invalid"]

    def test_paga_coordinate_ownership_is_native_inheritance(self, monkeypatch):
        from genome_spy.integrations.scanpy import pl

        original = pl.paga
        captured = []

        def parent(*args, **kwargs):
            chart = original(*args, **kwargs)
            spec = chart.to_dict()
            assert set(spec["encoding"]) == {"x", "y"}
            assert all(
                (not {"x", "y"} & mark["encoding"].keys() for mark in spec["layer"])
            )
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
        self, components, position_mode
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
            assert all(
                ("scale" not in mark["encoding"][axis] for mark in leaf_marks(graph))
            )
        assert spec.get("title") == common_title
        assert [
            embedding.get("title", {}).get("text", ""),
            graph["title"]["text"],
        ] == expected_titles
        nodes = next(
            (rows for rows in spec["datasets"].values() if rows and "_cells" in rows[0])
        )
        np.testing.assert_allclose(
            [[r["_x"], r["_y"]] for r in nodes], expected_positions
        )
        assert [r["_color"] for r in nodes] == (
            reference.obs.groupby("cluster", observed=True)["score"].mean().tolist()
            if position_mode == "cached"
            else reference.uns["cluster_colors"]
        )

    @pytest.mark.parametrize(
        "preferred", ["draw_graph_fa", "umap", "tsne", "draw_graph_fr"]
    )
    def test_automatic_basis_precedence_and_explicit_basis(self, preferred):
        a = make_compare()
        a.obsm.clear()
        priority = ["draw_graph_fa", "umap", "tsne", "draw_graph_fr"]
        for i, basis in enumerate(priority[priority.index(preferred) :]):
            a.obsm[f"X_{basis}"] = np.column_stack(
                [np.arange(a.n_obs) + i * 100, np.arange(a.n_obs)]
            )
        spec = gsc.pl.paga_compare(a, legend_fontweight="normal", show=False).to_dict()
        cells = next(
            (
                rows
                for rows in spec["datasets"].values()
                if rows and "_obs_id" in rows[0]
            )
        )
        np.testing.assert_array_equal(
            [r["_coord_0"] for r in cells], np.arange(a.n_obs)
        )
        a.obsm["custom"] = a.obsm[f"X_{preferred}"] + 5
        gsc.pl.paga_compare(a, basis="custom", legend_fontweight="normal", show=False)
        np.testing.assert_allclose(a.uns["paga"]["pos"][0], [9, 9])

    def test_reuses_parent_data_labels_aliases_and_independent_color_scales(self):
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
        assert spec["resolve"]["legend"] == {
            "default": "independent",
            "fill": "collected",
        }
        assert all(
            (
                points(embedding)["encoding"][axis]["scale"]["zoom"]
                for axis in ("x", "y")
            )
        )
        nodes = next(
            (rows for rows in spec["datasets"].values() if rows and "_cells" in rows[0])
        )
        assert [r["_label"] for r in nodes] == ["w", "x", "y", "z"]
        assert all(
            (
                m["mark"].get("tooltip") is None
                for m in leaf_marks(embedding) + leaf_marks(graph)
            )
        )
        labels = [m for m in leaf_marks(embedding) if m["mark"]["type"] == "text"]
        assert labels[0]["mark"]["fontWeight"] == "normal"
        np.testing.assert_array_equal(a.uns["paga"]["pos"], POSITIONS + 99)

    def test_no_analysis_expression_or_upstream_plotting_and_only_requested_cache_mutation(
        self, monkeypatch
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
            a.uns["paga"]["connectivities"].data,
            before.uns["paga"]["connectivities"].data,
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
            (
                {"transitions": "transitions_confidence"},
                NotImplementedError,
                "transitions",
            ),
            ({"title": 42}, TypeError, "title"),
            ({"title_graph": 42}, TypeError, "title_graph"),
        ],
    )
    def test_invalid_options_never_display_a_partial_comparison(
        self, monkeypatch, options, error, match
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
    def test_missing_or_misaligned_results_fail_explicitly(self, missing):
        a, options = (make_compare(), {})
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
