---
name: commit
description: Commit repository changes in small thematic chunks using conventional commits and concise changelog staging.
---

# Commit Workflow

Prefer several small thematic commits over one broad commit.

## Rules

* Run `git status --short` first.
* Use conventional commits: `<type>(<scope>): <description>`.
* Split independently meaningful changes.
* Keep implementation and its direct tests together when they form one change.
* Leave unrelated user changes unstaged.
* Do not amend, rewrite history, revert, force-push, or add co-author trailers unless explicitly requested.

## Efficient Inspection

Minimize token use.

Use:

```bash
git status --short
git diff --stat
```

Use targeted diffs only when needed:

```bash
git diff -- <files>
```

Do not read the full diff or re-review code by default.

## Workflow

1. Inspect `git status --short`.
2. Group files into thematic commit slices.
3. Use targeted diffs only when grouping is unclear.
4. Stage one slice.
5. Verify with `git diff --cached --stat`.
6. Commit with a conventional commit message.
7. Repeat for remaining slices.
8. Run `git status --short` at the end.
9. Update `CHANGELOG_STAGING.md` once if release-relevant changes were committed.
10. Report commit hashes and remaining uncommitted files.

## Commit Boundaries

A commit should represent one independently understandable change.

Split separate features, fixes, refactors, tooling/config changes, documentation, and unrelated test work.

Usually keep together:

* implementation and direct tests;
* API/schema changes and required supporting code;
* generated files and their source change.

Do not split mechanically by file.

When cleanly separable, prefer multiple commits.

## Conventional Commits

Common types:

* `feat`
* `fix`
* `refactor`
* `perf`
* `test`
* `docs`
* `chore`
* `build`
* `ci`

Examples:

```text
feat(parser): add strand-aware bigwig loading
fix(cache): invalidate stale entries
refactor(pipeline): simplify track dispatch
```

## Changelog Staging

`CHANGELOG_STAGING.md` is for future release notes.

Update it once per commit session only for release-relevant changes.

* Read only the minimum needed context.
* Add concise bullets under `Added`, `Changed`, `Fixed`, `Removed`, or `Performance`.
* Prefer one resulting-change bullet over one bullet per commit.
* Omit routine refactors, formatting, test-only work, and internal details unless release-relevant.
* Avoid duplicates.

## Default Rule

> Prefer the smallest coherent commit representing one independently understandable change.

Avoid unnecessary diff reading.
