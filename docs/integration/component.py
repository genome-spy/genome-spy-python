"""Shared chart and Python annotation logic for the notebook and web examples."""

import asyncio
from collections.abc import Callable
from typing import Any

import genome_spy as gs
from genome_spy.embed import EmbedResult

# Synthetic intervals on a fictional chromosome; no external data required.
features = (
    gs.Chart(
        [
            {"chrom": "chrDemo", "start": 100, "end": 300},
            {"chrom": "chrDemo", "start": 450, "end": 700},
        ]
    )
    .mark_rect(color="#547aa5")
    .encode(x=gs.Locus("chrom", "start"), x2=gs.Locus("chrom", "end"))
    .properties(height=70, title="Brush a region; release to save in Python")
)

saved = (
    gs.Chart(data={"name": "annotations"})
    .mark_rect(color="#d89632", opacity=0.7)
    .encode(
        x=gs.Locus("chrom", "start"),
        x2=gs.Locus("chrom", "end"),
        tooltip=["name:N", "chrom:N", "start:Q", "end:Q"],
    )
    .properties(height=22, title="Saved annotations")
)

chart = (
    (features & saved)
    .properties(
        width=700,
        assembly="demo",
        genomes={"demo": {"contigs": [{"name": "chrDemo", "size": 1000}]}},
        datasets={"annotations": []},
        scales=gs.scales(
            x=gs.Scale(
                domain=[
                    {"chrom": "chrDemo", "pos": 0},
                    {"chrom": "chrDemo", "pos": 1000},
                ]
            )
        ),
    )
    .add_params(
        gs.selection_interval(
            "brush", encodings=["x"], extent="container", on={"type": "mousedown"}
        )
    )
)


async def annotate(
    api: EmbedResult,
    annotations: list[dict[str, Any]],
    show: Callable[[str], None],
) -> None:
    """Listen until cancelled; save committed brushes and update the chart."""
    events: asyncio.Queue = asyncio.Queue()
    async with asyncio.timeout(30):
        brush = await api.params.get_selection("brush")
        stop = await brush.subscribe(events.put_nowait, {"delivery": "commit"})
    show("Ready — brush a region and release to save it in Python.")
    try:
        while True:
            snapshot = await events.get()
            endpoints = snapshot.get("complexIntervals", {}).get("x")
            if not snapshot.get("active") or not endpoints:
                continue
            left, right = endpoints
            start, end = left["pos"], right["pos"]
            if left["chrom"] != right["chrom"] or not 0 <= start < end:
                show("Choose a nonempty interval within one chromosome.")
                continue
            record = {
                "chrom": left["chrom"],
                "start": start,
                "end": end,
                "name": f"region_{len(annotations) + 1}",
            }
            async with asyncio.timeout(30):
                await api.datasets.set("annotations", [*annotations, record])
            annotations.append(record)
            show(f"Python saved {len(annotations)} region(s): {record}")
    finally:
        async with asyncio.timeout(2):
            await stop()
