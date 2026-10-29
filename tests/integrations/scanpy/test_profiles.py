"""Profiles behavior and regressions."""

import warnings
from copy import deepcopy

import numpy as np
import pandas as pd
import pytest
from scipy import sparse

import genome_spy.integrations.scanpy as gsc
from genome_spy.integrations.scanpy._timeseries.data import (
    prepare_sim,
    prepare_timeseries,
)
from tests.integrations.scanpy.helpers import leaf_marks, points
from tests.integrations.scanpy.paga_fixtures import make_adjacency, make_compare
from tests.integrations.scanpy.profile_fixtures import (
    make_sim,
    sim_cases,
    timeseries_cases,
)
from tests.integrations.scanpy.qc_fixtures import make_hvg_result

pytest.importorskip("scanpy")


class TestTimeseries:
    """Time-series data semantics compared with the pinned public Scanpy helper."""

    @pytest.mark.reference
    @pytest.mark.parametrize("family", ["timeseries", "timeseries_subplot"])
    @pytest.mark.parametrize("case", timeseries_cases())
    def test_profiles_match_scanpy_positions_limits_colors_and_draw_order(
        self, family, case, monkeypatch
    ):
        import matplotlib.pyplot as plt
        import scanpy as sc

        X, options = timeseries_cases()[case]
        original = X.copy()
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            getattr(sc.pl, family)(X, **options)
        fig, ax = (plt.gcf(), plt.gcf().axes[0])
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
            (m for m in leaf_marks(spec) if m.get("mark", {}).get("type") == "point")
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
                [
                    rules[0]["encoding"]["y"]["datum"],
                    rules[0]["encoding"]["y2"]["datum"],
                ],
                rule_limits[0],
            )
        else:
            assert not rules
        np.testing.assert_array_equal(X, original)

    def test_wrapper_and_subplot_share_plotting_defaults_at_the_same_size(self):
        values = [[1, 2], [3, 4]]
        # Scanpy gives the wrapper and subplot different physical default sizes.
        options = {"width": 240, "height": 180, "show": False}
        assert (
            gsc.pl.timeseries(values, **options).to_dict()
            == gsc.pl.timeseries_subplot(values, **options).to_dict()
        )

    @pytest.mark.reference
    def test_subplot_keeps_explicit_upstream_arguments_and_native_defaults(self):
        import matplotlib as mpl
        import matplotlib.pyplot as plt
        import scanpy as sc

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

    def test_subplot_errors_name_the_requested_entry(self):
        for options, error in [
            ({"time": [1]}, ValueError),
            ({"marker": "^"}, NotImplementedError),
            ({"ax": None}, TypeError),
            ({"return_fig": True}, TypeError),
        ]:
            with pytest.raises(error, match="gsc\\.pl\\.timeseries_subplot:"):
                gsc.pl.timeseries_subplot([[1, 2], [3, 4]], show=False, **options)

    @pytest.mark.parametrize("family", ["timeseries", "timeseries_subplot"])
    def test_numeric_colors_do_not_read_a_series_palette(self, family):
        plot = getattr(gsc.pl, family)
        options = {"color": [0.2, 0.8], "show": False}
        expected = plot([1, 2], palette=None, **options).to_dict()
        actual = plot([1, 2], palette=object(), **options).to_dict()
        assert actual == expected

    def test_numeric_tables_masks_missingness_and_ids_are_preserved(self):
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
            (
                [[1, 2], [3, 4]],
                {"var_names": ["A", "A"]},
                NotImplementedError,
                "repeated",
            ),
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
        self, values, options, error, match
    ):
        with pytest.raises(error, match=match):
            gsc.pl.timeseries(values, show=False, **options)


