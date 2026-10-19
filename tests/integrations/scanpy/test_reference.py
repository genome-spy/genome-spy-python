"""Tracked Scanpy contracts and image metadata; images are generated temporarily."""

from hashlib import sha256
import json
from pathlib import Path
import re

import pytest

FIXTURES = Path(__file__).with_name("fixtures")


def test_reference_inventory_matches_the_installed_public_api() -> None:
    sc = pytest.importorskip("scanpy")
    from tests.integrations.scanpy.generate_references import api_contract

    assert api_contract(sc) == json.loads((FIXTURES / "api.json").read_text())


def test_reference_image_inventory_and_checksums_are_recorded() -> None:
    manifest = json.loads((FIXTURES / "umap.json").read_text())
    expected = {f"{case}.png" for case in manifest["cases"]}
    expected.update(
        f"{case}-panel-{index}.png"
        for case, details in manifest["cases"].items()
        for index in range(len(details["panels"]))
    )
    expected.update(
        f"footprint-{marker}.png" for marker in ("dot", "circle", "dot-stroke")
    )
    assert set(manifest["assets"]) == expected
    assert all(
        re.fullmatch(r"[0-9a-f]{64}", digest) for digest in manifest["assets"].values()
    )


def test_reference_input_has_not_changed_without_regeneration():
    manifest = json.loads((FIXTURES / "umap.json").read_text())
    assert (
        sha256(Path(__file__).with_name("fixture_data.py").read_bytes()).hexdigest()
        == manifest["fixture_sha256"]
    )
