"""Stored ranking semantics, native panel bounds and expression-plot delegation."""

from copy import deepcopy
from hashlib import sha256
import inspect
import json
from pathlib import Path
import warnings

import numpy as np
import pytest

import genome_spy.integrations.scanpy as gsc
from genome_spy.integrations.scanpy._ranking.data import ranked_features
from tests.integrations.scanpy.helpers import units
from tests.integrations.scanpy.ranked_fixture import make_ranked_adata, ranked_cases

sc = pytest.importorskip("scanpy")
FAMILIES = ["dotplot", "matrixplot", "heatmap"]


def select(a, **options):
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


@pytest.mark.parametrize(
    "count,expected",
    [(2, ["g2", "g1"]), (-2, ["g3", "g4"]), (None, ["g2", "g1", "g3", "g4"])],
)
def test_stored_order_tail_and_repeated_slots_use_the_public_getter(
    monkeypatch, count, expected
):
    a = make_ranked_adata()
    before = deepcopy(a.uns)
    original, calls = sc.get.rank_genes_groups_df, []

    def get(adata, group, **kwargs):
        calls.append((group, kwargs))
        return original(adata, group, **kwargs)

    monkeypatch.setattr(sc.get, "rank_genes_groups_df", get)
    monkeypatch.setattr(
        sc.tl, "rank_genes_groups", lambda *a, **k: pytest.fail("Ran ranking")
    )
    markers, groupby = select(a, groups=["A", "C"], n_genes=count)
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


def test_strict_filter_symbols_filtered_names_and_custom_key():
    a = make_ranked_adata()
    a.uns["custom"] = a.uns.pop("rank_genes_groups")
    assert select(a, key="custom", groups="C", n_genes=4, min_logfoldchange=1)[0] == {
        "C": ["g2"]
    }
    assert select(a, key="custom", groups="C", n_genes=2, gene_symbols="symbol")[0] == {
        "C": ["S2", "S1"]
    }
    names = a.uns["custom"]["names"].astype([(g, object) for g in ["C", "A", "D", "B"]])
    names["C"][0] = np.nan
    a.uns["custom"]["names"] = names
    assert select(a, key="custom", groups="C", n_genes=2)[0] == {"C": ["g1", "g3"]}


def test_selection_uses_the_public_getters_returned_names(monkeypatch):
    original = sc.get.rank_genes_groups_df

    def get(*args, **kwargs):
        frame = original(*args, **kwargs)
        frame.loc[frame.index[0], "names"] = "g4"
        return frame

    monkeypatch.setattr(sc.get, "rank_genes_groups_df", get)
    assert select(make_ranked_adata(), groups="C", n_genes=1)[0] == {"C": ["g4"]}


@pytest.mark.parametrize("family", FAMILIES)
@pytest.mark.parametrize("tail", [False, True])
def test_ranked_wrapper_is_the_parent_chart_with_selected_markers(
    monkeypatch, family, tail
):
    a = make_ranked_adata()
    monkeypatch.setattr(
        sc.tl, "rank_genes_groups", lambda *a, **k: pytest.fail("Ran ranking")
    )
    count = -2 if tail else 2
    markers, groupby = select(a, n_genes=count)
    flags = {"zoom": "xy", "highlight" if family == "dotplot" else "show_values": True}
    options = {
        "dendrogram": False,
        "layer": "counts",
        "standard_scale": "var",
        "show": False,
        **flags,
    }
    if family == "heatmap":
        options["group_gap"] = 0 if tail else 7
    ranked = getattr(gsc.pl, f"rank_genes_groups_{family}")(a, n_genes=count, **options)
    parent = getattr(gsc.pl, family)(a, markers, groupby, **options)
    assert ranked.to_dict() == parent.to_dict()


@pytest.mark.parametrize("family", FAMILIES)
def test_explicit_markers_and_requested_rank_groups_keep_all_expression_groups(family):
    a = make_ranked_adata()
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", UserWarning)
        chart = getattr(gsc.pl, f"rank_genes_groups_{family}")(
            a, groups="C", n_genes=1, dendrogram=False, show=False
        )
    records = next(
        rows for rows in chart.to_dict()["datasets"].values() if "_group" in rows[0]
    )
    assert set(r["_group"] for r in records) == {"C", "A", "D", "B"}
    assert set(r["_gene"] for r in records) == {"g2"}
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
def test_invalid_selections_fail_clearly(options, message):
    with pytest.raises(ValueError, match=message):
        select(make_ranked_adata(), **options)


def test_missing_analysis_or_metrics_never_trigger_computation(monkeypatch):
    a = make_ranked_adata()
    monkeypatch.setattr(
        sc.tl, "rank_genes_groups", lambda *a, **k: pytest.fail("Ran ranking")
    )
    del a.uns["rank_genes_groups"]["pvals_adj"]
    with pytest.raises(ValueError, match="pvals_adj"):
        select(a)
    a.uns.clear()
    with pytest.raises(ValueError, match="run sc.tl.rank_genes_groups explicitly"):
        select(a)


def test_malformed_scores_and_nonfinite_panel_values_fail_without_repair():
    a = make_ranked_adata()
    a.uns["rank_genes_groups"]["scores"] = a.uns["rank_genes_groups"]["scores"][:2]
    with pytest.raises(ValueError, match="scores must match"):
        gsc.pl.rank_genes_groups(a, show=False)
    a = make_ranked_adata()
    a.uns["rank_genes_groups"]["scores"]["C"][0] = np.nan
    with pytest.raises(ValueError, match="finite scores"):
        gsc.pl.rank_genes_groups(a, groups="C", show=False)


