"""Observation membership independent of browser rendering or expression data."""

import numpy as np
import pandas as pd
import pytest

import genome_spy.scanpy as gsc

ad = pytest.importorskip("anndata")


@pytest.fixture
def adata():
    return ad.AnnData(
        obs=pd.DataFrame(index=list("abcdef")),
        obsm={"X_umap": np.array([[0, 0], [0, 0], [1, 1], [2, 1], [1, 2], [-1, 1]])},
    )


def snapshot(x=(0, 2), y=(0, 2)):
    return {"type": "interval", "intervals": {"x": x, "y": y}}


def test_membership_uses_half_open_bounds_and_distinct_coincident_rows(adata):
    assert adata.obs_names[gsc.selection_mask(adata, snapshot())].tolist() == list(
        "abc"
    )
    reordered = adata[[5, 2, 1, 0, 3, 4]]
    assert reordered.obs_names[
        gsc.selection_mask(reordered, snapshot())
    ].tolist() == list("cba")
    assert adata.X is None  # Membership never needs an expression matrix.


@pytest.mark.parametrize(
    "value", [None, snapshot(None, None), snapshot((0, 2), None), snapshot((1, 1))]
)
def test_cleared_partial_and_zero_area_brushes_select_no_cells(adata, value):
    assert not gsc.selection_mask(adata, value).any()


def test_uses_requested_dimensions_and_umap_key_precedence(adata):
    adata.obsm["umap"] = np.column_stack([np.full(6, 99), np.zeros(6), np.arange(6)])
    assert not gsc.selection_mask(adata, snapshot()).any()
    mask = gsc.selection_mask(adata, snapshot((0, 1), (1, 3)), dimensions=(1, 2))
    assert adata.obs_names[mask].tolist() == ["b", "c"]


def test_backed_metadata_selection_does_not_read_expression(
    adata, tmp_path, monkeypatch
):
    path = tmp_path / "cells.h5ad"
    adata.write_h5ad(path)
    backed = ad.read_h5ad(path, backed="r")
    try:
        monkeypatch.setattr(
            ad.AnnData,
            "X",
            property(lambda _: pytest.fail("Expression was accessed")),
        )
        assert backed.obs_names[
            gsc.selection_mask(backed, snapshot())
        ].tolist() == list("abc")
    finally:
        backed.file.close()


@pytest.mark.parametrize(
    "value",
    [
        snapshot((2, 0)),
        snapshot((0, float("nan"))),
        snapshot((True, 2)),
        snapshot("bad"),
        {"type": "point"},
    ],
)
def test_invalid_snapshots_fail_clearly(adata, value):
    with pytest.raises(ValueError, match="selection_mask:"):
        gsc.selection_mask(adata, value)


@pytest.mark.parametrize("dimensions", [(0,), (0, 2), (-1, 1), (True, 1)])
def test_invalid_dimensions_fail_clearly(adata, dimensions):
    with pytest.raises(ValueError, match="component pair"):
        gsc.selection_mask(adata, snapshot(), dimensions=dimensions)


def test_invalid_coordinates_and_input_types_fail_clearly(adata):
    with pytest.raises(TypeError, match="expected AnnData"):
        gsc.selection_mask(None, snapshot())
    with pytest.raises(TypeError, match="snapshot"):
        gsc.selection_mask(adata, [])
    del adata.obsm["X_umap"]
    with pytest.raises(ValueError, match="missing"):
        gsc.selection_mask(adata, snapshot())
    adata.obsm["X_umap"] = np.full((6, 2), np.inf)
    with pytest.raises(ValueError, match="finite"):
        gsc.selection_mask(adata, snapshot())
