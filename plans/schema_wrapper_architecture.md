# Schema Wrapper Architecture

## Goal

`genome-spy-python` should follow Altair's core architecture: generated schema
bindings provide broad, accurate coverage of the upstream JSON grammar, and a
smaller handwritten API provides the pleasant Python surface.

For GenomeSpy, the source of truth is the version-pinned npm package:

```text
@genome-spy/core@<version>
```

The version is configured in `pyproject.toml`:

```toml
[tool.genome-spy]
core-version = "0.81.0"
```

The npm package contains:

- `dist/schema.json`: the generated JSON Schema used for Python codegen.
- `dist/src/spec/*.d.ts`: compact TypeScript spec declarations that are more
  useful than the JSON Schema for coding-agent orientation.

The local `tmp/genome-spy` checkout is reference-only. It is intentionally
untracked and must not be required for schema generation.

## What Altair Actually Does

Altair is not mainly handwritten. Its schema package is generated from the
Vega-Lite JSON schema.

Important files in `tmp/altair`:

- `NOTES_FOR_MAINTAINERS.md`: explains the regeneration workflow.
- `tools/generate_schema_wrapper.py`: orchestrates schema download/copy,
  wrapper generation, channel generation, mixin generation, and `__init__`.
- `tools/schemapi/codegen.py`: turns JSON Schema definitions into Python class
  declarations.
- `tools/schemapi/utils.py`: resolves `$ref`, normalizes schema metadata,
  generates valid Python identifiers, docstrings, and type representations.
- `altair/utils/schemapi.py`: runtime base layer with `SchemaBase`,
  `Undefined`, validation, serialization, `copy`, `from_dict`, and property
  setters.
- `altair/vegalite/v6/schema/core.py`: generated low-level schema classes.
- `altair/vegalite/v6/schema/channels.py`: generated ergonomic channel classes
  with shorthand support.
- `altair/vegalite/v6/schema/mixins.py`: generated mark/config mixins.
- `altair/vegalite/v6/api.py`: handwritten public chart API that composes the
  generated pieces.

The generated files are deterministic. If the upstream schema has not changed,
running the generator should rewrite the same output.

Altair commits these generated files. They are not regenerated when a user
installs Altair. Instead, maintainers regenerate them before committing or
cutting a release, and CI verifies that rerunning the generator produces no
tracked diff.

## Altair Layering

Altair has four distinct layers.

1. Runtime schema machinery

`SchemaBase` stores positional args and keyword properties, supports attribute
and item access, serializes recursively with `to_dict`, validates with
`jsonschema`, and can reconstruct wrapper objects with `from_dict`.

This is shared infrastructure, not Vega-Lite-specific chart logic.

2. Generated low-level schema classes

`schema/core.py` contains one class per useful schema definition. Each class has
an `_schema` attribute and a generated `__init__` signature based on the JSON
Schema properties.

Example pattern:

```python
class Axis(VegaLiteSchema):
    _schema = {"$ref": "#/definitions/Axis"}

    def __init__(self, ..., **kwds):
        super(Axis, self).__init__(..., **kwds)
```

3. Generated ergonomic helpers

`schema/channels.py` and `schema/mixins.py` are still generated, but they are
higher-level than `core.py`.

Channel classes add a `shorthand` argument and mix in logic that parses strings
like `"field:Q"`.

Mark mixins add methods such as:

```python
chart.mark_rect(opacity=0.9)
```

Internally these methods write either `"rect"` or a generated `MarkDef`.

4. Handwritten public API

`api.py` defines user-facing `Chart`, `LayerChart`, `HConcatChart`, etc. These
classes inherit from generated schema classes and generated mixins, but the
workflow methods remain handwritten where they need custom behavior.

For example, Altair's `Chart` inherits roughly like this:

```python
class Chart(
    TopLevelMixin,
    _EncodingMixin,
    mixins.MarkMethodMixin,
    core.TopLevelUnitSpec,
):
    ...
```

The high-level API therefore stays friendly without drifting away from the
schema.

