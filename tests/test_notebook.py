from __future__ import annotations

from pathlib import Path

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
