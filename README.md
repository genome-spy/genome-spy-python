# genome-spy-python

`genome-spy-python` is a Python wrapper for
[GenomeSpy](https://github.com/genome-spy/genome-spy).

The goal is to let Python users author GenomeSpy specifications with an
idiomatic Python API, serialize them to valid GenomeSpy JSON, and render them
in notebooks. The public API aims to mirror Altair-style authoring where it
fits GenomeSpy naturally, while still exposing genomics-native features such as
locus-scaled axes and lazy genomic data sources.

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

## Example notebooks

Some notebooks use simple tabular data to show the core authoring model:

```python
import genome_spy as gs

chart = (
    gs.Chart(
        [
            {"x": 1.0, "y": 4.2, "category": "A"},
            {"x": 2.0, "y": 3.1, "category": "B"},
            {"x": 3.0, "y": 5.0, "category": "A"},
        ]
    )
    .mark_circle()
    .encode(
        gs.X("x:Q").scale(zero=False),
        gs.Y("y:Q").scale(zero=False, padding=1),
        color=gs.Color("category:N"),
    )
)

chart
```

GenomeSpy-specific genomic helpers such as
`gs.Locus("chrom", "start")` remain available for locus-scaled genomic axes.
For top-level chart config, prefer the generated fluent methods such as
`chart.configure_view(...)` and `chart.configure_axis(...)`; helper constructors
like `gs.config(...)` and `gs.view_config(...)` remain available when you want
to build schema objects directly.

Additional runnable notebooks live under `notebooks/`.

## Packaged Datasets

The library also ships a small set of real datasets used by the documentation
gallery:

```python
from genome_spy.datasets import available_datasets, load_dataset

gwas = load_dataset("hapmap_gwas", as_format="dataframe")
features = load_dataset("pik3ca_mutations", as_format="json")
```

Tabular packaged datasets load as pandas DataFrames; JSON datasets load as
plain Python objects.

## Schema Generation

Generated schema wrappers are committed to git and shipped with the package,
so normal users installing `genome-spy-python` do not need npm.

Maintainers regenerate wrappers only when updating the pinned GenomeSpy core
version:

```bash
uv run python tools/generate_schema_wrapper.py
```

That command requires `npm` on `PATH`, fetches the version-pinned
`@genome-spy/core` package temporarily, writes `src/genome_spy/schema/`, and
then updates the generated schema package in-place.