class TestTimeseriesHeatmap:
    """Supplied profile order, cropped limits and the pinned heatmap contract."""

    @pytest.mark.reference
    @pytest.mark.parametrize("shape", [(5, 3), (1, 3), (5, 1), (1, 1)])
    def test_values_limits_labels_and_highlights_match_scanpy_without_analysis(
        self, shape, monkeypatch
    ):
        import matplotlib.pyplot as plt
        import scanpy as sc

        values = np.arange(np.prod(shape), dtype=float).reshape(shape)
        original = values.copy()
        labels = np.array([f"v{i}" for i in range(shape[1])])
        # Read the upstream reference only in tests; runtime never calls its renderer.
        sc.pl.timeseries_as_heatmap(
            values, var_names=labels, highlights_x=[-1, 0.25, 20]
        )
        ax = plt.gcf().axes[0]
        expected = np.asarray(ax.images[0].get_array())
        limits = {"x": ax.get_xlim(), "y": ax.get_ylim()}
        plt.close("all")
        monkeypatch.setattr(
            sc.pl,
            "timeseries_as_heatmap",
            lambda *a, **k: pytest.fail("Called upstream plot"),
        )
        spec = gsc.pl.timeseries_as_heatmap(
            values,
            var_names=labels,
            highlights_x=[-1, 0.25, 20],
            show_values=True,
            zoom="xy",
            show=False,
        ).to_dict()
        tables = [rows for rows in spec["datasets"].values() if "_value" in rows[0]]
        assert len(tables) == 1
        np.testing.assert_array_equal(
            np.array([r["_value"] for r in tables[0]]).reshape(shape[::-1]), expected
        )
        np.testing.assert_array_equal(values, original)
        assert [r["_row"] for r in tables[0][:: shape[0]]] == list(labels)
        assert [r["_column"] for r in tables[0][: shape[0]]] == [
            str(i) for i in range(shape[0])
        ]
        for axis in ("x", "y"):
            np.testing.assert_allclose(spec["scales"][axis]["domain"], limits[axis])
            assert spec["scales"][axis]["type"] == "linear"
            assert spec["scales"][axis]["zoom"] is True
        assert spec["scales"]["y"]["reverse"] is False
        tile = points(spec)
        assert tile["encoding"]["x"]["field"] == "_x0"
        assert tile["encoding"]["x2"]["field"] == "_x1"
        assert {
            step.get("as"): step.get("expr")
            for step in spec["spec"]["layer"][0]["transform"]
            if step["type"] == "formula"
        } == {
            "_x0": "datum._x - 0.5",
            "_x1": "datum._x + 0.5",
            "_y0": "datum._y - 0.5",
            "_y1": "datum._y + 0.5",
        }
        rule = next(
            (mark for mark in leaf_marks(spec) if mark["mark"]["type"] == "rule")
        )
        assert spec["datasets"][rule["data"]["name"]] == [
            {"position": h} for h in (-1, 0.25, 20)
        ]
        assert rule["encoding"]["y"]["datum"] == 0
        assert rule["encoding"]["y2"]["datum"] == shape[1]
        assert rule["mark"]["clip"] is True

    @pytest.mark.parametrize(
        "labels", [(), ["same", "same"], np.array([["A", "unused"], ["B", "unused"]])]
    )
    def test_repeated_default_and_two_dimensional_labels_preserve_slots(self, labels):
        spec = gsc.pl.timeseries_as_heatmap(
            [[1, 2], [3, 4]], var_names=labels, show=False
        ).to_dict()
        expected = (
            ["0", "1"]
            if not len(labels)
            else ["A", "B"]
            if isinstance(labels, np.ndarray)
            else labels
        )
        table = next(
            (rows for rows in spec["datasets"].values() if "_value" in rows[0])
        )
        assert [r["_row"] for r in table[::2]] == list(expected)

    def test_nan_and_masked_inputs_follow_scanpy_conversion_without_mutation(self):
        values = np.ma.array(
            [[1.0, np.nan], [3.0, 4.0]], mask=[[True, False], [False, False]]
        )
        before = values.copy()
        spec = gsc.pl.timeseries_as_heatmap(values, hover=False, show=False).to_dict()
        table = next(
            (rows for rows in spec["datasets"].values() if "_value" in rows[0])
        )
        assert [row["_value"] for row in table] == [1.0, 3.0, None, 4.0]
        assert points(spec)["mark"]["tooltip"] is None
        np.testing.assert_array_equal(values.data, before.data)
        np.testing.assert_array_equal(values.mask, before.mask)
        assert spec["spec"]["width"] == 372 and spec["spec"]["height"] == 616

    @pytest.mark.parametrize(
        "values,options,error,match",
        [
            ([1, 2], {}, ValueError, "two nonempty"),
            ([], {}, ValueError, "two nonempty"),
            (sparse.eye(2), {}, TypeError, "resident 2D"),
            ([[1j]], {}, TypeError, "real numbers"),
            ([["abc"]], {}, TypeError, "real numbers"),
            (pd.DataFrame({"A": ["1", "2"]}), {}, TypeError, "real numbers"),
            (pd.DataFrame({"A": [1j, 2j]}), {}, TypeError, "real numbers"),
            (
                pd.DataFrame({"A": pd.array([1, np.inf], dtype="Float64")}),
                {},
                ValueError,
                "finite or missing",
            ),
            ([[np.inf]], {}, ValueError, "finite or missing"),
            ([[np.nan]], {}, ValueError, "finite value"),
            ([[1, 2]], {"var_names": ["one"]}, ValueError, "2 labels"),
            ([[1, 2]], {"var_names": "AB"}, TypeError, "var_names"),
            ([[1]], {"var_names": np.zeros((1, 0))}, ValueError, "var_names"),
            ([[1]], {"highlights_x": [np.inf]}, ValueError, "highlights_x"),
            ([[1]], {"highlights_x": [True]}, ValueError, "highlights_x"),
            ([[1]], {"highlights_x": "1"}, TypeError, "highlights_x"),
            ([[1]], {"color_map": object()}, NotImplementedError, "color_map"),
            ([[1]], {"width": 0}, ValueError, "positive"),
            ([[1]], {"hover": "yes"}, TypeError, "hover"),
            ([[1]], {"show_values": "yes"}, TypeError, "show_values"),
            ([[1]], {"zoom": "x"}, TypeError, "zoom"),
            ([[1]], {"ax": None}, TypeError, "ax"),
        ],
    )
    def test_invalid_inputs_fail_clearly(self, values, options, error, match):
        with pytest.raises(error, match=match):
            gsc.pl.timeseries_as_heatmap(values, show=False, **options)

    def test_dataframe_metadata_does_not_implicitly_supply_labels(self):
        frame = pd.DataFrame({"B": [1, 2], "A": [3, 4]}, index=["z", "a"])
        spec = gsc.pl.timeseries_as_heatmap(frame, show=False).to_dict()
        table = next(
            (rows for rows in spec["datasets"].values() if "_value" in rows[0])
        )
        assert [r["_row"] for r in table] == ["0", "0", "1", "1"]
        assert [r["_value"] for r in table] == [1, 2, 3, 4]

    @pytest.mark.parametrize(
        "columns,expected",
        [
            (
                {
                    "B": pd.array([1, 2, 3], dtype="Int64"),
                    "A": pd.array([4, 5, 6], dtype="Int64"),
                },
                [[1, 2, 3], [4, 5, 6]],
            ),
            (
                {
                    "B": pd.array([1, 2, 3], dtype="Float64"),
                    "A": pd.array([4, 5, 6], dtype="Float64"),
                },
                [[1, 2, 3], [4, 5, 6]],
            ),
            (
                {"B": [True, False, True], "A": [4.5, 5.5, 6.5]},
                [[1, 0, 1], [4.5, 5.5, 6.5]],
            ),
            (
                {"B": pd.array([1, None, 3], dtype="Int64"), "A": [4, 5, 6]},
                [[1, np.nan, 3], [4, 5, 6]],
            ),
            (
                {"B": pd.array([1, None, 3], dtype="Float64"), "A": [4, 5, 6]},
                [[1, np.nan, 3], [4, 5, 6]],
            ),
        ],
        ids=[
            "nullable-int",
            "nullable-float",
            "mixed-bool-float",
            "missing-int",
            "missing-float",
        ],
    )
    def test_numeric_dataframe_types_preserve_values_and_input(self, columns, expected):
        frame = pd.DataFrame(columns, index=["z", "a", "m"])
        original = frame.copy(deep=True)
        spec = gsc.pl.timeseries_as_heatmap(
            frame, var_names=frame.columns, show=False
        ).to_dict()
        table = next(
            (rows for rows in spec["datasets"].values() if "_value" in rows[0])
        )
        np.testing.assert_allclose(
            np.array([row["_value"] for row in table], dtype=float).reshape(2, 3),
            expected,
            equal_nan=True,
        )
        assert [row["_row"] for row in table] == ["B"] * 3 + ["A"] * 3
        assert [row["_column"] for row in table] == ["0", "1", "2"] * 2
        pd.testing.assert_frame_equal(frame, original)

    def test_readonly_noncontiguous_view_keeps_supplied_order_and_data(self):
        base = np.arange(24).reshape(6, 4)
        values = base[::2, ::-1]
        values.setflags(write=False)
        spec = gsc.pl.timeseries_as_heatmap(values, show=False).to_dict()
        table = next(
            (rows for rows in spec["datasets"].values() if "_value" in rows[0])
        )
        np.testing.assert_array_equal(
            np.array([row["_value"] for row in table]).reshape(4, 3), values.T
        )
        np.testing.assert_array_equal(base, np.arange(24).reshape(6, 4))

    def test_lazy_matrix_is_rejected_before_materializing(self):

        class LazyMatrix:
            def __array__(self, *args, **kwargs):
                pytest.fail("Materialized lazy input")

        with pytest.raises(TypeError, match="resident 2D"):
            gsc.pl.timeseries_as_heatmap(LazyMatrix(), show=False)


