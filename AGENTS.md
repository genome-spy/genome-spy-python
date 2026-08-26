## Project Orientation
`genome-spy-python` is a Python wrapper around GenomeSpy, similar in spirit to
how Altair wraps Vega-Lite. The library should let Python users build
GenomeSpy-compatible specs with an idiomatic Python API, serialize those specs
to JSON, and render them in notebook environments.

Key layout:
- `src/genome_spy/`: installable library code
- `tests/`: pytest test suite
- `scripts/`: local helper scripts run via `uv run`
- `plans/`: planning, context, and implementation notes
- `material/`: local reference documents; intentionally not committed
- `tmp/`: local reference repositories; intentionally not committed

Constraints:
- Treat this repository as a library with a clean public API.
- Build incrementally: start with the reusable GenomeSpy core grammar and only
  later add app-specific concepts.
- Notebook rendering is a first-class requirement; prefer `anywidget` for that
  integration.
- Keep reference material in `material/` and external code in `tmp/`.
- Prefer pure Python logic in the core; isolate I/O and integration edges.
- Use upstream projects for design guidance:
  `tmp/altair`, `tmp/gos`, `tmp/vega-lite`, `tmp/gosling.js`,
  `tmp/genome-spy`, and `tmp/anywidget`.

## General LLM Instructions
### 1. Think Before Coding
Don't assume. Surface tradeoffs. State assumptions explicitly. Push back when warranted.

### 2. Simplicity First
Minimum code that solves the problem. No speculative features, no premature abstractions. IF YOU WRITE 200 LINES AND IT COULD BE 50, REWRITE IT.

### 3. Surgical Changes
Touch only what you must. Match existing style. Remove orphaned imports/variables your changes created. Don't clean up unrelated code.

### 4. Goal-Driven Execution
Transform tasks into verifiable goals. State a brief plan for multi-step tasks.

## Python Conventions
- Type hints on all public APIs
- Use `list[T]`, `dict[K, V]`, `X | Y` — never `typing.List`, `Optional`
- `src/` layout; explicit `__all__` on public packages
- Protocols (PEP 544) over ABCs for structural typing
- `@dataclass(frozen=True, slots=True)` for value objects
- `pathlib` for paths; `os` for env vars only
- Prefer functions over single-use classes
- Fail fast: custom exceptions with contextual messages; zero silent failures
- I/O at edges, pure logic in core
- `logging.getLogger(__name__)` — never `print()` or `logging.basicConfig()`
- No speculative abstraction; duplicate a little first
- Explicit imports; no package-level magic re-exports

## Docstrings
Use Google-style docstrings for every public API via `sphinx.ext.napoleon`.
Types belong in signatures only and should not be repeated in docstrings.

Required public API sections:
- Summary
- Description
- Args
- Returns
- Raises
- Example

## Style and Formatting
Ruff is the source of truth for formatting and linting.

Rules:
- Run `uv run ruff format .` before finalizing non-trivial edits.
- Run `uv run ruff check .` and fix issues rather than suppressing them by default.
- Keep modules small and names descriptive.
- Prefer explicit imports and predictable control flow over cleverness.

## Testing
Use `pytest` for all tests.

Rules:
- Add or update tests with behavior changes.
- Use fixed seeds for any randomized behavior.
- Prefer small, focused tests with one behavior under test.
- Apply a "Suspicious Check": if a test can pass for the wrong reason, tighten it.

## Development Tooling
Use `uv` for environment and dependency management.

Common commands:

| Task | Command |
|---|---|
| Sync env | `uv sync --dev` |
| Run tests | `uv run pytest tests/ -x` |
| Run lint | `uv run ruff check .` |
| Format | `uv run ruff format .` |
| Type-check | `uv run mypy src/` |
| Install hooks | `uv run pre-commit install` |

Git rules:
- Make small, thematic commits.
- Use conventional commits: `<type>(<scope>): <description>` when a scope helps.
- Do not rewrite history unless explicitly asked.

## Plans and Reference Documents
| Document | When to Read |
|---|---|
| `plans/implementation_plan.md` | At the start of implementation work to understand current phases and open questions |
| `plans/deferred.md` | Before adding scope, to avoid implementing intentionally deferred work |
| `plans/architecture.md` | Before changing public API shape, schema strategy, or notebook integration |
| `plans/tmp_repo_index.md` | When using reference repos in `tmp/` for wrapper or widget design decisions |
| `plans/project_bootstrap.md` | When updating or extending the initial repository scaffold |

## Validation and Local Checks
Before handing work off:
- Run targeted tests for the changed behavior.
- Run `uv run ruff check .`.
- Run `uv run mypy src/` when public Python code changes.
- Call out anything you could not validate locally.

## Documentation Gallery Policy

- Keep documentation examples focused on the GenomeSpy visualization API, not
  statistical analysis or general-purpose data wrangling. Prepare derived
  example datasets, including p-values, adjusted p-values, transformed values,
  classifications, and plotting domains, in `src/genome_spy/datasets/` or in
  curated packaged data files. Examples should load the prepared table and
  demonstrate encodings, marks, transforms, and composition directly.
- Prefer Altair-style composition operators in examples when they express the
  intended structure clearly: `+` for layers, `&` for vertical concatenation,
  and `|` for horizontal concatenation.
- Documentation gallery embeds must use the direct static GenomeSpy bundle
  import followed by `embed(c, spec, { bare: true })`. Keep the chart container
  direct and avoid transform or resize wrappers around the embedded canvas;
  this is the known-working path for all gallery plots, including sashimi.
- Keep adapted gallery pages self-contained. Link the corresponding official
  GenomeSpy example as further reading, not as a substitute for local
  explanation.
- Put extended prose in an optional same-stem Markdown companion under
  `docs/examples/`.
- For the same data and processing, reuse the official GenomeSpy example's
  concise provenance or disclaimer wording. Update it when the sample, region,
  subset, preprocessing, or intended use differs.
- Keep provenance as brief as possible. Include only details needed to identify
  the data, disclose material processing, satisfy attribution or licensing, or
  prevent misuse. Use a note-styled admonition titled `Data use and
  provenance`; do not repeat it as a section heading.
- Adapt `What to notice` and implementation prose to the chart actually
  rendered. Verify every claim about data, encodings, transforms, interaction,
  and composition against the checked-in Python source.
- Explicitly distinguish processing performed in Python from GenomeSpy's
  browser-side dataflow. State whether an example loads a prepared packaged
  table, derives or filters data in Python, or sends data to GenomeSpy for
  declarative transforms.
- Do not describe packaged derived data as raw source data or imply that
  `.transform_*()` methods execute in Python. The Python API authors and
  serializes those transform definitions; GenomeSpy executes them while
  rendering or interacting with the visualization in the browser.
