"""Registered density point colors, footprints, guides and observed navigation."""

import xml.etree.ElementTree as ET

import pytest

import genome_spy.integrations.scanpy as gsc
from tests.integrations.scanpy.helpers import name_embedding_scales
from tests.integrations.scanpy.browser.test_embedding import assert_complete_chart
from tests.integrations.scanpy.browser.test_umap import render, move_to
from tests.integrations.scanpy.embedding_density_fixture import make_density
from tests.integrations.scanpy.helpers import points, units


@pytest.mark.parametrize("page", [1.5], indirect=True)
@pytest.mark.parametrize("mode", ["groups", "global", "bounds", "center", "unused"])
def test_density_panels_match_public_scanpy_background_foreground_and_guides(
    page, tmp_path, mode
):
    import matplotlib.pyplot as plt
    import scanpy as sc

    a = make_density(grouped=mode != "global")
    options = {"color_map": "viridis"}
    if mode == "groups":
        options["group"] = ["A", "B"]
    if mode == "unused":
        a.obs["condition"] = a.obs["condition"].cat.add_categories(["unused"])
        options["group"] = ["unused"]
    if mode == "bounds":
        options.update(vmin=0.2, vmax=0.7)
    if mode == "center":
        options.update(vcenter=0.3)
    with plt.rc_context(plt.rcParamsDefault):
        result = sc.pl.embedding_density(a.copy(), key="scores", show=False, **options)
    axes = result if isinstance(result, list) else [result]
    axes[0].figure.canvas.draw()
    references = []
    for i, ax in enumerate(axes):
        bounds = ax.get_window_extent()
        path = tmp_path / f"reference-{i}.png"
        ax.figure.savefig(
            path,
            dpi=150,
            bbox_inches=bounds.transformed(ax.figure.dpi_scale_trans.inverted()),
            pad_inches=0,
        )
        references.append(
            (
                path,
                {
                    "coordinates": ax.collections[0].get_offsets().tolist(),
                    "x_domain": ax.get_xlim(),
                    "y_domain": ax.get_ylim(),
                    "labels": [ax.get_xlabel(), ax.get_ylabel()],
                    "title": ax.get_title(),
                    "legend": None,
                },
            )
        )
    chart = gsc.pl.embedding_density(
        a, key="scores", width=bounds.width, height=bounds.height, show=False, **options
    )
    for i, (path, expected) in enumerate(references):
        assert_complete_chart(
            page, tmp_path, chart, expected, path, f"density-{mode}-{i}", panel_index=i
        )
    plt.close(axes[0].figure)


def test_default_palette_and_under_over_colors_use_native_point_encodings(page):
    a = make_density(False)
    chart = gsc.pl.embedding_density(a, vmin=0.2, vmax=0.8, show=False)
    render(page, chart)
    svg = page.evaluate("async () => (await api.imageExport.svg()).blob.text()")
    root = ET.fromstring(svg)
    circles = [e for e in root.iter() if e.tag.endswith("circle")]
    # Vega's yelloworangered endpoints intentionally differ from Matplotlib YlOrRd.
    assert len(circles) == a.n_obs
    assert {"rgb(254, 224, 135)", "rgb(175, 2, 37)"} <= {e.get("fill") for e in circles}
    for paint in ("lightgray", "black"):
        layer = next(e for e in root.iter() if e.get("fill") == paint)
        assert sum(e.tag.endswith("circle") for e in layer.iter()) == 2


@pytest.mark.parametrize("group", [["A", "B"], "A"])
def test_hover_reports_stored_density_and_shared_zoom_including_background_cells(
    page, tmp_path, group
):
    a = make_density()
    chart = gsc.pl.embedding_density(
        a,
        key="scores",
        group=group,
        obs_id="cell_id",
        zoom=True,
        width=280,
        height=260,
        show=False,
    )
    spec = chart.to_dict()
    bounds = render(page, name_embedding_scales(chart.to_dict(), "umap"))
    encoding = points(units(spec)[0])["encoding"]
    domains = [encoding[axis]["scale"]["domain"] for axis in ("x", "y")]
    for index in (0, 1):
        x, y = a.obsm["X_umap"][index, :2]
        move_to(page, bounds, x, y, *domains, f"id-{index}")
        page.get_by_text("scores (obs['scores'])", exact=True).wait_for(state="visible")
        values = [
            s.strip() for s in page.locator("table.attributes td").all_text_contents()
        ]
        assert values[:2] == [f"id-{index}", f"cell-{index}"]
        assert float(values[2]) == pytest.approx(a.obs["scores"].iloc[index])
    before = page.evaluate("api.getScaleResolutionByName('umap-x-0').getDomain()")
    page.mouse.wheel(0, -180)
    page.wait_for_function(
        "b=>{const d=api.getScaleResolutionByName('umap-x-0').getDomain();return d[1]-d[0]<b[1]-b[0]}",
        arg=before,
    )
    assert (
        page.evaluate("api.getScaleResolutionByName('umap-x-0').getDomain()") != before
    )
    path = tmp_path / "density.html"
    chart.save(path, inline=True, controls=False)
    page.context.set_offline(True)
    page.goto(path.as_uri())
    page.locator("canvas").first.wait_for(state="visible")
    assert not page.locator(".message-box").count()
