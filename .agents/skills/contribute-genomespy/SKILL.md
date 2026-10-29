---
name: contribute-genomespy
description: Use whenever work in genome-spy-python requires creating or updating an upstream GenomeSpy PR, including feature, fix, documentation and workflow changes.
---

# Contribute to GenomeSpy

1. Keep Python-specific work here. Put reusable engine behavior upstream when
   the existing native API cannot cover it cleanly.
2. Locate the intended GenomeSpy checkout and verify its Git remotes and branch;
   do not assume a temporary clone is current. Read its `AGENTS.md`.
3. Use that checkout's `.agents/skills/plan-genomespy-change/SKILL.md` before
   implementation and before opening or updating any upstream PR. If code is
   already written, run its architecture-fit check before PR preparation.
   Use `.agents/skills/prepare-genomespy-change/SKILL.md` for commits and PR
   preparation. Follow those upstream workflows rather than copying them here.
   If either skill is absent, locate the current instructions before proceeding.
4. Keep upstream edits separate from Python integration work and coordinate file
   ownership with active chats when authorized. Preserve the agreed release/source
   dependency; do not silently ship a local unreleased Core build.
5. Report the upstream PR/commit, verification and remaining integration dependency.
