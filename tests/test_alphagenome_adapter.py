from __future__ import annotations

import importlib.util
import sys
from dataclasses import dataclass
from pathlib import Path
from types import ModuleType

import numpy as np
import polars as pl
import pytest


@dataclass(frozen=True)
class _Interval:
    chromosome: str
    start: int
    end: int


@dataclass(frozen=True)
class _TrackData:
    values: np.ndarray
    metadata: list[dict[str, str]]
    resolution: int
    interval: _Interval | None


class _SliceTrackingArray:
    def __init__(self, values: np.ndarray) -> None:
        self._values = values
        self.shape = values.shape
        self.keys: list[tuple[slice, int]] = []

    def __getitem__(self, key: tuple[slice, int]) -> np.ndarray:
        self.keys.append(key)
        return self._values[key]


@pytest.fixture
def adapter() -> ModuleType:
    path = Path("notebooks/alphagenome/_alphagenome_adapter.py")
    module_spec = importlib.util.spec_from_file_location(path.stem, path)
    if module_spec is None or module_spec.loader is None:
        raise RuntimeError(f"Could not load AlphaGenome adapter from {path}.")
    module = importlib.util.module_from_spec(module_spec)
    sys.modules[module_spec.name] = module
    module_spec.loader.exec_module(module)
    return module


def test_adapter_selects_metadata_independent_of_track_order(
    adapter: ModuleType,
) -> None:
    interval = _Interval("chr1", 100, 106)
    reference = _TrackData(
        values=np.array([[1.0, 10.0], [2.0, 20.0], [3.0, 30.0]]),
        metadata=[
            {"name": "other", "strand": "."},
            {
                "name": "tal1_rna",
                "strand": "+",
                "biosample": "CD34-positive",
                "ontology_curie": "CL:0001059",
            },
        ],
        resolution=2,
        interval=interval,
    )
    alternate = _TrackData(
        values=np.array([[11.0, 1.5], [21.0, 2.5], [31.0, 3.5]]),
        metadata=[
            {
                "name": "tal1_rna",
                "strand": "+",
                "biosample": "CD34-positive",
                "ontology_curie": "CL:0001059",
            },
            {"name": "other", "strand": "."},
        ],
        resolution=2,
        interval=interval,
    )

    frame = adapter.adapt_prediction_pairs(
        [
            adapter.TrackPair(
                reference=reference,
                alternate=alternate,
                selector=adapter.TrackSelector(
                    output_type="RNA_SEQ",
                    metadata=(("name", "tal1_rna"), ("strand", "+")),
                ),
            )
        ],
        request_id="request-1",
        display_interval=_Interval("chr1", 100, 106),
    )

    assert frame.schema == {
        "chrom": pl.String,
        "start0": pl.Int64,
        "end0": pl.Int64,
        "output_type": pl.String,
        "track_name": pl.String,
        "biosample_name": pl.String,
        "ontology_curie": pl.String,
        "strand": pl.String,
        "histone_mark": pl.String,
        "resolution": pl.Int64,
        "reference": pl.Float64,
        "alternate": pl.Float64,
        "delta": pl.Float64,
        "request_id": pl.String,
    }
    assert frame.select("start0", "end0", "reference", "alternate", "delta").rows() == [
        (100, 102, 10.0, 11.0, 1.0),
        (102, 104, 20.0, 21.0, 1.0),
        (104, 106, 30.0, 31.0, 1.0),
    ]
    assert frame["biosample_name"].unique().to_list() == ["CD34-positive"]


def test_adapter_attaches_sequence_chunks_for_dynseq_logos(
    adapter: ModuleType,
) -> None:
    frame = pl.DataFrame(
        {
            "start0": [102, 104],
            "end0": [104, 106],
        }
    )

    enriched = adapter.add_sequence_chunks(
        frame,
        reference_sequence="ACGTACGT",
        alternate_sequence="ACATACGT",
        sequence_start0=100,
    )

    assert enriched.select("reference_bases", "alternate_bases").rows() == [
        ("GT", "AT"),
        ("AC", "AC"),
    ]


def test_adapter_rejects_sequence_chunks_outside_supplied_interval(
    adapter: ModuleType,
) -> None:
    frame = pl.DataFrame({"start0": [99], "end0": [101]})

    with pytest.raises(adapter.AlphaGenomeAdapterError, match="must fall within"):
        adapter.add_sequence_chunks(
            frame,
            reference_sequence="ACGT",
            alternate_sequence="ACAT",
            sequence_start0=100,
        )


