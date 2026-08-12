# Documentation Example Cleanup Plan

## Goal

Make the documentation examples short, readable, and centered on the
visualization grammar. Examples should show the data table being passed to
`gs.Chart(...)` and the field names being used in encodings, while keeping
dataset preparation and plot-specific computation compact and local.

## Current API Finding

The core API already accepts pandas-like data directly:

```python
gs.Chart(dataframe).mark_point().encode(
    x=gs.X("value:Q"),
    y=gs.Y("score:Q"),
)
```

`Chart` normalizes pandas-like inputs when serializing and can infer an
encoding type from the chart's data when a channel omits one. No new
DataFrame-owned chart abstraction is needed for the ordinary examples.

The repeated `pd.DataFrame(payload[...]).copy()` pattern is mainly caused by
the oncoprint fixtures containing multiple named tables in one JSON object.
Those tables are genuinely separate data sources for separate tracks, but the
examples should not eagerly materialize every table as a module-level global.

## Cleanup Rules

- Keep module-level state limited to gallery metadata and small immutable color
  or category definitions that are reused across several views.
- Load and prepare data inside one `build_chart()` function, or in a short
  dataset function when preparation is substantial.
- Pass a DataFrame, list of records, or other table-like object directly to
  `gs.Chart(...)`; do not convert it to a DataFrame merely because the source
  payload is JSON.
- Materialize only the tables used by a view. For multi-table fixtures, use
  clear local names rather than creating a global for every payload key.
- Keep helpers only when they encode a reusable plot operation, are used more
  than once, or make a long transformation block materially easier to read.
- Prefer local constants for one-plot dimensions, domains, and colors. Keep
  shared constants at module scope only when they define the visual vocabulary
  of the example.
- Keep descriptions to one concise sentence about what the chart shows. Put
  provenance or the original source in a short note or link, not in the code
  structure or title.
- Do not add a generic data adapter or convenience layer until a concrete API
  limitation appears in a simplified example.

## Implementation Order

### 1. Establish a baseline

- Inventory globals, helper functions, payload unpacking, and description
  length across `docs/examples/`.
- Add or preserve gallery serialization tests so cleanup remains behavior-only.
- Treat generated thumbnails and serialized specs as outputs to regenerate,
  not as source files to hand-edit.

### 2. Simplify small examples first

- Refactor `airway_ma_plot.py`, `airway_volcano_plot.py`, `qq_plot.py`,
  `manhattan_plot.py`, and `volcano_plot.py`.
- Move data construction and plot-local constants into a compact chart-builder
  function where that improves locality.
- Remove helpers that only wrap one DataFrame construction or one expression.
- Use direct DataFrame inputs and concise descriptions as the reference style.

### 3. Simplify structured examples

- Refactor `needle_plot.py` and `rainfall_plot.py` next; keep only the small
  transformations needed to make the visual encodings understandable.
- Refactor `oncoprint.py` and `luad_oncoprint.py` after the small-example style
  is established. These examples need multiple tables, but should use locals
  and lazy preparation rather than eagerly exposing every payload table.
- Keep domain-specific computations such as sample filtering and category
  ordering explicit, but colocated with the chart that needs them.

### 4. Review larger track examples

- Apply the same rules to genome browser, annotation, sashimi, and alignment
  examples without hiding important genomic transforms behind generic helpers.
- Preserve explicit transforms when they demonstrate GenomeSpy grammar; remove
  only Python scaffolding that obscures the visualization.

### 5. Consolidate documentation style

- Standardize concise module docstrings and one-sentence `description` values.
- Add a short provenance convention for examples using curated or adapted
  datasets.
- Update the gallery plan and devlog with the resulting authoring conventions.

## Data API Follow-up

No immediate DataFrame API work is required for this cleanup. During the pilot,
add focused tests for the behavior that examples rely on:

- pandas DataFrame input serializes as inline records;
- DataFrame-like inputs continue to work without pandas-specific code in
  `Chart`;
- omitted channel types are inferred from the chart's data;
- JSON/list-of-record inputs can be passed directly to `Chart`.

Only add a new public data helper if the simplified examples expose a repeated
and unavoidable need, such as a typed loader for multi-table packaged datasets.

## Dataset Preparation Boundary

Examples must not perform statistical inference or presentation-oriented data
wrangling merely to make a chart render. This includes t-tests, multiple-test
correction, p-value transformations, quantile/rank construction, significance
classification, derived cutoff columns, and plotting-domain calculations.

Move that work into one of these dataset-layer forms:

- a checked-in derived CSV/JSON fixture when the result is stable and small;
- a private dataset builder under `src/genome_spy/datasets/` when the source
  data is already packaged and the derivation should remain reproducible;
- a public dataset loader only when the prepared result is useful beyond one
  gallery example.

The preferred output is a chart-ready table with named fields such as
`pvalue`, `padj`, `neglog10_pvalue`, `classification`, and explicit domain
metadata. The example should then look like `gs.Chart(data).encode(...)` rather
than teaching SciPy, statsmodels, NumPy, or pandas operations.

For the airway MA/volcano examples, it is feasible to prepare the paired-test
and multiple-testing results once in the datasets layer and expose the derived
table to both plots. For QQ and Manhattan examples, ranks, transformed
p-values, classifications, and threshold metadata should likewise be prepared
before the visualization code. Keep provenance and the method used to derive a
fixture in the dataset module or a short dataset note, not in the chart body.

## Validation

After each example batch:

- run the focused gallery serialization tests;
- run `uv run ruff check .` and `uv run ruff format --check .`;
- rebuild the documentation with Sphinx warnings treated as errors;
- render thumbnails and inspect representative small, wide, layered, and
  composed examples.

## Optional Data Previews

Some examples should show readers the shape of the input table without turning
the source into a notebook. Add an optional module-level convention:

```python
DATA_PREVIEW = {
    "Samples": data.samples.head(),
    "Mutation matrix": data.matrix.head(),
}
```

The existing gallery extension already imports each example while generating
its spec. It can detect `DATA_PREVIEW` and render deterministic HTML tables on
the generated example page above the source code. The preview is documentation
output, not a commented code block or a second data-loading path.

Implementation scope:

- support pandas DataFrames and a small mapping of display names to DataFrames;
- render a bounded head with escaped HTML and no index by default;
- keep previews opt-in so ordinary examples remain unchanged;
- add one gallery test for rendered table headers and one example using the
  convention;
- do not add notebook execution, nbsphinx, or MyST-NB dependencies.

## Initial Pilot

The first pilot is now the airway pair, `qq_plot.py`, and `manhattan_plot.py`.
Their statistical and derived-column preparation lives in the datasets layer;
the remaining examples should be simplified around the resulting chart-ready
tables before the multi-table oncoprints are touched.