## What Gos Adds

`gos` is a smaller Altair-style wrapper around Gosling. It is useful because it
shows the same approach applied to a genomics visualization grammar.

Important files in `tmp/gos`:

- `tools/generate_schema_wrapper.py`: adapted from Altair's older generator.
- `gosling/schemapi.py`: copied/adapted Altair runtime schema base.
- `gosling/schema/core.py`: generated from the Gosling schema.
- `gosling/schema/channels.py`: generated channel wrappers.
- `gosling/schema/mixins.py`: generated mark methods.
- `gosling/api.py`: handwritten public `Track`, `View`, and composition API.

The most relevant Gos pattern is that public classes inherit from generated
schema classes:

```python
class Track(..., mixins.MarkMethodMixin, core.SingleTrack):
    ...
```

That is the shape we want: generated coverage below, custom Python ergonomics
above.

## GenomeSpy Mapping

Target package shape:

```text
src/genome_spy/
  schemapi.py
  schema/
    __init__.py
    core.py
    channels.py
    mixins.py
    genome-spy-core-schema.json
  api.py
  chart.py
  datasets/
  jupyter.py
  _widget.py
tools/
  generate_schema_wrapper.py
  schemapi/
```

Recommended generated files:

- `schema/genome-spy-schema.json`: copied from the version-pinned npm package's
  `dist/schema.json`.
- `schema/core.py`: generated classes for all `definitions` plus a root
  `CoreRootSpec`/`Root` class.
- `schema/channels.py`: generated or augmented channel constructors for
  encoding channels, including GenomeSpy-specific `locus` behavior.
- `schema/mixins.py`: generated `mark_*` methods from the mark enum or mark
  schema definitions.
- `schema/__init__.py`: generated exports plus `SCHEMA_URL` and
  `SCHEMA_VERSION`.

Recommended handwritten files:

- `schemapi.py`: adapted runtime base layer. Start from the smaller Gos version
  or a trimmed Altair version, then add modern validation and typing
  incrementally.
- `chart.py` / `api.py`: preserve our current user-facing API but migrate it to
  subclass or wrap generated root/unit/layer classes.
- `jupyter.py` and `_widget.py`: keep display separate from code generation.
- Derive the default CDN schema and JavaScript bundle URLs from generated
  `SCHEMA_VERSION` so Python wrappers, validation schema, and notebook runtime
  advance as one pinned unit.
- `datasets/`: keep dataset loading separate from code generation.

## Generator Design

The first generator should be intentionally smaller than Altair's current
generator but follow its shape.

Inputs:

- `[tool.genome-spy].core-version` from `pyproject.toml`
- optional `--core-version`
- optional `--output-dir`
- optional `--spec-reference-dir`

Prerequisite:

- `npm` must be installed and available on `PATH`, because the generator uses
  `npm pack` to fetch the version-pinned `@genome-spy/core` package from the
  npm registry.

Outputs:

- copied schema JSON
- generated `core.py`
- generated `__init__.py`
- copied TypeScript spec references in ignored local cache
  `.cache/genome-spy-python/genomespy-core-spec/`
- later generated `channels.py`
- later generated `mixins.py`

Workflow policy:

- Treat generated files in `src/genome_spy/schema/` as tracked source
  artifacts, just as Altair tracks `altair/vegalite/v6/schema/`.
- Do not run code generation during package installation or import.
- Keep npm as a maintainer/developer prerequisite only.
- Use the pinned npm package version as the source of truth, not `tmp/`.
- Add a CI freshness check that reruns the generator and fails if tracked files
  change.
- Include the generated schema JSON in wheels so runtime validation can work
  without network or npm access.

Algorithm for `core.py` MVP:

1. Load schema JSON.
2. Create a base class, for example `GenomeSpySchema(SchemaBase)`.
3. Generate a root class from the top-level schema.
4. Iterate over `schema["definitions"]`.
5. For each definition, generate a class named with a valid Python identifier.
6. Store `_schema = {"$ref": "#/definitions/Name"}` and
   `_rootschema = GenomeSpySchema._rootschema`.
