# Altair Alignment Plan

## Goal

Align `genome-spy-python` more closely with Altair's architecture:

1. generated schema coverage should provide most of the surface area,
2. a smaller handwritten layer should provide the ergonomic API, and
3. docs/examples should mainly exercise generated or generator-backed APIs,
   not accumulate bespoke wrapper helpers.

This is not a goal of one-to-one API parity with Altair. GenomeSpy has
different grammar concepts, especially around locus channels, lazy genomic
data, and browser-style composition. The goal is to recycle Altair's layering
and maintenance ideas.

## Current State

### Recent progress already landed

- generated `mark_*` methods now expose schema-backed signatures via a
  `use_signature`-style decorator,
- generated schema classes now use an Altair-style
  `with_property_setters` decorator,
- generated channel wrappers now emit schema-derived scalar setters such as
  `field(...)`, `type(...)`, `band(...)`, `value(...)`, and `title(...)`
  where the encoding schema supports them,
- channel `sort(...)` generation support exists and will be picked up
  automatically if the upstream encoding schema starts exposing `sort`,
- channel nested-setter discovery now walks the resolved encoding schema
  instead of relying on a fixed handwritten allowlist,
- config/view helpers now return generated schema wrappers instead of raw dicts
  where the schema already has a first-class object,
- helper signatures now reuse generated kwds types where available for
  config-adjacent wrapper helpers,
- `.properties(...)` now normalizes schema wrappers recursively, so top-level
  authoring behaves more like the rest of the schema-backed API,
- duplicated chart/composition plumbing for config, properties, transforms, and
  composition resolution now largely routes through shared `TopLevelSpec`
  helpers instead of separate unit/composition implementations.

### What already matches Altair's direction

- Generated schema package exists under `src/genome_spy/schema/`.
- Generated modules already cover:
  - `core.py`
  - `channels.py`
  - `mixins.py`
  - `_typing.py`
  - `_kwds.py`
- Public charts directly subclass generated schema classes in `src/genome_spy/chart.py`.
- Mark methods are generated from the upstream schema.
- Channel wrappers are generated from the upstream encoding schema.
- The runtime is schema-backed and validates complete specs through generated
  `Root`.

### What is still more manual than Altair

- `src/genome_spy/channels.py` contains handwritten channel behavior for:
  - shorthand parsing,
  - locus construction,
  - default `Channel` container behavior,
  - `compare(...)`.
- `src/genome_spy/chart.py` contains most transform ergonomics, encoding merge
  behavior, data normalization, and serialization/export workflow.
- `src/genome_spy/helpers.py` still contains a small handwritten convenience
  layer for common schema objects such as:
  - `title(...)`
  - `step(...)`
  - `dynamic_opacity(...)`
  - `scales(...)`
  - `view(...)`
  - `config(...)`
- the generator still emits only a subset of the richer ergonomic generated
  layer that Altair has, especially around config-family and nested object
  convenience.

## Ownership Matrix

This section is the concrete implementation map for the current codebase.
Anything not listed here should be treated as supporting detail rather than a
driver of architecture work.

### Keep handwritten on purpose

These are workflow or GenomeSpy-specific ergonomics and should remain manual
unless a much cleaner generated pattern becomes obvious.

#### `src/genome_spy/chart.py`

- chart construction and composition classes:
  - `Chart`
  - `LayerChart`
  - `HConcatChart`
  - `VConcatChart`
  - `ConcatChart`
- composition operators:
  - `__add__`
  - `__or__`
  - `__and__`
  - `layer(...)`
  - `hconcat(...)`
  - `vconcat(...)`
  - `concat(...)`
- notebook/export/runtime workflow:
  - `to_html(...)`
  - `save(...)`
  - `widget(...)`
  - `_repr_mimebundle_(...)`
