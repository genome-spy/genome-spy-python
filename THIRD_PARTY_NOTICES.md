# Third-party notices

## Code adapted from Vega-Altair

Parts of this project are adapted from
[Vega-Altair](https://github.com/vega/altair), copyright 2015–2025 the
Vega-Altair Developers, under the BSD-3-Clause license. The complete license
is in [`LICENSES/ALTAIR-BSD-3-Clause.txt`](LICENSES/ALTAIR-BSD-3-Clause.txt).

The adapted areas are:

- `src/genome_spy/schemapi.py`, a reduced schema-wrapper runtime based on
  `altair/utils/schemapi.py`;
- `tools/schemapi/codegen.py`, whose schema-wrapper generation architecture is
  adapted from Altair's `tools/schemapi/` package and
  `tools/generate_schema_wrapper.py`;
- the multifeature penguins and cars strip-plot cases in `tests/test_chart.py`,
  adapted from Altair's example suite and mark documentation.

Each adapted source location identifies its corresponding upstream source.

## Design references

Altair also informed the separation between generated schema bindings and the
handwritten chart API, composition operators, channel shorthand, and API
reference organization. Those areas use project-specific implementations and
are acknowledged as design references rather than adapted Altair code.
