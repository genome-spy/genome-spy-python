# Marimo + Arrow Interactive Demo Plan

## Objective

Build a polished, reproducible Marimo notebook that uses Polars for Python-side
data manipulation, transfers derived tables to GenomeSpy as Arrow IPC binary
data through the existing anywidget bridge, and links selected GenomeSpy
interactions back to reactive Python cells.

The final story is a mutation-impact comparison: a reference sequence, a
reference signal, an alternate signal produced for user-selected mutations,
and a derived difference track. The first milestones deliberately use tiny
synthetic tables and deterministic local computations. Model integration is a
later content layer, not a prerequisite for proving the transport and
interaction architecture.

## Status — 2026-08-06

- M0 is complete: the wrapper now targets the published GenomeSpy core 0.82.0
  release and its generated artifacts.
- M1 rendering is manually verified in the Marimo editor. The anywidget bridge
  exposes explicit parameter values, click state, and error state, and the
  checked-in source notebook now emits a visible Marimo output. Repeated-click
  and disposal behavior still need an explicit browser verification recipe.
- M2 has an initial implementation: `gs.to_arrow_ipc(...)`, an `arrow_data`
  binary widget trait, `arrow://name` Blob URL substitution, and a checked-in
  Polars notebook. The notebook uses Marimo's anywidget adapter and includes
  integer, floating-point, string, Boolean, and nullable columns. Blob
  revocation and mixed-type browser rendering still need focused verification
  before M2 is complete.
- M3 is in progress: the widget uses latest-update-wins render revisions and
  per-render Blob URL ownership. Reusable transport, lifecycle, and update
  behavior is covered by library tests; browser transfer/render latency remains
  a host-level measurement rather than maintained script tooling.
- The temporary non-model Marimo notebooks used to prove transport and
  interaction behavior have been removed. The maintained user-facing workflow
  is the AlphaGenome notebook under `notebooks/alphagenome/`; reusable Arrow and
  widget behavior remains covered by library tests.

## Current Evidence

- The Python widget synchronizes the authored spec, embed settings, explicit
  interaction state, and optional named Arrow IPC payloads. Arrow payload
  changes trigger a latest-update-wins re-embed; stale embeds are finalized and
  their render-owned Blob URLs are revoked.
- The M4 browser smoke showed the mutation control, colored base sequence,
  reference/alternate signal tracks, and a localized delta peak. The notebook
  is intentionally synthetic and offline; it is not a model-output claim.
  The browser click probe did not yet produce a reliable synced datum, so the
  interaction contract remains unverified for this notebook.
- anywidget transports Python `bytes`, `bytearray`, and `memoryview` values as
  binary widget buffers represented by `DataView` in JavaScript. This avoids
  JSON row conversion and base64 expansion during the Python-to-browser hop.
- Polars can write an uncompressed Arrow IPC file to an in-memory `BytesIO`
  object with `DataFrame.write_ipc(file=None)`.
- GenomeSpy 0.82 supports Arrow IPC file and stream encodings through an eager
  URL data source with `format.type = "arrow"`. It fetches an `ArrayBuffer` and
  uses Flechette to materialize mutable row objects.
- A widget can therefore expose the synced bytes through a browser `Blob` URL,
  inject that URL into a copy of the spec, and let GenomeSpy's own Arrow loader
  read it. Blob URLs must be revoked when replaced or when the widget is
  finalized.
- GenomeSpy's embed result already supports:
  - click events with the clicked datum;
  - named parameter handles with `getValue`, `setValue`, and `subscribe`;
  - runtime replacement of declared named datasets with JavaScript row arrays.
- Marimo supports anywidget and reacts to synced widget trait changes. A
  dedicated Marimo wrapper may improve ergonomics later, but it is not needed
  for the first compatibility proof.

## Important Semantics

This path is **binary and columnar in transit**, but it is not currently
zero-copy end to end:

1. Polars serializes a frame to Arrow IPC.
2. The widget protocol transfers a binary buffer.
3. GenomeSpy fetches the Blob URL and Flechette decodes IPC.
4. GenomeSpy materializes JavaScript row objects for its dataflow.

The initial claim should therefore be "direct binary Arrow IPC transport from
Polars to GenomeSpy," not "zero-copy Polars rendering."

## Scope

### In scope

- Upgrade the wrapper's pinned GenomeSpy core/schema/bundle version to 0.82.
- Verify the existing widget in Marimo before adding Marimo-specific code.
- Establish a small, typed Python representation for Arrow-backed widget data.
- Transfer one or more uncompressed Arrow IPC payloads over widget binary
  traits without temporary files or an HTTP server.