- GenomeSpy-specific transform convenience methods:
  - `transform_linearize_genomic_coordinate(...)`
  - `transform_measure_text(...)`
  - `transform_filter_scored_labels(...)`
  - `transform_pileup(...)`
  - other transform helpers as workflow sugar
- data normalization and type inference helpers that sit at the authoring edge:
  - `_normalize_data(...)`
  - `_records_from_data(...)`
  - `_infer_field_type(...)`
  - `_json_safe(...)`

#### `src/genome_spy/channels.py`

- shorthand parsing bridge:
  - `channel(...)`
- GenomeSpy-specific locus helper:
  - `locus(...)`
  - `Locus(...)`
  - dedicated `LocusChannel` fluent wrapper
- simple constant channel helper:
  - `value(...)`
- sort/compare workflow helper:
  - `compare(...)`
- a very small shared `Channel` base is acceptable if generated channels still
  need one common runtime-friendly container.

#### `src/genome_spy/helpers.py`

- tiny universal schema constructors that improve readability and are not worth
  generating as special cases:
  - `expr(...)`
  - `title(...)`
  - `step(...)`
  - `dynamic_opacity(...)`
  - `parse(...)`
  - `data_format(...)`
  - `param(...)`
- typed convenience wrappers are acceptable when they are only thin
  constructor aliases over generated schema objects and do not start carrying
  their own merge or normalization semantics.

### Transitional handwritten layer that should shrink

These pieces are acceptable today but should be treated as candidates to move
closer to generation or shared runtime support.

#### `src/genome_spy/channels.py`

- `Channel.sort(...)`
  - keep as runtime behavior backend for now,
  - long-term target is generated channel ownership where the schema allows it.
- `Channel._with_nested(...)`
- `Channel._with_property(...)`
  - these now mainly exist as tiny runtime backends used by generated channels
    and the handwritten `LocusChannel`, not as the main public channel surface.

#### `src/genome_spy/helpers.py`

- `scales(...)`
  - likely remains small handwritten glue because the schema models scales as a
    typed mapping rather than a dedicated object class.
- `view(...)`
- `view_config(...)`
- `config(...)`
  - these are much healthier now that they return schema wrappers, but they are
    still hand-curated entry points until a generated config ergonomics layer
    exists.
  - they should prefer generated kwds typing and docs guidance over adding more
    handwritten behavior.

#### `src/genome_spy/chart.py`

- `_normalize_channel(...)`
- `_merge_encoding_definitions(...)`
- `_normalize_transform(...)`
- `_normalize_transform_kwarg(...)`
  - these are useful and not urgent to remove, but they are exactly the kind of
    plumbing that should eventually lean more on shared runtime utilities or
    generated signatures instead of continuing to grow inside `chart.py`.

### Generated surface that still needs to grow

These are the clearest missing pieces if we want the codebase to feel more
Altair-like without copying Altair one-to-one.

- generated channel nested setters from resolved schema properties rather than
  the current fixed allowlist,
- generated config/configure-style ergonomics for reused config families,
- broader use of generated `_kwds.py` types in public helper signatures,
- optional property-setter generation pattern similar to Altair's
  `with_property_setters`,
- runtime helpers in `schemapi.py` only where generator work needs them.

## Current Gap List

This is the operational backlog, ordered by architectural value rather than by
user-facing flashiness.

### G1. Config ergonomics are still curated manually

Status: partially addressed

What is done:

- generated `ConfigMethodMixin` now exposes:
  - `configure(...)`
  - `configure_axis(...)`
  - `configure_view(...)`
  - and the rest of the schema-declared `GenomeSpyConfig` families
- handwritten charts and composition specs now share a small backend for
  merging generated config calls into top-level `config`.

What is missing:

- top-level config helpers are still manually chosen entry points,
- config families such as `AxisConfig`, `LegendConfig`, `ScaleConfig`,
  `TitleConfig`, and `ViewConfig` are now surfaced, and the helper layer/docs
  are substantially trimmed, but the helper surface still exists as a
  compatibility layer rather than disappearing behind generated config methods.

