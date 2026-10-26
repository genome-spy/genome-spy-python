"""Check that a guide and its download use the same runnable notebook source."""

from __future__ import annotations

import importlib
import io
import json
import re
import shutil
from pathlib import Path

import numpy as np
import pytest

pytestmark = pytest.mark.docs
ROOT = Path(__file__).resolve().parents[1]
GUIDE = ROOT / "integrations/scanpy/guides/umap.ipynb"
EXPRESSION_GUIDE = GUIDE.with_name("expression.ipynb")


@pytest.fixture
def notebook_extension(monkeypatch):
    pytest.importorskip("sphinx")
    monkeypatch.syspath_prepend(str(ROOT / "docs/_ext"))
    return importlib.import_module("genomespy_notebook")


def test_umap_page_uses_packaged_coordinates_without_analysis(
    notebook_extension, monkeypatch
):
    sc = pytest.importorskip("scanpy")
    from genome_spy.chart import TopLevelSpec

    original = sc.datasets.pbmc68k_reduced()
    loaded = original.copy()
    monkeypatch.setattr(sc.datasets, "pbmc68k_reduced", lambda: loaded)

    def forbidden(*args, **kwargs):
        pytest.fail(
            "A documentation page ran analysis, downloaded data or made a widget"
        )

    for module, name in [
        (sc.pp, "neighbors"),
        (sc.tl, "umap"),
        (sc.tl, "rank_genes_groups"),
        (sc.readwrite, "_download"),
        (TopLevelSpec, "widget"),
        (TopLevelSpec, "save"),
    ]:
        monkeypatch.setattr(module, name, forbidden)
    markdown = notebook_extension._notebook_markdown(
        GUIDE, download_path="umap.ipynb", bundle_url="/core.js"
    )
    specs = [json.loads(value) for value in re.findall(r"const spec = (.*);", markdown)]
    assert len(specs) == 3
    for spec in specs:
        rows = next(iter(spec["datasets"].values()))
        assert len(rows) == 700
        np.testing.assert_array_equal(
            [[row["_coord_0"], row["_coord_1"]] for row in rows],
            original.obsm["X_umap"],
        )
    np.testing.assert_array_equal(loaded.obsm["X_umap"], original.obsm["X_umap"])
    assert loaded.obs.equals(original.obs)
    assert "view.parameter_values.get(brush.name)" in markdown
    assert "{download}`Download notebook <umap.ipynb>`" in markdown


@pytest.mark.parametrize(
    "notebook, title, section",
    [
        (GUIDE, "UMAP and embeddings", "select-cells"),
        (EXPRESSION_GUIDE, "Expression plots", "heatmap"),
    ],
)
def test_notebook_download_and_page_build_from_one_source(
    notebook_extension, tmp_path, notebook, title, section
):
    pytest.importorskip("scanpy")
    from sphinx.testing.util import SphinxTestApp

    source = tmp_path / "docs"
    source.mkdir()
    guide = tmp_path / "integrations/scanpy/guides" / notebook.name
    guide.parent.mkdir(parents=True)
    shutil.copyfile(notebook, guide)
    (source / "conf.py").write_text(
        'extensions = ["myst_parser", "genomespy_notebook"]\n'
        'myst_enable_extensions = ["colon_fence"]\n'
    )
    (source / "index.md").write_text(
        f"```{{genomespy-notebook}} integrations/scanpy/guides/{notebook.name}\n```\n"
    )
    warnings = io.StringIO()
    app = SphinxTestApp(srcdir=source, builddir=tmp_path / "build", warning=warnings)
    output = Path(app.outdir)
    try:
        app.build()
    finally:
        app.cleanup()
    assert not warnings.getvalue()
    html = (output / "index.html").read_text()
    assert f"<h1>{title}" in html
    assert 'class="gs-notebook' in html
    assert html.count('class="gs-doc-embed"') == 3
    assert f'id="{section}"' in html
    downloads = list((output / "_downloads").glob(f"*/{notebook.name}"))
    assert len(downloads) == 1
    assert downloads[0].read_bytes() == notebook.read_bytes()


