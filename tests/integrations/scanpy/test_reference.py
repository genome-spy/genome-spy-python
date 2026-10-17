"""Tracked public-API and synthetic-image oracles for Scanpy 1.11.5."""

from hashlib import sha256
import json
from pathlib import Path

import pytest

FIXTURES = Path(__file__).with_name("fixtures")


def test_reference_inventory_matches_the_installed_public_api() -> None:
    sc = pytest.importorskip("scanpy")
    from tests.integrations.scanpy.generate_references import api_contract

    assert api_contract(sc) == json.loads((FIXTURES / "api.json").read_text())


def test_reference_assets_have_recorded_checksums() -> None:
    manifest = json.loads((FIXTURES / "umap.json").read_text())
    for name, expected in manifest["assets"].items():
        assert sha256((FIXTURES / name).read_bytes()).hexdigest() == expected


def test_reference_input_has_not_changed_without_regeneration():
    manifest = json.loads((FIXTURES / "umap.json").read_text())
    assert (
        sha256(Path(__file__).with_name("fixture_data.py").read_bytes()).hexdigest()
        == manifest["fixture_sha256"]
    )