Recommended direction:

- prefer the generated `configure*` surface for future config ergonomics work,
- keep handwritten `config(...)` / `view_config(...)` helpers small and avoid
  expanding them now that a generated path exists.

### G2. Channel generation is still narrower than the resolved schema

Status: partially addressed, with schema-driven nested-setter discovery landed

What is done:

- generated channel scalar setters such as `field(...)`, `type(...)`,
  `band(...)`, `value(...)`, and `title(...)` landed,
- channel `sort(...)` generation support is wired in when the schema permits
  it,
- channel nested-setter discovery now walks the resolved encoding schema
  instead of relying on a fixed `axis` / `scale` / `legend` allowlist,
- nested setters are only emitted for object-like nested properties that are
  actually compatible with fluent merge-style builder methods,
- handwritten locus ergonomics were isolated behind a dedicated
  `LocusChannel`, so ordinary channel fluency is now much more clearly owned by
  the generated wrappers.

What is missing:

- the current upstream GenomeSpy encoding schema still only exposes a small
  number of compatible nested channel objects, so the visible generated surface
  is not dramatically broader yet,
- the `Channel` handwritten base still owns the tiny merge/update runtime
  backend for generated wrappers and locus channels,
- `sort(...)` still intentionally lives in handwritten runtime code because the
  authoring surface is richer than the schema alone currently expresses.

Recommended direction:

- keep the schema-driven discovery logic and let future upstream channel-schema
  additions surface automatically,
- then decide whether a lightweight property-setter decorator is still useful
  once more compatible nested properties appear.

### G3. `chart.py` still mixes workflow API and normalization plumbing

Status: partially addressed

What is done:

- reusable runtime helpers for:
  - recursive schema-value normalization,
  - schema-wrapper-or-mapping normalization,
  - nested builder-style mapping merges
  now live in `src/genome_spy/schemapi.py`,
- `chart.py` now uses those shared helpers for top-level properties, transform
  kwarg normalization, and generated config/configure merge paths,
- duplicated unit/composition plumbing for:
  - top-level config merging,
  - property application,
  - transform appending,
  - composition resolution merging
  now largely routes through shared `TopLevelSpec` helpers.

What is missing:

- several chart-specific normalization helpers still live beside the public
  authoring API, especially data normalization and encoding merge logic,
- resolution/config/property/transform plumbing is now mostly centralized, but
  final chart-specific data/type behavior still intentionally stays in the
  chart layer.

Recommended direction:

- do not split files prematurely,
- keep moving only the clearly reusable schema-plumbing helpers into
  `schemapi.py`,
- leave data wrangling, type inference, and encode-specific behavior in the
  chart layer unless they start duplicating elsewhere,
- prefer collapsing duplicated chart/composition plumbing into shared
  `TopLevelSpec` helpers before inventing new runtime abstractions.

### G4. Helper permanence is not yet fully documented

Status: addressed by this plan, but not yet enforced in code review habits

What is now clear:

- which helpers are intentionally permanent,
- which helpers are transitional,
- which families should trigger generator work instead of more handwritten API.

Recommended direction:

- use this matrix as the stopping rule for future helper additions.

## What Altair Has That We Still Largely Lack

### 1. A much richer generated ergonomic layer

Altair does not only generate low-level schema classes. It also generates:

- channel classes with substantial behavior,
- property-setter-style channel ergonomics,
- config-related mixins and methods,
- typed keyword-object helpers used throughout the API.

For us, this means the gap is not just "more schema classes". The gap is
"more generated ergonomics around schema classes".

### 2. Better separation between generated ergonomics and handwritten API

Altair's handwritten `api.py` is still important, but it is not where most
schema-shaped convenience logic lives. In our codebase, some of that logic has
drifted into handwritten `channels.py`, `chart.py`, and `helpers.py`.

### 3. Property-setter / nested-setter generation

