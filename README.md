<p align="center">
  <img src="docs/_static/snaketie.svg" width="180" alt="GenomeSpy for Python logo">
</p>

<h1 align="center">genome-spy-python</h1>

<p align="center">
  <a href="https://github.com/genome-spy/genome-spy-python/actions/workflows/ci.yml"><img src="https://github.com/genome-spy/genome-spy-python/actions/workflows/ci.yml/badge.svg?branch=main" alt="CI status"></a>
  <a href="https://pypi.org/project/genome-spy-python/"><img src="https://img.shields.io/pypi/v/genome-spy-python" alt="PyPI version"></a>
  <a href="https://colab.research.google.com/github/genome-spy/genome-spy-python/blob/main/notebooks/brush_linked_genome_tracks.ipynb"><img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open brush example in Colab"></a>
</p>

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

For notebook use, install with Arrow support. This includes PyArrow for
dataframe transport:

```bash
pip install "genome-spy-python[arrow]"
```

See [creating and updating charts in notebooks](docs/user-guide/notebooks.md)
for supported tables and live updates.

See the [getting-started guide](docs/getting-started.md) for the first example.

## Examples

A zoomable Manhattan plot using the bundled HapMap data (requires `pandas`):

```python
import genome_spy as gs
from genome_spy.datasets import load_dataset

chart = (
    # Load data.
    gs.Chart(load_dataset("hapmap_gwas"))
    # Format chromosome names.
    .transform_formula(expr="datum.CHR == 23 ? 'chrX' : 'chr' + datum.CHR", as_="chrom")
    # Calculate −log10 p.
    .transform_formula(expr="-log(datum.P) / log(10)", as_="neglogp")
    # Draw variants.
    .mark_point(size=12)
    # Set positions and colors.
    .encode(
        x=gs.Locus("chrom", "BP").scale(assembly="hg18"),
        y=gs.Y("neglogp:Q").title("−log10 p"),
        color=gs.Color("CHR:N").scale(range=["#5b8fd6", "#8f98a3"]).legend(None),
    )
)
chart
```

![Manhattan plot zooming from the whole genome into an association peak](https://raw.githubusercontent.com/genome-spy/genome-spy-python/a6c724f48d94f86d8d0a8c3200549d7560a88a3c/docs/_static/readme-manhattan.webp)

[Explore the full example and data provenance](https://genomespy.app/genome-spy-python/gallery/manhattan_plot.html).

A sequence logo and aligned sequences with shared horizontal zoom:

```python
import genome_spy as gs

logo = (
    gs.Chart()
    # Count bases at each position.
    .transform_aggregate(groupby=["pos", "sequence"])
    # Handle gaps.
    .transform_formula(expr="datum.sequence == '-' ? null : datum.sequence", as_="base")
    # Stack bases by information content.
    .transform_stack(
        field="count",
        groupby=["pos"],
        offset="information",
        baseField="base",
        as_=["y0", "y1"],
    )
    # Draw logo letters.
    .mark_text(logoLetters=True, fitToBand=True, fontWeight="bold")
    # Set stack bounds.
    .encode(
        y=gs.Y("y0:Q").scale(domain=[0, 2], zoom=False).title("Bits"),
        y2="y1:Q",
        text="base:N",
    )
    .properties(height=100)
)
# Create sequence rows.
rows = gs.Chart().encode(y=gs.Y("identifier:N").scale(zoom=False).axis(None))
# Add base labels.
letters = rows.mark_text(size=11, fitToBand=True, opacity=0.7).encode(
    text="sequence:N", color=gs.value("black")
)
# Layer tiles and labels.
sequences = (rows.mark_rect() + letters).properties(
    height=gs.step(16), viewportHeight=160
)
chart = (
    # Combine panels.
    (logo & sequences)
    # Load data.
    .properties(
        data=gs.Data(
            url="https://data.genomespy.app/sample-data/16SRNA_Deino_87seq.aln",
            format=gs.data_format(type="fasta"),
        )
    )
    # Split sequences into bases.
    .transform_flatten_sequence()
    # Set positions and colors.
    .encode(
        x=gs.X("pos:I").scale(domain=[190, 310], zoom=True),
        color=gs.Color("sequence:N")
        .scale(
            domain=list("ACTGN-"),
            range=["#4FBF45", "#4D96E8", "#E85F78", "#E8B322", "#BDBDBD", "#f5f5f5"],
        )
        .legend(None),
    )
    # Share zoom and colors.
    .resolve_scale(x="shared", color="shared")
)
chart
```

![Sequence logo and aligned sequences zooming across multiple regions](https://raw.githubusercontent.com/genome-spy/genome-spy-python/main/docs/_static/readme-sequence-logo.webp?v=ac64144cdc0f)

Charts can be serialized to a portable GenomeSpy specification or standalone
HTML:

```python
# Export JSON.
chart.to_json()
# Save HTML.
chart.save("chart.html")
```

### Update data without recreating the chart

For reactive Jupyter or Marimo notebooks, create a widget with an explicitly
named dataset and replace that dataset as inputs change. The browser keeps the
existing GenomeSpy instance, so view state such as zoom is preserved.

```python
chart = (
    # Create an empty chart.
    gs.Chart(data={"name": "table"}, datasets={"table": []})
    .mark_point()
    .encode(x="x:Q", y="y:Q")
)
# Show widget.
view = chart.widget()

# Update data.
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
