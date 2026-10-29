"""Dpt behavior and regressions."""

import warnings

import numpy as np
import pandas as pd
import pytest
from scipy import sparse

import genome_spy.integrations.scanpy as gsc
from tests.integrations.scanpy.helpers import leaf_marks
from tests.integrations.scanpy.profile_fixtures import (
    dpt_cases,
    dpt_profile_cases,
    dpt_reference,
    make_dpt,
    make_dpt_profiles,
)

pytest.importorskip("scanpy")


class TestDptGroups:
    """Stored DPT group/pseudotime semantics and metadata-only access."""

    @pytest.mark.parametrize("case", dpt_cases())
    def test_panels_match_public_scanpy_values_bounds_colors_ticks_and_order(
        self, case, monkeypatch
    ):
        import matplotlib.pyplot as plt
        import scanpy as sc
        from matplotlib.colors import to_rgba

        adata, options = (make_dpt(case), dpt_cases()[case])
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
                target,
                name,
                lambda *a, **k: pytest.fail("Ran upstream plotting/analysis"),
            )
        spec = gsc.pl.dpt_groups_pseudotime(adata, show=False, **options).to_dict()
        assert len(spec["vconcat"]) == 2
        assert spec["resolve"]["scale"] == {"default": "independent"}
        for panel, (offsets, xlim, ylim, yticks, collections) in zip(
            spec["vconcat"], expected, strict=True
        ):
            point = next((m for m in leaf_marks(panel) if m["mark"]["type"] == "point"))
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
            assert (
                len(rows) == adata.n_obs
                and len({r["_id"] for r in rows}) == adata.n_obs
            )
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
                                (
                                    ~np.ma.getmaskarray(c.get_offsets()).any(axis=1)
                                ).sum(),
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
        self, tmp_path, monkeypatch, backed
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
    def test_missing_analysis_is_an_error(self, field):
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
    def test_invalid_stored_metadata_fails_clearly(self, field, value, error):
        adata = make_dpt()
        if field == "dpt_changepoints":
            adata.uns[field] = value
        else:
            adata.obs[field] = value
        with pytest.raises(error, match="gsc\\.pl\\.dpt_groups_pseudotime:"):
            gsc.pl.dpt_groups_pseudotime(adata, show=False)

    @pytest.mark.parametrize("options,error", [({"zoom": "xy"}, TypeError)])
    def test_invalid_options_precede_optional_imports(
        self, options, error, monkeypatch
    ):
        monkeypatch.setattr(
            gsc.pl, "_require_scanpy", lambda *a: pytest.fail("Loaded Scanpy")
        )
        with pytest.raises(error, match="gsc\\.pl\\.dpt_groups_pseudotime:"):
            gsc.pl.dpt_groups_pseudotime(object(), **options)

    def test_native_group_guide_uses_observed_names_and_time_guide_uses_visible_range(
        self,
    ):
        a = make_dpt()
        a.obs.loc["cell-0", "dpt_order"] = np.nan
        a.obs.loc["cell-0", "dpt_pseudotime"] = -100
        spec = gsc.pl.dpt_groups_pseudotime(a, show=False).to_dict()
        group, time = [
            next((m for m in leaf_marks(p) if m["mark"]["type"] == "point"))
            for p in spec["vconcat"]
        ]
        assert group["encoding"]["fill"]["scale"]["domain"] == ["alpha", "beta"]
        guide = group["encoding"]["fill"]["legend"]
        assert guide["title"] == "DPT group" and guide["orient"] == "right"
        assert guide["symbolSize"] == 49
        assert time["encoding"]["fill"]["legend"]["title"] == "pseudotime"
        assert time["encoding"]["fill"]["scale"]["domain"] == [0.2, 1.0]

    def test_constant_pseudotime_uses_the_shared_expanded_native_guide(self):
        a = make_dpt()
        a.obs["dpt_pseudotime"] = 0.5
        spec = gsc.pl.dpt_groups_pseudotime(a, show=False).to_dict()
        fill = next(
            (m for m in leaf_marks(spec["vconcat"][1]) if m["mark"]["type"] == "point")
        )["encoding"]["fill"]
        assert fill["field"] == "_color" and fill["legend"]["title"] == "pseudotime"
        np.testing.assert_allclose(fill["scale"]["domain"], [0.45, 0.55])

    @pytest.mark.parametrize(
        "marker,shape", [(".", "circle"), ("o", "circle"), ("s", "square")]
    )
    def test_group_key_keeps_the_native_marker_shape(self, marker, shape):
        spec = gsc.pl.dpt_groups_pseudotime(
            make_dpt(), marker=marker, show=False
        ).to_dict()
        points = next(
            (m for m in leaf_marks(spec["vconcat"][0]) if m["mark"]["type"] == "point")
        )
        guide = points["encoding"]["fill"]["legend"]
        assert guide["symbolType"] == shape
        assert guide["symbolStrokeWidth"] == 0


