"""Stored edges stay beneath points and follow native coordinate scales."""

from io import BytesIO

import numpy as np
import pytest
from PIL import Image
from scipy import sparse
from scipy.ndimage import distance_transform_cdt

import genome_spy.integrations.scanpy as gsc
from tests.integrations.scanpy.browser.test_colorbar import guide_geometry
from tests.integrations.scanpy.browser.test_umap import render
from tests.integrations.scanpy.test_embedding_edges import graph_adata


@pytest.mark.parametrize("page", [1.5], indirect=True)
@pytest.mark.parametrize("outlined", [False, True])
@pytest.mark.parametrize("width,color", [(0, "navy"), (0.1, "grey"), (1.2, "navy")])
def test_registered_edges_and_point_order_match_scanpy(
    page, tmp_path, outlined, width, color
):
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib.collections import LineCollection
    import scanpy as sc

    data = graph_adata()
    data.obsm["X_umap"] = np.array(
        [
            [-1, -1],
            [1, -1],
            [1, 1],
            [-1, 1],
            [0, 0],
            [0.2, -0.8],
            [0.8, 0.4],
            [-0.8, 0.3],
        ]
    )
    data.obs["score"] = np.arange(8, dtype=float)
    options = dict(
        color="score",
        edges=True,
        edges_width=width,
        edges_color=color,
        add_outline=outlined,
        alpha=0.6,
        size=144,
        marker="o",
        frameon=True,
        title="Stored graph",
        show=False,
    )
    reference = tmp_path / "scanpy.png"
    with plt.rc_context({"figure.figsize": (4, 3), "figure.dpi": 100}):
        ax = sc.pl.umap(data.copy(), **options)
        ax.figure.canvas.draw()
        box = ax.get_window_extent()
        segments = next(
            c for c in ax.collections if isinstance(c, LineCollection)
        ).get_segments()
        xdomain, ydomain = ax.get_xlim(), ax.get_ylim()
        ax.figure.savefig(
            reference,
            dpi=150,
            bbox_inches=box.transformed(ax.figure.dpi_scale_trans.inverted()),
            pad_inches=0,
        )
        plt.close(ax.figure)
    chart = gsc.pl.umap(data, width=box.width, height=box.height, **options)
    bounds = render(page, chart)
    canvas = page.locator("canvas").bounding_box()
    dpr = page.evaluate("devicePixelRatio")
    full = Image.open(BytesIO(page.screenshot())).convert("RGB")
    left, top = (canvas[axis] + bounds[axis] for axis in ("x", "y"))
    actual = full.crop(
        (
            round(left * dpr),
            round(top * dpr),
            round((left + bounds["width"]) * dpr),
            round((top + bounds["height"]) * dpr),
        )
    )
    oracle = Image.open(reference).convert("RGB")
    assert (
        abs(actual.width - oracle.width) <= 2
        and abs(actual.height - oracle.height) <= 2
    )
    extent = (0, 0, min(actual.width, oracle.width), min(actual.height, oracle.height))
    actual, oracle = actual.crop(extent), oracle.crop(extent)
    pixels, target = np.asarray(actual).astype(int), np.asarray(oracle).astype(int)
    radius = int(np.ceil(dpr))
    interior = [image[radius:-radius, radius:-radius] for image in (pixels, target)]
    masks = [image.min(axis=2) < 240 for image in interior]
    # Agg and WebGL distribute stroke coverage differently; compare position and total ink.
    for first, second in [(masks[0], masks[1]), (masks[1], masks[0])]:
        distance = distance_transform_cdt(~second, metric="chessboard")
        assert (distance[first] > radius).mean() < 0.01
    ink = [(255 - image).sum() for image in interior]
    assert abs(ink[0] / ink[1] - 1) < 0.1
    for x, y in data.obsm["X_umap"]:
        px = round((x - xdomain[0]) / np.ptp(xdomain) * actual.width)
        py = round((ydomain[1] - y) / np.ptp(ydomain) * actual.height)
        assert (
            np.abs(pixels[py - 1 : py + 2, px - 1 : px + 2] - target[py, px])
            .max(axis=2)
            .min()
            <= 12
        )
    rgb = np.asarray(matplotlib.colors.to_rgb(color)) * 255
    edge_hue = (255 - rgb) / (255 - rgb).max()
    for segment in segments:
        x, y = segment[0] * 0.7 + segment[1] * 0.3
        px = round((x - xdomain[0]) / np.ptp(xdomain) * actual.width)
        py = round((ydomain[1] - y) / np.ptp(ydomain) * actual.height)
        patch = pixels[py - 2 : py + 3, px - 2 : px + 3].reshape(-1, 3)
        # Every interior segment must paint; point-only charts cannot pass this check.
        painted = patch.min() < 250
        assert painted == (width > 0)
        if width:
            darkest = patch[patch.sum(axis=1).argmin()]
            hue = (255 - darkest) / (255 - darkest).max()
            np.testing.assert_allclose(hue, edge_hue, atol=0.03)
    guides = guide_geometry(page)
    assert {"Stored graph", "UMAP1", "UMAP2"} <= {
        item["label"] for item in guides["text"]
    }
    assert len(guides["gradients"]) == 1
    assert abs(guides["gradients"][0]["height"] - bounds["height"]) <= 2
    actual.save(tmp_path / "native-panel.png")
    Image.blend(actual, oracle, 0.5).save(tmp_path / "registered-overlay.png")
    page.screenshot(path=str(tmp_path / "complete.png"))


def test_empty_graph_renders_only_the_existing_points(page):
    data = graph_adata()
    data.obsp["connectivities"] = sparse.csr_matrix((8, 8))
    render(page, gsc.pl.umap(data, color="score", edges=True, show=False))
