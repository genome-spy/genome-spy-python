# Transform Authoring Plan

## Goal

Make common transform calls concise and familiar while keeping GenomeSpy Core's
schema as the source of truth. Transform methods must be generated from the
pinned schema; handwritten runtime translation layers are out of scope.

## Evidence Reviewed

- GenomeSpy's generated transform methods and Core transform definitions;
- Altair's schema generator, override registry, and handwritten top-level API;
- the packaged GenomeSpy and Vega-Lite schemas; and
- the transform APIs exercised by this repository's tests and examples.

Altair separates generated schema classes from selected API customizations. We
follow the same explicit-override principle, but generate the selected transform
methods too. This gives static signatures, keeps regeneration deterministic,
and makes schema drift fail in the generator instead of at runtime.

## Architectural Decision

`tools/generate_schema_wrapper.py` owns a small transform-method override
registry and supplies it to the generic machinery in
`tools/schemapi/codegen.py`. Each entry may only:

- make schema properties positional;
- expose a Python parameter alias for a schema property; or
- emit an additional method from an existing transform definition.

Every referenced property must exist in the upstream schema. Its annotation and
documentation remain schema-derived, and the generated method must serialize a
native GenomeSpy transform. Generated output is committed in
`src/genome_spy/schema/mixins.py` and exposed directly by `Chart` through
`TransformMethodMixin`.

The production generation entry point explicitly supplies the override
registry. Generic generator consumers may omit it. Generation fails when an
override's schema is no longer a member of `TransformParams` or when two
transforms would emit the same Python method name.

Do not add a runtime adapter, parallel normalization model, or transform
definition invented solely in Python. If a convenience cannot be described by
the transform's schema properties plus a small generation rule, defer it until
the schema or generator has a principled representation.

## Initial Generated Scope

| Method | Generation rule | Serialized result |
|---|---|---|
| `transform_calculate()` | Additional method generated from `FormulaParams`; `expr` is named `calculate`, and output keywords repeat the same formula template | One `formula` transform per output |
| `transform_flatten()` | Generate `fields` and `as_` as positional-or-keyword parameters | Native `flatten` transform |
| `transform_sample()` | Generate `size` as positional-or-keyword | Native `sample` transform; an omitted size retains Core's default |

The native `transform_formula()` remains available. The generated calculate
method supports both a direct pair and ordered output keywords:

```python
chart.transform_calculate(as_="double_x", calculate="datum.x * 2")
chart.transform_calculate(
    x="cos(datum.t * PI / 50)",
    y="sin(datum.t * PI / 25)",
)
```

## Deliberately Deferred

Aggregate, filter, lookup, stack, and window shorthands are not part of this
slice. Their alternate Python call shapes require parsers, cross-property
normalization, or foreign object models that the GenomeSpy schema does not
describe. The generated native methods remain the supported API.

Likewise, do not emulate transforms absent from GenomeSpy Core. Bin, density,
extent, fold, impute, joinaggregate, loess, pivot, quantile, regression, and
time-unit operations require renderer support or explicit preprocessing.

An expression-object API is a separate design problem. It should be considered
only against GenomeSpy's supported expression runtime, not copied wholesale
from another grammar.

## Future Core Upgrades

A new object included in the upstream `TransformParams` union automatically
receives a typed `transform_<type>()` method, schema-derived documentation, and
a capability-manifest entry. No registry entry is needed for the native method.

If the new transform uses one of the established Python call shapes, a small
registry entry can select positional properties, aliases, or an additional
method template. Call shapes that require parsing or relationships absent from
the schema need a deliberate new generation rule; they are not inferred or
implemented at runtime.

## Implementation Steps

1. Add schema-checked method overrides to the generator.
2. Regenerate the transform mixin and capability manifest.
3. Remove the handwritten transform mixin and normalization helpers.
4. Test generated source metadata, public signatures, serialization,
   immutability, ordering, errors, and the Core sample default.
5. Run generator freshness, formatting, lint, typing, and the full test suite.

## Acceptance Criteria

- `Chart` inherits the generated `TransformMethodMixin` directly.
- No handwritten transform-authoring layer is required for this scope.
- Regeneration reproduces all public transform signatures.
- An upstream override target rename or removal causes a clear generation
  error.
- Duplicate method names fail generation instead of silently shadowing one
  another.
- Existing native transform methods and serialized GenomeSpy semantics remain
  unchanged.
- Documentation describes only behavior covered by generated tests.
