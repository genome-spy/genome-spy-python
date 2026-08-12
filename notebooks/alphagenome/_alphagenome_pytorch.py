"""Lazy local AlphaGenome-PyTorch inference for the Marimo example.

This private helper deliberately keeps Torch, Hugging Face, and AlphaGenome
imports behind explicit calls. Importing the example never loads a checkpoint
or initializes an accelerator.
"""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from dataclasses import dataclass
import gc
from importlib.metadata import PackageNotFoundError, version
import json
from pathlib import Path
from typing import Any


CHECKPOINT_REPOSITORY = "gtca/alphagenome_pytorch"
CHECKPOINT_FILENAME = "model_all_folds.safetensors"
CHECKPOINT_REVISION = "b01c0ffa73e07c053491f3b5ea8bcf67d93b9920"
PACKAGE_VERSION = "0.3.1"
MODEL_INPUT_WIDTH = 131_072
DEFAULT_RESOLUTION = 128
PRECISION_AUTO = "auto"
PRECISION_FLOAT32 = "full_float32"
PRECISION_MIXED = "mixed_precision"
_loaded_model: Any | None = None
_loaded_model_key: tuple[str, int, int, str, str] | None = None


class AlphaGenomePyTorchError(RuntimeError):
    """Raised when the optional local model cannot produce display tracks."""


@dataclass(frozen=True, slots=True)
class ModelInterval:
    """A zero-based, half-open interval accepted by the local model."""

    chromosome: str
    start: int
    end: int

    @property
    def width(self) -> int:
        """Return the interval width in base pairs."""
        return self.end - self.start


@dataclass(frozen=True, slots=True)
class ModelVariant:
    """A one-based single-nucleotide substitution."""

    chromosome: str
    position: int
    reference_bases: str
    alternate_bases: str


@dataclass(frozen=True, slots=True)
class TrackSelector:
    """Select exactly one metadata-aware model track."""

    output_type: str
    metadata: tuple[tuple[str, object], ...]

    @property
    def signature(self) -> str:
        """Return a deterministic request identity for this exact selector."""
        payload = {
            "metadata": sorted(self.metadata, key=lambda item: item[0]),
            "output_type": self.output_type,
        }
        return json.dumps(payload, sort_keys=True, separators=(",", ":"))


@dataclass(frozen=True, slots=True)
class TrackSnapshot:
    """Small CPU snapshot implementing the visualization adapter contract."""

    values: Any
    metadata: tuple[dict[str, Any], ...]
    resolution: int
    interval: ModelInterval


@dataclass(frozen=True, slots=True)
class TrackSnapshotPair:
    """Cropped reference and alternate snapshots for one selected track."""

    reference: TrackSnapshot
    alternate: TrackSnapshot
    selector: TrackSelector


TAL1_TRACK_SELECTORS = (
    TrackSelector(
        "rna_seq",
        (
            ("ontology_curie", "CL:0001059"),
            ("track_name", "CL:0001059 polyA plus RNA-seq"),
            ("strand", "."),
        ),
    ),
    TrackSelector(
        "dnase",
        (
            ("ontology_curie", "CL:0001059"),
            ("track_name", "CL:0001059 DNase-seq"),
            ("strand", "."),
        ),
    ),
    TrackSelector(
        "chip_histone",
        (
            ("ontology_curie", "CL:0001059"),
            ("histone_mark", "H3K27ac"),
            ("strand", "."),
        ),
    ),
    TrackSelector(
        "chip_histone",
        (
            ("ontology_curie", "CL:0001059"),
            ("histone_mark", "H3K4me1"),
            ("strand", "."),
        ),
    ),
)


def download_checkpoint(
    *,
    repository: str = CHECKPOINT_REPOSITORY,
    filename: str = CHECKPOINT_FILENAME,
    revision: str = CHECKPOINT_REVISION,
) -> Path:
    """Resolve the model checkpoint through the Hugging Face cache."""
    try:
        from huggingface_hub import hf_hub_download
    except ImportError as exc:
        raise AlphaGenomePyTorchError(
            "Checkpoint download requires `huggingface-hub`."
        ) from exc

    return Path(
        hf_hub_download(repo_id=repository, filename=filename, revision=revision)
    )


