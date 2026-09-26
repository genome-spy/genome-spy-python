"""Check notebook index coordinates and the real review chart contract."""

import math

import pytest

from tests.test_workflow_notebooks import notebook_function
from tools.docs_workflows import load_spec


@pytest.mark.parametrize(
    "bounds,expected",
    [
        ([15646757, 15646758], {"start": 15646757, "end": 15646758}),
        ([15646757.2, 15646760.8], {"start": 15646758, "end": 15646761}),
        ([15646760.8, 15646757.2], {"start": 15646758, "end": 15646761}),
        ([0, 99999999], {"start": 15646649, "end": 15647250}),
    ],
)
def test_integer_selection_becomes_half_open_bed(bounds, expected):
    convert = notebook_function("annotate_squid", "base_interval", math=math)
    assert (
        convert({"active": True, "intervals": {"x": bounds}}, 15646649, 15647250)
        == expected
    )


@pytest.mark.parametrize(
    "bounds",
    [[15646757, 15646757], [0, 1], [15646757.2, 15646757.8], [float("nan"), 15646760]],
)
def test_empty_or_nonfinite_squid_selection_is_rejected(bounds):
    convert = notebook_function("annotate_squid", "base_interval", math=math)
    with pytest.raises(ValueError):
        convert({"active": True, "intervals": {"x": bounds}}, 15646649, 15647250)


def test_squid_adds_named_review_dataset_without_replacing_evidence():
    spec = load_spec("squid")
    prediction, middle, contribution, saved = spec["vconcat"]
    assert prediction["title"]["text"] == "Predicted accessibility"
    assert len(middle["layer"]) == 2
    assert contribution["name"] == "importance"
    assert spec["datasets"] == {"annotations": []}
    assert saved["name"] == "review-annotations"
    assert saved["height"] == 24
    assert "title" not in saved
    assert "y" not in saved["layer"][0]["encoding"]
    assert saved["layer"][0]["encoding"]["color"]["scale"] is None
    assert saved["layer"][0]["data"] == {"name": "annotations"}
    assert saved["layer"][0]["encoding"]["x"]["type"] == "index"


def test_browser_and_python_agree_on_base_boundaries():
    import json
    from pathlib import Path
    import subprocess

    root = Path(__file__).resolve().parents[1]
    bounds = [
        [15646757, 15646758],
        [15646757.2, 15646760.8],
        [15646760.8, 15646757.2],
        [0, 99999999],
    ]
    result = subprocess.run(
        [
            "node",
            "--input-type=module",
            "-e",
            """
import {squidInterval, squidDraft, annotationCsv} from './docs/_static/workflows.js';
const snapshots = JSON.parse(process.argv[1]).map(x => ({active: true, intervals: {x}}));
const results = snapshots.map(snapshot => squidInterval(snapshot, 15646649, 15647250));
const draft = squidDraft(snapshots[0], {active: false});
snapshots[0].intervals.x[0] = 15647000;
if (draft.start !== 15646757 || draft.output_start !== '') throw Error('Draft changed or invented output');
for (const x of [[0, 1], [15646757.2, 15646757.8], [NaN, 15646760]]) {
  let rejected = false;
  try { squidInterval({active: true, intervals: {x}}, 15646649, 15647250); }
  catch { rejected = true; }
  if (!rejected) throw Error('Invalid selection accepted');
}
console.log(JSON.stringify(results));
""",
            json.dumps(bounds),
        ],
        cwd=root,
        text=True,
        capture_output=True,
        check=True,
    )
    convert = notebook_function("annotate_squid", "base_interval", math=math)
    assert json.loads(result.stdout) == [
        convert({"active": True, "intervals": {"x": x}}, 15646649, 15647250)
        for x in bounds
    ]


def test_python_hooks_freeze_context_and_save_only_after_browser_ack(monkeypatch):
    import asyncio
    import json
    from pathlib import Path
    from types import SimpleNamespace
    from unittest.mock import AsyncMock

    import IPython.display

    monkeypatch.setattr(IPython.display, "display", lambda *args, **kwargs: None)
    notebook = json.loads(
        (Path(__file__).parents[1] / "notebooks/annotate_squid.ipynb").read_text()
    )
    source = "".join(notebook["cells"][2]["source"])

    async def run():
        snapshots = {
            "contributionRegion": {
                "active": True,
                "intervals": {"x": [15646757, 15646764]},
            },
            "accessibilityRegion": {
                "active": True,
                "intervals": {"x": [15646950, 15646960]},
            },
        }

        async def get_selection(name):
            return SimpleNamespace(
                get_value=AsyncMock(return_value=snapshots[name]),
                subscribe=AsyncMock(),
                clear=AsyncMock(),
            )

        async def get_view(address):
            assert address["view"] in ("importance", "prediction")
            return SimpleNamespace(params=SimpleNamespace(get_selection=get_selection))

        write = AsyncMock()
        api = SimpleNamespace(
            views=SimpleNamespace(get=get_view), datasets=SimpleNamespace(set=write)
        )
        widget = SimpleNamespace(get_embed_api=AsyncMock(return_value=api))
        namespace = {"chart": SimpleNamespace(widget=lambda **kwargs: widget)}
        exec(compile(source, "annotate_squid.ipynb", "exec"), namespace)
        await namespace["connection_task"]
        namespace["prepare_annotation"](None)
        namespace["snapshots"]["input"] = {"active": False, "intervals": {"x": None}}
        namespace["name_input"].value = "candidate"
        namespace["color_input"].value = "#224488"
        namespace["note_input"].value = 'Inspect "motif", <b>literal</b>'
        write.side_effect = RuntimeError("Browser disconnected")
        with pytest.raises(RuntimeError, match="disconnected"):
            await namespace["save_annotation"]()
        assert namespace["annotations"] == []
        assert namespace["pending"] is not None
        write.side_effect = None
        await namespace["save_annotation"]()
        (record,) = namespace["annotations"]
        assert (record["start"], record["end"]) == (15646757, 15646764)
        assert (record["output_start"], record["output_end"]) == (15646950, 15646960)
        assert record["id"] == 1
        assert record["color"] == "#224488"
        assert record["label_color"] == "#ffffff"
        assert record["note"] == 'Inspect "motif", <b>literal</b>'
        assert namespace["pending"] is None
        write.assert_awaited_with("annotations", [record])
        await namespace["clear_brushes"]()
        assert len(namespace["annotations"]) == 1
        await namespace["remove_annotation"]()
        assert namespace["annotations"] == []

    asyncio.run(run())
