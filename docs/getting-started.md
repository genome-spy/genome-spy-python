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
locus-scaled genomic axes. See the [gallery](gallery/index.md) for genomics-native
examples like the Manhattan plot.

For chart configuration, prefer the generated fluent methods such as
`chart.configure_view(...)` and `chart.configure_axis(...)`. Helper constructors
like `gs.config(...)` and `gs.view_config(...)` still exist when you want to
build schema objects directly.
