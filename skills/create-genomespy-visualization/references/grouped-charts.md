# Grouped charts, matrices, and distributions

Read this for grouped summaries, matrices, distribution shapes, and attached
clustering trees. Start with [table-chart.md](table-chart.md) for a runnable
chart and the basic reference-fidelity and color guidance.

## Prepared summaries and variable mark size

For grouped summaries, establish the aggregation, threshold, denominator,
missing-value handling, and whether zeros are included before chart authoring.
Check a few summaries against the underlying observations. Distinguish an empty
group from a valid zero result, and keep fractions versus percentages explicit.

Treat area, radius, and diameter as different quantities. Preserve any clipping,
minimum/maximum area, exponent, and unit conversion in the reference mapping.
When a prepared table contains display areas, use an explicit linear identity
mapping to avoid applying another size transform. Keep the original summary
values in tooltips and explain the size mapping in its guide.
Check guide symbols at representative values against the plotted area mapping,
including exponent, clipping, and unit conversion. Color guides must share the
plot's normalization and palette, rather than merely resembling them visually.

Verify first/last category positions in the browser. A reversed domain array
alone may not establish the intended visual direction; use the supported scale
`reverse` setting when needed, and check a known row/column against its label.

## Rectangular matrices and normalized summaries

Record whether normalization occurs before or after aggregation, and whether it
uses the entire table, each row, or each column. These choices change the meaning
of color. For independently normalized rows or columns, explain the scope in the
guide: equal colors need not mean equal original values. Define constant-range
behavior explicitly instead of silently dividing by zero.

Validate category pairs and uniqueness before rendering a matrix. Distinguish a
missing cell from an observed zero, and preserve explicit row and column orders.
For contiguous cells, use band scales with zero inner and outer padding; verify
cell boundaries, first/last labels, and any reference borders in the browser.
Keep the full labelled chart beside the reference as well as the registered
plot-area overlay. Ink-coverage overlays reveal geometry differences but do not
establish numeric or RGB equality; check those separately.

For observation-level heatmaps, preserve observation IDs and within-group order;
do not substitute group means. Align category strips, group-boundary rules, and
group labels on the same positional scale. Group labels belong at the midpoint
of their actual row spans, not on equal-width categorical bands when group sizes
differ. Constant positional `value` encodings use normalized view coordinates
(for example, `gs.value(1)` is the far edge), not pixel offsets.

If rows or columns are narrower than one display pixel, image resampling and
rectangle rasterization can show different stripes despite identical records and
lookup colors. Record the reference interpolation, intended display dimensions,
and pixels per cell. Diagnose ordering and color separately from sampling; do not
change values or silently average rows to make screenshots agree.

For an attached clustering tree, freeze the clustering input representation,
aggregation, distance metric, linkage method, and leaf order. The clustering input
may differ from the values shown in the chart; explain that distinction. Apply
one permutation consistently to observations, labels, category colors, and tree
leaves. Anchor leaves at actual group-span midpoints when group sizes differ;
equally spaced leaves would misrepresent their alignment with observation rows.
For a chart with one summary row per group, align one leaf with each categorical
band instead; do not weight leaf spacing by the number of source observations.
Preserve the chart's outer padding and category-slot geometry in the tree layout.
Use the same positional domain and direction for the chart and tree, and validate
leaf endpoints against known groups. Include the tree in the registered comparison
area as well as checking the chart values. A correct-looking tree alone does not
verify clustering or row alignment.
When matching a reference, check pixel-center versus cell-boundary conventions
and any half-cell offsets in its annotations. Preserve and disclose a demonstrated
offset instead of silently shifting the tree to satisfy an assumed convention.

## Distribution shapes without a native mark

Check the installed mark set before promising a specialized chart. When a filled
shape is unavailable, a bounded prototype can use prepared geometry and supported
primitives. For example, densely spaced rule spans can fill a simple density
polygon, with rule segments tracing its boundary. This is a sampled workaround,
not a native area mark: state its resolution, mark count, and zoom/resizing limits.
Check coverage and outline agreement at the intended display size; sparse spans
can leave gaps or distort narrow peaks. Avoid adding a public API solely for a
single recreation.
When layers use different color fields or lookup rules, resolve their color
scales independently; automatic scale sharing can silently change fills or
outlines even though each layer's specification validates.

For density plots, freeze the source observations, bandwidth, evaluation grid,
tail extension, and width normalization. Decide explicitly how constant or tiny
groups render. Separate distribution width from sample count and identify the
statistic used for color. Preserve per-panel value ranges and disclose independent
scales. Keep preparation reproducible and verify it separately from rendering;
replaying a reference's extracted geometry alone does not validate the estimator.

For filled observation tracks, distinguish continuous interpolation from bars or
step interpolation; these produce different envelopes from the same values.
Keep series/category breaks explicit so interpolation does not bridge unrelated
groups. Freeze the baseline and each panel's vertical range, retain the original
observations separately from sampled geometry, and check interpolated samples
against them. Color may identify the group while height carries the measurement;
the guide should explain both roles. State when track heights use independent
scales and cannot be compared directly across panels.

Frontend styling has limits beyond schema validation. In particular, test dash
patterns in the browser; fractional dash lengths may serialize successfully but
be rejected by the renderer. Use a supported pattern and disclose any visible
difference from the reference.
