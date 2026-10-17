# Scanpy integration workspace

Start with [status and next work](STATUS.md), the [implementation plan](PLAN.md), and the
[current compatibility guide](../../docs/integrations/scanpy/index.md).
Use `import genome_spy.integrations.scanpy as gsc`, then `gsc.pl.umap(...)`.
Scanpy still owns preprocessing, embedding, clustering, and gene ranking.

The implementation lives in the installable [source package](../../src/genome_spy/integrations/scanpy/),
not in this workspace or the documentation:

| Source | Responsibility |
| --- | --- |
| [__init__.py](../../src/genome_spy/integrations/scanpy/__init__.py) | Lightweight explicit namespace exports. |
| [pl.py](../../src/genome_spy/integrations/scanpy/pl.py) | Public UMAP signature, compatibility validation, optional dependency/version check, and display/return behavior. |
| [_data.py](../../src/genome_spy/integrations/scanpy/_data.py) | Shared raw/layer resolution and resident-expression checks, reused by UMAP and grouped data. |
| [_grouped_data.py](../../src/genome_spy/integrations/scanpy/_grouped_data.py) | Detached grouped values, feature slots/brackets, means, expression fractions and min–max scaling; no chart authoring. |
| [_umap_data.py](../../src/genome_spy/integrations/scanpy/_umap_data.py) | Read existing coordinates and selected expression/metadata; retain row identity, masks, sizes, and draw order. |
| [_umap_colors.py](../../src/genome_spy/integrations/scanpy/_umap_colors.py) | Category order, CSS palette values, numeric bounds, and native scheme validation. |
| [_umap_style.py](../../src/genome_spy/integrations/scanpy/_umap_style.py) | Explicit native presentation defaults and scalar style validation. |
| [_umap_chart.py](../../src/genome_spy/integrations/scanpy/_umap_chart.py) | Native points, axes, legends, labels, and panel composition. |
| [_umap_interactions.py](../../src/genome_spy/integrations/scanpy/_umap_interactions.py) | Optional hover, linked brush highlighting, ownership, and count. |
| [_selection.py](../../src/genome_spy/integrations/scanpy/_selection.py) | Pure interval-to-observation membership for Python subset retrieval. |

Scanpy owns analysis. UMAP's data module only resolves the inputs a plotting call
needs: which raw/layer vector a gene refers to, which categories to display, and
which existing coordinate columns to send. Expression access uses AnnData's
public `obs_vector`; no upstream plotting or private plotting helpers run.
`scanpy.get.obs_df` is not used for UMAP because its duplicate-label rejection and
raw symbol lookup differ from UMAP's behavior. Grouped plots use that public
getter directly, with only selected unique keys. Public AnnData string conversion
operates on the detached table, preserving category order without mutating AnnData.
Grouped statistics are independently tested before adding the dotplot chart.

There are no Matplotlib imports, figure creation, global style reads, or Python
colormap sampling in the adapter. CSS palette values, including saved AnnData
palettes and Scanpy's public default palette lists, go directly to native scales.
GenomeSpy maps continuous values and draws the guides. Plotting retains source
measurements; it does not compute embeddings, rankings, or new scientific results.

UMAP is the currently implemented plot family. Each future family gets its own
chart module and reuses compatible AnnData access, category/color handling, and
plotting computations. A separate data module per family is optional: add one
only when that family needs distinct preparation that merits its own module.
Share common operations directly; there is no requirement to implement another
family before extracting a useful shared helper. Reuse suitable public
Scanpy/AnnData functions and existing library helpers first.

Apply YAGNI to new functionality and abstractions: implement the current plot's
needs with small functions, without building a general adapter framework. Keep
shared functions focused on equivalent semantics, including raw/layer selection,
ordering, thresholds, and normalization. Review basic plot reproduction before
adding interactions.

## Plotting workflow

The [plotting notebook](notebooks/scanpy_plotting.ipynb) loads Scanpy's packaged
`pbmc68k_reduced()` dataset once and retains its stored UMAP coordinates:

1. Basic categorical and continuous plotting, with x/y zoom and panning.
2. Shift-drag linked brushing, selected-cell count, and Python subset retrieval.
3. Customization: subsets/titles, categorical order/palettes, a gene score with
   symmetric color bounds, and the tutorial's marker overview.

It adapts supported UMAP portions of the official core and advanced tutorials.
Gene scoring is an explicit Scanpy operation. Extend this workflow as plot families
arrive, keeping shared setup and avoiding repeated examples.

From the repository root:

```sh
uv sync --dev --extra scanpy --group scanpy-test
uv run jupyter lab integrations/scanpy/notebooks/scanpy_plotting.ipynb
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
uv run --no-sync python -m tests.integrations.scanpy.generate_grouped_references
uv run --no-sync python -m tests.integrations.scanpy.benchmark --help
```

Reference regeneration is a deliberate compatibility update, not a prerequisite
for using the integration. Notebook examples use real packaged data; synthetic
fixtures remain useful for independently checking missing values, duplicate
labels/coordinates, raw/layer differences, sparse allocation, and exact edges.