def test_adapter_rejects_misaligned_reference_and_alternate_tracks(
    adapter: ModuleType,
) -> None:
    metadata = [{"name": "track", "strand": "."}]
    reference = _TrackData(
        values=np.array([[1.0], [2.0]]),
        metadata=metadata,
        resolution=2,
        interval=_Interval("chr1", 100, 104),
    )
    alternate = _TrackData(
        values=np.array([[1.0], [2.0]]),
        metadata=metadata,
        resolution=2,
        interval=_Interval("chr1", 102, 106),
    )

    with pytest.raises(adapter.AlphaGenomeAdapterError, match="same interval"):
        adapter.adapt_prediction_pairs(
            [
                adapter.TrackPair(
                    reference=reference,
                    alternate=alternate,
                    selector=adapter.TrackSelector(
                        output_type="DNASE",
                        metadata=(("name", "track"), ("strand", ".")),
                    ),
                )
            ],
            request_id="request-1",
            display_interval=_Interval("chr1", 100, 104),
        )


def test_adapter_crops_and_concatenates_mixed_modalities(adapter: ModuleType) -> None:
    interval = _Interval("chr1", 100, 108)
    rna_metadata = [
        {
            "name": "rna",
            "strand": "+",
            "biosample_name": "CD34-positive",
            "ontology_curie": "CL:0001059",
        }
    ]
    histone_metadata = [
        {
            "name": "h3k27ac",
            "strand": ".",
            "biosample_name": "CD34-positive",
            "ontology_curie": "CL:0001059",
            "histone_mark": "H3K27ac",
        }
    ]
    rna = _TrackData(
        values=np.array([[1.0], [2.0], [3.0], [4.0]]),
        metadata=rna_metadata,
        resolution=2,
        interval=interval,
    )
    histone = _TrackData(
        values=np.array([[10.0], [20.0], [30.0], [40.0]]),
        metadata=histone_metadata,
        resolution=2,
        interval=interval,
    )

    frame = adapter.adapt_prediction_pairs(
        [
            adapter.TrackPair(
                reference=rna,
                alternate=rna,
                selector=adapter.TrackSelector("RNA_SEQ", (("name", "rna"),)),
            ),
            adapter.TrackPair(
                reference=histone,
                alternate=histone,
                selector=adapter.TrackSelector("CHIP_HISTONE", (("name", "h3k27ac"),)),
            ),
        ],
        request_id="request-1",
        display_interval=_Interval("chr1", 102, 106),
    )

    assert frame.height == 4
    assert frame["start0"].to_list() == [102, 104, 102, 104]
    assert frame["histone_mark"].to_list() == [None, None, "H3K27ac", "H3K27ac"]


def test_adapter_rejects_a_prediction_larger_than_the_display_budget(
    adapter: ModuleType,
) -> None:
    track = _TrackData(
        values=np.array([[1.0], [2.0], [3.0]]),
        metadata=[{"name": "track", "strand": "."}],
        resolution=1,
        interval=_Interval("chr1", 100, 103),
    )

    with pytest.raises(adapter.AlphaGenomeAdapterError, match="limit is 2"):
        adapter.adapt_prediction_pairs(
            [
                adapter.TrackPair(
                    reference=track,
                    alternate=track,
                    selector=adapter.TrackSelector("DNASE", (("name", "track"),)),
                )
            ],
            request_id="request-1",
            display_interval=_Interval("chr1", 100, 103),
            max_rows=2,
        )


def test_adapter_checks_row_budget_before_reading_values(adapter: ModuleType) -> None:
    values = _SliceTrackingArray(np.array([[1.0], [2.0], [3.0]]))
    track = _TrackData(
        values=values,  # type: ignore[arg-type]
        metadata=[{"name": "track", "strand": "."}],
        resolution=1,
        interval=_Interval("chr1", 100, 103),
    )

    with pytest.raises(adapter.AlphaGenomeAdapterError, match="limit is 2"):
        adapter.adapt_prediction_pairs(
            [
                adapter.TrackPair(
                    reference=track,
                    alternate=track,
                    selector=adapter.TrackSelector("DNASE", (("name", "track"),)),
                )
            ],
            request_id="request-1",
            display_interval=_Interval("chr1", 100, 103),
            max_rows=2,
        )

    assert values.keys == []


def test_adapter_slices_native_values_before_converting_to_python(
    adapter: ModuleType,
) -> None:
    values = _SliceTrackingArray(np.array([[1.0], [2.0], [3.0], [4.0]]))
    track = _TrackData(
        values=values,  # type: ignore[arg-type]
        metadata=[{"name": "track", "strand": "."}],
        resolution=2,
        interval=_Interval("chr1", 100, 108),
    )

    frame = adapter.adapt_prediction_pairs(
        [
            adapter.TrackPair(
                reference=track,
                alternate=track,
                selector=adapter.TrackSelector("DNASE", (("name", "track"),)),
            )
        ],
        request_id="request-1",
        display_interval=_Interval("chr1", 102, 106),
    )

    assert frame["start0"].to_list() == [102, 104]
    assert values.keys == [(slice(1, 3), 0), (slice(1, 3), 0)]
