"""Check scientific meaning and coordinate consistency of the new gallery data."""

from collections import Counter
from pathlib import Path
import runpy

import pytest

from genome_spy.datasets import load_dataset


def test_laml_joins_and_summaries() -> None:
    data = load_dataset("tcga_laml_combined_oncoplot")
    assert len(data["samples"]) == 200
    assert data["sample_domain"] == [0, 199]
    assert len(data["gene_order"]) == 18
    assert len({row["pathway"] for row in data["genes"]}) == 5
    genes = {row["gene"]: row for row in data["genes"]}
    # Values printed in the maftools vignette, independently of our preparation.
    assert genes["DNMT3A"]["vaf"] == pytest.approx(43.51556, abs=1e-5)
    assert genes["FLT3"]["neglog_q"] == pytest.approx(12.64176, abs=1e-5)
    assert any(
        row["gene"] == "TP53" and row["class"] == "Del" for row in data["copy_number"]
    )
    order = {row["sample"]: row["sample_order"] for row in data["samples"]}
    assert sorted(order.values()) == list(range(200))
    for key in ("events", "copy_number", "burden", "spectrum"):
        assert data[key]
        for row in data[key]:
            assert row["sample_order"] == order[row["sample"]]
    assert any(row["alt_c"] for row in data["events"])
    assert any(row["class"] == "Multi_Hit" for row in data["events"])
    assert {"Amp", "Del"} <= {row["class"] for row in data["burden"]}
    assert "Silent" not in {row["class"] for row in data["burden"]}
    assert data["burden_limit"] == 1894
    assert data["altered_samples"] == 159
    assert set(row["FAB_classification"] for row in data["samples"]) == {
        "M0",
        "M1",
        "M2",
        "M3",
        "M4",
        "M5",
        "M6",
        "M7",
        "Unknown",
    }
    totals: Counter[str] = Counter()
    for row in data["spectrum"]:
        totals[row["sample"]] += row["percent"]
    assert all(value == pytest.approx(100) for value in totals.values())


def test_laml_pathway_rows_summarize_member_genes() -> None:
    data = load_dataset("tcga_laml_combined_oncoplot")
    assert len(data["matrix_rows"]) == 23
    assert [row["row"] for row in data["matrix_rows"]] == list(range(23))
    assert [row["pathway"] for row in data["pathway_bounds"]] == [
        "Signalling",
        "DNAm",
        "ChromMod",
        "TSG",
        "TFs",
    ]
    for bound in data["pathway_bounds"]:
        pathway = bound["pathway"]
        members = {row["gene"] for row in data["genes"] if row["pathway"] == pathway}
        expected = {
            row["sample"]
            for key in ("events", "copy_number")
            for row in data[key]
            if row["gene"] in members
        }
        actual = {
            row["sample"] for row in data["pathway_events"] if row["gene"] == pathway
        }
        assert actual == expected
        summary = next(row for row in data["matrix_rows"] if row["gene"] == pathway)
        assert summary["altered_percent"] == 100 * len(expected) / 200
    totals: Counter[str] = Counter()
    for row in data["burden"]:
        totals[row["sample"]] += row["count"]
    assert max(totals.values()) == 1894


def test_laml_layout_keeps_rows_fixed_and_sample_column_responsive() -> None:
    example = runpy.run_path(
        str(
            Path(__file__).resolve().parents[1]
            / "docs/examples/combined_laml_oncoplot.py"
        )
    )
    spec = example["chart"].to_dict()
    assert example["row_scale"].to_dict()["zoom"] is False
    assert example["row_scale"].to_dict()["domain"] == [0, 22]
    column = spec["hconcat"][1]
    assert column["vconcat"][1]["layer"][0]["encoding"]["y"]["scale"] == {
        "name": "genes",
        "domain": [0, 22],
        "reverse": True,
        "padding": 0,
        "zoom": False,
    }
    assert column["width"] == {"grow": 1}
    assert column["scales"]["x"]["domain"] == [0, 199]
    assert column["scales"]["x"]["zoom"] is True
    assert column["resolve"]["scale"]["x"] == "shared"
    panels = spec
    assert panels["resolve"]["scale"]["y"] == "shared"
    assert all(
        child["resolve"]["scale"]["y"] == "shared" for child in panels["hconcat"]
    )
    assert column["vconcat"][0]["resolve"]["scale"]["y"] == "excluded"
    assert column["vconcat"][0]["height"] == 70
    assert column["vconcat"][-1]["resolve"]["scale"]["y"] == "excluded"
    assert column["vconcat"][-1]["height"] == 130
    left_header = spec["hconcat"][0]["vconcat"][0]["hconcat"]
    right_header = spec["hconcat"][2]["vconcat"][0]["hconcat"]
    assert [child["height"] for child in left_header] == [70, 70]
    assert [child["height"] for child in right_header] == [70, 70]
    assert example["qvalues"].to_dict()["encoding"]["x"]["field"] == "neglog_q"


