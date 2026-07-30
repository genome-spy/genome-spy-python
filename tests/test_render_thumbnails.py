from __future__ import annotations

import importlib.util
import sys
from pathlib import Path


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

    assert layout.stage_width == 760
    assert layout.min_stage_height == 660


def test_thumbnail_layout_defaults_to_card_width() -> None:
    renderer = _load_renderer()
    example = type("Example", (), {"height": 320, "max_width": None})()

    layout = renderer.thumbnail_layout(example)

    assert layout.stage_width == renderer.CARD_WIDTH
    assert layout.min_stage_height == 320


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
