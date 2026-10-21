"""Observe complete QC panels, shared native legends, hover, navigation and HTML."""

import xml.etree.ElementTree as ET

import numpy as np
import pytest

import genome_spy.integrations.scanpy as gsc
from tests.integrations.scanpy.browser.test_embedding import assert_complete_chart
from tests.integrations.scanpy.browser.test_umap import render, move_to
from tests.integrations.scanpy.helpers import units
from tests.integrations.scanpy.hvg_fixture import make_hvg_result


@pytest.mark.parametrize("page", [1.5], indirect=True)
@pytest.mark.parametrize("flavor", ["seurat", "seurat_v3"])
@pytest.mark.parametrize("log", [False, True])
def test_both_qc_panels_match_registered_scanpy_points_axes_and_legends(
    page, tmp_path, flavor, log
):
    import matplotlib.pyplot as plt
    import scanpy as sc

    data = make_hvg_result(flavor=flavor)
    references = []
    with plt.rc_context({"figure.dpi": 100}):
        sc.pl.highly_variable_genes(data, log=log, show=False)
        figure = plt.gcf()
        legend = [text.get_text() for text in figure.axes[0].get_legend().get_texts()]
        # Native guides are collected below the pair rather than over its points.
        figure.axes[0].get_legend().set_visible(False)
        figure.canvas.draw()
        for index, ax in enumerate(figure.axes):
            box = ax.get_window_extent()
            image = tmp_path / f"reference-{index}.png"
            figure.savefig(
                image,
                dpi=150,
                bbox_inches=box.transformed(figure.dpi_scale_trans.inverted()),
                pad_inches=0,
            )
            references.append(
                (
                    image,
                    {
                        "coordinates": np.concatenate(
                            [c.get_offsets() for c in ax.collections]
                        ).tolist(),
                        "x_domain": ax.get_xlim(),
                        "y_domain": ax.get_ylim(),
                        "log": log,
                        "labels": [ax.get_xlabel(), ax.get_ylabel()],
                        "title": None,
                        "legend": legend,
                        "width": box.width,
                        "height": box.height,
                    },
                )
            )
        plt.close(figure)
    chart = gsc.pl.highly_variable_genes(
        data,
        log=log,
        width=references[0][1]["width"],
        height=references[0][1]["height"],
        show=False,
    )
    for index, (image, expected) in enumerate(references):
        assert_complete_chart(
            page, tmp_path, chart, expected, image, f"hvg-{index}", panel_index=index
        )
    svg = page.evaluate("async()=> (await api.imageExport.svg()).blob.text()")
    root = ET.fromstring(svg)
    labels = [e.text for e in root.iter() if e.tag.endswith("text")]
    assert all(labels.count(label) == 1 for label in legend)
    fills = page.evaluate(
        """svg => {
        const root = new DOMParser().parseFromString(svg, 'image/svg+xml').documentElement;
        root.style.cssText = 'position:absolute;left:0;top:0;visibility:hidden';
        document.body.append(root);
        const colors = [...root.querySelectorAll('circle')]
            .filter(n => +n.getAttribute('r') > 2).map(n => getComputedStyle(n).fill);
        root.remove();
        return colors;
    }""",
        svg,
    )
    assert fills == ["rgb(0, 0, 0)", "rgb(128, 128, 128)"]
    assert len([e for e in root.iter() if e.tag.endswith("circle")]) == 2 * len(
        data
    ) + len(legend)


@pytest.mark.parametrize("log", [False, True])
def test_hover_zoom_and_offline_delivery(page, tmp_path, log):
    chart = gsc.pl.highly_variable_genes(
        make_hvg_result(), log=log, zoom=True, show=False
    )
    spec = chart.to_dict()
    encoding = units(spec)[0]["encoding"]
    bounds = render(page, chart)
    domains = [encoding[axis]["scale"]["domain"] for axis in ("x", "y")]
    coordinates = [2, 1.3]
    if log:
        domains = [np.log10(d).tolist() for d in domains]
        coordinates = np.log10(coordinates).tolist()
    move_to(page, bounds, *coordinates, *domains, "gene-4")
    page.get_by_text("Selection", exact=True).wait_for(state="visible")
    assert [
        value.strip()
        for value in page.locator("table.attributes td").all_text_contents()
    ] == ["gene-4", "gene-4", "highly variable genes", "2.000", "1.300"]
    names = ["hvg-x-0", "hvg-y-0", "hvg-x-1", "hvg-y-1"]
    before = page.evaluate(
        "names=>names.map(n=>api.getScaleResolutionByName(n).getDomain())", names
    )
    page.mouse.wheel(0, -220)
    page.wait_for_function(
        "({names,before})=>names.slice(0,2).every((n,i)=>{const d=api.getScaleResolutionByName(n).getDomain();return d[1]-d[0]<before[i][1]-before[i][0];})",
        arg={"names": names, "before": before},
    )
    assert (
        page.evaluate("api.getScaleResolutionByName('hvg-x-1').getDomain()")
        == before[2]
    )
    assert (
        page.evaluate("api.getScaleResolutionByName('hvg-y-1').getDomain()")
        == before[3]
    )
    path = tmp_path / "hvg.html"
    chart.save(path, inline=True, controls=False)
    page.context.set_offline(True)
    page.goto(path.as_uri())
    page.locator("canvas").first.wait_for(state="visible")
    assert not page.locator(".message-box").count()
