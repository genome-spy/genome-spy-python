"""Browser rendering and measured reference comparisons shared by Scanpy tests."""

import xml.etree.ElementTree as ET
from io import BytesIO

import numpy as np
from PIL import Image

from genome_spy._embed import bundled_module_url
from tests.integrations.scanpy.helpers import units


def style_profile_reference(ax):
    """Register stored positions using the reviewed native edge width and opacity."""
    for artist in ax.collections:
        artist.set_linewidths([0])
        artist.set_alpha(0.8)


def guide_geometry(page):
    """Measure exported guides in canvas coordinates without changing the chart."""
    svg = page.evaluate("async()=> (await api.imageExport.svg()).blob.text()")
    return page.evaluate(
        """svg => {
        const root = new DOMParser().parseFromString(svg, 'image/svg+xml').documentElement;
        root.style.cssText = 'position:absolute;left:0;top:0;visibility:hidden';
        document.body.append(root);
        const box = node => {
            const r = node.getBoundingClientRect();
            return {x:r.x,y:r.y,width:r.width,height:r.height};
        };
        const result = {
            text: [...root.querySelectorAll('text')].map(n=>({label:n.textContent,...box(n)})),
            gradients: [...root.querySelectorAll('rect')]
                .filter(n=>(n.getAttribute('fill')||'').startsWith('url(')).map(box),
        };
        root.remove();
        return result;
        }""",
        svg,
    )


def panel_image(page, bounds):
    """Capture the plot area at the browser's original pixel scale."""
    canvas = page.locator("canvas").first.bounding_box()
    clip = {
        "x": canvas["x"] + bounds["x"],
        "y": canvas["y"] + bounds["y"],
        "width": bounds["width"],
        "height": bounds["height"],
    }
    return Image.open(BytesIO(page.screenshot(clip=clip))).convert("RGB")


def assert_complete_chart(
    page, tmp_path, chart, expected, reference_image, case, *, panel_index=0
):
    """Compare registered point footprints, paints and complete native labels to an oracle."""
    bounds = render(page, chart)
    if panel_index:
        bounds = page.evaluate(
            "i=>api.views.getLayoutBounds({scope:[],view:'panel-'+i})", panel_index
        )
    actual = panel_image(page, bounds)
    oracle = Image.open(reference_image).convert("RGB")
    assert (
        abs(actual.width - oracle.width) <= 2
        and abs(actual.height - oracle.height) <= 2
    )
    # Equal coordinate registration and export DPI keep point locations and footprints comparable.
    mask = np.min(np.asarray(actual), axis=2) < 245
    target = np.min(np.asarray(oracle), axis=2) < 245
    for x, y in expected["coordinates"]:
        x0, x1 = expected["x_domain"]
        y0, y1 = expected["y_domain"]
        if expected.get("log", False):
            x, x0, x1 = np.log10([x, x0, x1])
            y, y0, y1 = np.log10([y, y0, y1])
        px, py = (
            round((x - x0) / (x1 - x0) * actual.width),
            round((y1 - y) / (y1 - y0) * actual.height),
        )
        assert (
            mask[py - 3 : py + 4, px - 3 : px + 4].any()
            and target[py - 3 : py + 4, px - 3 : px + 4].any()
        )
        patch = np.asarray(actual)[py - 1 : py + 2, px - 1 : px + 2].astype(int)
        paint = np.asarray(oracle)[py, px].astype(int)
        assert np.abs(patch - paint).max(axis=2).min() <= 12

    # Most raster differences should be confined to antialiased point boundaries.
    extent = (0, 0, min(actual.width, oracle.width), min(actual.height, oracle.height))
    pixels = np.asarray(actual.crop(extent)).astype(int)
    reference = np.asarray(oracle.crop(extent)).astype(int)
    assert (np.abs(pixels - reference).max(axis=2) > 32).mean() < 0.025
    svg = page.evaluate("async () => (await api.imageExport.svg()).blob.text()")
    labels = [e.text for e in ET.fromstring(svg).iter() if e.tag.endswith("text")]
    for label in expected["labels"] + [expected["title"]] + (expected["legend"] or []):
        if label:
            assert label in labels
    page.screenshot(path=str(tmp_path / f"{case}-complete.png"), full_page=True)
    Image.blend(actual.crop(extent), oracle.crop(extent), 0.5).save(
        tmp_path / f"{case}-registered-overlay.png"
    )


def render_heatmap(page, chart):
    """Wait for native track sizing before measuring exported geometry."""
    render(page, chart)
    page.wait_for_timeout(200)
    return page.evaluate("api.views.getLayoutBounds({scope:[],view:'panel-0'})")


def render(page, chart, *, renderer="webgl", scale_prefix=None):
    """Render a chart or prepared spec; return its first panel's native bounds."""
    spec = chart if isinstance(chart, dict) else chart.to_dict()
    if scale_prefix is not None:
        for axis in ("x", "y"):
            spec["scales"][axis]["name"] = f"{scale_prefix}-{axis}"
    for i, panel in enumerate(units(spec)):
        panel["name"] = f"panel-{i}"
    page.set_content(
        '<style>body{margin:0;background:white}</style><div id="chart"></div>'
    )
    page.evaluate(
        """async ({url,spec,renderer}) => {
        const {embed} = await import(url);
        window.api = await Promise.race([
            embed(document.querySelector('#chart'),spec,{renderer}),
            new Promise((_,reject)=>setTimeout(()=>reject(Error('Embed timeout')),20000)),
        ]);
        await new Promise(requestAnimationFrame);
        await new Promise(requestAnimationFrame);
    }""",
        {"url": bundled_module_url("embed"), "spec": spec, "renderer": renderer},
    )
    page.locator("canvas").first.wait_for(state="visible")
    page.wait_for_function("""() => Math.abs(
        document.querySelector('canvas').getBoundingClientRect().width
        - api.getLogicalCanvasSize().width) < 0.1""")
    assert page.locator(".message-box").count() == 0, page.locator(
        ".message-box"
    ).all_text_contents()
    return page.evaluate("api.views.getLayoutBounds({scope:[],view:'panel-0'})")
