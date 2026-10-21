"""Stored statistic colors remain separate from expression summaries and sizes."""

from copy import deepcopy

import numpy as np
import pandas as pd
import pytest

import genome_spy.integrations.scanpy as gsc
from genome_spy.integrations.scanpy._ranked_data import ranked_statistic
from tests.integrations.scanpy.helpers import points
from tests.integrations.scanpy.ranked_fixture import make_ranked_adata

sc = pytest.importorskip("scanpy")
METRICS = [
    "scores",
    "logfoldchanges",
    "pvals",
    "pvals_adj",
    "log10_pvals",
    "log10_pvals_adj",
]


@pytest.mark.parametrize("family", ["dotplot", "matrixplot"])
def test_one_ranking_read_preserves_unfiltered_colors_and_avoids_unused_expression(
    monkeypatch, family
):
    a = make_ranked_adata()
    ranking, expression = sc.get.rank_genes_groups_df, sc.get.obs_df
    calls, reads = [], []

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
    rows = next(rows for rows in chart["datasets"].values() if "_mean" in rows[0])
    assert {r["_gene"] for r in rows} == {"g2"}
    assert {r["_group"]: r["_mean"] for r in rows} == {"C": 4, "A": 6, "D": -1, "B": 1}
    if family == "matrixplot":
        assert reads == [(0, ["group", "g2"]), (8, ["group"])]
    else:
        assert reads == [(8, ["group", "g2"])]


def statistic(a, metric="scores", markers=None, **options):
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


def test_score_colors_are_by_gene_not_rank_and_use_all_groups(monkeypatch):
    a = make_ranked_adata()
    before = deepcopy(a.uns["rank_genes_groups"])
    getter, calls = sc.get.rank_genes_groups_df, []

    def get(*args, **kwargs):
        calls.append(args[1])
        frame = getter(*args, **kwargs)
        frame.loc[(frame["group"] == "C") & (frame["names"] == "g2"), "scores"] = 42
        return frame

    monkeypatch.setattr(sc.get, "rank_genes_groups_df", get)
    colors = statistic(a)
    assert calls == [["C", "A", "D", "B"]]
    assert colors.index.tolist() == ["A", "B", "C", "D"]
    assert colors.columns.tolist() == ["g2", "g4", "g2", "g1"]
    np.testing.assert_array_equal(
        colors, [[6, 3, 6, 0], [1, 8, 1, -4], [42, -3, 42, 2], [-1, 0, -1, 2]]
    )
    for key in ("names", "scores", "pvals", "pvals_adj", "logfoldchanges"):
        np.testing.assert_array_equal(a.uns["rank_genes_groups"][key], before[key])


@pytest.mark.parametrize("metric", METRICS)
@pytest.mark.parametrize("symbols", [False, True])
def test_color_table_matches_pinned_scanpy_public_getter_and_transform(metric, symbols):
    from scanpy.plotting._tools import _get_values_to_plot

    a = make_ranked_adata()
    genes = ["S2", "S4", "S2", "S1"] if symbols else ["g2", "g4", "g2", "g1"]
    symbol_key = "symbol" if symbols else None
    expected = _get_values_to_plot(a, metric, genes, gene_symbols=symbol_key)
    actual = statistic(a, metric, genes, gene_symbols=symbol_key)
    pd.testing.assert_frame_equal(actual, expected, check_names=False)


@pytest.mark.parametrize("family", ["dotplot", "matrixplot"])
@pytest.mark.parametrize("metric", METRICS)
@pytest.mark.parametrize("swapped", [False, True])
def test_metric_wrappers_delegate_to_supplied_tables_with_parent_scaling(
    family, metric, swapped
):
    a = make_ranked_adata()
    colors = statistic(a, metric)
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
        **({"highlight": True} if family == "dotplot" else {"show_values": True}),
    )
    actual = getattr(gsc.pl, f"rank_genes_groups_{family}")(
        a,
        groups=["A", "C"],
        n_genes=2,
        values_to_plot=metric,
        **options,
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
def test_stored_source_does_not_override_expression_sizes(source):
    a = make_ranked_adata()
    a.X[:] = 0
    a.layers["counts"][:] = 5
    a.uns["rank_genes_groups"]["params"].update(use_raw=False, layer="counts")
    options = dict(
        var_names=["g2"], expression_cutoff=1, dot_max=1, dendrogram=False, show=False
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


def test_explicit_symbols_custom_key_tail_and_threshold_only_select_slots():
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
def test_missing_nonfinite_or_invalid_requested_statistics_fail(field, value, message):
    a = make_ranked_adata()
    a.uns["rank_genes_groups"][field.removeprefix("log10_")]["C"][0] = value
    with pytest.raises(ValueError, match=message):
        statistic(a, field)


def test_zero_raw_pvalues_are_preserved_and_unselected_nonfinite_scores_are_ignored():
    a = make_ranked_adata()
    a.uns["rank_genes_groups"]["pvals"]["C"][0] = 0
    assert statistic(a, "pvals").loc["C"].iloc[0] == 0
    a.uns["rank_genes_groups"]["scores"]["C"][2] = np.inf
    assert np.isfinite(statistic(a).to_numpy()).all()


def test_complete_logreg_and_single_group_results_support_scores():
    a = make_ranked_adata()
    result = a.uns["rank_genes_groups"]
    result["params"]["method"] = "logreg"
    for field in ("pvals", "pvals_adj", "logfoldchanges"):
        del result[field]
    assert statistic(a).loc["C"].iloc[0] == 4
    for field in ("names", "scores"):
        result[field] = result[field][["C"]]
    assert statistic(a).index.tolist() == ["C"]
    with pytest.raises(ValueError, match="no pvals"):
        statistic(a, "pvals")


def test_missing_metrics_truncated_results_and_ambiguous_symbols_do_not_run_analysis(
    monkeypatch,
):
    monkeypatch.setattr(
        sc.tl, "rank_genes_groups", lambda *a, **k: pytest.fail("Ran analysis")
    )
    a = make_ranked_adata()
    for metric in ("pvals", "pvals_adj", "logfoldchanges"):
        saved = a.uns["rank_genes_groups"].pop(metric)
        with pytest.raises(ValueError, match=f"no {metric}"):
            statistic(a, metric)
        a.uns["rank_genes_groups"][metric] = saved
    a.var["symbol"] = ["ambiguous"] * 4
    with pytest.raises(ValueError, match="unambiguous"):
        statistic(a, markers=["ambiguous"], gene_symbols="symbol")
    a.uns["rank_genes_groups"]["names"] = a.uns["rank_genes_groups"]["names"][:2]
    a.uns["rank_genes_groups"]["scores"] = a.uns["rank_genes_groups"]["scores"][:2]
    with pytest.raises(ValueError, match="complete stored rankings"):
        statistic(a)


def test_missing_gene_group_pairs_and_incompatible_groupby_fail_clearly():
    a = make_ranked_adata()
    a.uns["rank_genes_groups"]["names"]["C"][0] = "absent"
    with pytest.raises(ValueError, match="every ranking group"):
        statistic(a)
    a = make_ranked_adata()
    with pytest.raises(ValueError, match="group/feature"):
        gsc.pl.rank_genes_groups_matrixplot(
            a, groupby="batch", values_to_plot="scores", dendrogram=False, show=False
        )


@pytest.mark.parametrize("family", ["dotplot", "matrixplot"])
def test_explicit_colorbar_title_overrides_statistic_title(family):
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
