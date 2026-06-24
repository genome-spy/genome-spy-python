"""A compact but growing Chart API for GenomeSpy core specifications."""

from __future__ import annotations

from dataclasses import dataclass, field, replace
from pathlib import Path
from typing import Any
from uuid import uuid4

from genome_spy._utils import compact_json, is_mapping, pretty_json
from genome_spy.channels import Channel, channel

DEFAULT_SCHEMA_URL = "https://cdn.jsdelivr.net/npm/@genome-spy/core/dist/schema.json"
DEFAULT_EMBED_URL = (
    "https://cdn.jsdelivr.net/npm/@genome-spy/core/dist/bundle/index.es.js"
)
MARK_TYPES = ("point", "rect", "rule", "tick", "text", "link")

HTML_TEMPLATE = """
<div id="{container_id}"></div>
<script type="text/javascript">
  (function(spec, moduleUrl) {{
    let outputDiv = document.currentScript.previousElementSibling;
    if (!outputDiv || outputDiv.id !== "{container_id}") {{
      outputDiv = document.getElementById("{container_id}");
    }}

    function showError(error) {{
      outputDiv.innerHTML = (
        '<div style="color:red;">'
        + '<p>JavaScript Error: ' + error.message + '</p>'
        + '<p>GenomeSpy failed to render in this notebook frontend. '
        + 'See the browser console for details.</p>'
        + '</div>'
      );
      throw error;
    }}

    (async function() {{
      try {{
        const module = await import(moduleUrl);
        const embed = module.embed ?? module.default?.embed ?? module.default;
        if (typeof embed !== "function") {{
          throw new Error("GenomeSpy embed export was not found.");
        }}
        await embed(outputDiv, spec);
      }} catch (error) {{
        showError(error);
      }}
    }})();
  }})({spec_json}, {module_url_json});
</script>
""".strip()


def _normalize_data(data: Any) -> Any:
    if data is None:
        return None
    if isinstance(data, list):
        return {"values": data}
    if is_mapping(data):
        return dict(data)
    raise TypeError(f"Unsupported data value: {type(data)!r}")


def _normalize_channel(value: Channel | str | dict[str, Any]) -> dict[str, Any]:
    return channel(value).to_dict()


def _normalize_transform(transform: dict[str, Any]) -> dict[str, Any]:
    if not is_mapping(transform):
        raise TypeError(f"Unsupported transform value: {type(transform)!r}")
    return dict(transform)


@dataclass(frozen=True, slots=True)
class TopLevelSpec:
    """Base class for top-level GenomeSpy specifications."""

    properties_map: dict[str, Any] = field(default_factory=dict)
    transform: list[dict[str, Any]] = field(default_factory=list)
    schema_url: str = DEFAULT_SCHEMA_URL

    def properties(self, **kwargs: Any) -> TopLevelSpec:
        """Return a new spec with merged top-level properties."""
        merged = dict(self.properties_map)
        merged.update(kwargs)
        return replace(self, properties_map=merged)

    def transform_filter(self, expression: str) -> TopLevelSpec:
        """Add a filter transform using a GenomeSpy expression string."""
        return self._append_transform({"type": "filter", "expr": expression})

    def transform_formula(self, *, expr: str, as_: str) -> TopLevelSpec:
        """Add a formula transform."""
        return self._append_transform({"type": "formula", "expr": expr, "as": as_})

    def to_dict(self, *, include_schema: bool = True) -> dict[str, Any]:
        """Serialize the spec to a JSON-compatible dictionary."""
        spec: dict[str, Any] = {}
        if include_schema:
            spec["$schema"] = self.schema_url
        spec.update(self.properties_map)
        if self.transform:
            spec["transform"] = [dict(item) for item in self.transform]
        spec.update(self._body_dict())
        return spec

    def to_json(self, *, include_schema: bool = True) -> str:
        """Serialize the spec to formatted JSON."""
        return pretty_json(self.to_dict(include_schema=include_schema))

    def to_html(
        self,
        *,
        bundle_url: str = DEFAULT_EMBED_URL,
        container_id: str | None = None,
    ) -> str:
        """Render the spec as a small self-contained HTML snippet."""
        container_id = container_id or f"genome-spy-{uuid4().hex}"
        spec_json = compact_json(self.to_dict())
        module_url_json = compact_json(bundle_url)
        return HTML_TEMPLATE.format(
            container_id=container_id,
            spec_json=spec_json,
            module_url_json=module_url_json,
        )

    def save(self, path: str | Path, *, format: str | None = None) -> None:
        """Save the spec as JSON or HTML based on suffix or explicit format."""
        output_path = Path(path)
        file_format = format or output_path.suffix.lstrip(".")
        if file_format == "json":
            output_path.write_text(self.to_json() + "\n", encoding="utf-8")
            return
        if file_format == "html":
            output_path.write_text(self.to_html() + "\n", encoding="utf-8")
            return
        raise ValueError("Unsupported format. Use 'json' or 'html'.")

    def widget(
        self,
        *,
        bundle_url: str = DEFAULT_EMBED_URL,
        embed_options: dict[str, Any] | None = None,
    ) -> Any:
        """Create a notebook widget for the spec."""
        from genome_spy.jupyter import JupyterChart

        return JupyterChart(
            self,
            bundle_url=bundle_url,
            embed_options=embed_options,
        )  # type: ignore[call-arg]

    def _repr_mimebundle_(
        self,
        include: object | None = None,
        exclude: object | None = None,
    ) -> object:
        """Display the spec in notebook environments.

        Prefer the anywidget path when available because notebook frontends
        such as VS Code are more reliable with widget bundles than with inline
        HTML that contains scripts. Fall back to HTML rendering if widget
        construction is unavailable.
        """
        del include, exclude
        try:
            return self.widget()._repr_mimebundle_()
        except ImportError:
            return {"text/html": self.to_html()}

    def __add__(self, other: TopLevelSpec) -> LayerChart:
        return layer(self, other)

    def __or__(self, other: TopLevelSpec) -> HConcatChart:
        return hconcat(self, other)

    def __and__(self, other: TopLevelSpec) -> VConcatChart:
        return vconcat(self, other)

    def _append_transform(self, transform: dict[str, Any]) -> TopLevelSpec:
        merged = list(self.transform)
        merged.append(_normalize_transform(transform))
        return replace(self, transform=merged)

    def _body_dict(self) -> dict[str, Any]:
        raise NotImplementedError


