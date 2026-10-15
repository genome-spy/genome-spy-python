# Grouped summaries and matrices

Use prepared summaries. Confirm aggregation, thresholds, denominator, zero/missing
handling, and fraction-versus-percent units before charting.

## Summary points with native guides

```python
import genome_spy as gs

rows = [
    {"group": "A", "mean": 0.3, "fraction": 0.25},
    {"group": "B", "mean": 0.7, "fraction": 0.75},
]
chart = gs.Chart(rows).mark_point(filled=True).encode(
    x=gs.X("group:N").scale(type="band", domain=["A", "B"]),
    color=gs.Color("mean:Q").scale(domain=[0, 1], scheme="blues")
    .legend(title="Mean score"),
    size=gs.Size("fraction:Q", format=".0%")
    .scale(type="linear", domain=[0, 1], range=[0, 400], nice=False)
    .legend(title="Fraction"),
    tooltip=["group:N", "mean:Q", gs.Tooltip("fraction:Q", format=".0%")],
)
chart.to_dict()
```

Use original summaries through native scales. Check area mappings at endpoints
and intermediate values, including clipping, exponent and units. Area, radius
and diameter differ. For prepared display areas, use an explicit linear identity
mapping; do not apply the transform twice. Power-before-normalization and
power-after-normalization differ when the minimum is nonzero.

## Contiguous matrix

Prepared values below are scaled independently within each column:

```python
import genome_spy as gs

cells = [
    {"group": "A", "feature": "one", "scaled_mean": 0.0},
    {"group": "B", "feature": "one", "scaled_mean": 1.0},
    {"group": "A", "feature": "two", "scaled_mean": 1.0},
    {"group": "B", "feature": "two", "scaled_mean": 0.0},
]
matrix = (
    gs.Chart(cells).mark_rect()
    .encode(
        x=gs.X("feature:N").scale(type="band", domain=["one", "two"], padding=0),
        y=gs.Y("group:N").scale(type="band", domain=["A", "B"], padding=0),
        color=gs.Color("scaled_mean:Q")
        .scale(domain=[0, 1], scheme="blues", nice=False)
        .legend(title="Mean scaled within each feature"),
        tooltip=["group:N", "feature:N", "scaled_mean:Q"],
    )
)
matrix.to_dict()
```

| Check | Preserve |
| --- | --- |
| Normalization | Before/after aggregation; whole table, row or column; explicit constant-range behavior. |
| Matrix coverage | Unique category pairs; expected grid; missing cells distinguished from valid zeros. |
| Equal colors | Guide states normalization scope; equal colors may not mean equal original values. |
| Contiguous cells | Zero band padding and no inherited mark insets; check boundaries and first/last labels. |
| Order | One supplied permutation across data, labels, colors and related panels; record its source. |

## Thin observation rows

Continues **Contiguous matrix**. Use these native mark settings when real rows
are thinner than one display pixel; this four-cell fixture is only an API example.

```python
thin_cells = matrix.mark_rect(minHeight=0, minOpacity=1)
thin_cells.to_dict()
```

For observation-level heatmaps, retain IDs and within-group order; do not replace
cells with group means. Share positions with annotation strips and boundaries;
anchor group labels at actual span midpoints when group sizes differ.

Below one pixel per cell, image sampling and rectangle rasterization can differ.
Record dimensions, pixels per cell and reference interpolation. Check ordering
and palette separately, using large flat color controls when cells have no clean
interior pixels. Do not change values or average rows to hide raster differences.

## Supplied order and capability boundaries

Check the installed public API and maintained examples before choosing a path:

| Outcome | Report |
| --- | --- |
| Native support | The documented mark/transform expresses the requested form. |
| Custom composition | Existing primitives assemble the form; this does not establish a native feature. |
| Capability gap | State the missing feature or fidelity limit and offer a supported alternative. |

Custom geometry requires an explicit request. Keep its code in task artifacts
and label rendering/interaction limits; no workaround recipes belong in the
skill or guides.

See [scales and guides](https://genomespy.app/genome-spy-python/agents/scales-axes-legends.md)
and [reference checks](table-chart.md).
