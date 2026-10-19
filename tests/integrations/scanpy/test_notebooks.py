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
    namespace = {}
    path = NOTEBOOKS / "scanpy_umap.ipynb"
    try:
        notebook = run_notebook(path, namespace)
        pbmc = namespace["pbmc"]
        assert pbmc.shape == original.shape == (700, 765)
        assert pbmc.obs_names.equals(original.obs_names)
        np.testing.assert_array_equal(pbmc.obsm["X_umap"], original.obsm["X_umap"])
        assert charts
        for chart in charts:
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
    run_notebook(NOTEBOOKS / "scanpy_expression.ipynb", namespace)
    assert charts == [
        namespace["dotplot"],
        namespace["matrixplot"],
        namespace["heatmap"],
        namespace["matrix"],
        namespace["clustermap"],
    ]
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
    for chart in charts[1:]:
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
