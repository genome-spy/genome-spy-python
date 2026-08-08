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
needed when viewing interactive charts. Gallery cards require manually reviewed
PNG thumbnails to exist before the build.

### Work on examples

Documentation examples live under `docs/examples/` and are the source of truth
for the generated gallery. Add or update an example there, then rebuild the
documentation and run the gallery tests:

```bash
uv run pytest tests/test_docs_gallery.py -q
uv run sphinx-build -b html -W --keep-going docs docs/_build/html
```

### Regenerate schema wrappers

Generated schema wrappers are committed to the repository. Maintainers should
regenerate them when the pinned GenomeSpy core version changes:

```bash
uv run python tools/generate_schema_wrapper.py
```

Schema regeneration requires `npm` on `PATH` and updates the generated schema
package from the pinned `@genome-spy/core` release. See
[Schema Generation](#schema-generation) for local upstream audit modes.

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

Existing GenomeSpy specifications can be validated, wrapped, and rendered
without rewriting them:

```python
chart = gs.TopLevelSpec.from_dict(spec)
```

The loader dispatches unit, layer, multiscale, and concatenated roots, including
template or URL imports nested inside compositions.

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

## Dataframe rendering

When a chart is displayed in a notebook or generated for the documentation
gallery, Polars dataframes are transferred automatically as uncompressed Arrow
IPC. pandas dataframes and PyArrow tables use the same path when the optional
Arrow support is installed:

```bash
pip install "genome-spy-python[arrow]"
```

No manual `arrow://` data source or widget buffer map is needed. Ordinary
Python record lists, and pandas installations without PyArrow, continue to use
inline JSON. `chart.to_dict()`, `chart.to_json()`, and saved specs always
remain JSON-compatible.

GenomeSpy currently decodes IPC into JavaScript row objects, so this is binary
columnar transport rather than zero-copy rendering. Use uncompressed IPC; dates
and timestamps follow GenomeSpy's normal JavaScript conversion behavior, and
integers beyond JavaScript's safe integer range can lose precision.

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
then updates the generated schema package in-place. It also writes a capability
manifest used to verify that generated transforms and root specification
variants remain covered.

To audit a built local GenomeSpy core package without fetching npm, generate
into a separate output directory:

```bash
uv run python tools/generate_schema_wrapper.py \
  --package-dir <path-to-genome-spy>/packages/core \
  --output-dir <audit-output>
```

An explicit schema file can be inspected in the same way:

```bash
uv run python tools/generate_schema_wrapper.py \
  --schema-path <path-to-schema.json> \
  --core-version <schema-version> \
  --output-dir <audit-output> \
  --spec-reference-dir ""
```

The default npm mode remains the release source of truth. Local modes are for
checking unreleased upstream changes before updating the pinned core version.
