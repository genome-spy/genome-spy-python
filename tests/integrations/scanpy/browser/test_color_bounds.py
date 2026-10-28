"""Centered colors retain native point paint, guides and registered Scanpy geometry."""

from io import BytesIO

import numpy as np
import pytest
from PIL import Image

import genome_spy.integrations.scanpy as gsc
from tests.integrations.scanpy.browser.rendering import (
    assert_complete_chart,
    guide_geometry,
)
from tests.integrations.scanpy.embedding_fixtures import make_embedding_adata


@pytest.mark.reference
@pytest.mark.parametrize("page", [1.5], indirect=True)
@pytest.mark.parametrize(
    "options,constant",
    [
        ({"vcenter": 0, "vmin": -2, "vmax": 4}, False),
        ({"vcenter": "p50"}, False),
        ({"vcenter": 10}, False),
        ({"vcenter": 2}, True),
        ({"vcenter": 2, "colorbar_loc": None}, True),
    ],
)
def test_centered_paint_and_guides_match_registered_scanpy(
    page, tmp_path, options, constant
):
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    import scanpy as sc

    data = make_embedding_adata()
    data.obs["score"] = 2.0 if constant else [-3, -2, -1, 0, 1, 2, 4, 6]
    options = dict(
        color="score",
        size=144,
        marker="o",
        cmap="viridis",
        frameon=True,
        title="Centered scores",
        show=False,
        **options,
    )
    reference = tmp_path / "scanpy-panel.png"
    with plt.rc_context({"figure.figsize": (4, 3), "figure.dpi": 100}):
        ax = sc.pl.umap(data, **options)
        ax.figure.canvas.draw()
        box = ax.get_window_extent()
        expected = dict(
            coordinates=data.obsm["X_umap"][:, :2].tolist(),
            x_domain=list(ax.get_xlim()),
            y_domain=list(ax.get_ylim()),
            labels=[ax.get_xlabel(), ax.get_ylabel()],
            title=ax.get_title(),
            legend=None,
        )
        ax.figure.savefig(
            reference,
            dpi=150,
            bbox_inches=box.transformed(ax.figure.dpi_scale_trans.inverted()),
            pad_inches=0,
        )
        plt.close(ax.figure)
    chart = gsc.pl.umap(data, width=box.width, height=box.height, **options)
    assert_complete_chart(page, tmp_path, chart, expected, reference, "centered")
    if options["vcenter"] == 0:
        guides = guide_geometry(page)
        assert len(guides["gradients"]) == 1
        gradient = guides["gradients"][0]
        zero = next(label for label in guides["text"] if label["label"] in {"0", "0.0"})
        assert (
            abs(zero["y"] + zero["height"] / 2 - gradient["y"] - gradient["height"] / 2)
            < 2
        )
        canvas = page.locator("canvas").first.bounding_box()
        dpr = page.evaluate("devicePixelRatio")
        x = round((canvas["x"] + gradient["x"] + gradient["width"] / 2) * dpr)
        y = round((canvas["y"] + gradient["y"] + gradient["height"] / 2) * dpr)
        pixels = np.asarray(Image.open(BytesIO(page.screenshot())).convert("RGB"))
        np.testing.assert_allclose(
            pixels[y, x],
            np.array(matplotlib.colormaps["viridis"](0.5)[:3]) * 255,
            atol=3,
        )
