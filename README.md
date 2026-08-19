# genome-spy-python

`genome-spy-python` is a Python interface for [GenomeSpy], a grammar for
interactive and scalable genomic visualization. It lets Python users build
GenomeSpy specifications with a declarative, fluent API, serialize them to
JSON, and display them in Jupyter notebooks.

[Altair] is the project's main source of inspiration. This codebase follows
Altair's approach of combining schema-backed specification objects with a small
handwritten Python API for marks, encodings, composition, and rendering. It
adapts that model to GenomeSpy's genomics-native grammar: locus scales, genomic
data sources, and coordinated genomic views.

The project is under active development. The current focus is the reusable
GenomeSpy Core grammar and notebook rendering; GenomeSpy App-specific features
will come later.

## Installation

The package requires Python 3.11 or newer. Until a package release is
published, install it from source with [uv]:

```bash
git clone https://github.com/genome-spy/genome-spy-python.git
cd genome-spy-python
uv sync
```

For dataframe-backed charts using Arrow transport, install the optional extra:

```bash
uv sync --extra arrow
```

## Examples

```python
import genome_spy as gs

chart = (
    gs.Chart(
        [
            {"x": 1, "y": 4, "group": "A"},
            {"x": 2, "y": 3, "group": "B"},
            {"x": 3, "y": 5, "group": "A"},
        ]
    )
    .mark_point(size=80)
    .encode(
        x="x:Q",
        y="y:Q",
        color="group:N",
    )
)

chart
```

GenomeSpy also has locus-scaled axes for genomic coordinates. This small
example renders intervals along a region of chromosome 1:

```python
import genome_spy as gs

intervals = [
    {"chrom": "chr1", "start": 100, "end": 220, "name": "gene A"},
    {"chrom": "chr1", "start": 280, "end": 420, "name": "gene B"},
]

chart = (
    gs.Chart(intervals)
    .mark_rect()
    .encode(
        x=gs.Locus("chrom", "start"),
        x2="end:Q",
        y="name:N",
        color="name:N",
    )
)

chart
```

Charts can be serialized to a portable GenomeSpy specification or standalone
HTML:

```python
chart.to_json()
chart.save("intervals.html")
```

### Update data without recreating the chart

For reactive notebooks, create a widget with an explicitly named dataset and
replace that dataset as inputs change. The browser keeps the existing
GenomeSpy instance, so view state such as zoom is preserved.

```python
chart = gs.Chart(data={"name": "table"}, datasets={"table": []})
view = chart.widget()

view.set_dataset("table", updated_dataframe)
```

Install the Arrow extra when updating from Polars, pandas, or PyArrow tables:

```bash
uv sync --extra arrow
```

## Contributing

Contributions are welcome. Set up the repository with its development and
documentation dependencies, then run the checks before opening a pull request:

```bash
uv sync --group dev --group docs
uv run pytest tests/ -x
uv run ruff check .
uv run ruff format --check .
uv run mypy src/
```

The source lives in `src/genome_spy/`, tests are in `tests/`, and documentation
examples are in `docs/examples/`. Generated schema wrappers are committed; only
regenerate them when updating the pinned GenomeSpy Core version:

```bash
uv run python tools/generate_schema_wrapper.py
```

### Regenerate the API reference index

`docs/api.md` lists every public object as an `autosummary` entry and is
generated from `genome_spy.__all__`. Regenerate it after changing the public
API:

```bash
uv run python tools/generate_api_docs.py
```

Sphinx writes one page per object into the ignored `docs/generated/` directory
during the build.

### Build and preview the documentation

Build the HTML documentation with:

```bash
uv run sphinx-build -b html -W --keep-going docs docs/_build/html
```

To view it in a browser, build and serve the output, then open
<http://localhost:8000>:

```bash
uv run sphinx-build -b html docs docs/_build/html
cd docs/_build/html && python3 -m http.server
```

NOTE: The live examples load the pinned GenomeSpy JavaScript bundle from the
CDN, so an internet connection is needed when viewing interactive charts.
Gallery cards require manually reviewed PNG thumbnails to exist before the
build.

### Work on examples

Documentation examples live under `docs/examples/` and are the source of truth
for the generated gallery. An example may have an optional Markdown companion
with the same stem, such as `bam_read_alignments.py` and
`bam_read_alignments.md`. The companion is rendered between the live chart and
its Python source and is the place for interpretation, data provenance,
disclaimers, and links to the corresponding official GenomeSpy example. Add or
update an example there, then rebuild the documentation and run the gallery
tests:

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

## References

- [GenomeSpy] — the upstream visualization grammar and JavaScript renderer.
- [Altair] — the primary design inspiration for this Python API.
- [Gos] — a related grammar and Python-wrapper design reference for
  genomics visualization.

[Altair]: https://altair-viz.github.io/
[GenomeSpy]: https://genome-spy.org/
[Gos]: https://gosling-lang.org/
[uv]: https://docs.astral.sh/uv/
