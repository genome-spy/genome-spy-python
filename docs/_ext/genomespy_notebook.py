"""Render a workflow notebook as prose, code and native GenomeSpy charts."""

from __future__ import annotations

import json
import posixpath
from hashlib import file_digest, sha256
from importlib.metadata import version
from pathlib import Path
from typing import Any

from docutils import nodes
from docutils.parsers.rst import Directive
from docutils.statemachine import StringList
from sphinx.application import Sphinx

from genomespy_gallery import _tutorial_embed_html, core
from genome_spy._embed import normalize_controls


def _preparation_digest(notebook: dict[str, Any]) -> str:
    """Identify the analysis code and Scanpy version used for prepared inputs."""
    sources = [
        cell["source"]
        for cell in notebook["cells"]
        if cell["cell_type"] == "code"
        and not cell.get("metadata", {}).get("genomespy", {}).get("chart")
        and "jupyter-only" not in cell.get("metadata", {}).get("tags", [])
    ]
    return sha256(
        json.dumps(
            [sources, notebook["metadata"]["genomespy"], version("scanpy")]
        ).encode()
    ).hexdigest()


def _prepared_paths(notebook: dict[str, Any], root: Path) -> dict[str, Path]:
    """Resolve prepared AnnData files inside the repository's ignored cache."""
    paths = {
        name: (root / filename).resolve()
        for name, filename in notebook.get("metadata", {})
        .get("genomespy", {})
        .get("prepared_data", {})
        .items()
    }
    if any(
        not path.is_relative_to((root / "tmp").resolve()) or path.suffix != ".h5ad"
        for path in paths.values()
    ):
        raise ValueError("Prepared notebook data must be H5AD files inside tmp/.")
    return paths


def _file_digest(path: Path) -> str:
    """Hash a prepared file without loading the matrix into memory."""
    with path.open("rb") as source:
        return file_digest(source, "sha256").hexdigest()


def _preparation_current(notebook: dict[str, Any], root: Path) -> bool:
    """Check that cached inputs match both their analysis code and file contents."""
    signature = _preparation_digest(notebook)
    try:
        return all(
            path.with_suffix(".sha256").read_text().splitlines()
            == [signature, _file_digest(path)]
            for path in _prepared_paths(notebook, root).values()
        )
    except OSError:
        return False


def _notebook_markdown(
    path: Path, *, download_path: str, bundle_url: str, root: Path | None = None
) -> str:
    """Read notebook cells, run page examples and return their Markdown and embeds."""
    notebook = json.loads(path.read_text(encoding="utf-8"))
    root = root or Path(__file__).resolve().parents[2]
    namespace: dict[str, Any] = {"__name__": "__genomespy_notebook__"}
    prepared = _prepared_paths(notebook, root)
    if prepared:
        if not _preparation_current(notebook, root):
            raise ValueError(
                f"Missing or stale prepared data for {path.name}; run uv run integrations/scanpy/prepare_guide_data.py {path.stem}."
            )
        from anndata import read_h5ad

        namespace.update(
            {name: read_h5ad(filename) for name, filename in prepared.items()}
        )
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
        # Show preparation and live-kernel cells without running them in Sphinx.
        if {"jupyter-only", "prepare-data"}.intersection(metadata.get("tags", [])):
            continue
        try:
            exec(compile(source, f"{path}:cell {index + 1}", "exec"), namespace)
            if chart := metadata.get("genomespy"):
                definitions, modules = core.default_control_config()
                markup = _tutorial_embed_html(
                    chart["chart"],
                    namespace[chart["chart"]].to_dict(),
                    bundle_url=bundle_url,
                    height=chart["height"],
                    title=chart["title"],
                    identity=f"{path}:{index}",
                    controls=normalize_controls(chart.get("controls", False)),
                    control_definitions=definitions,
                    control_module_urls=modules,
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
        notebook = json.loads(path.read_text(encoding="utf-8"))
        for prepared in _prepared_paths(notebook, root).values():
            env.note_dependency(str(prepared))
            env.note_dependency(str(prepared.with_suffix(".sha256")))
        download = posixpath.relpath(
            path.as_posix(), Path(env.doc2path(env.docname)).parent.as_posix()
        )
        try:
            markdown = _notebook_markdown(
                path,
                download_path=download,
                bundle_url=core.default_bundle_url(),
                root=root,
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
