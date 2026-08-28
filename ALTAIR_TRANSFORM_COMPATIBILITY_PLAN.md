# Altair Transform Compatibility Evaluation and Plan

## Goal

Make GenomeSpy's Python transform API more familiar to Altair users where a
Python-side adapter can preserve GenomeSpy semantics exactly. This is an API
compatibility effort, not an attempt to make GenomeSpy execute arbitrary
Vega-Lite specifications.

## Sources Reviewed

- the discussion with Kari Lavikka from 28 August 2026;
- `src/genome_spy/schema/mixins.py` and the transform schemas and runtime code
  in `tmp/genome-spy`;
- `tmp/altair/altair/vegalite/v6/api.py` and Altair's expression package;
- the packaged GenomeSpy and Vega-Lite JSON schemas; and
- the existing architecture and Altair-alignment plans in this repository.

The Altair reference checkout is v6.2.2 plus three commits. The GenomeSpy
checkout was last updated at commit `2a670d4f` from 11 August 2026.

## Executive Verdict

The package is **Altair-like, but not transform-API-compatible with Altair**.

- Altair exposes 19 `transform_*` methods.
- genome-spy-python exposes 31 methods generated from GenomeSpy Core.
- Only seven method names overlap: `aggregate`, `filter`, `flatten`, `lookup`,
  `sample`, `stack`, and `window`.
- `transform_calculate()` and `transform_formula()` provide the same underlying
  operation under different names, bringing the meaningful overlap to eight
  transforms.
- Of those eight, none is fully call-compatible today. `filter` comes closest
  for a positional expression string.

Calling the package a drop-in replacement for Altair would therefore be
misleading. The chart-building style is familiar, but an Altair chart that
uses transforms will usually need edits, and 11 Altair methods have no direct
GenomeSpy method counterpart. One of those, `joinaggregate`, can be represented
faithfully with GenomeSpy's window transform; the other ten require renderer
support or Python-side data preparation.

The encouraging finding is that the most commonly useful overlaps are real,
not superficial. Formula/calculate, filtering, aggregation, flattening,
sampling, stacking, windowing, and ordinary data lookup can all gain a more
Altair-like Python call shape without changing the JSON that GenomeSpy
executes.

## Second-Pass Review Findings

A second scan of Altair's transform tests and shorthand parser, GenomeSpy's
generated MRO, and the JavaScript transform implementations changed the first
draft in several material ways:

- aggregate `count()` compatibility is narrower than the schemas initially
  suggest because the Core aggregate runtime reserves fieldless aggregation
  for one output named `count`;
- joinaggregate remains a sound window translation, including fieldless
  count, because GenomeSpy's window contract permits `null` fields;
- true `transform_sample()` call compatibility requires an explicit 1000-row
  Python default, not preservation of Core's 500-row default;
- a string stack output must be expanded to two GenomeSpy output names rather
  than forwarded directly;
- positional parameter filtering is safe only for actual selection
  parameters, and interval selections still require an explicit channel-to-
  field projection;
- Altair's expression namespace is much broader than GenomeSpy's. Only the
  verified runtime intersection should be exposed; and
- a handwritten mixin should inherit the generated transform mixin rather than
  coexist with it as a second direct base of `TopLevelSpec`.

These corrections reduce the amount of compatibility that can honestly be
called drop-in, but they make the proposed subset implementable without hidden
browser-time differences.

## Transform-by-Transform Comparison

