# Implementation Plan

## Phases
| Phase | Goal | Status |
|---|---|---|
| 0 | Bootstrap + CI | done |
| 1 | Wrapper design research and API direction | done |
| 2 | Core schema wrapper MVP | in_progress |
| 3 | Notebook rendering with anywidget | in_progress |
| 4 | Polishing core ergonomics, datasets, and examples | exploratory |
| 5 | App-layer exploration and extensions | todo |
| 6 | Marimo interaction and Arrow IPC transport | in_progress |

## Open Questions
- How much of the Python API should be schema-generated versus handwritten convenience code?
- How far should generated Python type annotations go before the maintenance cost outweighs the benefit?
- Should notebook rendering live in the main package from the start or behind an optional dependency?
- What is the smallest useful core chart API that proves the wrapper approach before composition and app features?
- Resolved for examples: use Altair's datasets for now rather than maintaining
  our own dataset catalog. Python-side data inputs should support the
  DataFrame-like objects those examples return.
- Resolved: the core generator should treat the version-pinned
  `@genome-spy/core` npm package as the source of truth. The local
  `tmp/genome-spy` clone is reference-only and must not be required for
  generation.

## Direction
- Model the wrapper after Altair's split between generated schema bindings and a
  smaller handwritten ergonomic layer. The source code we should mirror most
  closely is `tmp/altair/tools/generate_schema_wrapper.py`,
  `tmp/altair/tools/schemapi/`, and `tmp/altair/altair/utils/schemapi.py`.
- Use `gos` as the closest domain-specific precedent for genomics-oriented
  wrapper patterns and notebook widget integration. Its simpler
  `tmp/gos/tools/generate_schema_wrapper.py` is a good first implementation
  template.
- Start with `@genome-spy/core` concepts only. Treat `@genome-spy/app` as a
  later layer once the core grammar and rendering path are stable.
- Make notebook support a first-class deliverable via `anywidget`.
- Mirror Altair's example ergonomics by using `from altair.datasets import data`
  in notebooks for now.

## Near-Term Milestones
1. Add a trimmed `genome_spy.schemapi` runtime based on Altair/Gos.
2. Maintain `tools/generate_schema_wrapper.py` so it fetches
   `@genome-spy/core@<version>` from npm, reads the package's `dist/schema.json`,
   and generates `src/genome_spy/schema/core.py`.
3. Copy the npm package schema JSON into `src/genome_spy/schema/`, copy compact
   TypeScript spec references into the ignored local cache
   `.cache/genome-spy-python/genomespy-core-spec/`, and generate deterministic
   `schema/__init__.py` exports.
4. Add tests that import generated classes, serialize them, and validate a
   minimal GenomeSpy spec.
5. Generate or augment channel wrappers, preserving our `gs.Locus(...)`
   ergonomics and secondary locus-channel normalization.
6. Generate mark mixins from the GenomeSpy mark schema and replace the
   handwritten `MARK_TYPES` constant.
7. Migrate the current `Chart` API to subclass or delegate to generated schema
   classes without breaking the working notebook examples.
8. Once the schema-backed API and notebook renderer are stable, build a
   documentation example gallery. Use the candidate inventory and maturity
   gates in `plans/example_gallery.md`; do not let gallery work drive
   speculative public API additions before then.
9. After the maintainer regeneration workflow is stable, automate checking for
   new `@genome-spy/core` releases and opening a regeneration PR. Keep that
   work separate from the core wrapper/runtime milestones so release automation
   does not block API and notebook progress.
10. Upgrade schema-generated Python signatures from blanket `Any = Undefined`
    to schema-derived annotations, following Altair's general direction:
    scalar primitives, enums, refs, arrays, and common object shapes should
    become explicit Python unions, while genuinely loose schema cases may still
    fall back to `Any`.
