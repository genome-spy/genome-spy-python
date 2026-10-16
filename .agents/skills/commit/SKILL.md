---
name: commit
description: Commit repository changes in small thematic chunks using conventional commits and concise changelog staging.
---

# Commit workflow

Prefer small, independently understandable commits. Keep unrelated user changes
unstaged. Do not amend, rewrite history, revert, force-push, or add co-author
trailers unless explicitly requested.

## Inspect and commit

1. Start with `git status --short` and `git diff --stat`.
2. Group changes into thematic slices. Split separate features, fixes, refactors,
   tooling/configuration, documentation, and unrelated test work when separable;
   do not split mechanically by file.
3. Keep implementation with its direct tests, API/schema changes with required
   supporting code, and generated files with their source change.
4. Read targeted diffs only when needed, including when grouping is unclear:
   `git diff -- <files>`. Minimize token use; do not read the full diff or re-review
   code by default.
5. Stage one slice, check `git diff --cached --stat`, and commit with a conventional
   message. Repeat for remaining slices.
6. Finish with `git status --short`, update changelog staging once if needed, and
   report commit hashes and remaining uncommitted files.

## Commit messages

Use `<type>(<scope>): <description>`. Common types: `feat`, `fix`, `refactor`,
`perf`, `test`, `docs`, `chore`, `build`, and `ci`.

```text
feat(parser): add strand-aware bigwig loading
fix(cache): invalidate stale entries
refactor(pipeline): simplify track dispatch
```

## Changelog staging

`CHANGELOG_STAGING.md` holds future release notes. Update it once per commit
session only for release-relevant changes:

- Read only the context needed.
- Add concise bullets under `Added`, `Changed`, `Fixed`, `Removed`, or `Performance`.
- Prefer one resulting-change bullet over one per commit; avoid duplicates.
- Omit routine refactors, formatting, test-only work, and internal details unless
  release-relevant.
