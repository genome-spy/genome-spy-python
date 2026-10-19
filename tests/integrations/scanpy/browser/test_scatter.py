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