11. Complete automatic dataframe-to-Arrow rendering using the single shared
    preparation path in `plans/issue_1_arrow_transport.md`. The exploratory
    Marimo work in `plans/marimo_arrow_demo_plan.md` remains supporting evidence,
    not a parallel implementation or required checked-in deliverable.

Current progress: the generator emits `MARK_TYPES` and a mark-method mixin from
the upstream `MarkType` enum. The handwritten chart layer consumes both,
directly subclasses generated `UnitSpec`, stores schema properties in `_kwds`,
and validates complete specs through generated `Root`. Generated runtime
objects support deep or shallow copying and validation with an opt-out flag.
Builder methods use shallow schema copies, following Altair's structure.

Channel progress: the generator now emits named wrappers for all properties in
GenomeSpy's `Encoding` schema. The public API uses generated wrappers for its
existing channel names while keeping shorthand parsing, constant values, and
locus construction in the handwritten ergonomic layer.

Typing progress: generated schema classes currently expose property names but
not property-level Python types in `__init__`; constructor arguments are
presently emitted as `Any = Undefined`. That is acceptable as a temporary
bootstrap state but is not the intended long-term wrapper quality bar.

## Typed Schema Generation Plan

Goal: move the generated schema layer toward Altair-style Python typing without
blocking incremental wrapper work or overcommitting to a full static-type model
in one jump.

### Phase T1 — Minimal schema-derived constructor typing
- Replace blanket `Any = Undefined` with schema-derived annotations for the
  common cases that are already unambiguous in GenomeSpy's JSON Schema:
  - `string` -> `str`
  - `boolean` -> `bool`
  - `number` / `integer` -> `float` / `int`
  - enums -> `Literal[...]` when compact enough, otherwise a shared alias
  - `$ref` -> referenced generated wrapper class
  - arrays -> `Sequence[...]`
  - objects with no better detail -> `dict[str, Any]`
- Preserve `Undefined` defaults so omission still round-trips cleanly.
- Keep `Any` only as the fallback when the schema case cannot be mapped
  reasonably yet.

### Phase T2 — Shared aliases and repeated schema shapes
- Generate a small typing support module for repeated aliases, similar in
  spirit to Altair's `_typing.py`.
- Deduplicate recurring concepts such as color strings, enum families,
  primitive JSON-like values, and commonly repeated object-or-wrapper unions.
- Prefer readable aliases over exploding constructor signatures with repeated
  giant unions.

### Phase T3 — Typed keyword-object helpers for config-heavy shapes
- Generate `TypedDict` helpers for selected keyword-heavy configuration
  objects, especially where nested raw mappings are part of normal usage.
- Focus first on places where users are likely to pass dicts directly even when
  wrapper classes exist, such as scale/legend/axis/config-like objects.
- Keep this selective; we do not need every object in the schema to also become
  a public `TypedDict`.

### Phase T4 — Channel and nested-setter alignment
- Reuse the same schema-derived typing logic for generated nested setter
  methods such as `.axis(...)`, `.scale(...)`, and `.legend(...)`.
- Ensure constructor signatures and fluent setters accept the same family of
  values where practical: wrapper instance, compatible raw mapping, `None`
  when the schema allows it, and fallback `Any` only where necessary.

### Phase T5 — Validation and maintenance guardrails
- Update codegen tests so they assert typed output for representative schema
  features instead of asserting `Any = Undefined`.
- Add focused regression tests for refs, enums, arrays, optional object
  properties, and fallback cases.
- Keep the typing generator deterministic and maintainable; if a schema form
  becomes too costly to model precisely, prefer an explicit fallback over
  brittle pseudo-precision.

### Non-goals for the first typing slice
- Consuming GenomeSpy's JS JSDoc directly as a required source of truth.
- Achieving perfect static typing for every `anyOf` / `oneOf` case.
- Reworking the handwritten API around type-checker tricks before the generated
  schema layer itself becomes meaningfully typed.

## Deferred
Link to `plans/deferred.md` for anything explicitly out of scope.