| Altair method | GenomeSpy support | Compatibility today | Assessment |
|---|---|---|---|
| `transform_aggregate` | `transform_aggregate` | Same broad operation; incompatible argument shape | Strong but bounded adapter candidate. Altair accepts field definitions or `output="op(field)"`; GenomeSpy uses parallel `fields`, `ops`, and `as_` arrays. GenomeSpy supports only a subset of Altair's aggregate operations, and Core cannot currently represent an arbitrarily named fieldless `count()` alongside other aggregate outputs. |
| `transform_bin` | None | None | Renderer feature, not Python sugar. Do not add an adapter until GenomeSpy Core has binning. |
| `transform_calculate` | `transform_formula` | Same semantics; different name and arguments | Best low-hanging fruit. An alias can translate one or many calculated fields into consecutive GenomeSpy formula transforms. |
| `transform_density` | None | None | Statistical renderer feature. Keep preprocessing in Python unless Core gains the transform. |
| `transform_impute` | None | None | No faithful adapter. Python preprocessing is the honest alternative. |
| `transform_joinaggregate` | `transform_window` | No direct method, but the operation is representable | Good compatibility helper for supported aggregate ops: emit a window transform with `frame=[None, None]`. |
| `transform_extent` | None | None | Altair writes an extent to a parameter; GenomeSpy has no corresponding transform. |
| `transform_filter` | `transform_filter` | Positional strings work; most Altair predicate forms do not | High-value partial compatibility. GenomeSpy supports expression strings and selection parameters, including projected selection fields, but not Vega-Lite structured field predicates or Altair's predicate composition API. |
| `transform_flatten` | `transform_flatten` | Same semantics; incompatible parameter name/position | Very small adapter. Altair's positional `flatten` can map to GenomeSpy's `fields`; GenomeSpy additionally supports an index output. |
| `transform_fold` | None | None | `transform_regex_fold` is specialized and is not a general Vega-Lite fold. It must not be advertised as equivalent. |
| `transform_loess` | None | None | Statistical renderer feature; not safely emulatable with Python-side spec rewriting. |
| `transform_lookup` | `transform_lookup` | Related data-lookup semantics; different object model | Medium effort. GenomeSpy supports ordinary data lookups and composite keys, but not Altair/Vega-Lite selection lookup. The `from_`, key, input-field, and copied-value structures differ. |
| `transform_pivot` | None | None | No renderer equivalent. Use prepared data in Python. |
| `transform_quantile` | None | None | No renderer equivalent. Use prepared data in Python. |
| `transform_regression` | None | None | No renderer equivalent. Use prepared data in Python. |
| `transform_sample` | `transform_sample` | Same operation; incompatible positional argument and default | Easy adapter, but true call compatibility requires the Python helper to emit Altair's 1000-row default instead of relying on GenomeSpy Core's 500-row default. |
| `transform_stack` | `transform_stack` | Closely related semantics; incompatible names and sort shape | Good adapter candidate. `stack` maps to `field`; Altair sort definitions can become GenomeSpy's compare object. GenomeSpy also has the extra `information` offset. |
| `transform_timeunit` | None | None | No faithful browser-side equivalent. Simple cases could be formulas, but a general alias would promise unsupported date semantics. |
| `transform_window` | `transform_window` | Same Vega-style model; incompatible field-definition shape | Strong adapter candidate. Altair uses per-output definitions or shorthand kwargs; GenomeSpy uses aligned arrays. Operation sets overlap substantially but are not identical. |

### Aggregate operation coverage

GenomeSpy supports 10 aggregate operations: `count`, `valid`, `sum`, `min`,
`max`, `mean`, `q1`, `median`, `q3`, and `variance`. All ten exist in Altair,
but Altair additionally exposes operations such as `argmax`, `argmin`,
`distinct`, `missing`, `product`, confidence intervals, standard deviations,
and `values`.

Compatibility shorthand must fail early when an Altair operation is not
implemented by GenomeSpy. It must not silently substitute a similar operation
unless that alias is an explicitly documented compatibility rule. One useful
rule is `average` to `mean`: Vega-Lite treats these as equivalent aggregate
names, while GenomeSpy exposes only `mean`.

There is one additional Core limitation. GenomeSpy's aggregate runtime treats
the complete absence of `fields` as one default output named `count`. It cannot
faithfully translate a general Altair aggregate such as
`rows="count()"` mixed with other outputs. The adapter may support the exact
special case `count="count()"`, but other fieldless-count forms must fail until
Core can represent fieldless operations in its aligned arrays. Window and
joinaggregate do not have this limitation because GenomeSpy window fields may
contain `null`.

### Window operation coverage

The window models are unusually well aligned. GenomeSpy explicitly follows
Vega's partition, sort, frame, peer, and operation contract. It supports all of
Altair's window-only operations and adds `prev_value` and `next_value`.
Aggregate operations inside windows remain limited to GenomeSpy's smaller
aggregate set.

This makes call-shape translation safe for supported operations. It does not
justify accepting unsupported Altair operation names.

### Filter and expression compatibility

The current convenient overlap is:

```python
chart.transform_filter("datum.year == 2000")
```

Both libraries ultimately run a JavaScript-like visualization expression in
the browser. However, Altair additionally offers:

- a Python expression builder (`alt.datum.year == 2000`);
- positional composition of several predicates;
- keyword equality constraints (`year=2000`);
- structured Vega-Lite field predicates; and
- selection predicates through Altair parameter wrapper objects.

