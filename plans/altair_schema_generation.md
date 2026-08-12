# Altair Schema Generation Machinery

Altair is schema-first, but not schema-only. Vega-Lite's JSON Schema is the source of truth for the broad Python object model, while Altair's handwritten API layer provides the user-friendly chart syntax, data handling, and notebook rendering.

## Main Pieces

Altair's generator lives in:

- `tmp/altair/tools/generate_schema_wrapper.py`
- `tmp/altair/tools/schemapi/codegen.py`
- `tmp/altair/tools/schemapi/utils.py`
- `tmp/altair/tools/schemapi/schemapi.py`

Generated package files live under a versioned schema package:

- `tmp/altair/altair/vegalite/v6/schema/core.py`
- `tmp/altair/altair/vegalite/v6/schema/channels.py`
- `tmp/altair/altair/vegalite/v6/schema/mixins.py`
- `tmp/altair/altair/vegalite/v6/schema/_typing.py`
- `tmp/altair/altair/vegalite/v6/schema/_config.py`
- `tmp/altair/altair/vegalite/v6/schema/vega-lite-schema.json`

The public API remains handwritten in files such as:

- `tmp/altair/altair/vegalite/v6/api.py`
- `tmp/altair/altair/vegalite/v6/data.py`
- `tmp/altair/altair/vegalite/v6/display.py`

## Generation Flow

Altair's maintainer workflow runs:

```bash
uv run task generate-schema-wrapper
```

That task downloads or refreshes the Vega-Lite schema, patches it for Altair-specific shorthand support, and writes generated modules.

The generator produces:

- low-level schema classes in `core.py`
- channel classes such as `X`, `Y`, and `Color` in `channels.py`
- generated `encode(...)` signatures
- mark helpers such as `mark_point(...)`
- config helpers such as `configure_axis(...)`
- type aliases and TypedDict helpers
- a package `__init__.py` with schema metadata and exports

## Generated Files Are Tracked

Altair commits the generated schema package to git. The generated files are not
temporary build products and are not recreated when a user installs Altair.

The important generated files include:

- `altair/vegalite/v6/schema/core.py`
- `altair/vegalite/v6/schema/channels.py`
- `altair/vegalite/v6/schema/mixins.py`
- `altair/vegalite/v6/schema/_typing.py`
- `altair/vegalite/v6/schema/_config.py`
- `altair/vegalite/v6/schema/vega-lite-schema.json`
- `altair/vegalite/v6/schema/vega-themes.json`

This means a normal package install uses already-generated Python source. It
does not need Node, npm, Vega-Lite, or the schema generator.

## Maintainer And CI Workflow

Altair treats code generation as a maintainer task:

1. Pin the upstream Vega-related versions in `pyproject.toml`.
2. Run `uv run task generate-schema-wrapper`.
3. Review the generated Python/schema diff.
4. Commit the generated files with the handwritten changes that required them.
5. In CI, run the generator again and fail if it changes tracked files.

The CI freshness check is important. It proves the committed generated files
match the pinned upstream schema. If the generator has no effect, the repository
is internally consistent.

The practical rule is:

```text
generation happens before commit/release, never during package installation
```

This keeps installs fast, deterministic, and independent of the JavaScript
toolchain.

## Runtime Layer

Generated classes inherit from Altair's runtime `SchemaBase`, which handles:

- storing keyword properties
- copying immutable chart objects
- serializing nested schema objects to dictionaries
- converting to JSON
- validating with `jsonschema`
- reconstructing wrappers from dictionaries
- property setters such as `.scale(...)` and `.axis(...)`

Altair copies the development-time schema runtime helper into the installed package as `altair/utils/schemapi.py`.

## Handwritten API Boundary

Altair's `Chart` class is not simply generated. It combines generated schema classes and mixins with handwritten logic for:

- `Chart(data)`
- top-level spec normalization
- data transformers
- renderer registration
- notebook MIME bundles
- chart composition
- user-facing convenience methods

This is the model for GenomeSpy Python: generated code should provide schema breadth and validation, while handwritten code should provide the pleasant API.

## Lessons For GenomeSpy Python

The GenomeSpy wrapper should mirror Altair's boundary:

- Generate broad, boring schema classes from `packages/core/dist/schema.json`.
- Keep `Chart`, DataFrame normalization, and notebook rendering handwritten.
- Add Python-only conveniences, then normalize them back to valid GenomeSpy JSON.
- Use generated schema classes for validation and coverage.
- Gradually replace handwritten channel and mark helpers with generated ones.
