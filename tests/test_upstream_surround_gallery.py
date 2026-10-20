"""Keep Python authoring equivalent to the published surround examples."""

import json
from pathlib import Path
import runpy
from typing import Any

import pytest

pytestmark = pytest.mark.docs
ROOT = Path(__file__).resolve().parents[1]


def _without_documentation(value: Any) -> Any:
    if isinstance(value, dict):
        return {
            key: _without_documentation(child)
            for key, child in value.items()
            if key not in {"$schema", "description"}
        }
    if isinstance(value, list):
        return [_without_documentation(child) for child in value]
    return value


@pytest.mark.parametrize(
    ("example", "upstream"),
    [
        ("pisa_interaction_matrix", "bpreveal-pisa-matrix"),
        ("upset_mutations", "upsetr-mutations"),
        ("clustered_heatmap", "clustered-heatmap"),
    ],
)
def test_python_reproduces_upstream_surround_spec(example: str, upstream: str) -> None:
    chart = runpy.run_path(str(ROOT / "docs" / "examples" / f"{example}.py"))["chart"]
    reference = json.loads(
        (
            ROOT / "tests" / "fixtures" / "upstream_examples" / f"{upstream}.json"
        ).read_text()
    )
    assert _without_documentation(chart.to_dict()) == _without_documentation(reference)