def test_laml_uses_collected_native_legends_with_local_snv_legend() -> None:
    example = runpy.run_path(
        str(
            Path(__file__).resolve().parents[1]
            / "docs/examples/combined_laml_oncoplot.py"
        )
    )
    spec = example["chart"].to_dict()
    assert spec["resolve"]["legend"] == {"default": "collected"}
    assert spec["config"]["legend"]["orient"] == "bottom"
    assert spec["config"]["legend"]["layout"] == {"right": {"anchor": "end"}}
    column = spec["hconcat"][1]
    assert column["resolve"]["scale"]["color"] == "shared"
    spectrum = column["vconcat"][-1]
    assert spectrum["resolve"]["legend"] == {"default": "excluded"}
    assert spectrum["resolve"]["scale"]["color"] == "excluded"
    assert spectrum["overhang"] == {"left": False, "right": False}
    assert spectrum["layer"][0]["encoding"]["color"]["legend"]["orient"] == "right"
    for track in column["vconcat"][2:4]:
        assert track["resolve"]["scale"]["color"] == "excluded"
        assert track["layer"][0]["encoding"]["color"]["legend"] is not None
    assert "color_key" not in example
    assert "followup_legend" not in example["data"]


def test_laml_decorations_do_not_hide_cell_tooltips() -> None:
    example = runpy.run_path(
        str(
            Path(__file__).resolve().parents[1]
            / "docs/examples/combined_laml_oncoplot.py"
        )
    )
    for name in ("background", "grid", "outlines"):
        assert example[name].to_dict()["mark"]["tooltip"] is None
    for name in ("mutations", "copy_number", "alt_c", "pathway_cells"):
        tooltip = example[name].to_dict()["encoding"]["tooltip"]
        assert {"sample", "gene"} <= {field["field"] for field in tooltip}


def test_laml_grid_uses_sample_edges_and_outlines_stay_inside_view() -> None:
    example = runpy.run_path(
        str(
            Path(__file__).resolve().parents[1]
            / "docs/examples/combined_laml_oncoplot.py"
        )
    )
    grid_x = example["grid"].to_dict()["encoding"]["x"]
    assert grid_x["field"] == "sample_order"
    assert grid_x["type"] == "index"
    assert grid_x["band"] == 0
    outline_mark = example["outlines"].to_dict()["mark"]
    assert outline_mark["xOffset"] == outline_mark["strokeWidth"] / 2
    assert outline_mark["x2Offset"] == -outline_mark["strokeWidth"] / 2


def test_laml_additional_feature_size_tracks_zoom() -> None:
    example = runpy.run_path(
        str(
            Path(__file__).resolve().parents[1]
            / "docs/examples/combined_laml_oncoplot.py"
        )
    )
    mark = example["alt_c"].to_dict()["mark"]
    assert mark["size"] == {"expr": "min((8 * pow(zoomLevel,1.5)),64)"}


def test_p53_residues_padding_and_column_statistics() -> None:
    data = load_dataset("p53_sequence_comparison")
    assert len(data["sequences"]) == 34
    assert data["length"] == 396
    assert len(data["cells"]) == 34 * 396
    assert len(data["columns"]) == 396
    for sequence in data["sequences"]:
        cells = [
            row for row in data["cells"] if row["identifier"] == sequence["identifier"]
        ]
        assert (
            "".join(row["residue"] for row in cells).rstrip("-") == sequence["sequence"]
        )
        assert [row["position"] for row in cells] == list(range(1, 397))
    for column in data["columns"]:
        position = column["position"] - 1
        counts = Counter(
            row["sequence"][position]
            for row in data["sequences"]
            if len(row["sequence"]) > position
        )
        assert column["coverage"] == pytest.approx(sum(counts.values()) / 34)
        assert column["identity"] == pytest.approx(max(counts.values()) / 34)
        assert counts[column["residue"]] == max(counts.values())
    # The incomplete sequences must not be mistaken for biological gap calls.
    assert data["columns"][-1]["coverage"] == pytest.approx(2 / 34)
    assert all("-" not in row["sequence"] for row in data["sequences"])
