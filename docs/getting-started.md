# Getting started

Build a point chart from a Python table, then apply the same grammar to genomic
intervals. The examples use plain Python records, so you do not need pandas or
prior genomics knowledge.

GenomeSpy uses a **declarative** visualization grammar: you describe what the
chart should show, and GenomeSpy determines how to draw it. A chart description
has three central ingredients:

- **data**: the values you want to show;
- a **mark**: the shape used to represent a row, such as a point or rectangle;
- **encodings**: rules that map data fields to visible properties.

This library builds the same specifications that the
[GenomeSpy visualization grammar](https://genomespy.app/docs/grammar/) defines,
so its documentation applies to the charts you write here.

## Install

Install the current version directly from its Git repository in a virtual
environment:

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install "genome-spy-python @ git+https://github.com/genome-spy/genome-spy-python.git"
python -m pip install jupyterlab
jupyter lab
```

On Windows PowerShell, activate the environment with
`.venv\Scripts\Activate.ps1`. Cloning the repository and running `uv sync` is
needed only when developing the library itself.

The examples work in JupyterLab, Jupyter Notebook, VS Code notebooks, and
Marimo. Notebook rendering loads the pinned GenomeSpy JavaScript bundle from a
CDN, so the browser needs network access when a chart first appears.

Start a notebook and import the package:

```python
import genome_spy as gs
```

## Start with a small table

This table contains six **records**, represented by Python dictionaries. Each
record is one row. The keys `day`, `value`, and `group` name the table's
**fields**, or columns.

```{literalinclude} tutorials/getting_started.py
:language: python
:start-after: getting-started-data-start
:end-before: getting-started-data-end
```

## Choose a mark

A point mark asks GenomeSpy to draw one point for every record:

```{literalinclude} tutorials/getting_started.py
:language: python
:start-after: getting-started-mark-start
:end-before: getting-started-mark-end
```

Without positional encodings, all six points overlap. An encoding assigns each
point a position.

## Map fields to visual channels

A **channel** is the visual property controlled by an encoding. The `x` channel
controls horizontal position:

```{literalinclude} tutorials/getting_started.py
:language: python
:start-after: getting-started-x-start
:end-before: getting-started-x-end
```

The text `"day:O"` contains a field name and a type code. A data type tells
GenomeSpy how values should behave:

| Code | Type | Use it for |
|---|---|---|
| `Q` | quantitative | Numeric amounts that can be compared mathematically |
| `N` | nominal | Unordered names or categories |
| `O` | ordinal | Values with a meaningful order or sequence |

Day is ordinal because day 1 comes before day 2. The measured value is
quantitative, while the groups are nominal categories:

```{literalinclude} tutorials/getting_started.py
:language: python
:start-after: getting-started-encodings-start
:end-before: getting-started-encodings-end
```

```{genomespy-chart} getting_started:encoded_points
:height: 260
:title: Point chart with day, value, and group encodings
```

The explicit `gs.Y("value", type="quantitative")` form means the same thing as
`gs.Y("value:Q")`. The shorthand is convenient once the type codes are
familiar.

## Adjust scales and guides

A **scale** converts data values into positions, colors, or sizes. An **axis**
is the visible guide for a positional scale, while a **legend** explains a
color, size, or shape scale.

Guide titles label the mappings. Setting `zero=False` lets the vertical scale
focus on the observed values instead of including zero:

```{literalinclude} tutorials/getting_started.py
:language: python
:start-after: getting-started-guides-start
:end-before: getting-started-guides-end
```

```{genomespy-chart} getting_started:measurement_chart
:height: 260
:title: Point chart with customized scale, axis title, and legend
```

## Make a genomic interval track

GenomeSpy extends the same grammar with chromosome-aware positions. A
**genomic interval** describes a span from a start position to an end position
on a chromosome.

The example uses three intervals on chromosome 17:

```{literalinclude} tutorials/getting_started.py
:language: python
:start-after: getting-started-genomic-data-start
:end-before: getting-started-genomic-data-end
```

Use a rectangle mark for each interval. The `x` encoding maps the start, and
`x2` maps the other edge of the rectangle:

```{literalinclude} tutorials/getting_started.py
:language: python
:start-after: getting-started-genomic-chart-start
:end-before: getting-started-genomic-chart-end
```

```{genomespy-chart} getting_started:genomic_track
:height: 190
:title: Three intervals on chromosome 17 in the hg38 assembly
```

`gs.Locus("chrom", "start")` combines a chromosome field and a position field
into a **locus**, meaning a place in the genome. The `hg38` **genome assembly**
supplies the chromosome names, lengths, and order needed by the locus scale.
Setting `zoom=True` lets you zoom and pan along that scale.

These example intervals use zero-based, half-open coordinates: the start is
included and the end is excluded. This is the convention used by formats such
as BED. Other formats may require a coordinate offset, as described in
[genomic coordinates](https://genomespy.app/docs/grammar/genomic-coordinates/).

## Where to go next

- Learn more about [encodings and channels](user-guide/encodings.md).
- Read about [genomic axes and intervals](user-guide/genomic-axes.md).
- Combine linked tracks with [composition](user-guide/composition.md).
- Browse complete applications in the [example gallery](gallery/index.md).
- Use `chart.to_dict()` or `chart.to_json()` when you are ready to inspect the
  generated GenomeSpy specification.
- Consult the [GenomeSpy documentation](https://genomespy.app/docs/grammar/) for
  the complete grammar. This guide teaches a subset; every property it describes
  is available here through the same names.
