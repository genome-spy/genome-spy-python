# Third-party notices

## Gallery data from maftools and Plotly

`tcga_laml_combined_oncoplot.json.gz` contains prepared TCGA LAML tables from
maftools revision `015a4cf8c69ba89a55a3fdcea911421509e9a198` (Anand Mayakonda,
MIT). `p53_sequence_comparison.json.gz` contains p53 sequences and derived
display tables from Plotly's datasets revision
`0c447c47b757ad74edecab31f0d72f849d2e67c2` (Plotly Technologies Inc., MIT).
Source file hashes are retained in the packaged data. The corresponding gallery
pages describe processing. Copyright notices and terms are included in
`LICENSES/GALLERY-DATA-MIT.txt`.

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

MutGlyph informed the generic scored gene-annotation track used by the
rainfall and GISTIC examples. The implementation and UCSC-derived data are
maintained independently in this repository.
