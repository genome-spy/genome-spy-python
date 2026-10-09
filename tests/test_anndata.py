from __future__ import annotations

from collections.abc import Callable
from io import BytesIO
from pathlib import Path
from typing import Any

import anndata as ad
import numpy as np
import pandas as pd
import pyarrow as pa
import pytest
from scipy import sparse

import genome_spy as gs
from genome_spy import arrow
from genome_spy.anndata import AnnDataProjectionError, from_anndata


@pytest.fixture
def adata() -> ad.AnnData:
    return ad.AnnData(
        np.array([[0, 2, 8], [3, 0, 9], [1, 4, 7]], dtype=np.float32),
        obs=pd.DataFrame(
            {
                "cell_type": pd.Categorical(
                    ["B", "A", None], categories=["B", "A"], ordered=True
                ),
                "counts": pd.array([2, None, 5], dtype="Int64"),
                "obs_id": ["authored-1", "authored-2", "authored-3"],
            },
            index=["c1", "c2", "c3"],
        ),
        var=pd.DataFrame(index=["G1", "G2", "unused"]),
        obsm={"X_umap": np.array([[1, 2], [3, 4], [5, 6]], dtype=np.float32)},
    )


def _rows(chart: gs.Chart) -> list[dict[str, object]]:
    spec = chart.to_dict()
    return spec["datasets"][spec["data"]["name"]]


@pytest.mark.parametrize("view", [False, True])
def test_direct_input_uses_metadata_in_json_and_arrow(
    adata: ad.AnnData, view: bool
) -> None:
    source = adata[[2, 0], :] if view else adata
    chart = gs.Chart(source).mark_point().encode(x="counts", color="cell_type")
    expected = _rows(gs.Chart(source.obs.copy()).mark_point())

    assert _rows(chart) == expected
    assert chart.to_dict()["encoding"] == {
        "x": {"field": "counts", "type": "quantitative"},
        "color": {"field": "cell_type", "type": "nominal"},
    }
    prepared = chart._prepare_render()
    assert len(prepared.buffers) == 1
    decoded = pa.ipc.open_file(BytesIO(next(iter(prepared.buffers.values()))))
    assert decoded.read_all().to_pylist() == expected
    assert set(expected[0]) == {"counts", "cell_type", "obs_id"}


def test_direct_input_supports_anndata_subclasses(adata: ad.AnnData) -> None:
    class CustomAnnData(ad.AnnData):
        pass

    source = CustomAnnData(obs=adata.obs.copy())
    assert _rows(gs.Chart(source).mark_point()) == _rows(
        gs.Chart(adata.obs).mark_point()
    )


