# genome-spy-python

`genome-spy-python` is a Python wrapper for
[GenomeSpy](https://github.com/genome-spy/genome-spy).

The goal is to let Python users author GenomeSpy specifications with an
idiomatic Python API, serialize them to valid GenomeSpy JSON, and render them
in notebooks. The public API aims to mirror Altair-style authoring where it
fits GenomeSpy naturally, while still exposing genomics-native features such as
locus-scaled axes and lazy genomic data sources.

## Contributing

### Set up the repository

Install [`uv`](https://docs.astral.sh/uv/getting-started/installation/), then
clone the repository and install the development and documentation dependencies:

```bash
git clone https://github.com/genome-spy/genome-spy-python.git
cd genome-spy-python
uv sync --group dev --group docs
```

The project requires Python 3.11 or newer. The `uv sync` command installs the
package in editable mode, so changes under `src/` are immediately available to
tests, notebooks, and documentation examples.

Run the basic verification suite from the repository root:

```bash
uv run pytest tests/ -x
uv run ruff check .
uv run ruff format --check .
uv run mypy src/
```

To install the repository's pre-commit hooks and run them manually:

```bash
uv run pre-commit install
uv run pre-commit run --all-files
```

### Build and preview the documentation

Build the HTML documentation with:

```bash
uv run sphinx-build -b html -W --keep-going docs docs/_build/html
```

The Sphinx build imports the examples, validates their serialized GenomeSpy
specifications, and generates the gallery pages and downloadable specs. Preview
the result locally with:

```bash
python3 -m http.server 8000 --directory docs/_build/html
```

Then open <http://localhost:8000/> in a browser. The live examples load the
pinned GenomeSpy JavaScript bundle from the CDN, so an internet connection is
needed when viewing interactive charts.

### Render gallery thumbnails

Gallery cards use real chart screenshots when thumbnails are rendered. This is
optional for ordinary documentation builds because the gallery has an SVG
fallback, but it is useful when reviewing visual changes:

```bash
uv run --with playwright playwright install chromium
uv run --with playwright python tools/render_thumbnails.py
```

On Linux CI, the browser installation may also need system dependencies:
`uv run --with playwright playwright install --with-deps chromium`.

### Work on examples and schema wrappers

Documentation examples live under `docs/examples/` and are the source of truth
for the generated gallery. Add or update an example there, then rebuild the
documentation and run the gallery tests:

```bash
uv run pytest tests/test_docs_gallery.py -q
uv run sphinx-build -b html -W --keep-going docs docs/_build/html
```

Generated schema wrappers are committed to the repository. If the pinned
GenomeSpy core version changes, regenerate them with:

```bash
uv run python tools/generate_schema_wrapper.py
```

Schema regeneration requires `npm` on `PATH` and updates the generated schema
package from the pinned `@genome-spy/core` release.

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
to build schema objects directly. Small mapping helpers such as `gs.scales(...)`
and ergonomic builders such as `gs.param(...)` also remain useful where they
keep the visualization code shorter and clearer.

Additional runnable notebooks live under `notebooks/`.

## Packaged Datasets

A small set of datasets used by the documentation examples is available through
`genome_spy.datasets.load_dataset(...)`.

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