GenomeSpy Core supports expression filtering and its own selection-parameter
filtering, including a `fields` projection for positional channels. It does
not support the general Vega-Lite structured-predicate grammar. The Python API
should expose only the overlap.

There is a useful compatibility opportunity in the existing `datum` and
`expr` names:

- `gs.datum(value)` already constructs a constant-datum encoding;
- `gs.expr("...")` already constructs a schema expression reference.

They can become callable expression namespaces without breaking those call
forms. `gs.datum.x` could create a field expression while `gs.datum(5)` keeps
its current encoding behavior. Likewise, `gs.expr.cos(...)` and
`gs.expr.PI` can coexist with `gs.expr("width / 2")`.

The expression namespaces must be derived from GenomeSpy's supported
expression runtime, not copied wholesale from Altair. The second code scan
found about 65 documented function/constant names shared by Altair and
GenomeSpy, but Altair exposes many Vega functions that GenomeSpy does not,
especially date/time, statistics, color, geo, scenegraph, and event helpers.
The motivating `sin`, `cos`, `PI`, arithmetic, and Boolean expressions are in
the verified intersection.

## Recommended Compatibility Boundary

Adopt this public claim:

> genome-spy-python follows Altair's chart-authoring style and accepts
> Altair-like calls for selected transforms that GenomeSpy Core can represent.
> It is not a drop-in Altair or Vega-Lite replacement.

Use three labels in documentation and tests:

1. **Call-compatible subset** — an ordinary Altair call works unchanged apart
   from importing `genome_spy as gs`.
2. **Familiar alias** — the method name and intent match, but unsupported
   options or renderer differences are documented.
3. **GenomeSpy-native only** — no Altair compatibility claim.

Never add a method that serializes to a different operation merely because the
name sounds similar. In particular, `regex_fold` is not `fold`, and formulas
are not a general replacement for binning or time units.

## Low-Hanging Fruits, Prioritized

### P0: Add `transform_calculate()`

Support both Altair forms:

```python
chart.transform_calculate(as_="double_x", calculate="datum.x * 2")
chart.transform_calculate(
    x="cos(datum.t * PI / 50)",
    y="sin(datum.t * PI / 25)",
)
```

Each output becomes one GenomeSpy formula transform, in keyword insertion
order. Retain `transform_formula()` as the GenomeSpy-native method.

Why first: exact semantics, tiny implementation, high visibility, and it
directly addresses the motivating conversation.

### P0: Accept Altair's flatten call shape

Allow:

```python
chart.transform_flatten(["items"], as_=["item"])
chart.transform_flatten(["items"], ["item"])
```

Allow both Altair positional arguments while preserving the current
`fields=...` spelling and GenomeSpy's optional `index`. Reject simultaneous
`flatten=` and `fields=` values or duplicate positional/keyword output names.

### P0: Accept a positional sample size

Allow `chart.transform_sample(1000)` as an alias for `size=1000` and preserve
`size=`. Because the package has not made its first public release, adopt
Altair's behavior for the Python convenience method: `transform_sample()`
should explicitly emit `size=1000`. Users can request GenomeSpy Core's native
default with `size=500` or a raw transform. If changing the current no-argument
behavior is rejected, label this only a familiar alias, not a call-compatible
subset.

### P1: Add conservative aggregate shorthand

Allow supported Altair-style keyword aggregates:

```python
chart.transform_aggregate(
    mean_response="mean(response)",
    groupby=["group"],
)
```

Translate them to aligned GenomeSpy arrays. Use a small, strict parser for the
`op(field)` form and validate the operation against GenomeSpy's generated
operation type. Continue to support the native `fields`, `ops`, and `as_`
arguments.

Also accept an `aggregate=` sequence of ordinary mappings shaped like
`{"op": "mean", "field": "response", "as": "mean_response"}`. Do not
accept Altair schema instances. Reject mixing `aggregate=` definitions with
the native aligned-array form; kwargs may be appended after explicit mappings,
matching Altair's ordering behavior.

Map the explicit compatibility alias `average` to GenomeSpy's `mean`. Apply
the fieldless-count restriction described above.

Do not import Altair or accept Altair schema instances. Compatibility should
be expressed through ordinary Python values owned by this package.

### P1: Add `transform_joinaggregate()` through window

Reuse the aggregate shorthand parser and plain-mapping definitions, and emit:

```json
{
  "type": "window",
  "ops": ["sum"],
  "fields": ["response"],
  "as": ["total_response"],
  "groupby": ["group"],
  "frame": [null, null]
}
```

