"""Verify PBMC values, grouping and shared gallery data."""

from importlib import import_module

import numpy as np
import pyarrow as pa
import pytest

from genome_spy.anndata import from_anndata
from genome_spy.datasets import load_dataset
from genome_spy.datasets._pbmc import expression_table, pbmc_markers


def test_pbmc_subset_preserves_counts_and_group_means() -> None:
    data = load_dataset("pbmc_markers", as_format="json")
    adata = pbmc_markers()
    assert adata.shape == (2638, 12)
    assert adata.obs_names.is_unique
    assert list(adata.var_names) == [
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
    # Independent reference counts from Scanpy's PBMC3k fixture.
    assert adata.obs["cell_type"].value_counts().to_dict() == {
        "CD4 T cells": 1144,
        "CD14+ Monocytes": 480,
        "B cells": 342,
        "CD8 T cells": 316,
        "NK cells": 154,
        "FCGR3A+ Monocytes": 150,
        "Dendritic cells": 37,
        "Megakaryocytes": 15,
    }
    counts = np.expm1(adata.X)
    np.testing.assert_allclose(counts, np.round(counts), atol=1e-4)
    assert np.isfinite(adata.X).all()
    assert np.count_nonzero(adata.X == 0) > 15000
    for group in data["groups"]:
        cells = adata.obs.iloc[group["start"] : group["end"]]
        assert cells["cell_type"].eq(group["cell_type"]).all()
        assert len(cells) == group["count"]
    assert data["groups"][0]["start"] == 0
    assert data["groups"][-1]["end"] == len(adata)
    for row in data["means"]:
        values = adata.X[
            adata.obs["cell_type"].eq(row["cell_type"]), row["marker_order"]
        ]
        assert row["mean_expression"] == pytest.approx(
            values.mean(dtype=np.float64), abs=1e-10
        )
    assert max(adata.X.ravel()) <= data["expression_limit"]


def test_pbmc_projection_reshape_preserves_cell_gene_values() -> None:
    adata = pbmc_markers()
    genes = list(adata.var_names)
    projection = from_anndata(
        adata, obs=["cell", "cell_type", "cell_order", "cell_end"], genes=genes
    )
    table = expression_table(projection, genes)
    assert len(table) == 31656
    assert not table.duplicated(["cell", "gene"]).any()
    for marker, gene in enumerate(genes):
        selected = table[table["gene"] == gene]
        np.testing.assert_array_equal(selected["expression"], adata.X[:, marker])
        assert selected["cell"].tolist() == adata.obs_names.tolist()
        assert selected["marker_order"].eq(marker).all()
        assert selected["cell_order"].tolist() == list(range(2638))
        assert selected["cell_end"].tolist() == list(range(1, 2639))


def test_pbmc_dendrogram_matches_marker_means_and_group_coordinates() -> None:
    from scipy.cluster.hierarchy import leaves_list, linkage

    data = load_dataset("pbmc_markers", as_format="json")
    tree = data["dendrogram"]
    means = {
        group: [
            row["mean_expression"] for row in data["means"] if row["cell_type"] == group
        ]
        for group in tree["input_groups"]
    }
    expected = linkage(
        [means[group] for group in tree["input_groups"]],
        method="single",
        metric="euclidean",
        optimal_ordering=False,
    )
    np.testing.assert_allclose(tree["linkage"], expected, atol=1e-12)
    assert tree["method"] == "single" and tree["metric"] == "euclidean"
    assert tree["features"] == list(pbmc_markers().var_names)
    assert tree["group_order"] == [
        tree["input_groups"][i] for i in leaves_list(expected)
    ]
    # Reference tutorial's leaf order; the fixture is unchanged by this clustering.
    assert tree["group_order"] == [
        "FCGR3A+ Monocytes",
        "CD14+ Monocytes",
        "Dendritic cells",
        "Megakaryocytes",
        "NK cells",
        "CD8 T cells",
        "CD4 T cells",
        "B cells",
    ]
    assert [group["cell_type"] for group in data["groups"]] == tree["group_order"]
    assert expected[-1, 2] == pytest.approx(3.99041187, abs=1e-8)
    segments = data["group_tree"]
    assert len(segments) == 21
    leaf_arms = [segment for segment in segments if segment["distance"] == 0]
    assert sorted((s["row"], s["cell"]) for s in leaf_arms) == [
        (group["group_order"], group["center"]) for group in data["groups"]
    ]
    for i in range(0, len(segments), 3):
        left, right, connector = segments[i : i + 3]
        assert (
            left["distance_end"]
            == right["distance_end"]
            == connector["distance"]
            == connector["distance_end"]
        )
        assert connector["row"] == left["row_end"]
        assert connector["row_end"] == right["row_end"]
        assert connector["cell"] == left["cell_end"]
        assert connector["cell_end"] == right["cell_end"]
    connectors = {s["distance"]: s for s in segments[2::3]}
    for arm in segments:
        if arm["distance"] > 0 and arm["distance"] != arm["distance_end"]:
            child = connectors[arm["distance"]]
            assert arm["row"] == (child["row"] + child["row_end"]) / 2
            assert arm["cell"] == (child["cell"] + child["cell_end"]) / 2
    assert tree["distance_limit"] > expected[-1, 2]


@pytest.mark.docs
@pytest.mark.parametrize("name", ["pbmc_cell_heatmap", "pbmc_expression_tracks"])
def test_pbmc_gallery_shares_one_expression_arrow_table(name: str) -> None:
    module = import_module(f"docs.examples.{name}")
    prepared = module.chart._prepare_render()
    tables = [
        pa.ipc.open_file(pa.BufferReader(buffer)).read_all()
        for buffer in prepared.buffers.values()
    ]
    expression = [table for table in tables if "expression" in table.column_names]
    assert len(expression) == 1
    assert expression[0].num_rows == 31656
    if name == "pbmc_expression_tracks":
        spec = prepared.spec
        assert len(spec["vconcat"]) == 14
        assert spec["resolve"]["scale"] == {
            "x": "shared",
            "y": "independent",
            "color": "shared",
        }
        assert spec["scales"]["x"]["domain"] == [0, 2638]
        assert spec["scales"]["x"]["type"] == "linear"
        assert all(
            track["layer"][0]["mark"]["minWidth"] == 0
            for track in spec["vconcat"][1:-1]
        )
        assert all(
            track["layer"][0]["encoding"]["x"]["type"] == "quantitative"
            for track in spec["vconcat"][1:-1]
        )


@pytest.mark.docs
@pytest.mark.parametrize(
    "name", ["pbmc_marker_matrix", "pbmc_cell_heatmap", "pbmc_expression_tracks"]
)
def test_pbmc_tree_shares_the_plotted_group_or_cell_axis(name: str) -> None:
    spec = import_module(f"docs.examples.{name}").chart._prepare_render().spec
    if name == "pbmc_expression_tracks":
        tree = spec["vconcat"][0]
        assert spec["resolve"]["scale"]["x"] == "shared"
        assert tree["encoding"]["x"]["field"] == "cell"
        assert tree["encoding"]["x"]["type"] == "quantitative"
        assert tree["height"] == 65
    else:
        column = spec["hconcat"][-1]
        tree = column["vconcat"][-1] if name == "pbmc_marker_matrix" else column
        assert spec["resolve"]["scale"]["y"] == "shared"
        assert tree["encoding"]["y"]["field"] == (
            "row" if name == "pbmc_marker_matrix" else "cell"
        )
        assert tree["encoding"]["y"]["type"] == "quantitative"
        if name == "pbmc_marker_matrix":
            scale = tree["encoding"]["y"]["scale"]
            assert scale.get("type", "linear") == "linear"
            assert scale["domain"] == [-0.5, 7.5]
            assert scale["nice"] is False and scale["zero"] is False
        else:
            assert spec["scales"]["y"]["type"] == "linear"
            assert spec["scales"]["y"]["domain"] == [0, 2638]
    assert tree["mark"]["type"] == "rule"
    assert tree["mark"]["tooltip"] is None


@pytest.mark.docs
def test_pbmc_matrix_annotations_cover_each_marker_and_align_row_intervals() -> None:
    data = load_dataset("pbmc_markers", as_format="json")
    genes = [marker["gene"] for marker in data["markers"]]
    covered = []
    for group in data["marker_groups"]:
        span = genes[
            genes.index(group["start_gene"]) : genes.index(group["end_gene"]) + 1
        ]
        covered.extend(span)
        assert group["end"] - group["start"] == len(span)
        assert group["center"] == (group["start"] + group["end"]) / 2
        assert all(
            marker["cell_type"] == group["cell_type"]
            for marker in data["markers"]
            if marker["gene"] in span
        )
    assert covered == genes
    assert data["marker_domain"] == [0, 12]
    assert len(data["marker_groups"]) == 8
    assert data["group_domain"] == [-0.5, 7.5]
    assert all(
        row["row_start"] == row["group_order"] - 0.5
        and row["row_end"] == row["group_order"] + 0.5
        for row in data["groups"] + data["means"]
    )
    spec = (
        import_module("docs.examples.pbmc_marker_matrix").chart._prepare_render().spec
    )
    header, matrix = spec["hconcat"][2]["vconcat"]
    assert header["resolve"]["scale"]["y"] == "excluded"
    assert header["layer"][1]["encoding"]["text"]["field"] == "cell_type"
    assert matrix["encoding"]["y"]["field"] == "row_start"
    assert matrix["encoding"]["y2"]["field"] == "row_end"
