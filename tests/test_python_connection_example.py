"""Validate the shared, downloadable Python integration example."""

import asyncio
from contextlib import suppress
import json
from pathlib import Path
import runpy
from types import SimpleNamespace


EXAMPLE = Path(__file__).parents[1] / "docs" / "integration"


def test_shared_chart_and_notebook():
    component = runpy.run_path(str(EXAMPLE / "component.py"))
    spec = component["chart"].to_dict()
    assert spec["assembly"] == "demo"
    assert spec["datasets"]["annotations"] == []
    assert spec["vconcat"][1]["height"] == 22
    notebook = json.loads((EXAMPLE / "notebook.ipynb").read_text())
    for cell in notebook["cells"]:
        if cell["cell_type"] == "code":
            compile("".join(cell["source"]), "notebook", "exec")


def test_python_saves_only_valid_committed_intervals_and_unsubscribes():
    component = runpy.run_path(str(EXAMPLE / "component.py"))

    async def run():
        updates = []
        messages = []
        annotations = []
        ready = asyncio.Event()
        changed = asyncio.Event()
        unsubscribed = False
        listener = None

        async def subscribe(callback, options):
            nonlocal listener
            assert options == {"delivery": "commit"}
            listener = callback
            ready.set()

            async def stop():
                nonlocal unsubscribed
                unsubscribed = True

            return stop

        async def get_selection(name):
            assert name == "brush"
            return SimpleNamespace(subscribe=subscribe)

        async def set_dataset(name, records):
            assert name == "annotations"
            updates.append(records)
            changed.set()

        api = SimpleNamespace(
            params=SimpleNamespace(get_selection=get_selection),
            datasets=SimpleNamespace(set=set_dataset),
        )
        task = asyncio.create_task(
            component["annotate"](api, annotations, messages.append)
        )
        try:
            await ready.wait()
            listener({"active": False})
            for end_chrom, end in [("chrOther", 30), ("chrDemo", 20), ("chrDemo", 30)]:
                listener(
                    {
                        "active": True,
                        "complexIntervals": {
                            "x": [
                                {"chrom": "chrDemo", "pos": 20},
                                {"chrom": end_chrom, "pos": end},
                            ]
                        },
                    }
                )
            await asyncio.wait_for(changed.wait(), 2)
            assert annotations == [
                {"chrom": "chrDemo", "start": 20, "end": 30, "name": "region_1"}
            ]
            assert updates == [annotations]
            assert "Python saved 1 region" in messages[-1]
        finally:
            task.cancel()
            with suppress(asyncio.CancelledError):
                await task
        assert unsubscribed

    asyncio.run(run())
