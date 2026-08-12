# Design Review

Evaluate simplicity, readability, maintainability, abstraction, coupling, cohesion, change locality, and architectural fit together.

The goal is low total cognitive and maintenance burden, not minimum line count or maximum reuse.

## Core Rule

Every added concept has a cost.

Examples include:

* classes and interfaces;
* factories and registries;
* wrappers and adapters;
* callbacks and indirection;
* configuration layers;
* caching and shared state;
* concurrency;
* generic frameworks.

Require that added complexity provides a concrete benefit such as:

* correctness or invariant enforcement;
* representing real variation;
* removing duplicated domain knowledge;
* improving change locality;
* meaningful reuse;
* isolating genuinely volatile behavior;
* material performance or scalability.

Be skeptical of complexity justified mainly by hypothetical future requirements.

## Simplicity

Prefer the least complicated implementation that adequately solves the current problem.

When appropriate, prefer:

* functions over classes when state or polymorphism is unnecessary;
* direct control flow over indirection;
* ordinary data structures over custom abstractions;
* small named helpers when they reduce cognitive load;
* existing repository mechanisms over new parallel systems.

Do not equate simplicity with fewer lines, fewer functions, or no abstraction.

An abstraction is useful when it reduces total reasoning and maintenance burden more than it adds conceptual or navigation cost.

## Abstraction and Duplication

Do not abstract merely because code looks similar.

Ask:

> Does this represent the same knowledge and therefore need to evolve together?

If multiple locations must remain synchronized, centralizing that knowledge may improve maintainability.

If pieces only look similar but may evolve independently, keeping them separate can be simpler.

Distinguish:

* **Useful abstraction** — represents real shared semantics or variation.
* **Premature abstraction** — models hypothetical future variation.
* **Wrong abstraction** — couples concepts that change for different reasons.

A small amount of duplication can be preferable to the wrong abstraction.

## Readability

Code should make intent, control flow, assumptions, and state understandable without excessive mental simulation.

Look for:

* unclear intent;
* deeply nested or hidden control flow;
* non-obvious mutation;
* excessive indirection;
* functions mixing unrelated conceptual levels;
* names that hide domain meaning.

Extract helpers when they name meaningful operations, isolate tricky logic, or reduce cognitive load.

Do not extract code solely because a function is long.

Prefer comments that explain rationale, constraints, or domain knowledge rather than restating the implementation.

## Maintainability and Change Locality

Prefer designs where conceptual changes remain localized.

Look for:

* duplicated domain rules;
* repeated mappings or configuration;
* parallel conditionals that must remain synchronized;
* equivalent state represented in multiple layers;
* unclear ownership;
* unnecessary knowledge of another component's internals.

Ask:

> How many places must change when this concept changes?

Multiple edits are not automatically bad. The concern is multiple independent representations of the same knowledge.

## Cohesion and Coupling

Related behavior should live together.

Ask whether a developer would naturally look for the behavior where it currently lives.

Flag coupling when implementation details leak across boundaries or unrelated changes propagate through the system.

Do not automatically respond with interfaces, dependency injection, or additional abstraction. Recommend new machinery only when it solves the concrete problem more simply.

## Architectural Fit

Review the change in repository context.

Check whether it:

* duplicates an existing utility or subsystem;
* introduces a second mechanism for the same problem;
* bypasses established ownership boundaries;
* adds concepts disproportionate to surrounding code.

Prefer existing patterns when they are adequate, but do not preserve a clearly harmful pattern merely for consistency.

## Change Blast Radius

Consider whether the breadth of the implementation is proportional to the conceptual change.

Ask:

> How much of the repository had to know about this change?

Be concerned when a small conceptual change requires synchronized modifications across unrelated layers because the same concept is represented repeatedly.

Do not penalize a large diff merely for being large.

## Accretion

Watch for systems that grow through repeated:

* special cases;
* flags;
* compatibility branches;
* wrappers;
* alternate execution paths.

Ask whether existing logic can be simplified, removed, or generalized instead of adding another layer.

## Default Rule

When multiple implementations are correct and sufficiently performant:

> Prefer the implementation with the lowest total cognitive and maintenance burden.

Complexity must justify itself.