Altair generates a lot of nested object handling rather than requiring raw
dicts or handwritten helper functions for each object family.

For us, the main missing area is:

- config-like objects,
- broader generated support for shared resolution/config surfaces,
- reusable nested object setters,
- schema-backed helper coverage for common top-level objects.

### 4. A clearer contract for what stays handwritten

Altair's handwritten layer focuses on workflow:

- chart construction,
- encode behavior,
- composition,
- transforms,
- notebook/runtime integration.

Our current handwritten layer still mixes workflow ergonomics with schema
coverage ergonomics.

### 5. Decorator-backed ergonomics on generated code

Altair uses two important ideas we currently do not recycle yet:

- `@use_signature(...)`
- `@with_property_setters`

What they contribute:

- `use_signature` makes generated or generated-adjacent helper methods present
  schema-derived signatures in editors, docs, and introspection instead of
  generic `**kwargs`.
- `with_property_setters` lets generated schema/channel classes expose more
  fluent ergonomic setters without hand-writing each one.

For us, this means there are two distinct opportunities:

- low-risk signature polish on generated methods,
- higher-impact generation of fluent property ergonomics.

## Recommended Target Architecture

### Layer 1: Runtime schema machinery

Keep `src/genome_spy/schemapi.py`, but evolve it toward a slightly richer
Altair-style runtime where it clearly supports generated wrappers first.

This layer should own:

- serialization,
- validation,
- copy behavior,
- nested property updates,
- schema-backed reconstruction utilities if we add them later.

### Layer 2: Generated schema layer

Keep generating:

- `schema/core.py`
- `schema/channels.py`
- `schema/mixins.py`
- `schema/_typing.py`
- `schema/_kwds.py`

Extend generation so more ergonomics move here:

- richer channel methods,
- more nested setter support,
- better method signatures for generated helpers,
- more typed keyword-object support for common object families.

### Layer 3: Handwritten ergonomic API

Keep this layer intentionally small.

This layer should own:

- `Chart`, `LayerChart`, `HConcatChart`, `VConcatChart`, `ConcatChart`,
- `encode(...)` behavior,
- transform convenience methods,
- GenomeSpy-specific concepts such as locus shorthand and lazy data entry
  points,
- notebook display/export helpers.

This layer should not keep expanding to cover more schema-shaped helper
families if generation can do that work.

### Layer 4: Documentation/examples

Examples should be downstream consumers of the API, not the driver of manual
surface expansion. If many examples need the same dict-shaped escape hatch,
that is a signal to improve generation or the handwritten workflow layer.

## Missing Pieces and How to Address Them

## A. Generator scope is still too narrow

### Current issue

The generator writes the core schema bindings, channels, mixins, typing
aliases, and keyword `TypedDict`s, but it does not yet generate enough of the
ergonomic layer that Altair generates.

### Recommendation

Expand `tools/schemapi/codegen.py` and `tools/generate_schema_wrapper.py` so
that generation can produce:

- richer channel class methods,
- more consistent nested setters,
- more object-family-specific helper support,
- selected config/configure-style mixins where the schema shape is stable.

## B. Handwritten helper growth needs a stopping rule

### Current issue

Recent helpers such as `compare(...)`, `scales(...)`, `view(...)`, and
`config(...)` are useful, but they show the pattern we should avoid scaling
indefinitely.

### Recommendation

Adopt this rule:

- handwritten helpers are acceptable when they express a workflow concept or a
  very common pattern;
- repeated schema-family helpers should trigger generator work instead of more
  handwritten additions.

Practical examples:

- keep: `Locus(...)`, `lazy.bigwig(...)`, `lazy.bam(...)`, chart composition,
  transform helpers;
- probably keep: `title(...)`, `step(...)`, `expr(...)`;
- probably generate or generator-back later: more config/view/legend/axis/scale
  object conveniences if the list keeps growing.

