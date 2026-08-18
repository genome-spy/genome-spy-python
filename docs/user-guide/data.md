# Data and chart inputs

GenomeSpy works with tabular data: rows are **records**, and columns are named
**fields**. Encodings refer to those field names when they assign values to
position, color, size, or another visual channel.

## Records and fields

A list of dictionaries is the smallest useful input. Each dictionary below is
one observation with the same three fields:

```{literalinclude} ../tutorials/data_inputs.py
:language: python
:start-after: data-inputs-records-start
:end-before: data-inputs-records-end
```

Pass the records as the first argument to `Chart`:

```{literalinclude} ../tutorials/data_inputs.py
:language: python
:start-after: data-inputs-inline-chart-start
:end-before: data-inputs-inline-chart-end
```

```{genomespy-chart} data_inputs:inline_chart
:height: 260
:title: Six measurements provided as inline Python records
```

The chart stores these rows as inline `data.values` in the generated GenomeSpy
specification. Inline data is a good fit for examples and small tables because
the specification remains self-contained. The GenomeSpy documentation describes
this and the other eager sources in
[inline data](https://genomespy.app/docs/grammar/data/eager/#inline-data).

## DataFrames and Arrow tables

`Chart` also accepts these table objects directly:

- pandas `DataFrame`;
- Polars `DataFrame`;
- PyArrow `Table` and `RecordBatch`.

Use the same chart construction for any of them: `gs.Chart(frame)`. GenomeSpy
uses column names as fields. A pandas index is not a field, so call
`frame.reset_index()` first when an index contains values needed by the chart.

When a supported table is displayed in a notebook, the renderer uses Arrow IPC
transport when available. `chart.to_dict()` still produces ordinary
JSON-compatible records. This distinction changes transport efficiency, not
the chart grammar.

The grammar is easiest to use with **long-form data**, where one row represents
one observation and categories such as `sample` are stored as values in a
field. If category names are spread across several columns, reshape the table
before constructing the chart or use a suitable GenomeSpy transform.

## Load a URL in the browser

For a CSV, TSV, JSON, or another eager file source, use `gs.Data` with a URL.
The format can often be inferred from the filename, but an explicit format
makes the intended parsing clear:

```{literalinclude} ../tutorials/data_inputs.py
:language: python
:start-after: data-inputs-url-start
:end-before: data-inputs-url-end
```

The URL is loaded by the browser that renders GenomeSpy, not by Python. It must
therefore be reachable from that browser and permit cross-origin access when it
uses another domain. A relative URL is resolved against the page containing the
visualization; it is not automatically resolved against the Python working
directory.

URL data is useful when embedding the rows would make the specification too
large. Indexed genomic formats use a separate lazy-loading API described later
in the genomic data guide.

The GenomeSpy documentation lists the supported
[tabular formats](https://genomespy.app/docs/grammar/data/eager/#tabular-formats)
and their parsing options under
[URL data](https://genomespy.app/docs/grammar/data/eager/#url-data).

## Inherit data in a composed view

Data declared on a parent view is available to its children. This avoids
repeating the same source when several layers use the same rows:

```{literalinclude} ../tutorials/data_inputs.py
:language: python
:start-after: data-inputs-inheritance-start
:end-before: data-inputs-inheritance-end
```

```{genomespy-chart} data_inputs:inherited_chart
:height: 260
:title: Points and labels inheriting one parent dataset
```

Here, neither child chart declares data. The layered parent owns one copy of
`measurements`, and both the point and text marks read it.

## Prepare in Python or transform in the chart?

Prepare data in Python when the work is independent of the visualization—for
example, validating identifiers, reshaping a wide table, or calculating a
statistical result. This keeps analysis explicit and testable.

Use a GenomeSpy transform when the operation belongs to the visualization,
such as filtering visible rows, deriving a label, aggregating marks, or reacting
to an interactive parameter. Transforms run in the browser before marks are
drawn and are covered in the transforms guide.
