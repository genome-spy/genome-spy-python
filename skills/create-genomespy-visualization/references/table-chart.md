# Table charts and reference checks

Use the installed public API; inspect signatures when versions differ. Plain
records need only the base package; dataframe inputs need the `arrow` extra.

## Runnable baseline

```python
import genome_spy as gs

rows = [
    {"id": "a", "x": -2.0, "y": 1.0, "group": "A"},
    {"id": "b", "x": 1.0, "y": -1.0, "group": "B"},
    {"id": "c", "x": 3.0, "y": 2.0, "group": "A"},
]
chart = (
    gs.Chart(rows).mark_point(filled=True, size=50, opacity=1, fillOpacity=1, strokeWidth=0)
    .encode(
        x=gs.X("x:Q").scale(zero=False).title("x"),
        y=gs.Y("y:Q").scale(zero=False).title("y"),
        color=gs.Color("group:N")
        .scale(domain=["A", "B"], range=["#1f77b4", "#ff7f0e"])
        .legend(title="Group"),
        tooltip=["id:N", "x:Q", "y:Q", "group:N"],
    )
    .properties(width=400, height=300, title="Prepared observations")
    .configure_legend(labelFontSize=13, titleFontSize=13, labelLimit=300)
)
spec = chart.to_dict()
chart.save("observations.html", inline=True)
```

## Equal coordinate units, when required

Continues the baseline. Preserve the reference's automatic aspect if that is its
intended mapping; do not impose equal units silently.

```python
x_domain, y_domain = [-2, 3], [-1, 2]
width = 400
height = width * (y_domain[1] - y_domain[0]) / (x_domain[1] - x_domain[0])
equal_units = chart.encode(
    x=gs.X("x:Q").scale(domain=x_domain, zero=False, nice=False),
    y=gs.Y("y:Q").scale(domain=y_domain, zero=False, nice=False),
).properties(width=width, height=height)
equal_units.to_dict()
```

A square panel alone does not establish equal units. Freeze each panel's plot
size separately; guides can consume different space in equally sized figures.

## Marker units and export DPI

Continues **Runnable baseline**. When a reference size is a squared diameter in
typographic points, convert using the saved image's DPI, not its display DPI:

```python
reference_size_pt2 = 36
export_dpi = 150
image_pixels_per_css_pixel = 1.0  # Reference displayed at its natural image size.
size_css2 = reference_size_pt2 * (export_dpi / 72 / image_pixels_per_css_pixel) ** 2
matched_points = chart.mark_point(
    filled=True, size=size_css2, opacity=1, fillOpacity=1, strokeWidth=0
)
matched_points.to_dict()
```

GenomeSpy point `size` is in squared pixels; nominal diameter is `sqrt(size)`.
This example gives 12.5 CSS pixels. For a measured image diameter, use
`size = (diameter_image_px / image_pixels_per_css_pixel) ** 2` instead.
Confirm the source's size convention; physical circle area differs from diameter
squared. Match stroke/opacity too and verify the rendered footprint. Do not
multiply by device pixel ratio again; the renderer handles that scaling.

## Diagnostic view from the same chart

Continues **Runnable baseline**. Keep the complete chart as the deliverable;
remove guides only for comparison:

```python
encoding = chart.to_dict()["encoding"]
plot_only = chart.encode(
    x=gs.X(encoding["x"]).axis(None),
    y=gs.Y(encoding["y"]).axis(None),
    color=gs.Color(encoding["color"]).legend(None),
).properties(padding=0)
plot_only.to_dict()
```

Check records, marks and scales stayed identical. Omit optional properties that
do not accept null; do not assume `None` clears every setting.

## Fidelity checklist

| Check | Requirement |
| --- | --- |
| Reference | Freeze call, version, data selection, field source, palette, domains, units and category order. |
| Records | Compare IDs/values to source, not just counts; retain actual draw order, including ties. |
| Marks | Match opacity, fill opacity and stroke; measure footprints rather than copying numeric sizes between libraries. |
| Guides | Preserve category/color mappings and original numeric units; retain axes, labels and legends. |
| Render | Inspect actual marks and page/resource errors; confirm the regenerated artifact loaded. |
| Tooltip | Hover a known record when possible. A click or declared tooltip is not a verified hover. |
| Overlay | Use settled layout, verified plot boundaries and equal dimensions; no fitted alignment/warp. Separate position from footprint/opacity. |
| Capture | Use one capture path, preferably lossless with known profiles. Inspect codec and dimensions; measure CSS-to-image pixel ratio. |
| RGB | Sample interiors; use large flat controls for compressed/unprofiled captures. Report tolerance and capture effects. |
| Export | Keep the native export; label diagnostic resampling. HTML success does not prove image export or hover worked. |

## Register plot-area captures

Compare complete charts first. Then use guide-free diagnostic views with the same
records, marks, scales and plot dimensions. Wait for opening animations/layout to
settle; a nonblank canvas alone is insufficient.

For a full-page screenshot, these DOM measurements give a guide-free canvas's
document-space crop. Run in the diagnostic document; a canvas with guides is not
the plot boundary.

```javascript
const canvas = document.querySelector("canvas");
const bounds = canvas.getBoundingClientRect();
const crop = {
  x: bounds.left + window.scrollX,
  y: bounds.top + window.scrollY,
  width: bounds.width,
  height: bounds.height,
};
```

For iframe captures, translate through the frame's measured content origin too.
Convert CSS bounds using the screenshot's image-pixel/CSS-pixel ratio; canvas
backing-store dimensions alone do not establish that ratio. Use the same capture
path for both charts, assert equal crop dimensions and inspect a half-opacity
blend. Keep original crops; do not resize or fit positions to improve alignment.
Image-difference scores diagnose discrepancies; inspect values, orientation,
palette, footprints and rasterization separately before claiming a match.

## Continuous color

Continues **Runnable baseline**; no dependency on the equal-units example.

```python
x_domain = [-2, 3]
continuous = chart.encode(
    color=gs.Color("x:Q")
    .scale(domain=x_domain, scheme="viridis", nice=False, zero=False, clamp=True)
    .legend(title="x"),
)
continuous.to_dict()
```

Preserve measurement source, normalization, clipping, palette direction and
interpolation. Palette endpoints alone do not establish equality. For discrete
lookups, check actual values and bin boundaries, including arithmetic precision.
If a native scale cannot express the required rule, report the fidelity limit;
custom matching requires explicit permission and stays in task-local code.

For summaries and matrices, read [grouped charts](grouped-charts.md).
