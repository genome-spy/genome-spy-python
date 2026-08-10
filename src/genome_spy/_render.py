"""Private render-time preparation for binary dataframe transport."""

from __future__ import annotations

from copy import deepcopy
from dataclasses import dataclass, field
from hashlib import sha256
from typing import Any, Callable, Literal, Protocol

from genome_spy._chart_authoring import normalize_data
from genome_spy.arrow import _try_to_arrow_ipc


@dataclass(frozen=True, slots=True)
class _PreparedSpec:
    """A JSON-ready spec and the binary Arrow payloads it references."""

    spec: dict[str, Any]
    buffers: dict[str, bytes]


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
    context = _RenderContext()
    spec = chart._to_dict(
        include_schema=True,
        validate=True,
        normalize_chart_data=context.normalize_data,
    )
    return _PreparedSpec(spec=spec, buffers=context.buffers)


def prepare_widget(chart: _RenderSerializable) -> _PreparedWidget:
    """Prepare a chart for live named-dataset widget updates."""
    return prepare_widget_spec(prepare_render(chart))


def prepare_widget_spec(prepared: _PreparedSpec) -> _PreparedWidget:
    """Rewrite known eager sources in a prepared spec as named datasets."""
    spec = deepcopy(prepared.spec)
    root_datasets = spec.setdefault("datasets", {})
    if not isinstance(root_datasets, dict):
        raise TypeError("GenomeSpy root datasets must be a mapping.")

    used_names = _declared_dataset_names(spec)
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

    def visit(value: Any, *, owner: str | None, scoped: bool) -> None:
        if isinstance(value, list):
            for item in value:
                visit(item, owner=owner, scoped=scoped)
            return
        if not isinstance(value, dict):
            return

        current_owner = owner
        current_scoped = scoped
        if value is not spec and "datasets" in value:
            current_scoped = True
            name = value.get("name")
            current_owner = name if isinstance(name, str) and name else None

        declared = value.get("datasets")
        if isinstance(declared, dict):
            for name in declared:
                if isinstance(name, str) and name:
                    register(name, owner=current_owner, scoped=current_scoped)

        data = value.get("data")
        if isinstance(data, dict):
            url = data.get("url")
            if isinstance(url, str) and url.startswith("arrow://"):
                token = url.removeprefix("arrow://")
                payload = prepared.buffers.get(token)
                if payload is None:
                    raise ValueError(f"No Arrow IPC payload provided for {token}.")
                name = generated_name(token)
                if name not in root_datasets:
                    root_datasets[name] = []
                    register(
                        name,
                        owner=None,
                        scoped=False,
                        initial_payload=payload,
                        initial_format="arrow",
                    )
                value["data"] = {"name": name}
            elif set(data) == {"values"} and isinstance(data["values"], list):
                name = generated_name(f"records:{len(generated_names)}")
                root_datasets[name] = data["values"]
                register(name, owner=None, scoped=False)
                value["data"] = {"name": name}

        for key, child in value.items():
            if key not in {"data", "datasets"}:
                visit(child, owner=current_owner, scoped=current_scoped)

    visit(spec, owner=None, scoped=False)
    return _PreparedWidget(spec=spec, datasets=tuple(datasets))


def _declared_dataset_names(value: Any) -> set[str]:
    """Return all existing named-dataset keys in a serialized spec."""
    names: set[str] = set()
    if isinstance(value, list):
        for item in value:
            names.update(_declared_dataset_names(item))
    elif isinstance(value, dict):
        datasets = value.get("datasets")
        if isinstance(datasets, dict):
            names.update(name for name in datasets if isinstance(name, str))
        for child in value.values():
            names.update(_declared_dataset_names(child))
    return names
