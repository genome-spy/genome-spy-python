# Contributing to genome-spy-python

Bug reports, documentation, examples, tests, and code contributions are welcome.

## How to contribute

Open an issue before starting a large change. Small fixes can go straight to a
pull request.

Explain what your pull request changes and why. Keep unrelated changes separate,
and update tests and docs when behavior or the public API changes.

## Development setup

Use Python 3.11 or newer and [`uv`](https://docs.astral.sh/uv/). Install the
development and docs dependencies from the repository root:

```bash
uv sync --group dev --group docs
```

Main directories:

- `src/genome_spy/` — library code
- `tests/` — tests
- `docs/examples/` — gallery examples
- `tools/` — code and documentation generators

Install pre-commit hooks to check changes before committing:

```bash
uv run pre-commit install
```

## Coding practices

### Python and typing

Use type hints such as `list[T]`, `dict[K, V]`, and `X | Y` for public APIs.
Add Google-style docstrings covering purpose, arguments, results, exceptions,
and an example. Keep file, network, and notebook code separate from core logic.

Keep changes small. Prefer generating APIs from the GenomeSpy schema over
adding handwritten alternatives.

### Formatting and linting

Format and lint with [Ruff](https://docs.astral.sh/ruff/):

```bash
uv run ruff format .
uv run ruff check .
```

Check types after changing library code:

```bash
uv run mypy src/
```

### Testing

Add a focused test for each behavior change. Run the Python tests with:

```bash
uv run pytest tests/ -x
```

Run the widget's JavaScript tests with:

```bash
node --test tests/widget.test.mjs
```

Run the checks relevant to your changes before submitting a pull request.
CI also checks generated code, docs, and the installed package.

### Performance

Avoid unnecessary data copies and large chart specifications. Measure performance
before adding complexity to make code faster.

## Generated schema and expression APIs

Do not edit generated files in `src/genome_spy/schema/` by hand. The generator
uses the GenomeSpy version in `pyproject.toml`, its schema, and the matching
GenomeSpy and Vega expression documentation.

Regenerate after changing that version or the generator:

```bash
uv run python tools/generate_schema_wrapper.py
```

This requires `npm` and internet access. Use `--package-dir` for a local package,
or both `--genome-spy-expression-docs` and `--vega-expression-docs` for local
expression docs.

Then check the results:

```bash
uv run pytest tests/test_schema_codegen.py -x
uv run ruff format src/genome_spy/schema src/genome_spy/helpers.py src/genome_spy/api.py src/genome_spy/__init__.py
git diff --check
```

Review and commit the generated files alongside your changes. CI checks that
regenerating them produces no differences.

New transforms should be generated from the schema. Add overrides in
`tools/generate_schema_wrapper.py` only for Python conventions the schema
cannot describe.

## Documentation

### API reference

After changing the public API, regenerate `docs/api.md` from `genome_spy.__all__`:

```bash
uv run python tools/generate_api_docs.py
```

Sphinx creates the individual pages in `docs/generated/`; do not commit them.

### Build and preview

Build the docs and check for warnings:

```bash
uv run sphinx-build -b html -W --keep-going docs docs/_build/html
```

Rerun the same command to rebuild changed pages and examples. Keep `docs/_build/`
and avoid `-E` and `-a` for faster builds. Changes to shared code, data, build
tools, or the lockfile regenerate all examples.

To force example regeneration, delete the gallery cache (normally
`docs/_build/html/.doctrees/genomespy-gallery`). Changes to remote data or files
outside the tracked dependencies are not detected automatically.

Preview locally:

```bash
cd docs/_build/html
python3 -m http.server
```

Open <http://localhost:8000>. Interactive examples need internet access to load
GenomeSpy.

### Gallery examples

Write examples in `docs/examples/`. Put explanations, data sources, any
necessary disclaimers, and upstream links in an optional Markdown file with
the same name.

Focus on plotting, not data preparation: load prepared packaged datasets and
prefer Python expressions such as `gs.datum.score > 0`. Remember that
`.transform_*()` defines work that GenomeSpy runs in the browser, not Python.

After editing an example, run:

```bash
uv run pytest tests/test_docs_gallery.py -q
uv run sphinx-build -b html -W --keep-going docs docs/_build/html
```

Check the chart visually before updating its committed thumbnail.

### Notebook rendering

CI checks that the brush notebook renders in a fresh environment. Follow
[the workflow](.github/workflows/ci.yml) for setup, then run with that
environment's Python:

```bash
python -m playwright install chromium
python tools/check_notebook_rendering.py notebooks/brush_linked_genome_tracks.ipynb --screenshot /tmp/notebook-rendering.png
```

## Commit guidelines

Keep each commit focused on one change. Use
[Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0/):

```text
feat(expressions): generate runtime helpers
fix(widget): preserve zoom during data updates
docs(gallery): add a sequence example
```

Do not rewrite shared history unless reviewers ask you to.

## Community and communication

Report wrapper bugs and request features in the
[Python package issue tracker](https://github.com/genome-spy/genome-spy-python/issues).
For GenomeSpy's grammar or renderer, use the upstream
[discussions](https://github.com/genome-spy/genome-spy/discussions) or
[issues](https://github.com/genome-spy/genome-spy/issues).
