"""Qc behavior and regressions."""

import json
import subprocess
import sys
from copy import deepcopy

import anndata as ad
import numpy as np
import pandas as pd
import pytest
from scipy import sparse

import genome_spy.integrations.scanpy as gsc
from genome_spy.integrations.scanpy._qc.highest_expr_data import (
    prepare_highest_expression,
)
from genome_spy.integrations.scanpy._qc.scrublet_data import prepare_scrublet
from tests.integrations.scanpy.helpers import leaf_marks, units
from tests.integrations.scanpy.qc_fixtures import (
    make_counts,
    make_hvg_result,
    make_scrublet,
)

sc = pytest.importorskip("scanpy")


class TestHighestExpr:
    """Public Scanpy normalization, box statistics and native highest-expression contract."""

    def test_data_module_defers_the_optional_scanpy_import(self):
        subprocess.run(
            [
                sys.executable,
                "-c",
                "import sys; import genome_spy.integrations.scanpy._qc.highest_expr_data; assert 'scanpy' not in sys.modules",
            ],
            check=True,
        )

    @pytest.mark.reference
    @pytest.mark.parametrize("storage", ["dense", "csr", "csc"])
    @pytest.mark.parametrize("log,symbols", [(False, None), (True, "symbol")])
    def test_normalization_ranks_quartiles_whiskers_fliers_and_limits_match_scanpy(
        self, storage, log, symbols
    ):
        import matplotlib.pyplot as plt

        a = make_counts(storage)
        before = a.copy()
        reference = a.copy()
        with pytest.warns(UserWarning, match="zero counts"):
            ax = sc.pl.highest_expr_genes(
                reference, n_top=5, gene_symbols=symbols, log=log, show=False
            )
        with pytest.warns(UserWarning, match="zero counts"):
            boxes, fliers, limits = prepare_highest_expression(a, 5, None, symbols)
        assert boxes.gene.tolist() == [t.get_text() for t in ax.get_yticklabels()]
        for i, row in boxes.iterrows():
            vertices = ax.patches[i].get_path().vertices
            np.testing.assert_allclose(
                [row.q1, row.q3], [vertices[:, 0].min(), vertices[:, 0].max()]
            )
            lines = ax.lines[i * 6 : (i + 1) * 6]
            np.testing.assert_allclose(
                [row.lower, row.upper, row["median"]],
                [lines[j].get_xdata()[0] for j in (2, 3, 4)],
            )
            np.testing.assert_allclose(
                sorted(fliers.loc[fliers.gene == row.gene, "percent"]),
                sorted(lines[5].get_xdata()),
            )
        with pytest.warns(UserWarning, match="zero counts"):
            spec = gsc.pl.highest_expr_genes(
                a, n_top=5, gene_symbols=symbols, log=log, show=False
            ).to_dict()
        np.testing.assert_allclose(
            spec["layer"][0]["encoding"]["x"]["scale"]["domain"], ax.get_xlim()
        )
        assert spec["width"] == ax.get_window_extent().width
        plt.close(ax.figure)
        np.testing.assert_array_equal(
            a.X.toarray() if sparse.issparse(a.X) else a.X,
            before.X.toarray() if sparse.issparse(before.X) else before.X,
        )
        assert (
            a.obs.equals(before.obs)
            and a.var.equals(before.var)
            and (a.uns == before.uns)
        )

    def test_one_public_normalization_uses_layer_ignores_raw_and_preserves_views(
        self, monkeypatch
    ):
        a = make_counts("csr")
        a.layers["counts"] = a.X.copy()
        a.raw = ad.AnnData(sparse.csr_matrix(np.ones(a.shape)))
        a.X = sparse.csr_matrix(np.zeros(a.shape))
        view = a[1:, :]
        normalize, calls = (sc.pp.normalize_total, [])

        def observed(data, **options):
            calls.append(options)
            assert (
                data.X is view.layers["counts"]
                or (data.X != view.layers["counts"]).nnz == 0
            )
            return normalize(data, **options)

        monkeypatch.setattr(sc.pp, "normalize_total", observed)
        chart = gsc.pl.highest_expr_genes(view, n_top=2, layer="counts", show=False)
        assert view.is_view and calls == [{"target_sum": 100, "inplace": False}]
        rows = next(iter(chart.to_dict()["datasets"].values()))
        assert [r["gene"] for r in rows] == ["gene-4", "gene-2"]
        assert a.X.nnz == 0 and (not a.uns)

    def test_sparse_access_only_densifies_one_selected_column(self, monkeypatch):
        a = make_counts("csr")
        dense, shapes = (sparse.csr_matrix.toarray, [])

        def observed(matrix, *args, **kwargs):
            shapes.append(matrix.shape)
            assert matrix.shape == (21, 1)
            return dense(matrix, *args, **kwargs)

        monkeypatch.setattr(sparse.csr_matrix, "toarray", observed)
        with pytest.warns(UserWarning, match="zero counts"):
            gsc.pl.highest_expr_genes(a, n_top=2, show=False)
        assert shapes == [(21, 1), (21, 1)]

    @pytest.mark.parametrize("dtype", [np.int32, np.float32, np.float64])
    def test_percentages_use_all_genes_and_include_zero_cells(self, dtype):
        a = ad.AnnData(np.array([[0, 0, 0], [1, 1, 8], [2, 2, 6]], dtype=dtype))
        with pytest.warns(UserWarning, match="zero counts"):
            boxes, _, _ = prepare_highest_expression(a, 1, None, None)
        assert boxes.gene.tolist() == ["2"]
        np.testing.assert_allclose(boxes["mean"], [140 / 3], rtol=1e-06)
        np.testing.assert_allclose(boxes["median"], [60])

    @pytest.mark.parametrize(
        "options,error",
        [
            ({"color": "red"}, TypeError),
            ({"whis": 2}, TypeError),
            ({"n_top": 0}, ValueError),
            ({"n_top": True}, ValueError),
            ({"n_top": 1.5}, ValueError),
            ({"layer": 1}, TypeError),
            ({"gene_symbols": []}, TypeError),
            ({"log": 1}, TypeError),
            ({"zoom": "xy"}, TypeError),
        ],
    )
    def test_invalid_options_fail_before_optional_imports(
        self, monkeypatch, options, error
    ):
        monkeypatch.setattr(
            gsc.pl, "_require_scanpy", lambda *a: pytest.fail("Loaded Scanpy")
        )
        with pytest.raises(error, match="gsc.pl.highest_expr_genes"):
            gsc.pl.highest_expr_genes(object(), **options)

    @pytest.mark.parametrize("bad", [-1, np.nan, np.inf, 1j])
    def test_invalid_counts_fail_clearly(self, bad):
        a = ad.AnnData(np.array([[1, bad]]))
        with pytest.raises(ValueError, match="finite nonnegative"):
            gsc.pl.highest_expr_genes(a, show=False)

    def test_labels_sources_empty_and_backed_are_explicit(self, tmp_path):
        a = make_counts()
        for options, error, match in [
            ({"layer": "missing"}, ValueError, "layer"),
            ({"gene_symbols": "missing"}, ValueError, "gene_symbols"),
        ]:
            with pytest.raises(error, match=match):
                gsc.pl.highest_expr_genes(a, show=False, **options)
        a.var["symbol"] = ["same"] * 5
        with (
            pytest.warns(UserWarning, match="zero counts"),
            pytest.raises(NotImplementedError, match="unique"),
        ):
            gsc.pl.highest_expr_genes(a, gene_symbols="symbol", show=False)
        a.var["symbol"] = [None] * 5
        with (
            pytest.warns(UserWarning, match="zero counts"),
            pytest.raises(NotImplementedError, match="nonmissing"),
        ):
            gsc.pl.highest_expr_genes(a, gene_symbols="symbol", show=False)
        with pytest.raises(ValueError, match="at least one"):
            gsc.pl.highest_expr_genes(a[:0], show=False)
        path = tmp_path / "counts.h5ad"
        make_counts().write_h5ad(path)
        backed = ad.read_h5ad(path, backed="r")
        try:
            with pytest.raises(TypeError, match="backed/lazy"):
                gsc.pl.highest_expr_genes(backed, show=False)
        finally:
            backed.file.close()

    def test_all_zero_single_gene_large_n_top_and_snapshot(self):
        a = ad.AnnData(np.zeros((3, 1)))
        with pytest.warns(UserWarning, match="zero counts"):
            chart = gsc.pl.highest_expr_genes(a, show=False)
        spec = chart.to_dict()
        assert (
            len(spec["datasets"]) == 1
            and len(next(iter(spec["datasets"].values()))) == 1
        )
        assert all(
            (
                m["mark"]["tooltip"] is None
                for m in leaf_marks(
                    gsc.pl.highest_expr_genes(a, hover=False, show=False).to_dict()
                )
            )
        )
        snapshot = deepcopy(spec)
        a.X[:] = 10
        assert chart.to_dict() == snapshot
        a.X[:] = 0
        with (
            pytest.warns(UserWarning, match="zero counts"),
            pytest.raises(ValueError, match="positive percentages"),
        ):
            gsc.pl.highest_expr_genes(a, log=True, show=False)

    @pytest.mark.reference
    @pytest.mark.parametrize("counts", [[[1], [2], [3]], [[1, 1], [2, 2]]])
    @pytest.mark.parametrize("log", [False, True])
    def test_constant_percentage_domains_match_public_scanpy(self, counts, log):
        import matplotlib.pyplot as plt

        a = ad.AnnData(np.array(counts, dtype=float))
        ax = sc.pl.highest_expr_genes(a, log=log, show=False)
        spec = gsc.pl.highest_expr_genes(a, log=log, show=False).to_dict()
        np.testing.assert_allclose(
            spec["layer"][0]["encoding"]["x"]["scale"]["domain"], ax.get_xlim()
        )
        plt.close(ax.figure)

    def test_duplicate_cell_labels_keep_separate_outlier_ids(self):
        a = make_counts()
        a.obs_names = ["cell"] * a.n_obs
        with pytest.warns(UserWarning, match="zero counts"):
            _, fliers, _ = prepare_highest_expression(a, 5, None, None)
        assert fliers["cell"].unique().tolist() == ["cell"]
        assert set(fliers.cell_id) == {"row-0", "row-20"}


