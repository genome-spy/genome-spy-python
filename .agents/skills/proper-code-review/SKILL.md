---
name: proper-code-review
description: Review code changes for correctness, simplicity, readability, maintainability, architectural fit, and meaningful system-level performance. Use when asked to review a diff, implementation, branch, or recent code changes.
---

# Code review

Review as a senior engineer. Prioritize correctness and low lifecycle complexity:
simple, readable, maintainable code that fits the repository and performs well for
realistic workloads. Prefer a few high-confidence findings over exhaustive
commentary; do not manufacture findings.

Added complexity must provide a concrete benefit: correctness, meaningful reuse,
change locality, real variation, necessary scalability, or material performance.
Prefer local reasoning and localized changes. Reuse suitable repository concepts,
avoid duplicated knowledge and parallel mechanisms, and reject speculative
abstraction/extensibility. Judge performance across the system, not just locally.

## Review method

1. **Understand the change.** Read the diff first. Identify its problem, behavior
   changes, affected interfaces, invariants, state, and architectural concepts.
   Read only enough surrounding code to answer concrete questions, not the whole
   repository. When relevant, inspect callers for compatibility, tests for intended
   behavior/invariants, existing mechanisms before proposing new ones, analogous
   implementations for duplication/fit, and broader execution paths for performance.
2. **Verify hypotheses.** Check concerns against repository evidence when possible.
   Locate duplicated representations, inspect callers before claiming breakage,
   search for existing abstractions, and establish performance significance before
   criticizing or recommending optimization. Do not present assumptions as facts.
3. **Review correctness.** Look for concrete behavioral bugs/regressions, broken
   invariants, invalid assumptions, relevant edge cases, unsafe mutations/state
   transitions, error/resource lifecycle issues, concurrency problems, and
   unintended compatibility changes. Passing tests are evidence, not proof.
   Read [correctness](references/correctness.md) for deeper analysis.
4. **Review design.** Consider simplicity (KISS), readability, maintainability,
   cohesion, coupling, abstraction, change locality, blast radius, and fit together.
   Check whether a simpler solution supports local understanding/change, whether
   synchronized edits duplicate knowledge, whether machinery is unnecessary,
   whether abstractions share real semantics, and whether scope is proportional.
   Apply YAGNI: avoid cleverness or future machinery without concrete benefit.
   Read [design](references/design.md) for deeper analysis.
5. **Review performance.** Check algorithmic complexity, repeated expensive work,
   I/O, memory/copying, serialization/data movement, CPU/GPU synchronization, and
   realistic scaling. Judge end-to-end impact; reject meaningful complexity for
   negligible local gains. Read [performance](references/performance.md) when relevant.
6. **Validate findings.** Each problem must be concrete, consequential, supported
   by evidence, and paired with a proportionate fix that reduces total complexity.
   Remove speculative, cosmetic, generic, and low-value comments. No finding is
   better than a weak finding.

## Output

Order findings by practical impact. For each, use:

### `[Severity] Short problem statement`

- **Location:** Smallest useful code region.
- **Problem:** What is wrong.
- **Impact:** Why it matters here.
- **Recommendation:** Smallest reasonable fix.

Severity:

- **Critical:** Correctness, data loss, security, or severe failure.
- **Important:** Substantial behavioral, architectural, maintainability,
  performance, or scalability issue.
- **Minor:** Worthwhile simplification or readability improvement.

Combine findings with the same root cause and state uncertainty explicitly.
Normally omit stylistic nits. Do not add generic best-practice advice, speculative
future concerns, praise for unaffected code, or alternative architectures merely
because they are possible. If none remain, say no significant issues were found.