This is semantically faithful because GenomeSpy's window implementation
preserves input rows and supports unbounded frames. Limit it to supported
aggregate operations.

### P1: Add Altair-style window shorthand and sort normalization

Allow:

```python
chart.transform_window(
    rank="rank()",
    running_total="sum(value)",
    sort=[{"field": "date", "order": "ascending"}],
)
```

Translate output definitions to GenomeSpy's aligned `ops`, `fields`, `params`,
and `as_` arrays, and translate a list of Altair-like sort mappings to one
GenomeSpy compare mapping. Preserve the native aligned-array form.

Accept a `window=` sequence of ordinary mappings as well as shorthand kwargs.
Normalize omitted sort orders to `ascending` before creating parallel
GenomeSpy `field` and `order` arrays. Allow empty fields only for genuinely
fieldless window operations. Apply the documented `average` to `mean` alias.

### P1: Add the basic expression builder

Implement a small expression AST with:

- `gs.datum.field` and `gs.datum["field with spaces"]`;
- arithmetic, comparison, Boolean, unary, and power operators;
- JavaScript-safe literals for strings, booleans, `None`, and numeric scalars;
- a callable `gs.expr(...)` namespace;
- common GenomeSpy/Vega expression functions, including `sin`, `cos`, `abs`,
  `pow`, and `if_`; and
- common constants, starting with `PI`.

Both `transform_filter()` and `transform_calculate()` should accept expression
objects and serialize them to strings. Keep raw expression strings fully
supported.

This is larger than the method aliases but provides the strongest subjective
familiarity gain for Altair users.

Do not include Altair's date/datetime literal conversion in the first slice.
GenomeSpy's documented expression surface does not currently promise the same
date/time function set. Expand the namespace from an explicit verified list;
do not dynamically accept arbitrary function names, because that would turn
typos and unsupported Altair functions into browser-time failures.

### P1: Normalize the stack call shape

Accept Altair's `stack=` alias for GenomeSpy's `field=`, an Altair-like sort
list, and a single output base name. Preserve GenomeSpy-native extras such as
the `information` offset. Fail on ambiguous duplicate arguments.

For a single Altair output name such as `as_="stacked"`, expand the GenomeSpy
output array to `["stacked", "stacked_end"]`. Passing the string through
directly would be invalid against the GenomeSpy schema and would be misread
character-by-character by the current JavaScript runtime.

### P2: Improve filter convenience within Core's grammar

After the expression builder exists, accept:

```python
chart.transform_filter(gs.datum.year == 2000)
chart.transform_filter(gs.datum.year > 1980, gs.datum.age != 90)
chart.transform_filter(year=2000, sex=1)
```

Combine multiple expressions and equality constraints with `&&`. Also accept
a GenomeSpy `Parameter` positionally only when its serialized definition has a
`select` property; extract its name and emit a selection filter. Reject value,
expression, transition, and ruler parameters in that position. Do not add
Vega-Lite `FieldEqualPredicate`, range predicates, or logical predicate schema
classes until GenomeSpy Core supports them. Preserve the existing `fields=`
argument because interval-selection filters require at least one primary
positional-channel mapping at runtime.

### P2: Evaluate a constrained lookup adapter

Support Altair-like names only for ordinary data lookup where the mapping is
unambiguous: explicit foreign `key`, explicit copied `values`, and a matching
output-name list. Explicitly exclude selection lookup and Altair's single
`as_` form that stores a whole foreign object, because GenomeSpy's lookup
writer has different output semantics. This should follow the first release
wave because a superficial adapter would be easy to misunderstand.

## Architecture

Keep Altair compatibility policy out of the schema generator's generic path.
The generator should continue to produce exact GenomeSpy transform methods
from the Core schema.

Add a small handwritten compatibility layer, for example:

- `src/genome_spy/_transform_compat.py` for the compatibility mixin and strict
  shorthand normalization;
- `src/genome_spy/expressions.py` for expression values and namespaces; and
- `AltairTransformCompatMixin(TransformMethodMixin)` so it inherits the full
  generated GenomeSpy surface and overrides only methods whose call shapes need
  widening; and
- `TopLevelSpec(..., AltairTransformCompatMixin)` in place of its direct
  `TransformMethodMixin` base.

This matches the repository's established rule: schema coverage remains
generated, while workflow ergonomics and transform convenience remain
handwritten. It also avoids accumulating transform-specific branches in
`tools/schemapi/codegen.py`, which currently has only a small filter exception.

