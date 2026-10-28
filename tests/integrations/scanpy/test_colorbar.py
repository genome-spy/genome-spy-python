"""Continuous guide placement through the shared native embedding pipeline."""

from copy import deepcopy

import pytest

import genome_spy as gs
import genome_spy.integrations.scanpy as gsc
from tests.integrations.scanpy.embedding_fixtures import make_embedding_adata
from tests.integrations.scanpy.helpers import points, units

pytest.importorskip("scanpy")


@pytest.mark.parametrize(
    "family,options,location",
    [("umap", {}, location) for location in (None, "right", "left", "top", "bottom")]
    + [
        (family, options, "left")
        for family, options in [
            ("embedding", {"basis": "custom"}),
            ("tsne", {}),
            ("diffmap", {}),
            ("draw_graph", {}),
            ("pca", {}),
            ("pca_scatter", {}),
        ]
    ],
)
def test_embedding_colorbar_locations_preserve_records_and_categorical_guides(
    family, options, location
):
    adata = make_embedding_adata()
    options = dict(
        options, color=["cell_type", "score"], width=420, height=180, show=False
    )
    call = getattr(gsc.pl, family)
    original = call(adata, **options).to_dict()
    spec = call(adata, colorbar_loc=location, **options).to_dict()
    assert spec["datasets"] == original["datasets"]
    legend = spec["config"]["legend"]
    horizontal = location in ("top", "bottom")
    assert legend["orient"] == (location or "right")
    assert legend["direction"] == ("horizontal" if horizontal else "vertical")
    assert legend["gradientLength"] == (420 if horizontal else 180)
    assert legend["gradientThickness"] == legend["gradientLength"] / 30
    categorical, continuous = [points(panel)["encoding"] for panel in units(spec)]
    expected = deepcopy(points(units(original)[0])["encoding"])
    if location not in (None, "right"):
        expected["color"]["legend"].update(orient="right", direction="vertical")
    assert categorical == expected
    expected = deepcopy(points(units(original)[1])["encoding"])
    if location is None:
        expected["color"]["legend"] = None
    assert continuous == expected


@pytest.mark.parametrize("linked", [False, True])
def test_native_configuration_and_collection_override_numeric_guide_defaults(linked):
    options = (
        {"selection": gs.selection_interval("cells", encodings=["x", "y"])}
        if linked
        else {}
    )
    chart = gsc.pl.umap(
        make_embedding_adata(),
        color=["score", "g1"],
        colorbar_loc="top",
        show=False,
        **options,
    )
    original = chart.to_dict()
    spec = (
        chart.resolve_legend(default="collected")
        .configure_legend(
            orient="left", direction="vertical", gradientLength=140, gradientThickness=8
        )
        .to_dict()
    )
    assert spec["resolve"]["legend"] == {"default": "collected"}
    assert spec["config"]["legend"]["orient"] == "left"
    assert spec["config"]["legend"]["direction"] == "vertical"
    assert spec["config"]["legend"]["gradientLength"] == 140
    assert spec["datasets"] == original["datasets"]
    assert units(spec) == units(original)


@pytest.mark.parametrize("location", ["none", "center", "RIGHT"])
def test_unsupported_colorbar_locations_fail_before_reading_data(location):
    with pytest.raises(NotImplementedError, match="colorbar_loc"):
        gsc.pl.umap(None, colorbar_loc=location, show=False)
