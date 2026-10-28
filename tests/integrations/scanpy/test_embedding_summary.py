"""Detached builder state, native composition and expression palette contracts."""

import json

import numpy as np
import pandas as pd
import pytest

import genome_spy.integrations.scanpy as gsc
from tests.integrations.scanpy.helpers import units, leaf_marks

pytest.importorskip("scanpy")


@pytest.fixture
def adata():
    from anndata import AnnData

    a = AnnData(
        np.array(
            [
                [-1, np.nan],
                [0, np.nan],
                [0.5, np.nan],
                [1, np.nan],
                [2, np.nan],
                [np.nan, np.nan],
            ]
        ),
        obs=pd.DataFrame(
            {"type": pd.Categorical(["A", "A", "B", "B", "B", "A"])},
            index=[f"cell-{i}" for i in range(6)],
        ),
        var=pd.DataFrame(index=["HLA-DRA", "missing.gene"]),
    )
    a.obsm["X_umap"] = np.array(
        [[0, 0], [1, 0], [2, 1], [3, 1], [4, 2], [5, 2]], dtype=float
    )
    return a


def records(chart):
    spec = chart.to_dict()
    return spec["datasets"][spec["data"]["name"]]


def panel_titles(chart):
    result = {}
    for view in units(chart.to_dict()):
        names = {leaf.get("name") for leaf in leaf_marks(view)}
        if view.get("name") == "umap-brush-cells":
            key = "embedding"
        elif "selected-expression" in names:
            key = "heatmap"
        elif "all-expression-histogram" in names:
            key = "histogram"
        elif "all-composition" in names:
            key = "composition"
        else:
            continue
        title = view.get("title")
        result[key] = title["text"] if isinstance(title, dict) else title
    return result


def test_omitted_titles_keep_current_automatic_defaults(adata):
    chart = (
        gsc.pl.EmbeddingSummary(adata, "HLA-DRA", "type")
        .add_heatmap()
        .add_histogram()
        .add_composition()
        .to_chart()
    )
    assert panel_titles(chart) == {
        "embedding": "type",
        "heatmap": "Selected cells: mean expression",
        "histogram": "HLA-DRA expression: selection vs all cells",
        "composition": "type: composition",
    }


def test_heatmap_labels_use_the_requested_grouping(adata):
    adata.obs = adata.obs.rename(columns={"type": "sample"})
    chart = gsc.pl.EmbeddingSummary(adata, "HLA-DRA", "sample").add_heatmap().to_chart()
    tiles = next(
        view
        for view in units(chart.to_dict())
        if view.get("name") == "selected-expression"
    )
    assert tiles["encoding"]["x"]["title"] == "sample"
    assert tiles["encoding"]["tooltip"][0]["title"] == "sample"


def test_heatmap_values_are_opt_in_and_preserve_data_and_snapshots(adata):
    plot = gsc.pl.EmbeddingSummary(adata, "HLA-DRA", "type").add_heatmap()
    first = plot.to_chart()
    snapshot = json.dumps(first.to_dict())
    enabled = plot.add_heatmap(show_values=True).to_chart()

    def labels(chart):
        return [
            leaf
            for unit in units(chart.to_dict())
            for leaf in leaf_marks(unit)
            if leaf.get("encoding", {}).get("text", {}).get("field") == "mean"
        ]

    assert not labels(first)
    assert len(labels(enabled)) == 1
    assert records(first) == records(enabled)
    assert json.dumps(first.to_dict()) == snapshot
    assert not labels(plot.add_heatmap(show_values=False).to_chart())


@pytest.mark.parametrize("value", [None, 1, "true"])
def test_heatmap_show_values_requires_a_boolean(adata, value):
    plot = gsc.pl.EmbeddingSummary(adata, "HLA-DRA", "type")
    with pytest.raises(TypeError, match="show_values must be boolean"):
        plot.add_heatmap(show_values=value)


@pytest.mark.parametrize("title", ["Custom title", "", None])
def test_custom_and_hidden_titles_preserve_snapshot_and_data(adata, title):
    plot = (
        gsc.pl.EmbeddingSummary(adata, "HLA-DRA", "type", title=title)
        .add_heatmap(title=title)
        .add_histogram(title=title)
        .add_composition(title=title)
    )
    first = plot.to_chart()
    snapshot = json.dumps(first.to_dict())
    assert panel_titles(first) == dict.fromkeys(
        ["embedding", "heatmap", "histogram", "composition"], title
    )
    second = plot.add_heatmap(title="Revised mean").to_chart()
    assert panel_titles(second)["heatmap"] == "Revised mean"
    assert json.dumps(first.to_dict()) == snapshot
    assert records(first) == records(second)


