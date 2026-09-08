"""Private render-time preparation for binary dataframe transport."""

from __future__ import annotations

from copy import deepcopy
from dataclasses import dataclass, field
from hashlib import sha256
from typing import Any, Callable, Literal, Protocol

from genome_spy._chart_authoring import normalize_data
from genome_spy.arrow import _try_to_arrow_ipc
from genome_spy.data_transformers import (
    _consolidate,
    _data_slots,
    _DatasetConsolidation,
    data_transformers,
)
from genome_spy.schema import Root


@dataclass(frozen=True, slots=True)
class _PreparedSpec:
    """A JSON-ready spec and the binary Arrow payloads it references."""

    spec: dict[str, Any]
    buffers: dict[str, bytes]
    consolidate_datasets: bool | None = None


_DatasetFormat = Literal["arrow", "records"]


@dataclass(frozen=True, slots=True)
class _LiveDataset:
    """One named dataset synchronized by a live notebook widget."""

    name: str
    owner: str | None
    scoped: bool
    initial_payload: bytes | None
    initial_format: _DatasetFormat | None


@dataclass(frozen=True, slots=True)
class _PreparedWidget:
    """A runtime spec and its live named-dataset declarations."""

    spec: dict[str, Any]
    datasets: tuple[_LiveDataset, ...]


class _RenderSerializable(Protocol):
    """Structural type for charts using the shared serialization traversal."""

    def _to_dict(
        self,
        *,
        include_schema: bool,
        validate: bool,
        normalize_chart_data: Callable[[Any], Any],
    ) -> dict[str, Any]: ...


@dataclass(slots=True)
class _RenderContext:
    """State shared by one render-preparation traversal."""

    buffers: dict[str, bytes] = field(default_factory=dict)
    _table_cache: dict[int, tuple[Any, dict[str, Any]]] = field(default_factory=dict)

    def normalize_data(self, data: Any) -> Any:
        """Return JSON data or a content-addressed Arrow data source."""
        cached = self._table_cache.get(id(data))
        if cached is not None and cached[0] is data:
            return dict(cached[1])

        payload = _try_to_arrow_ipc(data)
        if payload is None:
            return normalize_data(data)

        identifier = sha256(payload).hexdigest()
        self.buffers.setdefault(identifier, payload)
        normalized = {"url": f"arrow://{identifier}", "format": {"type": "arrow"}}
        self._table_cache[id(data)] = (data, normalized)
        return dict(normalized)


def prepare_render(chart: _RenderSerializable) -> _PreparedSpec:
    """Prepare one chart through its shared render-time serialization path."""
    enabled = data_transformers.consolidate_datasets
    context = _RenderContext()
    collector = _DatasetConsolidation(chart) if enabled else None
    spec = chart._to_dict(
        include_schema=True,
        validate=False,
        normalize_chart_data=(
            (lambda data: collector.source(context.normalize_data(data)))
            if collector is not None
            else context.normalize_data
        ),
    )
    if collector is not None:
        collector.finish(spec)
    return _PreparedSpec(
        spec=Root(**spec).to_dict(),
        buffers=context.buffers,
        consolidate_datasets=enabled,
    )


def prepare_widget(chart: _RenderSerializable) -> _PreparedWidget:
    """Prepare a chart for live named-dataset widget updates."""
    return prepare_widget_spec(prepare_render(chart))


def prepare_widget_spec(prepared: _PreparedSpec) -> _PreparedWidget:
    """Rewrite known eager sources in a prepared spec as named datasets."""
    spec = deepcopy(prepared.spec)
    enabled = prepared.consolidate_datasets
    if enabled is None:
        enabled = data_transformers.consolidate_datasets
    if enabled:
        _consolidate(spec)
    root_datasets = spec.setdefault("datasets", {})
    if not isinstance(root_datasets, dict):
        raise TypeError("GenomeSpy root datasets must be a mapping.")

    slots = [
        (kind, dict(value) if kind == "datasets" else value, owner, scoped)
        for kind, value, owner, scoped in _data_slots(spec)
    ]
    used_names: set[str] = set()
    for kind, value, _, _ in slots:
        if kind == "datasets":
            used_names.update(value)
        elif isinstance(value.get("name"), str):
            used_names.add(value["name"])
    generated_names: dict[str, str] = {}
    datasets: list[_LiveDataset] = []

    def register(
        name: str,
        *,
        owner: str | None,
        scoped: bool,
        initial_payload: bytes | None = None,
        initial_format: _DatasetFormat | None = None,
    ) -> None:
        datasets.append(
            _LiveDataset(
                name=name,
                owner=owner,
                scoped=scoped,
                initial_payload=initial_payload,
                initial_format=initial_format,
            )
        )

    def generated_name(token: str) -> str:
        existing = generated_names.get(token)
        if existing is not None:
            return existing
        index = len(generated_names)
        candidate = f"__genome_spy_python_data_{index}"
        while candidate in used_names:
            index += 1
            candidate = f"__genome_spy_python_data_{index}"
        used_names.add(candidate)
        generated_names[token] = candidate
        return candidate

    for kind, data, owner, scoped in slots:
        if kind == "datasets":
            for name in data:
                if isinstance(name, str) and name:
                    register(name, owner=owner, scoped=scoped)
        else:
            url = data.get("url")
            if isinstance(url, str) and url.startswith("arrow://"):
                token = url.removeprefix("arrow://")
                payload = prepared.buffers.get(token)
                if payload is None:
                    raise ValueError(f"No Arrow IPC payload provided for {token}.")
                name = generated_name(
                    token if enabled else f"{token}:{len(generated_names)}"
                )
                if name not in root_datasets:
                    root_datasets[name] = []
                    register(
                        name,
                        owner=None,
                        scoped=False,
                        initial_payload=payload,
                        initial_format="arrow",
                    )
                data.clear()
                data["name"] = name
            elif set(data) == {"values"} and isinstance(data["values"], list):
                name = generated_name(f"records:{len(generated_names)}")
                root_datasets[name] = data["values"]
                register(name, owner=None, scoped=False)
                data.clear()
                data["name"] = name
    return _PreparedWidget(spec=spec, datasets=tuple(datasets))
