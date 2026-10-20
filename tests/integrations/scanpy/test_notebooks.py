"""Run the independent plotting workflows on Scanpy's packaged PBMC data."""

import json
from pathlib import Path

import numpy as np
import pytest

import genome_spy.integrations.scanpy as gsc
from genome_spy.chart import TopLevelSpec
from tests.integrations.scanpy.helpers import points, units, leaf_marks

sc = pytest.importorskip("scanpy")
NOTEBOOKS = Path(__file__).resolve().parents[3] / "integrations/scanpy/notebooks"


def run_notebook(path, namespace):
    notebook = json.loads(path.read_text())
    for cell in notebook["cells"]:
        if cell["cell_type"] == "code":
            exec(compile("".join(cell["source"]), str(path), "exec"), namespace)
    return notebook


def test_umap_workflow_preserves_embedding_and_retrieves_selected_cells(monkeypatch):
    charts = []
    monkeypatch.setattr(
        TopLevelSpec, "display", lambda chart, **kwargs: charts.append(chart)
    )
    original = sc.datasets.pbmc68k_reduced()
    tsne, analyses = sc.tl.tsne, []

    def prepare_tsne(*args, **kwargs):
        analyses.append(kwargs)
        return tsne(*args, **kwargs)

    monkeypatch.setattr(sc.tl, "tsne", prepare_tsne)
    monkeypatch.setattr(sc.pp, "pca", lambda *a, **k: pytest.fail("Ran PCA"))
    monkeypatch.setattr(sc.tl, "pca", lambda *a, **k: pytest.fail("Ran PCA"))
    namespace = {}
    path = NOTEBOOKS / "scanpy_umap.ipynb"
    try:
        notebook = run_notebook(path, namespace)
        pbmc = namespace["pbmc"]
        assert pbmc.shape == original.shape == (700, 765)
        assert pbmc.obs_names.equals(original.obs_names)
        np.testing.assert_array_equal(pbmc.obsm["X_umap"], original.obsm["X_umap"])
        np.testing.assert_array_equal(pbmc.obsm["X_pca"], original.obsm["X_pca"])
        np.testing.assert_array_equal(pbmc.varm["PCs"], original.varm["PCs"])
        np.testing.assert_array_equal(
            pbmc.uns["pca"]["variance_ratio"], original.uns["pca"]["variance_ratio"]
        )
        assert analyses == [{"use_rep": "X_pca", "random_state": 0, "n_jobs": 1}]
        assert namespace["pca_chart"] in charts and namespace["tsne_chart"] in charts
        loadings = namespace["loadings_chart"]
        assert loadings in charts
        variance = namespace["variance_chart"]
        assert variance in charts
        assert (
            variance.to_dict()
            == gsc.pl.ranking(
                pbmc,
                "uns",
                "variance_ratio",
                dictionary="pca",
                labels="PC",
                n_points=10,
                log=True,
                width=360,
                height=240,
                show=False,
            ).to_dict()
        )
        assert (
            sum(len(table) for table in variance.to_dict()["datasets"].values()) == 11
        )
        overview = namespace["overview_chart"]
        assert overview in charts
        overview_spec = overview.to_dict()
        assert len(overview_spec["vconcat"]) == 3
        assert len(units(overview_spec["vconcat"][1])) == 3
        assert overview_spec["vconcat"][2]["hconcat"][0]["encoding"]["x"]["scale"][
            "domain"
        ] == [
            -0.9,
            30.9,
        ]
        for panel in units(overview_spec["vconcat"][0]):
            assert all(
                points(panel)["encoding"][axis]["scale"]["zoom"] is True
                for axis in ("x", "y")
            )
        assert namespace["pca_genes"].shape == (700, 309)
        assert (
            loadings.to_dict()
            == gsc.pl.ranking(
                namespace["pca_genes"],
                "varm",
                "PCs",
                indices=[0, 1],
                n_points=20,
                include_lowest=True,
                width=280,
                height=280,
                show=False,
            ).to_dict()
        )
        assert namespace["scatter_chart"] in charts
        scatter = namespace["scatter_chart"].to_dict()
        assert scatter["resolve"]["legend"] == {"default": "collected"}
        assert scatter["resolve"]["scale"]["color"] == "independent"
        legend = scatter["config"]["legend"]
        assert (
            legend["orient"],
            legend["direction"],
            legend["columns"],
            legend["symbolSize"],
        ) == ("bottom", "horizontal", 6, 64)
        assert legend["tickCount"] == 3
        assert namespace["gene_scatter_chart"] in charts
        gene_rows = next(
            iter(namespace["gene_scatter_chart"].to_dict()["datasets"].values())
        )
        assert len(gene_rows) == pbmc.n_vars
        assert [r["_obs_label"] for r in gene_rows] == list(pbmc.var_names)
        np.testing.assert_array_equal(
            [r["_coord_0"] for r in gene_rows], pbmc.var["means"]
        )
        assert pbmc.obsm["X_tsne"].shape == (700, 2)
        assert charts
        for chart in charts:
            if chart is loadings or chart is variance or chart is overview:
                continue
            spec = chart.to_dict()
            assert spec["datasets"]
            for panel in units(spec):
                for channel in ("x", "y"):
                    assert points(panel)["encoding"][channel]["scale"]["zoom"] is True
        view, brush = namespace["view"], namespace["brush"]
        assert view.parameter_names == [brush.name]
        assert brush.param.to_dict()["select"] == {
            "type": "interval",
            "encodings": ["x", "y"],
        }
        for panel in units(view.spec["vconcat"][0]):
            for channel in ("x", "y"):
                assert points(panel)["encoding"][channel]["scale"]["zoom"] is True
        xy = original.obsm["X_umap"]
        lower, upper = np.quantile(xy, [0.25, 0.75], axis=0)
        view.parameter_values = {
            brush.name: {
                "type": "interval",
                "intervals": {
                    "x": [lower[0], upper[0]],
                    "y": [lower[1], upper[1]],
                },
            }
        }
        retrieval = next(
            c
            for c in notebook["cells"]
            if "mask = gsc.selection_mask" in "".join(c["source"])
        )
        exec(compile("".join(retrieval["source"]), str(path), "exec"), namespace)
        expected = (
            (xy[:, 0] >= lower[0])
            & (xy[:, 0] < upper[0])
            & (xy[:, 1] >= lower[1])
            & (xy[:, 1] < upper[1])
        )
        assert 0 < expected.sum() < pbmc.n_obs
        assert namespace["selected_adata"].obs_names.equals(pbmc.obs_names[expected])
        assert namespace["selected_ids"].equals(pbmc.obs_names[expected])
        assert (
            gsc.selection_mask(pbmc, view.parameter_values[brush.name]).tolist()
            == expected.tolist()
        )
    finally:
        if "view" in namespace:
            namespace["view"].close()