@pytest.mark.parametrize(
    "panel", ["constructor", "add_heatmap", "add_histogram", "add_composition"]
)
def test_invalid_titles_fail_before_expression_reads(adata, monkeypatch, panel):
    import scanpy as sc

    plot = gsc.pl.EmbeddingSummary(adata, "HLA-DRA", "type")

    def forbidden(*args, **kwargs):
        pytest.fail("Changing or validating a title must not read expression")

    monkeypatch.setattr(sc.get, "obs_df", forbidden)
    with pytest.raises(TypeError, match="title must be a string or None"):
        if panel == "constructor":
            gsc.pl.EmbeddingSummary(adata, "HLA-DRA", "type", title=123)
        else:
            getattr(plot, panel)(title=123)


@pytest.fixture
def metadata_adata(adata):
    adata.obs["sample.label"] = pd.Categorical(
        ["D1", "D1", "D2", None, "D2", "D3"], categories=["D3", "D2", "D1", "Unused"]
    )
    adata.uns["sample.label_colors"] = ["purple", "orange", "teal", "pink"]
    adata.obs["qc.score"] = [0.0, np.nan, -0.5, 0.5, 1.0, np.nan]
    return adata


def test_observation_snapshot_and_panel_replacement(metadata_adata):
    a = metadata_adata
    original = a.copy()
    plot = gsc.pl.EmbeddingSummary(
        a, "HLA-DRA", "type", obs_keys=["sample.label", "qc.score"]
    )
    first = (
        plot.add_composition("sample.label").add_histogram(obs="qc.score").to_chart()
    )
    snapshot = json.dumps(first.to_dict())
    assert a.obs.equals(original.obs)
    a.obs["qc.score"] = 999
    a.obs["sample.label"] = "changed"
    second = plot.style(alpha=0.8).add_composition("type", position="left").to_chart()
    assert json.dumps(first.to_dict()) == snapshot
    data = records(second)
    assert any(row.get("_obs_1") == "NA" for row in data)
    assert any(
        value == -0.5
        for row in data
        for key, value in row.items()
        if key.startswith("_obs_")
    )
    leaves = [leaf for unit in units(first.to_dict()) for leaf in leaf_marks(unit)]
    bars = next(leaf for leaf in leaves if leaf.get("name") == "all-composition")
    assert bars["encoding"]["y"]["scale"]["domain"] == [
        "D3",
        "D2",
        "D1",
        "Unused",
        "NA",
    ]
    assert bars["encoding"]["color"]["scale"]["range"] == [
        "purple",
        "orange",
        "teal",
        "pink",
        "lightgray",
    ]
    spec = (
        plot.add_composition(show=False).add_histogram(show=False).to_chart().to_dict()
    )
    assert len(units(spec)) == 1


def test_composition_reuses_umap_palette_and_order_with_missing_values(adata):
    adata.obs.loc["cell-0", "type"] = None
    plot = gsc.pl.EmbeddingSummary(
        adata,
        "HLA-DRA",
        "type",
        palette={"A": "red", "B": "blue"},
        categories_order=["B", "A"],
    ).add_composition()
    leaves = [
        leaf for unit in units(plot.to_chart().to_dict()) for leaf in leaf_marks(unit)
    ]
    points = next(leaf for leaf in leaves if leaf.get("name") == "umap-points")
    bars = next(leaf for leaf in leaves if leaf.get("name") == "all-composition")
    assert bars["encoding"]["color"]["scale"] == points["encoding"]["color"]["scale"]
    assert bars["encoding"]["y"]["scale"]["domain"] == ["B", "A", "NA"]