Compatibility methods must append ordinary GenomeSpy transform mappings via
the existing `_append_transform()` boundary. They should not introduce a
second transform representation.

The generator currently contains a filter-specific positional-expression
exception. Once the handwritten layer owns the widened filter call shape,
revisit that exception: keep only the union validation needed to enforce
`expr` versus `param`, and move Altair-facing positional policy out of generic
generation.

## Implementation Plan

### Phase 1: Exact, small aliases

1. Add the compatibility mixin and focused normalization helpers.
2. Implement `transform_calculate()` with single-output and multi-output
   forms.
3. Widen `transform_flatten()` and `transform_sample()` to accept Altair's
   simple positional forms while retaining native arguments.
4. Add serialization, immutability, duplicate-argument, ordering, and signature
   tests.

Success criteria:

- Kari's multi-field calculate example serializes to two consecutive formula
  transforms when expressions are provided as strings;
- existing GenomeSpy calls serialize unchanged except for the deliberate,
  documented no-argument sample default; and
- schema regeneration still produces a complete native transform surface.

### Phase 2: Shared operation shorthand

1. Implement a strict `op(field)` / `op()` parser.
2. Add aggregate mappings and kwargs for GenomeSpy-supported operations.
3. Add `transform_joinaggregate()` as an unbounded window adapter.
4. Add window mappings, kwargs, and Altair-like sort-list normalization.
5. Add stack aliases using the same sort-list normalizer.
6. Add negative tests for every unsupported operation and malformed shorthand.

Success criteria:

- common Altair aggregate, joinaggregate, and window examples port with only
  the import changed;
- the basic Altair positional stack example ports with only the import changed;
- unsupported Vega-Lite operations fail in Python with contextual messages;
  and
- emitted JSON validates against the packaged GenomeSpy schema.

### Phase 3: Expression ergonomics

1. Implement the expression AST and literal serialization.
2. Turn `datum` into a callable expression namespace without breaking constant
   datum encodings.
3. Turn `expr` into a callable function/constant namespace without breaking
   `ExprRef` construction.
4. Accept expression values in calculate and filter adapters.
5. Add expression-based filter composition and equality constraints.

Success criteria:

- the exact expression-object form of the `cos`/`sin`/`PI` example from the
  conversation works;
- raw strings remain byte-for-byte unchanged in serialized transforms;
- string quoting, `None`, booleans, item access, and operator precedence
  have focused tests; and
- current `gs.datum(...)` and `gs.expr(...)` uses remain compatible.

### Phase 4: Remaining overlapping transforms

1. Design and test the ordinary-data subset of lookup compatibility.
2. Document the exact compatibility matrix in the transform user guide.
3. Port two or three Altair transform examples as compatibility tests, not as
   a promise that the full Altair gallery works.

Success criteria:

- every overlapping transform is labeled as call-compatible, familiar alias,
  or GenomeSpy-native;
- selection lookup and structured Vega-Lite predicates remain explicitly out
  of scope; and
- documentation never describes the package as a drop-in replacement.

## Testing Strategy

For every adapter, test four layers:

1. **Translation unit tests** for shorthand, expression, sort, and duplicate
   argument normalization.
2. **Serialization tests** asserting the exact GenomeSpy transform list and
   pipeline order.
3. **Schema validation tests** using normal `Chart.to_dict()` validation.
4. **Renderer smoke tests** for representative expression and translated
   pipeline behavior, because JSON Schema cannot validate expression syntax or
   prove that an unbounded window behaves as intended.

Add regression tests proving that existing GenomeSpy-native calls produce the
same dictionaries as before. Where an adapter claims Altair call compatibility,
copy a small call from Altair's own tests or documentation and assert the
equivalent GenomeSpy JSON; do not depend on Altair at runtime.

## Explicit Non-Goals

- accepting arbitrary Altair chart or schema objects;
- serializing Vega-Lite transform JSON directly into a GenomeSpy spec;
- implementing missing renderer transforms only in the Python wrapper;
- reproducing all of Altair's structured predicate types;
- treating `regex_fold` as general fold;
- silently preprocessing user data in Python when a browser-side transform is
  unavailable; or
- claiming drop-in compatibility based only on similar method names.

## Recommended First Implementation Slice

Land Phase 1 as one focused change. It delivers the two clearest wins from the
conversation—`transform_calculate()` and multiple calculated fields—plus the
nearly free flatten and sample call forms. It also establishes the handwritten
compatibility boundary before the more consequential shorthand and expression
work begins.
