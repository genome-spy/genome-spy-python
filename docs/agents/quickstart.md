# Quickstart

Requires Python 3.11+ and `genome-spy-python`. Plain records need no extras.
Read [llms.txt](https://genomespy.app/genome-spy-python/llms.txt) once, select a
[gallery example](gallery.md) by chart structure, and adapt its public API.

## Create, validate, save

Six fictional measurements; no analysis or browser transforms:

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
spec = chart.to_dict()  # Validates the spec, not the rendered chart.
chart.save(Path("table-chart.json"))
chart.save(Path("table-chart.html"), inline=True)
```

`Q`: quantitative; `N`: nominal; `O`: ordinal. Replace fields, units, domains,
and data together. Authoring methods return new charts; retain their result.
Inline HTML bundles the runtime and inline records, not remote datasets.

## Use a CSV instead

Continues the example; requires pandas and the `arrow` extra. The CSV must have
`id`, `depth`, `score`, and `group` fields with compatible types.

```python
import pandas as pd

frame = pd.read_csv("measurements.csv")
chart_from_csv = chart.properties(data=frame)
chart_from_csv.to_dict()
chart_from_csv.save("measurements.html", inline=True)
```

Inspect types, a bounded sample, missing values, ranges, and order before encoding.
Preserve supplied values; report filtering, sampling, and derived fields.
See [data inputs](data.md) for indexes, remote tables, and AnnData.

## Verify and deliver

Open the HTML: check six points, readable labels, both legend categories, and
relevant page/resource errors. Hover `r5`: depth **51**, score **0.82**, group
**treated**. Confirm the latest artifact loaded. If frontend tools are unavailable,
report visual/hover checks as unverified.

Deliver source and the requested artifact with processing and verification limits.
Use documented native features; a custom composition is not native support for a
specialized chart form. See [capability boundaries](grouped-charts.md#supplied-order-and-capability-boundaries).

| Next task | Guide |
| --- | --- |
| Fields, transforms, layers, panels, surround margins | [Encodings and composition](encodings.md) |
| Color, size, order, guides | [Scales, axes, legends](scales-axes-legends.md) |
| Notebook display, export, recovery | [Rendering](rendering.md) |
| Python callbacks and live chart updates | [Embed API](embed-api.md) |
| Recreate an existing chart | [Reference checks](table-chart.md) |
| Grouped summaries or matrices | [Grouped charts](grouped-charts.md) |
| Install the skill | [Installation](skill-distribution.md) |