class TestHvg:
    """Stored variable-gene data, Scanpy defaults and native chart semantics."""

    @pytest.mark.reference
    @pytest.mark.parametrize(
        "storage,flavor",
        [
            ("frame", "seurat"),
            ("adata", "seurat"),
            ("records", "seurat"),
            ("frame", "seurat_v3"),
            ("adata", "seurat_v3"),
        ],
    )
    @pytest.mark.parametrize("log", [False, True])
    @pytest.mark.parametrize("selected", [False, True])
    def test_points_limits_labels_order_and_selection_match_scanpy(
        self, storage, flavor, log, selected
    ):
        import matplotlib.pyplot as plt

        result = make_hvg_result(storage, flavor)
        snapshot = deepcopy(result)
        with plt.rc_context({"figure.dpi": 100}):
            sc.pl.highly_variable_genes(
                result, log=log, highly_variable_genes=selected, show=False
            )
            axes = plt.gcf().axes
            spec = gsc.pl.highly_variable_genes(
                result, log=log, highly_variable_genes=selected, show=False
            ).to_dict()
            assert len(spec["datasets"]) == 1
            rows = next(iter(spec["datasets"].values()))
            for panel, ax in zip(units(spec), axes, strict=True):
                encoding = panel["encoding"]
                for axis in ("x", "y"):
                    np.testing.assert_allclose(
                        encoding[axis]["scale"]["domain"],
                        getattr(ax, f"get_{axis}lim")(),
                        rtol=1e-07,
                    )
                    assert encoding[axis]["axis"]["title"] == (
                        "Mean expression"
                        if axis == "x"
                        else (
                            "Normalized "
                            if encoding[axis]["field"].endswith("_norm")
                            else ""
                        )
                        + ("variance" if flavor == "seurat_v3" else "dispersion")
                    )
                    assert encoding[axis]["scale"]["type"] == (
                        "log" if log else "linear"
                    )
                for artist, flag in zip(ax.collections, (True, False), strict=True):
                    expected = artist.get_offsets()
                    actual = [
                        [r[encoding[axis]["field"]] for axis in ("x", "y")]
                        for r in rows
                        if r["_selected"] == flag
                    ]
                    np.testing.assert_allclose(actual, expected, rtol=1e-07)
                    assert panel["mark"]["size"] == 9
                    assert panel["mark"]["strokeWidth"] == 0
                assert panel["transform"][-1]["sort"] == {
                    "field": "_selected",
                    "order": "ascending",
                }
            plt.close("all")
        if storage == "frame":
            pd.testing.assert_frame_equal(result, snapshot)
        elif storage == "adata":
            pd.testing.assert_frame_equal(result.var, snapshot.var)
            assert result.uns == snapshot.uns
        else:
            np.testing.assert_array_equal(result, snapshot)

    def test_legacy_wrapper_reuses_the_same_native_chart(self):
        result = make_hvg_result("records")
        with pytest.deprecated_call(match="highly_variable_genes"):
            actual = gsc.pl.filter_genes_dispersion(result, show=False).to_dict()
        assert (
            actual
            == gsc.pl.highly_variable_genes(
                result, highly_variable_genes=False, show=False
            ).to_dict()
        )

    def test_chart_keeps_a_snapshot_when_the_supplied_results_change(self):
        result = make_hvg_result()
        chart = gsc.pl.highly_variable_genes(result, show=False)
        before = chart.to_dict()
        result.loc[:, "means"] = 99
        result.loc[:, "highly_variable"] = False
        assert chart.to_dict() == before

    def test_duplicate_gene_labels_keep_distinct_shared_point_ids(self):
        result = make_hvg_result()
        result.index = ["same"] * len(result)
        spec = gsc.pl.highly_variable_genes(result, show=False).to_dict()
        rows = next(iter(spec["datasets"].values()))
        assert [r["_obs_label"] for r in rows] == list(result.index)
        assert len({r["_obs_id"] for r in rows}) == len(result)
        assert len({panel["data"]["name"] for panel in units(spec)}) == 1

    def test_missing_values_are_filtered_per_panel_without_changing_stored_values(self):
        result = make_hvg_result()
        result.loc["gene-0", "dispersions_norm"] = np.nan
        spec = gsc.pl.highly_variable_genes(result, show=False).to_dict()
        rows = next(iter(spec["datasets"].values()))
        assert rows[0]["dispersions_norm"] is None
        assert rows[0]["dispersions"] == result.loc["gene-0", "dispersions"]
        first, second = units(spec)
        assert (
            first["transform"][0]["expr"]
            == "isValid(datum.means) && isValid(datum.dispersions_norm)"
        )
        assert (
            second["transform"][0]["expr"]
            == "isValid(datum.means) && isValid(datum.dispersions)"
        )
        assert spec["resolve"]["scale"]["x"] == "independent"

    @pytest.mark.reference
    def test_missing_value_panel_bounds_match_scanpy(self):
        import matplotlib.pyplot as plt

        result = make_hvg_result()
        result.loc["gene-0", "dispersions_norm"] = np.nan
        spec = gsc.pl.highly_variable_genes(result, show=False).to_dict()
        sc.pl.highly_variable_genes(result, show=False)
        for panel, ax in zip(units(spec), plt.gcf().axes, strict=True):
            np.testing.assert_allclose(
                panel["encoding"]["x"]["scale"]["domain"], ax.get_xlim()
            )
            np.testing.assert_allclose(
                panel["encoding"]["y"]["scale"]["domain"], ax.get_ylim()
            )
        assert spec["resolve"]["scale"]["x"] == "independent"
        plt.close("all")

    def test_log_limits_follow_raw_statistics_including_negative_normalized_values(
        self,
    ):
        result = make_hvg_result()
        result.loc["gene-0", ["dispersions", "dispersions_norm"]] = [-1, -3]
        spec = gsc.pl.highly_variable_genes(result, log=True, show=False).to_dict()
        for panel in units(spec):
            np.testing.assert_allclose(
                panel["encoding"]["y"]["scale"]["domain"],
                [0.1, 1.05 * result.dispersions.max()],
            )
            assert "> 0" in panel["transform"][0]["expr"]
        assert next(iter(spec["datasets"].values()))[0]["dispersions_norm"] == -3
        assert all(
            (
                type(v) is float
                for panel in units(spec)
                for axis in ("x", "y")
                for v in panel["encoding"][axis]["scale"]["domain"]
            )
        )
        json.dumps(spec)

    def test_backed_metadata_never_reads_expression_or_reruns_analysis(
        self, tmp_path, monkeypatch
    ):
        from anndata import AnnData, read_h5ad

        a = make_hvg_result("adata")
        path = tmp_path / "hvg.h5ad"
        a.write_h5ad(path)
        backed = read_h5ad(path, backed="r")

        def forbidden(*args, **kwargs):
            pytest.fail("Accessed expression or reran gene selection/plotting")

        for owner, name in [
            (sc.pp, "highly_variable_genes"),
            (sc.pp, "filter_genes_dispersion"),
            (sc.pl, "highly_variable_genes"),
            (sc.pl, "filter_genes_dispersion"),
        ]:
            monkeypatch.setattr(owner, name, forbidden)
        monkeypatch.setattr(AnnData, "X", property(forbidden))
        try:
            assert gsc.pl.highly_variable_genes(backed, show=False) is not None
            assert gsc.pl.highly_variable_genes(a[:, [1, 0]], show=False) is not None
        finally:
            backed.file.close()

    @pytest.mark.parametrize(
        "change,error,match",
        [
            (lambda x: x.drop(columns="means"), ValueError, "means"),
            (lambda x: x.assign(highly_variable=1), TypeError, "boolean"),
            (lambda x: x.assign(means=np.inf), ValueError, "finite"),
            (lambda x: x.assign(means="x"), TypeError, "real"),
            (lambda x: x.iloc[:0], ValueError, "one gene"),
            (
                lambda x: x.assign(
                    highly_variable=pd.array([True] * 7 + [None], dtype="boolean")
                ),
                TypeError,
                "nonmissing",
            ),
        ],
    )
    def test_invalid_stored_results_fail_clearly(self, change, error, match):
        with pytest.raises(error, match=match):
            gsc.pl.highly_variable_genes(change(make_hvg_result()), show=False)

    def test_missing_analysis_metadata_is_not_invented(self):
        a = make_hvg_result("adata")
        del a.uns["hvg"]
        with pytest.raises(ValueError, match="flavor.*explicitly"):
            gsc.pl.highly_variable_genes(a, show=False)

    @pytest.mark.parametrize(
        "family", ["highly_variable_genes", "filter_genes_dispersion"]
    )
    @pytest.mark.parametrize(
        "options,error", [({"zoom": "xy"}, TypeError), ({"log": None}, TypeError)]
    )
    def test_native_options_fail_before_optional_imports(
        self, monkeypatch, family, options, error
    ):
        monkeypatch.setattr(
            gsc.pl, "_require_scanpy", lambda *a: pytest.fail("Imported Scanpy")
        )
        with pytest.raises(error):
            getattr(gsc.pl, family)(object(), show=False, **options)

    @pytest.mark.parametrize("means", [0, -1, np.nan])
    def test_unsupported_log_bounds_fail_clearly(self, means):
        result = make_hvg_result().assign(means=means)
        with pytest.raises(NotImplementedError, match="log=True"):
            gsc.pl.highly_variable_genes(result, log=True, show=False)