def test_obs_keys_and_panel_types_are_explicit(metadata_adata):
    for keys in (["absent"], ["qc.score", "qc.score"], {"a": "qc.score"}):
        with pytest.raises(ValueError, match="distinct observation columns"):
            gsc.pl.EmbeddingSummary(metadata_adata, "HLA-DRA", "type", obs_keys=keys)
    plot = gsc.pl.EmbeddingSummary(
        metadata_adata, "HLA-DRA", "type", obs_keys=["qc.score", "sample.label"]
    )
    with pytest.raises(ValueError, match="numeric column"):
        plot.add_histogram(obs="sample.label")
    with pytest.raises(ValueError, match="not both"):
        plot.add_histogram("HLA-DRA", obs="qc.score")
    with pytest.raises(ValueError, match="categorical column"):
        plot.add_composition("qc.score")
    metadata_adata.obs["qc.score"] = np.inf
    with pytest.raises(ValueError, match="finite or missing"):
        gsc.pl.EmbeddingSummary(metadata_adata, "HLA-DRA", "type", obs_keys="qc.score")


def test_snapshot_reuses_preparation_and_preserves_anndata(adata, monkeypatch):
    import scanpy as sc

    original = adata.copy()
    plot = gsc.pl.EmbeddingSummary(
        adata, ["HLA-DRA", "missing.gene"], "type", use_raw=False
    )
    assert list(adata.obs.columns) == list(original.obs.columns)
    assert dict(adata.uns) == dict(original.uns)
    np.testing.assert_equal(adata.X, original.X)
    first = plot.add_heatmap().add_histogram("HLA-DRA").to_chart()
    snapshot = json.dumps(first.to_dict())

    def forbidden(*args, **kwargs):
        pytest.fail("Builder presentation must not read AnnData again")

    monkeypatch.setattr(sc.get, "obs_df", forbidden)
    adata.X[:] = 999
    second = (
        plot.style(size=4, alpha=0.8)
        .add_heatmap(["missing.gene"], position="left")
        .to_chart()
    )
    assert json.dumps(first.to_dict()) == snapshot
    assert records(first)[0]["_expr_0"] == records(second)[0]["_expr_0"] == -1
    assert records(second)[0]["_expr_1"] is None
    assert records(first)[0]["_size_0"] == 12
    assert records(second)[0]["_size_0"] == 4


@pytest.mark.parametrize("storage", ["dense", "csr", "csc"])
def test_source_and_gene_symbol_reuse(adata, storage):
    from scipy import sparse

    adata.var["symbol"] = ["alpha", "beta"]
    adata.layers["counts"] = np.nan_to_num(adata.X) + 10
    if storage != "dense":
        adata.layers["counts"] = getattr(sparse, storage + "_matrix")(
            adata.layers["counts"]
        )
    adata.raw = adata.copy()
    plot = gsc.pl.EmbeddingSummary(
        adata,
        "alpha",
        "type",
        layer="counts",
        gene_symbols="symbol",
        categories_order=["B", "A"],
        palette="set1",
    )
    assert records(plot.to_chart())[0]["_expr_0"] == 9
    heatmap = next(
        v
        for v in units(plot.add_heatmap().to_chart().to_dict())
        if v.get("name") == "selected-expression"
    )
    assert heatmap["encoding"]["x"]["scale"]["domain"] == ["B", "A"]


@pytest.mark.parametrize("zoom", [False, True])
def test_native_scope_isotropy_and_panel_replacement(adata, zoom):
    plot = gsc.pl.EmbeddingSummary(adata, "HLA-DRA", "type", zoom=zoom)
    for side in ("left", "right", "top", "bottom"):
        chart = (
            plot.add_heatmap(position=side)
            .add_histogram("HLA-DRA", position=side)
            .to_chart()
        )
        spec = chart.to_dict()
        leaves = units(spec)
        embedding = next(v for v in leaves if v.get("name") == "umap-brush-cells")
        points = next(
            v for v in leaf_marks(embedding) if v.get("name") == "umap-points"
        )
        assert spec["params"][0]["name"] == "cells"
        assert embedding["params"][0]["push"] == "outer"
        assert spec["resolve"]["legend"]["default"] == "collected"
        assert (
            spec["resolve"]["scale"]["x"]
            == spec["resolve"]["scale"]["y"]
            == "independent"
        )
        x, y = [points["encoding"][d]["scale"]["domain"] for d in ("x", "y")]
        assert x[1] - x[0] == pytest.approx(y[1] - y[0])
        assert embedding["width"] == embedding["height"]
        assert all(
            points["encoding"][axis]["scale"]["zoom"] is zoom for axis in ("x", "y")
        )
        brush = embedding["params"][0]["select"]
        assert brush.get("on") == (None if zoom else "mousedown")
        assert brush["zoom"] is False
        assert len([v for v in leaves if v.get("name") == "selected-expression"]) == 1
        plot.add_histogram(position=side, show=False)
    spec = (
        plot.add_heatmap(show=False)
        .add_histogram(show=False)
        .legend(show=False)
        .to_chart()
        .to_dict()
    )
    assert len(units(spec)) == 1
    embedding = units(spec)[0]
    points = next(v for v in leaf_marks(embedding) if v.get("name") == "umap-points")
    assert points["encoding"]["color"]["legend"] is None


