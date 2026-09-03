from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

import pytest

pytestmark = pytest.mark.docs

REPO_ROOT = Path(__file__).resolve().parent.parent


def _load_renderer():
    path = REPO_ROOT / "tools" / "render_thumbnails.py"
    spec = importlib.util.spec_from_file_location("_gs_render_thumbnails", path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def test_thumbnail_layout_uses_example_dimensions() -> None:
    renderer = _load_renderer()
    example = type("Example", (), {"height": 660, "max_width": 760})()

    layout = renderer.thumbnail_layout(example)

    assert layout.stage_width == 1000
    assert layout.min_stage_height == 660


def test_thumbnail_layout_defaults_to_card_width() -> None:
    renderer = _load_renderer()
    example = type("Example", (), {"height": 320, "max_width": None})()

    layout = renderer.thumbnail_layout(example)

    assert layout.stage_width == renderer.CARD_WIDTH
    assert layout.min_stage_height == 320


def test_center_translation_centers_ink_bounds() -> None:
    renderer = _load_renderer()
    bounds = renderer.PaintBounds(left=40, top=80, right=1240, bottom=720)

    assert renderer.center_translation(bounds) == (40, 2.5)


def test_center_translation_keeps_ink_inside_padding() -> None:
    renderer = _load_renderer()
    bounds = renderer.PaintBounds(left=0, top=0, right=1400, bottom=786)

    assert renderer.center_translation(bounds) == (8, 0)


def test_thumbnail_spec_removes_transient_zoom_guidance_without_mutating_input() -> (
    None
):
    renderer = _load_renderer()
    spec = {"layer": [{"name": "zoom-message"}, {"name": "data"}]}

    assert renderer.thumbnail_spec(spec) == {"layer": [{"name": "data"}]}
    assert spec["layer"][0]["name"] == "zoom-message"

    nested = {"layer": [{"layer": [{"name": "zoom-message"}, {"mark": "text"}]}]}
    assert renderer.thumbnail_spec(nested) == {"layer": []}


def test_thumbnail_spec_resolves_container_width_without_mutating_input() -> None:
    renderer = _load_renderer()
    spec = {"width": "container", "mark": "point"}

    assert renderer.thumbnail_spec(spec, container_width=980)["width"] == 980
    assert spec["width"] == "container"


def test_select_examples_defaults_to_all_examples() -> None:
    renderer = _load_renderer()
    examples = [
        type("Example", (), {"name": "first"})(),
        type("Example", (), {"name": "second"})(),
    ]
    gallery = type("Gallery", (), {"collect_examples": lambda self: examples})()

    assert renderer._select_examples(gallery, []) == examples


def test_select_examples_rejects_unknown_name() -> None:
    renderer = _load_renderer()
    example = type("Example", (), {"name": "first"})()
    gallery = type("Gallery", (), {"collect_examples": lambda self: [example]})()

    try:
        renderer._select_examples(gallery, ["missing"])
    except ValueError as error:
        assert "Unknown example name(s): missing" in str(error)
    else:
        raise AssertionError("unknown example name should fail")


def test_card_css_matches_the_thumbnail_capture_ratio() -> None:
    """Gallery cards letterbox their thumbnails when the two ratios diverge."""
    renderer = _load_renderer()
    css = (REPO_ROOT / "docs" / "_static" / "genomespy.css").read_text(encoding="utf-8")

    assert renderer.CARD_WIDTH / renderer.CARD_HEIGHT == 16 / 9
    assert "aspect-ratio: 16 / 9;" in css


def test_stable_capture_stops_once_two_frames_match() -> None:
    renderer = _load_renderer()
    frames = iter([b"loading", b"half", b"done", b"done", b"never reached"])
    waits = []

    result = renderer.wait_until_stable(lambda: next(frames), lambda: waits.append(1))

    assert result == b"done"
    assert len(waits) == 3


def test_stable_capture_gives_up_on_a_chart_that_keeps_changing() -> None:
    renderer = _load_renderer()
    frames = iter([b"a", b"b", b"c", b"d"])

    result = renderer.wait_until_stable(lambda: next(frames), lambda: None, attempts=3)

    assert result == b"c"


def test_stable_capture_rejects_a_zero_attempt_budget() -> None:
    renderer = _load_renderer()

    with pytest.raises(ValueError, match="at least one"):
        renderer.wait_until_stable(lambda: b"", lambda: None, attempts=0)


@pytest.mark.parametrize(
    "message",
    [
        "Error: invalid specification",
        "Loading failed: Error: invalid specification",
    ],
)
def test_runtime_error_detection_handles_delayed_genomespy_failures(
    message: str,
) -> None:
    renderer = _load_renderer()

    assert renderer.has_runtime_error(message)
    assert not renderer.has_runtime_error("minMapq\n0\nminBaseQuality\n0")
