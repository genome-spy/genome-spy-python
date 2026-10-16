# Repository instructions

`genome-spy-python` wraps GenomeSpy in an idiomatic Python API, as Altair wraps
Vega-Lite. Users author compatible specs, serialize JSON, and render in notebooks.
Treat it as a library with a clean public API. Build the reusable Core grammar
before app-specific concepts. Notebook rendering is first-class; prefer `anywidget`.

## Layout

| Path | Purpose |
| --- | --- |
| `src/genome_spy/` | Installable library |
| `tests/` | pytest suite |
| `scripts/` | Helpers run via `uv run` |
| `plans/` | Plans, context, and implementation notes |
| `material/` | Local reference documents; not committed |
| `tmp/` | External reference code/repos; not committed |

## Working rules

- Think before coding: state assumptions and tradeoffs; push back when warranted.
- Solve the current problem with minimal code. Avoid speculative features and
  premature abstractions; duplicate a little first. If 200 lines could be 50,
  rewrite them.
- Make surgical changes: match existing style, remove imports/variables orphaned
  by your edits, and leave unrelated code alone.
- Set verifiable goals and give a brief plan for multi-step work.
- Keep core logic pure Python; isolate I/O and integration at the edges.
- Follow the linked [language, docstring, formatting, and gallery standards](docs/contributing/standards.md).
  Read the relevant sections before Python or gallery edits; they are requirements.

## Testing and handoff

Use pytest. Add or update tests for behavior changes, with fixed seeds for random
behavior. Keep tests small and focused on one behavior. Apply the "Suspicious
Check": tighten any test that could pass for the wrong reason.

Use `uv` for environments and dependencies. Before handoff, run targeted tests for
changed behavior and lint. Format before finalizing non-trivial edits; type-check
when public Python code changes. Report anything you could not validate locally.
Ruff is the formatting/lint authority; fix issues rather than suppressing them by
default.

| Task | Command |
| --- | --- |
| Sync environment | `uv sync --dev` |
| Run tests | `uv run pytest tests/ -x` |
| Lint | `uv run ruff check .` |
| Format | `uv run ruff format .` |
| Type-check | `uv run mypy src/` |
| Install hooks | `uv run pre-commit install` |

Make small, thematic commits. Use conventional commits:
`<type>(<scope>): <description>` when a scope helps. Do not rewrite history unless
explicitly asked.

## Plans and references

| Document | Read when |
| --- | --- |
| `plans/implementation_plan.md` | Starting implementation; understand phases and open questions |
| `plans/deferred.md` | Adding scope; avoid intentionally deferred work |
| `plans/architecture.md` | Changing public API shape, schema strategy, or notebook integration |
| `plans/tmp_repo_index.md` | Using `tmp/` repos for wrapper/widget design |
| `plans/project_bootstrap.md` | Updating or extending the initial scaffold |
