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

## Measurement source and selection scope

Before encoding, identify the source table/field, units, transformations and
aggregation. Normalizing before grouping differs from normalizing group means;
fractions also need a denominator and missing/zero rules.

Feature selection and record filtering are separate. Here a supplied feature
list chooses columns to show; both observation groups remain visible. The means
are prepared inputs, not calculated by this chart.

```python
import genome_spy as gs

summaries = [
    {"group": "A", "feature": "f1", "mean_normalized_score": 0.2},
    {"group": "B", "feature": "f1", "mean_normalized_score": 0.8},
    {"group": "A", "feature": "f2", "mean_normalized_score": 0.5},
    {"group": "B", "feature": "f2", "mean_normalized_score": 0.4},
]
feature_lists = {"A": ["f1"], "B": ["f2"]}
selected_features = feature_lists["A"]
visible_groups = ["A", "B"]
selected = [
    row for row in summaries
    if row["feature"] in selected_features and row["group"] in visible_groups
]
chart = gs.Chart(selected).mark_point(filled=True).encode(
    x=gs.X("feature:N").scale(type="band", domain=selected_features),
    y=gs.Y("group:N").scale(type="band", domain=visible_groups, reverse=True),
    color=gs.Color("mean_normalized_score:Q").legend(title="Mean normalized score"),
)
chart.to_dict()
```

Expected: two points for `f1`, one per group. Changing `visible_groups` filters
records; changing its order changes display order. Choosing a different value
field changes the measurement. Keep these decisions explicit.

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
