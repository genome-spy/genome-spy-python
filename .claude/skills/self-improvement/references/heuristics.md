# Workflow Review Heuristics

Use these heuristics to turn observations into actionable workflow improvements.

## Friction Categories

Prefer concrete workflow classifications over generic sentiment.

Useful categories include:

* **scope-miss** — agent solved the wrong or broader problem;
* **repeat-instruction** — user repeatedly supplies the same constraint;
* **overengineering** — unnecessary abstraction or machinery;
* **underexploration** — insufficient repository/context inspection;
* **overexploration** — unnecessary context or token-heavy investigation;
* **incorrect-assumption** — agent proceeded without verifying an important assumption;
* **missed-existing-pattern** — agent recreated something already present;
* **weak-validation** — implementation was insufficiently tested or checked;
* **large-change** — task was implemented as an unnecessarily broad change;
* **manual-step** — repeated mechanical work remains manual;
* **poor-decomposition** — task boundaries caused avoidable rework;
* **parallelization-opportunity** — independent work was performed sequentially.

User frustration may increase the significance of a signal, but the underlying engineering cause is more important than sentiment itself.

## Prompt Improvement

When a prompt required correction, ask:

> What stable information could have been provided earlier?

Good candidates include:

* scope boundaries;
* existing architectural constraints;
* expected validation;
* simplicity requirements;
* files or subsystems that matter;
* explicitly excluded work.

Do not make prompts longer by default. Prefer moving recurring instructions into stable reusable context.

## Skill Candidates

A repeated task is a good skill candidate when:

* the workflow occurs repeatedly;
* its rules are relatively stable;
* meaningful reasoning or judgment is required;
* encoding the process would reduce repeated prompting.

Examples:

* code review;
* commit preparation;
* debugging workflow;
* release preparation.

Do not create a skill merely because similar words appear frequently.

## Project Instruction Candidates

Prefer project instructions for stable repository-specific facts such as:

* architectural conventions;
* forbidden dependencies;
* testing requirements;
* domain invariants;
* preferred project structure.

Do not hide important repository invariants inside an optional skill when all coding agents should know them.

## Script or Tool Candidates

Prefer scripts for deterministic mechanical tasks with little judgment.

Examples:

* formatting generated files;
* repetitive conversions;
* collecting standard metrics;
* deterministic file manipulation.

If the same operation can be reliably expressed as code, a script is often cheaper than repeated agent reasoning.

## Automation Candidates

Prefer automation or hooks when:

* the trigger is predictable;
* the action is recurring;
* little human judgment is required at trigger time.

Avoid automation when the task regularly requires contextual decisions.

## Parallel Agent Candidates

Parallel work is useful when:

* tasks are independent;
* outputs can be synthesized cleanly;
* agents do not need frequent shared state;
* coordination overhead is lower than expected time savings.

Good examples:

* caller analysis and test analysis;
* separate subsystem exploration;
* independent benchmarking;
* disjoint implementation units.

Poor examples:

* several agents editing the same function;
* agents making competing architectural decisions;
* tiny tasks where dispatch overhead dominates.

## Detecting Repeated Patterns

Prefer recurrence over isolated incidents.

A pattern becomes stronger when:

* the same correction appears across multiple sessions;
* the same manual prompt is repeatedly issued;
* the same recovery workflow is repeatedly needed;
* a prior improvement measurably reduced the problem.

Record counter-evidence when a suspected pattern stops recurring.

## Improvement Experiments

Prefer small reversible experiments.

For each experiment, define:

* the observed problem;
* the proposed workflow change;
* what outcome would count as improvement.

Examples of useful outcomes:

* fewer corrective prompts;
* fewer unnecessary tool calls;
* smaller context consumption;
* fewer broad commits;
* less post-implementation simplification;
* reduced elapsed workflow steps.

## Anti-Overengineering Rule

The workflow system itself can become overengineered.

Do not recommend a new:

* skill;
* agent;
* log;
* automation;
* orchestration layer;

unless its expected benefit exceeds its maintenance and coordination cost.

The objective is better work, not more workflow infrastructure.