@dataclass(frozen=True, slots=True)
class Chart(TopLevelSpec):
    """A minimal immutable builder for single-view GenomeSpy core specs."""

    data: Any = None
    mark: str | dict[str, Any] | None = None
    encoding: dict[str, dict[str, Any]] = field(default_factory=dict)

    def mark_point(self, **kwargs: Any) -> Chart:
        return self._with_mark("point", **kwargs)

    def mark_rect(self, **kwargs: Any) -> Chart:
        return self._with_mark("rect", **kwargs)

    def mark_rule(self, **kwargs: Any) -> Chart:
        return self._with_mark("rule", **kwargs)

    def mark_tick(self, **kwargs: Any) -> Chart:
        return self._with_mark("tick", **kwargs)

    def mark_text(self, **kwargs: Any) -> Chart:
        return self._with_mark("text", **kwargs)

    def mark_link(self, **kwargs: Any) -> Chart:
        return self._with_mark("link", **kwargs)

    def encode(self, **kwargs: Channel | str | dict[str, Any]) -> Chart:
        """Return a new chart with merged channel encodings."""
        merged = dict(self.encoding)
        for name, value in kwargs.items():
            merged[name] = _normalize_channel(value)
        return replace(self, encoding=merged)

    def _body_dict(self) -> dict[str, Any]:
        spec: dict[str, Any] = {}
        normalized_data = _normalize_data(self.data)
        if normalized_data is not None:
            spec["data"] = normalized_data
        if self.mark is not None:
            spec["mark"] = self.mark
        if self.encoding:
            spec["encoding"] = dict(self.encoding)
        return spec

    def _with_mark(self, mark_type: str, **kwargs: Any) -> Chart:
        if mark_type not in MARK_TYPES:
            raise ValueError(f"Unsupported mark type: {mark_type}")
        mark: str | dict[str, Any]
        if kwargs:
            mark = {"type": mark_type, **kwargs}
        else:
            mark = mark_type
        return replace(self, mark=mark)


@dataclass(frozen=True, slots=True)
class LayerChart(TopLevelSpec):
    """A layered GenomeSpy specification."""

    layer: list[TopLevelSpec] = field(default_factory=list)

    def __add__(self, other: TopLevelSpec) -> LayerChart:
        return replace(self, layer=[*self.layer, other])

    def _body_dict(self) -> dict[str, Any]:
        return {"layer": [child.to_dict(include_schema=False) for child in self.layer]}


@dataclass(frozen=True, slots=True)
class HConcatChart(TopLevelSpec):
    """A horizontally concatenated GenomeSpy specification."""

    hconcat: list[TopLevelSpec] = field(default_factory=list)

    def __or__(self, other: TopLevelSpec) -> HConcatChart:
        return replace(self, hconcat=[*self.hconcat, other])

    def _body_dict(self) -> dict[str, Any]:
        return {
            "hconcat": [child.to_dict(include_schema=False) for child in self.hconcat]
        }


@dataclass(frozen=True, slots=True)
class VConcatChart(TopLevelSpec):
    """A vertically concatenated GenomeSpy specification."""

    vconcat: list[TopLevelSpec] = field(default_factory=list)

    def __and__(self, other: TopLevelSpec) -> VConcatChart:
        return replace(self, vconcat=[*self.vconcat, other])

    def _body_dict(self) -> dict[str, Any]:
        return {
            "vconcat": [child.to_dict(include_schema=False) for child in self.vconcat]
        }


@dataclass(frozen=True, slots=True)
class ConcatChart(TopLevelSpec):
    """A grid-concatenated GenomeSpy specification."""

    concat: list[TopLevelSpec] = field(default_factory=list)
    columns: int = 1

    def _body_dict(self) -> dict[str, Any]:
        return {
            "concat": [child.to_dict(include_schema=False) for child in self.concat],
            "columns": self.columns,
        }


def layer(*charts: TopLevelSpec, **kwargs: Any) -> LayerChart:
    """Compose a layered chart from multiple child charts."""
    chart = LayerChart(layer=list(charts))
    if kwargs:
        return replace(chart, properties_map={**chart.properties_map, **kwargs})
    return chart


def hconcat(*charts: TopLevelSpec, **kwargs: Any) -> HConcatChart:
    """Compose a horizontally concatenated chart."""
    chart = HConcatChart(hconcat=list(charts))
    if kwargs:
        return replace(chart, properties_map={**chart.properties_map, **kwargs})
    return chart


def vconcat(*charts: TopLevelSpec, **kwargs: Any) -> VConcatChart:
    """Compose a vertically concatenated chart."""
    chart = VConcatChart(vconcat=list(charts))
    if kwargs:
        return replace(chart, properties_map={**chart.properties_map, **kwargs})
    return chart


def concat(*charts: TopLevelSpec, columns: int, **kwargs: Any) -> ConcatChart:
    """Compose a grid concatenation."""
    chart = ConcatChart(concat=list(charts), columns=columns)
    if kwargs:
        return replace(chart, properties_map={**chart.properties_map, **kwargs})
    return chart
