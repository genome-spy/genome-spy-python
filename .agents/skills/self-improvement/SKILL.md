---
name: self-improvement
description: Analyze coding-agent workflow patterns, repeated prompts, friction, and task structure to improve prompting, identify skill or automation opportunities, and use parallel agents more effectively.
---

# Workflow Review

Analyze how coding agents are being used and identify concrete ways to reduce repeated effort, rework, token use, and unnecessary sequential work.

The goal is not to maximize skills, agents, or automation. Add structure only when it reduces real workflow cost.

## Files

* Recent observations: `.agent-workflow/prompt-log.md`
* Durable patterns: `.agent-workflow/patterns.md`
* Improvement experiments: `.agent-workflow/improvement-backlog.md`

Use `references/heuristics.md` for classification and recommendation guidance.

## Observe

When reviewing a session or workflow, capture compact workflow observations rather than prompt transcripts.

Record useful signals such as:

* task type and context;
* repeated instructions;
* corrections or rework;
* misunderstood scope;
* overengineering or underexploration;
* unnecessary token-heavy investigation;
* missing validation;
* repeated manual steps;
* potentially independent sequential tasks;
* effective prompting patterns worth preserving.

Do not log every interaction.

Prefer observations that may change future agent usage.

## Analyze

Look across recent observations and existing patterns for:

* repeated prompts that could become reusable instructions;
* recurring failure or friction modes;
* instructions repeatedly added after the first attempt;
* tasks that should become skills, scripts, project instructions, or automation;
* opportunities to reduce context use;
* opportunities for safe parallel agent work;
* previous workflow improvements that did or did not help.

Treat isolated events cautiously. Prefer patterns supported by repeated evidence.

## Classify Improvements

For repeated work, determine whether it is best handled by:

* **Prompt** — rare or highly context-specific work.
* **Project instruction** — stable repository-specific rules or invariants.
* **Skill** — reusable reasoning or procedural workflow.
* **Script/tool** — deterministic mechanical work.
* **Automation/hook** — recurring work with a clear trigger.
* **Parallel agents** — independent tasks whose coordination cost is lower than the expected benefit.

Do not turn every recurring behavior into a skill.

## Parallelization

Recommend parallel agents only when tasks are meaningfully independent.

Good candidates include:

* inspecting separate subsystems;
* finding callers while another agent inspects tests;
* independent research or benchmarking;
* disjoint implementation work with clear ownership.

Avoid parallel work when agents would modify or reason heavily about the same code and require frequent synchronization.

Prefer one lead agent to synthesize parallel findings.

## Update Workflow State

When a durable pattern emerges:

1. Add or update it in `.agent-workflow/patterns.md`.
2. Record evidence concisely.
3. Note whether it is active, addressed, or being watched.

When an actionable improvement is identified:

1. Add it to `.agent-workflow/improvement-backlog.md`.
2. Prefer a small experiment over a large workflow redesign.
3. Define what improvement would indicate success.

Do not duplicate existing patterns or backlog items.

## Prompt Log Rotation

Keep `.agent-workflow/prompt-log.md` small.

Target approximately:

* newest 25–30 useful observations;
* no more than roughly 500 lines.

Before archiving old observations:

1. extract any durable recurring patterns;
2. move complete old observations into `.agent-workflow/archives/`;
3. preserve archived observations rather than summarizing them away.

Do not read archives unless older evidence is needed.

## Evaluation Principles

Prefer recommendations that:

* reduce repeated prompting;
* reduce corrections and rework;
* reduce unnecessary context or tool use;
* improve task decomposition;
* improve validation;
* encode stable knowledge once;
* make parallel work genuinely faster.

Avoid adding process whose coordination or maintenance cost exceeds its benefit.

## Output

When asked for a workflow review, report:

1. **Observed patterns** — supported by concrete recent evidence.
2. **Highest-value improvements** — prioritized by expected benefit.
3. **Skill/tool opportunities** — only where repetition is stable.
4. **Parallelization opportunities** — only where independence is clear.
5. **Experiments** — small workflow changes worth testing.

Prefer a few specific recommendations over broad prompting advice.

## Default Rule

> Optimize the human-agent system for useful work per unit of time, context, and coordination.

Encode repeated knowledge once, parallelize only independent work, and avoid workflow machinery that does not pay for itself.
