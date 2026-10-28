"""Tracked Scanpy contracts and image metadata; images are generated temporarily."""

from hashlib import sha256
import json
from pathlib import Path
import re

import pytest
from packaging.version import Version

FIXTURES = Path(__file__).with_name("fixtures")


def test_reference_inventory_matches_the_installed_public_api() -> None:
    sc = pytest.importorskip("scanpy")
    from tests.integrations.scanpy.generate_references import api_contract

    reference = json.loads((FIXTURES / "api.json").read_text())
    assert reference["scanpy"] == "1.11.5"
    current = api_contract(sc)
    if Version(current["scanpy"]) < Version("1.12"):
        assert current == {**reference, "scanpy": current["scanpy"]}
        return

    # Newer Scanpy keeps these calls behind deprecated forwarding wrappers.
    forwarding = {
        "timeseries",
        "timeseries_subplot",
        "timeseries_as_heatmap",
        "pca_scatter",
    }
    assert reference["entries"].keys() <= current["entries"].keys()
    assert current["entries"].keys() <= reference["entries"].keys() | {"dogplot"}
    for name, entry in reference["entries"].items():
        actual = current["entries"][name]
        assert actual["kind"] == entry["kind"]
        if name in forwarding and actual["parameters"][0]["kind"] == "VAR_POSITIONAL":
            assert [(p["name"], p["kind"]) for p in actual["parameters"]] == [
                ("args", "VAR_POSITIONAL"),
                ("params" if name == "pca_scatter" else "kwargs", "VAR_KEYWORD"),
            ]
            continue
        expected = {p["name"]: p for p in entry["parameters"]}
        parameters = {p["name"]: p for p in actual["parameters"]}
        if name in {"dotplot", "DotPlot"}:
            assert parameters.pop("group_colors") == {
                "name": "group_colors",
                "kind": "KEYWORD_ONLY",
                "default": "None",
            }
        if name == "dpt_groups_pseudotime" and "return_fig" in parameters:
            assert parameters.pop("return_fig") == {
                "name": "return_fig",
                "kind": "KEYWORD_ONLY",
                "default": "False",
            }
        if name == "violin":
            expected["multi_panel"]["default"] = "False"
        assert parameters == expected, name
        positional = {"POSITIONAL_ONLY", "POSITIONAL_OR_KEYWORD"}
        assert [p for p in actual["parameters"] if p["kind"] in positional] == [
            p for p in entry["parameters"] if p["kind"] in positional
        ], name


def test_reference_image_inventory_and_checksums_are_recorded() -> None:
    manifest = json.loads((FIXTURES / "umap.json").read_text())
    expected = {f"{case}.png" for case in manifest["cases"]}
    expected.update(
        f"{case}-panel-{index}.png"
        for case, details in manifest["cases"].items()
        for index in range(len(details["panels"]))
    )
    expected.update(
        f"footprint-{marker}.png"
        for marker in (
            "dot",
            "circle",
            "dot-stroke",
            "square",
            "square-stroke",
            "diamond",
            "diamond-stroke",
        )
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
