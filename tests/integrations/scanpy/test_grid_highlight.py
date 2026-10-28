"""Optional grid feedback preserves data and validates before preparation."""

from importlib import import_module
import warnings

import numpy as np
import pytest

import genome_spy.integrations.scanpy as gsc
from tests.integrations.scanpy.heatmap_fixture import make_heatmap_adata
from tests.integrations.scanpy.clustermap_fixture import make_cluster_adata

pytest.importorskip("scanpy")

FAMILIES = ["dotplot", "matrixplot", "heatmap", "matrix", "clustermap"]


def make_chart(family, **options):
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", UserWarning)
        common = dict(width=320, height=260, **options)
        if family == "matrix":
            return gsc.pl.matrix(np.arange(1, 13).reshape(4, 3), show=False, **common)
        if family == "clustermap":
            return gsc.pl.clustermap(make_cluster_adata(), show=False, **common)
        if family in ("DotPlot", "MatrixPlot"):
            return getattr(gsc.pl, family)(
                make_heatmap_adata(), ["g1", "g2", "g1"], "group", **common
            ).to_chart()
        return getattr(gsc.pl, family)(
            make_heatmap_adata(), ["g1", "g2", "g1"], "group", show=False, **common
        )


def parameters(spec):
    if isinstance(spec, dict):
        yield from spec.get("params", [])
        for value in spec.values():
            yield from parameters(value)
    elif isinstance(spec, list):
        for value in spec:
            yield from parameters(value)


@pytest.mark.parametrize("family", [*FAMILIES, "DotPlot", "MatrixPlot"])
def test_feedback_modes_preserve_values_and_are_disabled_by_default(family):
    baseline = make_chart(family).to_dict()
    assert not {p["name"] for p in parameters(baseline)} & {"grid_cursor", "grid_hover"}
    for mode, name in [(True, "grid_cursor"), ("outline", "grid_hover")]:
        spec = make_chart(family, highlight=mode, hover=False).to_dict()
        assert spec["datasets"] == baseline["datasets"]
        feedback = [
            p for p in parameters(spec) if p["name"] in ("grid_cursor", "grid_hover")
        ]
        assert len(feedback) == 1
        assert feedback[0]["name"] == name
        if mode == "outline":
            assert feedback[0]["select"] == {
                "type": "point",
                "on": "mousemove",
                "clear": "mouseleave",
                "toggle": False,
            }
            assert feedback[0]["persist"] is False


@pytest.mark.parametrize("family", [*FAMILIES, "DotPlot", "MatrixPlot"])
@pytest.mark.parametrize("value", [None, 1, "ruler", []])
def test_invalid_feedback_fails_before_optional_dependencies(
    monkeypatch, family, value
):
    def forbidden(*args, **kwargs):
        pytest.fail("Invalid highlight must fail before optional imports or data reads")

    for name in ["pl", "_expression.dotplot_builder", "_expression.matrixplot_builder"]:
        monkeypatch.setattr(
            import_module(f"genome_spy.integrations.scanpy.{name}"),
            "_require_scanpy",
            forbidden,
        )
    function = getattr(gsc.pl, family)
    args = (None,) if family in ("matrix", "clustermap") else (None, ["g1"], "group")
    with pytest.raises(TypeError, match="highlight"):
        function(*args, highlight=value)
