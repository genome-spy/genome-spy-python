# Grouped summaries and matrices

Read this for grouped summaries and matrices. Start with
[table-chart.md](table-chart.md) for a runnable chart and the basic reference-fidelity and color guidance.

## Prepared summaries and variable mark size

For grouped summaries, establish the aggregation, threshold, denominator,
missing-value handling, and whether zeros are included before chart authoring.
Check a few summaries against the underlying observations. Distinguish an empty
group from a valid zero result, and keep fractions versus percentages explicit.

Treat area, radius, and diameter as different quantities. Preserve any clipping,
minimum/maximum area, exponent, and unit conversion in the reference mapping.
Prefer encoding the original summary through a supported native scale when it
expresses the reference mapping, so the attached guide retains the original units.
Check the equation at endpoints and intermediate values: a native power scale
and a power applied after normalization need not agree for nonzero domain minima.
If encoding prepared display areas, use an explicit linear identity mapping to
avoid applying another size transform. Keep the original summary values in
tooltips and explain the size mapping in its guide. Format fractions as percentages
on the channel definition when needed; guide geometry and placement belong to
the legend configuration.
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

Validate category pairs and uniqueness before rendering a matrix. Compare them
with the expected row-by-column grid and account for missing cells; do not fill
them with zero unless the data contract requires it. Preserve explicit orders.
For contiguous cells, use band scales with zero inner and outer padding. Also
check borrowed mark offsets or insets: they can introduce gutters despite zero
scale padding. Verify cell boundaries, first/last labels, and reference borders
in the browser.
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
and pixels per cell. Reuse the cell-heatmap pattern's `minHeight=0, minOpacity=1`
when thin rectangles should retain their true extent and remain opaque; verify
these settings in the browser rather than enlarging rows to a pixel minimum.
Check palette agreement with large flat controls when individual cells have no
uncontaminated interior pixels. Diagnose ordering and color separately from
sampling; do not change values or silently average rows to make screenshots agree.

## Supplied order and capability boundaries

Keep a supplied row/column order consistent across the data, labels, annotation
colors, and related panels. Identify how the order was obtained when it affects
interpretation; ordering inputs can differ from the displayed measurements.

A gallery example built from primitives does not make its specialized chart form
native. Check the installed marks, transforms, and public APIs before promising
support. Prefer a maintained example that meets the task. If custom geometry is
explicitly requested, keep preparation and implementation in the task's artifacts,
label the result as custom, and disclose its rendering and interaction limits.
This guide does not provide recipes for unsupported chart forms.
