from __future__ import annotations

import pytest

import genome_spy as gs
from genome_spy.datasets import DatasetAccessor, DatasetNotFoundError, data, load


def test_data_object_lists_builtin_datasets() -> None:
    assert data.list_datasets() == ["copy_number_segments", "point_features"]


def test_dataset_accessors_are_callable() -> None:
    accessor = data.point_features

    assert isinstance(accessor, DatasetAccessor)
    assert accessor.description
    assert accessor()[0]["chrom"] == "chr1"


def test_load_returns_fresh_copy() -> None:
    first = data.point_features()
    first[0]["score"] = 99

    second = load("point_features")

    assert second[0]["score"] == 0.28


def test_missing_dataset_has_clear_error() -> None:
    with pytest.raises(DatasetNotFoundError, match="Available datasets"):
        load("missing")


def test_dataset_can_be_used_in_chart() -> None:
    chart = (
        gs.Chart(data=data.copy_number_segments())
        .mark_rect()
        .encode(
            x=gs.X("start:Q"),
            x2=gs.X2("end:Q"),
            y=gs.Y("sample:N"),
            color=gs.Color("copy_number:Q"),
        )
    )

    spec = chart.to_dict()

    assert spec["data"]["values"][0]["sample"] == "sample-a"
    assert spec["encoding"]["x2"] == {"field": "end", "type": "quantitative"}


def test_dataset_accessor_exposes_data_url() -> None:
    assert data.point_features.url.startswith("data:application/json,")
