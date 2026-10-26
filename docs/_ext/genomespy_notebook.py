"""Render a workflow notebook as prose, code and native GenomeSpy charts."""

from __future__ import annotations

import json
import posixpath
from pathlib import Path
from typing import Any

from docutils import nodes
from docutils.parsers.rst import Directive
from docutils.statemachine import StringList
from sphinx.application import Sphinx

from genomespy_gallery import _tutorial_embed_html, core


def _notebook_markdown(path: Path, *, download_path: str, bundle_url: str) -> str:
    """Read notebook cells, run page examples and return their Markdown and embeds."""
    notebook = json.loads(path.read_text(encoding="utf-8"))
    namespace: dict[str, Any] = {"__name__": "__genomespy_notebook__"}
    parts = []
    for index, cell in enumerate(notebook["cells"]):
        source = "".join(cell["source"])
        if cell["cell_type"] == "markdown":
            parts.append(source)
            if index == 0:
                parts.append(f"{{download}}`Download notebook <{download_path}>`")
            continue
        if cell["cell_type"] != "code":
            raise ValueError(
                f"{path.name}, cell {index + 1}: expected code or Markdown"
            )

        parts.append(f"```python\n{source.rstrip()}\n```")
        metadata = cell.get("metadata", {})
        # Python retrieval needs a live kernel; the page shows those cells as code.
        if "jupyter-only" in metadata.get("tags", []):
            continue
        try:
            exec(compile(source, f"{path}:cell {index + 1}", "exec"), namespace)
            if chart := metadata.get("genomespy"):
                markup = _tutorial_embed_html(
                    chart["chart"],
                    namespace[chart["chart"]].to_dict(),
                    bundle_url=bundle_url,
                    height=chart["height"],
                    title=chart["title"],
                    identity=f"{path}:{index}",
                )
                parts.append(f"```{{raw}} html\n{markup}\n```")
        except Exception as exc:
            raise ValueError(f"{path.name}, cell {index + 1}: {exc}") from exc
    return "\n\n".join(parts)


class GenomeSpyNotebook(Directive):
    """Show a repository notebook and its live charts from one example source."""

    required_arguments = 1
    has_content = False

    def run(self) -> list[nodes.Node]:
        env = self.state.document.settings.env
        root = Path(env.srcdir).parent.resolve()
        path = (root / self.arguments[0]).resolve()
        if not path.is_relative_to(root) or path.suffix != ".ipynb":
            raise self.error("Expected a notebook path inside this repository.")
        env.note_dependency(str(path))
        download = posixpath.relpath(
            path.as_posix(), Path(env.doc2path(env.docname)).parent.as_posix()
        )
        try:
            markdown = _notebook_markdown(
                path, download_path=download, bundle_url=core.default_bundle_url()
            )
        except (OSError, ValueError, KeyError) as exc:
            raise self.error(f"Cannot render notebook: {exc}") from exc
        container = nodes.container(classes=["gs-notebook"])
        self.state.nested_parse(
            StringList(markdown.splitlines(), source=str(path)),
            0,
            container,
            match_titles=True,
        )
        return [container]


def setup(app: Sphinx) -> dict[str, bool]:
    """Register the notebook directive with Sphinx."""
    app.add_directive("genomespy-notebook", GenomeSpyNotebook)
    return {"parallel_read_safe": True, "parallel_write_safe": True}
