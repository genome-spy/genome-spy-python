"""Project-specific Markdown export of maintained guides and gallery sources."""

from __future__ import annotations

import ast
import json
import posixpath
from pathlib import Path
import re
import textwrap

from tools.docs_gallery import CATEGORIES, UNKNOWN_CATEGORY

__all__: list[str] = []


def _documentation_pages(root: Path) -> list[dict]:
    """Collect guides and gallery entries without executing example modules."""
    pages = []
    for source in sorted((root / "docs/user-guide").rglob("*.md")):
        text = source.read_text(encoding="utf-8")
        title = re.search(r"^# (.+)$", text, re.MULTILINE)
        if title is None:
            raise ValueError(f"Missing documentation title: {source}")
        paragraphs = text.split("\n\n")[1:]
        description = next(
            part
            for part in paragraphs
            if part.strip() and not part.startswith("{download}")
        )
        description = re.sub(
            r"\{[^}]+\}`([^`]+)`",
            lambda m: m[1].split(" <", 1)[0].lstrip("~"),
            description,
        )
        description = re.sub(r"\[([^]]+)\]\([^)]+\)", r"\1", description).replace(
            "\n", " "
        )
        pages.append(
            {
                "destination": source.relative_to(root / "docs").as_posix(),
                "source": source.relative_to(root).as_posix(),
                "title": title[1],
                "section": "User guide",
                "description": description,
                "convert": True,
            }
        )
    examples = []
    for source in (root / "docs/examples").glob("*.py"):
        tree = ast.parse(source.read_text(encoding="utf-8"))
        doc = (ast.get_docstring(tree) or source.stem).split("\n", 1)
        meta = {}
        meta_node = None
        for node in tree.body:
            if isinstance(node, ast.Assign) and any(
                isinstance(target, ast.Name) and target.id == "META"
                for target in node.targets
            ):
                meta = ast.literal_eval(node.value)
                meta_node = node
        code = source.read_text(encoding="utf-8").splitlines(keepends=True)
        if meta_node is not None:
            del code[meta_node.lineno - 1 : meta_node.end_lineno]
        prose = source.with_suffix(".md")
        title = meta.get("title", doc[0].rstrip("."))
        description = meta.get(
            "description", doc[1].strip().split("\n\n", 1)[0] if len(doc) > 1 else ""
        )
        content = f"# {title}\n\n{description}\n\n"
        if prose.is_file():
            content += prose.read_text(encoding="utf-8").strip() + "\n\n"
        content += "## Code\n\n```python\n" + "".join(code).strip() + "\n```\n"
        examples.append(
            (
                meta.get("category", "Basic charts and composition"),
                meta.get("order", 100),
                source.stem,
                meta,
                doc,
                content,
            )
        )
    examples.sort(
        key=lambda item: (
            CATEGORIES.get(item[0], UNKNOWN_CATEGORY)[0],
            item[0],
            item[1],
            item[2],
        )
    )
    for category, _order, name, meta, doc, content in examples:
        pages.append(
            {
                "destination": f"gallery/{name}.md",
                "source": f"docs/gallery/{name}.md",
                "content": content,
                "title": meta.get("title", doc[0].rstrip(".")),
                "section": f"Gallery: {category}",
                "description": meta.get(
                    "description",
                    doc[1].strip().split("\n\n", 1)[0].replace("\n", " ")
                    if len(doc) > 1
                    else "Runnable chart example.",
                ),
                "convert": True,
            }
        )
    if examples:
        catalog = [
            "# Reuse gallery examples",
            "",
            "Find the closest use case, then read its Python source and explanation.",
            "Adapt the data inputs, fields, domains, and labels while preserving the working",
            "composition and rendering path. Check dependencies and provenance; some examples",
            "use prepared datasets or internal dataset helpers rather than public loading APIs.",
            "Use the public API and user-supplied data for delivered work.",
            "",
        ]
        for category in dict.fromkeys(item[0] for item in examples):
            catalog.extend(
                [
                    f"## {category}",
                    "",
                    CATEGORIES.get(category, UNKNOWN_CATEGORY)[1],
                    "",
                ]
            )
            for page in pages:
                if page["section"] == f"Gallery: {category}":
                    catalog.append(
                        f"- [{page['title']}](../{page['destination']}): {page['description']}"
                    )
            catalog.append("")
        pages.insert(
            0,
            {
                "destination": "agents/gallery.md",
                "source": "docs/agents/gallery.md",
                "aliases": ["docs/gallery/index.md"],
                "title": "Reuse gallery examples",
                "section": "Start here",
                "description": "Find working Python examples by use case and adapt their maintained patterns.",
                "content": "\n".join(catalog),
            },
        )
    return pages


