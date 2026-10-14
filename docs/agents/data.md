# Data inputs

Use `gs.Chart(records)` for a list of dictionaries. Plain records require only
`genome-spy-python`. Pandas, Polars, and PyArrow tables need the `arrow` extra;
AnnData projection also needs the `anndata` extra.

```python
import genome_spy as gs

rows = [{"id": "a", "x": 2, "y": 5}, {"id": "b", "x": 4, "y": 3}]
chart = gs.Chart(rows).mark_point().encode(x="x:Q", y="y:Q", tooltip=["id:N"])
chart.to_dict()
```

Inspect schema, dtypes, bounded samples, ranges, missing/nonfinite values, and
category order before authoring. A pandas index is not a field: call
`reset_index()` when it contains IDs or coordinates to encode. Preserve supplied
measurements; disclose filtering, sampling, conversions, and derived columns.

The Python API accepts prepared tables and serializes declarative transforms;
GenomeSpy executes `.transform_*()` definitions in the browser. Do not describe
them as Python calculations. URL data stays a reference: even inline HTML needs
network access to fetch remote data.

`genome_spy.anndata.from_anndata` projects selected `obs` fields, `X` gene columns,
and zero-based `obsm` components into a pandas snapshot. It does not select `.raw`
or a layer. Establish the intended source rather than assuming another renderer's
defaults match this helper.

Continue with [encodings](encodings.md) or the [complete quickstart](quickstart.md).