class TestSim:
    """Simulation metadata, fixed shuffle and shared renderers against public Scanpy."""

    @pytest.mark.reference
    @pytest.mark.parametrize("case", sim_cases())
    def test_values_boundaries_ticks_and_limits_match_scanpy(self, case, monkeypatch):
        import matplotlib.pyplot as plt
        import scanpy as sc

        adata, options = (make_sim(), sim_cases()[case])
        before = adata.copy()
        state = np.random.get_state()
        try:
            with warnings.catch_warnings():
                warnings.simplefilter("ignore")
                sc.pl.sim(adata, show=False, **options)
            ax = plt.gcf().axes[0]
            heatmap = bool(ax.images)
            expected = (
                np.asarray(ax.images[0].get_array())
                if heatmap
                else np.ma.concatenate([c.get_offsets() for c in ax.collections])
            )
            limits = [ax.get_xlim(), ax.get_ylim()]
            ticks = ax.get_xticks().tolist()
            labels = [label.get_text() for label in ax.get_xticklabels()]
            highlights = [line.get_xdata()[0] for line in ax.lines]
            xlabel = ax.get_xlabel()
            plt.close("all")
        finally:
            np.random.set_state(state)
        monkeypatch.setattr(
            sc.pl, "sim", lambda *a, **k: pytest.fail("Called upstream renderer")
        )
        monkeypatch.setattr(sc.tl, "sim", lambda *a, **k: pytest.fail("Ran simulation"))
        spec = gsc.pl.sim(adata, show=False, **options).to_dict()
        mark = next(
            (
                m
                for m in leaf_marks(spec)
                if m.get("mark", {}).get("type") == ("rect" if heatmap else "point")
            )
        )
        table = spec["datasets"][mark["data"]["name"]]
        if heatmap:
            actual = np.array([r["_value"] for r in table]).reshape(
                adata.n_vars, adata.n_obs
            )
            scales = spec["scales"]
        else:
            actual = np.array([[r["_time"], r["_value"]] for r in table])
            scales = {axis: mark["encoding"][axis]["scale"] for axis in ("x", "y")}
        np.testing.assert_array_equal(actual, expected)
        for axis, domain in zip(("x", "y"), limits):
            np.testing.assert_allclose(scales[axis]["domain"], domain)
        rules = [m for m in leaf_marks(spec) if m.get("mark", {}).get("type") == "rule"]
        actual_highlights = spec["datasets"][rules[0]["data"]["name"]] if rules else []
        assert [r["position"] for r in actual_highlights] == highlights
        if not options.get("shuffle"):
            track = spec["surround"]["bottom"][0]
            rows = spec["datasets"][track["data"]["name"]]
            assert [r["position"] for r in rows] == ticks
            assert [r["label"] for r in rows] == labels
        assert mark["encoding"]["x"]["axis"]["title"] == (
            xlabel if options.get("shuffle") else None
        )
        np.testing.assert_array_equal(adata.X, before.X)
        assert adata.uns == before.uns and adata.var_names.equals(before.var_names)

    def test_length_fallback_and_shuffle_are_read_only_and_preserve_global_rng(self):
        adata = make_sim()
        del adata.uns["tmax_write"]
        _, boundaries, ticks = prepare_sim(adata, None, False)
        assert boundaries == [] and ticks == {0: "1"}
        state = np.random.get_state()
        expected = np.random.RandomState(1).choice(
            adata.n_obs, adata.n_obs, replace=False
        )
        for source in (adata, adata[:5]):
            before = source.X.copy()
            spec = gsc.pl.sim(source, shuffle=True, show=False).to_dict()
            mark = next((m for m in leaf_marks(spec) if m["mark"]["type"] == "point"))
            rows = spec["datasets"][mark["data"]["name"]]
            order = (
                expected
                if source is adata
                else np.random.RandomState(1).choice(5, 5, replace=False)
            )
            np.testing.assert_array_equal(
                [r["_value"] for r in rows], before[order].T.ravel()
            )
            np.testing.assert_array_equal(source.X, before)
        after = np.random.get_state()
        assert state[0] == after[0] and state[2:] == after[2:]
        np.testing.assert_array_equal(state[1], after[1])

    def test_backed_and_sparse_sources_are_rejected_before_loading(
        self, tmp_path, monkeypatch
    ):
        import anndata as ad

        adata = make_sim()
        adata.write_h5ad(tmp_path / "simulation.h5ad")
        backed = ad.read_h5ad(tmp_path / "simulation.h5ad", backed="r")
        try:
            sources = [backed, backed[:2]]
            with monkeypatch.context() as guarded:
                guarded.setattr(
                    ad.AnnData, "X", property(lambda self: pytest.fail("Read backed X"))
                )
                for source in sources:
                    with pytest.raises(TypeError, match="backed/lazy"):
                        gsc.pl.sim(source, show=False)
        finally:
            backed.file.close()
        adata.X = sparse.csr_matrix(adata.X)
        monkeypatch.setattr(
            sparse.csr_matrix,
            "toarray",
            lambda *a, **k: pytest.fail("Densified sparse X"),
        )
        with pytest.raises(TypeError, match="resident"):
            gsc.pl.sim(adata, show=False)

    @pytest.mark.parametrize("length", [0, -1, np.inf, np.nan, True, "3"])
    @pytest.mark.parametrize("stored", [False, True])
    def test_invalid_realization_lengths_fail_clearly(self, length, stored):
        adata = make_sim()
        options = {"tmax_realization": length}
        if stored:
            adata.uns["tmax_write"] = length
            options = {}
        with pytest.raises(ValueError, match="gsc\\.pl\\.sim:.*tmax"):
            gsc.pl.sim(adata, show=False, **options)

    @pytest.mark.parametrize(
        "options",
        [
            {"as_heatmap": 1},
            {"shuffle": "yes"},
            {"hover": 1},
            {"show_values": "yes"},
            {"zoom": "x"},
        ],
    )
    def test_invalid_flags_fail_before_optional_import(self, options, monkeypatch):
        monkeypatch.setattr(
            gsc.pl, "_require_scanpy", lambda *a: pytest.fail("Imported Scanpy")
        )
        with pytest.raises(TypeError, match="gsc\\.pl\\.sim:"):
            gsc.pl.sim(object(), **options)

    def test_point_value_labels_and_single_variable_profiles_fail_clearly(self):
        with pytest.raises(NotImplementedError, match="show_values"):
            gsc.pl.sim(make_sim(), show_values=True, show=False)
        with pytest.raises(ValueError, match="requires color"):
            gsc.pl.sim(make_sim()[:, :1], show=False)


