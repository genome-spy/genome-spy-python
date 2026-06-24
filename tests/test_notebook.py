from __future__ import annotations

from pathlib import Path

import nbformat


def test_notebook_example_is_valid() -> None:
    notebook_path = Path("notebooks/basic_point_chart.ipynb")
    notebook = nbformat.read(notebook_path, as_version=4)

    assert notebook["nbformat"] == 4
    assert any("chart" == "".join(cell["source"]).strip() for cell in notebook["cells"])