7. Generate `__init__` from object properties where possible.
8. Fall back to `*args, **kwds` for complex `anyOf`/`oneOf` cases.
9. Topologically sort inheritance where schema definitions are unions of other
   references, as Altair/Gos do.
10. Run Ruff formatting after writing files.

## GenomeSpy-Specific Concerns

1. Secondary locus channels

GenomeSpy primary locus channels include `"type": "locus"`, but secondary
channels like `x2` and `y2` use `SecondaryChromPosDef` and should not include a
`type` property. Our current handwritten normalization handles this. The
generated channel layer must preserve that behavior.

2. Locus ergonomics

GenomeSpy users need a first-class helper:

```python
gs.Locus("chrom", "chromStart")
```

The generated layer can provide broad schema coverage, but this helper should
remain a public ergonomic convenience.

3. Schema naming

The TypeScript generator may produce names that are not valid Python
identifiers, especially if generic-like names or special characters appear. We
should reuse Altair's `get_valid_identifier` approach and keep a mapping from
original schema definition name to generated Python class name.

4. JSON Schema draft and reference handling

Altair's runtime avoids validating the schema itself and validates user specs
against the generated schema directly. It also handles modern `jsonschema`
reference behavior. We should use the same idea to avoid brittle validation
errors.

5. Handwritten API migration

Do not delete the current working `Chart` API in one shot. First generate
schema classes and validate specs alongside the handwritten chart builder.
Then migrate `Chart` to inherit from or delegate to the generated root/unit
classes.

## Implementation Milestones

### Milestone 1: Schema Runtime MVP

- Add `genome_spy.schemapi`.
- Include `Undefined`, `SchemaBase`, validation, recursive `to_dict`, `to_json`,
  `copy`, and `from_dict` basics.
- Add tests against small hand-authored schema classes before generation.

### Milestone 2: Core Generator MVP

- Add `tools/generate_schema_wrapper.py`.
- Fetch `@genome-spy/core@<version>` from npm into a temporary directory.
- Generate `schema/core.py`, `schema/__init__.py`, and copy the package's
  `dist/schema.json`.
- Copy compact TypeScript spec references from the npm package into the ignored
  local cache `.cache/genome-spy-python/genomespy-core-spec/` for coding-agent
  orientation.
- Add a smoke test that imports generated classes and validates a minimal
  GenomeSpy spec.

### Milestone 3: Build Integration

- Add a documented command, for example:

```bash
uv run python tools/generate_schema_wrapper.py
```

- Keep the local `tmp/genome-spy` checkout reference-only.
- Add a project task once we choose a task runner convention.
- Add an Altair-style CI check that runs the generator and verifies no tracked
  generated files changed.
- Confirm that builds and installs use committed generated files only.

### Milestone 4: Channel Layer

- Generate channel classes from GenomeSpy encoding definitions.
- Add `shorthand` support for simple field/type strings.
- Preserve `gs.Locus(...)` and secondary channel normalization.
- Keep value channels such as `gs.value(...)`.

### Milestone 5: Mark and Composition Mixins

- Generate `mark_*` methods from GenomeSpy mark definitions.
- Keep existing composition operators working.
- Replace handwritten `MARK_TYPES` with schema-derived mark names.

### Milestone 6: API Migration

- Make public `Chart` schema-backed.
- Keep notebook rendering unchanged.
- Add validation-on-serialization with a `validate` flag.
- Update notebooks to use schema-backed objects.

### Milestone 7: App Schema Later

- Repeat the same structure for `@genome-spy/app` only after core stabilizes.
- Keep app schema generation separate from core schema generation.

## Working Principle

Generated code should maximize spec coverage. Handwritten code should maximize
user experience. If a feature is part of the GenomeSpy JSON grammar, prefer
generating it from `schema.json`; if a feature is Python ergonomics, notebook
rendering, datasets, or common shortcuts, keep it handwritten.
