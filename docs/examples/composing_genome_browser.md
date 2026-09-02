:::{admonition} Data use and provenance
:class: note

The imported specifications and their data come from the official GenomeSpy
examples listed below. The URLs are pinned to one upstream commit so the
gallery does not silently change when GenomeSpy's main branch changes.
:::

## Imported track specifications

This example intentionally loads four existing JSON view specifications. Each
source has a corresponding Python-authored gallery example that shows how the
track itself can be constructed:

| Imported JSON specification | Python-authored example | Official GenomeSpy example |
| --- | --- | --- |
| `cytobands.json` | [Chromosome ideogram](../gallery/cytobands.md) | [Cytobands](https://genomespy.app/docs/examples/genomic-data/cytobands/) |
| `indexed-fasta-six-frame-translation.json` | [Indexed FASTA six-frame translation](../gallery/six_frame_translation.md) | [Six-frame translation](https://genomespy.app/docs/examples/genomic-data/indexed-fasta-six-frame-translation/) |
| `bam-read-alignments.json` | [BAM read alignments](../gallery/bam_read_alignments.md) | [BAM alignments](https://genomespy.app/docs/examples/genomic-data/bam-read-alignments/) |
| `scored-refSeq-genes.json` | [RefSeq genes with scored labels](../gallery/refseq_scored_genes.md) | [RefSeq genes](https://genomespy.app/docs/examples/genomic-data/refseq-genes/) |

## What to notice

The parent specification supplies the assembly, locus domain, and shared genome
axis. The imported children keep their own dataflows, marks, and vertical
scales while panning and zooming together.

## Python implementation

This is deliberately an import example rather than a reimplementation of its
tracks. `gs.import_view(url=...)` creates each child and `gs.vconcat()` arranges
them vertically. GenomeSpy retrieves and resolves the JSON specifications in
the browser when the visualization is rendered.

See [Import remote view specifications](../user-guide/importing-specifications.md)
for URL handling, version pinning, and reuse considerations. The
[official composed genome browser](https://genomespy.app/docs/examples/genomic-data/genome-browser/)
provides the original composition discussion.