- Connect a small supported interaction surface in both directions:
  - Python to GenomeSpy through writable named parameters;
  - GenomeSpy to Python through parameter subscriptions and click events.
- Define lifecycle, error, and update semantics for binary payloads.
- Build a deterministic genomics-shaped demo before introducing a model.
- Measure payload size and update behavior against the current JSON-row path.

### Out of scope for the first project

- General support for every Arrow producer, extension type, or compression
  codec.
- A promise of zero-copy rendering or Arrow-native transforms inside
  GenomeSpy.
- Live AlphaGenome credentials, quota management, or long-running inference.
- Writing or mutating BigWig files in the notebook.
- A generic Python wrapper for the complete GenomeSpy JavaScript API.
- Collaborative multi-user widget state or deployment infrastructure.

## Proposed Architecture

```text
Marimo control / GenomeSpy event
              |
              v
      reactive Python cell
              |
       Polars DataFrame
              |
   uncompressed Arrow IPC bytes
              |
   anywidget binary trait (DataView)
              |
    Blob URL + data.format="arrow"
              |
        GenomeSpy 0.82 embed
```

Keep three responsibilities separate:

1. **Serialization:** a pure Python helper converts a supported table to IPC
   bytes and reports contextual errors.
2. **Transport:** the widget synchronizes named binary payloads and manages Blob
   URL ownership.
3. **Interaction:** the widget maps an explicit allowlist of GenomeSpy params
   and events to small JSON-safe traits. It does not expose the raw JavaScript
   embed object to Python.

The first Arrow implementation should use a copied render spec with Blob URLs;
the authored chart/spec must remain unchanged. For reactive data replacement,
start with safe re-embedding. Only add an incremental update path after
measuring whether re-embedding loses important viewport, selection, or
parameter state.

## Milestones

### M0 — Align with GenomeSpy 0.82

Scope:

- Pin `@genome-spy/core` schema and notebook bundle URLs to 0.82.
- Regenerate schema bindings and capability metadata.
- Add a schema/spec regression for `{format: {type: "arrow"}}` even though the
  upstream schema currently permits arbitrary format strings.
- Record upstream limitations: dates/timestamps become numbers, 64-bit integers
  become JavaScript numbers, and IPC buffer compression is unsupported.

Exit criteria:

- Existing tests pass against regenerated 0.82 artifacts.
- A minimal Arrow URL spec validates and serializes.
- The widget loads the 0.82 bundle.

### M1 — Marimo compatibility and interaction spike

Scope:

- Add a tiny checked-in Marimo notebook with an inline point chart.
- Confirm a normal `JupyterChart` renders without a Marimo-specific adapter.
- Prototype one writable numeric parameter in each direction.
- Forward click datum as a JSON-safe synced trait with a monotonic revision so
  repeated clicks on the same datum remain observable.
- Unsubscribe and finalize cleanly when the widget is disposed or re-embedded.

Exit criteria:

- A Marimo slider updates a GenomeSpy parameter without rebuilding the chart.
- A GenomeSpy click updates Python-visible state and reruns a dependent Marimo
  cell.
- Repeated clicks, missing params, and disposal have focused tests or a written
  manual verification recipe where browser automation is required.

API decision gate:

- Keep the spike private until event payloads, update-loop prevention, and
  error reporting are understood.

### M2 — One-shot Polars-to-Arrow rendering

Scope:

- Add Polars and Marimo as example/development dependencies, not mandatory core
  runtime dependencies.
- Serialize a small Polars frame using uncompressed Arrow IPC file encoding.
- Sync the payload through a binary trait.
- In JavaScript, create a Blob URL, inject it into a copied data specification,
  render through GenomeSpy's `format.type = "arrow"` loader, and revoke it on
  cleanup.
- Surface serialization and load failures visibly instead of silently falling
  back to JSON.

Exit criteria:

- No temporary data file, local web server, JSON records, or base64 encoding is
  used between Polars and GenomeSpy.
- Null, Boolean, string, integer, and floating-point columns render correctly.
- A test or browser probe confirms old Blob URLs are revoked.
- The notebook states the supported type and compression limits.

API decision gate:

- Compare a dedicated `ArrowData`/`arrow(...)` value object with a
  widget-only `arrow_data={name: frame}` argument. Prefer the smallest API that
  composes with existing `Chart` and named-dataset authoring.

### M3 — Reactive Arrow updates

Scope:

- Recompute a Polars frame from a Marimo control and replace the IPC payload.
- Implement latest-update-wins behavior so stale asynchronous loads cannot
  replace a newer result.