def checkpoint_identity(checkpoint: str | Path, *, pinned: bool) -> str:
    """Return a cache-safe identity for a pinned or user-supplied checkpoint."""
    if pinned:
        return f"{CHECKPOINT_REPOSITORY}:{CHECKPOINT_FILENAME}@{CHECKPOINT_REVISION}"
    checkpoint_path = Path(checkpoint).expanduser().resolve()
    if not checkpoint_path.is_file():
        raise AlphaGenomePyTorchError(
            f"AlphaGenome checkpoint does not exist: {checkpoint_path}"
        )
    stat = checkpoint_path.stat()
    return f"local:{checkpoint_path}:{stat.st_size}:{stat.st_mtime_ns}"


def update_prediction_cache(
    cache: Mapping[str, Any],
    request_id: str,
    result: Any,
    *,
    max_entries: int = 8,
) -> dict[str, Any]:
    """Return a bounded insertion-ordered session prediction cache."""
    if max_entries < 1:
        raise AlphaGenomePyTorchError("Prediction cache size must be positive.")
    updated = {key: value for key, value in cache.items() if key != request_id}
    updated[request_id] = result
    while len(updated) > max_entries:
        del updated[next(iter(updated))]
    return updated


def resolve_precision(device: str, requested: str = PRECISION_AUTO) -> str:
    """Resolve a supported compute-precision policy for the selected device."""
    if requested not in {PRECISION_AUTO, PRECISION_FLOAT32, PRECISION_MIXED}:
        raise AlphaGenomePyTorchError(f"Unsupported precision policy: {requested!r}.")
    try:
        import torch
    except ImportError as exc:
        raise AlphaGenomePyTorchError(
            "Device validation requires the notebook-only Torch install."
        ) from exc

    if device == "cpu":
        if requested == PRECISION_MIXED:
            raise AlphaGenomePyTorchError(
                "Mixed precision is only enabled for compatible CUDA devices."
            )
        return PRECISION_FLOAT32
    if not device.startswith("cuda"):
        raise AlphaGenomePyTorchError(
            "AlphaGenome-PyTorch 0.3.1 is supported here on CUDA or CPU only."
        )
    if not torch.cuda.is_available():
        raise AlphaGenomePyTorchError(
            "CUDA was selected, but Torch reports that CUDA is unavailable."
        )
    supports_bfloat16 = bool(torch.cuda.is_bf16_supported())
    if requested == PRECISION_MIXED and not supports_bfloat16:
        raise AlphaGenomePyTorchError(
            "Mixed precision requires a CUDA device with bfloat16 support."
        )
    if requested == PRECISION_AUTO:
        return PRECISION_MIXED if supports_bfloat16 else PRECISION_FLOAT32
    return requested


def unload_model() -> None:
    """Release the notebook's current model before loading another one."""
    global _loaded_model, _loaded_model_key
    previous_model = _loaded_model
    _loaded_model = None
    _loaded_model_key = None
    if previous_model is not None:
        del previous_model
    gc.collect()
    try:
        import torch
    except ImportError:
        return
    if torch.cuda.is_available():
        torch.cuda.empty_cache()


def load_model(
    checkpoint: str | Path,
    *,
    device: str = "cuda",
    precision: str = PRECISION_FLOAT32,
) -> Any:
    """Load at most one local model, replacing the prior model before allocation."""
    global _loaded_model, _loaded_model_key
    checkpoint_path = Path(checkpoint).expanduser().resolve()
    if not checkpoint_path.is_file():
        raise AlphaGenomePyTorchError(
            f"AlphaGenome checkpoint does not exist: {checkpoint_path}"
        )
    try:
        installed_version = version("alphagenome-pytorch")
    except PackageNotFoundError as exc:
        raise AlphaGenomePyTorchError(
            "Local inference requires the notebook-only `alphagenome-pytorch` install."
        ) from exc
    if installed_version != PACKAGE_VERSION:
        raise AlphaGenomePyTorchError(
            f"Expected alphagenome-pytorch {PACKAGE_VERSION}, found "
            f"{installed_version}."
        )
    if precision not in {PRECISION_FLOAT32, PRECISION_MIXED}:
        raise AlphaGenomePyTorchError(
            "Resolve the compute precision before loading the model."
        )
    checkpoint_stat = checkpoint_path.stat()
    key = (
        str(checkpoint_path),
        checkpoint_stat.st_size,
        checkpoint_stat.st_mtime_ns,
        device,
        precision,
    )
    if _loaded_model is not None and _loaded_model_key == key:
        return _loaded_model

    unload_model()
    try:
        model = _load_fresh_model(checkpoint_path, device=device, precision=precision)
    except Exception:
        unload_model()
        raise
    _loaded_model = model
    _loaded_model_key = key
    return model


