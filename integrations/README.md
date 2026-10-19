# Library integrations

Integrations let users keep another library's analysis workflow and replace its
supported plotting calls with native GenomeSpy charts. Implementations live in
`genome_spy.integrations.<library>`. Each integration declares optional
dependencies, a compatibility contract, and tested upstream versions.

| Integration | Implementation | Progress | Development workspace | User guide |
| --- | --- | --- | --- | --- |
| Scanpy (nineteen plotting previews) | [Python package](../src/genome_spy/integrations/scanpy/) | [Status and next work](scanpy/STATUS.md) | [Plan and notebooks](scanpy/README.md) | [Compatibility guide](../docs/integrations/scanpy/index.md) |

Use these locations for each integration:

- `src/genome_spy/integrations/<library>/`: installable implementation.
- `integrations/<library>/PLAN.md`: scope, delivery slices, acceptance criteria.
- `integrations/<library>/STATUS.md`: current progress, next slice, blockers,
  evidence, and plan clearance decisions.
- `integrations/<library>/notebooks/`: canonical runnable upstream workflows.
- `tests/integrations/<library>/`: semantics, reference fixtures, browser checks,
  explicit reference generation, and benchmarks.
- `docs/integrations/<library>/`: user-facing documentation.

Use `genome_spy.integrations.<library>` consistently in code and examples.
Base and integration namespace imports must remain lightweight.

Generic `tools/` stays for shared schema/Altair-derived development and
documentation utilities. Integration-specific validation belongs with its tests.
Runtime modules must never import notebooks, validation code, or research trials.

Keep integrations thin and explicit. Reuse compatible data access, colors, and
computations within an integration. Add shared cross-library abstractions only
when another implemented library demonstrates a concrete need. Do not create
empty integration packages or a generic adapter framework in advance.

## Plan lifecycle

Use Markdown and the existing tests and Git history. There is no separate project
tracker to keep synchronized. Each integration has one live plan and one status
ledger. A short working plan for a complex slice is optional; link it from the
ledger and remove it through the clearance process below.

| State | Meaning and required evidence |
| --- | --- |
| Planned | Named outputs, dependencies, and completion criteria exist; implementation has not started. |
| Ready | Required inputs and released native capabilities exist, and the next slice has a concrete upstream call and validation cases. |
| In progress | Work has started; record the active slice and unresolved decisions. |
| Implemented | Runtime behavior and direct tests exist; required verification is still outstanding. |
| Verified | The slice's semantic, chart, workflow, interaction (if offered), and resource checks passed; evidence and limits are linked. |
| Closed | Verified outputs are in their permanent homes; residual work has explicit owners in later slices, and the next ready item is recorded. |
| Blocked | Record the unavailable dependency, affected slice, and event that warrants rechecking. Independent work continues. |

A preview can close a deliberately limited slice. It cannot close a full-family
milestone whose required parameters or builder methods remain missing. Status
must distinguish function availability, parameter coverage, and method coverage.
Every implementation change updates the relevant ledger row, acceptance evidence,
remaining limits, and next item. Record a commit/PR or stable source/test links;
long console logs do not belong in the plan. Do not mark future work verified
because a prototype or a different plot passed.

## Clearance and retention

Completion and readiness to remove a plan are separate decisions. Give each
working document a clearance state: **retain**, **eligible**, or **cleared**.

A working plan becomes eligible when:

1. Its implementation is verified and recorded in Git.
2. Every contract, design decision, and known limitation has moved to maintained
   documentation, source, tests, or an explicitly named future slice.
3. Reproduction inputs, reference metadata, provenance, and unique findings are
   retained where a fresh clone can use them, or deliberately identified as local
   historical evidence.
4. Its status row records completion evidence, residual work, and the next item.

Then remove redundant working prose in a small change and leave a completion
record in `STATUS.md` with the commit and retained evidence. Record the removal
commit there on a later update if needed. Do not clear active scope merely
because one preview works. Keep live `PLAN.md` and `STATUS.md` until the integration
roadmap is closed; then replace the plan with a short completed-scope record.
Keep user contracts, API inventories, tests, provenance, and useful notebooks as
maintained assets rather than treating them as disposable plans.

Ignored research under `plans/` and `tmp/` is not required for a fresh clone.
Reconcile its unique findings before marking it eligible; archive useful historical
evidence and discard redundant scratch material only after that review. Never
remove the only copy of a reference or an unfinished study by calling it an
implemented plan. Cleanup is an explicit scoped change, not a side effect of
finishing a plot.

## Documentation publication

Design navigation and notebook presentation before adding rendered integration
workflows to the site. The [Scanpy roadmap](scanpy/PLAN.md#documentation-and-release)
includes the first landing/workflow layouts and rendering proof. New integrations
reuse that presentation only when it fits their actual workflows.
