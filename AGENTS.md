# Repository instructions

`genome-spy-python` wraps GenomeSpy in an idiomatic Python API, as Altair wraps
Vega-Lite. Users author compatible specs, serialize JSON, and render in notebooks.
Treat it as a library with a clean public API. Build the reusable Core grammar
before app-specific concepts. Notebook rendering is first-class; prefer `anywidget`.

## Layout

| Path | Purpose |
| --- | --- |
| `src/genome_spy/` | Installable library |
| `src/genome_spy/integrations/<library>/` | Optional integration implementations |
| `tests/` | pytest suite |
| `integrations/` | Tracked integration plans and per-library workflow notebooks |
| `scripts/` | Helpers run via `uv run` |
| `plans/` | Plans, context, and implementation notes |
| `material/` | Local reference documents; not committed |
| `tmp/` | External reference code/repos; not committed |

## Working rules

- Think before coding: state assumptions and tradeoffs; push back when warranted.
- Apply YAGNI and the [Ponytail rules](https://github.com/DietrichGebert/ponytail/blob/main/.agents/rules/ponytail.md):
  complete the task with the least new code. Avoid unrequested features,
  wrappers, conversions, options, and speculative abstractions. If 200 lines
  could be 50, rewrite them.
- Prefer existing repository code, then standard-library/platform features,
  then installed dependencies, then minimal new code. Do not add a dependency
  for a few lines of functionality.
- Before editing, trace affected callers, tests, fixtures, configuration, and
  exports. Fix shared root causes once and complete every affected part.
- Make surgical changes: match existing style, remove imports/variables orphaned
  by your edits, preserve existing layers and native value forms, and leave
  unrelated code alone. Keep validation and error handling when moving code.
- Prefer equally small solutions that handle edge cases. Preserve security,
  accessibility, trust-boundary checks, and required hardware calibration.
- Keep comments to one-line explanations of why. Document deliberate shortcuts
  as `shortcut: <the limit>, <when to upgrade>`.
- Set verifiable goals and give a brief plan for multi-step work.
- Keep core logic pure Python; isolate I/O and integration at the edges.
- Follow the linked [language, docstring, formatting, and gallery standards](docs/contributing/standards.md).
  Read the relevant sections before Python or gallery edits; they are requirements.

## Testing and handoff

Use pytest. Add or update tests for behavior changes, with fixed seeds for random
behavior. Keep tests small and focused on one behavior. Apply the "Suspicious
Check": tighten any test that could pass for the wrong reason.

Never commit or push generated test images, including reference PNGs, screenshots
and overlays. Generate them in temporary directories or ignored local caches;
track only their generators and text metadata. Check outgoing commit history
before pushing: deleting images from the current tree does not remove old blobs.

Use `uv` for environments and dependencies. Before handoff, run targeted tests for
changed behavior and lint. Format before finalizing non-trivial edits; type-check
when public Python code changes. End the handoff with any skipped or unvalidated
work and material risks.
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
| `integrations/README.md` | Integration layout, plan lifecycle, and clearance rules |
| `integrations/<library>/STATUS.md` | Current implementation, next slice, blockers, and retained evidence |
| `integrations/<library>/PLAN.md` | Planning or extending a library integration; update status with implementation |
| `plans/implementation_plan.md` | Starting implementation; understand phases and open questions |
| `plans/deferred.md` | Adding scope; avoid intentionally deferred work |
| `plans/architecture.md` | Changing public API shape, schema strategy, or notebook integration |
| `plans/tmp_repo_index.md` | Using `tmp/` repos for wrapper/widget design |
| `plans/project_bootstrap.md` | Updating or extending the initial scaffold |
