# Python Project Bootstrap

Instructions for a coding agent to set up a new Python project from scratch using a
structured, agent-friendly workflow. Follow the phases in order. Ask the user for any
missing inputs before executing each phase.

---

## Phase 0 — Clarify before touching anything

Ask the user for the following. Do not proceed until you have answers:

1. **Project name** — used as the directory name and Git repo name (kebab-case, e.g. `my-project`)
2. **Package name** — the Python import name (snake_case, e.g. `my_project`)
3. **One-line description** — what the project does
4. **Python minimum version** — default: `>=3.12`
5. **Library or app?** — library (installable package with public API) or app (scripts/CLI only)
6. **Reference material?** — any PDFs, papers, or external docs to keep in `material/`?
7. **Reference repos?** — any GitHub repos to clone into `tmp/` for reading/reference?
8. **GitHub org/user** — for CI config and remote URL

Confirm everything with the user before proceeding.

---

## Phase 1 — Repository and package structure

```sh
# In the parent directory where the project should live:
uv init <project-name> --lib        # for a library
# OR
uv init <project-name>              # for an app / scripts-only project
cd <project-name>
git init
```

Create the canonical directory layout:

```
<project-name>/
├── src/
│   └── <package_name>/
│       └── __init__.py
├── scripts/          # entry-point scripts (not installed, run with uv run)
├── tests/
│   └── __init__.py  # leave empty
├── plans/            # all planning and reference documents (see Phase 3)
├── material/         # PDFs, papers, reference spreadsheets (gitignored)
├── tmp/              # cloned reference repos, read-only (gitignored)
├── AGENTS.md         # agent instructions (canonical — CLAUDE.md points here)
├── CLAUDE.md         # one line: @AGENTS.md
├── pyproject.toml    # managed by uv
├── uv.lock           # committed
└── .gitignore
```

Configure `pyproject.toml` — replace the uv-generated stub with:

```toml
[project]
name = "<project-name>"
version = "0.1.0"
description = "<one-line description>"
readme = "README.md"
requires-python = ">=3.12"
dependencies = []

[project.optional-dependencies]
dev = []

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[tool.hatch.build.targets.wheel]
packages = ["src/<package_name>"]

[tool.pytest.ini_options]
testpaths = ["tests"]

[tool.mypy]
python_version = "3.12"
strict = true
ignore_missing_imports = true

[tool.ruff]
src = ["src"]
ignore = ["E501", "S101"]
```

Set up `.gitignore`:

```gitignore
# Reference material and repos (large, locally cloned)
material/
tmp/

# Planning scratch files
scratchbook.md
CHANGELOG_STAGING.md

# Dev tooling
.venv/
__pycache__/
*.py[cod]
.pytest_cache/
.mypy_cache/
.ruff_cache/
*.egg-info/
.env
.claude/
.agents/

# Project-specific large data (add your own)
# /data/
```

---

## Phase 2 — Agent infrastructure

### CLAUDE.md

```markdown
@AGENTS.md
```

That is the entire file — it delegates to `AGENTS.md` which is the canonical instruction source.

### AGENTS.md

Write a full `AGENTS.md` covering:

**Sections (in order):**

1. `## Project Orientation` — what the project is, key directory layout, any external services or compute constraints the agent must know about
2. `## General LLM Instructions` — the standard rules below (copy verbatim, they are project-agnostic)
3. `## Python Conventions` — copy from the standard conventions below
4. `## Docstrings` — Google style, all six sections, copy from standard below
5. `## Style and Formatting` — ruff as source of truth, copy from standard below
6. `## Testing` — pytest, fixed seeds, Suspicious Check, copy from standard below
7. `## Development Tooling` — uv commands table, pre-commit, git rules, copy from standard below
8. `## Plans and Reference Documents` — table of planning docs with "when to read" column
9. `## Validation and Local Checks` — copy from standard below

**Standard general LLM instructions to include in section 2:**

```markdown
### 1. Think Before Coding
Don't assume. Surface tradeoffs. State assumptions explicitly. Push back when warranted.

### 2. Simplicity First
Minimum code that solves the problem. No speculative features, no premature abstractions. IF YOU WRITE 200 LINES AND IT COULD BE 50, REWRITE IT.

### 3. Surgical Changes
Touch only what you must. Match existing style. Remove orphaned imports/variables your changes created. Don't clean up unrelated code.

### 4. Goal-Driven Execution
Transform tasks into verifiable goals. State a brief plan for multi-step tasks.
```

**Standard Python conventions to include in section 3:**

```markdown
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
```

**Standard docstring format (section 4):** Google style via sphinx.ext.napoleon. Types in signatures only — never repeat in Args/Returns. All six sections (Summary, Description, Args, Returns, Raises, Example) for public APIs.

---

## Phase 3 — Planning structure

Create `plans/` with these starter documents:

### `plans/implementation_plan.md`

Top-level map of the work: phases, milestones, open questions. This is the first document an agent reads when picking up work for the first time.

