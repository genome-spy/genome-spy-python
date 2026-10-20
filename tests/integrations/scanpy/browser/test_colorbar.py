"""Native continuous guides fit their panels and remain configurable after collection."""

import pytest

import genome_spy.integrations.scanpy as gsc
from tests.integrations.scanpy.browser.test_umap import render
from tests.integrations.scanpy.embedding_fixture import make_embedding_adata


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


@pytest.mark.parametrize("location", [None, "right", "left", "top", "bottom"])
@pytest.mark.parametrize("rows", [1, 2])
def test_colorbars_fit_mixed_panel_grids_without_moving_category_legends(
    page, tmp_path, location, rows
):
    colors = ["cell_type", "score"] if rows == 1 else ["cell_type", "score", "g1", "g2"]
    chart = gsc.pl.umap(
        make_embedding_adata(),
        color=colors,
        ncols=2,
        colorbar_loc=location,
        width=320,
        height=180,
        frameon=True,
        show=False,
    )
    render(page, chart)
    bounds = [
        page.evaluate("i=>api.views.getLayoutBounds({scope:[],view:'panel-'+i})", i)
        for i in range(len(colors))
    ]
    guides = guide_geometry(page)
    assert len(guides["gradients"]) == (0 if location is None else len(colors) - 1)
    for gradient, panel in zip(
        guides["gradients"], bounds[1:], strict=location is not None
    ):
        if location in ("top", "bottom"):
            assert abs(gradient["width"] - panel["width"]) <= 2
            assert gradient["height"] < 15
            if location == "top":
                assert gradient["y"] + gradient["height"] <= panel["y"]
            else:
                assert gradient["y"] >= panel["y"] + panel["height"]
        else:
            assert abs(gradient["height"] - panel["height"]) <= 2
            assert gradient["width"] < 15
            if location == "left":
                assert gradient["x"] + gradient["width"] <= panel["x"]
            else:
                assert gradient["x"] >= panel["x"] + panel["width"]
    categories = [
        item
        for item in guides["text"]
        if item["label"] in {"C", "B", "A", "unused", "NA"}
    ]
    assert len(categories) == 5
    assert all(item["x"] >= bounds[0]["x"] + bounds[0]["width"] for item in categories)
    size = page.evaluate("api.getLogicalCanvasSize()")
    for item in guides["text"] + guides["gradients"]:
        assert item["x"] >= -1 and item["y"] >= -1
        assert item["x"] + item["width"] <= size["width"] + 1
        assert item["y"] + item["height"] <= size["height"] + 1
    page.screenshot(path=str(tmp_path / f"{rows}-{location}.png"), full_page=True)


def test_collected_numeric_colorbars_accept_native_orientation_and_size_overrides(page):
    chart = (
        gsc.pl.umap(
            make_embedding_adata(),
            color=["score", "g1", "g2", "raw_only"],
            colorbar_loc="top",
            ncols=2,
            width=320,
            height=180,
            show=False,
        )
        .resolve_legend(default="collected")
        .configure_legend(
            orient="left",
            direction="vertical",
            gradientLength=140,
            gradientThickness=8,
        )
    )
    render(page, chart)
    guides = guide_geometry(page)
    assert len(guides["gradients"]) == 4
    plot_left = min(
        page.evaluate("i=>api.views.getLayoutBounds({scope:[],view:'panel-'+i}).x", i)
        for i in range(4)
    )
    assert all(
        bar["x"] + bar["width"] < plot_left
        and abs(bar["height"] - 140) <= 2
        and abs(bar["width"] - 8) < 1
        for bar in guides["gradients"]
    )
    size = page.evaluate("api.getLogicalCanvasSize()")
    for item in guides["text"] + guides["gradients"]:
        assert item["x"] >= -1 and item["y"] >= -1
        assert item["x"] + item["width"] <= size["width"] + 1
        assert item["y"] + item["height"] <= size["height"] + 1
