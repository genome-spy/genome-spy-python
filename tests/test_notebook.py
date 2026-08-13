from __future__ import annotations

import importlib.util
import sys
from pathlib import Path
from types import ModuleType

import pytest


def test_alphagenome_pytorch_notebook_opens_real_editor_without_loading_model(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.syspath_prepend("notebooks/alphagenome")
    sys.modules.pop("alphagenome_pytorch", None)
    module = _load_python_module(
        Path("notebooks/alphagenome/genome_spy_alphagenome_pytorch.py")
    )

    outputs, definitions = module.app.run()

    assert any(output is not None for output in outputs)
    assert "alphagenome_pytorch" not in sys.modules
    assert definitions["reference_asset"]["provenance"]["assembly"] == "GRCh38"
    assert definitions["view"].dataset_names == (
        "sequence",
        "sequence_summary",
        "genes",
        "selected_site",
        "predictions",
    )
    assert definitions["sequence_rows"].height == definitions["display_interval"].width
    assert definitions["sequence_summary_rows"].height == 256
    assert definitions["gene_rows"].filter(
        definitions["gene_rows"]["feature"] == "transcript"
    )["gene"].to_list() == ["TAL1", "STIL"]
    assert (
        definitions["default_selection"]["pos0"] - definitions["display_interval"].start
    ) % definitions["DEFAULT_RESOLUTION"] == 0
    source = Path("notebooks/alphagenome/genome_spy_alphagenome_pytorch.py").read_text(
        encoding="utf-8"
    )
    assert 'view.set_dataset("predictions",' in source
    assert "accepts SNVs only" in source
    assert "mo.ui.run_button" not in source


def test_alphagenome_pytorch_prediction_tracks_share_zoom_and_expose_context(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.syspath_prepend("notebooks/alphagenome")
    module = _load_python_module(
        Path("notebooks/alphagenome/genome_spy_alphagenome_pytorch.py")
    )
    _, definitions = module.app.run()

    spec = definitions["view"].spec
    sequence = spec["vconcat"][0]
    genes = spec["vconcat"][1]
    prediction_tracks = spec["vconcat"][2]
    panels = prediction_tracks["vconcat"]

    assert spec["scales"]["x"] == {
        "domain": [
            definitions["display_interval"].start,
            definitions["display_interval"].end,
        ],
        "zoom": True,
    }
    assert spec["resolve"] == {"scale": {"x": "shared"}}
    assert sequence["layer"][0]["data"] == {"name": "sequence_summary"}
    assert sequence["layer"][0]["opacity"] == {
        "unitsPerPixel": [40, 8],
        "values": [1, 0],
    }
    sequence_bases = sequence["layer"][1]
    assert "scale" not in sequence_bases["encoding"]["x"]
    assert sequence_bases["layer"][2]["mark"]["type"] == "text"
    assert sequence_bases["layer"][2]["encoding"]["text"]["field"] == "base"
    assert sequence_bases["layer"][2]["opacity"] == {
        "unitsPerPixel": [100, 10],
        "values": [0, 1],
    }
    assert genes["title"] == "NCBI RefSeq genes (hg38)"
    assert [layer["mark"]["type"] for layer in genes["layer"]] == [
        "rule",
        "rect",
        "text",
        "rule",
    ]
    assert len(panels) == 8
    assert all(panel["layer"][0]["mark"]["type"] == "rect" for panel in panels)
    assert all(panel["layer"][0]["encoding"]["y2"] == {"datum": 0} for panel in panels)
    assert all(
        panel["layer"][1]["encoding"]["x"]
        == {"field": "pos0", "type": "quantitative", "title": None}
        for panel in panels
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


def test_alphagenome_pytorch_sequence_click_builds_one_prediction_submission(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.syspath_prepend("notebooks/alphagenome")
    module = _load_python_module(
        Path("notebooks/alphagenome/genome_spy_alphagenome_pytorch.py")
    )
    _, definitions = module.app.run()
    clicked = {
        "interaction_kind": "sequence_base",
        "chrom": "chr1",
        "pos0": 10,
        "pos1": 11,
        "base": "C",
    }

    assert definitions["sequence_click_submission"](clicked, 4, "T") == {
        "click_revision": 4,
        "selection": {
            "chrom": "chr1",
            "pos0": 10,
            "pos1": 11,
            "base": "C",
        },
        "alternate": "T",
    }
    assert definitions["alternate_options"]("C") == ("A", "G", "T")
    assert definitions["sequence_click_submission"](clicked, 5, "C")["alternate"] == "A"
    assert definitions["sequence_click_submission"]({}, 6, "T") is None
    prediction = {"click_revision": 4}
    submission = definitions["sequence_click_submission"](clicked, 4, "T")
    assert definitions["should_run_submission"](submission, prediction) is False
    assert (
        definitions["should_run_submission"](
            {**submission, "click_revision": 5}, prediction
        )
        is True
    )
    assert definitions["should_run_submission"](None, prediction) is False


def test_alphagenome_pytorch_prediction_state_reports_stale_and_failed_inputs(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.syspath_prepend("notebooks/alphagenome")
    module = _load_python_module(
        Path("notebooks/alphagenome/genome_spy_alphagenome_pytorch.py")
    )
    _, definitions = module.app.run()

    pending = definitions["prediction_input_key"](
        definitions["default_selection"],
        "T",
        "",
        "cuda",
        "auto",
    )
    changed_pending = definitions["prediction_input_key"](
        definitions["default_selection"],
        "A",
        "",
        "cuda",
        "auto",
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


def _load_python_module(path: Path) -> ModuleType:
    module_spec = importlib.util.spec_from_file_location(path.stem, path)
    if module_spec is None or module_spec.loader is None:
        raise RuntimeError(f"Could not load notebook module from {path}.")
    module = importlib.util.module_from_spec(module_spec)
    module_spec.loader.exec_module(module)
    return module
