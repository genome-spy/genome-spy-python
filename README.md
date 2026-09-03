<p align="center">
  <img src="docs/_static/snaketie.svg" width="180" alt="GenomeSpy for Python logo">
</p>

<h1 align="center">genome-spy-python</h1>

`genome-spy-python` is a Python interface for
<a href="https://genomespy.app/" target="_blank" rel="noopener noreferrer">GenomeSpy</a>,
a grammar for interactive and scalable genomic visualization. It lets Python
users build GenomeSpy specifications with a declarative, fluent API, serialize
them to JSON, and display them in Jupyter or Marimo notebooks.

Read the [documentation](https://genomespy.app/genome-spy-python/) for the
getting-started guide, user guide, examples, and API reference.

<a href="https://altair-viz.github.io/" target="_blank" rel="noopener noreferrer">Altair</a>
is the project's main source of inspiration. This codebase follows Altair's
approach of combining schema-backed specification objects with a small
handwritten Python API for marks, encodings, composition, and rendering. It
adapts that model to GenomeSpy's genomics-native grammar: locus scales, genomic
data sources, and coordinated genomic views.

The project is under active development. The current focus is the reusable
GenomeSpy Core grammar and notebook rendering; GenomeSpy App-specific features
will come later.

## Installation

The package requires Python 3.11 or newer.

From PyPI:

```bash
pip install genome-spy-python
```

From source:

```bash
pip install uv
git clone https://github.com/genome-spy/genome-spy-python.git
cd genome-spy-python
uv sync
```

For efficient dataframe transport:

```bash
pip install "genome-spy-python[arrow]"
```

See [creating and updating charts in notebooks](docs/user-guide/notebooks.md)
for supported tables and live updates.

See the [getting-started guide](docs/getting-started.md) for the first example.

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

For reactive Jupyter or Marimo notebooks, create a widget with an explicitly
named dataset and replace that dataset as inputs change. The browser keeps the
existing GenomeSpy instance, so view state such as zoom is preserved.

```python
chart = (
    gs.Chart(data={"name": "table"}, datasets={"table": []})
    .mark_point()
    .encode(x="x:Q", y="y:Q")
)
view = chart.widget()

view.set_dataset("table", updated_dataframe)
```

See [creating and updating charts in notebooks](docs/user-guide/notebooks.md)
for the Marimo pattern.

## Contributing

Contributions are welcome. See [CONTRIBUTING.md](CONTRIBUTING.md) for development
setup, testing, code generation, documentation, gallery, and pull-request
guidelines.

## References

- <a href="https://genomespy.app/" target="_blank" rel="noopener noreferrer">GenomeSpy</a>
  — the upstream visualization grammar and JavaScript renderer.
- <a href="https://altair-viz.github.io/" target="_blank" rel="noopener noreferrer">Altair</a>
  — a schema-wrapper design reference.
- <a href="https://gosling-lang.org/" target="_blank" rel="noopener noreferrer">Gos</a>
  — a related grammar and Python-wrapper design reference for
  genomics visualization.

Portions of the schema-wrapper implementation and selected tests are adapted
from Altair under its BSD-3-Clause license. See
[Third-party notices](THIRD_PARTY_NOTICES.md) for the exact sources and license.