Structure:
```markdown
# Implementation Plan

## Phases
| Phase | Goal | Status |
|---|---|---|
| 0 | Bootstrap + CI | done |
| 1 | ... | todo |

## Open Questions
- ...

## Deferred
Link to plans/deferred.md for anything explicitly out of scope.
```

### `plans/devlog.md`

Running log of what has been built, decided, and done. Agents read this every session to rebuild context without re-reading git history.

Structure:
```markdown
# Dev Log

## YYYY-MM-DD — Session title
- What was done
- Decisions made and why
- Numbers/results if relevant
```

Add a `.claude/skills/devlog/SKILL.md` so agents can append to it with `/devlog`.

### `plans/deferred.md`

Explicit list of things that are out of scope. Prevents agents from implementing features that were intentionally excluded. Format:

```markdown
# Deferred

| ID | Feature | Reason |
|---|---|---|
| D1 | ... | out of scope for v1 |
```

### Optional plans (add as the project grows)

- `plans/architecture.md` — module structure, design decisions
- `plans/data.md` — data sources, formats, preprocessing (for data-heavy projects)
- `plans/benchmark.md` — performance baselines and targets

---

## Phase 4 — Developer tooling

### Pre-commit

```sh
uv add --dev pre-commit ruff mypy
uv run pre-commit install
```

Create `.pre-commit-config.yaml`:

```yaml
repos:
  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.9.10          # pin to a specific release — never use latest
    hooks:
      - id: ruff
        args: [--fix]
      - id: ruff-format
  - repo: https://github.com/astral-sh/uv-pre-commit
    rev: 0.5.21           # pin to a specific release
    hooks:
      - id: uv-lock
      - id: uv-sync
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v5.0.0
    hooks:
      - id: end-of-file-fixer
      - id: trailing-whitespace
```

### GitHub Actions CI

Create `.github/workflows/ci.yml`:

```yaml
name: CI

on:
  push:
    branches: [main]
  pull_request:

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: astral-sh/setup-uv@v5
        with:
          enable-cache: true
      - run: uv sync --locked --all-extras --dev
      - run: uv run ruff format --check .
      - run: uv run ruff check .
      - run: uv run mypy src/
      - run: uv run pytest tests/ -x
```

---

## Phase 5 — Agent skills

Create `.claude/skills/` for reusable agent commands. Each skill is a folder with a
`SKILL.md` that defines what the skill does and how to invoke it.

### Mandatory skills to create

**`/devlog`** — appends a dated entry to `plans/devlog.md`
```
.claude/skills/devlog/SKILL.md
```
Contents: instructions to append a `## YYYY-MM-DD — <title>` block summarising what was done in the current session.

**`/commit`** — enforces conventional commits format
```
.claude/skills/commit/SKILL.md
```
Contents:
- Conventional commits: `<type>(<scope>): <description>`
- Commit in thematic chunks, tests always separate
- No co-author trailers
- Append to `CHANGELOG_STAGING.md` after each commit session

### Optional skills to add later

- `/plan-context` — reads the relevant plan before implementation work
- `/ref-impl` — searches reference repos in `tmp/` for a specific pattern
- `/changelog` — generates versioned `CHANGELOG.md` entry from staging file

---

## Phase 6 — Reference material (if applicable)

If the project involves papers, specs, or external documents:

```sh
mkdir material/
# Copy PDFs, spreadsheets, etc. here
# Already gitignored from Phase 1
```

If the project involves reading other codebases as reference:

```sh
mkdir tmp/
# Clone reference repos here, read-only
# Already gitignored from Phase 1
# Document each repo in plans/tmp_repo_index.md:
#   - what it is
#   - what it is good for
#   - key files to look at
```

---

## Phase 7 — Scratchbook

Create `scratchbook.md` (gitignored) as a running glossary of domain concepts.
Agents append an entry whenever a non-obvious term appears (assay types, domain jargon, format names, algorithmic concepts):

```markdown
## <Concept name>

**What it is:** one-sentence definition.

**Analogy:** how this maps onto something familiar.

**Why it matters here:** which part of the project it touches.
```

---

## Phase 8 — First commit

```sh
git add AGENTS.md CLAUDE.md pyproject.toml uv.lock .gitignore .pre-commit-config.yaml \
        .github/ plans/ src/ tests/ scripts/
git commit -m "chore: bootstrap project structure"
```

Verify CI passes on the first push before doing any implementation work.

---

## Checklist

- [ ] `uv init` done, `src/` layout in place
- [ ] `pyproject.toml` configured with ruff, mypy, pytest sections
- [ ] `.gitignore` covers material/, tmp/, .claude/, .venv/, data/
- [ ] `CLAUDE.md` → `@AGENTS.md`
- [ ] `AGENTS.md` with all 9 sections filled in
- [ ] `plans/implementation_plan.md` drafted
- [ ] `plans/devlog.md` with session 0 entry
- [ ] `plans/deferred.md` created (even if empty)
- [ ] Pre-commit installed and hooks passing
- [ ] `.github/workflows/ci.yml` in place
- [ ] `.claude/skills/devlog/` and `.claude/skills/commit/` created
- [ ] First commit pushed, CI green
