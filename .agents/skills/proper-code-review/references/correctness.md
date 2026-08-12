# Correctness Review

Correctness review asks whether the change preserves the intended behavior of the system across realistic inputs, states, and failure conditions.

Passing tests are evidence of correctness, not proof.

## Understand the Contract

Determine what the code is expected to guarantee.

Consider:

* input assumptions;
* output guarantees;
* state transitions;
* API behavior;
* ordering;
* persistence;
* error behavior;
* compatibility;
* important domain invariants.

A correctness finding should identify a concrete way the intended contract can be violated.

## Behavioral Changes

Check whether the patch changes behavior beyond its stated purpose.

Look for unintended changes to:

* defaults;
* return values or shapes;
* ordering;
* mutation;
* exceptions;
* serialization;
* persistence;
* handling of missing or invalid input;
* behavior visible to callers.

Small implementation changes can have large effects at module boundaries.

## Edge Cases and Invariants

Prioritize edge cases that are realistic for the domain and changed logic.

Examples include:

* empty or single-element inputs;
* missing or malformed data;
* duplicates;
* boundary values;
* partial failures;
* large inputs where behavior changes.

Identify invariants that must remain true, such as:

* related collections remaining aligned;
* identifiers remaining unique;
* ordering being preserved;
* cached state matching source state;
* state transitions occurring in a valid order.

Do not generate exhaustive theoretical edge cases without evidence that they matter.

## State and Mutation

Ask:

* What state is mutated?
* Is mutation expected by callers?
* Can partial mutation remain after failure?
* Is state shared across calls?
* Can stale state survive?
* Does aliasing versus copying matter?

Pay particular attention when the change introduces shared state, caching, batching, or multiple representations of the same data.

## Error and Resource Handling

Look for:

* swallowed exceptions;
* overly broad exception handling;
* failures converted into silently incorrect results;
* lost error context;
* retries that can duplicate side effects;
* cleanup skipped on exceptions or early returns.

When relevant, verify lifecycle handling for files, sockets, database connections, subprocesses, locks, temporary files, and accelerator resources.

Do not recommend defensive error handling without a concrete failure mode.

## Concurrency

When the change involves threads, processes, asynchronous execution, or shared state, inspect:

* races;
* ordering assumptions;
* atomicity;
* cancellation;
* shared mutation;
* duplicated work;
* deadlocks;
* partial completion;
* exception propagation.

Do not flag concurrency merely because it is complex. Identify a concrete unsafe interaction.

## Boundaries and Compatibility

Pay attention where assumptions cross boundaries, such as:

* parser → internal representation;
* serializer → external format;
* CPU → GPU;
* synchronous → asynchronous execution;
* library → application;
* application → persistent storage.

Check relevant types, shapes, units, coordinate systems, encoding, ownership, and lifetime.

When interfaces change, inspect relevant consumers before claiming breakage.

Do not demand backward compatibility unless the repository actually requires it.

## Tests

Use tests to understand intended behavior, invariants, and regression risk.

Recommend a test when it protects an important contract, subtle behavior, edge case, or plausible regression.

Do not request tests merely because code changed.

Avoid tests that only duplicate implementation details.

## Uncertainty

Distinguish demonstrated bugs from risks that still require verification.

State missing assumptions explicitly.

Never present speculation as fact.

## Default Rule

Before reporting a correctness finding, answer:

> Under what realistic condition does this implementation violate its intended contract?

If that cannot be explained, the concern may be a design issue rather than a correctness bug.