def _load_fresh_model(checkpoint: Path, *, device: str, precision: str) -> Any:
    try:
        from alphagenome_pytorch import AlphaGenome
        from alphagenome_pytorch.config import DtypePolicy
    except ImportError as exc:
        raise AlphaGenomePyTorchError(
            "Local inference requires Python 3.12+ and `alphagenome-pytorch`."
        ) from exc

    policy = (
        DtypePolicy.mixed_precision()
        if precision == PRECISION_MIXED
        else DtypePolicy.full_float32()
    )
    model = AlphaGenome.from_pretrained(
        checkpoint,
        dtype_policy=policy,
        device="cpu",
    )
    if device != "cpu":
        model.to(device)
    model.eval()
    return model


def apply_snv(
    reference_sequence: str,
    interval: ModelInterval,
    variant: ModelVariant,
) -> str:
    """Return an equal-length alternate sequence after strict REF validation."""
    reference = reference_sequence.upper()
    ref = variant.reference_bases.upper()
    alt = variant.alternate_bases.upper()
    if len(ref) != 1 or len(alt) != 1 or ref == alt:
        raise AlphaGenomePyTorchError(
            "The first local notebook backend supports one non-reference SNV."
        )
    if variant.chromosome != interval.chromosome:
        raise AlphaGenomePyTorchError("Variant and model interval chromosomes differ.")
    if len(reference) != interval.width:
        raise AlphaGenomePyTorchError(
            "Reference sequence length must equal the model interval width."
        )
    offset = variant.position - 1 - interval.start
    if offset < 0 or offset >= len(reference):
        raise AlphaGenomePyTorchError("Variant falls outside the model interval.")
    if reference[offset] != ref:
        raise AlphaGenomePyTorchError(
            f"Reference mismatch: expected {ref!r}, found {reference[offset]!r}."
        )
    return reference[:offset] + alt + reference[offset + 1 :]


def predict_variant_tracks(
    model: Any,
    *,
    reference_sequence: str,
    model_interval: ModelInterval,
    display_interval: ModelInterval,
    variant: ModelVariant,
    selectors: Sequence[TrackSelector] = TAL1_TRACK_SELECTORS,
    organism_index: int = 0,
    resolution: int = DEFAULT_RESOLUTION,
) -> list[TrackSnapshotPair]:
    """Predict and crop selected reference/alternate tracks sequentially."""
    if not selectors:
        raise AlphaGenomePyTorchError("At least one track selector is required.")
    first_bin, last_bin, cropped_interval = _crop_bounds(
        model_interval, display_interval, resolution
    )
    alternate_sequence = apply_snv(reference_sequence, model_interval, variant)
    reference_tracks = _predict_sequence_tracks(
        model,
        reference_sequence,
        selectors,
        organism_index=organism_index,
        resolution=resolution,
        first_bin=first_bin,
        last_bin=last_bin,
        interval=cropped_interval,
    )
    alternate_tracks = _predict_sequence_tracks(
        model,
        alternate_sequence,
        selectors,
        organism_index=organism_index,
        resolution=resolution,
        first_bin=first_bin,
        last_bin=last_bin,
        interval=cropped_interval,
    )
    return [
        TrackSnapshotPair(reference_tracks[index], alternate_tracks[index], selector)
        for index, selector in enumerate(selectors)
    ]


