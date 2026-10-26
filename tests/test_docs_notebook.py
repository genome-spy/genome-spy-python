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


def test_notebook_download_and_page_build_from_one_source(notebook_extension, tmp_path):
    pytest.importorskip("scanpy")
    from sphinx.application import Sphinx

    source = tmp_path / "docs"
    source.mkdir()
    guide = tmp_path / "integrations/scanpy/guides/umap.ipynb"
    guide.parent.mkdir(parents=True)
    shutil.copyfile(GUIDE, guide)
    (source / "conf.py").write_text(
        'extensions = ["myst_parser", "genomespy_notebook"]\n'
        'myst_enable_extensions = ["colon_fence"]\n'
    )
    (source / "index.md").write_text(
        "```{genomespy-notebook} integrations/scanpy/guides/umap.ipynb\n```\n"
    )
    warnings = io.StringIO()
    output = tmp_path / "html"
    app = Sphinx(
        str(source),
        str(source),
        str(output),
        str(tmp_path / "doctrees"),
        "html",
        status=io.StringIO(),
        warning=warnings,
        freshenv=True,
    )
    app.build()
    assert not warnings.getvalue()
    html = (output / "index.html").read_text()
    assert "<h1>UMAP and embeddings" in html
    assert 'class="gs-notebook' in html
    assert html.count('class="gs-doc-embed"') == 3
    assert 'id="select-cells"' in html
    downloads = list((output / "_downloads").glob("*/umap.ipynb"))
    assert len(downloads) == 1
    assert downloads[0].read_bytes() == GUIDE.read_bytes()


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


def test_guide_source_has_no_saved_outputs():
    notebook = json.loads(GUIDE.read_text())
    assert "widgets" not in notebook["metadata"]
    for cell in notebook["cells"]:
        if cell["cell_type"] == "code":
            assert cell["outputs"] == []
            assert cell["execution_count"] is None
