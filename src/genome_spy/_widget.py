"""Anywidget-backed notebook renderer for GenomeSpy charts."""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from pathlib import Path
from typing import Any, Literal, cast

import anywidget
import traitlets

from genome_spy._chart_authoring import json_safe, records_from_data
from genome_spy._render import _PreparedSpec, prepare_widget_spec
from genome_spy.arrow import to_arrow_ipc
from genome_spy.chart import DEFAULT_EMBED_URL

_ESM_PATH = Path(__file__).with_name("static") / "widget.js"
_DatasetFormat = Literal["arrow", "records"]


class JupyterChart(anywidget.AnyWidget):
    """A lightweight anywidget wrapper around GenomeSpy's ``embed`` API."""

    _esm = _ESM_PATH

    spec = traitlets.Dict().tag(sync=True)
    bundle_url = traitlets.Unicode(DEFAULT_EMBED_URL).tag(sync=True)
    embed_options = traitlets.Dict(default_value={}).tag(sync=True)
    dataset_manifest = traitlets.List(trait=traitlets.Dict(), default_value=[]).tag(
        sync=True
    )
    parameter_names = traitlets.List(trait=traitlets.Unicode(), default_value=[]).tag(
        sync=True
    )
    parameter_values = traitlets.Dict(default_value={}).tag(sync=True)
    enable_click_events = traitlets.Bool(False).tag(sync=True)
    clicked_datum = traitlets.Dict(default_value={}).tag(sync=True)
    click_revision = traitlets.Int(0).tag(sync=True)
    error = traitlets.Unicode("").tag(sync=True)

    def __init__(
        self,
        chart: Any,
        *,
        bundle_url: str = DEFAULT_EMBED_URL,
        embed_options: dict[str, Any] | None = None,
        parameter_names: Sequence[str] = (),
        parameter_values: Mapping[str, Any] | None = None,
        enable_click_events: bool = False,
        **kwargs: Any,
    ) -> None:
        if hasattr(chart, "_prepare_widget"):
            prepared = chart._prepare_widget()
        else:
            prepared = prepare_widget_spec(_PreparedSpec(spec=dict(chart), buffers={}))

        manifest: list[dict[str, Any]] = []
        for index, dataset in enumerate(prepared.datasets):
            prefix = f"_dataset_{index}"
            manifest.append(
                {
                    "name": dataset.name,
                    "owner": dataset.owner,
                    "scoped": dataset.scoped,
                    "payload_trait": f"{prefix}_payload",
                    "format_trait": f"{prefix}_format",
                    "revision_trait": f"{prefix}_revision",
                    "initial_payload": dataset.initial_payload,
                    "initial_format": dataset.initial_format,
                }
            )

        super().__init__(
            spec=prepared.spec,
            bundle_url=bundle_url,
            embed_options=embed_options or {},
            dataset_manifest=[self._manifest_entry(entry) for entry in manifest],
            parameter_names=list(parameter_names),
            parameter_values=dict(parameter_values or {}),
            enable_click_events=enable_click_events,
            **kwargs,
        )

        for entry in manifest:
            initial_payload = entry["initial_payload"]
            initial_format = entry["initial_format"] or "records"
            self.add_traits(
                **{
                    entry["payload_trait"]: traitlets.Any(initial_payload).tag(
                        sync=True
                    ),
                    entry["format_trait"]: traitlets.Unicode(initial_format).tag(
                        sync=True
                    ),
                    entry["revision_trait"]: traitlets.Int(
                        1 if initial_payload is not None else 0
                    ).tag(sync=True),
                }
            )

    @property
    def dataset_names(self) -> tuple[str, ...]:
        """Return live dataset names in declaration order.

        Description:
            Names are taken from the widget's fixed runtime dataset manifest.
            Repeated names indicate scoped declarations and require a unique
            name before they can be addressed through :meth:`set_dataset`.

        Returns:
            Dataset names in declaration order.

        Raises:
            No exceptions are raised directly here.

        Example:
            >>> chart.widget().dataset_names
            ('table',)
        """
        return tuple(str(entry["name"]) for entry in self.dataset_manifest)

    def set_dataset(
        self,
        name: str,
        data: object,
        *,
        format: _DatasetFormat = "arrow",
    ) -> None:
        """Replace one declared live dataset without recreating GenomeSpy.

        Description:
            Arrow is the default and transfers supported dataframe/table inputs
            as a binary AnyWidget buffer. Use ``format="records"`` only for
            ordinary JSON-compatible record lists.

        Args:
            name: Declared dataset name.
            data: Table or records used as the replacement value.
            format: Transport format, either ``"arrow"`` or ``"records"``.

        Returns:
            ``None`` after the synchronized transport state has been updated.

        Raises:
            KeyError: If no declared dataset has ``name``.
            ValueError: If ``name`` is ambiguous or cannot be addressed.
            TypeError: If ``data`` cannot be serialized using ``format``.

        Example:
            >>> view.set_dataset('table', dataframe)
        """
        entry = self._dataset_entry(name)
        payload = self._serialize_dataset(data, format)
        revision_trait = cast(str, entry["revision_trait"])
        with self.hold_sync():
            setattr(self, cast(str, entry["payload_trait"]), payload)
            setattr(self, cast(str, entry["format_trait"]), format)
            setattr(self, revision_trait, getattr(self, revision_trait) + 1)

    def set_data(
        self,
        data: object,
        *,
        format: _DatasetFormat = "arrow",
    ) -> None:
        """Replace the only declared live dataset.

        Description:
            This is a convenience alias for :meth:`set_dataset` when the widget
            has exactly one live dataset.

        Args:
            data: Table or records used as the replacement value.
            format: Transport format, either ``"arrow"`` or ``"records"``.

        Returns:
            ``None`` after the synchronized transport state has been updated.

        Raises:
            ValueError: If the widget has zero or multiple live datasets.
            TypeError: If ``data`` cannot be serialized using ``format``.

        Example:
            >>> view.set_data(dataframe)
        """
        if len(self.dataset_manifest) != 1:
            names = ", ".join(self.dataset_names) or "none"
            raise ValueError(
                "set_data() requires exactly one live dataset; "
                f"available datasets: {names}."
            )
        self.set_dataset(str(self.dataset_manifest[0]["name"]), data, format=format)

    def _dataset_entry(self, name: str) -> dict[str, Any]:
        """Return the unambiguous manifest entry for a public dataset name."""
        matches = [entry for entry in self.dataset_manifest if entry["name"] == name]
        if not matches:
            available = ", ".join(self.dataset_names) or "none"
            raise KeyError(
                f"Unknown dataset {name!r}. Available datasets: {available}."
            )
        if len(matches) != 1:
            raise ValueError(
                f"Dataset {name!r} is declared in multiple scopes and cannot be "
                "addressed by name alone."
            )
        entry = dict(matches[0])
        if entry["scoped"] and entry["owner"] is None:
            raise ValueError(
                f"Dataset {name!r} is declared in an unnamed nested view. "
                "Give its owner view a unique name before updating it."
            )
        return entry

    @staticmethod
    def _manifest_entry(entry: Mapping[str, Any]) -> dict[str, Any]:
        """Return synchronized metadata without Python-only initial values."""
        return {
            key: value
            for key, value in entry.items()
            if key not in {"initial_payload", "initial_format"}
        }

    @staticmethod
    def _serialize_dataset(data: object, format: _DatasetFormat) -> bytes | list[Any]:
        """Serialize one dataset before mutating synchronized trait state."""
        if format == "arrow":
            return to_arrow_ipc(data)
        if format == "records":
            records = records_from_data(data)
            if records is None:
                raise TypeError(
                    "Record transport requires a list of records or a supported "
                    "table with record conversion."
                )
            return cast(list[Any], json_safe(records))
        raise ValueError(f"Unsupported dataset format {format!r}.")
