"""Generated from the GenomeSpy JSON Schema. Do not edit by hand."""

from __future__ import annotations
from collections.abc import Sequence
from typing import Any, cast, Literal

from genome_spy.schema._typing import PrimaryPositionalChannel_T
from genome_spy.schema._kwds import ParseKwds
from genome_spy.schemapi import Undefined, UndefinedType
from genome_spy.schema import core


class LazyDataMethodMixin:
    """Schema-derived named lazy data-source helpers."""

    def bam(
        self,
        url: str | core.ExprRef | dict[str, Any] | core.UrlTemplate,
        /,
        *,
        channel: PrimaryPositionalChannel_T | UndefinedType = Undefined,
        debounce: float | core.ExprRef | dict[str, Any] | UndefinedType = Undefined,
        debounceDomainChange: float
        | core.ExprRef
        | dict[str, Any]
        | UndefinedType = Undefined,
        debounceMode: Literal["domain", "window"] | UndefinedType = Undefined,
        indexUrl: str
        | core.ExprRef
        | dict[str, Any]
        | core.IndexUrlTemplate
        | UndefinedType = Undefined,
        windowSize: float | core.ExprRef | dict[str, Any] | UndefinedType = Undefined,
    ) -> core.Data:
        """Create a lazy ``bam`` data source.

        Args:
            channel (PrimaryPositionalChannel_T): Which channel's scale domain to monitor. __Default value:__ ``"x"``
            debounce (float | ExprRef | dict[str, Any]): Debounce time for data updates, in milliseconds. Debouncing prevents excessive data updates when the user is zooming or panning around. __Default value:__ ``200``
            debounceDomainChange (float | ExprRef | dict[str, Any]): Debounce time for scale-domain driven data updates, in milliseconds. __Default value:__ ``200``
            debounceMode (Literal['domain', 'window']): The debounce mode for data updates. If set to ``"domain"``, domain change events (panning and zooming) will be debounced. If set to ``"window"``, the data fetches initiated by the changes to the visible window (or tile) will be debounced. If your data is small, the ``"window"`` is better as it will start fetching data while the user is still panning around, resulting in a shorter perceived latency. __Default value:__ ``"window"``
            indexUrl (str | ExprRef | dict[str, Any] | IndexUrlTemplate): URL of the index file. When ``url`` is a template, this can be an index URL template using the same placeholder and values. __Default value:__ ``url`` + ``".bai"``.
            windowSize (float | ExprRef | dict[str, Any]): Size of each chunk when fetching the BAM file. Data is only fetched when the length of the visible domain smaller than the window size. __Default value:__ ``10000``
        """
        properties = {
            "channel": channel,
            "debounce": debounce,
            "debounceDomainChange": debounceDomainChange,
            "debounceMode": debounceMode,
            "indexUrl": indexUrl,
            "windowSize": windowSize,
        }
        defined: dict[str, Any] = {
            key: value for key, value in properties.items() if value is not Undefined
        }
        return core.Data(
            lazy=core.LazyDataParams(type=cast(Any, "bam"), url=url, **defined)
        )

    def bigbed(
        self,
        url: str | Sequence[str] | core.ExprRef | dict[str, Any] | core.UrlTemplate,
        /,
        *,
        channel: PrimaryPositionalChannel_T | UndefinedType = Undefined,
        debounce: float | core.ExprRef | dict[str, Any] | UndefinedType = Undefined,
        debounceDomainChange: float
        | core.ExprRef
        | dict[str, Any]
        | UndefinedType = Undefined,
        debounceMode: Literal["domain", "window"] | UndefinedType = Undefined,
        windowSize: float | core.ExprRef | dict[str, Any] | UndefinedType = Undefined,
    ) -> core.Data:
        """Create a lazy ``bigbed`` data source.

        Args:
            channel (PrimaryPositionalChannel_T): Which channel's scale domain to monitor. __Default value:__ ``"x"``
            debounce (float | ExprRef | dict[str, Any]): Debounce time for data updates, in milliseconds. Debouncing prevents excessive data updates when the user is zooming or panning around. __Default value:__ ``200``
            debounceDomainChange (float | ExprRef | dict[str, Any]): Debounce time for scale-domain driven data updates, in milliseconds. __Default value:__ ``200``
            debounceMode (Literal['domain', 'window']): The debounce mode for data updates. If set to ``"domain"``, domain change events (panning and zooming) will be debounced. If set to ``"window"``, the data fetches initiated by the changes to the visible window (or tile) will be debounced. If your data is small, the ``"window"`` is better as it will start fetching data while the user is still panning around, resulting in a shorter perceived latency. __Default value:__ ``"window"``
            windowSize (float | ExprRef | dict[str, Any]): Size of each chunk when fetching the BigBed file. Data is only fetched when the length of the visible domain smaller than the window size. __Default value:__ ``1000000``
        """
        properties = {
            "channel": channel,
            "debounce": debounce,
            "debounceDomainChange": debounceDomainChange,
            "debounceMode": debounceMode,
            "windowSize": windowSize,
        }
        defined: dict[str, Any] = {
            key: value for key, value in properties.items() if value is not Undefined
        }
        return core.Data(
            lazy=core.LazyDataParams(type=cast(Any, "bigbed"), url=url, **defined)
        )

    def bigwig(
        self,
        url: str | Sequence[str] | core.ExprRef | dict[str, Any] | core.UrlTemplate,
        /,
        *,
        channel: PrimaryPositionalChannel_T | UndefinedType = Undefined,
        debounce: float | core.ExprRef | dict[str, Any] | UndefinedType = Undefined,
        debounceDomainChange: float
        | core.ExprRef
        | dict[str, Any]
        | UndefinedType = Undefined,
        debounceMode: Literal["domain", "window"] | UndefinedType = Undefined,
        pixelsPerBin: float | core.ExprRef | dict[str, Any] | UndefinedType = Undefined,
    ) -> core.Data:
        """Create a lazy ``bigwig`` data source.

        Args:
            channel (PrimaryPositionalChannel_T): Which channel's scale domain to monitor. __Default value:__ ``"x"``
            debounce (float | ExprRef | dict[str, Any]): Debounce time for data updates, in milliseconds. Debouncing prevents excessive data updates when the user is zooming or panning around. __Default value:__ ``200``
            debounceDomainChange (float | ExprRef | dict[str, Any]): Debounce time for scale-domain driven data updates, in milliseconds. __Default value:__ ``200``
            debounceMode (Literal['domain', 'window']): The debounce mode for data updates. If set to ``"domain"``, domain change events (panning and zooming) will be debounced. If set to ``"window"``, the data fetches initiated by the changes to the visible window (or tile) will be debounced. If your data is small, the ``"window"`` is better as it will start fetching data while the user is still panning around, resulting in a shorter perceived latency. __Default value:__ ``"window"``
            pixelsPerBin (float | ExprRef | dict[str, Any]): The approximate minimum width of each data bin, in pixels. __Default value:__ ``2``
        """
        properties = {
            "channel": channel,
            "debounce": debounce,
            "debounceDomainChange": debounceDomainChange,
            "debounceMode": debounceMode,
            "pixelsPerBin": pixelsPerBin,
        }
        defined: dict[str, Any] = {
            key: value for key, value in properties.items() if value is not Undefined
        }
        return core.Data(
            lazy=core.LazyDataParams(type=cast(Any, "bigwig"), url=url, **defined)
        )

    def gff3(
        self,
        url: str | Sequence[str] | core.ExprRef | dict[str, Any] | core.UrlTemplate,
        /,
        *,
        addChrPrefix: bool | str | UndefinedType = Undefined,
        channel: PrimaryPositionalChannel_T | UndefinedType = Undefined,
        debounce: float | core.ExprRef | dict[str, Any] | UndefinedType = Undefined,
        debounceDomainChange: float
        | core.ExprRef
        | dict[str, Any]
        | UndefinedType = Undefined,
        debounceMode: Literal["domain", "window"] | UndefinedType = Undefined,
        indexUrl: str
        | core.ExprRef
        | dict[str, Any]
        | core.IndexUrlTemplate
        | UndefinedType = Undefined,
        windowSize: float | UndefinedType = Undefined,
    ) -> core.Data:
        """Create a lazy ``gff3`` data source.

        Args:
            addChrPrefix (bool | str): Add a ``chr`` (boolean) or custom (string) prefix to the chromosome names in the Tabix file. __Default value:__ ``false``
            channel (PrimaryPositionalChannel_T): Which channel's scale domain to monitor. __Default value:__ ``"x"``
            debounce (float | ExprRef | dict[str, Any]): Debounce time for data updates, in milliseconds. Debouncing prevents excessive data updates when the user is zooming or panning around. __Default value:__ ``200``
            debounceDomainChange (float | ExprRef | dict[str, Any]): Debounce time for scale-domain driven data updates, in milliseconds. __Default value:__ ``200``
            debounceMode (Literal['domain', 'window']): The debounce mode for data updates. If set to ``"domain"``, domain change events (panning and zooming) will be debounced. If set to ``"window"``, the data fetches initiated by the changes to the visible window (or tile) will be debounced. If your data is small, the ``"window"`` is better as it will start fetching data while the user is still panning around, resulting in a shorter perceived latency. __Default value:__ ``"window"``
            indexUrl (str | ExprRef | dict[str, Any] | IndexUrlTemplate): URL of the tabix index file. When ``url`` is a template, this can be an index URL template using the same placeholder and values. __Default value:__ ``url`` + ``".tbi"``.
            windowSize (float): Size of each chunk when fetching the Tabix file. Data is only fetched when the length of the visible domain smaller than the window size. __Default value:__ ``30000000``
        """
        properties = {
            "addChrPrefix": addChrPrefix,
            "channel": channel,
            "debounce": debounce,
            "debounceDomainChange": debounceDomainChange,
            "debounceMode": debounceMode,
            "indexUrl": indexUrl,
            "windowSize": windowSize,
        }
        defined: dict[str, Any] = {
            key: value for key, value in properties.items() if value is not Undefined
        }
        return core.Data(
            lazy=core.LazyDataParams(type=cast(Any, "gff3"), url=url, **defined)
        )

    def indexed_fasta(
        self,
        url: str | core.ExprRef | dict[str, Any] | core.UrlTemplate,
        /,
        *,
        channel: PrimaryPositionalChannel_T | UndefinedType = Undefined,
        debounce: float | core.ExprRef | dict[str, Any] | UndefinedType = Undefined,
        debounceDomainChange: float
        | core.ExprRef
        | dict[str, Any]
        | UndefinedType = Undefined,
        debounceMode: Literal["domain", "window"] | UndefinedType = Undefined,
        indexUrl: str
        | core.ExprRef
        | dict[str, Any]
        | core.IndexUrlTemplate
        | UndefinedType = Undefined,
        windowSize: float | UndefinedType = Undefined,
    ) -> core.Data:
        """Create a lazy ``indexedFasta`` data source.

        Args:
            channel (PrimaryPositionalChannel_T): Which channel's scale domain to monitor. __Default value:__ ``"x"``
            debounce (float | ExprRef | dict[str, Any]): Debounce time for data updates, in milliseconds. Debouncing prevents excessive data updates when the user is zooming or panning around. __Default value:__ ``200``
            debounceDomainChange (float | ExprRef | dict[str, Any]): Debounce time for scale-domain driven data updates, in milliseconds. __Default value:__ ``200``
            debounceMode (Literal['domain', 'window']): The debounce mode for data updates. If set to ``"domain"``, domain change events (panning and zooming) will be debounced. If set to ``"window"``, the data fetches initiated by the changes to the visible window (or tile) will be debounced. If your data is small, the ``"window"`` is better as it will start fetching data while the user is still panning around, resulting in a shorter perceived latency. __Default value:__ ``"window"``
            indexUrl (str | ExprRef | dict[str, Any] | IndexUrlTemplate): URL of the index file. When ``url`` is a template, this can be an index URL template using the same placeholder and values. __Default value:__ ``url`` + ``".fai"``.
            windowSize (float): Size of each chunk when fetching the fasta file. Data is only fetched when the length of the visible domain smaller than the window size. __Default value:__ ``7000``
        """
        properties = {
            "channel": channel,
            "debounce": debounce,
            "debounceDomainChange": debounceDomainChange,
            "debounceMode": debounceMode,
            "indexUrl": indexUrl,
            "windowSize": windowSize,
        }
        defined: dict[str, Any] = {
            key: value for key, value in properties.items() if value is not Undefined
        }
        return core.Data(
            lazy=core.LazyDataParams(type=cast(Any, "indexedFasta"), url=url, **defined)
        )

    def tabix(
        self,
        url: str | Sequence[str] | core.ExprRef | dict[str, Any] | core.UrlTemplate,
        /,
        *,
        addChrPrefix: bool | str | UndefinedType = Undefined,
        channel: PrimaryPositionalChannel_T | UndefinedType = Undefined,
        columns: Sequence[str] | UndefinedType = Undefined,
        debounce: float | core.ExprRef | dict[str, Any] | UndefinedType = Undefined,
        debounceDomainChange: float
        | core.ExprRef
        | dict[str, Any]
        | UndefinedType = Undefined,
        debounceMode: Literal["domain", "window"] | UndefinedType = Undefined,
        indexUrl: str
        | core.ExprRef
        | dict[str, Any]
        | core.IndexUrlTemplate
        | UndefinedType = Undefined,
        parse: core.Parse | ParseKwds | None | UndefinedType = Undefined,
        windowSize: float | UndefinedType = Undefined,
    ) -> core.Data:
        """Create a lazy ``tabix`` data source.

        Args:
            addChrPrefix (bool | str): Add a ``chr`` (boolean) or custom (string) prefix to the chromosome names in the Tabix file. __Default value:__ ``false``
            channel (PrimaryPositionalChannel_T): Which channel's scale domain to monitor. __Default value:__ ``"x"``
            columns (Sequence[str]): Ordered list of field names for headerless tabix TSV input. If omitted, the source tries to read a commented header line from the tabix file header or the first row of a plain TSV header.
            debounce (float | ExprRef | dict[str, Any]): Debounce time for data updates, in milliseconds. Debouncing prevents excessive data updates when the user is zooming or panning around. __Default value:__ ``200``
            debounceDomainChange (float | ExprRef | dict[str, Any]): Debounce time for scale-domain driven data updates, in milliseconds. __Default value:__ ``200``
            debounceMode (Literal['domain', 'window']): The debounce mode for data updates. If set to ``"domain"``, domain change events (panning and zooming) will be debounced. If set to ``"window"``, the data fetches initiated by the changes to the visible window (or tile) will be debounced. If your data is small, the ``"window"`` is better as it will start fetching data while the user is still panning around, resulting in a shorter perceived latency. __Default value:__ ``"window"``
            indexUrl (str | ExprRef | dict[str, Any] | IndexUrlTemplate): URL of the tabix index file. When ``url`` is a template, this can be an index URL template using the same placeholder and values. __Default value:__ ``url`` + ``".tbi"``.
            parse (Parse | ParseKwds | None): Optional type parsing for TSV fields. When omitted, field types are inferred automatically. Set to ``null`` to disable spec-based type inference and rely on data inference, or provide a field-to-type map to override selected columns. __Default value:__ ``"auto"``
            windowSize (float): Size of each chunk when fetching the Tabix file. Data is only fetched when the length of the visible domain smaller than the window size. __Default value:__ ``30000000``
        """
        properties = {
            "addChrPrefix": addChrPrefix,
            "channel": channel,
            "columns": columns,
            "debounce": debounce,
            "debounceDomainChange": debounceDomainChange,
            "debounceMode": debounceMode,
            "indexUrl": indexUrl,
            "parse": parse,
            "windowSize": windowSize,
        }
        defined: dict[str, Any] = {
            key: value for key, value in properties.items() if value is not Undefined
        }
        return core.Data(
            lazy=core.LazyDataParams(type=cast(Any, "tabix"), url=url, **defined)
        )

    def vcf(
        self,
        url: str | Sequence[str] | core.ExprRef | dict[str, Any] | core.UrlTemplate,
        /,
        *,
        addChrPrefix: bool | str | UndefinedType = Undefined,
        channel: PrimaryPositionalChannel_T | UndefinedType = Undefined,
        debounce: float | core.ExprRef | dict[str, Any] | UndefinedType = Undefined,
        debounceDomainChange: float
        | core.ExprRef
        | dict[str, Any]
        | UndefinedType = Undefined,
        debounceMode: Literal["domain", "window"] | UndefinedType = Undefined,
        indexUrl: str
        | core.ExprRef
        | dict[str, Any]
        | core.IndexUrlTemplate
        | UndefinedType = Undefined,
        windowSize: float | UndefinedType = Undefined,
    ) -> core.Data:
        """Create a lazy ``vcf`` data source.

        Args:
            addChrPrefix (bool | str): Add a ``chr`` (boolean) or custom (string) prefix to the chromosome names in the Tabix file. __Default value:__ ``false``
            channel (PrimaryPositionalChannel_T): Which channel's scale domain to monitor. __Default value:__ ``"x"``
            debounce (float | ExprRef | dict[str, Any]): Debounce time for data updates, in milliseconds. Debouncing prevents excessive data updates when the user is zooming or panning around. __Default value:__ ``200``
            debounceDomainChange (float | ExprRef | dict[str, Any]): Debounce time for scale-domain driven data updates, in milliseconds. __Default value:__ ``200``
            debounceMode (Literal['domain', 'window']): The debounce mode for data updates. If set to ``"domain"``, domain change events (panning and zooming) will be debounced. If set to ``"window"``, the data fetches initiated by the changes to the visible window (or tile) will be debounced. If your data is small, the ``"window"`` is better as it will start fetching data while the user is still panning around, resulting in a shorter perceived latency. __Default value:__ ``"window"``
            indexUrl (str | ExprRef | dict[str, Any] | IndexUrlTemplate): URL of the tabix index file. When ``url`` is a template, this can be an index URL template using the same placeholder and values. __Default value:__ ``url`` + ``".tbi"``.
            windowSize (float): Size of each chunk when fetching the Tabix file. Data is only fetched when the length of the visible domain smaller than the window size. __Default value:__ ``30000000``
        """
        properties = {
            "addChrPrefix": addChrPrefix,
            "channel": channel,
            "debounce": debounce,
            "debounceDomainChange": debounceDomainChange,
            "debounceMode": debounceMode,
            "indexUrl": indexUrl,
            "windowSize": windowSize,
        }
        defined: dict[str, Any] = {
            key: value for key, value in properties.items() if value is not Undefined
        }
        return core.Data(
            lazy=core.LazyDataParams(type=cast(Any, "vcf"), url=url, **defined)
        )


__all__ = ["LazyDataMethodMixin"]
