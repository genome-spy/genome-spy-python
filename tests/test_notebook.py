from __future__ import annotations

import importlib.util
from pathlib import Path
from types import ModuleType

import nbformat
import pytest


@pytest.mark.parametrize("notebook_path", sorted(Path("notebooks").glob("*.ipynb")))
def test_notebook_example_is_valid(notebook_path: Path) -> None:
    notebook = nbformat.read(notebook_path, as_version=4)

    assert notebook["nbformat"] == 4
    assert any(
        "chart" in "".join(cell["source"])
        for cell in notebook["cells"]
        if cell["cell_type"] == "code"
    )


@pytest.mark.parametrize(
    "notebook_path",
    [
        Path("notebooks/genome_spy_interactions.py"),
        Path("notebooks/genome_spy_arrow.py"),
    ],
)
def test_marimo_notebook_emits_visible_output(notebook_path: Path) -> None:
    module = _load_python_module(notebook_path)

    outputs, definitions = module.app.run()

    assert any(output is not None for output in outputs)
    assert hasattr(definitions["chart_widget"], "widget")


def _load_python_module(path: Path) -> ModuleType:
    module_spec = importlib.util.spec_from_file_location(path.stem, path)
    if module_spec is None or module_spec.loader is None:
        raise RuntimeError(f"Could not load notebook module from {path}.")
    module = importlib.util.module_from_spec(module_spec)
    module_spec.loader.exec_module(module)
    return module
