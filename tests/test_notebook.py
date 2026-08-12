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
    assert definitions["view"].dataset_names == ("sequence", "predictions")
    assert definitions["sequence_rows"].height == 81
    source = Path("notebooks/alphagenome/genome_spy_alphagenome_pytorch.py").read_text(
        encoding="utf-8"
    )
    assert 'view.set_dataset("predictions",' in source
    assert "accepts SNVs only" in source


def test_alphagenome_pytorch_prediction_tracks_share_zoom_and_expose_context(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.syspath_prepend("notebooks/alphagenome")
    module = _load_python_module(
        Path("notebooks/alphagenome/genome_spy_alphagenome_pytorch.py")
    )
    _, definitions = module.app.run()

    prediction_tracks = definitions["view"].spec["vconcat"][1]
    panels = prediction_tracks["vconcat"]

    assert prediction_tracks["scales"]["x"] == {
        "domain": [
            definitions["display_interval"].start,
            definitions["display_interval"].end,
        ],
        "zoom": True,
    }
    assert len(panels) == 8
    assert all(panel["mark"]["type"] == "rule" for panel in panels)
    assert all(
        panels[index]["encoding"]["y"]["field"] == "delta" for index in range(1, 8, 2)
    )
    assert all(
        panels[index]["encoding"]["y"]["scale"] == {"zero": True}
        for index in range(1, 8, 2)
    )
    assert {item["field"] for item in panels[0]["encoding"]["tooltip"]} >= {
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


def test_alphagenome_pytorch_prediction_state_avoids_redundant_dataset_updates(
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
        "request_id": "request-1",
        "variant_key": "chr1:47239296:C:T",
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
    assert definitions["should_apply_prediction"](succeeded, None) is True
    assert definitions["should_apply_prediction"](succeeded, "request-1") is False
    assert definitions["should_apply_prediction"](failed, "request-1") is False


def _load_python_module(path: Path) -> ModuleType:
    module_spec = importlib.util.spec_from_file_location(path.stem, path)
    if module_spec is None or module_spec.loader is None:
        raise RuntimeError(f"Could not load notebook module from {path}.")
    module = importlib.util.module_from_spec(module_spec)
    module_spec.loader.exec_module(module)
    return module