def test_direct_input_falls_back_to_records_without_arrow(
    adata: ad.AnnData, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setattr(arrow, "_load_pyarrow", lambda: None)
    chart = gs.Chart(adata).mark_point()
    prepared = chart._prepare_render()
    assert prepared.buffers == {}
    assert prepared.spec == chart.to_dict()
    with pytest.raises(TypeError, match="requires PyArrow"):
        gs.to_arrow_ipc(adata)


def test_metadata_never_reads_expression_or_embeddings(
    adata: ad.AnnData, monkeypatch: pytest.MonkeyPatch
) -> None:
    def forbidden_access(self: ad.AnnData) -> None:
        pytest.fail("Metadata input read a matrix")

    monkeypatch.setattr(ad.AnnData, "X", property(forbidden_access))
    monkeypatch.setattr(ad.AnnData, "obsm", property(forbidden_access))
    chart = gs.Chart(adata).mark_point().encode(x="counts")
    assert len(_rows(chart)) == 3
    assert chart._prepare_render().buffers
    pd.testing.assert_frame_equal(from_anndata(adata), adata.obs)


@pytest.mark.parametrize(
    "matrix_type",
    [
        np.asarray,
        sparse.csr_matrix,
        sparse.csc_matrix,
        sparse.csr_array,
        sparse.csc_array,
    ],
)
@pytest.mark.parametrize("view", [False, True])
def test_projection_preserves_values_order_and_source(
    adata: ad.AnnData, matrix_type: Callable[[Any], Any], view: bool
) -> None:
    adata.X = matrix_type(adata.X)
    original_obs = adata.obs.copy()
    original_X = adata.X.copy()
    original_embedding = adata.obsm["X_umap"].copy()
    # Duplicate identifiers must not trigger a join or reorder rows.
    adata.obs_names = ["duplicate", "duplicate", "other"]
    source = adata[[2, 0], :] if view else adata
    cells = from_anndata(
        source, obs=["cell_type"], genes=["G2"], obsm_keys=[("X_umap", 1)]
    )

    positions = [2, 0] if view else [0, 1, 2]
    # AnnData itself removes unused categories when constructing a view.
    expected = source.obs[["cell_type"]].copy()
    expected["G2"] = np.array([2, 0, 4], dtype=np.float32)[positions]
    expected["X_umap-1"] = np.array([2, 4, 6], dtype=np.float32)[positions]
    pd.testing.assert_frame_equal(cells, expected)
    assert source.is_view is view
    pd.testing.assert_frame_equal(
        adata.obs.reset_index(drop=True), original_obs.reset_index(drop=True)
    )
    np.testing.assert_array_equal(adata.obsm["X_umap"], original_embedding)
    actual = adata.X.toarray() if sparse.issparse(adata.X) else adata.X
    before = original_X.toarray() if sparse.issparse(original_X) else original_X
    np.testing.assert_array_equal(actual, before)
    cells.iloc[0, 1] = -100
    np.testing.assert_array_equal(actual, before)


def test_sparse_conversion_only_densifies_selected_columns(
    adata: ad.AnnData, monkeypatch: pytest.MonkeyPatch
) -> None:
    adata.X = sparse.csr_matrix(adata.X)
    original = sparse.csr_matrix.toarray
    shapes = []

    def checked_toarray(
        self: sparse.csr_matrix, *args: object, **kwargs: object
    ) -> np.ndarray:
        shapes.append(self.shape)
        assert self.shape == (3, 1), "Whole expression matrix was densified"
        return original(self, *args, **kwargs)

    monkeypatch.setattr(sparse.csr_matrix, "toarray", checked_toarray)
    cells = from_anndata(adata, obs=[], genes=["G2"])
    assert cells["G2"].tolist() == [2, 0, 4]
    assert shapes == [(3, 1)]


@pytest.mark.parametrize(
    "embedding_type", [pd.DataFrame, sparse.csr_matrix, sparse.csr_array]
)
def test_projection_supports_pandas_and_sparse_embeddings(
    adata: ad.AnnData, embedding_type: Callable[[Any], Any]
) -> None:
    values = adata.obsm["X_umap"]
    adata.obsm["X_umap"] = (
        pd.DataFrame(values, index=adata.obs_names)
        if embedding_type is pd.DataFrame
        else embedding_type(values)
    )
    cells = from_anndata(adata[[2, 0], :], obs=[], obsm_keys=[("X_umap", 0)])
    assert cells["X_umap-0"].tolist() == [5, 1]


@pytest.mark.parametrize(
    ("kwargs", "message"),
    [
        ({"obs": ["missing"]}, "Observation column 'missing'"),
        ({"genes": ["missing"]}, "Gene 'missing'"),
        ({"obs": ["counts", "counts"]}, "collide"),
        ({"genes": ["counts"]}, "collide"),
        ({"genes": ["G2", "G2"]}, "collide"),
        ({"obsm_keys": [("missing", 0)]}, "Embedding 'missing'"),
        ({"obsm_keys": [("X_umap", -1)]}, "Invalid component"),
        ({"obsm_keys": [("X_umap", 2)]}, "Invalid component"),
        ({"obsm_keys": [("X_umap", True)]}, "Invalid component"),
        ({"obsm_keys": [("X_umap", 0), ("X_umap", 0)]}, "collide"),
        ({"obs": "counts"}, "sequences"),
        ({"genes": "G2"}, "sequences"),
    ],
)
def test_projection_errors_are_contextual(
    adata: ad.AnnData, kwargs: dict[str, object], message: str
) -> None:
    with pytest.raises(AnnDataProjectionError, match=message):
        from_anndata(adata, **kwargs)


def test_projection_rejects_ambiguous_gene_names(adata: ad.AnnData) -> None:
    adata.var_names = ["G2", "G2", "unused"]
    with pytest.raises(AnnDataProjectionError, match="Gene 'G2'.*ambiguous"):
        from_anndata(adata, genes=["G2"])


def test_projection_ignores_unselected_duplicate_genes(adata: ad.AnnData) -> None:
    adata.var_names = ["duplicate", "G2", "duplicate"]
    assert from_anndata(adata, genes=["G2"])["G2"].tolist() == [2, 0, 4]


def test_backed_metadata_works_without_loading_expression(
    adata: ad.AnnData, tmp_path: Path
) -> None:
    path = tmp_path / "cells.h5ad"
    adata.write_h5ad(path)
    backed = ad.read_h5ad(path, backed="r")
    try:
        assert _rows(gs.Chart(backed).mark_point()) == _rows(
            gs.Chart(adata).mark_point()
        )
        assert backed.isbacked
        with pytest.raises(TypeError, match="NumPy or SciPy"):
            from_anndata(backed, genes=["G2"])
    finally:
        backed.file.close()


def test_empty_projection_and_wrong_source() -> None:
    adata = ad.AnnData(
        obs=pd.DataFrame(
            {"x": pd.Series(dtype="float64")}, index=pd.Index([], dtype=str)
        )
    )
    assert _rows(gs.Chart(adata).mark_point().encode(x="x")) == []
    cells = from_anndata(adata, obs=["x"])
    assert cells.empty and list(cells.columns) == ["x"]
    with pytest.raises(TypeError, match="Expected AnnData"):
        from_anndata(pd.DataFrame())


def test_projection_is_a_snapshot_and_direct_input_reads_current_metadata(
    adata: ad.AnnData,
) -> None:
    adata.obs = adata.obs.drop(columns="obs_id")
    cells = from_anndata(adata, genes=["G2"], obsm_keys=[("X_umap", 0)])
    chart = gs.Chart(adata).mark_point()
    adata.obs.loc["c1", "counts"] = 100
    adata.X[0, 1] = 100
    adata.obsm["X_umap"][0, 0] = 100
    assert cells.loc["c1", ["counts", "G2", "X_umap-0"]].tolist() == [2, 2, 1]
    assert _rows(chart)[0] == {"counts": 100, "cell_type": "B"}


def test_projection_rejects_selected_backed_embedding(
    adata: ad.AnnData, tmp_path: Path
) -> None:
    import h5py

    with h5py.File(tmp_path / "embedding.h5", "w") as file:
        embedding = file.create_dataset("embedding", data=np.zeros((3, 2)))
        adata.obsm["backed"] = embedding
        with pytest.raises(TypeError, match="Embedding 'backed'.*NumPy"):
            from_anndata(adata, obsm_keys=[("backed", 0)])


def test_composition_and_widget_updates_reuse_existing_tables(
    adata: ad.AnnData,
) -> None:
    cells = from_anndata(
        adata, obs=["cell_type"], genes=["G2"], obsm_keys=[("X_umap", 0)]
    )
    chart = gs.Chart(cells).mark_point().encode(x="X_umap-0", color="G2")
    spec = (chart | chart).to_dict()
    assert len(spec["datasets"]) == 1
    assert spec["hconcat"][0]["data"] == spec["hconcat"][1]["data"]
    widget = gs.Chart(adata).mark_point().encode(x="counts").widget()
    widget.set_data(adata)
    entry = widget.dataset_manifest[0]
    payload = getattr(widget, entry["payload_trait"])
    assert pa.ipc.open_file(BytesIO(payload)).read_all().to_pylist() == _rows(
        gs.Chart(adata).mark_point()
    )
    widget.set_data(cells, format="records")
    assert getattr(widget, entry["payload_trait"]) == _rows(chart)
