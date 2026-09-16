"""Regression checks for the executable embed notebook."""

import ast
import asyncio
import json
from pathlib import Path


def test_annotation_save_ignores_overlapping_requests() -> None:
    notebook = json.loads(
        (Path(__file__).parents[1] / "notebooks" / "embed_api.ipynb").read_text()
    )
    source = "\n".join(
        "".join(cell["source"])
        for cell in notebook["cells"]
        if cell["cell_type"] == "code"
    )
    start_save = next(
        node
        for node in ast.parse(source).body
        if isinstance(node, ast.FunctionDef) and node.name == "start_save"
    )

    async def run() -> None:
        release = asyncio.Event()
        saves = []

        async def save_annotation() -> None:
            await release.wait()
            saves.append("saved")

        namespace = {"asyncio": asyncio, "save_annotation": save_annotation}
        exec(
            compile(ast.Module(body=[start_save], type_ignores=[]), "notebook", "exec"),
            namespace,
        )
        namespace["start_save"]()
        first = namespace["annotation_save_task"]
        namespace["start_save"]()  # Another click queued before the task starts.
        assert namespace["annotation_save_task"] is first
        release.set()
        await first
        assert saves == ["saved"]
        namespace["start_save"]()  # Saving again after completion is allowed.
        await namespace["annotation_save_task"]
        assert saves == ["saved", "saved"]

    asyncio.run(run())
