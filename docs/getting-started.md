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

## Altair-style ergonomics

The API mirrors Altair wherever GenomeSpy's grammar allows, so many examples
port by changing only the import:

```python
import genome_spy as alt
from altair.datasets import data

source = data.penguins()

alt.Chart(source).mark_circle().encode(
    alt.X("Flipper Length (mm)").scale(zero=False),
    alt.Y("Body Mass (g)").scale(zero=False),
    color="Species",
)
```

GenomeSpy-specific helpers such as `alt.Locus("chrom", "pos")` give you
locus-scaled genomic axes. See the [gallery](gallery/index.md) for genomics-native
examples like the Manhattan plot.
