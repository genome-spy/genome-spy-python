# Transforms

A **transform** changes the rows that flow from a chart's data source to its
marks. Transforms can remove rows, add fields, summarize groups, or perform
more specialized visualization operations. They run in the browser before the
marks are drawn.

::::{admonition} Transforms define GenomeSpy's data flow
:class: note

Transform methods define the data flow inside the serialized GenomeSpy
specification. They do not process data in Python: the browser-side GenomeSpy
runtime executes them when it renders or interacts with the visualization.
::::

```{literalinclude} ../tutorials/transforms.py
:language: python
:start-after: transforms-data-start
:end-before: transforms-data-end
```

The original Python data remains unchanged. Each chart below starts with these
six rows and builds a transformation pipeline in its GenomeSpy specification.

## Filter rows

A filter keeps rows for which its predicate is true:

```{literalinclude} ../tutorials/transforms.py
:language: python
:start-after: transforms-filter-start
:end-before: transforms-filter-end
```

```{genomespy-chart} transforms:filtered_chart
:height: 260
:title: Only rows with quality of at least 0.7 reach the marks
```

Inside an expression, `datum` refers to the current row. Thus,
`datum.quality >= 0.7` is evaluated once for every input row. Four rows pass
this filter, so GenomeSpy draws four points.

Transform expressions use GenomeSpy's JavaScript-like expression language,
not Python syntax. Common operators include `&&` for “and”, `||` for “or”, and
`!` for “not”. Keep predicates short; complicated validation and cleaning are
usually clearer in Python.

The GenomeSpy documentation describes the
[expression language](https://genomespy.app/docs/grammar/expressions/) and the
[constants and functions](https://genomespy.app/docs/grammar/expressions/#provided-constants-and-functions)
available inside an expression, as well as the
[filter transform](https://genomespy.app/docs/grammar/transform/filter/) itself.

## Derive a field with a formula

A formula calculates a value and stores it in a new field.
`transform_calculate()` accepts the output field as a keyword:

```{literalinclude} ../tutorials/transforms.py
:language: python
:start-after: transforms-formula-start
:end-before: transforms-formula-end
```

```{genomespy-chart} transforms:formula_chart
:height: 290
:title: Response fractions converted to percentages
```

For the first row, the formula adds `responsePercent=42`. Existing fields such
as `sample`, `group`, and `response` remain available. Encodings and later
transforms can refer to the derived field by name.

`transform_calculate()` authors native GenomeSpy `formula` transforms. The
schema-native `transform_formula(expr=..., as_=...)` method remains available.
Formula transforms are useful for small visualization-specific calculations:
converting units, constructing labels, calculating interval endpoints, or
deriving a category used only by the chart. See the
[formula transform](https://genomespy.app/docs/grammar/transform/formula/) in
the GenomeSpy documentation.

## Summarize groups

An aggregate transform reduces many rows into summary rows. `groupby` chooses
which input rows belong together; `fields`, `ops`, and `as_` are parallel lists
that specify the input fields, aggregate operations, and output names:

```{literalinclude} ../tutorials/transforms.py
:language: python
:start-after: transforms-aggregate-start
:end-before: transforms-aggregate-end
```

```{genomespy-chart} transforms:aggregate_chart
:height: 290
:title: Mean response calculated for each group
```

The six input rows become two output rows, one for `control` and one for
`treated`. Available operations include `count`, `sum`, `min`, `max`, `mean`,
`median`, quartiles, and variance. GenomeSpy Core currently retains a legacy
fieldless count when no fields or operations are supplied, but new code should
not rely on it because the Core behavior may be removed. The
[aggregate transform](https://genomespy.app/docs/grammar/transform/aggregate/)
lists every supported operation.

## Python transform conveniences

Transform methods and their types are generated from GenomeSpy Core's schema.
A few generation rules provide concise Python call shapes without changing the
underlying GenomeSpy grammar:

| Method | Convenience | Serialized transform |
|---|---|---|
| `transform_calculate()` | Direct `as_`/`calculate` strings or output-name keyword expressions | `formula` |
| `transform_flatten()` | Positional fields and output names; `fields=` and `index=` remain available | `flatten` |
| `transform_sample()` | Positional sample size | `sample` |

For example, calculations can use output keywords while still serializing
native GenomeSpy formula transforms:

```python
chart = chart.transform_calculate(
    doubled="datum.value * 2",
    centered="datum.value - 10",
)
```

Multiple keyword calculations are appended in their written order. The direct
form is available when the output name is only known dynamically:

```python
chart = chart.transform_calculate(
    as_=output_name,
    calculate="datum.response * 100",
)
```

Calling `transform_sample()` without a size leaves the property out of the
specification and therefore preserves GenomeSpy Core's current default. Other
transforms use their generated GenomeSpy-native signatures. Operations absent
from GenomeSpy Core are not emulated by the Python wrapper.

## Transform order matters

Transforms run from top to bottom, and each step receives the output of the
previous step. In the aggregate example:

1. `transform_calculate()` adds `responsePercent` to every row.
2. `transform_aggregate()` groups those rows and reads the new field.
3. Encodings read `group` and `meanResponse` from the two summary rows.

Reversing the first two transforms would fail because `responsePercent` would
not exist when the aggregate tried to read it. The serialized `transform` list
preserves the same order as the method chain.

Filtering before an aggregate changes which rows contribute to the summary;
filtering afterward tests the summary rows instead. Choose the order from the
question the visualization should answer.

## Transform in Python or in GenomeSpy?

Prepare data in Python when the operation:

- cleans or validates source data;
- performs statistical analysis;
- joins or reshapes a large table;
- produces a reusable result needed outside the visualization.

Use a GenomeSpy transform when the operation is part of the visual
specification, should run after browser-side data loading, or needs to react to
an interactive parameter. Keeping that boundary clear makes both the analysis
and visualization easier to test.

The [linked genome tracks](../gallery/genome_tracks.md) example chains nine of
them, including pileup, label placement, and coordinate linearization.

GenomeSpy also provides transforms for sorting and stacking, lookups, windows,
genomic coordinates, sequence data, read alignments, and label placement.
Those transforms are introduced by the focused examples that need them; their
complete signatures are available in the [API reference](../api.md), and the
GenomeSpy documentation describes each one in its
[transform reference](https://genomespy.app/docs/grammar/transform/).
