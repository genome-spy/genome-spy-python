"""Dataset helpers for packaged GenomeSpy example data."""

from __future__ import annotations

import json
from importlib.abc import Traversable
from importlib.resources import files
from pathlib import Path
from typing import Any, Literal, cast, overload

__all__ = [
    "DatasetNotFoundError",
    "available_datasets",
    "load_dataset",
]

_DATA_DIR = files("genome_spy.datasets").joinpath("data")
_DATASETS = {
    "airway_metadata": "airway_metadata.csv",
    "airway_scaledcounts": "airway_scaledcounts.csv",
    "brca_maf": "brca.maf.gz",
    "hapmap_gwas": "hapmap_gwas.csv",
    "mutation_impact_reference": "mutation_impact_reference.json",
    "pik3ca_mutations": "pik3ca_mutations.json",
    "pyoncoprint_tcga": "tcga.tsv",
    "tcga_laml_annotations": "tcga_laml_annot.tsv",
    "tcga_laml_maf": "tcga_laml.maf.gz",
    "tcga_oncoprint": "oncoprint_dataset3.json",
}


class DatasetNotFoundError(ValueError):
    """Dataset name lookup failed.

    Description:
        ``load_dataset`` and related helpers use this exception to report an
        unknown dataset name together with the valid packaged choices.
    """


def available_datasets() -> tuple[str, ...]:
    """Packaged dataset names.

    Description:
        The returned names are the public identifiers accepted by
        ``load_dataset``.

    Returns:
        Dataset names that ``load_dataset`` accepts.

    Raises:
        None.

    Example:
        >>> available_datasets()
        ('airway_metadata', 'airway_scaledcounts', 'hapmap_gwas', ...)
    """

    return tuple(sorted(_DATASETS))


def _resource_for(name: str) -> Traversable:
    try:
        filename = _DATASETS[name]
    except KeyError as exc:
        known = ", ".join(available_datasets())
        raise DatasetNotFoundError(
            f"Unknown dataset {name!r}. Available datasets: {known}."
        ) from exc
    return _DATA_DIR.joinpath(filename)


def _load_dataframe(name: str) -> Any:
    try:
        import pandas as pd
    except ImportError as exc:
        raise ImportError(
            f"Loading dataset {name!r} as a DataFrame requires pandas. "
            "Install pandas or use as_format='text' or as_format='json'."
        ) from exc

    resource = _resource_for(name)
    suffixes = Path(_DATASETS[name]).suffixes
    if suffixes == [".csv"]:
        return pd.read_csv(resource)
    if suffixes == [".tsv"]:
        return pd.read_csv(resource, sep="\t")
    if suffixes[-2:] == [".maf", ".gz"]:
        return pd.read_csv(resource, sep="\t", compression="gzip")
    raise ValueError(
        f"Dataset {name!r} is not tabular and cannot be read as a DataFrame."
    )


@overload
def load_dataset(name: str, *, as_format: Literal["auto"] = "auto") -> Any: ...


@overload
def load_dataset(name: str, *, as_format: Literal["dataframe"]) -> Any: ...


@overload
def load_dataset(
    name: str, *, as_format: Literal["json"]
) -> dict[str, Any] | list[Any]: ...


@overload
def load_dataset(name: str, *, as_format: Literal["text"]) -> str: ...


def load_dataset(
    name: str,
    *,
    as_format: Literal["auto", "dataframe", "json", "text"] = "auto",
) -> Any:
    """Load a packaged example dataset by name.

    Description:
        The loader understands the small set of real datasets vendored with the
        package for examples and tutorials. ``"auto"`` returns a pandas
        ``DataFrame`` for CSV, TSV, and compressed MAF files and parsed Python
        objects for JSON files.

    Args:
        name: Dataset name from ``available_datasets()``.
        as_format: Output format to return.

    Returns:
        The loaded dataset in the requested format.

    Raises:
        DatasetNotFoundError: If the dataset name is unknown.
        ImportError: If ``as_format="dataframe"`` is requested without pandas.
        ValueError: If the requested format does not match the stored file type.

    Example:
        >>> load_dataset("hapmap_gwas").head()
        >>> load_dataset("pik3ca_mutations", as_format="json")["domains"][0]
    """

    resource = _resource_for(name)
    filename = _DATASETS[name]
    suffix = Path(filename).suffix
    suffixes = Path(filename).suffixes

    if as_format == "text":
        if suffix == ".gz":
            import gzip

            return gzip.decompress(resource.read_bytes()).decode("utf-8")
        return resource.read_text(encoding="utf-8")
    if as_format == "json":
        if suffix != ".json":
            raise ValueError(f"Dataset {name!r} is stored as {suffix}, not JSON.")
        return cast(dict[str, Any] | list[Any], json.loads(resource.read_text("utf-8")))
    if as_format == "dataframe":
        return _load_dataframe(name)
    if suffix == ".json":
        return json.loads(resource.read_text("utf-8"))
    if suffix in {".csv", ".tsv"} or suffixes[-2:] == [".maf", ".gz"]:
        return _load_dataframe(name)
    raise ValueError(f"Unsupported dataset format for {name!r}: {suffix}.")
