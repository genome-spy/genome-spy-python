"""Convert selected sequence-model track pairs into GenomeSpy signal rows.

This private example helper accepts a small structural track contract shared
by the local PyTorch backend and test fixtures. The public library does not
import it.
"""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from typing import Any, Protocol

import polars as pl


class AlphaGenomeAdapterError(ValueError):
    """Raised when a model output cannot become an aligned display track."""


class IntervalLike(Protocol):
    """The interval attributes used from AlphaGenome's genome.Interval."""

    chromosome: str
    start: int
    end: int


class TrackDataLike(Protocol):
    """The TrackData attributes used by this notebook-local adapter."""

    values: Any
    metadata: Any
    resolution: int
    interval: IntervalLike | None


@dataclass(frozen=True, slots=True)
class TrackSelector:
    """Stable output and metadata selector for one display panel."""

    output_type: str
    metadata: tuple[tuple[str, str], ...]


@dataclass(frozen=True, slots=True)
class TrackPair:
    """Reference and alternate TrackData used for one display panel."""

    reference: TrackDataLike
    alternate: TrackDataLike
    selector: TrackSelector


_PREDICTION_SCHEMA = {
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

_SEQUENCE_COLUMNS = {
    "reference_bases": pl.String,
    "alternate_bases": pl.String,
}


def empty_prediction_frame() -> pl.DataFrame:
    """Return an empty dataframe with the live prediction schema."""
    return pl.DataFrame(schema={**_PREDICTION_SCHEMA, **_SEQUENCE_COLUMNS})


def add_sequence_chunks(
    frame: pl.DataFrame,
    *,
    reference_sequence: str,
    alternate_sequence: str,
    sequence_start0: int,
) -> pl.DataFrame:
    """Attach the reference and alternate bases covered by each signal bin."""
    reference = reference_sequence.upper()
    alternate = alternate_sequence.upper()
    if len(reference) != len(alternate):
        raise AlphaGenomeAdapterError(
            "Reference and alternate sequences must have the same length."
        )
    sequence_end0 = sequence_start0 + len(reference)
    chunks: list[tuple[str, str]] = []
    for start0, end0 in frame.select("start0", "end0").iter_rows():
        if start0 < sequence_start0 or end0 > sequence_end0:
            raise AlphaGenomeAdapterError(
                "Prediction bins must fall within the supplied sequences."
            )
        start_offset = start0 - sequence_start0
        end_offset = end0 - sequence_start0
        chunks.append(
            (
                reference[start_offset:end_offset],
                alternate[start_offset:end_offset],
            )
        )
    return frame.with_columns(
        pl.Series("reference_bases", [chunk[0] for chunk in chunks], pl.String),
        pl.Series("alternate_bases", [chunk[1] for chunk in chunks], pl.String),
    )


def adapt_prediction_pairs(
    pairs: Sequence[TrackPair],
    *,
    request_id: str,
    display_interval: IntervalLike,
    max_rows: int = 250_000,
) -> pl.DataFrame:
    """Return cropped long-form rows for one complete model result."""
    if not pairs:
        raise AlphaGenomeAdapterError("At least one selected track pair is required.")
    if max_rows < 1:
        raise AlphaGenomeAdapterError("max_rows must be positive.")
    frames: list[pl.DataFrame] = []
    rows_so_far = 0
    for pair in pairs:
        frame = _adapt_pair(
            pair,
            request_id=request_id,
            display_interval=display_interval,
            rows_so_far=rows_so_far,
            max_rows=max_rows,
        )
        frames.append(frame)
        rows_so_far += frame.height
    return pl.concat(frames, how="vertical")


def _adapt_pair(
    pair: TrackPair,
    *,
    request_id: str,
    display_interval: IntervalLike,
    rows_so_far: int,
    max_rows: int,
) -> pl.DataFrame:
    reference_index, reference_metadata = _track_index(
        pair.reference.metadata, pair.selector
    )
    alternate_index, alternate_metadata = _track_index(
        pair.alternate.metadata, pair.selector
    )
    chromosome, start0, end0 = _shared_interval(pair)
    _validate_display_interval(display_interval, chromosome, start0, end0)
    resolution = _shared_resolution(pair)
    reference_bin_count = _track_bin_count(pair.reference.values, reference_index)
    alternate_bin_count = _track_bin_count(pair.alternate.values, alternate_index)
    if reference_bin_count != alternate_bin_count:
        raise AlphaGenomeAdapterError(
            "Reference and alternate tracks have different bin counts."
        )
    if start0 + reference_bin_count * resolution != end0:
        raise AlphaGenomeAdapterError(
            "Track bin count and interval width disagree with the resolution."
        )
    first_bin, last_bin = _display_bin_bounds(
        display_interval, start0, resolution, reference_bin_count
    )
    total_rows = rows_so_far + last_bin - first_bin
    if total_rows > max_rows:
        raise AlphaGenomeAdapterError(
            f"Cropped prediction has {total_rows} rows; limit is {max_rows}."
        )
    reference_values = _track_values(
        pair.reference.values, reference_index, first_bin, last_bin
    )
    alternate_values = _track_values(
        pair.alternate.values, alternate_index, first_bin, last_bin
    )
    bins = [start0 + bin_index * resolution for bin_index in range(first_bin, last_bin)]
    biosample_name = _metadata_value(reference_metadata, "biosample_name", "biosample")
    ontology_curie = _metadata_value(reference_metadata, "ontology_curie")
    histone_mark = _metadata_value(
        reference_metadata, "histone_mark", "histone", "target"
    )
    return pl.DataFrame(
        {
            "chrom": [chromosome] * len(bins),
            "start0": bins,
            "end0": [start + resolution for start in bins],
            "output_type": [pair.selector.output_type] * len(bins),
            "track_name": [str(reference_metadata["name"])] * len(bins),
            "biosample_name": [biosample_name] * len(bins),
            "ontology_curie": [ontology_curie] * len(bins),
            "strand": [str(reference_metadata["strand"])] * len(bins),
            "histone_mark": [histone_mark] * len(bins),
            "resolution": [resolution] * len(bins),
            "reference": reference_values,
            "alternate": alternate_values,
            "delta": [
                alternate - reference
                for reference, alternate in zip(reference_values, alternate_values)
            ],
            "request_id": [request_id] * len(bins),
        },
        schema=_PREDICTION_SCHEMA,
    )


def _track_index(metadata: Any, selector: TrackSelector) -> tuple[int, dict[str, Any]]:
    records = _metadata_records(metadata)
    matches = [
        (index, record)
        for index, record in enumerate(records)
        if all(record.get(column) == expected for column, expected in selector.metadata)
    ]
    if len(matches) != 1:
        raise AlphaGenomeAdapterError(
            f"Selector for {selector.output_type!r} matched {len(matches)} tracks; "
            "expected exactly one."
        )
    return matches[0]


def _metadata_records(metadata: Any) -> list[dict[str, Any]]:
    if isinstance(metadata, Sequence) and not isinstance(metadata, (str, bytes)):
        records = metadata
    elif hasattr(metadata, "to_dict"):
        records = metadata.to_dict("records")
    else:
        raise AlphaGenomeAdapterError("Track metadata must provide row records.")
    if not all(isinstance(record, Mapping) for record in records):
        raise AlphaGenomeAdapterError("Track metadata rows must be mappings.")
    normalized = [dict(record) for record in records]
    if any("name" not in record or "strand" not in record for record in normalized):
        raise AlphaGenomeAdapterError('Track metadata requires "name" and "strand".')
    return normalized


def _shared_interval(pair: TrackPair) -> tuple[str, int, int]:
    reference_interval = pair.reference.interval
    alternate_interval = pair.alternate.interval
    if reference_interval is None or alternate_interval is None:
        raise AlphaGenomeAdapterError("TrackData interval is required for plotting.")
    reference_coordinates = (
        reference_interval.chromosome,
        reference_interval.start,
        reference_interval.end,
    )
    alternate_coordinates = (
        alternate_interval.chromosome,
        alternate_interval.start,
        alternate_interval.end,
    )
    if reference_coordinates != alternate_coordinates:
        raise AlphaGenomeAdapterError(
            "Reference and alternate tracks must cover the same interval."
        )
    chromosome, start0, end0 = reference_coordinates
    if start0 >= end0:
        raise AlphaGenomeAdapterError("Track interval must have positive width.")
    return chromosome, start0, end0


def _shared_resolution(pair: TrackPair) -> int:
    if pair.reference.resolution != pair.alternate.resolution:
        raise AlphaGenomeAdapterError(
            "Reference and alternate tracks must have the same resolution."
        )
    if pair.reference.resolution <= 0:
        raise AlphaGenomeAdapterError("Track resolution must be positive.")
    return pair.reference.resolution


def _validate_display_interval(
    interval: IntervalLike,
    chromosome: str,
    start0: int,
    end0: int,
) -> None:
    if interval.chromosome != chromosome:
        raise AlphaGenomeAdapterError(
            "Display interval chromosome differs from TrackData."
        )
    if interval.start < start0 or interval.end > end0 or interval.start >= interval.end:
        raise AlphaGenomeAdapterError(
            "Display interval must be a positive subinterval of TrackData."
        )


def _track_bin_count(values: Any, track_index: int) -> int:
    try:
        bin_count, track_count = values.shape
    except (IndexError, TypeError, ValueError) as exc:
        raise AlphaGenomeAdapterError(
            "Track values must have shape (positional_bins, tracks)."
        ) from exc
    if track_index >= track_count:
        raise AlphaGenomeAdapterError("Track selector index exceeds the values array.")
    return int(bin_count)


def _display_bin_bounds(
    interval: IntervalLike,
    start0: int,
    resolution: int,
    bin_count: int,
) -> tuple[int, int]:
    first_bin = (interval.start - start0 + resolution - 1) // resolution
    last_bin = (interval.end - start0) // resolution
    first_bin = max(first_bin, 0)
    last_bin = min(last_bin, bin_count)
    if first_bin >= last_bin:
        raise AlphaGenomeAdapterError(
            "Display interval contains no complete prediction bins."
        )
    return first_bin, last_bin


def _track_values(
    values: Any,
    track_index: int,
    first_bin: int,
    last_bin: int,
) -> list[float]:
    try:
        selected_values = values[first_bin:last_bin, track_index]
    except (IndexError, TypeError, ValueError) as exc:
        raise AlphaGenomeAdapterError(
            "Track values must have shape (positional_bins, tracks)."
        ) from exc
    if getattr(selected_values, "ndim", None) != 1:
        raise AlphaGenomeAdapterError(
            "Only one-dimensional signal tracks can be displayed in this notebook."
        )
    return [float(value) for value in selected_values]


def _metadata_value(record: Mapping[str, Any], *columns: str) -> str | None:
    for column in columns:
        value = record.get(column)
        if value is not None:
            return str(value)
    return None
