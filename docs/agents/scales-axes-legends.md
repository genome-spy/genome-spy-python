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

Continues **Quantitative color and area**. Put A above B explicitly; setting
`reverse=False` puts A below B instead.

```python
ordered = summary.encode(
    x=gs.X("mean:Q").scale(domain=[0, 1], nice=False).axis(title="Mean score"),
    y=gs.Y("group:N")
    .scale(type="band", domain=["A", "B"], reverse=True, padding=0),
)
ordered.to_dict()
```

Check first/last categories in the browser; preserve the same order in related
panels. For numeric axes, `reverse=True` reverses the numeric direction too.

## Discrete colors for numeric values

Continues **Quantitative color and area**. Equal-width bins retain numeric guide
units; explicit ticks keep a larger palette from crowding its guide.

```python
discrete = summary.encode(
    color=gs.Color("mean:Q", format=".2f")
    .scale(type="quantize", domain=[0, 1], range=["#deebf7", "#9ecae1", "#3182bd"])
    .legend(title="Mean score", values=[0, 0.5, 1], orient="bottom"),
)
discrete.to_dict()
```

Use `quantize` for equal-width bins, not a nominal type for continuous values.
Check bin boundaries, endpoint behavior and palette direction against the task.
Scale options depend on scale type; `quantize` does not need `clamp=True`.
See [panel composition](encodings.md#layers-and-panels) for collected bottom guides.

Palette names alone do not establish equal RGB mapping: domain, normalization,
clipping, direction and interpolation also matter.
Retain axes and guides in delivered charts, even when overlays crop them away.

See [color and footprint checks](table-chart.md) and [grouped summaries](grouped-charts.md).