def test_large_summary_reads_only_requested_genes_and_observations(monkeypatch):
    from anndata import AnnData
    from scipy import sparse

    count = 100_001
    a = AnnData(
        sparse.csr_matrix((count, 20_000)),
        obs=pd.DataFrame(
            {
                "type": pd.Categorical(["A"] * count),
                "qc": np.arange(count),
                "batch": pd.Categorical(["D1"] * count),
            }
        ),
    )
    a.var_names = [f"g{i}" for i in range(a.n_vars)]
    a.obsm["X_umap"] = np.zeros((count, 2))
    original, shapes = sparse.csr_matrix.toarray, []

    def selected(matrix, *args, **kwargs):
        shapes.append(matrix.shape)
        assert matrix.shape == (count, 1), "Densified unrequested genes"
        return original(matrix, *args, **kwargs)

    monkeypatch.setattr(sparse.csr_matrix, "toarray", selected)
    plot = gsc.pl.EmbeddingSummary(a, "g1", "type", obs_keys=["qc", "batch"])
    assert shapes == [(count, 1)]
    assert len(plot._prepared.table) == count
    assert set(plot._observations) == {"type", "qc", "batch"}


def test_invalid_genes_and_numeric_grouping_are_explicit(adata):
    for genes in ([], ["HLA-DRA", "HLA-DRA"], {"markers": "HLA-DRA"}):
        with pytest.raises(ValueError, match="unique gene names"):
            gsc.pl.EmbeddingSummary(adata, genes, "type")
    plot = gsc.pl.EmbeddingSummary(adata, ["HLA-DRA", "missing.gene"], "type")
    with pytest.raises(ValueError, match="gene_controls requires gene"):
        plot.add_histogram(obs="type", gene_controls=True)
    with pytest.raises(ValueError, match="subset"):
        plot.add_heatmap("other")
    adata.obs["numeric"] = range(len(adata))
    with pytest.raises(NotImplementedError, match="numeric grouping"):
        gsc.pl.EmbeddingSummary(adata, "HLA-DRA", "numeric")


@pytest.mark.parametrize("show_values", [False, True])
def test_shared_seurat_palette_in_cell_and_mean_heatmaps(adata, show_values):
    from genome_spy.integrations.scanpy._expression.colors import expression_scale

    expected = expression_scale(
        np.array([-1, 2]), "seurat", -2.5, 2.5, context="test"
    ).to_dict()
    assert expected["domain"] == [-2.5, 0, 2.5]
    assert expected["range"] == ["#ff00ff", "#000000", "#ffff00"]
    for chart in [
        gsc.pl.heatmap(
            adata,
            ["HLA-DRA"],
            "type",
            cmap="seurat",
            vmin=-2.5,
            vmax=2.5,
            show=False,
            show_values=show_values,
        ),
        gsc.pl.MatrixPlot(
            adata, ["HLA-DRA"], "type", vmin=-2.5, vmax=2.5, show_values=show_values
        )
        .style(cmap="seurat")
        .to_chart(),
    ]:
        leaves = [leaf for unit in units(chart.to_dict()) for leaf in leaf_marks(unit)]
        assert any(
            leaf.get("encoding", {}).get("color", {}).get("scale") == expected
            for leaf in leaves
        )


def test_gene_controls_use_loaded_choices_and_preserve_snapshots(adata, monkeypatch):
    import scanpy as sc

    plot = gsc.pl.EmbeddingSummary(adata, ["HLA-DRA", "missing.gene"], "type")
    first = plot.add_histogram("HLA-DRA").to_chart()
    snapshot = first.to_json()

    def forbidden(*args, **kwargs):
        pytest.fail("Gene controls must use the detached constructor values")

    monkeypatch.setattr(sc.get, "obs_df", forbidden)
    second = (
        plot.add_heatmap("HLA-DRA", gene_controls=True)
        .add_histogram(["HLA-DRA", "missing.gene"], gene_controls=True)
        .to_chart()
    )
    controls = [p for p in second.to_dict()["params"] if "bind" in p]
    assert [p["name"] for p in controls] == [
        "heatmap_gene_0",
        "histogram_gene_0",
        "histogram_gene_1",
    ]
    assert [p["value"] for p in controls] == ["HLA-DRA", "HLA-DRA", "missing.gene"]
    assert all(p["bind"]["options"] == ["HLA-DRA", "missing.gene"] for p in controls)
    assert first.to_json() == snapshot
    assert records(first) == records(second)


