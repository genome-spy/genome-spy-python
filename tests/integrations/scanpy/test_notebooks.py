"""Run the supported official-tutorial examples on Scanpy's packaged PBMC data."""

import json
from pathlib import Path

import numpy as np
import pytest

import genome_spy.scanpy as gsc
from genome_spy.chart import TopLevelSpec

sc = pytest.importorskip("scanpy")
NOTEBOOKS = Path(__file__).resolve().parents[3] / "integrations/scanpy/notebooks"


@pytest.mark.parametrize(
    "name", ["scanpy_umap", "scanpy_umap_customization", "scanpy_linked_brushing"]
)
def test_tutorial_notebooks_use_packaged_data_and_preserve_embedding(name, monkeypatch):
    charts = []
    monkeypatch.setattr(
        TopLevelSpec, "display", lambda chart, **kwargs: charts.append(chart)
    )
    original = sc.datasets.pbmc68k_reduced()
    namespace = {}
    notebook = json.loads((NOTEBOOKS / f"{name}.ipynb").read_text())
    try:
        for cell in notebook["cells"]:
            if cell["cell_type"] == "code":
                exec(compile("".join(cell["source"]), name, "exec"), namespace)
        pbmc = namespace["pbmc"]
        assert pbmc.shape == original.shape == (700, 765)
        assert pbmc.obs_names.equals(original.obs_names)
        np.testing.assert_array_equal(pbmc.obsm["X_umap"], original.obsm["X_umap"])
        for chart in charts:
            spec = chart.to_dict()
            assert spec[
                "datasets"
            ]  # Exercise complete spec validation, not just construction.
        if name == "scanpy_linked_brushing":
            view, brush = namespace["view"], namespace["brush"]
            assert view.parameter_names == [brush.name]
            assert brush.param.to_dict()["select"] == {
                "type": "interval",
                "encodings": ["x", "y"],
                "on": "mousedown",
                "zoom": False,
            }
            xy = original.obsm["X_umap"]
            lower, upper = np.quantile(xy, [0.25, 0.75], axis=0)
            view.parameter_values = {
                brush.name: {
                    "type": "interval",
                    "intervals": {
                        "x": [lower[0], upper[0]],
                        "y": [lower[1], upper[1]],
                    },
                }
            }
            retrieval = next(
                c
                for c in notebook["cells"]
                if "mask = gsc.selection_mask" in "".join(c["source"])
            )
            exec("".join(retrieval["source"]), namespace)
            expected = (
                (xy[:, 0] >= lower[0])
                & (xy[:, 0] < upper[0])
                & (xy[:, 1] >= lower[1])
                & (xy[:, 1] < upper[1])
            )
            assert 0 < expected.sum() < pbmc.n_obs
            assert namespace["selected_adata"].obs_names.equals(
                pbmc.obs_names[expected]
            )
            assert namespace["selected_ids"].equals(pbmc.obs_names[expected])
            assert (
                gsc.selection_mask(pbmc, view.parameter_values[brush.name]).tolist()
                == expected.tolist()
            )
    finally:
        if "view" in namespace:
            namespace["view"].close()