## C. Channel ergonomics should move closer to generated channels

### Current issue

`src/genome_spy/channels.py` is much smaller now, but the remaining runtime
backend still exists outside generation and `sort(...)` is still partly
handwritten by necessity.

### Recommendation

Move toward this split:

- generator owns most channel-class-specific methods and typing,
- handwritten `channels.py` becomes a small compatibility/ergonomic shim for:
  - shorthand parsing,
  - locus-specific construction,
  - a tiny common `Channel` behavior base and `sort(...)` backend.

## D. Config and view surfaces need a stronger schema-backed story

### Current issue

We still expose handwritten helper entry points for some top-level surfaces
even though the generated config surface is now substantially better.

### Recommendation

Prefer schema-backed config objects or generated configure-style support over
growing a large family of handwritten dict helpers.

This does not mean copying Altair's exact `configure_*` API immediately. It
means reusing the idea that config surfaces should be systematic, not
hand-curated one helper at a time.

## E. We still need a cleaner chart/API file split

### Current issue

`src/genome_spy/chart.py` currently holds both public chart behavior and a
fair amount of plumbing, although much of the duplicated unit/composition copy
plumbing has now been centralized.

### Recommendation

As generation grows, consider splitting responsibilities more clearly:

- `chart.py`: top-level chart/composition workflows,
- `channels.py`: very small ergonomic shim,
- `helpers.py`: only the truly universal handwritten helpers,
- generated schema files: most schema-family behavior.

## Implementation Phases

## Phase 1: Freeze handwritten helper growth

Goal: stop adding more tiny schema-family helpers unless they are genuinely
workflow-level ergonomics.

Tasks:

- Treat the current helper set as a temporary boundary.
- Document which helpers are intentionally permanent versus transitional.
- Avoid adding more helper families until the next generator pass lands.

Success criteria:

- no new helper is added without explicitly answering "why is this not
  generator work?"

## Phase 2: Expand generator-backed nested ergonomics

Goal: move more ergonomics into generation.

Tasks:

- review `tools/schemapi/codegen.py` against Altair's generator patterns,
- identify where generated channels and generated schema classes can expose
  more nested setters,
- reuse generated `_kwds.py` typed shapes more aggressively,
- keep the output deterministic and small enough to maintain.

Success criteria:

- fewer handwritten schema-family helpers are needed for docs examples,
- generated surfaces cover more common nested object patterns.

## Phase 3: Shrink the handwritten compatibility layer

Goal: make `channels.py` and `helpers.py` smaller and more intentional.

Tasks:

- re-evaluate each helper in `src/genome_spy/helpers.py`,
- re-evaluate each method in `src/genome_spy/channels.py`,
- move what can be generated,
- keep only the GenomeSpy-specific or workflow-specific pieces.

Success criteria:

- handwritten code is clearly ergonomic glue, not schema coverage.

## Phase 4: Regenerate and migrate examples

Goal: make docs reflect the architecture, not compensate for it.

Tasks:

- regenerate schema outputs,
- update examples to prefer generated or generator-backed surfaces,
- reduce remaining raw dict usage only where it materially improves clarity.

Success criteria:

- docs examples mainly demonstrate the intended API shape,
- remaining raw dicts are rare and justified.

## Suggested Immediate Next Task

The next implementation task should be:

1. inspect `tools/schemapi/codegen.py` against Altair's generator patterns,
2. identify one concrete generator-backed improvement to land first,
3. implement that generator change before adding any more handwritten helper
   families.

The best first candidate is:

- expand generated ergonomic support for common nested schema objects so we can
  stop growing handwritten config/view/scale-style helper coverage.

After the recent chart/channels/helpers cleanup, that recommendation can now
be narrowed further:

- most remaining tiny handwritten helpers are intentional and low-cost,
- the clearest remaining generator-backed target is the top-level config
  compatibility layer,
