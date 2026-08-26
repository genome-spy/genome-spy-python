# Scales, axes, and legends

An encoding says which data field controls a visual channel. A **scale** performs
the conversion from data values to visible values. **Axes** and **legends** are
guides that explain the conversion to the reader.

## Start with automatic defaults

GenomeSpy chooses scales and guides from the channel and data type. This chart
does not configure any of them explicitly:

```{literalinclude} ../tutorials/scales_and_guides.py
:language: python
:start-after: scales-guides-data-start
:end-before: scales-guides-data-end
```

```{literalinclude} ../tutorials/scales_and_guides.py
:language: python
:start-after: scales-guides-automatic-start
:end-before: scales-guides-automatic-end
```

```{genomespy-chart} scales_and_guides:automatic_chart
:height: 310
:title: Automatically generated scales, axes, and legend
```

The quantitative `x` and `y` fields create continuous positional scales and
axes. The nominal `color` field creates a discrete color scale and a legend.
These defaults are usually the best starting point.

## Domain and range

Every scale maps a **domain** to a **range**:

- the domain contains data values, such as times from `1` to `3` or the sample
  names `control` and `treated`;
- the range contains visible outputs, such as pixel positions or the colors
  blue and red.

For an `x` scale, the chart width supplies the pixel range. For a color scale,
the range is a palette. GenomeSpy normally derives the domain from the data and
chooses a suitable range for the channel.

Use `.scale(...)` when the automatic choice does not express the intended
comparison. This example fixes the visible domains, assigns stable group
colors, and makes the horizontal scale zoomable:

```{literalinclude} ../tutorials/scales_and_guides.py
:language: python
:start-after: scales-guides-custom-start
:end-before: scales-guides-custom-end
```

```{genomespy-chart} scales_and_guides:customized_chart
:height: 320
:title: Explicit domains, color range, axes, and legend
```

The color mapping is now deterministic:
`[control, treated]` → `[blue, red]`. This is useful when the same category must
retain the same color across figures. The positional domain represents the
intended analytical window rather than merely the smallest and largest values
present in this small table.

Set only the options that communicate intent. For example,
`.scale(zero=False)` prevents an otherwise useful zero baseline from flattening
variation in measurements far from zero, while leaving the other scale choices
automatic. The GenomeSpy documentation lists the scale types and every scale
option in [scale](https://genomespy.app/docs/grammar/scale/#properties).


## Axes explain positional scales

GenomeSpy creates axes for scaled `x` and `y` field encodings. Axis options
control the guide, not the data mapping:

```python
gs.Y("value:Q").axis(grid=True, tickCount=4).title("Response")
```

Common axis adjustments include:

- `grid=True` to support comparison across the plot;
- `tickCount=4` to request a readable tick density;
- `tickMinStep=1` when fractional steps would be misleading;
- `orient="right"` or `orient="top"` to move the guide;
- `format=".1f"` to format numeric labels.

`tickCount` is a request rather than an exact count. GenomeSpy may choose a
nearby set of round, readable values. A channel `.title(...)` supplies the
default axis title; `.axis(title=...)` can override it when necessary. See
[ticks, labels, and grid lines](https://genomespy.app/docs/grammar/axis/#ticks-labels-and-grid-lines)
for the remaining axis options.

## Zoomable positional scales

Set `zoom=True` on a positional scale to allow its visible domain to change
interactively:

```python
gs.X("time:Q").scale(domain=[0.5, 3.5], zoom=True)
```

Zooming applies to quantitative, index, and locus scales. Nominal and ordinal
positional scales represent categorical data and do not support interactive
zooming, so leave `zoom` unset for them.

The customized chart above uses a zoomable horizontal scale. Zoom
extent and domain transitions are described in
[zooming and panning](https://genomespy.app/docs/grammar/scale/#zooming-and-panning).

## Legends explain visual scales

Color, size, shape, and opacity encodings can produce legends. Use
`.legend(...)` to adjust presentation without changing the scale:

```python
gs.Color("sample:N").legend(
    title="Sample group",
    orient="top",
    direction="horizontal",
)
```

The title states what the categories mean, `orient` selects the side of the
plot, and `direction` controls how entries are arranged within the legend.
Continuous quantitative colors use a gradient legend; discrete categories use
symbols. Symbol and gradient legends, placement, and styling are documented in
[legend](https://genomespy.app/docs/grammar/legend/).

## Remove a guide with `None`

An axis or legend can be redundant when the same information is already clear
from labels, surrounding tracks, or another shared guide:

```{literalinclude} ../tutorials/scales_and_guides.py
:language: python
:start-after: scales-guides-hidden-start
:end-before: scales-guides-hidden-end
```

```{genomespy-chart} scales_and_guides:minimal_chart
:height: 260
:title: The x axis and color legend are hidden
```

`.axis(None)` and `.legend(None)` hide guides but retain their scales. The
points therefore keep their positions and colors. By contrast, `.scale(None)`
disables the scale itself and sends values directly to the visual channel; use
that only when the data already contains suitable visual values.

Removing a guide also removes its explanation. Keep at least one clear label or
guide for every visual distinction the reader must interpret. The GenomeSpy
documentation covers the alternatives in
[disabling legends](https://genomespy.app/docs/grammar/legend/#disabling-legends).
