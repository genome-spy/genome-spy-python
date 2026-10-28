"""Stored graph edges retain Scanpy ordering, source cells and native point layers."""

from copy import deepcopy

import numpy as np
import pytest
from scipy import sparse

import genome_spy.integrations.scanpy as gsc
from tests.integrations.scanpy.embedding_fixture import make_embedding_adata
from tests.integrations.scanpy.fixture_support import FAMILIES, graph_adata
from tests.integrations.scanpy.helpers import leaf_marks, points, units

sc = pytest.importorskip("scanpy")


@pytest.mark.reference
@pytest.mark.parametrize(
    "storage", ["csr", "csc", "csr_array", "csc_array", "dense", "legacy_lil"]
)
@pytest.mark.parametrize("key", ["neighbors", "saved"])
def test_graph_geometry_order_and_style_match_public_scanpy(storage, key):
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib.collections import LineCollection

    data = graph_adata(storage, key)
    data.obsm["X_umap"] = data.obsm["X_umap"][:, :2].copy()
    options = dict(
        color=["cell_type", "score"],
        edges=True,
        edges_width=0.7,
        edges_color="navy",
        neighbors_key=key,
        obs_id="cell_id",
        zoom=True,
        show=False,
    )
    reference_options = {
        k: v for k, v in options.items() if k not in {"obs_id", "zoom"}
    }
    # AnnData.copy() migrates legacy graphs to obsp, which rejects LIL storage.
    axes = sc.pl.umap(deepcopy(data), **reference_options)
    references = [
        next(c for c in ax.collections if isinstance(c, LineCollection)) for ax in axes
    ]
    spec = gsc.pl.umap(data, **options).to_dict()
    assert len(spec["datasets"]) == 2
    cell_rows = next(rows for rows in spec["datasets"].values() if "_obs_id" in rows[0])
    cells = {row["_obs_id"]: row for row in cell_rows}
    for panel, ax, reference in zip(units(spec), axes, references, strict=True):
        edge = leaf_marks(panel)[0]
        assert edge["mark"] == {
            "type": "rule",
            "color": "navy",
            "size": pytest.approx(0.7 * 100 / 72),
            "clip": True,
            "tooltip": None,
        }
        rows = spec["datasets"][edge["data"]["name"]]
        segments = [
            [
                [cells[row[end]][axis] for axis in ["_coord_0", "_coord_1"]]
                for end in ["_source", "_target"]
            ]
            for row in rows
        ]
        np.testing.assert_array_equal(segments, reference.get_segments())
        assert len(edge["transform"]) == 2
        assert all(
            t["from"]["name"] == points(panel)["data"]["name"]
            for t in edge["transform"]
        )
        assert reference.get_zorder() == -2
        for axis, expected in [("x", ax.get_xlim()), ("y", ax.get_ylim())]:
            np.testing.assert_allclose(
                points(panel)["encoding"][axis]["scale"]["domain"], expected
            )
    plt.close(axes[0].figure)


@pytest.mark.parametrize("family", FAMILIES)
@pytest.mark.parametrize("outline", [False, True])
def test_shared_embeddings_reuse_points_and_read_graph_without_analysis(
    family, outline, monkeypatch
):
    data = graph_adata()
    original = deepcopy(data)
    for module, name in [
        (sc.pp, "neighbors"),
        (sc.tl, "umap"),
        (sc.tl, "pca"),
        (sc.tl, "diffmap"),
        (sc.tl, "tsne"),
        (sc.pl, "embedding"),
    ]:
        monkeypatch.setattr(
            module, name, lambda *a, **k: pytest.fail("Ran analysis or Scanpy plotting")
        )
    args = (data, "umap") if family == "embedding" else (data,)
    options = dict(
        color=["cell_type", "score"],
        dimensions=(0, 1),
        marker=["s", "D"],
        add_outline=outline,
        size=20,
        show=False,
    )
    plain = getattr(gsc.pl, family)(*args, **options).to_dict()
    chart = getattr(gsc.pl, family)(*args, edges=True, **options)
    spec = chart.to_dict()
    for panel, normal in zip(units(spec), units(plain), strict=True):
        assert leaf_marks(panel)[0]["mark"]["type"] == "rule"
        assert [m["mark"] for m in leaf_marks(panel)[1:]] == [
            m["mark"] for m in leaf_marks(normal)
        ]
    assert all(
        mark["encoding"]["shape"] == {"value": "diamond"}
        for mark in leaf_marks(units(spec)[1])[1:]
    )
    assert all(rows in spec["datasets"].values() for rows in plain["datasets"].values())
    np.testing.assert_array_equal(
        data.obsp["connectivities"].data, original.obsp["connectivities"].data
    )
    np.testing.assert_array_equal(data.obsm["X_umap"], original.obsm["X_umap"])
    assert data.uns["neighbors"] == original.uns["neighbors"]
    chart.to_html(inline=True, controls=False)


