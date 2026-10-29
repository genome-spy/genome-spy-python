"""Ranked behavior and regressions."""

import json
import warnings
from copy import deepcopy
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

import genome_spy.integrations.scanpy as gsc
from genome_spy.integrations.scanpy._ranking.data import (
    ranked_features,
    ranked_statistic,
)
from tests.integrations.scanpy.helpers import points, scanpy_rank_labels, units
from tests.integrations.scanpy.ranked_fixture import make_ranked_adata, ranked_cases

sc = pytest.importorskip("scanpy")
RANKED_FAMILIES = ["dotplot", "matrixplot", "heatmap"]


def ranked_select(a, **options):
    """Select fixture markers with the public wrapper's default options."""
    return ranked_features(
        a,
        options.pop("groups", None),
        context="test",
        **{
            "n_genes": None,
            "groupby": None,
            "var_names": None,
            "gene_symbols": None,
            "min_logfoldchange": None,
            "key": None,
            **options,
        },
    )


class TestRanked:
    """Stored ranking semantics, native panel bounds and expression-plot delegation."""

    @pytest.mark.parametrize(
        "count,expected",
        [(2, ["g2", "g1"]), (-2, ["g3", "g4"]), (None, ["g2", "g1", "g3", "g4"])],
    )
    def test_stored_order_tail_and_repeated_slots_use_the_public_getter(
        self, monkeypatch, count, expected
    ):
        a = make_ranked_adata()
        before = deepcopy(a.uns)
        original, calls = (sc.get.rank_genes_groups_df, [])

        def get(adata, group, **kwargs):
            calls.append((group, kwargs))
            return original(adata, group, **kwargs)

        monkeypatch.setattr(sc.get, "rank_genes_groups_df", get)
        monkeypatch.setattr(
            sc.tl, "rank_genes_groups", lambda *a, **k: pytest.fail("Ran ranking")
        )
        markers, groupby = ranked_select(a, groups=["A", "C"], n_genes=count)
        assert list(markers) == ["A", "C"] and groupby == "group"
        assert markers["C"] == expected
        assert len(calls) == 1 and calls[0][0] == ["A", "C"]
        assert calls[0][1] == {
            "key": "rank_genes_groups",
            "gene_symbols": None,
            "log2fc_min": None,
        }
        for field in ("names", "scores", "logfoldchanges", "pvals", "pvals_adj"):
            np.testing.assert_array_equal(
                a.uns["rank_genes_groups"][field], before["rank_genes_groups"][field]
            )

    def test_strict_filter_symbols_filtered_names_and_custom_key(self):
        a = make_ranked_adata()
        a.uns["custom"] = a.uns.pop("rank_genes_groups")
        assert ranked_select(
            a, key="custom", groups="C", n_genes=4, min_logfoldchange=1
        )[0] == {"C": ["g2"]}
        assert ranked_select(
            a, key="custom", groups="C", n_genes=2, gene_symbols="symbol"
        )[0] == {"C": ["S2", "S1"]}
        names = a.uns["custom"]["names"].astype(
            [(g, object) for g in ["C", "A", "D", "B"]]
        )
        names["C"][0] = np.nan
        a.uns["custom"]["names"] = names
        assert ranked_select(a, key="custom", groups="C", n_genes=2)[0] == {
            "C": ["g1", "g3"]
        }

    def test_selection_uses_the_public_getters_returned_names(self, monkeypatch):
        original = sc.get.rank_genes_groups_df

        def get(*args, **kwargs):
            frame = original(*args, **kwargs)
            frame.loc[frame.index[0], "names"] = "g4"
            return frame

        monkeypatch.setattr(sc.get, "rank_genes_groups_df", get)
        assert ranked_select(make_ranked_adata(), groups="C", n_genes=1)[0] == {
            "C": ["g4"]
        }

    @pytest.mark.parametrize("family", RANKED_FAMILIES)
    @pytest.mark.parametrize("tail", [False, True])
    def test_ranked_wrapper_is_the_parent_chart_with_selected_markers(
        self, monkeypatch, family, tail
    ):
        a = make_ranked_adata()
        monkeypatch.setattr(
            sc.tl, "rank_genes_groups", lambda *a, **k: pytest.fail("Ran ranking")
        )
        count = -2 if tail else 2
        markers, groupby = ranked_select(a, n_genes=count)
        flags = {
            "zoom": "xy",
            "highlight" if family == "dotplot" else "show_values": True,
        }
        options = {
            "dendrogram": False,
            "layer": "counts",
            "standard_scale": "var",
            "show": False,
            **flags,
        }
        if family == "heatmap":
            options["group_gap"] = 0 if tail else 7
        ranked = getattr(gsc.pl, f"rank_genes_groups_{family}")(
            a, n_genes=count, **options
        )
        parent = getattr(gsc.pl, family)(a, markers, groupby, **options)
        assert ranked.to_dict() == parent.to_dict()

    @pytest.mark.parametrize("family", RANKED_FAMILIES)
    def test_explicit_markers_and_requested_rank_groups_keep_all_expression_groups(
        self, family
    ):
        a = make_ranked_adata()
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", UserWarning)
            chart = getattr(gsc.pl, f"rank_genes_groups_{family}")(
                a, groups="C", n_genes=1, dendrogram=False, show=False
            )
        records = next(
            (
                rows
                for rows in chart.to_dict()["datasets"].values()
                if "_group" in rows[0]
            )
        )
        assert set((r["_group"] for r in records)) == {"C", "A", "D", "B"}
        assert set((r["_gene"] for r in records)) == {"g2"}
        chart = getattr(gsc.pl, f"rank_genes_groups_{family}")(
            a, var_names={"manual": ["g1", "g1"]}, dendrogram=False, show=False
        )
        parent = getattr(gsc.pl, family)(
            a, {"manual": ["g1", "g1"]}, "group", dendrogram=False, show=False
        )
        assert chart.to_dict() == parent.to_dict()

    @pytest.mark.parametrize(
        "options,message",
        [
            ({"groups": ["missing"]}, "groups are missing"),
            ({"groups": ["C", "C"]}, "distinct"),
            ({"n_genes": 0}, "nonzero"),
            ({"n_genes": True}, "nonzero"),
            ({"n_genes": 1, "var_names": ["g1"]}, "mutually exclusive"),
            ({"min_logfoldchange": 100}, "no ranked genes"),
        ],
    )
    def test_invalid_selections_fail_clearly(self, options, message):
        with pytest.raises(ValueError, match=message):
            ranked_select(make_ranked_adata(), **options)

    def test_missing_analysis_or_metrics_never_trigger_computation(self, monkeypatch):
        a = make_ranked_adata()
        monkeypatch.setattr(
            sc.tl, "rank_genes_groups", lambda *a, **k: pytest.fail("Ran ranking")
        )
        del a.uns["rank_genes_groups"]["pvals_adj"]
        with pytest.raises(ValueError, match="pvals_adj"):
            ranked_select(a)
        a.uns.clear()
        with pytest.raises(ValueError, match="run sc.tl.rank_genes_groups explicitly"):
            ranked_select(a)

    def test_malformed_scores_and_nonfinite_panel_values_fail_without_repair(self):
        a = make_ranked_adata()
        a.uns["rank_genes_groups"]["scores"] = a.uns["rank_genes_groups"]["scores"][:2]
        with pytest.raises(ValueError, match="scores must match"):
            gsc.pl.rank_genes_groups(a, show=False)
        a = make_ranked_adata()
        a.uns["rank_genes_groups"]["scores"]["C"][0] = np.nan
        with pytest.raises(ValueError, match="finite scores"):
            gsc.pl.rank_genes_groups(a, groups="C", show=False)

    def test_metric_fields_are_matched_by_group_name_not_array_field_order(self):
        a = make_ranked_adata()
        result = a.uns["rank_genes_groups"]
        for field in ("scores", "logfoldchanges", "pvals", "pvals_adj"):
            result[field] = result[field][["B", "D", "A", "C"]]
        assert ranked_select(a, groups=["C", "A"], n_genes=2)[0] == {
            "C": ["g2", "g1"],
            "A": ["g2", "g4"],
        }

    def test_stored_score_panels_work_with_backed_data_and_views(self, tmp_path):
        import anndata as ad

        path = tmp_path / "ranked.h5ad"
        make_ranked_adata().write_h5ad(path)
        backed = ad.read_h5ad(path, backed="r")
        try:
            for data in (backed, backed[:4]):
                chart = gsc.pl.rank_genes_groups(
                    data, groups="C", n_genes=2, gene_symbols="symbol", show=False
                )
                spec = chart.to_dict()
                assert [
                    r["_label"] for r in spec["datasets"][spec["data"]["name"]]
                ] == ["S2", "S1"]
        finally:
            backed.file.close()

    def test_packaged_logreg_results_and_unavailable_fold_change_filter(self):
        a = sc.datasets.pbmc68k_reduced()
        markers, grouping = ranked_select(a, n_genes=2)
        assert len(markers) == 10 and grouping == "bulk_labels"
        assert (
            markers[next(iter(markers))]
            == a.uns["rank_genes_groups"]["names"][next(iter(markers))][:2].tolist()
        )
        with pytest.raises(ValueError, match="logreg results have none"):
            ranked_select(a, min_logfoldchange=1)

    @pytest.mark.parametrize("sharey", [False, True])
    def test_score_panels_keep_stored_order_symbols_titles_and_score_bounds(
        self, sharey
    ):
        a = make_ranked_adata()
        a.var["symbol"] = ["different"] * 4
        chart = gsc.pl.rank_genes_groups(
            a,
            ["A", "C"],
            n_genes=2,
            gene_symbols="symbol",
            sharey=sharey,
            n_panels_per_row=2,
            show=False,
        )
        spec = chart.to_dict()
        panels = units(spec)
        assert [p["title"] for p in panels] == ["A vs. rest", "C vs. rest"]
        rows = [spec["datasets"][p["data"]["name"]] for p in panels]
        assert [[r["_label"] for r in table] for table in rows] == [
            ["S2", "S4"],
            ["S2", "S1"],
        ]
        assert [[r["_score"] for r in table] for table in rows] == [[6, 3], [4, 2]]
        assert [p["encoding"]["y"]["scale"]["domain"] for p in panels] == (
            [[2, 7.2], [2, 7.2]] if sharey else [[3, 6.9], [2, 4.6]]
        )
        assert all(
            (p["encoding"]["x"]["scale"]["domain"] == [-0.9, 1.9] for p in panels)
        )

    def test_ranking_supplied_dictionary_log_and_numbered_labels(self):
        a = make_ranked_adata()
        spec = gsc.pl.ranking(
            a,
            "uns",
            "score_name",
            dictionary="provided",
            labels="L",
            log=True,
            n_points=2,
            show=False,
        ).to_dict()
        rows = spec["datasets"][spec["data"]["name"]]
        assert [r["_label"] for r in rows] == ["L4", "L6", "L2"]
        np.testing.assert_allclose([r["_score"] for r in rows], np.log([8, 7, 4]))
        assert spec["title"] == "score name"

    def test_ranking_indices_and_extreme_gap_match_scanpy(self):
        a = make_ranked_adata()
        a.varm["PCs"] = np.array([[4, 1], [2, 2], [8, 3], [6, 4]])
        spec = gsc.pl.ranking(
            a,
            "varm",
            "PCs",
            indices=[1, 0],
            n_points=2,
            include_lowest=True,
            show=False,
        ).to_dict()
        panels = units(spec)
        assert [p["title"] for p in panels] == ["PC2", "PC1"]
        rows = spec["datasets"][panels[0]["data"]["name"]]
        assert [(r["_rank"], r["_label"], r["_score"]) for r in rows] == [
            (0, "g4", 4),
            (1, "⋮", 2.5),
            (3, "g1", 1),
        ]
        assert panels[0]["encoding"]["x"]["axis"]["labels"] is False

    @pytest.mark.parametrize("family", ["dotplot", "matrixplot"])
    def test_invalid_metric_colors_fail_instead_of_falling_back_to_expression(
        self, family
    ):
        with pytest.raises(ValueError, match="values_to_plot"):
            getattr(gsc.pl, f"rank_genes_groups_{family}")(
                make_ranked_adata(), values_to_plot="unknown", show=False
            )

    @pytest.mark.reference
    @pytest.mark.parametrize("case", ranked_cases())
    def test_rank_data_and_guides_match_scanpy_with_documented_pca_label_space(
        self, case
    ):
        manifest = json.loads(
            (Path(__file__).with_name("fixtures") / "ranked.json").read_text()
        )
        reference = manifest["cases"][case]["panels"]
        family, args, options = ranked_cases()[case]
        spec = getattr(gsc.pl, family)(
            make_ranked_adata(), *args, show=False, **options
        ).to_dict()
        panels = units(spec)
        assert len(panels) == len(reference)
        upstream = scanpy_rank_labels(family, make_ranked_adata(), *args, **options)
        for panel, expected, labels in zip(panels, reference, upstream, strict=True):
            rows = spec["datasets"][panel["data"]["name"]]
            assert [(r["_rank"], r["_label"], r["_score"]) for r in rows] == labels
            # Frozen fixtures retain every label and score, allowing only tied reordering.
            assert sorted(((r["_label"], r["_score"]) for r in rows)) == sorted(
                ((label["text"], label["position"][1]) for label in expected["labels"])
            )
            assert [[r["_rank"], r["_score"]] for r in rows] == [
                label["position"] for label in expected["labels"]
            ]
            for axis in ("x", "y"):
                domain = list(expected[f"{axis}_domain"])
                if axis == "y" and family in ("pca_loadings", "pca_variance_ratio"):
                    # PCA reserves room above scores for the rotated labels.
                    domain[1] += 0.3 * (domain[1] - domain[0])
                np.testing.assert_allclose(
                    panel["encoding"][axis]["scale"]["domain"], domain
                )
                assert panel["encoding"][axis]["axis"]["title"] == (
                    expected[f"{axis}label"] or None
                )
            assert panel["title"] == expected["title"]

    @pytest.mark.parametrize(
        "show,autoshow", [(False, True), (True, False), (None, True), (None, False)]
    )
    def test_ranking_display_keeps_scanpy_autoshow_and_ignores_autosave(
        self, monkeypatch, show, autoshow
    ):
        from genome_spy.chart import TopLevelSpec

        displayed = []
        monkeypatch.setattr(
            TopLevelSpec, "display", lambda self: displayed.append(self)
        )
        monkeypatch.setattr(sc.settings, "_autoshow", autoshow)
        monkeypatch.setattr(sc.settings, "_autosave", True)
        result = gsc.pl.ranking(
            make_ranked_adata(), "uns", "score_name", dictionary="provided", show=show
        )
        assert len(displayed) == (autoshow if show is None else show)
        assert (result is None) == bool(displayed)

    @pytest.mark.parametrize(
        "family,metric",
        [
            ("dotplot", None),
            ("matrixplot", None),
            ("heatmap", None),
            ("dotplot", "scores"),
            ("matrixplot", "scores"),
        ],
    )
    def test_large_sparse_ranked_plots_only_read_the_selected_genes(
        self, monkeypatch, family, metric
    ):
        import anndata as ad
        import pandas as pd
        from scipy import sparse

        a = ad.AnnData(
            sparse.csr_matrix((100000, 20000), dtype=np.float32),
            obs=pd.DataFrame(
                {"group": pd.Categorical(["C", "A", "D", "B"] * 25000)},
                index=[f"c{i}" for i in range(100000)],
            ),
        )
        a.var_names = [f"g{i + 1}" for i in range(a.n_vars)]
        a.uns["rank_genes_groups"] = make_ranked_adata().uns["rank_genes_groups"]
        if metric is not None:
            result = a.uns["rank_genes_groups"]
            # Append complete ranks without changing the first four marker positions.
            for field in ("names", "scores", "logfoldchanges", "pvals", "pvals_adj"):
                first = result[field]
                rest = [
                    a.var_names[4:].tolist()
                    if field == "names"
                    else np.zeros(a.n_vars - 4)
                    for _ in first.dtype.names
                ]
                result[field] = np.concatenate(
                    [first, np.rec.fromarrays(rest, names=first.dtype.names)]
                )
        original, shapes = (sparse.csr_matrix.toarray, [])

        def selected(matrix, *args, **kwargs):
            shapes.append(matrix.shape)
            assert matrix.shape[1] <= 4, "Densified unrequested genes"
            return original(matrix, *args, **kwargs)

        monkeypatch.setattr(sparse.csr_matrix, "toarray", selected)
        if family == "heatmap":
            from genome_spy import Chart
            from genome_spy.integrations.scanpy._expression import heatmap_chart

            displayed = []

            def render(prepared, *args, **kwargs):
                displayed.append(prepared.values.shape)
                return Chart().mark_rect()

            monkeypatch.setattr(heatmap_chart, "build_heatmap", render)
            gsc.pl.rank_genes_groups_heatmap(a, n_genes=2, dendrogram=False, show=False)
            assert shapes == [(100000, 4)]
            assert displayed == [(100000, 8)]
        else:
            chart = getattr(gsc.pl, f"rank_genes_groups_{family}")(
                a,
                n_genes=2,
                dendrogram=False,
                show=False,
                values_to_plot=metric,
                **{"dot_max": 1} if family == "dotplot" else {},
            )
            assert shapes == [(0 if family == "matrixplot" and metric else 100000, 4)]
            assert (
                len(
                    next(
                        (
                            rows
                            for rows in chart.to_dict()["datasets"].values()
                            if "_mean" in rows[0]
                        )
                    )
                )
                == 32
            )