- so future generator work should prioritize overlap around `config(...)`,
  `view(...)`, and `view_config(...)` rather than trying to eliminate helpers
  like `expr(...)`, `step(...)`, `parse(...)`, or `data_format(...)`.

## Concrete Generator Worklist

This section translates the architecture direction into specific code changes.

### Current generator boundaries in this repo

Today our generator already produces:

- schema classes in `tools/schemapi/codegen.py` via:
  - `generate_core_module()`
  - `generate_typing_module()`
  - `generate_kwds_module()`
  - `generate_mark_mixins_module()`
  - `generate_channels_module()`
- orchestration in `tools/generate_schema_wrapper.py`

The main missing piece is not basic generation. It is that the generated
surface is still thinner than the handwritten compatibility layer.

### Altair decorator ideas worth recycling

#### `use_signature`

Altair uses `@use_signature(...)` heavily on generated mixin methods such as:

- `mark_*` methods,
- config/configure-style methods.

The point is not validation. The point is to expose the underlying schema
object's signature on a convenience method.

What this suggests for us:

- generated `mark_*` methods in `src/genome_spy/schema/mixins.py` are a strong
  first candidate for signature-copying support,
- future generated config/configure methods should likely use the same pattern,
- this is a relatively low-risk improvement because it mainly affects
  introspection and editor ergonomics.

#### `with_property_setters`

Altair uses `@with_property_setters` on many generated channel classes to
provide richer fluent behavior directly on generated classes.

What this suggests for us:

- this is the larger architectural move,
- it belongs after or alongside generator-backed channel ergonomics work,
- it could eventually reduce how much custom behavior stays in
  `src/genome_spy/channels.py`.

### Missing generated capabilities vs. current handwritten code

#### 1. Generated channels are still too passive

Current state:

- `src/genome_spy/schema/channels.py` generates wrappers plus `axis`, `scale`,
  and `legend` setters.
- `src/genome_spy/channels.py` still owns:
  - `.title(...)`
  - `.sort(...)`
  - nested setter merge behavior
  - the base `Channel` mapping container
  - shorthand handling

Altair idea to recycle:

- generated channel classes should carry more of their own ergonomic behavior,
  with the handwritten layer becoming a smaller shim.

Concrete tasks:

- extend `generate_channels_module()` so channel classes can generate:
  - `title(...)` where schema permits it,
  - `sort(...)` where schema permits it,
  - nested setter methods from the resolved property schema rather than the
    current fixed `axis` / `scale` / `legend` trio.
- move channel-specific typing decisions into generation where practical.
- evaluate whether a lightweight property-setter decorator is worth adopting
  after the schema-driven method generation lands.

#### 2. Config-family support is not systematic yet

Current state:

- we have `_kwds.py` typed helpers for many config-like objects,
- but no generated config/configure-style ergonomic layer.
- handwritten `helpers.py` now contains `scales(...)`, `view(...)`,
  `config(...)`, and related glue.

Altair idea to recycle:

- generate config-related methods systematically rather than adding helper
  families ad hoc.

Concrete tasks:

- inspect config-like definitions already listed in `KWDS_TARGETS`,
- add a first generated config-support pass:
  - either generate a config mixin layer,
  - or generate top-level config object helpers in a dedicated module,
  - but keep the surface schema-derived rather than curated manually.
- decide whether GenomeSpy should mirror Altair's `configure_*` naming, or use
  a smaller GenomeSpy-specific variant.

#### 3. The runtime is still a minimal bootstrap runtime

Current state:

- `src/genome_spy/schemapi.py` is intentionally small.
- it supports validation, copy, serialization, and `_with_property(...)`.

Altair idea to recycle:

- keep a runtime that is generic enough for generated wrappers to rely on
  directly for more behavior.

Concrete tasks:

- audit whether `SchemaBase` should gain:
  - safer nested property merge helpers,
  - optional signature/decorator support hooks for generated methods,
  - optional property-setter support for generated classes,
  - reconstruction/from-dict helpers later.
