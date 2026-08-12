# GenomeSpy Codegen Mapping

This note maps our current generator to Altair's architecture.

## Current State

The generator is now active for the first low-level slice. It builds a real `genome_spy.schema` package from the version-pinned `@genome-spy/core` npm package.

The source of truth is the npm package configured in `pyproject.toml`:

```toml
[tool.genome-spy]
core-version = "0.81.0"
```

The local `tmp/genome-spy` clone is reference-only and must not be used as the schema source.

Generated files:

- `src/genome_spy/schema/genome-spy-schema.json`
- `src/genome_spy/schema/core.py`
- `src/genome_spy/schema/__init__.py`

Generation command:

```bash
uv run python tools/generate_schema_wrapper.py
```

Prerequisite: `npm` must be installed and available on `PATH`, because the
generator fetches `@genome-spy/core` from the npm registry.

The command fetches `@genome-spy/core@0.81.0` with `npm pack`, unpacks it in a temporary directory, copies `dist/schema.json`, generates Python wrappers, copies compact `dist/src/spec/*.d.ts` references into the ignored local cache `.cache/genome-spy-python/genomespy-core-spec/`, and deletes the temporary npm package directory when generation finishes.

## Workflow Policy

This project should mimic Altair's generated-artifact workflow:

- Generated files under `src/genome_spy/schema/` are committed to git.
- The package wheel includes the generated Python modules and
  `genome-spy-schema.json`.
- End users installing `genome-spy-python` do not need npm.
- npm is only a developer prerequisite for running
  `tools/generate_schema_wrapper.py`.
- The temporary `@genome-spy/core` npm package unpack directory is deleted after
  generation.
- The ignored TypeScript reference cache under `.cache/` is local convenience
  material for agents and maintainers, not a source file.

The intended maintainer flow is:

1. Update `[tool.genome-spy].core-version` when intentionally changing the
   wrapped GenomeSpy core version.
2. Run `uv run python tools/generate_schema_wrapper.py`.
3. Run `uv run ruff format src/genome_spy/schema`.
4. Review changes in `src/genome_spy/schema/`.
5. Run tests and notebook checks.
6. Commit the generated files together with any handwritten compatibility
   changes.

Future CI should add an Altair-style freshness check:

```bash
uv run python tools/generate_schema_wrapper.py
uv run ruff format src/genome_spy/schema
git diff --exit-code src/genome_spy/schema tools
```

That check should fail if regeneration changes tracked generated files. This is
how we verify that committed artifacts match the pinned npm package without
making package installation depend on npm.

## Mapping To Altair

| Altair | GenomeSpy Python | Status |
| --- | --- | --- |
| `tools/generate_schema_wrapper.py` | `tools/generate_schema_wrapper.py` | Writes generated schema package files. |
| `tools/schemapi/codegen.py` | `tools/schemapi/codegen.py` | Emits low-level wrapper classes from schema definitions. |
| `tools/schemapi/schemapi.py` | not mirrored | GenomeSpy keeps its small runtime directly in the package until runtime generation provides concrete value. |
| `altair/utils/schemapi.py` | `src/genome_spy/schemapi.py` | Package runtime with serialization, copy, and validation primitives. |
| `schema/core.py` | `src/genome_spy/schema/core.py` | Generated from GenomeSpy schema. |
| `schema/channels.py` | `src/genome_spy/schema/channels.py` | Generates named wrappers for every property in the upstream `Encoding` schema. |
| `schema/mixins.py` | `src/genome_spy/schema/mixins.py` | Generates mark methods from the upstream `MarkType` enum. |
| `vegalite/v6/api.py` | `src/genome_spy/chart.py` and `src/genome_spy/api.py` | Handwritten public API. |

## What Works Now

Low-level wrappers can be imported and serialized:

```python
from genome_spy.schema import Root, UnitSpec, load_schema

schema = load_schema()
Root(mark="point").to_dict()
UnitSpec(mark="point", width=320).to_dict()
```

The generated package currently exposes 215 GenomeSpy schema definition wrappers from the npm-published core schema.

## What Is Still Smaller Than Altair

The current generator is intentionally smaller than Altair's:

- It does not yet resolve `$ref`, `anyOf`, `oneOf`, or `allOf` into Python inheritance.
- It now resolves reachable properties through `$ref` and union branches for
  generated constructor signatures, and channel wrappers now expose
  schema-derived nested setters such as `.scale(...)`, `.axis(...)`, and
  `.legend(...)`. However, it does not yet generate the broader fluent setter
  surface that Altair emits across many schema wrappers.
- Generated schema wrappers now expose immutable `with_<property>(...)`
  methods. Nested object properties accept helper-wrapper instances, raw
  mappings, or keyword merges, which brings helper objects such as `Scale`,
  `Legend`, and `GenomeAxis` closer to the fluent style already used by the
  channel wrappers.
- It validates generated wrappers and complete public chart specs with
  `jsonschema`, but does not yet provide Altair's detailed error grouping.
- The handwritten `Chart` directly subclasses generated `UnitSpec`, uses
  schema-object copy semantics, and validates complete output through generated
  `Root`. Composition containers remain handwritten immutable dataclasses.

## Next Steps

The next useful generator milestones are:

1. Refine which generated properties should expose richer typed fluent setters
   versus plain value setters, especially for enum-like helper objects where
   dict-style keyword merges add little value.
2. Evaluate generated schema bases for layer and concatenation containers once
   unit-chart behavior has stabilized.
3. Gradually expose additional generated channels publicly as use cases prove
   their ergonomics.
