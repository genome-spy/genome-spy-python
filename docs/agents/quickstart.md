# Agent quickstart: a table to an interactive chart

Start with
[the agent documentation index](https://genomespy.app/genome-spy-python/llms.txt)
for task-specific Markdown pages. See [skill installation](skill-distribution.md)
for discovery, packaging, and updates.

Use this workflow to map a prepared table to a chart, validate its specification,
and deliver HTML or notebook output. It requires Python 3.11 or newer and
`genome-spy-python`. Plain records need no dataframe dependency; pandas, Polars,
and PyArrow inputs require the package's `arrow` extra. AnnData projection also
requires its `anndata` extra.

Before writing a new chart, consult [the gallery catalog](gallery.md) for a
related working example. Reuse its chart structure and rendering path, adapting
the data and labels for the requested comparison.

## Inspect before encoding

For a local table, inspect field names, types, a small sample, missing/nonfinite
values, relevant ranges, and category order. Establish the comparison and units.
Avoid printing an entire dataset to the agent context. When missing values need
filtering, report which rule was applied and how many rows it removed. Do not
let a failed load produce an apparently successful empty chart.

The example below uses six fictional prepared records. `depth` is read depth,
`score` is a supplied score between zero and one, and `group` is an unordered
category. No statistical analysis or browser transform is needed.

## Complete runnable example

Run this in the environment that will author the chart. The script writes files
into its current directory; choose an appropriate output directory for user work.

```python
from pathlib import Path

import genome_spy as gs

rows = [
    {"id": "r1", "depth": 18, "score": 0.20, "group": "control"},
    {"id": "r2", "depth": 32, "score": 0.55, "group": "control"},
    {"id": "r3", "depth": 47, "score": 0.42, "group": "control"},
    {"id": "r4", "depth": 25, "score": 0.35, "group": "treated"},
    {"id": "r5", "depth": 51, "score": 0.82, "group": "treated"},
    {"id": "r6", "depth": 68, "score": 0.70, "group": "treated"},
]

chart = (
    gs.Chart(rows)
    .mark_point(filled=True, size=90, opacity=0.85)
    .encode(
        x=gs.X("depth:Q").title("Read depth"),
        y=gs.Y("score:Q").scale(domain=[0, 1]).title("Supplied score"),
        color=gs.Color("group:N")
        .scale(domain=["control", "treated"], range=["#4c78a8", "#f58518"])
        .legend(title="Group"),
        tooltip=["id:N", "depth:Q", "score:Q", "group:N"],
    )
    .properties(width=480, height=320, title="Score versus read depth")
)

# Default validation checks the specification, not the rendered picture.
spec = chart.to_dict()
chart.save(Path("table-chart.json"))
chart.save(Path("table-chart.html"), inline=True)
```

`Q` means quantitative, `N` nominal, and `O` ordinal. Here nominal group color
has an explicit domain and range, keeping its mapping stable if rows change.
The score domain follows the supplied score definition; do not copy `[0, 1]`
for a field with different meaning. The Python API returns new chart objects
when chaining authoring methods.

HTML includes the inline records and, with `inline=True`, the packaged rendering
runtime. It remains interactive without Python. Remote dataset URLs still need
network access. JSON contains the specification and data references, not a
rendered chart or a live Python connection.

## Replace the records with a CSV or dataframe

With pandas and `genome-spy-python[arrow]` installed:

```python
import pandas as pd

frame = pd.read_csv("measurements.csv")
# Inspect dtypes, a bounded sample, missing values, and numeric ranges first.
chart_from_csv = chart.properties(data=frame)
chart_from_csv.to_dict()
chart_from_csv.save("measurements.html", inline=True)
```

This snippet continues the complete example and expects the same four fields.
CSV types and meanings must be checked; numeric-looking strings are not evidence
that parsing succeeded. If a pandas index contains useful IDs, use
`reset_index()` and encode the resulting column. For another schema, adapt
encodings and domains as well as the data.

## Notebook output

Leave `chart` as the last expression in a cell. To explicitly use the packaged
runtime, call `chart.display(inline=True)`. Keep `view = chart.widget(inline=True)`
and display `view` when a retained widget is needed. Merely constructing a widget
or executing a notebook does not verify that its frontend displayed the chart.

## Verify the delivered chart

- Specification: expected rows, field references, types, color mapping, and domains.
- Rendering: six points, readable axes/title, and both legend categories for this
  fixture. A visible canvas is necessary but insufficient.
- Hover: `r5` shows depth 51, score 0.82, and group treated.
- Runtime: no relevant page errors or failed resources. Confirm the intended
  output file, not an older chart at the same location.

Use browser inspection and a screenshot when available. If unavailable, report
that serialization/export passed but visual and hover checks remain unverified.
Deliver the Python source and HTML (or requested notebook), and state any
filtering, derived values, sampling, or verification limitations.

When matching an existing chart, compare equal-sized plot areas side by side.
An overlay should use verified plot boundaries and no fitted geometric warp.
Check positions separately from the mark footprint: the same numeric size can
produce different diameters because libraries use different units or normalized
marker shapes. Stroke and anti-aliasing also affect apparent point density.

Use a common capture path for rendered-color comparisons. Prefer lossless images
with known profiles. If a screenshot has no color profile or is compressed,
calibrate with large flat color controls in the same browser, sample interiors,
and report tolerances. Raw RGB differences between a screenshot and a native
export can reflect capture effects rather than an incorrect palette.

## Adapting an existing scatter plot

An existing scatter plot is another table-chart input: two coordinate columns
plus a category or quantitative field. Preserve those values and their source.
Choose quantitative positional encodings with `zero=False`; preserve geometry
by matching the reference plot-area dimensions and axis directions. For equal
coordinate units, use `height = width * y_span / x_span` and explicit domains
with `nice=False`. A square panel alone does not ensure equal units. Preserve
automatic aspect when the reference uses it; do not impose equal aspect silently.
Use nominal color for categories and quantitative color for measurements. Preserve
the reference palette, clipping, and observation draw order when they matter.
For continuous color, also preserve normalization, palette direction, and
interpolation semantics. Sorting by the same value does not establish identical
draw order among ties; overlapping marks may require preserving the actual
reference order. A discrete color lookup and continuous interpolation can differ
slightly even when they share the same palette endpoints.
For an exact discrete mapping, verify the lookup rule and arithmetic precision
against supplied values and bin-boundary cases. Prepared explicit colors with
a verified ordinal lookup can avoid interpolation when needed. Keep original
measurements in tooltips and supply a truthful quantitative guide if the automatic
legend is no longer applicable. Confirm browser rendering as well as serialization.

Freeze the exact reference call, package version, data, category order, and
palette before recreating it. Set point `fillOpacity`, opacity, and stroke
explicitly when matching appearance. Keep data preparation explicit. A similar
packaged dataset is not an exact substitute for the user's input.

Legend placement and titles can be set with the encoding's `.legend(...)`.
Legend fonts and spacing use chart configuration, for example:

```python
chart = chart.configure_legend(labelFontSize=13, titleFontSize=13, labelLimit=400)
```

This snippet continues the complete example. `labelFontSize` is not a keyword
of `gs.Color(...).legend(...)` in this version. For unexpected keywords, inspect
the installed method signature before retrying.

The public `genome_spy.anndata.from_anndata` helper projects selected `obs`
fields, `X` gene columns, and zero-based `obsm` components into a pandas snapshot.
It does not select `.raw` or a layer. Resolve the intended expression source
explicitly before using this helper; another renderer may use different defaults.

For advanced options, consult the current [API reference](https://genomespy.app/genome-spy-python/api.html),
[data inputs](https://genomespy.app/genome-spy-python/user-guide/data.html),
[scales](https://genomespy.app/genome-spy-python/user-guide/scales-axes-legends.html),
and [serialization](https://genomespy.app/genome-spy-python/user-guide/serialization.html).
Check `gs.__version__` before using version-dependent details. Prefer matching
local documentation and installed signatures when online docs differ.

## Rendering and export failures

For a table of grouped summaries, verify the aggregation and denominator before
encoding. Preserve thresholds, zero/missing-value treatment, and fraction versus
percentage units. Variable mark size may use a nonlinear area mapping; do not
confuse area with radius or apply a second transform to prepared display areas.
Check category direction with known first/last records in the browser rather
than relying solely on serialized domain order.

For a blank chart, inspect browser errors/resources and field/domain definitions
even when `to_dict()` succeeds. Keep validation enabled. Use a supported preview
mechanism if browser tools cannot open files. Any local HTTP preview should bind
loopback and serve only the output directory.

An image-download failure does not establish a chart-rendering failure. Preserve
HTML, use a browser screenshot when available, and report which check failed.
Use bounded waits. If tools cannot hover a known record, record that limitation
instead of treating a click or a tooltip declaration as a successful hover test.
