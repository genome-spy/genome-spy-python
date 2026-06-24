# genome-spy-python

`genome-spy-python` is a Python wrapper for
[GenomeSpy](https://github.com/genome-spy/genome-spy), analogous to how Altair
wraps Vega-Lite.

The goal is to let Python users author GenomeSpy specifications with an
idiomatic Python API, serialize them to valid GenomeSpy JSON, and render them
in notebooks. The project starts with the reusable `@genome-spy/core`
grammar and notebook embedding, then expands toward the richer cohort
application concepts in `@genome-spy/app`.

## Notebook Usage

The current notebook path uses `anywidget` as a thin bridge to GenomeSpy's
JavaScript `embed(...)` API:

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

A runnable example notebook is available at
`notebooks/basic_point_chart.ipynb`.

`chart.widget()` is also available for explicit `anywidget` usage, but plain
`chart` display is the most portable default across notebook frontends.

## Built-in Example Datasets

The package includes a tiny Altair-style datasets interface for tutorials and
tests:

```python
import genome_spy as gs
from genome_spy.datasets import data

chart = (
    gs.Chart(data=data.point_features())
    .mark_point(size=120)
    .encode(
        x=gs.X("pos:Q"),
        y=gs.Y("score:Q"),
        color=gs.Color("category:N"),
    )
)

chart
```

Current datasets:

- `data.point_features()`
- `data.copy_number_segments()`

Dataset examples are available in `notebooks/datasets_point_features.ipynb`
and `notebooks/datasets_copy_number_segments.ipynb`.

Reference implementations and upstream context live in `tmp/`:

- `tmp/altair`: the canonical Vega-Lite Python wrapper
- `tmp/gos`: a Gosling Python wrapper inspired by Altair
- `tmp/vega-lite`: upstream Vega-Lite specification and grammar
- `tmp/gosling.js`: upstream Gosling JavaScript library
- `tmp/genome-spy`: upstream GenomeSpy monorepo
- `tmp/anywidget`: notebook widget infrastructure for rich rendering
