---
name: devlog
description: Append a concise development log entry for the current session while keeping recent history small and older entries archived and discoverable.
---

# Devlog Workflow

Use this skill when asked to record development work from the current session.

## Files

* Active log: `plans/devlog.md`
* Archive index: `plans/devlog/index.md`
* Archives: date-range Markdown files in `plans/devlog/`

`plans/devlog/index.md` is the navigation index, not an archive.

`plans/devlog.md` contains recent working history only.

## Entry Rules

* Use `## YYYY-MM-DD - <title>`.
* Keep entries concise and factual.
* Record:

  * what was implemented;
  * consequential technical decisions;
  * validation or tests performed;
  * important limitations or follow-up work.
* Prefer information future agents need to understand the current implementation.
* Omit conversational narrative, transient exploration, and details obvious from the code.
* Mention failed approaches only when they explain an important constraint or decision.

## Workflow

1. Read only the most recent relevant entries in `plans/devlog.md`.
2. Summarize the current session in one short entry.
3. Include meaningful commands/tests and whether they passed.
4. Append the entry to `plans/devlog.md`.
5. Check whether the active log needs rotation.
6. If needed, archive the oldest complete entries and update `plans/devlog/index.md`.

## Rotation

Keep the active log small.

Target:

* newest ~15 entries;
* roughly no more than 500 lines.

Prefer a date cutoff that keeps one cohesive recent implementation phase in the
active log. The entry count is approximate; staying below the line target is
more important than splitting a same-day phase solely to reach 15 entries.

If either limit is substantially exceeded:

1. Move the oldest complete entries into `plans/devlog/`.
2. Never split an entry.
3. Preserve archived entries verbatim.
4. Use date-range filenames such as `2026-07-01_to_2026-07-31.md`.
5. Append to an existing suitable archive instead of creating unnecessary files.
6. Keep the newest entries in `plans/devlog.md`.

Do not summarize away archived history during rotation.

When rotating a legacy log whose entries are out of chronological order, first
parse complete heading-delimited entries, sort them by heading date descending
while preserving original order for equal dates, and then apply the cutoff.
Preserve every entry block verbatim; only its archive placement may change.

## Archive Index

Keep `plans/devlog/index.md` as a compact navigation aid.

For each archive, record:

* filename;
* date range;
* a few major topics or milestones.

Do not list every individual entry.

When older context is needed, read the index first and open only the relevant archive.

The workflow does not change `.gitignore` rules. If plans or skills are ignored
locally, decide separately whether those files should remain local context or
receive explicit repository tracking exceptions.

## Entry Shape

```markdown
## YYYY-MM-DD - Short Title

- Implemented ...
- Decided ...
- Validated with ...
- Follow-up: ...
```

Omit bullets that add no useful information.

## Default Rule

Optimize for future context recovery per token.

Preserve important decisions and validation results while keeping the active log cheap to read.
