# Performance Review

Performance should be evaluated in the context of the system rather than through isolated local improvements.

The goal is sufficiently performant software with justified complexity, not maximum local benchmark performance.

## Start with significance

Before recommending or defending a performance optimization, ask:

1. How often is this code executed?
2. How expensive is it relative to the surrounding operation?
3. What fraction of end-to-end runtime or resource use does it represent?
4. What is the expected system-level improvement?
5. What additional implementation and maintenance complexity does the optimization introduce?
6. Is the workload realistic for the repository's actual use cases?

A local 2× improvement may be irrelevant if the operation represents only a tiny fraction of end-to-end cost.

Prefer simpler code when the system-level improvement is negligible.

## Complexity must be justified

Performance can justify additional complexity when the benefit is meaningful.

Examples include:

* removing a demonstrated bottleneck;
* materially reducing end-to-end latency;
* materially increasing throughput;
* materially reducing memory pressure;
* reducing significant compute or infrastructure cost;
* avoiding pathological behavior for realistic workloads;
* enabling workloads that otherwise would not fit or complete.

Be skeptical of optimization complexity justified only by an isolated microbenchmark.

## Distinguish optimization types

### Bottleneck optimization

Evidence shows the affected code is a meaningful portion of runtime or resource consumption.

This is strong justification for optimization.

### Scaling optimization

The current workload may be acceptable, but algorithmic behavior becomes impractical for realistic larger inputs.

Examples:

* `O(n²)` behavior where expected input sizes make quadratic growth problematic;
* materializing datasets that may exceed memory;
* network calls proportional to individual records where batching is available.

Scaling improvements can justify additional complexity before current runtime becomes problematic, provided the expected scale is concrete.

### Micro-optimization

An isolated operation becomes faster but has little impact on the overall system.

Normally do not accept substantial complexity for this class of improvement.

## Consider more than runtime

Performance review may include:

* latency;
* throughput;
* memory usage;
* allocations and copies;
* disk I/O;
* network I/O;
* serialization;
* GPU utilization;
* CPU/GPU synchronization;
* accelerator data transfer;
* startup cost;
* compute or infrastructure cost;
* algorithmic scaling.

Review what matters for the actual workload.

## Avoid speculative optimization

Do not recommend:

* caching without a demonstrated reuse pattern;
* concurrency without meaningful parallel work;
* vectorization when the operation is not performance-sensitive;
* custom low-level implementations when standard implementations are adequate;
* memory pooling or reuse without allocation pressure;
* complicated batching without evidence that call overhead matters.

These mechanisms introduce their own complexity and failure modes.

## Performance regressions

Performance review should identify obvious regressions even without benchmarks.

Examples:

* moving an invariant computation inside a hot loop;
* introducing repeated disk or network access;
* converting a streaming operation into full materialization;
* repeated large tensor or array copies;
* unnecessary CPU/GPU transfers;
* accidentally changing linear behavior to quadratic behavior;
* recomputing identical expensive results.

When possible, explain the mechanism rather than claiming an unsupported magnitude.

## End-to-end impact

Do not treat a local benchmark improvement as sufficient justification.

For example, reducing a step from 200 ms to 100 ms is a 2× local speedup.

If the complete pipeline takes 30 seconds, the user-visible improvement is only about 0.3%.

When optimization adds significant complexity, evaluate the improvement at the level experienced by the caller or system.

Prefer the simpler implementation when the global impact is immaterial.

## Evidence

Prefer evidence in roughly this order:

1. end-to-end measurements;
2. profiler evidence;
3. representative benchmarks;
4. algorithmic analysis;
5. clearly justified reasoning from implementation behavior.

Do not invent performance claims.

If the impact cannot be established, state the uncertainty.

## Trade-off rule

When comparing implementations, consider:

* system-level performance benefit;
* expected scale;
* implementation complexity;
* cognitive cost;
* maintenance burden;
* new state or failure modes.

A useful default is:

> Accept meaningful complexity for meaningful performance or scaling benefits. Prefer simplicity when the benefit is marginal.

Performance is a constraint to satisfy, not an objective to maximize independently of the rest of the system.
