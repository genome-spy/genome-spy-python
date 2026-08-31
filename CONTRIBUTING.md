# Contributing to genome-spy-python

Thank you for considering a contribution to `genome-spy-python`. Bug reports,
documentation improvements, examples, tests, and code contributions are all
welcome.

## How to contribute

Use a GitHub issue to report a bug or propose a substantial change before
starting work. Small, well-scoped fixes can go directly to a pull request.

Pull requests should explain the motivation and user-visible effect of the
change. Keep unrelated changes separate and update tests and documentation when
behavior or the public API changes.

## Development setup

The project requires Python 3.11 or newer and uses
[`uv`](https://docs.astral.sh/uv/) for its development environment. From the
repository root, install the development and documentation dependencies:

```bash
uv sync --group dev --group docs
```

The main project directories are:

- `src/genome_spy/` — installable library code;
- `tests/` — the pytest suite;
- `docs/examples/` — source files for the documentation gallery;
- `tools/` — schema, API-reference, and gallery tooling;
- `plans/` — architectural and implementation notes.

You can install the repository's pre-commit hooks with:

```bash
uv run pre-commit install
```

## Coding practices

### Python and typing

Public APIs must have type hints. Prefer modern annotations such as `list[T]`,
`dict[K, V]`, and `X | Y`. Keep the core implementation in pure Python where
possible and isolate file, network, and notebook integration at the edges.
Document public APIs with Google-style docstrings, including a summary,
description, arguments, return value, raised exceptions, and an example.

The package is a schema-backed public API. Favor small, predictable changes and
avoid adding parallel representations or runtime adapters when the behavior can
be expressed through the schema generator.

### Formatting and linting

[Ruff](https://docs.astral.sh/ruff/) is the source of truth for formatting and
linting:

```bash
uv run ruff format .
uv run ruff check .
```

Run the type checker when Python library code changes:

```bash
uv run mypy src/
```

### Testing

Use pytest for Python tests and add focused coverage for behavior changes. Run
the complete suite with:

```bash
uv run pytest tests/ -x
```

The notebook widget also has Node-based tests:

```bash
node --test tests/widget.test.mjs
```

Before submitting a pull request, run the checks relevant to the files you
changed. CI runs formatting, linting, typing, package tests, code-generation
checks, documentation tests, and wheel smoke tests.

### Performance

GenomeSpy is designed for scalable visualization. Consider serialization size,
data copying, and browser transfer when changing data or rendering paths. Use
measurements to justify optimization work; readability is preferable to
speculative performance complexity.

## Generated schema and expression APIs

Generated files under `src/genome_spy/schema/` are committed but should not be
edited by hand. The generator reads the pinned `@genome-spy/core` version from
`pyproject.toml`, fetches its schema, and generates the Python wrappers. The
expression namespace is generated from that GenomeSpy release's expression
documentation and the corresponding `vega-expression` documentation.

Regenerate after changing the Core pin or the generator:

```bash
uv run python tools/generate_schema_wrapper.py
```

Schema generation requires `npm` on `PATH` and network access. For local
upstream auditing, the command also accepts an unpacked package with
`--package-dir`. Local expression documentation can be supplied together with
`--genome-spy-expression-docs` and `--vega-expression-docs`.

After regeneration, run:

```bash
uv run pytest tests/test_schema_codegen.py -x
uv run ruff format src/genome_spy/schema
git diff --check
```

Inspect and commit the generated artifacts with the generator changes. CI reruns
the generator and rejects any uncommitted drift in `src/genome_spy/schema/` or
`tools/`.

If an upstream transform follows the existing schema structure, its public
`transform_*()` method should be generated. Keep the small override registry in
`tools/generate_schema_wrapper.py` limited to intentional Python authoring
conventions that cannot be inferred from the schema alone.

## Documentation

### API reference

`docs/api.md` is generated from `genome_spy.__all__`. Regenerate it after
changing the public API:

```bash
uv run python tools/generate_api_docs.py
```

Sphinx creates the individual API pages in the ignored `docs/generated/`
directory.

### Build and preview

Build the documentation with warnings treated as errors:

```bash
uv run sphinx-build -b html -W --keep-going docs docs/_build/html
```

To preview it locally:

```bash
cd docs/_build/html
python3 -m http.server
```

Then open <http://localhost:8000>. Interactive examples load the pinned
GenomeSpy JavaScript bundle from a CDN, so they require an internet connection.

### Gallery examples

Python files under `docs/examples/` are the source of truth for the generated
gallery. An example can have a same-stem Markdown companion for interpretation,
provenance, disclaimers, and links to the corresponding official GenomeSpy
example.

Keep examples focused on visualization. Prefer prepared packaged datasets over
embedding general-purpose analysis, and use Python-authored expressions such as
`gs.datum.score > 0` and `gs.expr.isValid(gs.datum.value)` where possible.
Remember that `.transform_*()` methods only author the specification;
GenomeSpy executes the transforms in the browser.

After changing an example, run:

```bash
uv run pytest tests/test_docs_gallery.py -q
uv run sphinx-build -b html -W --keep-going docs docs/_build/html
```

Gallery thumbnails are checked in and should be updated only after visually
reviewing the rendered chart.

## Commit guidelines

Keep commits atomic: each commit should contain one logical change that can be
reviewed independently. Use
[Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0/):

```text
feat(expressions): generate runtime helpers
fix(widget): preserve zoom during data updates
docs(gallery): add a sequence example
```

Do not rewrite shared history unless the reviewers explicitly request it.

## Community and communication

Use the
[`genome-spy-python` issue tracker](https://github.com/genome-spy/genome-spy-python/issues)
for package-specific bugs and feature requests. Questions about the underlying
GenomeSpy grammar or JavaScript renderer belong in the upstream
[GenomeSpy discussions](https://github.com/genome-spy/genome-spy/discussions)
or [issue tracker](https://github.com/genome-spy/genome-spy/issues).
