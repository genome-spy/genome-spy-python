# Data inputs

## Records: base package

Use when the input is a list of records with numeric `x` and `y`, plus an `id`.

```python
import genome_spy as gs

rows = [{"id": "a", "x": 2, "y": 5}, {"id": "b", "x": 4, "y": 3}]
chart = gs.Chart(rows).mark_point().encode(x="x:Q", y="y:Q", tooltip=["id:N"])
chart.to_dict()
```

## Dataframes and indexes: `arrow` extra

Pandas, Polars, and PyArrow tables are accepted directly. Expose useful indexes
as columns; inspect types, bounded samples, missing values, ranges, and order.

```python
import genome_spy as gs
import pandas as pd

rows = [{"id": "a", "x": 2, "y": 5}, {"id": "b", "x": 4, "y": 3}]
frame = pd.DataFrame(rows).set_index("id")
records_with_ids = frame.reset_index()
assert records_with_ids["id"].is_unique
chart = gs.Chart(records_with_ids).mark_point().encode(
    x="x:Q", y="y:Q", tooltip=["id:N"]
)
chart.to_dict()
```

CSV loading and data checks happen in Python; [declarative transforms](encodings.md#browser-transforms)
execute in GenomeSpy. Preserve supplied measurements and report any filtering,
sampling, conversions, or derived columns.

## Remote CSV

```python
import genome_spy as gs

remote = gs.Chart(
    gs.Data(url="https://example.org/measurements.csv", format=gs.data_format(type="csv"))
).mark_point().encode(x="x:Q", y="y:Q")
remote.to_dict()  # Serializes the URL; does not fetch or validate its contents.
```

Replace the illustrative URL with an accessible table. `inline=True` bundles the
runtime, not URL data; rendering still needs network access.

## AnnData projection: `anndata` and `arrow` extras

A small synthetic input makes the source selection explicit:

```python
import anndata as ad
import genome_spy as gs
import numpy as np
import pandas as pd
from genome_spy.anndata import from_anndata

adata = ad.AnnData(
    X=np.array([[1.0], [2.0]]),
    obs=pd.DataFrame({"group": ["A", "B"]}, index=["a", "b"]),
    var=pd.DataFrame(index=["feature_a"]),
)
adata.obsm["embedding"] = np.array([[0.0, 1.0], [2.0, 3.0]])
snapshot = from_anndata(
    adata, obs=["group"], genes=["feature_a"], obsm_keys=[("embedding", 0)]
).reset_index()
projected = gs.Chart(snapshot).mark_point().encode(
    x="embedding-0:Q", y="feature_a:Q", color="group:N"
)
projected.to_dict()
```

`from_anndata` reads selected `X` genes, `obs` fields, and zero-based `obsm`
components into a pandas snapshot. It does not select `.raw` or a layer.
Resolve the intended source before calling it; no analysis is performed.
Expected: two points with `embedding-0` on x, `feature_a` on y, colored by group.

Continue with [encodings](encodings.md) or [quickstart](quickstart.md).
