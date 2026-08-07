"""Helpers for schema-backed GenomeSpy data sources."""

from __future__ import annotations

from collections.abc import Sequence
from typing import Any, cast

from genome_spy.schema import Data, ExprRef, LazyDataParams, UrlTemplate
from genome_spy.schema.lazy import LazyDataMethodMixin

__all__ = ["Data", "LazyNamespace", "lazy"]

_LazyUrl = str | Sequence[str] | ExprRef | dict[str, Any] | UrlTemplate


class LazyNamespace(LazyDataMethodMixin):
    """Convenience builders for GenomeSpy lazy data sources.

    Description:
        These helpers build schema-backed :class:`genome_spy.schema.Data`
        objects with a populated ``lazy`` block so callers can stay within the
        handwritten chart API instead of assembling nested dictionaries by hand.

    Example:
        >>> lazy.bigwig("https://example.test/signal.bw")
        >>> lazy.gff3("https://example.test/genes.gff3.gz", windowSize=2_000_000)
    """

    def source(self, type: str, url: _LazyUrl, /, **kwargs: Any) -> Data:
        """Create a lazy data source of an arbitrary GenomeSpy type.

        Description:
            This is the generic escape hatch for lazy data sources. Named
            helpers such as :meth:`bigwig` and :meth:`gff3` cover each
            schema-defined URL-backed source type.

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


lazy = LazyNamespace()