class TestScrublet:
    """Stored histogram semantics, upstream defaults and native Scrublet charts."""

    @pytest.mark.reference
    @pytest.mark.parametrize("batched", [False, True])
    @pytest.mark.parametrize(
        "observed_scale,simulated_scale",
        [("log", "linear"), ("linear", "log"), ("linear", "linear"), ("log", "log")],
    )
    def test_bins_densities_thresholds_titles_limits_and_batches_match_scanpy(
        self, batched, observed_scale, simulated_scale
    ):
        import matplotlib.pyplot as plt

        a = make_scrublet(batched)
        with plt.rc_context(plt.rcParamsDefault):
            axes = np.asarray(
                sc.pl.scrublet_score_distribution(
                    a,
                    scale_hist_obs=observed_scale,
                    scale_hist_sim=simulated_scale,
                    show=False,
                )
            ).ravel()
        table, thresholds = prepare_scrublet(a)
        spec = gsc.pl.scrublet_score_distribution(
            a, scale_hist_obs=observed_scale, scale_hist_sim=simulated_scale, show=False
        ).to_dict()
        assert len(units(spec)) == len(axes) == (4 if batched else 2)
        assert len(table) == len(axes) * 49
        for i, (panel, ax) in enumerate(zip(units(spec), axes, strict=True)):
            rows = table[table.panel == i]
            np.testing.assert_allclose(
                rows.start, [p.get_x() for p in ax.patches], atol=2e-16
            )
            np.testing.assert_allclose(
                rows.end - rows.start, [p.get_width() for p in ax.patches]
            )
            np.testing.assert_allclose(
                rows.density, [p.get_height() for p in ax.patches], rtol=1e-14
            )
            assert panel["title"]["text"] == ax.get_title()
            bars = leaf_marks(panel)[0]
            for axis in ("x", "y"):
                np.testing.assert_allclose(
                    bars["encoding"][axis]["scale"]["domain"],
                    getattr(ax, f"get_{axis}lim")(),
                )
                assert (
                    bars["encoding"][axis]["axis"]["title"]
                    == getattr(ax, f"get_{axis}label")()
                )
            assert len(ax.lines) == int(thresholds[i] is not None)
            if ax.lines:
                np.testing.assert_allclose(ax.lines[0].get_xdata(), thresholds[i])
                assert leaf_marks(panel)[-1]["mark"]["type"] == "rule"
        if batched:
            assert table.batch.unique().tolist() == ["B", "A"] and thresholds == [
                0.27,
                0.27,
                None,
                None,
            ]
        plt.close(axes[0].figure)

    def test_denominator_ignores_missing_and_out_of_range_and_includes_right_edge(self):
        table, _ = prepare_scrublet(make_scrublet())
        rows = table[table.panel == 0]
        assert rows["count"].sum() == 10
        assert (
            rows.iloc[0]["count"] == 1
            and rows.iloc[1]["count"] == 1
            and (rows.iloc[-1]["count"] == 1)
        )
        np.testing.assert_allclose(np.sum(rows.density * (rows.end - rows.start)), 1)
        assert rows.density.max() == pytest.approx(3 * 49 / 10)

    @pytest.mark.reference
    @pytest.mark.parametrize("threshold", [-0.2, 0, 1, 1.4, None])
    @pytest.mark.parametrize("threshold_slider", [False, True])
    def test_thresholds_preserve_expanded_x_limits_and_density_limits(
        self, threshold, threshold_slider
    ):
        import matplotlib.pyplot as plt

        a = make_scrublet()
        a.uns["scrublet"]["threshold"] = threshold
        axes = sc.pl.scrublet_score_distribution(a, show=False)
        spec = gsc.pl.scrublet_score_distribution(
            a, threshold_slider=threshold_slider, show=False
        ).to_dict()
        if threshold_slider:
            control = spec["vconcat"][0]["params"][0]
            assert control["value"] == (0.5 if threshold is None else threshold)
            assert control["bind"]["min"] <= control["value"] <= control["bind"]["max"]
        for panel, ax in zip(units(spec), axes, strict=True):
            bars = leaf_marks(panel)[0]
            for axis in ("x", "y"):
                np.testing.assert_allclose(
                    bars["encoding"][axis]["scale"]["domain"],
                    getattr(ax, f"get_{axis}lim")(),
                )
        plt.close(axes[0].figure)

    @pytest.mark.reference
    def test_constant_log_histogram_uses_shared_domain_helper(self):
        import matplotlib.pyplot as plt

        a = make_scrublet()
        a.obs["doublet_score"] = 0.5
        axes = sc.pl.scrublet_score_distribution(a, show=False)
        spec = gsc.pl.scrublet_score_distribution(a, show=False).to_dict()
        np.testing.assert_allclose(
            leaf_marks(units(spec)[0])[0]["encoding"]["y"]["scale"]["domain"],
            axes[0].get_ylim(),
        )
        plt.close(axes[0].figure)

    def test_metadata_only_views_backed_and_no_analysis_fallback(
        self, monkeypatch, tmp_path
    ):
        a = make_scrublet()
        path = tmp_path / "stored.h5ad"
        a.write_h5ad(path)
        backed = ad.read_h5ad(path, backed="r")
        view = a[:10]
        monkeypatch.setattr(
            sc.pp, "scrublet", lambda *a, **k: pytest.fail("Reran Scrublet")
        )
        monkeypatch.setattr(
            ad.AnnData, "X", property(lambda *a: pytest.fail("Read expression"))
        )
        try:
            for data in (a, view, backed):
                assert gsc.pl.scrublet_score_distribution(data, show=False).to_dict()[
                    "datasets"
                ]
            assert view.is_view
            del a.uns["scrublet"]
            with pytest.raises(ValueError, match="run sc.pp.scrublet explicitly"):
                gsc.pl.scrublet_score_distribution(a, show=False)
        finally:
            backed.file.close()

    @pytest.mark.parametrize(
        "options,error",
        [
            ({"bins": 20}, TypeError),
            ({"scale_hist_obs": "symlog"}, NotImplementedError),
            ({"scale_hist_sim": "logit"}, NotImplementedError),
            ({"scale_hist_sim": 1}, NotImplementedError),
            ({"figsize": None}, TypeError),
            ({"figsize": (1, 1)}, ValueError),
            ({"figsize": (8, float("nan"))}, ValueError),
            ({"figsize": (10, 4), "width": 200}, TypeError),
            ({"zoom": "xy"}, TypeError),
            ({"threshold_slider": 1}, TypeError),
        ],
    )
    def test_unsupported_options_fail_before_dependencies(
        self, monkeypatch, options, error
    ):
        monkeypatch.setattr(
            gsc.pl, "_require_scanpy", lambda *a: pytest.fail("Loaded Scanpy")
        )
        with pytest.raises(error, match="gsc.pl.scrublet_score_distribution"):
            gsc.pl.scrublet_score_distribution(object(), **options)

    @pytest.mark.parametrize(
        "change,error,match",
        [
            (lambda a: a.uns.clear(), ValueError, "stored scrublet"),
            (lambda a: a.obs.pop("doublet_score"), ValueError, "doublet_score"),
            (
                lambda a: a.uns["scrublet"].pop("doublet_scores_sim"),
                ValueError,
                "doublet_scores_sim",
            ),
            (
                lambda a: a.uns["scrublet"].update(threshold=float("nan")),
                ValueError,
                "threshold",
            ),
            (
                lambda a: a.uns["scrublet"].update(doublet_scores_sim=[np.nan, 2, -1]),
                ValueError,
                "at least one score",
            ),
            (
                lambda a: a.uns["scrublet"].update(doublet_scores_sim=[[0.1, 0.2]]),
                TypeError,
                "one-dimensional",
            ),
            (
                lambda a: a.uns["scrublet"].update(doublet_scores_sim=[float("inf")]),
                ValueError,
                "finite",
            ),
            (
                lambda a: a.uns["scrublet"].update(doublet_scores_sim=["bad"]),
                TypeError,
                "real numbers",
            ),
            (
                lambda a: a.uns["scrublet"].update(batched_by="missing"),
                ValueError,
                "batched_by",
            ),
        ],
    )
    def test_invalid_results_fail_clearly(self, change, error, match):
        a = make_scrublet()
        change(a)
        with pytest.raises(error, match=match):
            gsc.pl.scrublet_score_distribution(a, show=False)

    def test_batch_order_missing_values_unused_categories_and_missing_results(self):
        a = make_scrublet(True)
        a.obs["sample"] = a.obs["sample"].astype(str)
        table, _ = prepare_scrublet(a)
        assert table.batch.unique().tolist() == ["A", "B"]
        a.obs.iloc[0, a.obs.columns.get_loc("sample")] = None
        table, _ = prepare_scrublet(a)
        assert table[table.panel == 0]["count"].sum() == 9
        a.obs["sample"] = pd.Categorical(
            a.obs["sample"], categories=["A", "B", "unused"]
        )
        with pytest.raises(NotImplementedError, match="unused batch"):
            prepare_scrublet(a)
        a = make_scrublet(True)
        del a.uns["scrublet"]["batches"]["A"]
        with pytest.raises(ValueError, match="batch 'A'"):
            prepare_scrublet(a)

    def test_native_dimensions_hover_and_chart_snapshot(self):
        a = make_scrublet()
        chart = gsc.pl.scrublet_score_distribution(
            a, figsize=(10, 4), hover=False, show=False
        )
        spec = chart.to_dict()
        assert all(
            (panel["width"] == 440 and panel["height"] == 310 for panel in units(spec))
        )
        assert all(
            (
                mark["mark"]["tooltip"] is None
                for panel in units(spec)
                for mark in leaf_marks(panel)
            )
        )
        snapshot = deepcopy(spec)
        a.uns["scrublet"]["doublet_scores_sim"][:] = 0
        a.obs["doublet_score"] = 0
        assert chart.to_dict() == snapshot

    def test_duplicate_metadata_columns_fail_with_plot_context(self):
        a = make_scrublet()
        a.obs = pd.concat([a.obs, a.obs], axis=1)
        with pytest.raises(
            ValueError,
            match="gsc.pl.scrublet_score_distribution: obs column names must be unique",
        ):
            gsc.pl.scrublet_score_distribution(a, show=False)

    @pytest.mark.parametrize("batched", [False, True])
    def test_slider_reuses_stored_bins_and_cutoffs_without_mutation(self, batched):
        a = make_scrublet(batched)
        before_obs, before_uns = (a.obs.copy(deep=True), deepcopy(a.uns))
        plain = gsc.pl.scrublet_score_distribution(a, show=False).to_dict()
        preview = gsc.pl.scrublet_score_distribution(
            a, threshold_slider=True, show=False
        ).to_dict()
        for datasets in (plain["datasets"], preview["datasets"]):
            bins = next(
                (rows for rows in datasets.values() if rows and "density" in rows[0])
            )
            assert bins == prepare_scrublet(a)[0].to_dict("records")
        pairs = preview["vconcat"]
        assert len(pairs) == (2 if batched else 1)
        assert [p["params"][0]["value"] for p in pairs] == (
            [0.27, 0.5] if batched else [0.3]
        )
        assert all((p["params"][0]["bind"]["input"] == "range" for p in pairs))
        assert all(("params" not in p for p in plain["vconcat"]))
        pd.testing.assert_frame_equal(a.obs, before_obs)
        np.testing.assert_equal(a.uns, before_uns)