class TestDptTimeseries:
    """Stored DPT expression ordering against public Scanpy, without analysis or mutation."""

    @pytest.mark.reference
    @pytest.mark.parametrize("case", dpt_profile_cases())
    def test_profiles_order_limits_labels_and_boundaries_match_public_scanpy(
        self, case, monkeypatch
    ):
        import matplotlib.pyplot as plt
        import scanpy as sc

        adata, options = (make_dpt_profiles(case), dpt_profile_cases()[case])
        before, obs = (adata.X.copy(), adata.obs.copy(deep=True))
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            sc.pl.dpt_timeseries(adata, show=False, **options)
        ax = plt.gcf().axes[0]
        heatmap = bool(ax.images)
        expected = (
            np.asarray(ax.images[0].get_array())
            if heatmap
            else np.ma.concatenate([c.get_offsets() for c in ax.collections])
        )
        limits = [ax.get_xlim(), ax.get_ylim()]
        boundaries = [line.get_xdata()[0] for line in ax.lines]
        xlabel = ax.get_xlabel()
        plt.close("all")
        for owner, name in [
            (sc.pl, "dpt_timeseries"),
            (sc.tl, "dpt"),
            (sc.tl, "diffmap"),
            (sc.pp, "neighbors"),
        ]:
            monkeypatch.setattr(
                owner,
                name,
                lambda *a, **k: pytest.fail("Ran upstream plotting/analysis"),
            )
        spec = gsc.pl.dpt_timeseries(adata, show=False, **options).to_dict()
        mark = next(
            (
                m
                for m in leaf_marks(spec)
                if m["mark"]["type"] == ("rect" if heatmap else "point")
            )
        )
        table = spec["datasets"][mark["data"]["name"]]
        actual = (
            np.array([r["_value"] for r in table]).reshape(adata.n_vars, -1)
            if heatmap
            else np.array([[r["_time"], r["_value"]] for r in table])
        )
        np.testing.assert_array_equal(actual, expected)
        scales = (
            spec["scales"]
            if heatmap
            else {a: mark["encoding"][a]["scale"] for a in ("x", "y")}
        )
        for axis, domain in zip(("x", "y"), limits, strict=True):
            np.testing.assert_allclose(scales[axis]["domain"], domain)
        rules = [m for m in leaf_marks(spec) if m["mark"]["type"] == "rule"]
        highlights = spec["datasets"][rules[0]["data"]["name"]] if rules else []
        assert [row["position"] for row in highlights] == boundaries
        if heatmap:
            assert any(
                (
                    m.get("encoding", {}).get("x", {}).get("axis", {}).get("title")
                    == xlabel
                    for m in leaf_marks(spec)
                )
            )
        else:
            assert mark["encoding"]["x"]["axis"]["title"] == xlabel
        np.testing.assert_array_equal(adata.X, before)
        pd.testing.assert_frame_equal(adata.obs, obs)
        assert adata.uns["dpt_changepoints"] == boundaries

    def test_gene_view_uses_x_and_saved_indices_without_raw_layers_or_other_dpt_fields(
        self, monkeypatch
    ):
        from anndata import AnnData

        source = make_dpt_profiles()
        source.raw = source
        adata = source[:, [1, 0]]
        expected = source.X[source.obs["dpt_order_indices"].to_numpy()][:, [1, 0]]
        monkeypatch.setattr(
            AnnData, "raw", property(lambda self: pytest.fail("Read raw"))
        )

        # AnnData 0.13 stores X under layers[None]; named layers must remain unread.
        def guard(getitem):

            def read(self, key):
                assert key is None, "Read a named layer"
                return getitem(self, key)

            return read

        for layer_type in {type(source.layers), type(adata.layers)}:
            monkeypatch.setattr(
                layer_type, "__getitem__", guard(layer_type.__getitem__)
            )
        spec = gsc.pl.dpt_timeseries(adata, show=False).to_dict()
        mark = next((m for m in leaf_marks(spec) if m["mark"]["type"] == "rect"))
        rows = spec["datasets"][mark["data"]["name"]]
        np.testing.assert_array_equal(
            np.array([r["_value"] for r in rows]).reshape(2, -1), expected.T
        )
        assert adata.is_view

    @pytest.mark.parametrize("field", ["dpt_order_indices", "dpt_changepoints"])
    def test_missing_metadata_errors_before_expression_access(self, field, monkeypatch):
        from anndata import AnnData

        adata = make_dpt_profiles()
        del (adata.obs if field == "dpt_order_indices" else adata.uns)[field]
        monkeypatch.setattr(
            AnnData, "X", property(lambda self: pytest.fail("Read expression"))
        )
        with pytest.raises(ValueError, match="run sc.tl.dpt"):
            gsc.pl.dpt_timeseries(adata, show=False)

    @pytest.mark.parametrize("indices", [[0.5] * 7, ["0"] * 7, [7] * 7, [-8] * 7])
    def test_invalid_indices_fail_without_reconstructing_an_order(self, indices):
        adata = make_dpt_profiles()
        adata.obs["dpt_order_indices"] = indices
        with pytest.raises(
            ValueError, match="gsc.pl.dpt_timeseries:.*valid row indices"
        ):
            gsc.pl.dpt_timeseries(adata, show=False)

    def test_backed_and_sparse_sources_fail_without_loading_or_densifying(
        self, tmp_path, monkeypatch
    ):
        from anndata import AnnData, read_h5ad

        adata = make_dpt_profiles()
        adata.write_h5ad(tmp_path / "dpt.h5ad")
        backed = read_h5ad(tmp_path / "dpt.h5ad", backed="r")
        try:
            with monkeypatch.context() as guarded:
                guarded.setattr(
                    AnnData, "X", property(lambda self: pytest.fail("Read backed X"))
                )
                with pytest.raises(TypeError, match="backed/lazy"):
                    gsc.pl.dpt_timeseries(backed, show=False)
        finally:
            backed.file.close()
        adata.X = sparse.csr_matrix(adata.X)
        monkeypatch.setattr(
            sparse.csr_matrix, "toarray", lambda *a, **k: pytest.fail("Densified X")
        )
        with pytest.raises(TypeError, match="resident"):
            gsc.pl.dpt_timeseries(adata, show=False)

    @pytest.mark.parametrize(
        "options,error",
        [
            ({"as_heatmap": 1}, TypeError),
            ({"show_values": 1}, TypeError),
            ({"zoom": "x"}, TypeError),
            ({"as_heatmap": False, "show_values": True}, NotImplementedError),
        ],
    )
    def test_invalid_flags_precede_optional_imports(self, options, error, monkeypatch):
        monkeypatch.setattr(
            gsc.pl, "_require_scanpy", lambda *a: pytest.fail("Imported Scanpy")
        )
        with pytest.raises(error, match="gsc\\.pl\\.dpt_timeseries:"):
            gsc.pl.dpt_timeseries(object(), **options)

    def test_single_gene_points_keep_the_parent_color_requirement(self):
        with pytest.raises(ValueError, match="one variable requires color"):
            gsc.pl.dpt_timeseries(
                make_dpt_profiles("single_gene"), as_heatmap=False, show=False
            )
