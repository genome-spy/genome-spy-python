"""Regression tests for the RNF7 direct-RNA gallery example."""

from __future__ import annotations

import json
from pathlib import Path

from tools.docs_gallery import collect_example


def test_rnf7_gallery_spec_contains_only_strict_json_values() -> None:
    """Reject pandas NaN values before the gallery writes its JSON spec."""
    root = Path(__file__).resolve().parents[1]
    example = collect_example(root / "docs/examples/rnf7_direct_rna.py")

    json.dumps(example.spec, allow_nan=False)


def test_rnf7_lane_height_uses_a_smooth_transition() -> None:
    """Keep slider-driven pileup resizing animated rather than abrupt."""
    root = Path(__file__).resolve().parents[1]
    example = collect_example(root / "docs/examples/rnf7_direct_rna.py")
    lane_height = next(
        param for param in example.spec["params"] if param["name"] == "laneHeight"
    )

    assert lane_height["transition"] == {
        "type": "lerp",
        "halfLife": 30,
        "epsilon": 0.02,
    }


def test_rnf7_chart_aligns_condition_level_m6a_sites_with_reads() -> None:
    """Show paired m6Anet scores without presenting them as per-read calls."""
    root = Path(__file__).resolve().parents[1]
    example = collect_example(root / "docs/examples/rnf7_direct_rna.py")
    detail_tracks = example.spec["vconcat"][0]["vconcat"]
    m6a_track = next(
        track
        for track in detail_tracks
        if track.get("name") == "reference-sequence-m6a"
    )

    assert len(example.spec["datasets"]["sites"]) == 24
    _, _, wild_type_sites, knockout_sites = m6a_track["layer"]
    assert wild_type_sites["mark"] == {
        "type": "point",
        "clip": "x",
        "color": "#6656c7",
        "filled": True,
        "shape": "triangle-down",
        "stroke": "white",
        "strokeWidth": 0.8,
        "y": 0.12,
    }
    assert knockout_sites["mark"]["shape"] == "triangle-up"
    assert knockout_sites["mark"]["y"] == 0.88
    assert wild_type_sites["encoding"]["size"]["field"] == "probability"


def test_rnf7_combines_coverage_and_keeps_one_footer_legend() -> None:
    """Overlay translucent coverage bars and collect condition labels at the bottom."""
    root = Path(__file__).resolve().parents[1]
    example = collect_example(root / "docs/examples/rnf7_direct_rna.py")
    coverage = example.spec["vconcat"][0]["vconcat"][0]

    knockout, wild_type = coverage["layer"]
    assert knockout["encoding"]["x"]["type"] == "index"
    assert knockout["encoding"]["y"]["field"] == "coverage"
    assert knockout["encoding"]["y"]["scale"]["domain"] == [0, 160]
    assert knockout["mark"]["type"] == "rect"
    assert knockout["mark"]["opacity"] == 0.5
    assert wild_type["mark"]["type"] == "rect"
    assert wild_type["mark"]["opacity"] == 0.5
    assert (
        example.spec["vconcat"][1]["vconcat"][0]["layer"][0]["encoding"]["x"]["type"]
        == "index"
    )

    legends: list[dict[str, object]] = []

    def collect_legends(value: object) -> None:
        if isinstance(value, dict):
            for key, child in value.items():
                if key == "legend" and isinstance(child, dict):
                    legends.append(child)
                else:
                    collect_legends(child)
        elif isinstance(value, list):
            for child in value:
                collect_legends(child)

    collect_legends(example.spec)
    assert legends == [{"direction": "horizontal", "orient": "bottom", "title": None}]


def test_rnf7_deletions_align_to_index_boundaries() -> None:
    """Keep deletion intervals fixed to read coordinates on the index scale."""
    root = Path(__file__).resolve().parents[1]
    example = collect_example(root / "docs/examples/rnf7_direct_rna.py")
    wild_type_reads = example.spec["vconcat"][0]["vconcat"][3]
    deletions = wild_type_reads["layer"][1]

    assert deletions["encoding"]["x"]["band"] == 0
    assert deletions["encoding"]["x2"]["band"] == 0
