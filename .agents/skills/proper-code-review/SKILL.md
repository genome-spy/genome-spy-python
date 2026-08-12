---
name: proper-code-review
description: Review code changes for correctness, simplicity, readability, maintainability, architectural fit, and meaningful system-level performance. Use when asked to review a diff, implementation, branch, or recent code changes.
---

# Code Review

Review the current changes as a senior engineer.

Optimize for correctness and low total lifecycle complexity. Prefer simple, readable, maintainable implementations that fit the existing repository and are sufficiently performant for realistic workloads.

Prefer a few high-confidence findings over exhaustive commentary.

## Core Principles

* Correctness comes first.
* Prefer the simplest adequate solution (the KISS principle).
* Optimize for local reasoning and localized change.
* Avoid duplicated knowledge and parallel mechanisms.
* Reuse existing repository concepts when appropriate.
* Avoid speculative abstraction and extensibility.
* Require concrete justification for added complexity.
* Judge performance at the system level, not only locally.
* Do not manufacture findings.

Complexity must pay for itself through a concrete benefit such as correctness, meaningful reuse, change locality, real variation, necessary scalability, or material performance.

## Review Method

### 1. Understand the change

Read the diff first.

Determine:

* what problem the change solves;
* what behavior changes;
* which interfaces, invariants, state, or architectural concepts are affected.

Inspect only enough surrounding repository context to answer concrete review questions.

When relevant:

* inspect callers before claiming breakage;
* inspect tests for intended behavior and invariants;
* search for existing mechanisms before proposing new ones;
* inspect analogous implementations when evaluating duplication or architectural fit;
* inspect the broader execution path when evaluating performance.

Do not attempt to understand the entire repository.

### 2. Verify before judging

Treat potential findings as hypotheses.

Before reporting a concern, verify it against the repository when possible.

Examples:

* locate the duplicated representation before claiming duplicated knowledge;
* inspect callers before claiming API incompatibility;
* search for existing abstractions before proposing a new one;
* establish performance significance before criticizing or recommending optimization.

Do not present assumptions as facts.

### 3. Review correctness

Look for concrete:

* behavioral bugs and regressions;
* broken invariants;
* invalid assumptions;
* relevant edge cases;
* unsafe mutation or state transitions;
* error-handling or resource-lifecycle problems;
* concurrency issues;
* unintended compatibility changes.

Passing tests are evidence, not proof.

Use `references/correctness.md` when deeper analysis is useful.

### 4. Review design

Evaluate simplicity, readability, maintainability, cohesion, coupling, abstraction, change locality, blast radius, and architectural fit together.

Ask:

* Could this be simpler? The KISS principle!
* Can it be understood and changed locally?
* Does one conceptual change require synchronized edits?
* Has unnecessary machinery been introduced?
* Does this duplicate an existing repository mechanism?
* Does an abstraction represent real shared semantics?
* Is the solution proportional to the problem?
* YAGNI principle ("You Aren't Gonna Need It")

Prefer straightforward implementations when additional cleverness provides little concrete benefit.

Use `references/design.md` when deeper analysis is useful.

### 5. Review performance

Look for meaningful issues involving:

* algorithmic complexity;
* repeated expensive work;
* I/O;
* memory and copying;
* serialization or data movement;
* CPU/GPU synchronization;
* realistic scaling.

Judge optimizations by end-to-end impact.

Do not accept meaningful complexity for negligible local gains.

Use `references/performance.md` when performance is relevant.

### 6. Validate findings

Before reporting each finding, ask:

* Is the problem concrete?
* Is the consequence meaningful?
* Does the evidence support it?
* Is the recommendation proportionate?
* Does the proposed fix reduce total complexity?

Remove speculative, cosmetic, generic, or low-value comments.

Prefer no finding over a weak finding.

## Output

Report findings in descending order of practical impact.

For each finding:

### `[Severity] Short problem statement`

**Location:** Smallest useful code region.

**Problem:** What is wrong.

**Impact:** Why it matters here.

**Recommendation:** Smallest reasonable fix.

Use:

* **Critical** — correctness, data loss, security, or severe failure.
* **Important** — substantial behavioral, architectural, maintainability, performance, or scalability issue.
* **Minor** — worthwhile simplification or readability improvement.

Normally omit stylistic nits.

Combine findings with the same root cause.

State uncertainty explicitly.

Do not include generic best-practice advice, speculative future concerns, praise for unaffected code, or alternative architectures merely because they are possible.

If no meaningful issues remain, say that no significant issues were found.
