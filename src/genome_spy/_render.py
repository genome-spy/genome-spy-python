"""Private render-time preparation for binary dataframe transport."""

from __future__ import annotations

from dataclasses import dataclass, field
from hashlib import sha256
from typing import Any, Callable, Protocol

from genome_spy._chart_authoring import normalize_data
from genome_spy.arrow import _try_to_arrow_ipc


@dataclass(frozen=True, slots=True)
class _PreparedSpec:
    """A JSON-ready spec and the binary Arrow payloads it references."""

    spec: dict[str, Any]
    buffers: dict[str, bytes]


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
