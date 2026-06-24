"""Altair-inspired dataset accessors for built-in GenomeSpy examples."""

from __future__ import annotations

import json
from copy import deepcopy
from dataclasses import dataclass
from typing import Any, Final, Literal, cast, overload
from urllib.parse import quote

DatasetName = Literal["copy_number_segments", "point_features"]
DatasetRecord = dict[str, Any]
DatasetValues = list[DatasetRecord]


class DatasetNotFoundError(ValueError):
    """Raised when a named built-in dataset is not available."""


@dataclass(frozen=True, slots=True)
class DatasetDefinition:
    """Metadata and records for one built-in dataset."""

    name: DatasetName
    description: str
    values: DatasetValues


_DATASETS: Final[dict[DatasetName, DatasetDefinition]] = {
    "point_features": DatasetDefinition(
        name="point_features",
        description="Toy point-like genomic features with positions and scores.",
        values=[
            {"chrom": "chr1", "pos": 12_000_000, "score": 0.28, "category": "A"},
            {"chrom": "chr1", "pos": 38_000_000, "score": 0.66, "category": "B"},
            {"chrom": "chr1", "pos": 72_000_000, "score": 0.41, "category": "A"},
            {"chrom": "chr2", "pos": 18_000_000, "score": 0.84, "category": "C"},
            {"chrom": "chr2", "pos": 59_000_000, "score": 0.52, "category": "B"},
            {"chrom": "chr3", "pos": 25_000_000, "score": 0.73, "category": "C"},
        ],
    ),
    "copy_number_segments": DatasetDefinition(
        name="copy_number_segments",
        description="Toy copy-number segments for two samples across three chromosomes.",
        values=[
            {
                "sample": "sample-a",
                "chrom": "chr1",
                "start": 0,
                "end": 30_000_000,
                "copy_number": 2.0,
            },
            {
                "sample": "sample-a",
                "chrom": "chr1",
                "start": 30_000_000,
                "end": 78_000_000,
                "copy_number": 3.1,
            },
            {
                "sample": "sample-a",
                "chrom": "chr2",
                "start": 0,
                "end": 62_000_000,
                "copy_number": 1.6,
            },
            {
                "sample": "sample-b",
                "chrom": "chr1",
                "start": 0,
                "end": 45_000_000,
                "copy_number": 2.2,
            },
            {
                "sample": "sample-b",
                "chrom": "chr2",
                "start": 0,
                "end": 52_000_000,
                "copy_number": 2.8,
            },
            {
                "sample": "sample-b",
                "chrom": "chr3",
                "start": 0,
                "end": 38_000_000,
                "copy_number": 1.3,
            },
        ],
    ),
}


def _dataset(name: str) -> DatasetDefinition:
    try:
        return _DATASETS[cast(DatasetName, name)]
    except KeyError as error:
        available = ", ".join(list_datasets())
        raise DatasetNotFoundError(
            f"Dataset {name!r} not found. Available datasets: {available}"
        ) from error


@dataclass(frozen=True, slots=True)
class DatasetAccessor:
    """Callable accessor for one built-in dataset.

    This mirrors the convenient part of Altair's ``data.cars()`` interface,
    while keeping this early project slice dependency-free.
    """

    name: DatasetName

    @property
    def description(self) -> str:
        """Return a short human-readable dataset description."""
        return _dataset(self.name).description

    @property
    def url(self) -> str:
        """Return the dataset encoded as a JSON data URL."""
        payload = json.dumps(load(self.name), separators=(",", ":"))
        return f"data:application/json,{quote(payload)}"

    def load(self) -> DatasetValues:
        """Load this dataset as a fresh list of dictionaries."""
        return load(self.name)

    def __call__(self) -> DatasetValues:
        """Load this dataset as a fresh list of dictionaries."""
        return self.load()

    def __repr__(self) -> str:
        return f"DatasetAccessor({self.name!r})"


class DataObject:
    """Attribute-based access to built-in datasets.

    Examples
    --------
    >>> from genome_spy.datasets import data
    >>> values = data.point_features()
    >>> data.list_datasets()
    ['copy_number_segments', 'point_features']
    """

    def __init__(self) -> None:
        self._accessors: dict[DatasetName, DatasetAccessor] = {}

    def __dir__(self) -> list[str]:
        return sorted([*super().__dir__(), *list_datasets()])

    def __getattr__(self, name: str) -> DatasetAccessor:
        _dataset(name)
        dataset_name = cast(DatasetName, name)
        if dataset_name not in self._accessors:
            self._accessors[dataset_name] = DatasetAccessor(dataset_name)
        return self._accessors[dataset_name]

    def list_datasets(self) -> list[DatasetName]:
        """Return available built-in dataset names."""
        return list_datasets()

    def __repr__(self) -> str:
        return f"GenomeSpyDataObject(datasets={len(_DATASETS)})"


@overload
def load(name: Literal["copy_number_segments"]) -> DatasetValues: ...


@overload
def load(name: Literal["point_features"]) -> DatasetValues: ...


@overload
def load(name: str) -> DatasetValues: ...


def load(name: str) -> DatasetValues:
    """Load a built-in dataset by name.

    A deep copy is returned so examples and notebooks can mutate the result
    without changing future calls.
    """
    return deepcopy(_dataset(name).values)


def list_datasets() -> list[DatasetName]:
    """Return available built-in dataset names."""
    return sorted(_DATASETS)


data = DataObject()
