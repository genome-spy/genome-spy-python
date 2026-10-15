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
| Overlay | Use verified plot boundaries and equal dimensions; no fitted warp. Separate position from footprint/opacity. |
| Capture | Use one capture path, preferably lossless with known profiles. Inspect codec and dimensions; measure CSS-to-image pixel ratio. |
| RGB | Sample interiors; use large flat controls for compressed/unprofiled captures. Report tolerance and capture effects. |
| Export | Keep the native export; label diagnostic resampling. HTML success does not prove image export or hover worked. |

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
