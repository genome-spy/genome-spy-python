"""Keep the linked expression page runnable without analysis or a kernel."""

import json
from pathlib import Path

import pytest

from tests.test_docs_notebook import notebook_extension as notebook_extension

pytestmark = pytest.mark.docs


def test_linked_expression_page_runs_without_analysis_and_has_clean_download(
    notebook_extension, monkeypatch
):
    sc = pytest.importorskip("scanpy")
    from genome_spy.chart import TopLevelSpec

    def forbidden(*args, **kwargs):
        pytest.fail("The linked expression guide must not rerun analysis")

    for module, name in [
        (sc.pp, "neighbors"),
        (sc.tl, "umap"),
        (sc.tl, "rank_genes_groups"),
        (sc.tl, "score_genes"),
        (sc.tl, "score_genes_cell_cycle"),
        (sc.pp, "calculate_qc_metrics"),
        (sc.readwrite, "_download"),
        (TopLevelSpec, "widget"),
    ]:
        monkeypatch.setattr(module, name, forbidden)

    path = (
        Path(__file__).resolve().parents[1]
        / "integrations/scanpy/guides/linked_expression.ipynb"
    )
    notebook = json.loads(path.read_text())
    if not notebook_extension._preparation_current(notebook, path.parents[3]):
        pytest.skip(
            "Run integrations/scanpy/prepare_guide_data.py linked_expression first"
        )
    monkeypatch.setattr(sc.datasets, "pbmc3k_processed", forbidden)
    markdown = notebook_extension._notebook_markdown(
        path, download_path="linked_expression.ipynb", bundle_url="/core.js"
    )
    assert "{download}`Download notebook <linked_expression.ipynb>`" in markdown
    assert [
        cell["metadata"]["genomespy"]["chart"]
        for cell in notebook["cells"]
        if "genomespy" in cell["metadata"]
    ] == ["phase_qc", "marker_distribution", "linked_expression", "linked_tracks"]
    assert "widgets" not in notebook["metadata"]
    assert all(
        cell["execution_count"] is None and cell["outputs"] == []
        for cell in notebook["cells"]
        if cell["cell_type"] == "code"
    )