- do not widen runtime surface speculatively; add only what directly unblocks
  generator-backed ergonomics.

#### 4. Typed keyword-object generation is underused

Current state:

- `_kwds.py` already exists and covers many object-like schema shapes.
- generated channels use only a small slice of those types.

Altair idea to recycle:

- generated `TypedDict` coverage should actively shape the public generated
  signatures, not just exist as side artifacts.

Concrete tasks:

- review each use of `raw_mapping_annotation(...)` in `SchemaAnalyzer`,
- prefer generated kwds helpers whenever an object-like schema has stable,
  usable structure,
- expand use of anonymous helper generation beyond the current
  `axes` / `legends` / `resolve` / `scales` cases if it helps config surfaces.

### Recommended implementation order

#### Step 1: Add signature-copying support for generated helper methods

Files:

- `src/genome_spy/schemapi.py` or a small new utility module
- `tools/schemapi/codegen.py`
- regenerated `src/genome_spy/schema/mixins.py`

Work:

- add a small `use_signature`-style utility,
- apply it first to generated `mark_*` methods,
- verify that generated methods expose more informative signatures without
  changing runtime behavior.

Why first:

- it is the lowest-risk Altair idea to borrow,
- it improves developer experience immediately,
- it does not force a larger redesign before we are ready.

#### Step 2: Generalize generated nested setters

Files:

- `tools/schemapi/codegen.py`
- regenerated `src/genome_spy/schema/channels.py`

Work:

- replace the current hardcoded nested-setter generation logic with a schema-
  driven pass that can emit more than `axis`, `scale`, and `legend`.
- add generated `title` and `sort` support where the resolved channel schema
  permits them.

Why first:

- it directly shrinks handwritten `channels.py`,
- it affects many examples,
- it is the clearest Altair-like improvement with limited blast radius.

#### Step 3: Introduce a generated config ergonomics surface

Files:

- `tools/schemapi/codegen.py`
- possibly a new generated module under `src/genome_spy/schema/`
- `src/genome_spy/chart.py` or `src/genome_spy/api.py` for wiring

Work:

- choose one small, systematic config-generation pattern:
  - generated config mixin methods, or
  - generated config helper module.
- cover the most reused config families first:
  - `Config`
  - `ViewConfig`
  - `ScaleConfig`
  - `AxisConfig`
  - `LegendConfig`
  - `TitleConfig`

Why second:

- it addresses the exact helper growth problem we just hit in docs work.

#### Step 4: Reduce handwritten helper overlap

Files:

- `src/genome_spy/channels.py`
- `src/genome_spy/helpers.py`
- `src/genome_spy/chart.py`

Work:

- after regeneration, audit each handwritten helper or method and classify it:
  - permanent ergonomic API,
  - compatibility shim,
  - now redundant and removable.

Why third:

- we should not remove handwritten helpers before the generated surface exists.

### First concrete engineering slice I would implement

If we want the smallest meaningful generator improvement next, it should be:

1. add a small `use_signature`-style utility,
2. teach `tools/schemapi/codegen.py` to apply it to generated `mark_*`
   methods,
3. regenerate `src/genome_spy/schema/mixins.py`,
4. add tests that verify better signatures or at least preserved helper
   behavior,
5. then move to generated `title(...)` and `sort(...)` channel methods.

That is the cleanest next step because it is:

- highly Altair-aligned,
- incremental,
- easy to validate,
- and directly reduces the amount of handcrafted schema ergonomics.

## Non-goals

- Exact Altair API parity.
- Copying Vega-Lite-specific APIs that do not fit GenomeSpy's grammar.
- Replacing GenomeSpy-specific concepts such as locus channels or lazy genomic
  data with Altair-like abstractions where they do not fit.
- Eliminating all raw dict usage from examples; some low-level transforms may
  still be clearer as explicit schema mappings.
