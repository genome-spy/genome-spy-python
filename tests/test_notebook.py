from __future__ import annotations

import importlib.util
import sys
from pathlib import Path
from types import ModuleType

import pytest


def test_alphagenome_pytorch_notebook_opens_designer_without_loading_model(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    definitions = _run_notebook(monkeypatch)

    assert "alphagenome_pytorch" not in sys.modules
    assert definitions["reference_asset"]["provenance"]["assembly"] == "GRCh38"
    assert definitions["view"].dataset_names == (
        "designer",
        "edits",
        "sequence_summary",
        "genes",
        "selected_site",
        "predictions",
    )
    assert definitions["designer_rows"].height == definitions["display_interval"].width
    assert definitions["sequence_summary_rows"].height == 256
    assert definitions["gene_rows"].filter(
        definitions["gene_rows"]["feature"] == "transcript"
    )["gene"].to_list() == ["TAL1", "STIL"]
    source = Path("notebooks/alphagenome/genome_spy_alphagenome_pytorch.py").read_text(
        encoding="utf-8"
    )
    assert 'view.set_dataset("predictions",' in source
    assert "mo.ui.run_button" not in source
    assert "mo.ui.radio" not in source
    assert "mo.ui.dropdown" not in source
    assert "mo.ui.text" not in source


def test_alphagenome_pytorch_tracks_share_zoom_and_expose_designer(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    definitions = _run_notebook(monkeypatch)

    spec = definitions["view"].spec
    reference_sequence = spec["vconcat"][0]
    designer_group = spec["vconcat"][1]
    genes = spec["vconcat"][2]
    prediction_tracks = spec["vconcat"][3]
    assay_panels = prediction_tracks["vconcat"]
    panels = [panel for assay in assay_panels for panel in assay["vconcat"]]

    assert spec["scales"]["x"] == {
        "domain": [
            {"chrom": "chr1", "pos": definitions["tal1_pos0"] - 4},
            {"chrom": "chr1", "pos": definitions["tal1_pos0"] + 4},
        ],
        "zoom": {
            "extent": [
                {"chrom": "chr1", "pos": definitions["display_interval"].start},
                {"chrom": "chr1", "pos": definitions["display_interval"].end},
            ]
        },
    }
    assert spec["assembly"] == "hg38"
    assert spec["resolve"] == {"scale": {"x": "shared"}}
    assert reference_sequence["title"] == "hg38 reference sequence"
    assert reference_sequence["layer"][0]["data"] == {"name": "sequence_summary"}
    assert reference_sequence["layer"][0]["opacity"] == {
        "unitsPerPixel": [20, 5],
        "values": [1, 0],
    }
    reference_bases = reference_sequence["layer"][1]
    assert reference_bases["data"] == {"name": "designer"}
    assert reference_bases["layer"][1]["encoding"]["text"]["field"] == "reference"
    assert designer_group["title"].startswith("Allele designer")
    designer = designer_group["layer"][0]
    assert designer["data"] == {"name": "designer"}
    assert designer["transform"] == [
        {"type": "flatten", "fields": ["alleles"], "as": ["allele"]}
    ]
    assert "scale" not in designer["encoding"]["x"]
    assert designer["encoding"]["y"]["scale"]["domain"] == ["A", "C", "G", "T"]
    assert designer["layer"][1]["mark"]["type"] == "text"
    assert designer["layer"][1]["encoding"]["text"]["field"] == "allele"
    assert designer_group["opacity"] == {
        "unitsPerPixel": [20, 5],
        "values": [0, 1],
    }
    reference_tiles = designer_group["layer"][1]
    assert [layer["data"] for layer in reference_tiles["layer"]] == [
        {"name": "designer"},
        {"name": "designer"},
    ]
    assert reference_tiles["layer"][0]["encoding"]["y"]["field"] == "reference"
    assert reference_tiles["layer"][1]["mark"]["type"] == "text"
    assert reference_tiles["layer"][1]["encoding"]["text"]["field"] == "reference"
    edited_tiles = designer_group["layer"][2]
    assert [layer["data"] for layer in edited_tiles["layer"]] == [
        {"name": "edits"},
        {"name": "edits"},
        {"name": "edits"},
        {"name": "edits"},
    ]
    assert edited_tiles["layer"][0]["encoding"]["y"]["field"] == "reference"
    assert edited_tiles["layer"][1]["encoding"]["text"]["field"] == "reference"
    assert edited_tiles["layer"][2]["encoding"]["y"]["field"] == "alternate"
    assert edited_tiles["layer"][3]["encoding"]["text"]["field"] == "alternate"
    assert "params" not in spec
    assert genes["title"] == "NCBI RefSeq genes (hg38)"
    assert [layer["mark"]["type"] for layer in genes["layer"]] == [
        "rule",
        "rect",
        "text",
        "rule",
    ]
    assert len(assay_panels) == 4
    assert all(len(assay["vconcat"]) == 2 for assay in assay_panels)
    assert all(assay["resolve"]["axis"]["x"] == "shared" for assay in assay_panels)
    assert len(panels) == 8
    assert all(panel["layer"][0]["mark"]["type"] == "rect" for panel in panels)
    assert all(panel["layer"][0]["encoding"]["y2"] == {"datum": 0} for panel in panels)
    assert all(
        assay["vconcat"][0]["layer"][0]["encoding"]["x"]["axis"] is None
        for assay in assay_panels
    )
    assert all(
        assay["vconcat"][1]["layer"][0]["encoding"]["x"]["axis"] == {"title": None}
        for assay in assay_panels
    )
    assert all(
        panels[index]["layer"][0]["encoding"]["y"]["field"] == "delta"
        for index in range(1, 8, 2)
    )
    assert all(
        panels[index]["layer"][0]["encoding"]["y"]["scale"] == {"zero": True}
        for index in range(1, 8, 2)
    )
    assert {item["field"] for item in panels[0]["layer"][0]["encoding"]["tooltip"]} >= {
        "chrom",
        "start0",
        "end0",
        "output_type",
        "track_name",
        "biosample_name",
        "ontology_curie",
        "reference",
        "alternate",
        "delta",
    }


def test_alphagenome_pytorch_allele_click_builds_multi_edit_submission(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    definitions = _run_notebook(monkeypatch)
    clicked = {
        "interaction_kind": "allele_choice",
        "chrom": "chr1",
        "pos0": 10,
        "pos1": 11,
        "reference": "C",
        "allele": "T",
    }

    first = definitions["allele_click_submission"](clicked, 4, ())
    assert first == {
        "click_revision": 4,
        "variants": (
            {
                "chrom": "chr1",
                "pos0": 10,
                "pos1": 11,
                "reference": "C",
                "alternate": "T",
            },
        ),
    }
    second = definitions["allele_click_submission"](
        {
            "interaction_kind": "allele_choice",
            "chrom": "chr1",
            "pos0": 12,
            "pos1": 13,
            "reference": "A",
            "allele": "G",
        },
        5,
        first["variants"],
    )
    assert [variant["pos0"] for variant in second["variants"]] == [10, 12]
    restored = definitions["allele_click_submission"](
        {**clicked, "allele": "C"}, 6, second["variants"]
    )
    assert [variant["pos0"] for variant in restored["variants"]] == [12]
    assert definitions["allele_click_submission"]({}, 7, ()) is None
    prediction = {"click_revision": 4}
    assert definitions["should_run_submission"](first, prediction) is False
    assert (
        definitions["should_run_submission"]({**first, "click_revision": 5}, prediction)
        is True
    )
    assert (
        definitions["should_run_submission"](
            {"click_revision": 5, "variants": ()}, prediction
        )
        is False
    )
    assert definitions["should_run_submission"](None, prediction) is False


def test_alphagenome_pytorch_prediction_state_reports_stale_and_failed_inputs(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    definitions = _run_notebook(monkeypatch)
    variants = (
        {
            "chrom": "chr1",
            "pos1": 11,
            "reference": "C",
            "alternate": "T",
        },
    )
    pending = definitions["prediction_input_key"](variants, "", "cuda", "auto")
    changed_pending = definitions["prediction_input_key"](
        ({**variants[0], "alternate": "A"},), "", "cuda", "auto"
    )
    succeeded = {
        "status": "succeeded",
        "message": "done",
        "frame": object(),
        "input_key": pending,
    }
    failed = {
        **succeeded,
        "status": "failed",
        "message": "CUDA out of memory",
    }

    assert definitions["prediction_display_state"](succeeded, pending) == (
        "succeeded",
        "done",
    )
    assert (
        definitions["prediction_display_state"](succeeded, changed_pending)[0]
        == "stale"
    )
    assert definitions["prediction_display_state"](failed, changed_pending) == (
        "failed",
        "CUDA out of memory",
    )


def _run_notebook(monkeypatch: pytest.MonkeyPatch):
    monkeypatch.syspath_prepend("notebooks/alphagenome")
    sys.modules.pop("alphagenome_pytorch", None)
    module = _load_python_module(
        Path("notebooks/alphagenome/genome_spy_alphagenome_pytorch.py")
    )
    outputs, definitions = module.app.run()
    assert any(output is not None for output in outputs)
    return definitions


def _load_python_module(path: Path) -> ModuleType:
    module_spec = importlib.util.spec_from_file_location(path.stem, path)
    if module_spec is None or module_spec.loader is None:
        raise RuntimeError(f"Could not load notebook module from {path}.")
    module = importlib.util.module_from_spec(module_spec)
    module_spec.loader.exec_module(module)
    return module