@pytest.mark.parametrize("panel", ["add_heatmap", "add_histogram"])
def test_gene_controls_require_boolean(adata, panel):
    plot = gsc.pl.EmbeddingSummary(adata, "HLA-DRA", "type")
    with pytest.raises(TypeError, match="gene_controls must be boolean"):
        getattr(plot, panel)(gene_controls="yes")


def test_histogram_groups_replace_and_hide_only_their_own_side(adata, monkeypatch):
    import scanpy as sc

    plot = gsc.pl.EmbeddingSummary(adata, ["HLA-DRA", "missing.gene"], "type")

    def forbidden(*args, **kwargs):
        pytest.fail("Histogram groups must reuse the detached expression values")

    monkeypatch.setattr(sc.get, "obs_df", forbidden)
    first = (
        plot.add_histogram("HLA-DRA", position="left", gene_controls=True)
        .add_histogram(["HLA-DRA", "missing.gene"], gene_controls=True)
        .to_chart()
    )
    snapshot = first.to_json()
    controls = [p for p in first.to_dict()["params"] if "bind" in p]
    assert [p["name"] for p in controls] == [f"histogram_gene_{i}" for i in range(3)]
    assert [p["value"] for p in controls] == ["HLA-DRA", "HLA-DRA", "missing.gene"]

    plot.add_histogram("missing.gene", position="bottom", gene_controls=True)
    second = plot.to_chart()
    assert [p["value"] for p in second.to_dict()["params"] if "bind" in p] == [
        "HLA-DRA",
        "missing.gene",
    ]
    plot.add_histogram(position="bottom", show=False)
    remaining = plot.to_chart()
    assert [p["value"] for p in remaining.to_dict()["params"] if "bind" in p] == [
        "HLA-DRA"
    ]
    histograms = [
        leaf["name"]
        for unit in units(remaining.to_dict())
        for leaf in leaf_marks(unit)
        if "histogram" in leaf.get("name", "")
    ]
    assert histograms == ["all-expression-histogram", "selected-expression-histogram"]
    assert first.to_json() == snapshot
    assert records(first) == records(second) == records(remaining)


@pytest.mark.parametrize("name", ["show_count", "zoom"])
@pytest.mark.parametrize("value", [None, 1, "yes"])
def test_boolean_options_reject_before_data_access(monkeypatch, name, value):
    import scanpy as sc

    def forbidden(*args, **kwargs):
        pytest.fail("Invalid count options must fail before reading data")

    monkeypatch.setattr(sc.get, "obs_df", forbidden)
    with pytest.raises(TypeError, match=f"{name} must be boolean"):
        gsc.pl.EmbeddingSummary(None, "HLA-DRA", "type", **{name: value})


def test_show_count_keeps_default_and_omits_disabled_dataflow(adata, monkeypatch):
    from genome_spy.integrations.scanpy._embedding import (
        summary_chart as _embedding_summary_chart,
    )

    first = gsc.pl.EmbeddingSummary(adata, "HLA-DRA", "type").to_chart()
    explicit = gsc.pl.EmbeddingSummary(
        adata, "HLA-DRA", "type", show_count=True, zoom=False
    ).to_chart()
    assert first.to_dict() == explicit.to_dict()

    def forbidden(*args, **kwargs):
        pytest.fail("Hidden counts must not build a counter branch")

    monkeypatch.setattr(_embedding_summary_chart, "brush_count", forbidden)
    hidden = (
        gsc.pl.EmbeddingSummary(adata, "HLA-DRA", "type", show_count=False)
        .add_histogram()
        .to_chart()
    )
    assert records(hidden) == records(first)
    assert hidden.to_dict()["params"][0] == first.to_dict()["params"][0]
    assert not any(
        leaf.get("name") == "umap-count-cells"
        for unit in units(hidden.to_dict())
        for leaf in leaf_marks(unit)
    )
