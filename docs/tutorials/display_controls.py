"""Executable snippets used by the display controls user guide."""

from pathlib import Path

import genome_spy as gs


variants = [
    {"chrom": "chr17", "position": 43_044_295, "score": 4.2},
    {"chrom": "chr17", "position": 43_051_232, "score": 7.8},
    {"chrom": "chr17", "position": 43_063_418, "score": 5.6},
]

chart = (
    gs.Chart(variants)
    .mark_point(size=110)
    .encode(
        x=gs.Locus("chrom", "position")
        .scale(
            domain=[
                {"chrom": "chr17", "pos": 43_040_000},
                {"chrom": "chr17", "pos": 43_070_000},
            ]
        )
        .title("Position"),
        y=gs.Y("score:Q").title("Score"),
    )
    .properties(assembly="hg38")
)


# display-controls-basic-start
# Leaving the chart as the final expression uses SVG, PNG, and Inspector.
chart
# display-controls-basic-end


def display_overrides() -> None:
    """Display the chart with temporary control choices."""
    # display-controls-override-start
    # Display once without controls.
    chart.display(controls=False)

    # Display only PNG and SVG, in this order.
    chart.display(controls=["png", "svg"])
    # display-controls-override-end


def inspector_widget() -> gs.JupyterChart:
    """Create a retained widget with only the Inspector control."""
    # display-controls-widget-start
    widget = chart.widget(controls=["inspector"])
    # display-controls-widget-end
    return widget


def canvas_renderer_widget() -> gs.JupyterChart:
    """Create a widget with a GenomeSpy embed option."""
    # display-controls-embed-options-start
    canvas_widget = chart.widget(embed_options={"renderer": "canvas"})
    # display-controls-embed-options-end
    return canvas_widget


def save_examples(directory: Path) -> str:
    """Return HTML and save a control-free copy."""
    # display-controls-output-start
    html = chart.to_html(controls=["svg", "png"])
    chart.save(directory / "variants.html", controls=False)
    # display-controls-output-end
    return html


CHARTS = {"chart": chart}