- Begin with re-embedding and document which runtime state is reset.
- Measure payload size, encode time, transfer time where observable, and render
  latency against the JSON-record path for representative table sizes.

Exit criteria:

- A control change produces a visibly updated chart with no manual cell run.
- Rapid updates do not display stale data or leak Blob URLs.
- Benchmarks justify keeping the Arrow path and clearly avoid zero-copy claims.

Upstream decision gate:

- If preserving zoom, selection, and parameter state is required, propose an
  upstream API that accepts Arrow IPC for a declared dataset or exposes the
  registered Arrow decoder. Do not duplicate Flechette in the widget bundle
  without first evaluating that API addition.

### M4 — Deterministic mutation-impact prototype

Scope:

- Use a short packaged reference region and synthetic or redistributable signal
  values.
- Let the user select or enter a small mutation set.
- Use Polars to build reference, alternate, and delta signal tables.
- Render a reference-sequence track plus aligned reference/alternate/difference
  tracks using Altair-style composition operators where practical.
- Use a GenomeSpy click or interval parameter to feed a selected locus back to
  Python.

Exit criteria:

- The notebook is deterministic, fast, offline-capable after installation, and
  contains no model credentials.
- The dataflow is understandable from the notebook: mutation input → Polars
  computation → Arrow IPC → linked GenomeSpy tracks.
- Reference and alternate coordinates and signal domains remain aligned.

### M5 — Showcase notebook

Scope:

- Replace the toy scorer with a small curated pair of precomputed model outputs
  with clear source, license, genome assembly, tissue/assay, and model-version
  metadata.
- Treat model outputs as tabular signal intervals transported via Arrow; use
  BigWig only for remote/lazy baseline tracks where it adds value.
- Add concise narrative, loading/error state, environment instructions, and a
  social-media-friendly default view.
- Optionally document live inference as a separate extension if access,
  latency, quota, and redistribution constraints are acceptable.

Exit criteria:

- A clean environment can run the notebook from its checked-in Python source.
- The default story works without secrets or a live model service.
- Screenshots/video and claims are reproducible from pinned inputs.
- Tests cover helpers and serialization; a manual browser checklist covers
  rendering and interaction.

## Validation Matrix

| Concern | Minimum validation |
|---|---|
| Schema/version | Generated artifact tests and serialized Arrow URL spec |
| Polars serialization | Round-trip IPC fixture and unsupported-input errors |
| Binary transport | Widget trait test plus browser confirmation of `DataView` |
| Arrow rendering | Browser smoke test with mixed primitive/null columns |
| Lifecycle | Re-embed/dispose test; Blob URL and listener cleanup |
| Python → JS | Writable parameter update without re-embed |
| JS → Python | Click/parameter change updates trait revision and Marimo cell |
| Reactivity | Rapid changes are latest-update-wins |
| Performance | JSON versus Arrow payload size and timed representative updates |
| Demo reproducibility | Clean-environment notebook run and pinned data provenance |

## Risks and Mitigations

- **Blob URL loading behavior differs by notebook host.** Prove it in Marimo in
  M2 before designing a public data abstraction.
- **Re-embedding resets interaction state.** Accept this for the first reactive
  spike, measure the user impact, then pursue a runtime Arrow dataset API if
  needed.
- **Two-way traits can create feedback loops.** Track update origin/revision and
  make programmatic parameter writes idempotent.
- **Large binary traits may still incur copies.** Benchmark realistic sizes and
  keep the first demo bounded.
- **Arrow type coercion can surprise users.** Test the supported subset and fail
  with column/type context where Python can detect incompatibility.
- **Model integration can dominate the project.** Keep precomputed outputs as
  the default showcase path and make live inference optional.
- **BigWig is not the natural reactive result format.** Use BigWig for remote
  windowed source data; use Arrow tables for newly computed reference,
  alternate, and delta signals.

## Open Decisions

- Should Arrow payloads be addressed by named dataset, by a data-source token,
  or through a chart-local value object?
- Should the first public interaction API expose explicit params/clicks only,
  or a generic event mapping with typed convenience methods later?
- What viewport and selection state must survive reactive data replacement?
- What table sizes make Arrow materially better than the existing `to_dicts()`
  normalization after browser-side row materialization?
- Which model output can be redistributed and cited in the final example?

## Immediate Next Slice

Manually verify the M3 reactive Arrow notebook in the Marimo editor. Move the
amplitude slider slowly and rapidly, confirm that the chart ends on the latest
value, and observe whether re-embedding resets useful viewport state. Then add
repeatable Blob URL cleanup coverage before treating reactive transport as
complete. Keep the private `arrow://name` convention until that evidence
supports a public API.