RANKED_STATISTICS_METRICS = [
    "scores",
    "logfoldchanges",
    "pvals",
    "pvals_adj",
    "log10_pvals",
    "log10_pvals_adj",
]


def ranked_statistics_statistic(a, metric="scores", markers=None, **options):
    """Read a small color table with explicit repeated fixture slots."""
    return ranked_statistic(
        a,
        ["g2", "g4", "g2", "g1"] if markers is None else markers,
        metric,
        key=options.pop("key", None),
        gene_symbols=options.pop("gene_symbols", None),
        context="test",
        **options,
    )


class TestRankedStatistics:
    """Stored statistic colors remain separate from expression summaries and sizes."""

    @pytest.mark.parametrize("family", ["dotplot", "matrixplot"])
    def test_one_ranking_read_preserves_unfiltered_colors_and_avoids_unused_expression(
        self, monkeypatch, family
    ):
        a = make_ranked_adata()
        ranking, expression = (sc.get.rank_genes_groups_df, sc.get.obs_df)
        calls, reads = ([], [])

        def ranked(*args, **kwargs):
            calls.append(args[1])
            return ranking(*args, **kwargs)

        def read(adata, keys, **kwargs):
            reads.append((adata.n_obs, list(keys)))
            return expression(adata, keys, **kwargs)

        monkeypatch.setattr(sc.get, "rank_genes_groups_df", ranked)
        monkeypatch.setattr(sc.get, "obs_df", read)
        chart = getattr(gsc.pl, f"rank_genes_groups_{family}")(
            a,
            groups=["A", "C"],
            n_genes=1,
            min_logfoldchange=1,
            values_to_plot="scores",
            dendrogram=False,
            show=False,
        ).to_dict()
        assert calls == [["C", "A", "D", "B"]]
        rows = next((rows for rows in chart["datasets"].values() if "_mean" in rows[0]))
        assert {r["_gene"] for r in rows} == {"g2"}
        assert {r["_group"]: r["_mean"] for r in rows} == {
            "C": 4,
            "A": 6,
            "D": -1,
            "B": 1,
        }
        if family == "matrixplot":
            assert reads == [(0, ["group", "g2"]), (8, ["group"])]
        else:
            assert reads == [(8, ["group", "g2"])]

    def test_score_colors_are_by_gene_not_rank_and_use_all_groups(self, monkeypatch):
        a = make_ranked_adata()
        before = deepcopy(a.uns["rank_genes_groups"])
        getter, calls = (sc.get.rank_genes_groups_df, [])

        def get(*args, **kwargs):
            calls.append(args[1])
            frame = getter(*args, **kwargs)
            frame.loc[(frame["group"] == "C") & (frame["names"] == "g2"), "scores"] = 42
            return frame

        monkeypatch.setattr(sc.get, "rank_genes_groups_df", get)
        colors = ranked_statistics_statistic(a)
        assert calls == [["C", "A", "D", "B"]]
        assert colors.index.tolist() == ["A", "B", "C", "D"]
        assert colors.columns.tolist() == ["g2", "g4", "g2", "g1"]
        np.testing.assert_array_equal(
            colors, [[6, 3, 6, 0], [1, 8, 1, -4], [42, -3, 42, 2], [-1, 0, -1, 2]]
        )
        for key in ("names", "scores", "pvals", "pvals_adj", "logfoldchanges"):
            np.testing.assert_array_equal(a.uns["rank_genes_groups"][key], before[key])

    @pytest.mark.parametrize("metric", RANKED_STATISTICS_METRICS)
    @pytest.mark.parametrize("symbols", [False, True])
    def test_color_table_matches_pinned_scanpy_public_getter_and_transform(
        self, metric, symbols
    ):
        from scanpy.plotting._tools import _get_values_to_plot

        a = make_ranked_adata()
        genes = ["S2", "S4", "S2", "S1"] if symbols else ["g2", "g4", "g2", "g1"]
        symbol_key = "symbol" if symbols else None
        expected = _get_values_to_plot(a, metric, genes, gene_symbols=symbol_key)
        actual = ranked_statistics_statistic(a, metric, genes, gene_symbols=symbol_key)
        pd.testing.assert_frame_equal(actual, expected, check_names=False)

    @pytest.mark.parametrize("family", ["dotplot", "matrixplot"])
    @pytest.mark.parametrize("metric", RANKED_STATISTICS_METRICS)
    @pytest.mark.parametrize("swapped", [False, True])
    def test_metric_wrappers_delegate_to_supplied_tables_with_parent_scaling(
        self, family, metric, swapped
    ):
        a = make_ranked_adata()
        colors = ranked_statistics_statistic(a, metric)
        markers = {"A": ["g2", "g4"], "C": ["g2", "g1"]}
        title = (
            "log fold change"
            if metric == "logfoldchanges"
            else metric.replace("_", " ").replace("pvals", "p-value")
        )
        options = dict(
            dendrogram=True,
            swap_axes=swapped,
            standard_scale="var",
            layer="counts",
            log=True,
            zoom=True,
            show=False,
            **{"highlight": True} if family == "dotplot" else {"show_values": True},
        )
        actual = getattr(gsc.pl, f"rank_genes_groups_{family}")(
            a, groups=["A", "C"], n_genes=2, values_to_plot=metric, **options
        )
        expected = getattr(gsc.pl, family)(
            a,
            markers,
            "group",
            colorbar_title=title,
            **options,
            **{"dot_color_df" if family == "dotplot" else "values_df": colors},
        )
        assert actual.to_dict() == expected.to_dict()

    @pytest.mark.parametrize("source", [{}, {"use_raw": False}, {"layer": "counts"}])
    def test_stored_source_does_not_override_expression_sizes(self, source):
        a = make_ranked_adata()
        a.X[:] = 0
        a.layers["counts"][:] = 5
        a.uns["rank_genes_groups"]["params"].update(use_raw=False, layer="counts")
        options = dict(
            var_names=["g2"],
            expression_cutoff=1,
            dot_max=1,
            dendrogram=False,
            show=False,
        )
        colored = gsc.pl.rank_genes_groups_dotplot(
            a, values_to_plot="scores", **options, **source
        ).to_dict()
        plain = gsc.pl.rank_genes_groups_dotplot(a, **options, **source).to_dict()
        actual = colored["datasets"][points(colored)["data"]["name"]]
        expected = plain["datasets"][points(plain)["data"]["name"]]
        assert [r["_percent"] for r in actual] == [r["_percent"] for r in expected]
        assert [r["_mean"] for r in actual] == [4, 6, -1, 1]
        assert len(actual) == 4

    def test_explicit_symbols_custom_key_tail_and_threshold_only_select_slots(self):
        a = make_ranked_adata()
        a.uns["custom"] = a.uns.pop("rank_genes_groups")
        options = dict(
            key="custom",
            values_to_plot="scores",
            gene_symbols="symbol",
            dendrogram=False,
            show=False,
        )
        chart = gsc.pl.rank_genes_groups_matrixplot(
            a, groups="C", n_genes=-1, min_logfoldchange=0, **options
        ).to_dict()
        rows = chart["datasets"][points(chart)["data"]["name"]]
        assert {r["_gene"] for r in rows} == {"S3"}
        assert [r["_group"] for r in rows] == ["A", "B", "C", "D"]
        assert [r["_mean"] for r in rows] == [-2, 2, 1, 5]
        # Explicit markers bypass a threshold that would otherwise remove all genes.
        chart = gsc.pl.rank_genes_groups_matrixplot(
            a, var_names={"manual": ["S2", "S2"]}, min_logfoldchange=99, **options
        )
        spec = chart.to_dict()
        assert len(spec["datasets"][points(spec)["data"]["name"]]) == 8

    @pytest.mark.parametrize(
        "field,value,message",
        [
            ("scores", np.nan, "finite stored"),
            ("scores", np.inf, "finite"),
            ("pvals", -0.1, "between 0 and 1"),
            ("pvals_adj", 1.1, "between 0 and 1"),
            ("log10_pvals", 0, "positive p-values"),
        ],
    )
    def test_missing_nonfinite_or_invalid_requested_statistics_fail(
        self, field, value, message
    ):
        a = make_ranked_adata()
        a.uns["rank_genes_groups"][field.removeprefix("log10_")]["C"][0] = value
        with pytest.raises(ValueError, match=message):
            ranked_statistics_statistic(a, field)

    def test_zero_raw_pvalues_are_preserved_and_unselected_nonfinite_scores_are_ignored(
        self,
    ):
        a = make_ranked_adata()
        a.uns["rank_genes_groups"]["pvals"]["C"][0] = 0
        assert ranked_statistics_statistic(a, "pvals").loc["C"].iloc[0] == 0
        a.uns["rank_genes_groups"]["scores"]["C"][2] = np.inf
        assert np.isfinite(ranked_statistics_statistic(a).to_numpy()).all()

    def test_complete_logreg_and_single_group_results_support_scores(self):
        a = make_ranked_adata()
        result = a.uns["rank_genes_groups"]
        result["params"]["method"] = "logreg"
        for field in ("pvals", "pvals_adj", "logfoldchanges"):
            del result[field]
        assert ranked_statistics_statistic(a).loc["C"].iloc[0] == 4
        for field in ("names", "scores"):
            result[field] = result[field][["C"]]
        assert ranked_statistics_statistic(a).index.tolist() == ["C"]
        with pytest.raises(ValueError, match="no pvals"):
            ranked_statistics_statistic(a, "pvals")

    def test_missing_metrics_truncated_results_and_ambiguous_symbols_do_not_run_analysis(
        self, monkeypatch
    ):
        monkeypatch.setattr(
            sc.tl, "rank_genes_groups", lambda *a, **k: pytest.fail("Ran analysis")
        )
        a = make_ranked_adata()
        for metric in ("pvals", "pvals_adj", "logfoldchanges"):
            saved = a.uns["rank_genes_groups"].pop(metric)
            with pytest.raises(ValueError, match=f"no {metric}"):
                ranked_statistics_statistic(a, metric)
            a.uns["rank_genes_groups"][metric] = saved
        a.var["symbol"] = ["ambiguous"] * 4
        with pytest.raises(ValueError, match="unambiguous"):
            ranked_statistics_statistic(a, markers=["ambiguous"], gene_symbols="symbol")
        a.uns["rank_genes_groups"]["names"] = a.uns["rank_genes_groups"]["names"][:2]
        a.uns["rank_genes_groups"]["scores"] = a.uns["rank_genes_groups"]["scores"][:2]
        with pytest.raises(ValueError, match="complete stored rankings"):
            ranked_statistics_statistic(a)

    def test_missing_gene_group_pairs_and_incompatible_groupby_fail_clearly(self):
        a = make_ranked_adata()
        a.uns["rank_genes_groups"]["names"]["C"][0] = "absent"
        with pytest.raises(ValueError, match="every ranking group"):
            ranked_statistics_statistic(a)
        a = make_ranked_adata()
        with pytest.raises(ValueError, match="group/feature"):
            gsc.pl.rank_genes_groups_matrixplot(
                a,
                groupby="batch",
                values_to_plot="scores",
                dendrogram=False,
                show=False,
            )

    @pytest.mark.parametrize("family", ["dotplot", "matrixplot"])
    def test_explicit_colorbar_title_overrides_statistic_title(self, family):
        chart = getattr(gsc.pl, f"rank_genes_groups_{family}")(
            make_ranked_adata(),
            n_genes=1,
            values_to_plot="scores",
            colorbar_title="My statistic",
            dendrogram=False,
            show=False,
        )
        assert (
            points(chart.to_dict())["encoding"]["color"]["legend"]["title"]
            == "My statistic"
        )
