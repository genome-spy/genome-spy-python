"""Check notebook coordinate handling and selection semantics."""

import ast
import json
from pathlib import Path

import pandas as pd
import pytest


NOTEBOOKS = Path(__file__).parents[1] / "notebooks"


def test_annotation_track_is_one_fixed_row_without_scrolling():
    notebook = json.loads((NOTEBOOKS / "annotate_genomic_intervals.ipynb").read_text())
    cell = next(
        cell
        for cell in notebook["cells"]
        if "workflow-chart" in cell.get("metadata", {}).get("tags", [])
    )
    namespace = {}
    exec("".join(cell["source"]), namespace)
    track = namespace["chart"].to_dict()["vconcat"][-1]
    assert track["height"] == 26
    assert "viewportHeight" not in track
    assert all("y" not in layer["encoding"] for layer in track["layer"])


def test_one_hot_edit_changes_only_one_column():
    reference = "ACGT"
    one_hot = notebook_function(
        "edit_sequence", "one_hot", REFERENCE=reference, BASES=list("ACGT")
    )
    rows = one_hot("CCGT")
    for position in range(1, 5):
        column = [row for row in rows if row["position"] == position]
        assert len(column) == 4
        assert sum(row["value"] for row in column) == 1
        assert {row["changed"] for row in column} == {position == 1}
    assert [row["base"] for row in rows if row["value"]] == list("CCGT")


def test_sequence_grid_shows_letters_with_consistent_nucleotide_colors():
    notebook = json.loads((NOTEBOOKS / "edit_sequence.ipynb").read_text())
    cell = next(
        cell
        for cell in notebook["cells"]
        if "workflow-chart" in cell.get("metadata", {}).get("tags", [])
    )
    namespace = {}
    exec("".join(cell["source"]), namespace)
    reference, edited, grid = namespace["chart"].to_dict()["vconcat"]
    assert edited["encoding"]["color"] == reference["encoding"]["color"]
    letters = grid["layer"][1]["encoding"]
    assert letters["text"]["field"] == "base"
    assert (
        letters["color"]["scale"]["range"][:4]
        == reference["encoding"]["color"]["scale"]["range"]
    )
    assert letters["color"]["scale"]["range"][-1] == "#c5cad0"
    assert grid["resolve"]["scale"]["color"] == "independent"


def notebook_function(notebook, name, **namespace):
    cells = json.loads((NOTEBOOKS / f"{notebook}.ipynb").read_text())["cells"]
    source = "\n".join(
        "".join(cell["source"]) for cell in cells if cell["cell_type"] == "code"
    )
    function = next(
        node
        for node in ast.parse(source).body
        if isinstance(node, ast.FunctionDef) and node.name == name
    )
    exec(
        compile(ast.Module(body=[function], type_ignores=[]), notebook, "exec"),
        namespace,
    )
    return namespace[name]


def test_bed_preserves_zero_based_half_open_endpoints():
    convert = notebook_function("annotate_genomic_intervals", "bed_interval")
    snapshot = {
        "active": True,
        "complexIntervals": {
            "x": [{"chrom": "chr5", "pos": 0}, {"chrom": "chr5", "pos": 20}]
        },
    }
    assert convert(snapshot) == {"chrom": "chr5", "start": 0, "end": 20}


@pytest.mark.parametrize(
    "left,right,message",
    [
        ({"chrom": "chr5", "pos": 10}, {"chrom": "chr6", "pos": 20}, "one chromosome"),
        ({"chrom": "chr5", "pos": 10}, {"chrom": "chr5", "pos": 10}, "one whole base"),
        ({"chrom": "chr5", "pos": -1}, {"chrom": "chr5", "pos": 20}, "one whole base"),
    ],
)
def test_bed_rejects_invalid_regions(left, right, message):
    convert = notebook_function("annotate_genomic_intervals", "bed_interval")
    with pytest.raises(ValueError, match=message):
        convert({"active": True, "complexIntervals": {"x": [left, right]}})


def test_bed_rejects_cleared_brush():
    convert = notebook_function("annotate_genomic_intervals", "bed_interval")
    with pytest.raises(ValueError, match="Brush a region"):
        convert({"active": False, "complexIntervals": {"x": None}})


def test_gene_selection_uses_both_plotted_coordinates_and_keeps_identifiers():
    genes = pd.DataFrame(
        {
            "ensgene": ["left", "inside", "above", "clipped"],
            "log2fc": [-1, 1, 1, 1],
            "neglog10_pvalue_plot": [2, 2, 4, 2],
            "neglog10_pvalue": [2, 2, 4, 300],
        }
    )
    select = notebook_function("select_genes", "select_rows", genes=genes)
    result = select({"active": True, "intervals": {"x": [0, 2], "y": [3, 1]}})
    assert result.ensgene.tolist() == ["inside", "clipped"]
    assert select({"active": False, "intervals": {"x": None, "y": None}}).empty
    assert len(genes) == 4
