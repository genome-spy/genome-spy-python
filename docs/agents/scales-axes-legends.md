# Scales, axes, and legends

Set explicit category domains and color ranges together to preserve mappings.
For fixed numeric reference limits, use `nice=False` and disable unintended zero
inclusion. Check first/last category positions in the browser: reversing a domain
array alone may not establish direction; use the supported `reverse` setting.

```python
import genome_spy as gs

rows = [{"x": 1, "y": 2, "group": "A"}, {"x": 3, "y": 1, "group": "B"}]
chart = (
    gs.Chart(rows).mark_point(filled=True)
    .encode(
        x=gs.X("x:Q").scale(domain=[0, 4], nice=False).axis(title="x"),
        y=gs.Y("y:Q").axis(title="y"),
        color=gs.Color("group:N")
        .scale(domain=["A", "B"], range=["#1f77b4", "#ff7f0e"])
        .legend(title="Group", orient="right"),
    )
    .configure_legend(labelFontSize=13, titleFontSize=13, labelLimit=300)
)
chart.to_dict()
```

Legend placement/title belong to the channel's `.legend(...)`; font sizes,
spacing, and label limits belong to `.configure_legend(...)`. Inspect installed
signatures before transferring options from another library.

A shared palette name does not guarantee equivalent colors. Preserve domain,
clipping, normalization, palette direction, arithmetic precision, and lookup or
interpolation behavior. Prepared exact color values need a verified identity
lookup and a quantitative guide that preserves their original numeric meaning.

Point area, diameter, and radius are different. Preserve any exponent, minimum,
maximum, and unit conversion; avoid a second transform on prepared display areas.
Guides must use the same mappings as the marks. Retain axes, labels, and color/size
guides in delivered charts, even when diagnostic overlays crop them away.

See [color and footprint checks](table-chart.md) and
[grouped summary and matrix guidance](grouped-charts.md).
