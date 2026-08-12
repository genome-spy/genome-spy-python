# Architecture Notes

## Project Shape

The project should follow the general architecture proven by Altair and reused
by `gos`:

1. A schema-aligned object model that can produce valid JSON specifications.
2. A handwritten ergonomic API layer that adds methods such as marks,
   encodings, composition, serialization helpers, and notebook display hooks.
3. A notebook rendering layer that embeds the upstream JavaScript runtime.

See `plans/schema_wrapper_architecture.md` for a plain-language walkthrough of
how Altair and `gos` build Python APIs around JavaScript JSON schemas, and how
that maps onto the GenomeSpy implementation.

## Proposed Layers

### 1. Schema Layer
- Purpose: represent GenomeSpy spec objects faithfully and validate them.
- Likely shape: generated classes from upstream GenomeSpy schema artifacts,
  plus small shared schema utilities.
- Guidance:
  - Altair uses generated schema bindings plus `schemapi`.
  - `gos` adapts the same approach and generates wrappers from the upstream
    Gosling schema.
  - The handwritten `Chart` directly subclasses generated `UnitSpec` and uses
    schema-object copy semantics for builder methods, matching Altair's
    handwritten-mixin plus generated-spec structure.
  - Generated mark methods now supply grammar-derived names, and complete chart
    specs are validated through generated `Root`. Python-only aliases and data
    normalization remain handwritten.
  - Generated constructor signatures should trend toward Altair's style:
    schema-derived Python unions for common cases, small shared type aliases
    for repeated concepts, and `Any` only as a deliberate fallback for schema
    forms we cannot model precisely yet.

### 2. API Layer
- Purpose: expose Pythonic chart-building ergonomics.
- Likely handwritten entry points:
  - `Chart` or an equivalent top-level core-spec object
  - mark methods such as `.mark_point()`, `.mark_rect()`, `.mark_bar()`
  - `.encode(...)`
  - composition helpers
  - `.to_dict()`, `.to_json()`, `.save(...)`
- Guidance:
  - Altair and `gos` both keep the highest-level user API small and idiomatic.
  - `gos` is especially relevant because it wraps a genomics grammar with
    Track/View composition patterns.

### 3. Notebook Layer
- Purpose: render specs in Jupyter-compatible environments.
- Preferred implementation: `anywidget`.
- Likely responsibilities:
  - sync spec JSON from Python to the front end
  - host a small JS entrypoint that loads GenomeSpy core
  - optionally expose lightweight interaction state later

#### Marimo and Arrow investigation

- Treat Marimo as an anywidget host first. Add a Marimo-specific wrapper only
  if the host compatibility spike demonstrates a concrete missing ergonomic or
  lifecycle behavior.
- Carry Arrow IPC as a binary widget trait. In the first implementation, expose
  the bytes to GenomeSpy through a browser Blob URL and an eager data source
  with `format.type = "arrow"`.
- Keep the authored spec immutable: Blob URLs are runtime resources injected
  into a render-time copy and revoked on replacement or disposal.
- Separate serialization, transport, and interaction code so Polars remains an
  example/development dependency rather than a required core dependency.
- Call this binary columnar transport, not zero-copy rendering. GenomeSpy 0.82
  decodes Arrow IPC and materializes JavaScript row objects for its dataflow.
- Limit the first interaction surface to explicit writable parameters,
  parameter subscriptions, and click events already supported by the upstream
  embed API. Do not wrap the complete JavaScript API speculatively.
- Start reactive payload replacement by re-embedding. If preserving viewport or
  selection state is required, prefer an upstream Arrow-aware named-dataset API
  over bundling a second Arrow decoder in the Python widget.
- See `plans/marimo_arrow_demo_plan.md` for milestones and acceptance criteria.

### 4. Datasets Layer
- Purpose: provide convenient data sources for examples and tutorials.
- Initial shape: use Altair's existing datasets directly:
  `from altair.datasets import data`.
- Guidance:
  - Do not maintain our own dataset catalog yet.
  - Keep notebook examples as close to Altair examples as possible, ideally
    changing only `import altair as alt` to `import genome_spy as alt`.
  - Revisit a `genome_spy.datasets` catalog only after the schema-backed API is
    stable and we know which GenomeSpy-specific examples need package-owned
    data.

## Incremental Scope

### First implementation target
- Core grammar only
- Simple tracks/views
- Basic marks and encodings
- JSON serialization
- Notebook display for simple examples

### Deferred until core is stable
- `@genome-spy/app`-specific sample collection features
- Provenance/session concepts from the app package
- Rich bidirectional notebook interaction APIs
- Advanced data adapters and convenience layers

## Key Design Decisions to Preserve
- Keep the first public API small.
- Prefer incremental coverage of the upstream spec over premature completeness.
- Separate generated schema code from handwritten ergonomic code.
- Keep notebook rendering optional at runtime if dependency weight becomes an issue.

## Composition Resolution Caveat

- GenomeSpy treats view-level composition settings such as `scales`, `axes`,
  and `legends` as resolution-specific configuration on a composed subtree.
- Those view-level settings must map to a single visible resolution for the
  relevant channel. Concat roots often do not satisfy that requirement.
- GenomeSpy also rejects mixing a view-level setting with a conflicting
  encoding-level channel setting in the same resolution.
- In practice, examples and future convenience APIs should avoid composition-
  level overrides on channels where the child encodings already carry channel
  config. For this wrapper, the default `Y(...).scale(...)` behavior is the
  main recurring example.
