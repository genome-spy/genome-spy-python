# Arrow data transport

Arrow moves dataframe data from Python to the GenomeSpy widget efficiently. It
changes how data is transferred, not how a chart is defined.

## Install

Install the Arrow extra when using pandas or PyArrow tables:

```bash
pip install "genome-spy-python[arrow]"
```

Polars can write Arrow data directly, but installing the extra is a simple
default when a project uses several dataframe libraries.

## Display a dataframe

Pass a dataframe to `Chart` as usual:

```python
import genome_spy as gs
import pandas as pd

frame = pd.DataFrame({"sample": ["A", "B"], "value": [2.1, 3.4]})

chart = gs.Chart(frame).mark_point().encode(x="sample:N", y="value:Q")
chart
```

Notebook rendering uses Arrow automatically when the table supports it.
`chart.to_dict()` and `chart.to_json()` still produce ordinary JSON-compatible
specifications.

## Update a displayed chart

Arrow is the default transport for dataframe updates:

```python
chart = (
    gs.Chart(frame).mark_point().encode(x="sample:N", y="value:Q")
)
view = chart.widget()

view.set_data(updated_frame)
```

The existing widget stays mounted, so its zoom and selections are preserved.
Use record transport for a list of dictionaries:

```python
view.set_data(updated_rows, format="records")
```

Supported Arrow inputs are pandas and Polars dataframes, plus PyArrow `Table`
and `RecordBatch` objects. Keep column names and value types compatible with the
fields used by the chart.

If a pandas update reports that PyArrow is missing, install the Arrow extra
shown above. Most users do not need to call `to_arrow_ipc()` directly; it is
available for code that needs the serialized bytes.
