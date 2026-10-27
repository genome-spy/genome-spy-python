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
TRACKS_GUIDE = GUIDE.with_name("tracks.ipynb")
PCA_GUIDE = GUIDE.with_name("pca.ipynb")
RANKED_GUIDE = GUIDE.with_name("ranked.ipynb")
QUALITY_GUIDE = GUIDE.with_name("quality.ipynb")
LARGER_GUIDE = GUIDE.with_name("larger_data.ipynb")
PAGA_GUIDE = GUIDE.with_name("paga.ipynb")
PROFILES_GUIDE = GUIDE.with_name("profiles.ipynb")


@pytest.fixture
def notebook_extension(monkeypatch):
    pytest.importorskip("sphinx")
    monkeypatch.syspath_prepend(str(ROOT / "docs/_ext"))
    return importlib.import_module("genomespy_notebook")


def test_tracks_page_reuses_scanpy_access_and_only_the_explicit_tree(
    notebook_extension, monkeypatch
):
    sc = pytest.importorskip("scanpy")
    from genome_spy.chart import TopLevelSpec
    from anndata import read_h5ad

    notebook = json.loads(TRACKS_GUIDE.read_text())
    if not notebook_extension._preparation_current(notebook, ROOT):
        pytest.skip("Run integrations/scanpy/prepare_guide_data.py tracks first")

    original = sc.datasets.pbmc68k_reduced()
    loaded = original.copy()
    genes = ["CD79A", "MS4A1", "CST3", "LYZ", "CD3D", "IL32"]
    expected = sc.get.obs_df(original, keys=genes, use_raw=True)
    large = read_h5ad(notebook_extension._prepared_paths(notebook, ROOT)["pbmc3k"])
    large_genes = [
        "IL7R",
        "CD14",
        "LYZ",
        "MS4A1",
        "CD8A",
        "GNLY",
        "NKG7",
        "FCGR3A",
        "MS4A7",
        "FCER1A",
        "CST3",
        "PPBP",
    ]
    large_expected = sc.get.obs_df(large, keys=large_genes, use_raw=True)
    monkeypatch.setattr(sc.datasets, "pbmc68k_reduced", lambda: loaded)
    getter, tree = sc.get.obs_df, sc.tl.dendrogram
    reads, analyses = [], []

    def selected(*args, **kwargs):
        reads.append(kwargs)
        return getter(*args, **kwargs)

    def prepare_tree(*args, **kwargs):
        analyses.append(kwargs)
        return tree(*args, **kwargs)

    def forbidden(*args, **kwargs):
        pytest.fail("The tracks guide refitted analysis or used another renderer")

    monkeypatch.setattr(sc.get, "obs_df", selected)
    monkeypatch.setattr(sc.tl, "dendrogram", prepare_tree)
    for module, name in [
        (sc.pp, "neighbors"),
        (sc.tl, "pca"),
        (sc.tl, "umap"),
        (sc.tl, "rank_genes_groups"),
        (sc.pl, "tracksplot"),
        (sc.datasets, "pbmc3k_processed"),
        (sc.readwrite, "_download"),
        (TopLevelSpec, "widget"),
    ]:
        monkeypatch.setattr(module, name, forbidden)
    markdown = notebook_extension._notebook_markdown(
        TRACKS_GUIDE, download_path="tracks.ipynb", bundle_url="/core.js"
    )
    specs = [json.loads(value) for value in re.findall(r"const spec = (.*);", markdown)]
    assert len(specs) == 3
    assert analyses == [{"groupby": "bulk_labels"}]
    assert len(reads) == 3 and all(call["use_raw"] for call in reads)
    assert all(call["keys"] == ["bulk_labels", *genes] for call in reads[:2])
    assert reads[2]["keys"] == ["louvain", *large_genes]
    for spec, source, oracle in zip(
        specs,
        [original, original, large],
        [expected, expected, large_expected],
        strict=True,
    ):
        rows = spec["datasets"][spec["data"]["name"]]
        assert len(rows) == len(source)
        assert {row["_obs_id"] for row in rows} == set(source.obs_names)
        labels = [
            panel["title"]["text"]
            for panel in spec["vconcat"]
            if "layer" in panel.get("spec", panel)
        ]
        assert set(labels) == set(oracle.columns)
        np.testing.assert_array_equal(
            [[row[f"_value_{i}"] for i in range(len(labels))] for row in rows],
            oracle.loc[[row["_obs_id"] for row in rows], labels].to_numpy(),
        )
    assert len(large) == 2638 and len(large_genes) == 12
    assert specs[2]["spacing"] == 6 and specs[2]["scales"]["x"]["gapWidth"] == 3
    assert loaded.obs.equals(original.obs)
    np.testing.assert_array_equal(loaded.X, original.X)