def _plain_markdown(text: str, source: Path, root: Path) -> str:
    """Expand the directives used by this project's docs; reject unknown ones."""

    def directive(match: re.Match[str]) -> str:
        kind, argument, body = match.group(1, 2, 3)
        options = dict(re.findall(r"^:([\w-]+):\s*(.*)$", body, re.MULTILINE))
        if kind == "raw":
            return ""
        if kind == "literalinclude":
            path = (source.parent / argument).resolve()
            code = path.read_text(encoding="utf-8")
            for option, before in (("start-after", False), ("end-before", True)):
                if option in options:
                    marker = options[option]
                    if marker not in code:
                        raise ValueError(
                            f"Missing {option} marker {marker!r} in {path}"
                        )
                    if before:
                        code = code.split(marker, 1)[0].rsplit("\n", 1)[0]
                    else:
                        code = code.split(marker, 1)[1].split("\n", 1)[1]
            unsupported = options.keys() - {
                "language",
                "start-after",
                "end-before",
                "dedent",
            }
            if unsupported:
                raise ValueError(
                    f"Unsupported include options in {source}: {unsupported}"
                )
            return f"```{options.get('language', path.suffix.lstrip('.'))}\n{textwrap.dedent(code).strip()}\n```"
        if kind in {"genomespy-chart", "genomespy-workflow"}:
            if kind == "genomespy-workflow" and options.get("code") in {
                "chart",
                "hooks",
            }:
                from tools.docs_workflows import NOTEBOOKS

                notebook = json.loads(NOTEBOOKS[argument].read_text(encoding="utf-8"))
                cells = [
                    cell for cell in notebook["cells"] if cell["cell_type"] == "code"
                ]
                selected = cells[0 if options["code"] == "chart" else 1]
                return "```python\n" + "".join(selected["source"]).rstrip() + "\n```"
            return (
                "[Open the interactive example]("
                + source.relative_to(root / "docs").name.replace(".md", ".html")
                + ")."
            )
        if kind == "toctree":
            return "\n".join(
                f"- [{line}]({line}.md)"
                for line in body.splitlines()
                if line.strip() and not line.startswith(":")
            )
        raise ValueError(f"Unsupported Markdown directive {kind} in {source}")

    # Expand project directives before simplifying roles and containers.
    text = re.sub(
        r"^```\{([^}]+)\}[ \t]*([^\n]*)\n(.*?)^```[ \t]*$",
        directive,
        text,
        flags=re.MULTILINE | re.DOTALL,
    )
    lines = []
    in_code = False
    for line in text.splitlines():
        if line.startswith("```"):
            in_code = not in_code
        if not in_code:
            opening = re.match(r"^:{3,}\{([^}]+)\}\s*(.*)", line)
            if opening:
                kind, title = opening.groups()
                if kind not in {
                    "admonition",
                    "dropdown",
                    "grid",
                    "grid-item-card",
                    "note",
                    "warning",
                    "tip",
                }:
                    raise ValueError(
                        f"Unsupported Markdown container {kind} in {source}"
                    )
                if kind != "grid":
                    lines.append(f"**{title or kind.title()}**\n")
                continue
            if re.match(r"^:{3,}$|^:[\w-]+:", line):
                if line.startswith(":link:"):
                    target = line.removeprefix(":link:").strip()
                    lines.append(f"[Open this workflow]({target}.md)")
                continue
            label = re.match(r"^\(([^)]+)\)=$", line)
            if label:
                lines.append(f'<a id="{label[1]}"></a>')
                continue

            def role(match: re.Match[str]) -> str:
                kind, value = match.groups()
                explicit = re.match(r"(.+) <([^>]+)>$", value)
                title, target = (
                    explicit.groups()
                    if explicit
                    else (value.lstrip("~"), value.lstrip("~"))
                )
                if kind.startswith("py:"):
                    return f"`{title}`"
                if kind == "ref":
                    for page in (root / "docs").rglob("*.md"):
                        if (
                            "_build" not in page.parts
                            and f"({target})=" in page.read_text(encoding="utf-8")
                        ):
                            return f"[{title}]({posixpath.relpath(page, source.parent)}#{target})"
                    raise ValueError(f"Unresolved reference {target!r} in {source}")
                if kind == "doc":
                    return f"[{title}]({target}.md)"
                if kind == "download":
                    # Human page serves Sphinx's hashed download asset.
                    return f"{title} (download from the interactive page)"
                raise ValueError(f"Unsupported Markdown role {kind} in {source}")

            line = re.sub(r"\{([^}]+)\}`([^`]+)`", role, line)
        lines.append(line)
    return "\n".join(lines).strip() + "\n"
