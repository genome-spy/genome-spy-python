"""Helpers for schema-backed GenomeSpy data sources."""

from __future__ import annotations

from typing import Any, cast

from genome_spy.schema import Data, LazyDataParams

__all__ = ["Data", "LazyNamespace", "lazy"]


class LazyNamespace:
    """Convenience builders for GenomeSpy lazy data sources.

    Description:
        These helpers build schema-backed :class:`genome_spy.schema.Data`
        objects with a populated ``lazy`` block so callers can stay within the
        handwritten chart API instead of assembling nested dictionaries by hand.

    Example:
        >>> lazy.bigwig("https://example.test/signal.bw")
        >>> lazy.gff3("https://example.test/genes.gff3.gz", windowSize=2_000_000)
    """

    def source(self, type: str, url: str, /, **kwargs: Any) -> Data:
        """Create a lazy data source of an arbitrary GenomeSpy type.

        Description:
            This is the generic escape hatch for lazy data sources. Named
            helpers such as :meth:`bigwig` and :meth:`gff3` delegate here.

        Args:
            type: GenomeSpy lazy source type such as ``"bigwig"`` or
                ``"gff3"``.
            url: Remote data URL.
            **kwargs: Additional lazy-source parameters supported by GenomeSpy.

        Returns:
            A schema-backed :class:`genome_spy.schema.Data` object.

        Raises:
            No exceptions are raised directly here.

        Example:
            >>> lazy.source("bigwig", "https://example.test/signal.bw")
        """

        return Data(lazy=LazyDataParams(type=cast(Any, type), url=url, **kwargs))

    def bam(self, url: str, /, **kwargs: Any) -> Data:
        """Create a lazy BAM data source.

        Description:
            Builds a schema-backed lazy BAM source for alignment tracks.

        Args:
            url: Remote BAM URL.
            **kwargs: Additional lazy-source parameters.

        Returns:
            A schema-backed :class:`genome_spy.schema.Data` object.

        Raises:
            No exceptions are raised directly here.

        Example:
            >>> lazy.bam("https://example.test/sample.bam")
        """

        return self.source("bam", url, **kwargs)

    def bigbed(self, url: str, /, **kwargs: Any) -> Data:
        """Create a lazy BigBed data source.

        Description:
            Builds a schema-backed lazy BigBed source for interval annotations.

        Args:
            url: Remote BigBed URL.
            **kwargs: Additional lazy-source parameters.

        Returns:
            A schema-backed :class:`genome_spy.schema.Data` object.

        Raises:
            No exceptions are raised directly here.

        Example:
            >>> lazy.bigbed("https://example.test/annotations.bb")
        """

        return self.source("bigbed", url, **kwargs)

    def bigwig(self, url: str, /, **kwargs: Any) -> Data:
        """Create a lazy BigWig data source.

        Description:
            Builds a schema-backed lazy BigWig source for genomic signal tracks.

        Args:
            url: Remote BigWig URL.
            **kwargs: Additional lazy-source parameters such as
                ``pixelsPerBin``.

        Returns:
            A schema-backed :class:`genome_spy.schema.Data` object.

        Raises:
            No exceptions are raised directly here.

        Example:
            >>> lazy.bigwig("https://example.test/signal.bw", pixelsPerBin=1)
        """

        return self.source("bigwig", url, **kwargs)

    def gff3(self, url: str, /, **kwargs: Any) -> Data:
        """Create a lazy GFF3 data source.

        Description:
            Builds a schema-backed lazy GFF3 source for gene-annotation tracks.

        Args:
            url: Remote GFF3 URL.
            **kwargs: Additional lazy-source parameters such as
                ``windowSize``.

        Returns:
            A schema-backed :class:`genome_spy.schema.Data` object.

        Raises:
            No exceptions are raised directly here.

        Example:
            >>> lazy.gff3("https://example.test/genes.gff3.gz", windowSize=2_000_000)
        """

        return self.source("gff3", url, **kwargs)

    def indexed_fasta(self, url: str, /, **kwargs: Any) -> Data:
        """Create a lazy indexed FASTA data source.

        Description:
            Builds a schema-backed lazy indexed FASTA source for sequence
            tracks.

        Args:
            url: Remote indexed FASTA URL.
            **kwargs: Additional lazy-source parameters.

        Returns:
            A schema-backed :class:`genome_spy.schema.Data` object.

        Raises:
            No exceptions are raised directly here.

        Example:
            >>> lazy.indexed_fasta("https://example.test/reference.fa.gz")
        """

        return self.source("indexedFasta", url, **kwargs)

    def vcf(self, url: str, /, **kwargs: Any) -> Data:
        """Create a lazy VCF data source.

        Description:
            Builds a schema-backed lazy VCF source for variant tracks.

        Args:
            url: Remote VCF URL.
            **kwargs: Additional lazy-source parameters.

        Returns:
            A schema-backed :class:`genome_spy.schema.Data` object.

        Raises:
            No exceptions are raised directly here.

        Example:
            >>> lazy.vcf("https://example.test/variants.vcf.gz")
        """

        return self.source("vcf", url, **kwargs)


lazy = LazyNamespace()
