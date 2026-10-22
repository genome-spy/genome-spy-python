"""Publish focused, plain Markdown agent documentation alongside Sphinx HTML."""

from __future__ import annotations

import inspect
import json
from pathlib import Path
import re
from urllib.parse import urljoin, urlsplit

from tools.agent_markdown import _documentation_pages, _plain_markdown

import genome_spy as gs
from genome_spy import embed

__all__ = ["publish_agent_docs"]

_LINK = re.compile(r"(?<!!)\[([^\]]+)\]\(([^)]+)\)")


def _api(section: str | None = None) -> str:
    groups = {
        "Chart authoring": {
            "gs.Chart": gs.Chart,
            **{
                f"Chart.{name}": getattr(gs.Chart, name)
                for name in (
                    "encode",
                    "mark_point",
                    "mark_rect",
                    "mark_rule",
                    "properties",
                    "configure_legend",
                )
            },
            "LayerChart.resolve_scale": gs.LayerChart.resolve_scale,
        },
        "Fields and guides": {
            **{
                f"gs.{name}": getattr(gs, name)
                for name in ("X", "Y", "Color", "Size", "Tooltip")
            },
            "X.scale": gs.X("x:Q").scale,
            "X.axis": gs.X("x:Q").axis,
            "Color.legend": gs.Color("group:N").legend,
        },
        "Validation and output": {
            f"Chart.{name}": getattr(gs.Chart, name)
            for name in ("to_dict", "to_json", "save", "display", "widget")
        },
        "Live embed": {
            **{
                f"JupyterChart.{name}": getattr(gs.JupyterChart, name)
                for name in ("get_embed_api", "set_dataset", "set_data")
            },
            **{
                f"{cls.__name__}.{name}": getattr(cls, name)
                for cls, names in (
                    (embed.ParamNamespace, ("get", "get_selection")),
                    (embed.ParamApi, ("get_value", "set_value", "subscribe")),
                    (embed.PointSelectionApi, ("get_value", "subscribe", "clear")),
                    (
                        embed.IntervalSelectionApi,
                        ("get_value", "subscribe", "clear", "contains"),
                    ),
                    (embed.DatasetApi, ("set", "reset")),
                    (embed.ViewApi, ("get",)),
                    (embed.EmbedResult, ("finalize",)),
                )
                for name in names
            },
        },
    }
    if section is None:
        return """# Python API reference

Signatures are generated from the documentation build's installed public API.
This is a focused subset of the library. Load the relevant page:

- [Chart authoring](api-chart.md): charts, marks, properties, and composition scales.
- [Encodings and guides](api-encodings.md): fields, channels, scales, axes, and legends.
- [Validation and output](api-output.md): serialization, files, display, and widgets.
- [Live Embed API](api-embed.md): notebook connection and live runtime operations.

For semantics, read [encodings](encodings.md), [scales](scales-axes-legends.md),
and [rendering](rendering.md). For callbacks and data updates, read the
[Embed API guide](embed-api.md). For other marks, transforms, genomic types, or full
option descriptions, use the [full API reference](../api.html) and installed signatures.
"""
    groups = {section: groups[section]}
    text = [
        "# Python API signatures",
        "",
        "Generated from the documentation build's installed public API. This is a",
        "focused subset, not the full schema/API inventory. Check installed signatures",
        "if an option is unavailable. Read the task guides for semantics.",
        "",
    ]
    for title, entries in groups.items():
        text.extend([f"## {title}", ""])
        for name, value in entries.items():
            summary = (inspect.getdoc(value) or "").split("\n", 1)[0]
            text.extend(
                [
                    f"### `{name}`",
                    "",
                    summary,
                    "",
                    "```text",
                    f"{name}{inspect.signature(value)}",
                    "```",
                    "",
                ]
            )
    text.extend(
        [
            "For other marks, transforms, genomic types, or complete option descriptions,",
            "use the [full API reference](../api.html) and installed signatures.",
            "",
        ]
    )
    return "\n".join(text)


