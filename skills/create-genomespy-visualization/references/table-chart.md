# Table charts: minimal fallback and consequential details

For genome-spy-python 0.6.0. Prefer matching installed signatures if versions
differ. Plain records work with the base package; dataframes require its `arrow`
extra. This bundled reference is independent of repository paths and web access.

```python
import genome_spy as gs

rows = [
    {"id": "a", "x": -2.0, "y": 1.0, "group": "A"},
    {"id": "b", "x": 1.0, "y": -1.0, "group": "B"},
    {"id": "c", "x": 3.0, "y": 2.0, "group": "A"},
]
chart = (
    gs.Chart(rows)
    .mark_point(filled=True, size=50, opacity=1, fillOpacity=1, strokeWidth=0)
    .encode(
        x=gs.X("x:Q").scale(zero=False).title("x"),
        y=gs.Y("y:Q").scale(zero=False).title("y"),
        color=gs.Color("group:N")
        .scale(domain=["A", "B"], range=["#1f77b4", "#ff7f0e"])
        .legend(title="Group", orient="right"),
        tooltip=["id:N", "group:N", "x:Q", "y:Q"],
    )
    .properties(width=400, height=300, title="Prepared observations")
    .configure_legend(labelFontSize=13, titleFontSize=13, labelLimit=300)
)
spec = chart.to_dict()
chart.save("observations.html", inline=True)
```

Choose output paths for the task. `chart.save()` writes files; `to_dict()`
validates but does not render. In notebooks display `chart`, or retain and display
`chart.widget(inline=True)`. Inline runtime export does not bundle URL datasets.

## Reference plot fidelity

- Preserve all required IDs, coordinates, categories, and source row order.
  Compare exported records against the prepared source, not just against counts.
  If the reference sorts marks, preserve its actual draw order, including ties;
  overlapping marks can differ even with the same ascending sort key.
- Freeze nominal color domain/range together. Specify fill opacity and stroke
  when matching appearance: renderer defaults and anti-aliasing differ.
- Check rendered point footprints rather than copying numeric mark sizes between
  libraries. Units, device scale, marker shape normalization, and stroke can make
  the same size value look different and change the apparent density of clusters.
- Use `nice=False` with explicit positional domains to preserve reference bounds.
  For a reference plot, match its plot-area width/height ratio and axis directions.
  If equal coordinate units are intended, use
  `height = width * (ymax - ymin) / (xmax - xmin)`. A square panel alone does not
  ensure equal units, and an automatic-aspect reference should not be silently
  changed to equal aspect.
- For multiple panels, freeze each plot area's dimensions separately. Legends
  and colorbars can consume different amounts of space, even in equally sized
  figures. Preserve each panel's geometry when composing existing references;
  an overall figure size does not establish matching plot areas.
- Set channel legend placement/title with `.legend(...)`. Set font sizes,
  spacing, and label limits through `.configure_legend(...)`. Check signatures
  instead of transferring arbitrary Altair/Matplotlib options.
- Tooltips must use actual fields. A pandas index needs `reset_index()` when used
  as a field. Hover a known isolated observation when tools support it; lack of
  hover automation is a verification limitation, not proof of working hover.

Inspect the actual chart for expected geometry, category colors, labels, and
runtime errors. Repair demonstrated failures and record deviations. Screenshot
review complements record/spec checks; neither establishes the other's result.
After regenerating an artifact, confirm that the frontend loaded the new version;
cached embedded views can survive a parent-page reload. Do not judge an edit from
a stale preview.

For close visual recreation, show the reference and output side by side at the
same plot-area dimensions. Crop from verified plot boundaries, excluding legends
and titles, and overlay without fitted warping; otherwise alignment may hide a
scale error. Separate positional agreement from marker size, stroke, and opacity.
Plot-area crops are diagnostics, not complete deliverables. Retain category
labels, meaningful axis titles or units, and size/color guides in the delivered
chart. Use categorical band scales for labelled categories; reserve index scales
for numbered positions where linear zoom and pan are needed.
Derive complete and diagnostic views from the same base. Check that removing
guides leaves records, marks, and scales unchanged; omit optional properties that
do not accept null rather than assuming `None` clears every setting.

Compare rendered colors through a common capture path. Prefer lossless captures
with known color profiles. If screenshots lack profile metadata or use lossy
compression, use large flat color controls in the same browser to assess capture
effects, sample interiors away from edges, and state the tolerance and limitations.
Do not diagnose a palette error solely from raw RGB differences between an export
and a screenshot. Compare each category's mapping as well as visible swatches.
Inspect the actual image codec and dimensions instead of trusting its filename.
Convert browser CSS bounds to image pixels using the measured capture ratio;
native exports may use a different pixel ratio from browser screenshots. Preserve
the original export, and label any resampling used for a diagnostic comparison.

## Continuous color

Resolve the numeric field's source and preparation before encoding: alternate
tables, matrix layers, normalization, and transformations may supply different
values under the same field name. Preserve the supplied values and use `Q`.

Freeze the reference color domain, clipping, palette direction, normalization,
and interpolation. A shared palette name alone does not establish equivalence.
Disable unintended zero inclusion or nicing when using fixed reference limits.
Check endpoint and intermediate colors, including whether the source uses a
discrete lookup table while the output interpolates continuously. State residual
differences rather than treating approximate palette agreement as pixel equality.
When exact discrete mapping matters, preserve the lookup rule, arithmetic
precision, endpoint behavior, and colors. Test actual values and values at and
immediately around bin boundaries. If a native scale cannot express the required
rule, report the fidelity limit.
Custom color-matching code requires an explicit user request and belongs in the
task artifacts, not in this skill's reusable instructions.

For grouped summaries and matrices, read [grouped-charts.md](grouped-charts.md).
