"""Observe scatter's shared point renderer, native axes, hover and navigation."""

import json
from pathlib import Path

import pytest

import genome_spy.integrations.scanpy as gsc
from tests.integrations.scanpy.browser.test_embedding import assert_complete_chart
from tests.integrations.scanpy.browser.test_umap import render, move_to
from tests.integrations.scanpy.helpers import points
from tests.integrations.scanpy.scatter_fixture import make_scatter_adata, scatter_cases

REFERENCE = json.loads(
    (Path(__file__).parents[1] / "fixtures/scatter.json").read_text()
)["cases"]


@pytest.mark.parametrize("family", ["umap", "scatter"])
@pytest.mark.parametrize(
    "marker,shape", [("o", "circle"), ("s", "rect"), ("D", "path")]
)
def test_category_legend_matches_panel_marker_and_expected_width(
    page, family, marker, shape
):
    import scanpy as sc
    import matplotlib.pyplot as plt
    from matplotlib.markers import MarkerStyle

    data = make_scatter_adata()
    data.obs["two"] = ["A", "B"] * (data.n_obs // 2)
    args = (data, "x_value", "y_value") if family == "scatter" else (data,)
    options = dict(color="two", marker=marker, show=False)
    ax = getattr(sc.pl, family)(*args, **options)
    handle = ax.get_legend().legend_handles[0]
    reference_marker = MarkerStyle(marker)
    path = (
        reference_marker.get_path().transformed(reference_marker.get_transform())
        if family == "umap"
        else handle.get_paths()[0]
    )
    expected_width = handle.get_sizes()[0] ** 0.5 * path.get_extents().width * 100 / 72
    plt.close(ax.figure)
    bounds = render(page, getattr(gsc.pl, family)(*args, **options))
    svg = page.evaluate("async () => (await api.imageExport.svg()).blob.text()")
    symbols = page.evaluate(
        """({svg,edge}) => {
        const root = new DOMParser().parseFromString(svg,'image/svg+xml').documentElement;
        root.style.cssText = 'position:absolute;left:0;top:0;visibility:hidden';
        document.body.append(root);
        const symbols = [...root.querySelectorAll('circle,rect,path')].flatMap(n => {
            const b=n.getBoundingClientRect();
            return b.x > edge ? [{shape:n.tagName,width:b.width}] : [];
        });
        root.remove();
        return symbols;
        }""",
        {"svg": svg, "edge": bounds["x"] + bounds["width"]},
    )
    assert len(symbols) == 2
    assert all(s["shape"] == shape for s in symbols)
    assert all(s["width"] == pytest.approx(expected_width, abs=0.1) for s in symbols)


@pytest.mark.parametrize("page", [1.5], indirect=True)
@pytest.mark.parametrize("case", scatter_cases())
def test_complete_scatter_matches_registered_points_axes_labels_and_guides(
    page, tmp_path, reference_images, case
):
    expected = REFERENCE[case]
    chart = gsc.pl.scatter(
        make_scatter_adata(),
        **scatter_cases()[case],
        size=80,
        frameon=True,
        width=expected["plot_size"][0],
        height=expected["plot_size"][1],
        show=False,
    )
    assert_complete_chart(
        page,
        tmp_path,
        chart,
        expected,
        reference_images("scatter") / f"{case}-panel.png",
        case,
    )


@pytest.mark.parametrize("axis", ["obs", "var"])
def test_scatter_hover_zoom_and_offline_html_use_existing_embedding_interactions(
    page, tmp_path, axis
):
    options = (
        dict(x="x_value", y="y_value", color="cell_type")
        if axis == "obs"
        else dict(x="mean_value", y="dispersion", color="gene_group")
    )
    chart = gsc.pl.scatter(
        make_scatter_adata(), **options, size=200, zoom=True, show=False
    )
    spec = chart.to_dict()
    point = points(spec)
    bounds = render(page, chart)
    row = next(iter(spec["datasets"].values()))[4 if axis == "obs" else 1]
    domains = [point["encoding"][a]["scale"]["domain"] for a in ("x", "y")]
    move_to(page, bounds, row["_coord_0"], row["_coord_1"], *domains, row["_obs_label"])
    page.get_by_text(
        "Observation" if axis == "obs" else "Variable", exact=True
    ).wait_for(state="visible")
    assert [name for name in page.locator("table.attributes th").all_text_contents()][
        -2:
    ] == [options["x"], options["y"]]
    assert [
        value.strip()
        for value in page.locator("table.attributes td").all_text_contents()[:2]
    ] == [
        row["_obs_id"],
        row["_obs_label"],
    ]
    names = ["scatter-x-0", "scatter-y-1"]
    expression = "names=>names.map(n=>api.getScaleResolutionByName(n).getDomain())"
    before = page.evaluate(expression, names)
    page.mouse.wheel(0, -220)
    page.wait_for_function(
        "({names,before})=>names.every((n,i)=>api.getScaleResolutionByName(n).getDomain()[1]-api.getScaleResolutionByName(n).getDomain()[0]<before[i][1]-before[i][0])",
        arg={"names": names, "before": before},
    )
    path = tmp_path / f"scatter-{axis}.html"
    chart.save(path, inline=True, controls=False)
    page.context.set_offline(True)
    page.goto(path.as_uri())
    page.locator("canvas").first.wait_for(state="visible")
    assert not page.locator(".message-box").count()


@pytest.mark.parametrize("family,rows", [("scatter", 1), ("umap", 1), ("umap", 2)])
def test_native_collected_legends_fit_below_all_panels_with_compact_symbols(
    page, tmp_path, family, rows
):
    import scanpy as sc

    a = sc.datasets.pbmc68k_reduced()
    options = {"x": "n_counts", "y": "n_genes"} if family == "scatter" else {"ncols": 2}
    colors = (
        ["louvain", "percent_mito"]
        if rows == 1
        else ["louvain", "n_counts", "phase", "percent_mito"]
    )
    chart = (
        getattr(gsc.pl, family)(
            a, color=colors, width=280, height=280, show=False, **options
        )
        .resolve_legend(default="collected")
        .configure_legend(
            orient="bottom",
            direction="horizontal",
            columns=6,
            symbolSize=64,
            gradientLength=140,
            gradientThickness=10,
            tickCount=3,
            layout={"anchor": "middle", "wrap": True},
        )
    )
    render(page, chart)
    bounds = [
        page.evaluate("i=>api.views.getLayoutBounds({scope:[],view:'panel-'+i})", i)
        for i in range(len(colors))
    ]
    plot_bottom = max(b["y"] + b["height"] for b in bounds)
    svg = page.evaluate("async()=> (await api.imageExport.svg()).blob.text()")
    guides = page.evaluate(
        """svg=>{
        const root = new DOMParser().parseFromString(svg, 'image/svg+xml').documentElement;
        root.style.cssText = 'position:absolute;left:0;top:0;visibility:hidden';
        document.body.append(root);
        const box = node => { const r=node.getBoundingClientRect(); return {x:r.x,y:r.y,width:r.width,height:r.height}; };
        const result = {
            text: [...root.querySelectorAll('text')].map(n=>({label:n.textContent,...box(n)})),
            shapes: [...root.querySelectorAll('path,circle,rect')].map(box),
            gradients: [...root.querySelectorAll('rect')].filter(n=>(n.getAttribute('fill')||'').startsWith('url(')).map(box),
        };
        root.remove();
        return result;
    }""",
        svg,
    )
    labels = [
        r
        for r in guides["text"]
        if r["label"] in [str(i) for i in range(11)] + ["G1", "S", "G2M"]
    ]
    assert len(labels) == 11 + (3 if rows == 2 else 0)
    assert all(label["y"] > plot_bottom for label in labels)
    symbols = [
        b
        for b in guides["shapes"]
        if b["y"] > plot_bottom
        and b["width"] > 4
        and abs(b["width"] - b["height"]) < 0.1
    ]
    assert len(symbols) == len(labels)
    assert all(symbol["width"] < 12 for symbol in symbols)
    assert len(guides["gradients"]) == (1 if rows == 1 else 2)
    assert all(
        g["y"] > plot_bottom and abs(g["width"] - 140) < 1 for g in guides["gradients"]
    )
    for gradient in guides["gradients"]:
        ticks = sorted(
            (
                label
                for label in guides["text"]
                if gradient["y"] + gradient["height"]
                <= label["y"]
                < gradient["y"] + gradient["height"] + 25
                and gradient["x"] - 20
                <= label["x"]
                < gradient["x"] + gradient["width"] + 20
            ),
            key=lambda label: label["x"],
        )
        assert len(ticks) >= 2
        assert all(
            left["x"] + left["width"] <= right["x"]
            for left, right in zip(ticks, ticks[1:])
        )
    size = page.evaluate("api.getLogicalCanvasSize()")
    for item in labels + symbols + guides["gradients"]:
        assert 0 <= item["x"] and item["x"] + item["width"] <= size["width"] + 1
        assert item["y"] + item["height"] <= size["height"] + 1
    page.screenshot(
        path=str(tmp_path / f"{family}-{rows}-bottom-guides.png"), full_page=True
    )
