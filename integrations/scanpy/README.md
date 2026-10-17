# Scanpy integration workspace

Start with the [implementation plan](PLAN.md) and the
[current compatibility guide](../../docs/integrations/scanpy/index.md).
The API is `import genome_spy.scanpy as gsc`, then `gsc.pl.umap(...)`.
Scanpy still owns preprocessing, embedding, clustering, and gene ranking.

The implementation lives in the installable [source package](../../src/genome_spy/scanpy/),
not in this workspace or the documentation:

| Source | Responsibility |
| --- | --- |
| [__init__.py](../../src/genome_spy/scanpy/__init__.py) | Lightweight explicit namespace exports. |
| [pl.py](../../src/genome_spy/scanpy/pl.py) | Public UMAP signature, compatibility validation, optional dependency/version check, and display/return behavior. |
| [_prepare.py](../../src/genome_spy/scanpy/_prepare.py) | UMAP-only AnnData extraction, ordered observation snapshot, color/size semantics, and prepared panel descriptions. |
| [_charts.py](../../src/genome_spy/scanpy/_charts.py) | Native UMAP marks, guides, panel composition, linked brush, and count. |
| [_selection.py](../../src/genome_spy/scanpy/_selection.py) | Pure interval-to-observation membership for Python subset retrieval. |

These preparation and chart modules currently implement UMAP only. Their names
do not imply a completed common adapter framework. Future plot families get
explicit preparation/rendering modules as described in the plan.

## Workflow notebooks

All examples load Scanpy's packaged `pbmc68k_reduced()` dataset and retain its
stored UMAP coordinates. The advanced example runs gene scoring explicitly in
Scanpy. These cover supported UMAP portions of the official plotting tutorials.

- [Core UMAP examples](notebooks/scanpy_umap.ipynb)
- [Advanced UMAP customization](notebooks/scanpy_umap_customization.ipynb)
- [Linked brushing and Python retrieval](notebooks/scanpy_linked_brushing.ipynb)

From the repository root:

```sh
uv sync --dev --extra scanpy --group scanpy-test
uv run jupyter lab integrations/scanpy/notebooks
```

## Validation

[Validation sources](../../tests/integrations/scanpy/) contain the tests,
reference images/contracts, explicit reference generator, and resource benchmark.
They are development code and are not shipped as part of the Python package.

```sh
uv run --no-sync pytest tests/integrations/scanpy --ignore=tests/integrations/scanpy/browser
uv run --no-sync pytest tests/integrations/scanpy/browser
```

The former `tools/scanpy_reference.py` is now
[generate_references.py](../../tests/integrations/scanpy/generate_references.py).
It explicitly runs pinned Scanpy plotting on small synthetic test fixtures and
records signatures, figures, domains, colors, draw order, and point footprints.
Inspecting Matplotlib artists is confined to this reference-generation step;
production plotting never recovers input data from rendered artists. Ordinary
tests compare against the frozen results instead of regenerating them.

```sh
uv run --no-sync python -m tests.integrations.scanpy.generate_references --help
uv run --no-sync python -m tests.integrations.scanpy.benchmark --help
```

Reference regeneration is a deliberate compatibility update, not a prerequisite
for using the integration. Notebook examples use real packaged data; synthetic
fixtures remain useful for independently checking missing values, duplicate
labels/coordinates, raw/layer differences, sparse allocation, and exact edges.
