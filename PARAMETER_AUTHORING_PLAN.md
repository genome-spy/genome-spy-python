# Parameter and Interaction Authoring Plan

## Goal

Bring GenomeSpy Python's parameter authoring close to Altair's ergonomics while
keeping GenomeSpy Core's schema and runtime semantics as the source of truth.
Users should be able to create typed input bindings, keep a parameter in a
Python variable, attach it with `.add_params()`, and reuse it in expressions,
selection conditions, and selection filters without repeating its JavaScript
name.

This work must not add Vega-Lite features that GenomeSpy Core does not support.
Raw mappings and expression strings remain escape hatches, not the preferred
form in documentation.

## Evidence Reviewed

- Altair's `Parameter`, `param()`, `selection_interval()`, binding helpers,
  `.add_params()`, expression operators, and `when()` implementation in
  `tmp/altair/altair/vegalite/v6/api.py` and `tmp/altair/altair/expr/core.py`.
- Altair's guides for [parameters and filters](https://altair-viz.github.io/user_guide/interactions/parameters.html),
  [bindings and widgets](https://altair-viz.github.io/user_guide/interactions/bindings_widgets.html),
  and [expressions](https://altair-viz.github.io/user_guide/interactions/expressions.html).
- GenomeSpy Core's parameter and conditional-encoding declarations in
  `tmp/genome-spy/packages/core/src/spec/parameter.d.ts` and
  `tmp/genome-spy/packages/core/src/spec/channel.d.ts`, plus the official
  [parameter documentation](https://genomespy.app/docs/grammar/parameters/).
- The pinned 0.86.0 JSON Schema, generated wrappers, generator, tests, user
  guide, and every parameterized gallery example in this repository.

## Current Findings

### Generated types exist, but the public ergonomics stop too early

The generated package already contains `BindRange`, `BindCheckbox`,
`BindRadioSelect`, `BindInput`, `BrushConfig`, `IntervalSelectionConfig`,
`PointSelectionConfig`, `RulerConfig`, and `RulerMarkConfig`. Nested setters
such as `Parameter.ruler(..., mark=...)` are also generated.

However, common examples still use raw mappings because top-level helpers such
as `binding_range()`, `selection_interval()`, and `ruler()` are missing. The
low-level classes are therefore accurate but undiscoverable compared with
Altair's public API.

### The current generated `param()` signature loses union information

`Parameter` is a union of value, expression, selection, and ruler parameter
variants. The generator currently flattens the union into one property set and
lets later variants overwrite earlier property types. As a result, the
generated `value` annotation is effectively the ruler value type even though
examples validly pass numbers, strings, and booleans.

The fix is not another broad `Any` annotation. Parameter construction must
preserve the schema's discriminated branches and instantiate the exact
generated class: `PlainValueParameter`, `TransitionedValueParameter`,
`ExprParameter`, `SelectionParameter`, or `RulerParameter`.

### Python expression support exists but parameters cannot participate in it

`gs.datum`, expression operators, and the generated `gs.expr` function catalog
already work. The earlier expression work did not provide an Altair-style
parameter handle, so examples still create `gs.Expression("parameterName")`
and use JavaScript ternaries manually.

The gallery ternaries are already expressible with the existing generated
function API:

```python
direction = gs.expr.if_(
    (gs.datum.neglog10_pvalue >= significance_cutoff)
    & (abs(gs.datum.log2fc) >= effect_cutoff),
    gs.expr.if_(gs.datum.log2fc < 0, "down in dex", "up in dex"),
    "n.s.",
)
```

The missing capability is for `significance_cutoff` and `effect_cutoff` to be
objects returned by `gs.param()`, rather than separate manually synchronized
`Expression` instances.

### The documentation debt is measurable

The current tutorials and gallery contain:

- 16 raw `bind={...}` mappings;
- 4 raw `ruler={...}` mappings;
- 33 direct `gs.Expression(...)` constructions, including built-in runtime
  variables and named parameters;
- 27 `params=[...]` property lists instead of `.add_params(...)`.

Not every `Expression` is wrong: built-in runtime variables such as
`zoomLevel`, `width`, and `height` are not declared parameters and still need
an explicit expression reference. Declared parameters should no longer repeat
their names as strings.

## Target User API

### Bound value parameter

```python
slider = gs.binding_range(
    min=0,
    max=1,
    step=0.05,
    name="Minimum score: ",
)
min_score = gs.param("minScore", value=0.4, bind=slider)

chart = (
    gs.Chart(data)
    .transform_filter(gs.datum.score >= min_score)
    .mark_point(opacity=min_score)
    .add_params(min_score)
)
```

`param()` should also accept an omitted name and create a deterministic name,
as Altair does. GenomeSpy documentation should continue to prefer explicit
names when parameters are shared across scopes, synchronized with Python, or
persisted by GenomeSpy App.

### Selection, condition, and filter

```python
brush = gs.selection_interval(encodings=["x"], empty=False)

points = (
    gs.Chart(data)
    .mark_point()
    .encode(
        x="position:Q",
        y="score:Q",
        color=(
            gs.when(brush)
            .then("group:N")
            .otherwise(gs.value("lightgray"))
        ),
    )
    .add_params(brush)
)

summary = gs.Chart(data).transform_filter(brush)
chart = points & summary
```

The existing `gs.condition()` helper remains as a compact compatibility form,
but new documentation should prefer `when().then().otherwise()`.

### GenomeSpy ruler

Rulers are GenomeSpy-specific, so they need an analogous helper rather than a
fabricated Altair name:

```python
cursor = gs.ruler(
    "cursor",
    persist=False,
    encodings=["x"],
    extent="container",
    display="line",
    mark=gs.RulerMarkConfig(stroke="#d62728", strokeWidth=1),
)

chart = (top & bottom).add_params(cursor)
```

### Reactive expression parameter

```python
point_size = gs.param(
    "pointSize",
    expr=60 + min_score * 100,
)

chart = chart.mark_point(size=point_size).add_params(min_score, point_size)
```

All of these forms must serialize only native GenomeSpy JSON. Python helper
objects must never leak into the output.

## Architectural Design

### 1. Keep schema breadth generated

Extend `tools/schemapi/codegen.py` and the production configuration in
`tools/generate_schema_wrapper.py` so that public parameter helpers are emitted
from the pinned schema into the existing `schema/ergonomics.py` module. Do not
create a parallel handwritten set of binding, selection-config, or ruler-config
models.

Build a structural parameter-capability model inside stable GenomeSpy grammar
families instead of listing supported features by name. The family anchors are
`Parameter`, `Binding`, `SelectionParameter.select`, `FilterParams`, and
conditional predicates reachable from encoding `condition` properties. Within
those families, the generator must recursively discover:

- every concrete member of the `Parameter` union;
- every concrete member of `Binding` and each literal accepted by its `input`
  discriminator;
- every selection config reachable from `SelectionParameter.select` and each
  literal accepted by its `type` discriminator;
- nested parameter/config pairs such as `RulerParameter.ruler`;
- every filter variant and the required property that distinguishes it; and
- every predicate shape accepted by conditional encodings, including any
  future `test` or predicate-composition definitions.

Public helper names should follow deterministic rules from required schema
discriminators: `input="range"` becomes `binding_range()`,
`type="interval"` becomes `selection_interval()`, and a required `ruler`
config becomes `ruler()`. An optional discriminator remains an argument of a
generic helper, so `BindInput(input="text")` maps to `binding(input="text")`
rather than separate `binding_text()`, `binding_number()`, and
`binding_color()` names. A tiny naming policy may resolve Python keywords or
genuine ambiguity, but it must not enumerate the supported GenomeSpy feature
set.

The initial schema therefore produces these helpers:

| Helper | Schema source | Injected value |
|---|---|---|
| `binding()` | `BindInput` | none |
| `binding_checkbox()` | `BindCheckbox` | `input="checkbox"` |
| `binding_radio()` | `BindRadioSelect` | `input="radio"` |
| `binding_select()` | `BindRadioSelect` | `input="select"` |
| `binding_range()` | `BindRange` | `input="range"` |
| `selection_point()` | `SelectionParameter` + `PointSelectionConfig` | `type="point"` |
| `selection_interval()` | `SelectionParameter` + `IntervalSelectionConfig` | `type="interval"` |
| `ruler()` | `RulerParameter` + `RulerConfig` | none |

The capability manifest and code-generation tests must list the generated
helpers, source definitions, discriminators, condition predicates, filter
variants, and composition operators. Generated top-level exports must come
from the same manifest rather than handwritten lists. A schema addition inside
an anchored family that follows an established protocol must be emitted
automatically with its schema-derived signature, types, documentation, and
exports. Unrelated definitions continue through ordinary wrapper generation
and do not trigger interaction-capability errors.

Keep export generation explicit and lean: update generated import/`__all__`
blocks in the existing public API modules from the manifest. Do not add runtime
`__getattr__`, wildcard-based package magic, or a separate registry module.

If GenomeSpy adds an unmatched leaf inside an anchored family, generation must
fail with an actionable uncovered-capability error. It must not silently omit
the public route, weaken the type to `Any`, or leave dictionaries as the only
route. Supporting a genuinely new protocol should require one generic
generator rule that also covers later features of that shape—not a one-off
GenomeSpy feature adapter.

### 2. Add one Altair-style parameter handle

Add one small handwritten authoring module for behavior the JSON Schema cannot
describe: a `Parameter` handle and the `when/then/otherwise` builder. This is
the same boundary Altair uses: generated objects describe the JSON grammar,
while a handwritten object provides Python expression and chart-attachment
behavior.

`Parameter` should:

- hold the exact generated parameter definition in `.param`, matching Altair;
- expose `.name` and its parameter kind;
- provide its name to the expression operator machinery through a narrow
  `_to_expr()` protocol;
- serialize expression-like value/ruler references as `ExprRef` only in schema
  positions that accept expression references;
- participate in arithmetic, comparisons, boolean expression composition, and
  `abs()` when used as a GenomeSpy expression;
- allow attribute/item access for values such as `cursor.values.y`;
- retain whether an empty selection matches for condition/filter use; and
- use a deterministic schema-definition hash when no name is supplied.

The same handle has context-specific representations: `.add_params()` unwraps
the generated declaration; expression normalization consumes `_to_expr()`;
condition normalization emits selection predicate metadata; and filter
normalization emits a selection-filter transform. Do not make the core
serializer accept arbitrary objects merely because they have `to_dict()`.
Introduce only a narrow parameter-reference protocol or explicit normalization
at those boundaries. Reject a selection in an expression-only position and a
value/ruler parameter in a selection-predicate position. Generated annotations
for `ExprRef`-capable positions must accept the authoring reference through a
cycle-safe protocol or alias.

Refactor the current expression operators into a small shared operator mixin,
following Altair's `OperatorMixin`, so `Expression` and `Parameter` use one
serializer. Do not special-case individual expression functions or transforms.
Selection `&`, `|`, and `~` must not masquerade as filter-predicate composition;
GenomeSpy has no schema representation for those predicates yet.

The generated low-level union wrapper remains available as
`genome_spy.schema.Parameter`. The top-level `gs.Parameter` becomes the
authoring handle returned by `gs.param()` and selection/ruler helpers. This is
an intentional pre-1.0 API correction: direct `gs.Parameter(...)` construction
migrates to `gs.param(...)`. Add a migration note and import-boundary test; do
not add a permanent dual-purpose compatibility constructor.

### 3. Add `.add_params()` once at the common chart layer

Implement `.add_params(*params)` on `TopLevelSpec`, so unit, layer, concat, and
multiscale charts share identical behavior. This is handwritten chart workflow
logic, as it is in Altair; parameter property types and serialized definitions
remain generated.

The method must:

- append each handle's generated `.param` definition immutably;
- accept generated low-level parameter definitions as an escape hatch;
- preserve argument order;
- reject conflicting duplicate explicit names;
- deduplicate repeated hash-named handles by generated name and reject duplicate
  explicit names, matching Altair's rule; and
- work independently at each GenomeSpy parameter scope.

Treat every name on a raw generated parameter definition as explicit for
duplicate detection.

For compatibility, central top-level normalization should also unwrap handles
inside an existing `params=[...]` property. Documentation and gallery code move
to `.add_params()`, but old valid construction does not silently serialize a
parameter as an expression reference.

### 4. Generate parameter construction by schema branch

Replace the current flattened `param()` factory with branch-aware generation.
Implement a reusable union-leaf analyzer that:

1. recursively expands references and nested `anyOf`/`oneOf` branches;
2. merges `allOf` properties and required sets without merging sibling
   alternatives;
3. preserves required properties, discriminator constants/enums, forbidden
   properties, and `additionalProperties` constraints;
4. generates one overload per concrete leaf; and
5. selects the unique compatible leaf at runtime, raising a clear ambiguity or
   no-match error instead of relying on branch order.

For the current parameter family, branch-aware generation means:

- `expr` creates `ExprParameter`;
- `value` without a transition creates `PlainValueParameter`;
- numeric `value` plus `transition` creates `TransitionedValueParameter`;
- `select` creates `SelectionParameter`;
- `ruler` creates `RulerParameter`.

Reject schema-invalid combinations early, including `value` with `expr`,
bindings on expression parameters, and transitions on selections or rulers.
Generated overloads should expose the correct accepted types for each branch
instead of collapsing the union to an inaccurate signature.

Keep `gs.param(select=...)` and `gs.param(ruler=...)` working for compatibility,
but teach new users the clearer `selection_point()`, `selection_interval()`,
and `ruler()` helpers. The selection helpers' Python-only `empty` option is
derived from the generated conditional and selection-filter schemas, where
`empty` is applied when the selection is consumed rather than stored in the
serialized selection definition.

### 5. Integrate parameters with generated transforms

Generate the filter call shape from all members of the schema's filter union.
For the current two variants this means:

- `transform_filter(Expression | str)` serializes an expression filter;
- `transform_filter(selection_parameter)` serializes
  `{ "type": "filter", "param": selection.name }`;
- the existing explicit `param="name"` form remains available.

Passing a value or ruler parameter as a selection filter must fail with a clear
error. Dispatch belongs in the generated filter method because accepted forms
are derived from `FilterParams` members, their required properties, and their
property schemas. If GenomeSpy later adds a Vega-Lite-style predicate or
composition member to that union, regeneration must add the corresponding
typed route without a filter-specific patch.

Generated transform properties whose schema type is an expression string must
normalize expression-capable parameter operands to their name. Properties that
accept `ExprRef` continue to receive the parameter handle directly. Cover both
paths with generation and serialization tests instead of transform-specific
gallery workarounds.

### 6. Add schema-bounded `when().then().otherwise()`

Implement the Altair-shaped builder for the conditional structures that
GenomeSpy actually supports:

```python
gs.when(selection).then(gs.value("red")).otherwise(gs.value("gray"))
```

The builder should accept selection parameters, preserve `empty`, normalize
field shorthand and channel/value objects, and produce a neutral schema-shaped
condition payload. Multiple selection branches may be supported where the
target channel schema permits a condition array.

The builder must consume a compact generated predicate-capability description
rather than hardcode `param` as the only possible predicate. With the current
schema it accepts only selection predicates and must not emit Vega-Lite's
`{ "test": ... }` form. If GenomeSpy later adds `test` conditions or predicate
compositions under the anchored conditional-predicate family, regeneration
must extend the predicate union and `when()` typing automatically.

The handwritten `When`/`Then` state machine manages chaining and assembles a
neutral condition payload because the destination channel is not yet known at
`.then()` time. Generated predicate capabilities determine which predicates
are accepted; existing generated channel definitions and final root validation
determine whether the branch and fallback are legal for the destination
channel. Do not generate an adapter for every channel-specific
`ConditionalParameter*` instantiation.

## Generalization Contract for Future GenomeSpy Releases

Schema upgrades must follow this pipeline:

```text
GenomeSpy schema change
        ↓
anchored-family protocol discovery
        ↓
generated wrappers + helper signatures + predicate/filter adapters
        ↓
capability manifest completeness check
        ↓
existing handwritten Parameter / When / Then workflow
```

The generator must cover future additions by protocol inside the anchored
families. Declaration and consumption capabilities are discovered separately:
membership in `Parameter` proves that a definition can be declared, while
expression-reference, condition-predicate, and filter behavior must each be
reachable from their corresponding consumer schema.

| Upstream addition | Expected regeneration result |
|---|---|
| Property added to a binding | Existing `binding_*()` signatures and docs gain it |
| New literal in an optional generic binding discriminator | The generated `binding()` signature expands |
| New literal in a required binding discriminator | A typed specialized helper is emitted |
| Property added to point/interval selection config | Existing `selection_*()` signature gains it |
| New selection `type` config | A typed `selection_<type>()` helper is emitted |
| New parameter union leaf matching an established declaration protocol | An exact generated constructor route is emitted |
| Parameter leaf becomes reachable through an expression/condition/filter consumer | Only that usage adapter is added |
| New filter union member | `transform_filter()` gains a generated overload and serializer branch |
| `test` added to conditional predicates | `when(expression)` becomes available through generated predicate typing |
| Predicate composition added | Generated predicate adapters expose only the composition operators in the schema |

Do not use Vega-Lite's schema as a second source of truth. GenomeSpy may adopt
similar features with different constraints. Altair guides the Python shape;
the pinned GenomeSpy schema decides whether a feature exists and exactly which
arguments it accepts.

Add synthetic-schema generator tests for each row above. These fixtures should
add a hypothetical property or union member to a minimal schema and assert that
the generated API expands without editing a feature allowlist. This is the
proof that future upstream additions generalize rather than merely working for
GenomeSpy 0.86.0.

For additions that use an established family protocol, the upgrade workflow must
be only: update the pinned GenomeSpy version, regenerate, and review the
generated diff. No handwritten helper registry, public export list, overload
table, predicate dispatch, or serializer branch should need a corresponding
edit. The capability-manifest diff should make newly discovered API visible in
review. A handwritten change is justified only when the upstream schema
introduces a genuinely new protocol or runtime semantic that its consumer
schemas do not express.

## Explicit GenomeSpy Boundaries

The following Altair features are not part of this implementation because the
GenomeSpy 0.86.0 schema/runtime does not provide the corresponding grammar:

| Altair feature | GenomeSpy status | Supported alternative |
|---|---|---|
| `when(datum.x > cutoff)` test conditions | Conditional encodings accept selection `param`, not `test` | Use `gs.expr.if_()` for expression-valued properties or a formula transform that derives a field |
| `brush & brush2`, `brush | brush2`, `~brush` as filter predicates | Selection filters accept one parameter name | Use one selection or restructure the dataflow; wait for upstream predicate composition |
| `selection_interval(bind="scales")` | No selection scale binding | Use GenomeSpy zoomable scales and `SelectionDomainRef` for overview/detail linking |
| Vega-Lite selection `fields`, `nearest`, and `resolve` options | Absent from GenomeSpy selection configs | Use GenomeSpy's encoded/keyed point selection semantics |
| Arbitrary HTML element bindings | Core schema exposes built-in input bindings only | Use `binding()`, checkbox, radio, select, and range helpers |

`SelectionDomainRef` remains the native way to connect a brush to a scale.
Because GenomeSpy adds `initial` and hierarchical `push="outer"` semantics,
the first implementation should keep this explicit rather than pretending
that `scale(domain=brush)` is always equivalent.

## Implementation Phases

### Phase 1: Lock down current schema behavior

1. Add focused tests demonstrating the inaccurate current `param()` value
   annotation and each concrete parameter variant.
2. Add golden serialization tests for bindings, point/interval selections,
   rulers, selection filters, conditional encodings, transitions, and
   `push="outer"`.
3. Add negative tests for unsupported combinations and unsupported Altair
   predicate forms.

### Phase 2: Generate typed factories

1. Add the reusable union-leaf analyzer and anchored-family discovery for
   parameter, binding, selection, filter, and conditional-predicate
   capabilities.
2. Generate binding factories and branch-aware parameter/config construction
   into `schema/ergonomics.py` without a feature allowlist.
3. Generate predicate/filter capability descriptions from their consumer
   schema families, independently of parameter declarations.
4. Generate ergonomic public exports from the discovered helper manifest.
5. Record discovered and emitted capabilities in `capabilities.json`, and fail
   if an anchored-family leaf has no generated route.
6. Add synthetic future-schema tests for nested unions, inherited properties,
   shared and optional discriminators, multiple required properties, ambiguous
   leaves, new properties, new leaf variants, and predicate shapes.
7. Regenerate committed schema artifacts and verify a no-diff second run.

### Phase 3: Add the parameter authoring layer

1. Introduce the shared expression operator mixin and `Parameter` handle.
2. Make generated `param()`, selection helpers, and `ruler()` return the handle.
3. Add `.add_params()` to the common top-level chart API.
4. Normalize handles in legacy `params=[...]` input centrally.
5. Add generated selection-filter dispatch.

### Phase 4: Add conditional ergonomics

1. Implement `when().then().otherwise()` for selection predicates.
2. Reuse generated conditional definitions and channel shorthand parsing.
3. Route `condition()` through the same normalization path while preserving its
   existing compact signature.
4. Test value, field, datum, expression, empty-selection, fallback, and
   permitted multi-branch cases across numeric and string channels.

### Phase 5: Migrate documentation and gallery

1. Rewrite `docs/user-guide/interaction.md` around the new public contract:
   value parameters, bindings, `.add_params()`, expressions, point/interval
   selections, selection conditions, selection filters, linked genomic
   brushes, rulers, and parameter scope.
2. Keep the prose at the same concise, technical level as the rest of the user
   guide: explain each concept for a Python user without reproducing the full
   GenomeSpy runtime model.
3. Update `docs/user-guide/transforms.md` so named parameters no longer require
   raw expression strings when a handle is available.
4. Migrate all 16 raw binding mappings and 4 ruler mappings in tutorials and
   gallery examples to typed helpers.
5. Migrate repository examples from `params=[...]` to `.add_params(...)` where
   they define authored parameters. Leave transform properties named `params`
   untouched.
6. Rewrite the Manhattan, both volcano, and MA threshold examples so the
   parameter objects drive guide lines, filters, and Python-authored
   `gs.expr.if_()` expressions. Remove their JavaScript ternaries and duplicate
   `Expression("parameterName")` values.
7. Replace other direct `Expression("parameterName")` instances when the
   parameter is declared in Python. Retain explicit expressions for GenomeSpy
   built-ins and runtime-only names, with a short comment where their origin is
   not obvious.
8. Add API-reference entries for `Parameter`, binding helpers, selection
   helpers, `ruler`, and `when` without duplicating the user guide. Re-export
   schema-generated configuration objects used directly by these helpers,
   including `BrushConfig` and `RulerMarkConfig`.
9. Update `plans/architecture.md` with the anchored-family generation contract,
   union-leaf analysis, and the boundary between generated grammar objects and
   handwritten authoring behavior.

### Phase 6: Verify runtime behavior

1. Run targeted schema-codegen, expression, chart, interaction tutorial, and
   gallery tests.
2. Run schema regeneration twice and the tracked-artifact freshness check.
3. Run Ruff, mypy, the full pytest suite, JavaScript widget tests, and the
   strict Sphinx build.
4. Open the rendered interaction guide and parameterized gallery charts in a
   browser. Exercise sliders, point selections, interval brushes, conditional
   styling, linked filtering, rulers, and zoom-linked domains.
5. Refresh thumbnails only if the rendered default view changed; do not replace
   good thumbnails merely because source code changed.

## Acceptance Criteria

- The documented slider pattern uses `binding_range()`, a reusable parameter
  object, and `.add_params()` with no raw mapping or repeated parameter name.
- `gs.param()` values and overloads accurately represent all generated
  GenomeSpy parameter branches.
- `gs.selection_point()`, `gs.selection_interval()`, and `gs.ruler()` serialize
  native generated parameter definitions.
- Declared parameters participate in Python-authored expressions and direct
  expression-reference properties.
- Each parameter kind has tested declaration, expression-reference,
  condition-predicate, and filter representations; unsupported contexts reject
  it before serialization, and no authoring handle leaks into JSON.
- `transform_filter(brush)` emits a native selection filter, while expression
  filters continue to accept `gs.datum` expressions.
- `gs.when(brush).then(...).otherwise(...)` works for every conditional branch
  shape accepted by the pinned GenomeSpy schema and rejects unsupported test
  predicates clearly.
- Existing `.properties(params=[...])` code remains valid during migration.
- The Manhattan, two volcano, and MA examples contain no JavaScript ternary or
  duplicated parameter-name expressions.
- Generated helpers, signatures, docs, and capability metadata reproduce
  deterministically from the pinned schema.
- Synthetic future-schema tests prove that established-protocol binding,
  selection, parameter, filter, and conditional additions expand the public API
  without editing a feature allowlist.
- For an established-protocol upstream addition, changing the pinned GenomeSpy
  version and regenerating is sufficient; public exports, signatures, adapters,
  and capability metadata update together.
- An unsupported novel schema shape fails generation as an uncovered
  capability instead of silently degrading to `Any` or raw dictionaries.
- No new interaction semantics are invented in Python, and no Python helper
  object appears in serialized JSON.

## Commit Strategy

Keep the PR reviewable with small thematic commits:

1. `test(params): capture schema branches and interaction contracts`
2. `feat(codegen): discover parameter interaction capabilities`
3. `feat(params): add parameter handles and chart attachment`
4. `feat(interaction): add selection conditions and filters`
5. `docs(interaction): migrate parameter guide and gallery examples`
