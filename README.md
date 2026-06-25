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

## Altair-Style Examples

The public API aims to mirror Altair wherever GenomeSpy's grammar allows it.
For now, example notebooks use Altair's datasets directly:

```python
import genome_spy as alt
from altair.datasets import data

source = data.penguins()

chart = (
    alt.Chart(source)
    .mark_circle()
    .encode(
        alt.X("Flipper Length (mm)").scale(zero=False),
        alt.Y("Body Mass (g)").scale(zero=False, padding=1),
        alt.Size("Beak Depth (mm)").scale(zero=False),
        color="Species",
    )
)

chart
```

The goal is that many simple Altair examples should require only the first
import line to change. GenomeSpy-specific genomic helpers such as
`alt.Locus("chrom", "start")` remain available for locus-scaled genomic axes.

A runnable Altair-style example is available in
`notebooks/altair_penguins_style.ipynb`.

Architecture notes:

- `plans/altair_schema_generation.md`: how Altair generates Python wrappers
  from the Vega-Lite schema and how that maps to the GenomeSpy wrapper plan
- `plans/genomespy_codegen_mapping.md`: how the local GenomeSpy codegen
  scaffold matches and differs from Altair's machinery

Reference implementations and upstream context live in `tmp/`:

- `tmp/altair`: the canonical Vega-Lite Python wrapper
- `tmp/gos`: a Gosling Python wrapper inspired by Altair
- `tmp/vega-lite`: upstream Vega-Lite specification and grammar
- `tmp/gosling.js`: upstream Gosling JavaScript library
- `tmp/genome-spy`: upstream GenomeSpy monorepo
- `tmp/anywidget`: notebook widget infrastructure for rich rendering
