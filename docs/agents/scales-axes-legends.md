# Scales, axes, and legends

## Fixed numeric limits and category colors

```python
import genome_spy as gs

rows = [{"x": 1, "y": 2, "group": "A"}, {"x": 3, "y": 1, "group": "B"}]
chart = (
    gs.Chart(rows).mark_point(filled=True)
    .encode(
        x=gs.X("x:Q").scale(domain=[0, 4], nice=False).axis(title="x"),
        y=gs.Y("y:Q").scale(domain=[1, 2], zero=False, nice=False).axis(title="y"),
        color=gs.Color("group:N")
        .scale(domain=["A", "B"], range=["#1f77b4", "#ff7f0e"])
        .legend(title="Group", orient="right"),
    )
    .configure_legend(labelFontSize=13, titleFontSize=13, labelLimit=300)
)
chart.to_dict()
```

Keep category domain/range paired. For fixed numeric limits, use `nice=False`
and disable unwanted zero inclusion. Legend placement/title use `.legend()`;
fonts and spacing use `.configure_legend()`. Inspect installed signatures for
unfamiliar options.

## Quantitative color and area

Prepared summaries; no aggregation is performed here:

```python
import genome_spy as gs

summaries = [
    {"group": "A", "mean": 0.2, "fraction": 0.25},
    {"group": "B", "mean": 0.8, "fraction": 0.75},
]
summary = (
    gs.Chart(summaries).mark_point(filled=True)
    .encode(
        x=gs.X("group:N").scale(type="band", domain=["A", "B"]),
        color=gs.Color("mean:Q")
        .scale(domain=[0, 1], scheme="blues", nice=False, clamp=True)
        .legend(title="Mean score"),
        size=gs.Size("fraction:Q", format=".0%")
        .scale(type="linear", domain=[0, 1], range=[0, 400], nice=False)
        .legend(title="Fraction", values=[0.25, 0.5, 0.75]),
        tooltip=["group:N", "mean:Q", gs.Tooltip("fraction:Q", format=".0%")],
    )
)
summary.to_dict()
```

Size encodes **area**, not radius or diameter. Keep original units in tooltips
and guides; do not transform prepared display areas a second time. Here 75%
has three times the area of 25%. Use a nonlinear mapping only when the task
explicitly calls for one; do not inherit an example exponent.

## Ordered bands and direction

Continues **Quantitative color and area**. Adds a numeric y position; larger
means appear lower because `reverse=True`.

```python
ordered = summary.encode(
    x=gs.X("group:N").scale(type="band", domain=["A", "B"], padding=0),
    y=gs.Y("mean:Q").scale(domain=[0, 1], reverse=True, nice=False),
)
ordered.to_dict()
```

Check first/last categories in the browser; reversing a domain array alone may
not set the intended direction. Palette names alone do not establish equal RGB
mapping: domain, clipping, normalization, direction and interpolation also matter.
Retain axes and guides in delivered charts, even when overlays crop them away.

See [color and footprint checks](table-chart.md) and [grouped summaries](grouped-charts.md).
