"""Preserve the upstream PISA coordinate and interaction contracts."""

from pathlib import Path
import runpy

import pytest

import genome_spy as gs

pytestmark = pytest.mark.docs
EXAMPLES = Path(__file__).resolve().parents[1] / "docs" / "examples"


def test_squid_projects_brushes_and_reuses_one_highlight_predicate() -> None:
    example = runpy.run_path(str(EXAMPLES / "pisa_squid.py"))
    assert isinstance(example["highlighted_link"], gs.SelectionPredicateDefinition)
    assert isinstance(example["output_endpoint"], gs.SelectionPredicateOperand)
    assert isinstance(example["input_endpoint"], gs.SelectionPredicateOperand)
    spec = example["chart"].to_dict()
    prediction, middle, importance = spec["vconcat"]
    links, motifs = middle["layer"]
    assert spec["scales"]["x"] == {"domain": [15646649, 15647250], "zoom": True}
    assert spec["resolve"]["scale"]["x"] == "shared"
    for track, name in [
        (prediction, "accessibilityRegion"),
        (importance, "contributionRegion"),
    ]:
        selection = track["params"][0]
        assert selection["name"] == name
        assert selection["push"] == "outer"
        assert selection["select"]["encodings"] == ["x"]
        assert selection["select"]["zoom"] is False
    for channel in ["color", "opacity", "order"]:
        assert links["encoding"][channel]["condition"]["test"] == {
            "ref": "highlightedLink"
        }
    hovered, brushed = links["predicates"]["highlightedLink"]["or"]
    assert hovered == {"param": "pisaLinkHover", "empty": False}
    assert brushed["and"][:2] == [
        {"param": "accessibilityRegion", "project": {"x": "x2"}},
        {"param": "contributionRegion", "project": {"x": "x"}},
    ]
    assert brushed["and"][2]["or"] == [
        {"param": "pisaLinkHover"},
        {"param": "accessibilityRegion", "project": {"x": "x2"}, "empty": False},
        {"param": "contributionRegion", "project": {"x": "x"}, "empty": False},
    ]
    assert links["data"]["url"].endswith("/v3/fig2c-atac-links.parquet")
    assert motifs["encoding"]["y2"] == {"value": {"expr": "(20 / height)"}}
    assert importance["stops"]["values"] == [0.15]


def test_matrix_aligns_margin_tracks_and_limits_label_materialization() -> None:
    spec = runpy.run_path(str(EXAMPLES / "pisa_interaction_matrix.py"))[
        "chart"
    ].to_dict()
    matrix, accessibility, contribution = spec["concat"]
    assert spec["columns"] == 2
    assert spec["scales"]["y"] == {
        "type": "index",
        "domain": [15646499, 15647400],
        "reverse": True,
    }
    assert accessibility["resolve"]["scale"]["x"] == "excluded"
    assert contribution["resolve"]["scale"]["y"] == "excluded"
    assert matrix["data"]["url"].endswith("/v3/fig2d-atac-matrix.parquet")
    params = {parameter["name"]: parameter for parameter in matrix["params"]}
    assert params["matrixCursor"]["ruler"]["encodings"] == ["x", "y"]
    assert params["matrixCursor"]["ruler"]["mark"]["opacity"] == {
        "expr": "rulerOpacity"
    }
    assert params["labelXBinSize"]["value"] == 10
    assert params["labelYBinSize"]["value"] == 15
    labels = matrix["layer"][2]
    assert labels["transform"] == [
        {"type": "collect"},
        {
            "type": "filter",
            "expr": "((((showCellLabels && (datum.input >= labelXStart)) && (datum.input < labelXEnd)) && (datum.output >= labelYStart)) && (datum.output < labelYEnd))",
        },
    ]
    assert labels["encoding"]["text"]["format"] == ".2f"
    assert {p["name"]: p["expr"] for p in labels["params"]} == {
        f"label{axis}{edge}": (
            f"if(showCellLabels,({rounding}(({extreme}(domain('{axis.lower()}')[0],"
            f"domain('{axis.lower()}')[1]) / label{axis}BinSize)) * label{axis}BinSize),null)"
        )
        for axis in ("X", "Y")
        for edge, rounding, extreme in (
            ("Start", "floor", "min"),
            ("End", "ceil", "max"),
        )
    }
    assert contribution["multiscale"][1]["mark"]["logoLetters"] is True
