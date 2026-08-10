# Getting started

## Install

```bash
pip install genome-spy-python
# or, in this repo:
uv sync --dev
```

The package ships the generated schema wrappers, so normal installation needs no
Node/npm. Notebook rendering pulls the pinned `@genome-spy/core` bundle from a
CDN at display time.

## Your first chart

```python
import genome_spy as gs

chart = (
    gs.Chart(data=[{"x": 1, "y": 2, "category": "A"}])
    .mark_point(size=90)
    .encode(
        x=gs.X("x:Q"),
        y=gs.Y("y:Q"),
        color=gs.Color("category:N"),
    )
)

chart
```

In a Jupyter notebook, displaying `chart` renders a live, interactive GenomeSpy
view. `chart.widget()` returns an explicit `anywidget` instance if you need one.

## Updating a live dataset

For reactive notebooks, declare a named dataset, construct the widget once in a
stable cell, and update that same widget from downstream cells. Supported
dataframes and tables use Arrow IPC automatically:

```python
view = (
    gs.Chart(data={"name": "table"}, datasets={"table": []})
    .mark_point()
    .encode(x="x:Q", y="y:Q")
    .widget()
)
view.set_dataset("table", dataframe)
```

`set_dataset()` keeps the embedded GenomeSpy instance and its interaction state
alive. When the widget has exactly one live dataset, `view.set_data(dataframe)`
is a convenient equivalent.

## Serializing a spec

```python
chart.to_dict()   # Python dict (validated against the GenomeSpy schema)
chart.to_json()   # pretty-printed JSON string
```

## Authoring style

The API keeps the authoring flow compact and composable for tabular charts as
well as genomics-native views:

```python
import genome_spy as gs

gs.Chart(
    [
        {"x": 1.0, "y": 4.2, "category": "A"},
        {"x": 2.0, "y": 3.1, "category": "B"},
        {"x": 3.0, "y": 5.0, "category": "A"},
    ]
).mark_circle().encode(
    gs.X("x:Q").scale(zero=False),
    gs.Y("y:Q").scale(zero=False),
    color=gs.Color("category:N"),
)
```

GenomeSpy-specific helpers such as `gs.Locus("chrom", "pos")` give you
locus-scaled genomic axes. See the [gallery](gallery/index.md) for fuller
genomics examples.

For chart configuration, prefer the generated fluent methods such as
`chart.configure_view(...)` and `chart.configure_axis(...)`. Helper constructors
like `gs.config(...)` and `gs.view_config(...)` still exist when you want to
build schema objects directly. Small mapping or parameter helpers such as
`gs.scales(...)` and `gs.param(...)` also remain available when they keep the
spec clearer.

For direct top-level spec properties, charts also support generated-style
setters such as `chart.with_view(...)`, `chart.with_config(...)`, and
`chart.with_scales(...)`.
