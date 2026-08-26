# Display and update charts in notebooks

GenomeSpy charts display through a notebook widget in JupyterLab, Jupyter
Notebook, VS Code notebooks, and Marimo. The browser needs network access when
it first loads the pinned GenomeSpy JavaScript bundle.

## Display a chart

Build a chart normally:

```{literalinclude} ../tutorials/notebooks.py
:language: python
:start-after: notebooks-chart-start
:end-before: notebooks-chart-end
```

Leave the chart as the final expression in a notebook cell to display it:

```{literalinclude} ../tutorials/notebooks.py
:language: python
:start-after: notebooks-implicit-display-start
:end-before: notebooks-implicit-display-end
```

This form is enough when later Python cells do not need to update the displayed
data.

## Keep a widget for updates

Call `.widget()` when the displayed chart must receive new data:

```{literalinclude} ../tutorials/notebooks.py
:language: python
:start-after: notebooks-widget-start
:end-before: notebooks-widget-end
```

Display `view` once and keep the same object alive. Updating it preserves the
mounted GenomeSpy instance, including its current zoom and selections.

The chart uses a named dataset:

```python
data={"name": "measurements"},
datasets={"measurements": initial_rows},
```

`data.name` tells the chart which dataset to read. The root `datasets` mapping
provides its initial rows and gives later updates a stable target. The GenomeSpy
documentation describes this indirection in
[named data](https://genomespy.app/docs/grammar/data/eager/#named-data).

## Replace the named dataset

Use `set_dataset()` to replace its records:

```{literalinclude} ../tutorials/notebooks.py
:language: python
:start-after: notebooks-record-update-start
:end-before: notebooks-record-update-end
```

New rows should retain the fields and value types expected by the chart. For a
widget with exactly one named dataset, `view.set_data(updated_rows,
format="records")` is a shorter equivalent.

Supported pandas, Polars, and PyArrow tables can also be passed directly.
GenomeSpy uses Arrow transport for those tables when available; this affects
transfer efficiency, not the chart definition. See
[Arrow data transport](arrow-transport.md) for installation and supported
inputs.

In a reactive notebook, create and display the widget in a stable cell. Let
dependent cells prepare new rows and call `set_dataset()` on that same object.
Create a new chart only when its fields, marks, encodings, or composition need
to change.

## Use Marimo

Marimo displays the same widget through its anywidget support. Create and wrap
the widget once in a stable cell:

```python
import marimo as mo

view = chart.widget()
chart_widget = mo.ui.anywidget(view)
chart_widget
```

Dependent cells can prepare a new dataframe and update the existing widget:

```python
view.set_dataset("measurements", updated_frame)
```

Keeping the widget in its original cell avoids rebuilding the chart whenever a
Marimo control changes.

See the {py:class}`genome_spy.api.JupyterChart` reference for multiple datasets,
transport options, and method signatures.