def test_metric_fields_are_matched_by_group_name_not_array_field_order():
    a = make_ranked_adata()
    result = a.uns["rank_genes_groups"]
    for field in ("scores", "logfoldchanges", "pvals", "pvals_adj"):
        result[field] = result[field][["B", "D", "A", "C"]]
    assert select(a, groups=["C", "A"], n_genes=2)[0] == {
        "C": ["g2", "g1"],
        "A": ["g2", "g4"],
    }


def test_stored_score_panels_work_with_backed_data_and_views(tmp_path):
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
            assert [r["_label"] for r in spec["datasets"][spec["data"]["name"]]] == [
                "S2",
                "S1",
            ]
    finally:
        backed.file.close()


def test_packaged_logreg_results_and_unavailable_fold_change_filter():
    a = sc.datasets.pbmc68k_reduced()
    markers, grouping = select(a, n_genes=2)
    assert len(markers) == 10 and grouping == "bulk_labels"
    assert (
        markers[next(iter(markers))]
        == a.uns["rank_genes_groups"]["names"][next(iter(markers))][:2].tolist()
    )
    with pytest.raises(ValueError, match="logreg results have none"):
        select(a, min_logfoldchange=1)


@pytest.mark.parametrize("sharey", [False, True])
def test_score_panels_keep_stored_order_symbols_titles_and_score_bounds(sharey):
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
    assert all(p["encoding"]["x"]["scale"]["domain"] == [-0.9, 1.9] for p in panels)


def test_ranking_supplied_dictionary_log_and_numbered_labels():
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


def test_ranking_indices_and_extreme_gap_match_scanpy():
    a = make_ranked_adata()
    a.varm["PCs"] = np.array([[4, 1], [2, 2], [8, 3], [6, 4]])
    spec = gsc.pl.ranking(
        a, "varm", "PCs", indices=[1, 0], n_points=2, include_lowest=True, show=False
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


@pytest.mark.parametrize(
    "family",
    ["ranking", "rank_genes_groups", *[f"rank_genes_groups_{f}" for f in FAMILIES]],
)
def test_signatures_match_scanpy_except_renderer_objects_and_native_controls(family):
    upstream = inspect.signature(getattr(sc.pl, family)).parameters
    native = inspect.signature(getattr(gsc.pl, family)).parameters
    for name, parameter in upstream.items():
        if name in {"ax", "return_fig"}:
            assert name not in native
        else:
            assert native[name].kind == parameter.kind
            assert native[name].default == parameter.default
    assert all(
        p.kind is inspect.Parameter.KEYWORD_ONLY
        for name, p in native.items()
        if name not in upstream
    )


@pytest.mark.parametrize("family", ["dotplot", "matrixplot"])
def test_invalid_metric_colors_fail_instead_of_falling_back_to_expression(family):
    with pytest.raises(ValueError, match="values_to_plot"):
        getattr(gsc.pl, f"rank_genes_groups_{family}")(
            make_ranked_adata(), values_to_plot="unknown", show=False
        )


@pytest.mark.parametrize("case", ranked_cases())
def test_rank_data_and_guides_match_scanpy_with_documented_pca_label_space(case):
    manifest = json.loads(
        (Path(__file__).with_name("fixtures") / "ranked.json").read_text()
    )
    assert (
        manifest["input_sha256"]
        == sha256(
            Path(__file__).with_name("ranked_fixture.py").read_bytes()
        ).hexdigest()
    )
    reference = manifest["cases"][case]["panels"]
    family, args, options = ranked_cases()[case]
    spec = getattr(gsc.pl, family)(
        make_ranked_adata(), *args, show=False, **options
    ).to_dict()
    panels = units(spec)
    assert len(panels) == len(reference)
    for panel, expected in zip(panels, reference, strict=True):
        rows = spec["datasets"][panel["data"]["name"]]
        assert [(r["_label"], [r["_rank"], r["_score"]]) for r in rows] == [
            (label["text"], label["position"]) for label in expected["labels"]
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
    monkeypatch, show, autoshow
):
    from genome_spy.chart import TopLevelSpec

    displayed = []
    monkeypatch.setattr(TopLevelSpec, "display", lambda self: displayed.append(self))
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
    monkeypatch, family, metric
):
    import anndata as ad
    import pandas as pd
    from scipy import sparse

    a = ad.AnnData(
        sparse.csr_matrix((100_000, 20_000), dtype=np.float32),
        obs=pd.DataFrame(
            {"group": pd.Categorical(["C", "A", "D", "B"] * 25_000)},
            index=[f"c{i}" for i in range(100_000)],
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
                a.var_names[4:].tolist() if field == "names" else np.zeros(a.n_vars - 4)
                for _ in first.dtype.names
            ]
            result[field] = np.concatenate(
                [first, np.rec.fromarrays(rest, names=first.dtype.names)]
            )
    original, shapes = sparse.csr_matrix.toarray, []

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
        assert shapes == [(100_000, 4)]
        assert displayed == [(100_000, 8)]
    else:
        chart = getattr(gsc.pl, f"rank_genes_groups_{family}")(
            a,
            n_genes=2,
            dendrogram=False,
            show=False,
            values_to_plot=metric,
            **({"dot_max": 1} if family == "dotplot" else {}),
        )
        assert shapes == [(0 if family == "matrixplot" and metric else 100_000, 4)]
        assert (
            len(
                next(
                    rows
                    for rows in chart.to_dict()["datasets"].values()
                    if "_mean" in rows[0]
                )
            )
            == 32
        )
