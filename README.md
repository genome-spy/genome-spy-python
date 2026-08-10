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

Build a simple scatter plot from Python records. In a notebook, evaluate the
last line to display the interactive chart.

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

See the [documentation sources](docs/) for more examples and API reference
material.

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

### Build the documentation

Build the documentation site from the repository root:

```bash
uv run sphinx-build -b html -W --keep-going docs docs/_build/html
```

Preview the result locally with:

```bash
python3 -m http.server 8000 --directory docs/_build/html
```

Then open <http://localhost:8000/>. Interactive examples load the GenomeSpy
JavaScript bundle from a CDN, so viewing them requires an internet connection.

For the project's design and current implementation direction, see the
[`plans/`](plans/) directory.

## References

- [GenomeSpy] — the upstream visualization grammar and JavaScript renderer.
- [Altair] — the primary design inspiration for this Python API.
- [Gosling] — a related grammar and Python-wrapper design reference for
  genomics visualization.

[Altair]: https://altair-viz.github.io/
[GenomeSpy]: https://genome-spy.org/
[Gosling]: https://gosling-lang.org/
[uv]: https://docs.astral.sh/uv/
