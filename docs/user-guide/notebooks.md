# Charts in notebooks

Create a chart in Python and display it in JupyterLab, Jupyter Notebook,
VS Code notebooks, or Marimo. You can explore it with the mouse without writing
any JavaScript.

## Install for notebooks

Install GenomeSpy in the Python environment your notebook uses:

```sh
pip install genome-spy-python
```

If you use pandas, Polars, or PyArrow tables, also install the optional
`arrow` support:

```sh
pip install "genome-spy-python[arrow]"
```

## Display a chart

Here is a complete example with three measurements:

```python
import genome_spy as gs
```

```{literalinclude} ../tutorials/notebooks.py
:language: python
:start-after: notebooks-chart-start
:end-before: notebooks-chart-end
```

Leave the chart as the last expression in a cell:

```{literalinclude} ../tutorials/notebooks.py
:language: python
:start-after: notebooks-implicit-display-start
:end-before: notebooks-implicit-display-end
```

This is enough to display and explore a chart.

### Create a chart from a dataframe

You can pass a pandas or Polars dataframe directly to `gs.Chart()`. PyArrow
tables and record batches also work. For example, with pandas installed:

```python
import pandas as pd

frame = pd.DataFrame({"sample": ["A", "B"], "value": [2.1, 3.4]})
gs.Chart(frame).mark_point().encode(x="sample:N", y="value:Q")
```

GenomeSpy uses Arrow to send these tables to the displayed chart efficiently.
You do not need to manage that transfer yourself. A pandas index is not a
chart field: use `frame.reset_index()` if you want to plot it.

## Keep a widget for later updates

A *widget* is the displayed chart's connection to Python. Keep it in a variable
when you want a later cell to change the data in that same chart. Continuing
with the measurements chart above:

```{literalinclude} ../tutorials/notebooks.py
:language: python
:start-after: notebooks-widget-start
:end-before: notebooks-widget-end
```

Display `view` once. Update that object rather than creating another chart.

## Update the chart’s data

To update `view`, specify which dataset to replace. The measurements chart
already declares a dataset named `"measurements"` in its `gs.Chart(...)` call:

```python
data={"name": "measurements"},
datasets={"measurements": initial_rows},
```

`data` tells the chart to read that dataset; `datasets` supplies its initial
rows. Use the same name in `view.set_dataset()` to replace those rows.

Run this in a later cell:

```{literalinclude} ../tutorials/notebooks.py
:language: python
:start-after: notebooks-record-update-start
:end-before: notebooks-record-update-end
```

Keep the column names and value types that the chart expects. You can also
pass an updated dataframe directly:

```python
view.set_dataset("measurements", updated_frame)
```

The chart updates without being rebuilt, so you do not have to start exploring
from scratch. For a widget with exactly one named dataset,
`view.set_data(updated_rows, format="records")` is a shorter alternative.

Equal unnamed tables may be shared automatically. Use separate explicit names
when different charts need independent updates; see {ref}`reuse-chart-data`.

## Use Marimo

Marimo can display the same widget. Create it once in a cell:

```python
import marimo as mo

view = chart.widget()
chart_widget = mo.ui.anywidget(view)
chart_widget
```

Other cells can update its data with `view.set_dataset("measurements", updated_frame)`.
Keep the original widget instead of rebuilding it whenever a control changes.

## Use it without internet access

Normally the chart downloads GenomeSpy's display code when it opens. Use the
copy included with the Python package instead:

```python
chart.display(inline=True)
```

For a chart you plan to update, use `chart.widget(inline=True)`. This sends
more data to the notebook, but avoids downloading the display code. Datasets
loaded from remote URLs still need network access.

## If a chart does not appear

Check that GenomeSpy is installed in the notebook's Python environment.
After installing or upgrading, restart the kernel (the Python session) and
rerun the cells. If downloads are blocked, try `inline=True` as shown above.

You can also [save an HTML file](serialization.md) and open it in a browser.
See the {py:class}`genome_spy.api.JupyterChart` reference for all widget options.