def publish_agent_docs(root: Path, output: Path, base_url: str) -> list[Path]:
    """Publish indexed agent Markdown to an HTML documentation output directory.

    The explicit manifest routes authored pages and canonical skill references.
    Local links are rewritten to published pages and checked before files are
    written. Gallery categories and user guides reuse their maintained sources.

    Args:
        root: Repository root containing docs, skills, and project metadata.
        output: Sphinx HTML output directory.
        base_url: Absolute public documentation base URL, including any subpath.

    Returns:
        Paths of the Markdown pages and llms.txt index written.

    Raises:
        ValueError: Routes, base URL, directives, or local links are invalid.
        OSError: A source cannot be read or an output cannot be written.

    Example:
        >>> publish_agent_docs(Path("."), Path("docs/_build/html"),
        ...                    "https://genomespy.app/genome-spy-python/")  # doctest: +SKIP
    """
    root = root.resolve()
    base_url = base_url.rstrip("/") + "/"
    if (
        urlsplit(base_url).scheme not in {"https", "http"}
        or not urlsplit(base_url).netloc
    ):
        raise ValueError(f"Expected an absolute documentation URL: {base_url}")
    pages = json.loads((root / "docs/agents/manifest.json").read_text(encoding="utf-8"))
    for page in pages:
        if "url" in page:
            url = urlsplit(page["url"])
            if url.scheme != "https" or not url.netloc:
                raise ValueError(
                    f"Expected an absolute HTTPS documentation URL: {page['url']}"
                )
        else:
            page["destination"] = "agents/" + page["path"]
    pages.extend(_documentation_pages(root))
    local_pages = [page for page in pages if "url" not in page]
    routes: dict[Path, str] = {}
    names: set[str] = set()
    for page in local_pages:
        path = Path(page["destination"])
        if (
            path.is_absolute()
            or ".." in path.parts
            or path.suffix != ".md"
            or path.as_posix() in names
        ):
            raise ValueError(f"Invalid or duplicate agent route: {path}")
        names.add(path.as_posix())
        routes[(root / "docs" / path).resolve()] = path.as_posix()
        routes[
            (root / page.get("source", "docs/agents/" + page.get("path", ""))).resolve()
        ] = path.as_posix()
        for alias in page.get("aliases", []):
            routes[(root / alias).resolve()] = path.as_posix()
    rendered: dict[str, str] = {}
    for page in local_pages:
        source = (
            root / page.get("source", "docs/agents/" + page.get("path", ""))
        ).resolve()
        text = (
            page["content"]
            if "content" in page
            else source.read_text(encoding="utf-8")
            if "source" in page
            else _api(page.get("api_section"))
        )
        if page.get("convert"):
            text = _plain_markdown(text, source, root)
            heading, separator, body = text.partition("\n")
            text = (
                heading
                + separator
                + f"\n[Open the rendered page]({source.stem}.html).\n"
                + body
            )
        if re.search(
            r"^\s*(?:```\{|\.\. (?:automodule|autoclass|autofunction|include)::)",
            text,
            re.MULTILINE,
        ):
            raise ValueError(
                f"Agent Markdown must not contain Sphinx directives: {source}"
            )

        def rewrite(match: re.Match[str]) -> str:
            label, href = match.groups()
            if urlsplit(href).scheme or href.startswith("#"):
                return match.group(0)
            target = (source.parent / href.split("#", 1)[0]).resolve()
            if not target.suffix and target.with_suffix(".md") in routes:
                target = target.with_suffix(".md")
            fragment = "#" + href.split("#", 1)[1] if "#" in href else ""
            if target in routes:
                href = urljoin(base_url, routes[target]) + fragment
            elif href.split("#", 1)[0].endswith(".html"):
                href = urljoin(urljoin(base_url, page["destination"]), href)
            elif page.get("convert") and target.is_file():
                relative = target.relative_to(root / "docs")
                href = (
                    urljoin(base_url, relative.with_suffix(".html").as_posix())
                    + fragment
                )
            else:
                raise ValueError(f"Unpublished local link in {source}: {href}")
            return f"[{label}]({href})"

        parts = re.split(
            r"(^```[^\n]*\n.*?^```[ \t]*$)", text, flags=re.MULTILINE | re.DOTALL
        )
        text = "".join(
            part if i % 2 else _LINK.sub(rewrite, part) for i, part in enumerate(parts)
        )
        rendered[page["destination"]] = text
    index = [
        "# genome-spy-python",
        "",
        "> Agent documentation for authoring, connecting, validating, and delivering GenomeSpy charts.",
        "",
        "Read the relevant pages only. Local guides are plain Markdown; upstream JavaScript",
        "references are labeled HTML and may expose features not wrapped in Python.",
        "Start with a relevant gallery example and adapt its working",
        "data, encodings, composition, and rendering path before adding workarounds.",
        "Check installed signatures if an option is unavailable.",
        "",
    ]
    for section in dict.fromkeys(page["section"] for page in pages):
        index.extend([f"## {section}", ""])
        for page in pages:
            if page["section"] == section:
                href = (
                    page["url"]
                    if "url" in page
                    else urljoin(base_url, page["destination"])
                )
                index.append(f"- [{page['title']}]({href}): {page['description']}")
        index.append("")
    written = []
    for name, text in {
        **rendered,
        "llms.txt": "\n".join(index),
    }.items():
        destination = output / name
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_text(text, encoding="utf-8")
        written.append(destination)
    return written