class TestPresentation:
    """Native presentation options retain source values, IDs and analysis ownership."""

    def test_hvg_preview_reuses_stored_scores_and_keeps_saved_selection(self):
        frame = make_hvg_result()
        original = frame.copy(deep=True)
        base = gsc.pl.highly_variable_genes(frame, show=False).to_dict()
        preview = gsc.pl.highly_variable_genes(
            frame, threshold_slider=True, show=False
        ).to_dict()
        assert len(preview["datasets"]) == 2
        # Gene table plus one cutoff-rule record.
        genes = next(
            (rows for rows in preview["datasets"].values() if "_selected" in rows[0])
        )
        assert genes == next(iter(base["datasets"].values()))
        assert (
            len(preview["params"]) == 1
            and preview["params"][0]["bind"]["input"] == "range"
        )
        pd.testing.assert_frame_equal(frame, original)

    @pytest.mark.parametrize(
        "result",
        [
            lambda: make_hvg_result().assign(dispersions_norm=1),
            lambda: make_hvg_result().assign(dispersions_norm=np.nan),
        ],
    )
    def test_hvg_slider_requires_a_varying_stored_score(self, result):
        with pytest.raises(ValueError, match="varying normalized score"):
            gsc.pl.highly_variable_genes(result(), threshold_slider=True, show=False)

    @pytest.mark.parametrize("family", ["timeseries", "timeseries_subplot"])
    def test_focus_and_ruler_leave_profile_records_and_ids_unchanged(self, family):
        source = pd.DataFrame({"A": [1, np.nan, 3], "B": [4, 5, 6]})
        options = dict(var_names=source.columns, show=False)
        base = getattr(gsc.pl, family)(source, **options).to_dict()
        interactive = getattr(gsc.pl, family)(
            source, series_select=True, ruler=True, zoom=True, **options
        ).to_dict()
        assert interactive["datasets"] == base["datasets"]
        mark = leaf_marks(interactive)[0]
        assert mark["encoding"]["opacity"]["scale"] is None
        assert "zoomLevel" in mark["mark"]["size"]["expr"]
        assert len(interactive["params"]) == 2

    @pytest.mark.parametrize("labels", [["only one"], "ABC"])
    def test_adjacency_labels_must_cover_the_explicit_matrix_order(self, labels):
        with pytest.raises(ValueError, match="labels.*3 labels"):
            gsc.pl.paga_adjacency(make_adjacency(), labels=labels, show=False)

    def test_compare_uses_small_default_cells_and_respects_explicit_sizes(self):
        adata = make_compare()
        before = deepcopy(adata)
        for size in [None, 25]:
            spec = gsc.pl.paga_compare(
                adata,
                size=size,
                zoom=True,
                legend_fontweight="normal",
                add_pos=False,
                show=False,
            ).to_dict()
            cells = points(spec["hconcat"][0])
            records = spec["datasets"][cells["data"]["name"]]
            assert {r["_size_0"] for r in records} == {9 if size is None else size}
            assert "zoomLevel" in cells["encoding"]["size"]["scale"]["range"][1]["expr"]
        np.testing.assert_array_equal(adata.obsm["X_umap"], before.obsm["X_umap"])
        pd.testing.assert_frame_equal(adata.obs, before.obs)

    @pytest.mark.parametrize(
        "options",
        [
            {"shuffle": True, "connect": True},
            {"shuffle": True, "run_select": True},
            {"as_heatmap": True, "connect": True},
        ],
    )
    def test_simulation_controls_reject_modes_without_ordered_run_coordinates(
        self, options
    ):
        from tests.integrations.scanpy.profile_fixtures import make_sim

        with pytest.raises(NotImplementedError, match="gsc.pl.sim"):
            gsc.pl.sim(make_sim(), show=False, **options)

    @pytest.mark.parametrize("alias", ["color", "colors"])
    def test_edge_slider_rejects_degree_colors_instead_of_showing_stale_statistics(
        self, alias
    ):
        from tests.integrations.scanpy.paga_fixtures import make_paga

        with pytest.raises(NotImplementedError, match="graph-degree"):
            gsc.pl.paga(
                make_paga(), **{alias: "degree_solid"}, edge_slider=True, show=False
            )
