# Transforms

A **transform** changes the rows that flow from a chart's data source to its
marks. Transforms can remove rows, add fields, summarize groups, or perform
more specialized visualization operations. They run in the browser before the
marks are drawn.

::::{admonition} Transforms leave source data alone
:class: note

Transforms change the rows used by a chart. They do not modify the original
Python data.
::::

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

{py:obj}`~genome_spy.datum` means “the row currently being considered.” In the
example, {py:obj}`~genome_spy.datum`.quality is at least `0.7`, so four rows
remain. Use the following Python syntax to build short conditions:

| Write | Meaning |
| --- | --- |
| {py:obj}`~genome_spy.datum`.quality | Read the `quality` value from the current row. |
| `>=`, `<`, `==` | Compare values. |
| `&`, `\|` | Both conditions, or either condition. |
| `~` | Reverse a condition. |

For a small calculation inside a condition, use the {py:obj}`~genome_spy.expr`
helpers, such as {py:meth}`~genome_spy.expr.if_`
or {py:meth}`~genome_spy.expr.isValid`.

The GenomeSpy documentation describes the
[expression language](https://genomespy.app/docs/grammar/expressions/) and the
[constants and functions](https://genomespy.app/docs/grammar/expressions/#provided-constants-and-functions)
available inside an expression, as well as the
[filter transform](https://genomespy.app/docs/grammar/transform/filter/) itself.

## Derive a field with a formula

A formula calculates a value and stores it in a new field.
{py:meth}`~genome_spy.TopLevelSpec.transform_calculate` accepts the output field as a keyword:

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

Formula transforms are useful for small visualization-specific calculations:
converting units, constructing labels, calculating interval endpoints, or
deriving a category used only by the chart. See the
[formula transform](https://genomespy.app/docs/grammar/transform/formula/) in
the GenomeSpy documentation.

## Summarize groups

An aggregate transform reduces many rows into summary rows. {py:meth}`~genome_spy.TopLevelSpec.transform_aggregate` uses `groupby` to choose
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
`median`, quartiles, and variance. The
[aggregate transform](https://genomespy.app/docs/grammar/transform/aggregate/)
lists every supported operation.

## Convenient Python forms

These shortcuts make common transforms easier to read. They behave like their
GenomeSpy counterparts:

| Method | Use it when you want to… |
| --- | --- |
| {py:meth}`~genome_spy.TopLevelSpec.transform_calculate` | add one or more calculated columns. |
| {py:meth}`~genome_spy.TopLevelSpec.transform_flatten` | turn values nested in a list into separate rows. |
| {py:meth}`~genome_spy.TopLevelSpec.transform_sample` | draw a smaller sample of a large table. |

For example, calculations can use output keywords:

```python
chart = chart.transform_calculate(
    doubled=gs.datum.value * 2,
    centered=gs.datum.value - 10,
)
```

Multiple keyword calculations are added in their written order. Use the direct
form when the output name is only known dynamically:

```python
chart = chart.transform_calculate(
    as_=output_name,
    calculate=gs.datum.response * 100,
)
```

The {py:class}`~genome_spy.Chart` API reference lists every available transform
method.

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
