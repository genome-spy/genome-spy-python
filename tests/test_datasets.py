"""Tests for the packaged dataset loader."""

from __future__ import annotations

import pytest

from genome_spy.datasets import DatasetNotFoundError, available_datasets, load_dataset
from genome_spy.datasets._airway import airway_paired_logcounts


def test_available_datasets_are_stable() -> None:
    assert available_datasets() == (
        "airway_metadata",
        "airway_scaledcounts",
        "dnmt3a_lollipop",
        "hapmap_gwas",
        "pik3ca_mutations",
        "tcga_laml_oncoprint",
        "tcga_oncoprint",
    )


def test_load_tabular_dataset_as_dataframe() -> None:
    data = load_dataset("hapmap_gwas", as_format="dataframe")

    assert list(data.columns[:4]) == ["CHR", "BP", "P", "SNP"]
    assert not data.empty


def test_load_json_dataset() -> None:
    data = load_dataset("pik3ca_mutations", as_format="json")

    assert isinstance(data, dict)
    assert "domains" in data
    assert isinstance(data["domains"], list)


def test_load_dnmt3a_lollipop_dataset() -> None:
    data = load_dataset("dnmt3a_lollipop", as_format="json")

    assert isinstance(data, dict)
    assert data["gene"] == "DNMT3A"
    assert data["transcript"] == "NM_022552"
    assert data["protein_length"] == 912
    assert data["total_samples"] == 193
    assert data["mutated_samples"] == 47
    assert data["mutation_rate"] == 24.35
    assert len(data["features"]) == 22
    assert any(
        feature["position"] == 882 and feature["count"] == 27
        for feature in data["features"]
    )


def test_auto_format_loads_json_as_python_object() -> None:
    data = load_dataset("tcga_oncoprint")

    assert isinstance(data, list)
    assert data
    assert "gene" in data[0]


def test_load_curated_laml_oncoprint_dataset() -> None:
    data = load_dataset("tcga_laml_oncoprint", as_format="json")

    assert isinstance(data, dict)
    assert data["cohort"] == "TCGA LAML"
    assert data["total_samples"] == 193
    assert data["altered_samples"] == 141
    assert len(data["genes"]) == 10
    assert len(data["samples"]) == 193
    assert len(data["matrix"]) == 247
    assert {"sample", "gene", "class"} <= set(data["matrix"][0])


def test_airway_paired_logcounts_uses_packaged_data() -> None:
    base_mean, treated, control = airway_paired_logcounts()

    assert len(base_mean) == len(treated) == len(control)
    assert not treated.empty
    assert list(treated.columns) == list(control.columns)
    assert treated.index.equals(control.index)
    assert treated.index.equals(base_mean.index)


def test_unknown_dataset_raises_contextual_error() -> None:
    with pytest.raises(DatasetNotFoundError, match="Unknown dataset"):
        load_dataset("not_a_dataset")
