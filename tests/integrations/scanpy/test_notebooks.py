"""Run both real-data notebooks; detailed plot behavior is tested by each family."""

import json
from pathlib import Path

import numpy as np
import pytest

from genome_spy.chart import TopLevelSpec

sc = pytest.importorskip("scanpy")
pytestmark = pytest.mark.workflow
NOTEBOOKS = Path(__file__).resolve().parents[3] / "integrations/scanpy/notebooks"


def run_notebook(path, namespace):
    """Execute a clean notebook in order and return its cells for later interaction."""
    notebook = json.loads(path.read_text())
    assert not notebook.get("metadata", {}).get("widgets")
    for cell in notebook["cells"]:
        if cell["cell_type"] == "code":
            assert not cell["outputs"] and cell["execution_count"] is None
            exec(compile("".join(cell["source"]), str(path), "exec"), namespace)
    return notebook


def test_umap_workflow_preserves_embedding_and_retrieves_selected_cells(monkeypatch):
    charts = []
    monkeypatch.setattr(
        TopLevelSpec, "display", lambda chart, **kwargs: charts.append(chart)
    )
    original = sc.datasets.pbmc68k_reduced()
    for owner, name in [(sc.pp, "pca"), (sc.tl, "pca"), (sc.pp, "neighbors")]:
        monkeypatch.setattr(
            owner, name, lambda *a, **k: pytest.fail("Recomputed stored analysis")
        )
    namespace = {}
    path = NOTEBOOKS / "scanpy_umap.ipynb"
    try:
        notebook = run_notebook(path, namespace)
        pbmc = namespace["pbmc"]
        assert pbmc.shape == original.shape == (700, 765)
        assert pbmc.obs_names.equals(original.obs_names)
        for key in ("X_umap", "X_pca"):
            np.testing.assert_array_equal(pbmc.obsm[key], original.obsm[key])
        assert pbmc.obsm["X_tsne"].shape == (700, 2)
        assert "umap_density_phase" in pbmc.obs
        assert charts
        for chart in charts:
            assert chart.to_dict()["datasets"]

        # Exercise the notebook's Python retrieval cell with an actual brush value.
        view, brush = namespace["view"], namespace["brush"]
        assert view.parameter_names == [brush.name]
        xy = pbmc.obsm["X_umap"]
        lower, upper = np.quantile(xy, [0.25, 0.75], axis=0)
        view.parameter_values = {
            brush.name: {
                "type": "interval",
                "intervals": {"x": [lower[0], upper[0]], "y": [lower[1], upper[1]]},
            }
        }
        retrieval = next(
            c
            for c in notebook["cells"]
            if "mask = gsc.selection_mask" in "".join(c["source"])
        )
        exec(compile("".join(retrieval["source"]), str(path), "exec"), namespace)
        expected = ((xy >= lower) & (xy < upper)).all(axis=1)
        assert 0 < expected.sum() < pbmc.n_obs
        assert namespace["selected_adata"].obs_names.equals(pbmc.obs_names[expected])
        assert namespace["selected_ids"].equals(pbmc.obs_names[expected])
    finally:
        if "view" in namespace:
            namespace["view"].close()


def test_expression_workflow_runs_independently_with_summary_hover(monkeypatch):
    charts, display_options = [], []

    def display(chart, **kwargs):
        charts.append(chart)
        display_options.append(kwargs)

    monkeypatch.setattr(TopLevelSpec, "display", display)
    namespace = {}
    run_notebook(NOTEBOOKS / "scanpy_expression.ipynb", namespace)
    expected_names = [
        "dotplot",
        "matrixplot",
        "heatmap",
        "tracks",
        "matrix",
        "correlations",
        "clustermap",
        "rank_scores",
        "ranked_dotplot",
        "ranked_matrixplot",
        "ranked_heatmap",
        "statistic_dotplot",
        "statistic_matrixplot",
        "variable_genes",
        "highest_expression",
        "scrublet_scores",
        "timeseries_heatmap",
        "time_series",
        "time_series_subplots",
        "simulation_points",
        "simulation_heatmap",
        "dpt_groups_chart",
        "dpt_expression",
        "paga_graph",
        "paga_numeric",
        "paga_gene",
        "paga_degree",
        "paga_component",
        "paga_adjacency",
        "paga_stripplot",
        "adjacency_panels",
        "paga_comparison",
        "independent_comparisons",
        "paga_path_chart",
        "paga_path_lines",
        "builder_tree_chart",
        "builder_totals_chart",
        "matrix_builder_tree_chart",
        "matrix_builder_totals_chart",
    ]
    assert charts == [namespace[name] for name in expected_names]
    assert display_options == [{"inline": True, "controls": False}] * len(charts)
    assert namespace["pbmc"].shape == (700, 765)
    for chart in charts:
        assert chart.to_dict()["datasets"]
    # Check workflow-level results without repeating each renderer's geometry tests.
    assert "rank_stats" in namespace["pbmc"].uns
    assert "paga" in namespace["pbmc"].uns
