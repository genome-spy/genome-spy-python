"""Exercise the notebook's actual snapshot-to-observation mapping."""

import ast
import json
from pathlib import Path
from types import SimpleNamespace

import numpy as np
import pandas as pd
import pytest

NOTEBOOK = Path(__file__).parents[1] / "notebooks/scanpy_linked_brushing.ipynb"


def selection_namespace(adata):
    notebook = json.loads(NOTEBOOK.read_text())
    source = "\n".join(
        "".join(cell["source"])
        for cell in notebook["cells"]
        if cell["cell_type"] == "code"
    )
    callback = next(
        node
        for node in ast.parse(source).body
        if isinstance(node, ast.FunctionDef) and node.name == "show_selection"
    )
    namespace = {
        "np": np,
        "adata": adata,
        "plotted_coordinates": adata.obsm["X_umap"][:, :2].copy(),
        "plotted_ids": adata.obs["cell_id"].astype(str).to_numpy(copy=True),
        "status": SimpleNamespace(value=""),
        "table": SimpleNamespace(value=""),
    }
    exec(
        compile(ast.Module(body=[callback], type_ignores=[]), str(NOTEBOOK), "exec"),
        namespace,
    )
    return namespace


def test_membership_uses_snapshot_ids_half_open_bounds_and_distinct_duplicates():
    ad = pytest.importorskip("anndata")
    adata = ad.AnnData(
        obs=pd.DataFrame(
            {"cell_id": ["a", "b", "c", "d", "e", "f"]}, index=list("abcdef")
        ),
        obsm={"X_umap": np.array([[0, 0], [0, 0], [1, 1], [2, 1], [1, 2], [-1, 1]])},
    )
    namespace = selection_namespace(adata)
    # The already-rendered snapshot must survive later coordinate/order edits.
    adata.obsm["X_umap"][:] = 99
    namespace["adata"] = adata[[5, 2, 1, 0, 3, 4]].copy()
    namespace["show_selection"]({"intervals": {"x": [0, 2], "y": [0, 2]}})
    assert namespace["selected_ids"] == ["a", "b", "c"]
    assert namespace["selected_obs"]["cell_id"].tolist() == ["c", "b", "a"]
    assert "3 cells selected" in namespace["status"].value
    pd.testing.assert_frame_equal(
        namespace["selected_obs"], namespace["adata"].obs.iloc[1:4]
    )


@pytest.mark.parametrize(
    "intervals",
    [{"x": None, "y": None}, {"x": [0, 2], "y": None}, {"x": [1, 1], "y": [0, 2]}],
)
def test_cleared_partial_and_zero_area_brushes_select_no_cells(intervals):
    ad = pytest.importorskip("anndata")
    adata = ad.AnnData(
        obs=pd.DataFrame({"cell_id": ["a"]}, index=["a"]),
        obsm={"X_umap": np.array([[1, 1]])},
    )
    namespace = selection_namespace(adata)
    namespace["show_selection"]({"intervals": {"x": [0, 2], "y": [0, 2]}})
    assert namespace["selected_ids"] == ["a"]
    namespace["show_selection"]({"intervals": intervals})
    assert namespace["selected_ids"] == []
    assert namespace["selected_obs"].empty
    assert "0 cells selected" in namespace["status"].value
    assert namespace["table"].value == ""