def test_notebook_failures_identify_the_cell(notebook_extension, tmp_path):
    path = tmp_path / "broken.ipynb"
    path.write_text(
        json.dumps(
            {
                "cells": [
                    {"cell_type": "code", "source": ["raise ValueError('bad example')"]}
                ]
            }
        )
    )
    with pytest.raises(ValueError, match="broken.ipynb, cell 1: bad example"):
        notebook_extension._notebook_markdown(
            path, download_path=path.name, bundle_url="/core.js"
        )


@pytest.mark.parametrize("path", [GUIDE, EXPRESSION_GUIDE])
def test_guide_source_has_no_saved_outputs(path):
    notebook = json.loads(path.read_text())
    assert "widgets" not in notebook["metadata"]
    for cell in notebook["cells"]:
        if cell["cell_type"] == "code":
            assert cell["outputs"] == []
            assert cell["execution_count"] is None


def test_expression_page_reuses_one_explicit_tree(notebook_extension, monkeypatch):
    sc = pytest.importorskip("scanpy")
    from genome_spy.chart import TopLevelSpec

    original = sc.datasets.pbmc68k_reduced()
    loaded = original.copy()
    monkeypatch.setattr(sc.datasets, "pbmc68k_reduced", lambda: loaded)
    dendrogram, calls = sc.tl.dendrogram, []

    def prepare_tree(adata, **kwargs):
        calls.append((adata, kwargs))
        return dendrogram(adata, **kwargs)

    def forbidden(*args, **kwargs):
        pytest.fail("Expression documentation reran analysis or made a widget")

    monkeypatch.setattr(sc.tl, "dendrogram", prepare_tree)
    for module, name in [
        (sc.pp, "neighbors"),
        (sc.tl, "umap"),
        (sc.tl, "rank_genes_groups"),
        (sc.readwrite, "_download"),
        (TopLevelSpec, "widget"),
    ]:
        monkeypatch.setattr(module, name, forbidden)
    markdown = notebook_extension._notebook_markdown(
        EXPRESSION_GUIDE, download_path="expression.ipynb", bundle_url="/core.js"
    )
    assert len(calls) == 1
    assert calls[0][0] is loaded
    assert calls[0][1] == {"groupby": "bulk_labels"}
    assert loaded.obs.equals(original.obs)
    assert set(loaded.uns) - set(original.uns) == {"dendrogram_bulk_labels"}
    np.testing.assert_array_equal(loaded.obsm["X_pca"], original.obsm["X_pca"])
    specs = [json.loads(value) for value in re.findall(r"const spec = (.*);", markdown)]
    assert len(specs) == 3
    rows = [
        next(rows for rows in spec["datasets"].values() if "_gene" in rows[0])
        for spec in specs
    ]
    assert [len(table) for table in rows] == [100, 100, 7000]
    for table in rows[:2]:
        assert len({row["_gene"] for row in table}) == 10
        assert len({row["_group"] for row in table}) == 10
    cells = rows[2]
    assert {row["_obs_id"] for row in cells} == set(original.obs_names)
    assert [row["_group"] for row in rows[0]] == [row["_group"] for row in rows[1]]
    gene = sc.get.obs_df(original, keys=["CD79A"], use_raw=True)["CD79A"].to_numpy()
    group = original.obs["bulk_labels"] == rows[0][0]["_group"]
    assert rows[0][0]["_mean"] == pytest.approx(gene[group].mean())
    assert rows[0][0]["_percent"] == pytest.approx(100 * (gene[group] > 0).mean())
    assert all(0 <= row["_mean"] <= 1 for row in rows[1])
    cell = next(
        row for row in cells if row["_gene"] == "CD79A" and 0 < row["_value"] < 1
    )
    index = original.obs_names.get_loc(cell["_obs_id"])
    expected = (gene[index] - gene.min()) / (gene.max() - gene.min())
    assert cell["_value"] == pytest.approx(expected)
