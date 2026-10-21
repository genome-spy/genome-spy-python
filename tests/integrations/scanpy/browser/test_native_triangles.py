"""Retain C14's native triangle comparison without approximating Scanpy markers."""

from io import BytesIO
import json
import re
import xml.etree.ElementTree as ET

import numpy as np
import pytest
from PIL import Image

import genome_spy as gs
from tests.integrations.scanpy.browser.test_umap import fixture, render


@pytest.fixture(
    params=[
        (marker, shape, linewidth)
        for marker, shape in [
            ("^", "triangle-up"),
            ("v", "triangle-down"),
            ("<", "triangle-left"),
            (">", "triangle-right"),
        ]
        for linewidth in (0, 2)
    ],
    ids=lambda case: f"{case[1]}-{case[2]}pt",
)
def triangle_geometry(page, tmp_path, request):
    """Measure native paths and paint against Scanpy; return both for the gap check."""
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    import scanpy as sc

    marker, shape, linewidth = request.param
    data = fixture()[:1].copy()
    data.obsm["X_umap"] = np.array([[0.0, 0.0]])
    with plt.rc_context({"figure.figsize": (3, 3), "figure.dpi": 100}):
        ax = sc.pl.umap(
            data,
            size=5184,
            marker=marker,
            na_color="black",
            edgecolor="black" if linewidth else "none",
            linewidth=linewidth,
            frameon=False,
            title="",
            show=False,
        )
        artist = ax.collections[0]
        expected = (
            artist.get_paths()[0].vertices[:-1]
            * np.sqrt(artist.get_sizes()[0])
            * [100 / 72, -100 / 72]
        )
        ax.figure.canvas.draw()
        output = BytesIO()
        ax.figure.savefig(
            output,
            dpi=150,
            bbox_inches=ax.get_window_extent().transformed(
                ax.figure.dpi_scale_trans.inverted()
            ),
            pad_inches=0,
        )
        reference = Image.open(output).convert("RGB")
        plt.close(ax.figure)
    chart = (
        gs.Chart([{"x": 0, "y": 0}])
        .mark_point(
            size=100**2,
            filled=True,
            color="black",
            stroke="black",
            strokeOpacity=1 if linewidth else 0,
            strokeWidth=linewidth * 100 / 72,
            inwardStroke=False,
        )
        .encode(
            shape=gs.value(shape),
            x=gs.X("x:Q").scale(domain=[-1, 1], nice=False).axis(None),
            y=gs.Y("y:Q").scale(domain=[-1, 1], nice=False).axis(None),
        )
        .properties(width=300, height=300)
        .configure_view(strokeWidth=0)
    )
    bounds = render(page, chart)
    page.wait_for_timeout(500)
    canvas = page.locator("canvas").first.bounding_box()
    actual = Image.open(
        BytesIO(
            page.screenshot(
                clip={
                    "x": canvas["x"] + bounds["x"],
                    "y": canvas["y"] + bounds["y"],
                    "width": bounds["width"],
                    "height": bounds["height"],
                }
            )
        )
    ).convert("RGB")
    svg = page.evaluate("async()=> (await api.imageExport.svg()).blob.text()")
    paths = [
        element for element in ET.fromstring(svg).iter() if element.tag.endswith("path")
    ]
    assert len(paths) == 1
    path = paths[0].get("d")
    assert re.fullmatch(r"M[-+\d., eE]+L[-+\d., eE]+L[-+\d., eE]+Z", path), path
    native = np.array(
        re.findall(r"[-+]?\d*\.?\d+(?:[eE][-+]?\d+)?", path), dtype=float
    ).reshape(3, 2)
    vertices, footprints = [], []
    for coordinates, image, name in (
        (native, actual, "native"),
        (expected, reference, "scanpy"),
    ):
        centered = np.round(
            coordinates - (coordinates.min(axis=0) + coordinates.max(axis=0)) / 2, 10
        )
        vertices.append(centered[np.lexsort((centered[:, 1], centered[:, 0]))])
        yy, xx = np.where(np.asarray(image).max(axis=2) < 128)
        assert len(xx) > 1000
        footprints.append([int(xx.max() - xx.min() + 1), int(yy.max() - yy.min() + 1)])
        image.save(tmp_path / f"{name}.png")
    (tmp_path / "geometry.json").write_text(
        json.dumps(
            {
                "marker": marker,
                "linewidth": linewidth,
                "native_vertices": vertices[0].tolist(),
                "scanpy_vertices": vertices[1].tolist(),
                "footprints": footprints,
            },
            indent=2,
        )
    )
    return vertices, footprints


@pytest.mark.parametrize("page", [1.5], indirect=True)
@pytest.mark.xfail(
    strict=True,
    raises=AssertionError,
    reason="C14: native equilateral triangles differ from Scanpy's 1:1 triangle geometry",
)
def test_native_triangle_matches_scanpy_path_and_paint(triangle_geometry):
    vertices, footprints = triangle_geometry
    np.testing.assert_allclose(vertices[0], vertices[1], atol=0.001)
    np.testing.assert_allclose(footprints[0], footprints[1], atol=2)
