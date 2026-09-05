# Large and indexed genomic data

A genome-wide signal or alignment file can contain far more rows than a browser
should download at once. GenomeSpy's **lazy data sources** request only the part
needed for the visible genomic region. Zooming or panning changes that region
and causes the source to request another indexed slice.

This is **viewport-driven loading**: the current locus scale domain—the interval
visible on screen—determines which data are loaded. Python constructs the
specification, but the browser performs the requests while the chart is open.
The GenomeSpy documentation covers every source type in
[lazy data sources](https://genomespy.app/docs/grammar/data/lazy/).

## A lazy quantitative signal

BigWig stores dense quantitative signal such as coverage, conservation, or GC
content. {py:meth}`gs.lazy.bigwig(...) <genome_spy.data.LazyNamespace.bigwig>` produces rows with `chrom`, `start`, `end`, and
`score` fields:

```{literalinclude} ../tutorials/genomic_data.py
:language: python
:start-after: genomic-data-bigwig-start
:end-before: genomic-data-bigwig-end
```

```{genomespy-chart} genomic_data:bigwig_chart
:height: 230
:title: BigWig data loaded for the visible hg38 region
```

The source watches the x scale because genomic lazy sources use `channel="x"`
by default. BigWig chooses an appropriate data resolution for the zoom level;
`pixelsPerBin` can tune the approximate minimum bin width when necessary.

## Lazy genomic intervals

BigBed is the indexed counterpart for interval annotations. Its extra fields
depend on how the file was created. This ENCODE file exposes `ucscLabel`, which
the chart uses for color:

```{literalinclude} ../tutorials/genomic_data.py
:language: python
:start-after: genomic-data-bigbed-start
:end-before: genomic-data-bigbed-end
```

```{genomespy-chart} genomic_data:bigbed_chart
:height: 190
:title: BigBed intervals loaded for the visible hg38 region
```

The interval pattern is the same as for inline data: encode the start with `x`
and the end with `x2`. Lazy loading changes where the rows come from, not how
marks and encodings work.

## Choose a source for the file format

Choose the builder that matches the hosted file:

| Format | Builder | Rows provided to the chart |
| --- | --- | --- |
| [BigWig](https://genomespy.app/docs/grammar/data/lazy/#bigwig) | {py:meth}`gs.lazy.bigwig(url) <genome_spy.data.LazyNamespace.bigwig>` | Quantitative genomic intervals |
| [BigBed](https://genomespy.app/docs/grammar/data/lazy/#bigbed) | {py:meth}`gs.lazy.bigbed(url) <genome_spy.data.LazyNamespace.bigbed>` | Annotation intervals |
| [FASTA](https://genomespy.app/docs/grammar/data/lazy/#indexed-fasta) | {py:meth}`gs.lazy.indexed_fasta(url) <genome_spy.data.LazyNamespace.indexed_fasta>` | Sequence chunks |
| [BAM](https://genomespy.app/docs/grammar/data/lazy/#bam) | {py:meth}`gs.lazy.bam(url) <genome_spy.data.LazyNamespace.bam>` | Read alignments |
| [Tabix TSV](https://genomespy.app/docs/grammar/data/lazy/#tabix-tsv) | {py:meth}`gs.lazy.tabix(url) <genome_spy.data.LazyNamespace.tabix>` | Parsed tabular intervals |
| [GFF3](https://genomespy.app/docs/grammar/data/lazy/#gff3) | {py:meth}`gs.lazy.gff3(url) <genome_spy.data.LazyNamespace.gff3>` | Gene and transcript features |
| [VCF](https://genomespy.app/docs/grammar/data/lazy/#vcf) | {py:meth}`gs.lazy.vcf(url) <genome_spy.data.LazyNamespace.vcf>` | Variant records |

Each format links to its section in the GenomeSpy documentation, which lists the
source's parameters and the fields it returns.

The BigWig and BigBed examples above use working public files. For the other
formats, the gallery links below provide complete charts backed by real data.

## The scale controls loading

A lazy source observes the scale resolution of the view where it is declared.
For the usual horizontal genome track, three pieces must agree:

1. the chart has an assembly, such as `assembly="hg38"`;
2. the x encoding has the `locus` type;
3. the source's `channel` is `"x"`, which is the default.

For an unusual vertical genome track, use a locus encoding on y and pass
`channel="y"` to the source. A lazy source cannot choose a genomic window when
the observed channel has no locus scale.

Most sources have a `windowSize` threshold. When the visible region is wider
than that threshold, the source waits for the user to zoom in instead of
returning an impractically large result. BigWig is different: it can summarize
signal at progressively coarser resolutions.

The `debounce`, `debounceDomainChange`, and `debounceMode` options control how
quickly requests follow scale changes. Keep their defaults until a real track
shows excessive requests or noticeable latency. Each source's own defaults are
listed with its parameters in the GenomeSpy documentation.

## Index files and hosting

Indexed FASTA, BAM, Tabix TSV, GFF3, and VCF use companion index files. By
default, GenomeSpy derives conventional names from the data URL:

- FASTA: `.fai`;
- BAM: `.bai`;
- Tabix TSV, GFF3, and VCF: `.tbi`.

Pass `indexUrl=...` when an index is stored elsewhere or uses another name.
BigWig and BigBed contain their indexes internally.

Because the browser makes the requests, both the data and index URLs must be
reachable from it. A server on another origin must allow cross-origin requests
and byte-range access. Test the deployed URL, not only a local Python path.

## Complete track examples

The gallery develops the format-specific transforms and marks without
duplicating them here:

- [indexed FASTA sequence](../gallery/indexed_fasta_sequence.md) flattens each
  returned sequence chunk into individual bases;
- [BAM read alignments](../gallery/bam_read_alignments.md) builds coverage,
  pileup lanes, CIGAR operations, and mismatch marks;
- [GFF3 gene annotations](../gallery/gff3_gene_annotations.md) projects and
  packs hierarchical transcript features;
- [stacked genome browser](../gallery/stacked_genome_browser.md) combines
  several lazy sources on one linked locus scale.

Use eager inline or URL data for a small table that can be downloaded in full.
Use a lazy source when the format has a genomic index and loading should follow
the visible region.