def test_legacy_storage_and_current_storage_precedence():
    data = graph_adata()
    expected = gsc.pl.umap(data, edges=True, show=False).to_dict()
    matrix = data.obsp.pop("connectivities")
    data.uns["neighbors"]["connectivities"] = matrix
    assert gsc.pl.umap(data, edges=True, show=False).to_dict() == expected
    data.obsp["connectivities"] = matrix
    data.uns["neighbors"]["connectivities"] = sparse.eye(8)
    data.uns["neighbors"]["connectivities_key"] = "ignored_for_default_neighbors"
    assert gsc.pl.umap(data, edges=True, show=False).to_dict() == expected


def test_disabled_edges_do_not_read_graph_or_change_chart():
    data = make_embedding_adata()
    plain = gsc.pl.umap(data, show=False).to_dict()
    assert (
        gsc.pl.umap(
            data,
            edges=False,
            neighbors_key="missing",
            edges_width=2,
            edges_color="navy",
            show=False,
        ).to_dict()
        == plain
    )


@pytest.mark.parametrize(
    "options,error,message",
    [
        ({"neighbors_key": "missing"}, ValueError, "neighbors metadata"),
        ({"edges_width": -1}, ValueError, "edges_width"),
        ({"edges_width": np.inf}, ValueError, "edges_width"),
        ({"edges_color": ["red", "blue"]}, NotImplementedError, "edges_color"),
        ({"edges_color": "C0"}, NotImplementedError, "edges_color"),
        ({"dimensions": (1, 2)}, NotImplementedError, "first two"),
    ],
)
def test_invalid_or_unsupported_edge_options_fail_clearly(options, error, message):
    with pytest.raises(error, match=message):
        gsc.pl.umap(graph_adata(), edges=True, show=False, **options)


@pytest.mark.parametrize("problem", ["missing", "nonfinite", "shape", "loops"])
def test_invalid_graphs_do_not_silently_disappear(problem):
    data = graph_adata()
    matrix = data.obsp.pop("connectivities")
    if problem == "nonfinite":
        matrix.data[0] = np.nan
    elif problem == "shape":
        matrix = sparse.csr_matrix((4, 4))
    elif problem == "loops":
        matrix = sparse.eye(8)
    if problem != "missing":
        data.uns["neighbors"]["connectivities"] = matrix
    error = NotImplementedError if problem == "loops" else ValueError
    with pytest.raises(error, match="self-loop|connectivities"):
        gsc.pl.umap(data, edges=True, show=False)


def test_empty_graph_retains_points_without_an_edge_layer_failure():
    data = graph_adata()
    data.obsp["connectivities"] = sparse.csr_matrix((8, 8))
    spec = gsc.pl.umap(data, edges=True, show=False).to_dict()
    assert spec == gsc.pl.umap(data, show=False).to_dict()


def test_nonfinite_legacy_lil_graph_is_rejected():
    data = graph_adata("legacy_lil")
    data.uns["neighbors"]["connectivities"][0, 1] = np.nan
    with pytest.raises(ValueError, match="finite real square matrix"):
        gsc.pl.umap(data, edges=True, show=False)


def test_views_and_backed_graphs_keep_cell_identity_without_densifying(
    tmp_path, monkeypatch
):
    import anndata as ad

    data = graph_adata()
    path = tmp_path / "graph.h5ad"
    data.write_h5ad(path)
    backed = ad.read_h5ad(path, backed="r")
    monkeypatch.setattr(
        sparse.csr_matrix, "toarray", lambda *a, **k: pytest.fail("Densified a matrix")
    )
    try:
        for candidate in [data[[7, 3, 0, 2, 1]], backed]:
            spec = gsc.pl.umap(
                candidate, color="score", obs_id="cell_id", edges=True, show=False
            ).to_dict()
            cells = next(
                rows
                for rows in spec["datasets"].values()
                if rows and "_obs_id" in rows[0]
            )
            assert [r["_obs_id"] for r in cells] == candidate.obs.cell_id.tolist()
            endpoints = next(
                rows
                for rows in spec["datasets"].values()
                if rows and "_source" in rows[0]
            )
            assert {r[end] for r in endpoints for end in ["_source", "_target"]} <= set(
                candidate.obs.cell_id
            )
    finally:
        backed.file.close()