def test_umap_page_preserves_coordinates_and_prepares_density(
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
    density, density_calls = sc.tl.embedding_density, []

    def prepare_density(*args, **kwargs):
        density_calls.append(kwargs)
        return density(*args, **kwargs)

    monkeypatch.setattr(sc.tl, "embedding_density", prepare_density)
    markdown = notebook_extension._notebook_markdown(
        GUIDE, download_path="umap.ipynb", bundle_url="/core.js"
    )
    specs = [json.loads(value) for value in re.findall(r"const spec = (.*);", markdown)]
    assert len(specs) == 11
    for spec in specs[:7]:
        rows = next(rows for rows in spec["datasets"].values() if "_coord_0" in rows[0])
        assert len(rows) == 700
        np.testing.assert_array_equal(
            [[row["_coord_0"], row["_coord_1"]] for row in rows],
            original.obsm["X_umap"],
        )
    np.testing.assert_array_equal(loaded.obsm["X_umap"], original.obsm["X_umap"])
    assert loaded.obs[original.obs.columns].equals(original.obs)
    assert set(loaded.obs) - set(original.obs) == {"umap_density_phase"}
    assert density_calls == [{"basis": "umap", "groupby": "phase"}]
    pca_rows = next(iter(specs[7]["datasets"].values()))
    np.testing.assert_array_equal(
        [[r["_coord_0"], r["_coord_1"]] for r in pca_rows],
        original.obsm["X_pca"][:, :2],
    )
    assert "view.parameter_values.get(brush.name)" in markdown
    assert "{download}`Download notebook <umap.ipynb>`" in markdown


@pytest.mark.parametrize(
    "notebook, title, section, charts",
    [
        (GUIDE, "UMAP and embeddings", "select-cells", 11),
        (EXPRESSION_GUIDE, "Expression plots", "heatmap", 9),
        (TRACKS_GUIDE, "Expression tracks", "plot-individual-cells", 3),
        (PCA_GUIDE, "PCA diagnostics", "show-the-pca-overview", 3),
        (RANKED_GUIDE, "Ranked genes", "inspect-ranking-scores", 4),
        (QUALITY_GUIDE, "Data checks", "check-the-most-abundant-genes", 3),
        (LARGER_GUIDE, "A larger PBMC dataset", "inspect-the-original-counts", 4),
        (PAGA_GUIDE, "PAGA graphs and paths", "plot-group-connections", 10),
        (PROFILES_GUIDE, "Profiles and simulations", "plot-simulation-runs", 7),
    ],
)
def test_notebook_download_and_page_build_from_one_source(
    notebook_extension, tmp_path, notebook, title, section, charts
):
    pytest.importorskip("scanpy")
    from sphinx.testing.util import SphinxTestApp

    source = tmp_path / "docs"
    source.mkdir()
    guide = tmp_path / "integrations/scanpy/guides" / notebook.name
    guide.parent.mkdir(parents=True)
    shutil.copyfile(notebook, guide)
    content = json.loads(notebook.read_text())
    prepared = notebook_extension._prepared_paths(content, ROOT)
    if prepared and not notebook_extension._preparation_current(content, ROOT):
        pytest.skip("Run integrations/scanpy/prepare_guide_data.py first")
    for path in prepared.values():
        target = tmp_path / path.relative_to(ROOT)
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(path, target)
        shutil.copyfile(path.with_suffix(".sha256"), target.with_suffix(".sha256"))
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
    assert html.count('class="gs-doc-embed"') == charts
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


@pytest.mark.parametrize(
    "path",
    [
        GUIDE,
        EXPRESSION_GUIDE,
        TRACKS_GUIDE,
        PCA_GUIDE,
        RANKED_GUIDE,
        QUALITY_GUIDE,
        LARGER_GUIDE,
        PAGA_GUIDE,
        PROFILES_GUIDE,
    ],
)
def test_guide_source_has_no_saved_outputs(path):
    notebook = json.loads(path.read_text())
    assert "widgets" not in notebook["metadata"]
    ids = [cell["id"] for cell in notebook["cells"]]
    assert len(ids) == len(set(ids))
    for cell in notebook["cells"]:
        if cell["cell_type"] == "code":
            assert cell["outputs"] == []
            assert cell["execution_count"] is None


def test_prepared_inputs_skip_analysis_and_detect_stale_data(
    notebook_extension, tmp_path, monkeypatch
):
    """Prepared pages load matching data and fail before executing analysis."""
    ad = pytest.importorskip("anndata")
    pytest.importorskip("scanpy")
    data = tmp_path / "tmp/input.h5ad"
    data.parent.mkdir()
    ad.AnnData(np.ones((2, 3))).write_h5ad(data)
    notebook = {
        "metadata": {"genomespy": {"prepared_data": {"adata": "tmp/input.h5ad"}}},
        "cells": [
            {
                "cell_type": "code",
                "source": ["raise RuntimeError('analysis ran')"],
                "metadata": {"tags": ["prepare-data"]},
            },
            {
                "cell_type": "code",
                "source": ["assert adata.shape == (2, 3)"],
                "metadata": {},
            },
        ],
    }
    path = tmp_path / "example.ipynb"
    path.write_text(json.dumps(notebook))

    def render():
        return notebook_extension._notebook_markdown(
            path, download_path=path.name, bundle_url="/core.js", root=tmp_path
        )

    with pytest.raises(ValueError, match="Missing or stale prepared data"):
        render()
    signature = notebook_extension._preparation_digest(notebook)
    data.with_suffix(".sha256").write_text(
        f"{signature}\n{notebook_extension._file_digest(data)}\n"
    )
    assert "analysis ran" in render()
    with monkeypatch.context() as changed_version:
        changed_version.setattr(
            notebook_extension, "version", lambda name: "new-version"
        )
        with pytest.raises(ValueError, match="Missing or stale prepared data"):
            render()
    # New analysis invalidates a cached file even when its bytes are unchanged.
    notebook["cells"][0]["source"] = ["raise RuntimeError('new analysis ran')"]
    path.write_text(json.dumps(notebook))
    with pytest.raises(ValueError, match="Missing or stale prepared data"):
        render()
    path.write_text(path.read_text().replace("new analysis ran", "analysis ran"))
    data.write_bytes(b"corrupted data")
    with pytest.raises(ValueError, match="Missing or stale prepared data"):
        render()


@pytest.mark.parametrize("filename", ["../input.h5ad", "input.h5ad", "tmp/input.csv"])
def test_prepared_paths_stay_in_ignored_cache(notebook_extension, tmp_path, filename):
    notebook = {"metadata": {"genomespy": {"prepared_data": {"adata": filename}}}}
    with pytest.raises(ValueError, match="H5AD files inside tmp/"):
        notebook_extension._prepared_paths(notebook, tmp_path)


def test_preparation_command_reuses_matching_inputs(
    notebook_extension, monkeypatch, tmp_path
):
    """The explicit command runs analysis once and restores its working folder."""
    sc = pytest.importorskip("scanpy")
    spec = importlib.util.spec_from_file_location(
        "prepare_guide_data", ROOT / "integrations/scanpy/prepare_guide_data.py"
    )
    command = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(command)
    monkeypatch.setattr(command, "ROOT", tmp_path)
    monkeypatch.setattr(sc.settings, "_datasetdir", sc.settings.datasetdir)
    monkeypatch.setattr("sys.argv", ["prepare_guide_data.py", "example"])
    guide = tmp_path / "integrations/scanpy/guides/example.ipynb"
    guide.parent.mkdir(parents=True)
    guide.write_text(
        json.dumps(
            {
                "metadata": {
                    "genomespy": {"prepared_data": {"adata": "tmp/input.h5ad"}}
                },
                "cells": [
                    {
                        "cell_type": "code",
                        "metadata": {"tags": ["prepare-data"]},
                        "source": [
                            "import anndata as ad\nimport numpy as np\nadata = ad.AnnData(np.ones((2, 3)))"
                        ],
                    }
                ],
            }
        )
    )
    cwd = Path.cwd()
    command.main()
    assert Path.cwd() == cwd
    target = tmp_path / "tmp/input.h5ad"
    stamp = target.stat().st_mtime_ns
    command.main()
    assert target.stat().st_mtime_ns == stamp
    assert notebook_extension._preparation_current(
        json.loads(guide.read_text()), tmp_path
    )
    monkeypatch.setattr("sys.argv", ["prepare_guide_data.py", "../../../outside"])
    with pytest.raises(SystemExit):
        command.main()


@pytest.mark.parametrize("path, charts", [(QUALITY_GUIDE, 3), (LARGER_GUIDE, 4)])
def test_real_data_pages_use_sparse_prepared_inputs(
    notebook_extension, monkeypatch, path, charts
):
    sc = pytest.importorskip("scanpy")
    from scipy.sparse import csc_matrix, csr_matrix, issparse

    notebook = json.loads(path.read_text())
    if not notebook_extension._preparation_current(notebook, ROOT):
        pytest.skip("Run integrations/scanpy/prepare_guide_data.py first")

    def forbidden(*args, **kwargs):
        pytest.fail("A prepared page downloaded data or reran analysis")

    for module, name in [
        (sc.pp, "scrublet"),
        (sc.pp, "highly_variable_genes"),
        (sc.pp, "pca"),
        (sc.pp, "neighbors"),
        (sc.tl, "umap"),
        (sc.datasets, "pbmc3k"),
        (sc, "read_10x_mtx"),
    ]:
        monkeypatch.setattr(module, name, forbidden)
    toarrays = {csr_matrix: csr_matrix.toarray, csc_matrix: csc_matrix.toarray}
    dense_shapes = []

    def selected_columns(matrix, *args, **kwargs):
        assert matrix.shape[1] <= 20, (
            "Plotting densified an unselected expression matrix"
        )
        dense_shapes.append(matrix.shape)
        return toarrays[type(matrix)](matrix, *args, **kwargs)

    for matrix_type in toarrays:
        monkeypatch.setattr(matrix_type, "toarray", selected_columns)
    markdown = notebook_extension._notebook_markdown(
        path, download_path=path.name, bundle_url="/core.js"
    )
    specs = [json.loads(value) for value in re.findall(r"const spec = (.*);", markdown)]
    assert len(specs) == charts
    assert dense_shapes
    assert max(rows for rows, _ in dense_shapes) == (
        2700 if path == QUALITY_GUIDE else 11769
    )
    files = notebook_extension._prepared_paths(notebook, ROOT)
    counts = sc.read_h5ad(files["counts" if path == QUALITY_GUIDE else "raw"])
    assert counts.shape == ((2700, 32738) if path == QUALITY_GUIDE else (11769, 33538))
    assert issparse(counts.X)
    if path == LARGER_GUIDE:
        prepared = sc.read_h5ad(files["adata"])
        assert prepared.shape == (11537, 20292)
        assert isinstance(prepared.X, csr_matrix)
        rows = next(iter(specs[2]["datasets"].values()))
        assert len(rows) == 11537
        np.testing.assert_array_equal(
            [[r["_coord_0"], r["_coord_1"]] for r in rows], prepared.obsm["X_umap"]
        )


@pytest.mark.parametrize("path, charts", [(PAGA_GUIDE, 10), (PROFILES_GUIDE, 7)])
def test_graph_and_profile_pages_read_prepared_results(
    notebook_extension, monkeypatch, path, charts
):
    sc = pytest.importorskip("scanpy")
    notebook = json.loads(path.read_text())
    if not notebook_extension._preparation_current(notebook, ROOT):
        pytest.skip("Run integrations/scanpy/prepare_guide_data.py first")
    files = notebook_extension._prepared_paths(notebook, ROOT)
    pbmc = sc.read_h5ad(files["pbmc"])

    def forbidden(*args, **kwargs):
        pytest.fail("A graph/profile page reran analysis, layout or simulation")

    for module, name in [
        (sc.pp, "neighbors"),
        (sc.tl, "paga"),
        (sc.pl, "paga"),
        (sc.tl, "diffmap"),
        (sc.tl, "dpt"),
        (sc.tl, "sim"),
        (sc.datasets, "pbmc68k_reduced"),
        (sc.datasets, "krumsiek11"),
    ]:
        monkeypatch.setattr(module, name, forbidden)
    markdown = notebook_extension._notebook_markdown(
        path, download_path=path.name, bundle_url="/core.js"
    )
    specs = [json.loads(value) for value in re.findall(r"const spec = (.*);", markdown)]
    assert len(specs) == charts
    if path == PAGA_GUIDE:
        from tests.integrations.scanpy.helpers import leaf_marks

        assert not any(
            mark.get("encoding", {}).get("text", {}).get("field") == "_value"
            for mark in leaf_marks(specs[5])
        )
        for spec in specs[:4]:
            nodes = next(
                rows for rows in spec["datasets"].values() if "_group" in rows[0]
            )
            assert len(nodes) == 10
            np.testing.assert_array_equal(
                [[r["_x"], r["_y"]] for r in nodes], pbmc.uns["paga"]["pos"]
            )
        rows = next(
            rows for rows in specs[7]["datasets"].values() if "_coord_0" in rows[0]
        )
        np.testing.assert_array_equal(
            [[r["_coord_0"], r["_coord_1"]] for r in rows], pbmc.obsm["X_umap"]
        )
    else:
        simulation = sc.read_h5ad(files["simulation"])
        assert simulation.shape == (640, 11)
        assert simulation.obs_names.is_unique
        assert "dpt_order_indices" in simulation.obs
        genes = ["Gata2", "Gata1", "Cebpa", "Pu.1", "Gfi1"]
        points = next(
            rows for rows in specs[3]["datasets"].values() if "_series" in rows[0]
        )
        assert len(points) == 640 * len(genes)
        for row in points:
            assert row["_time"] == row["_sample"]
            gene = simulation.var_names.get_loc(row["_series"])
            assert row["_value"] == simulation.X[row["_sample"], gene]
        tiles = next(
            rows for rows in specs[6]["datasets"].values() if "_value" in rows[0]
        )
        assert len(tiles) == len(points)
        order = simulation.obs["dpt_order_indices"].to_numpy()
        values = simulation[:, genes].X[order]
        for row in tiles:
            assert row["_value"] == values[row["_x"], row["_y"]]


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
    assert len(specs) == 9
    assert "Cell group" not in json.dumps(specs[3])
    assert all(specs[2]["scales"][axis]["gapWidth"] == 1 for axis in ("x", "y"))
    rows = [
        next(rows for rows in spec["datasets"].values() if "_gene" in rows[0])
        for spec in specs[:3]
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


@pytest.mark.parametrize("path, charts", [(PCA_GUIDE, 3), (RANKED_GUIDE, 4)])
def test_diagnostic_guides_read_stored_results(
    notebook_extension, monkeypatch, path, charts
):
    sc = pytest.importorskip("scanpy")
    original = sc.datasets.pbmc68k_reduced()
    loaded = original.copy()
    monkeypatch.setattr(sc.datasets, "pbmc68k_reduced", lambda: loaded)

    def forbidden(*args, **kwargs):
        pytest.fail(
            "A diagnostic guide reran PCA, embeddings or differential expression"
        )

    for module, name in [
        (sc.pp, "pca"),
        (sc.tl, "pca"),
        (sc.tl, "umap"),
        (sc.tl, "rank_genes_groups"),
        (sc.readwrite, "_download"),
    ]:
        monkeypatch.setattr(module, name, forbidden)
    markdown = notebook_extension._notebook_markdown(
        path, download_path=path.name, bundle_url="/core.js"
    )
    assert len(re.findall(r"const spec = (.*);", markdown)) == charts
    assert loaded.obs.equals(original.obs)
    assert loaded.var.equals(original.var)
    np.testing.assert_array_equal(loaded.obsm["X_pca"], original.obsm["X_pca"])
    np.testing.assert_array_equal(loaded.varm["PCs"], original.varm["PCs"])
    np.testing.assert_array_equal(
        loaded.uns["pca"]["variance_ratio"], original.uns["pca"]["variance_ratio"]
    )
    for key in ("names", "scores"):
        np.testing.assert_array_equal(
            loaded.uns["rank_genes_groups"][key], original.uns["rank_genes_groups"][key]
        )