def test_expression_workflow_runs_independently_with_summary_hover(monkeypatch):
    charts = []
    monkeypatch.setattr(
        TopLevelSpec, "display", lambda chart, **kwargs: charts.append(chart)
    )
    namespace = {}
    ranking, calls = sc.tl.rank_genes_groups, []

    def prepare_ranking(*args, **kwargs):
        calls.append(kwargs)
        assert kwargs["key_added"] == "rank_stats"
        return ranking(*args, **kwargs)

    monkeypatch.setattr(sc.tl, "rank_genes_groups", prepare_ranking)
    run_notebook(NOTEBOOKS / "scanpy_expression.ipynb", namespace)
    assert charts == [
        namespace["dotplot"],
        namespace["matrixplot"],
        namespace["heatmap"],
        namespace["matrix"],
        namespace["clustermap"],
        namespace["rank_scores"],
        namespace["ranked_dotplot"],
        namespace["ranked_matrixplot"],
        namespace["ranked_heatmap"],
        namespace["statistic_dotplot"],
        namespace["statistic_matrixplot"],
    ]
    assert len(calls) == 1 and calls[0]["n_genes"] == 765
    assert namespace["pbmc"].shape == (700, 765)
    order = namespace["pbmc"].uns["dendrogram_bulk_labels"]["categories_ordered"]
    for chart in charts[:3]:
        chart_spec = chart.to_dict()
        values = next(
            rows for rows in chart_spec["datasets"].values() if "_group" in rows[0]
        )
        assert list(dict.fromkeys(row["_group"] for row in values)) == list(order)
        tree = chart_spec["layer"][-1]["layer"][0]
        assert tree["mark"]["type"] == "rule"
        assert len(chart_spec["datasets"][tree["data"]["name"]]) == 3 * (len(order) - 1)
    spec = charts[0].to_dict()
    dot = points(spec)
    assert len(spec["datasets"][dot["data"]["name"]]) == 100
    assert dot["encoding"]["color"]["scale"]["scheme"] == "reds"
    assert dot["encoding"]["x"]["type"] == dot["encoding"]["y"]["type"] == "index"
    assert [item["title"] for item in dot["encoding"]["tooltip"]] == [
        "Gene",
        "Group",
        "Mean expression",
        "Expressing cells (%)",
    ]
    spec = charts[1].to_dict()
    tiles = points(spec)
    records = spec["datasets"][spec["layer"][0]["data"]["name"]]
    assert tiles["mark"]["type"] == "rect"
    assert len(records) == 100
    assert tiles["encoding"]["color"]["scale"]["scheme"] == "blues"
    assert tiles["encoding"]["color"]["scale"]["domain"] == [0, 1]
    assert [item["title"] for item in tiles["encoding"]["tooltip"]] == [
        "Gene",
        "Group",
        "Mean expression (scaled)",
    ]
    for gene in namespace["marker_genes"].values():
        for name in gene:
            values = [row["_mean"] for row in records if row["_gene"] == name]
            assert min(values) == 0 and max(values) == 1
    spec = charts[2].to_dict()
    tiles = points(spec)
    cells = spec["datasets"][spec["layer"][0]["data"]["name"]]
    assert tiles["encoding"]["x"]["scale"]["zoom"] is False
    assert tiles["encoding"]["y"]["scale"]["zoom"] is True
    assert len(cells) == 700 * 10
    assert len({row["_obs_id"] for row in cells}) == 700
    assert tiles["encoding"]["color"]["scale"]["domain"] == [0, 1]
    assert tiles["encoding"]["tooltip"][-1]["title"] == "Expression (scaled)"
    assert all(
        sum(row["_obs_id"] == name for row in cells) == 10
        for name in namespace["pbmc"].obs_names
    )
    spec = charts[3].to_dict()
    records = spec["datasets"][spec["layer"][0]["data"]["name"]]
    np.testing.assert_array_equal(
        np.array([row["_value"] for row in records]).reshape(10, 10),
        namespace["pbmc"].uns["dendrogram_bulk_labels"]["correlation_matrix"],
    )
    assert [row["_column"] for row in records[:10]] == namespace["group_labels"]

    rulers = [p for p in charts[0].to_dict()["params"] if "ruler" in p]
    assert len(rulers) == 1
    assert rulers[0]["ruler"]["encodings"] == ["x", "y"]
    assert rulers[0]["ruler"]["display"] == "center"
    for chart in charts[1:5]:
        grid = chart.to_dict()["layer"][0]
        text = grid["layer"][1]["layer"][0]
        assert text["mark"]["fitToBand"] is True
        assert all(
            grid["layer"][0]["encoding"][axis]["scale"]["zoom"] is (axis == "y")
            for axis in ("x", "y")
        )
    clustered = charts[4].to_dict()
    tiles = points(clustered)
    cells = clustered["datasets"][clustered["layer"][0]["data"]["name"]]
    assert len(cells) == 700 * 10
    assert {row["_row"] for row in cells} == set(namespace["pbmc"].obs_names)
    assert {row["_column"] for row in cells} == set(namespace["marker_names"])
    annotation = next(
        mark["encoding"]["color"]
        for mark in leaf_marks(clustered)
        if mark.get("encoding", {}).get("color", {}).get("legend", {}) is not None
        and mark.get("encoding", {}).get("color", {}).get("legend", {}).get("title")
        == "bulk_labels"
    )
    assert annotation["scale"]["domain"] == namespace["group_labels"]
    assert annotation["scale"]["range"] == list(
        namespace["pbmc"].uns["bulk_labels_colors"]
    )
    branches = [mark for mark in clustered["layer"] if "layer" in mark]
    assert [
        len(clustered["datasets"][mark["layer"][0]["data"]["name"]])
        for mark in branches[-2:]
    ] == [3 * 699, 3 * 9]

    scores = charts[5].to_dict()
    assert len(units(scores)) == 2
    assert sum(len(rows) for rows in scores["datasets"].values()) == 10
    expected_genes = [
        gene
        for group in namespace["ranked_groups"]
        for gene in namespace["pbmc"].uns[namespace["rank_key"]]["names"][group][:3]
    ]
    for chart in charts[6:9]:
        spec = chart.to_dict()
        records = next(
            rows
            for rows in spec["datasets"].values()
            if "_gene" in rows[0] and "_group" in rows[0]
        )
        assert {r["_gene"] for r in records} == set(expected_genes)
        assert {r["_group"] for r in records} == set(namespace["group_labels"])
    heatmap_rows = next(
        rows
        for rows in charts[8].to_dict()["datasets"].values()
        if "_obs_id" in rows[0]
    )
    assert len(heatmap_rows) == 700 * 6
    stored = namespace["pbmc"].uns["rank_stats"]
    for chart, metric in [(charts[9], "logfoldchanges"), (charts[10], "pvals_adj")]:
        spec = chart.to_dict()
        rows = next(rows for rows in spec["datasets"].values() if "_mean" in rows[0])
        assert {r["_group"] for r in rows} == set(namespace["group_labels"])
        for row in rows:
            group, gene = row["_group"], row["_gene"]
            value = stored[metric][group][list(stored["names"][group]).index(gene)]
            assert row["_mean"] == pytest.approx(
                -np.log10(value) if metric == "pvals_adj" else value
            )