def _predict_sequence_tracks(
    model: Any,
    sequence: str,
    selectors: Sequence[TrackSelector],
    *,
    organism_index: int,
    resolution: int,
    first_bin: int,
    last_bin: int,
    interval: ModelInterval,
) -> list[TrackSnapshot]:
    try:
        from alphagenome_pytorch.utils.sequence import sequence_to_onehot_tensor
    except ImportError as exc:
        raise AlphaGenomePyTorchError(
            "Local inference requires `alphagenome-pytorch`."
        ) from exc

    try:
        device = next(model.parameters()).device
    except (AttributeError, StopIteration) as exc:
        raise AlphaGenomePyTorchError("Model does not expose a Torch device.") from exc
    onehot = sequence_to_onehot_tensor(sequence, device=device).unsqueeze(0)
    heads = tuple(dict.fromkeys(selector.output_type for selector in selectors))
    outputs = model.predict(
        onehot,
        organism_index=organism_index,
        named_outputs=True,
        strict_metadata=True,
        heads=heads,
        resolutions=(resolution,),
    )
    return [
        _snapshot_from_named_outputs(
            outputs,
            selector,
            resolution=resolution,
            first_bin=first_bin,
            last_bin=last_bin,
            interval=interval,
        )
        for selector in selectors
    ]


def _snapshot_from_named_outputs(
    outputs: Any,
    selector: TrackSelector,
    *,
    resolution: int,
    first_bin: int,
    last_bin: int,
    interval: ModelInterval,
) -> TrackSnapshot:
    try:
        selected = outputs[selector.output_type].select(**dict(selector.metadata))[
            resolution
        ]
    except (AttributeError, KeyError, ValueError) as exc:
        raise AlphaGenomePyTorchError(
            f"Could not select {selector.output_type!r} track: {exc}"
        ) from exc
    if len(selected.tracks) != 1:
        raise AlphaGenomePyTorchError(
            f"Selector for {selector.output_type!r} matched "
            f"{len(selected.tracks)} tracks; expected exactly one."
        )
    try:
        values = selected.tensor[0, first_bin:last_bin, 0]
    except (IndexError, TypeError) as exc:
        raise AlphaGenomePyTorchError(
            "Selected output must have shape (batch, positional_bins, tracks)."
        ) from exc
    values = _to_cpu_values(values)
    metadata = _metadata_record(selected.tracks[0])
    return TrackSnapshot(
        values=values,
        metadata=(metadata,),
        resolution=resolution,
        interval=interval,
    )


def _to_cpu_values(values: Any) -> Any:
    if hasattr(values, "detach"):
        values = values.detach()
    if hasattr(values, "cpu"):
        values = values.cpu()
    if hasattr(values, "numpy"):
        values = values.numpy()
    try:
        return values.reshape(-1, 1)
    except (AttributeError, ValueError) as exc:
        raise AlphaGenomePyTorchError(
            "Selected output could not become a one-track CPU array."
        ) from exc


def _metadata_record(metadata: Any) -> dict[str, Any]:
    if hasattr(metadata, "to_dict"):
        record = dict(metadata.to_dict())
    elif isinstance(metadata, Mapping):
        record = dict(metadata)
    else:
        raise AlphaGenomePyTorchError("Selected track metadata is not serializable.")
    track_name = record.get("track_name") or record.get("name")
    if not track_name:
        raise AlphaGenomePyTorchError("Selected track metadata has no track name.")
    record["name"] = str(track_name)
    record["strand"] = str(record.get("strand") or ".")
    return record


def _crop_bounds(
    model_interval: ModelInterval,
    display_interval: ModelInterval,
    resolution: int,
) -> tuple[int, int, ModelInterval]:
    if resolution <= 0 or model_interval.width % resolution:
        raise AlphaGenomePyTorchError(
            "Model interval width must be divisible by the output resolution."
        )
    if (
        display_interval.chromosome != model_interval.chromosome
        or display_interval.start < model_interval.start
        or display_interval.end > model_interval.end
        or display_interval.start >= display_interval.end
    ):
        raise AlphaGenomePyTorchError(
            "Display interval must be a positive subinterval of the model interval."
        )
    first_bin = (
        display_interval.start - model_interval.start + resolution - 1
    ) // resolution
    last_bin = (display_interval.end - model_interval.start) // resolution
    if first_bin >= last_bin:
        raise AlphaGenomePyTorchError(
            "Display interval contains no complete prediction bins."
        )
    cropped_interval = ModelInterval(
        model_interval.chromosome,
        model_interval.start + first_bin * resolution,
        model_interval.start + last_bin * resolution,
    )
    return first_bin, last_bin, cropped_interval
