# Library integrations

Integrations let users keep another library's analysis workflow and replace its
supported plotting calls with native GenomeSpy charts. The installed namespace
is `genome_spy.<library>`; each integration declares its own optional dependencies,
compatibility contract, and tested upstream versions.

| Integration | Implementation | Development workspace | Validation | User guide |
| --- | --- | --- | --- | --- |
| Scanpy (UMAP preview) | [Python package](../src/genome_spy/scanpy/) | [Plan and notebooks](scanpy/README.md) | [Tests and reference tooling](../tests/integrations/scanpy/) | [Compatibility guide](../docs/integrations/scanpy/index.md) |

Use these locations for each integration:

- `src/genome_spy/<library>/`: installable plotting implementation.
- `integrations/<library>/`: tracked implementation plan and workflow notebooks.
- `tests/integrations/<library>/`: semantics, reference fixtures, browser checks,
  explicit reference generation, and benchmarks.
- `docs/integrations/<library>/`: user-facing documentation.

Generic `tools/` stays for shared schema/Altair-derived development and
documentation utilities. Integration-specific validation belongs with its tests.
Runtime modules must never import notebooks, validation code, or research trials.

Keep the integrations thin and explicit. Add shared integration abstractions only
when a second implemented library demonstrates a concrete need. Documentation
navigation and notebook presentation must be designed before adding a rendered
integration-workflow section to the site; see the [Scanpy plan](scanpy/PLAN.md).
