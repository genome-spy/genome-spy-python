from __future__ import annotations

import importlib.util
import sys
import tomllib
from dataclasses import dataclass
from pathlib import Path
from types import ModuleType, SimpleNamespace

import numpy as np
import pytest


@pytest.fixture
def backend() -> ModuleType:
    path = Path("notebooks/alphagenome/_alphagenome_pytorch.py")
    module_spec = importlib.util.spec_from_file_location(path.stem, path)
    if module_spec is None or module_spec.loader is None:
        raise RuntimeError(f"Could not load AlphaGenome PyTorch helper from {path}.")
    module = importlib.util.module_from_spec(module_spec)
    sys.modules[module_spec.name] = module
    module_spec.loader.exec_module(module)
    return module


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


@dataclass(frozen=True)
class _Metadata:
    track_name: str
    strand: str = "."

    def to_dict(self) -> dict[str, str]:
        return {"track_name": self.track_name, "strand": self.strand}


class _SelectedTrack:
    def __init__(self, tensor: np.ndarray, tracks: list[_Metadata]) -> None:
        self.tensor = tensor
        self.tracks = tracks


class _Head:
    def __init__(self, selected: _SelectedTrack) -> None:
        self.selected = selected
        self.criteria: dict[str, object] | None = None

    def select(self, **criteria: object) -> dict[int, _SelectedTrack]:
        self.criteria = criteria
        return {128: self.selected}


def test_apply_snv_validates_reference_and_keeps_length(backend: ModuleType) -> None:
    interval = backend.ModelInterval("chr1", 100, 104)
    variant = backend.ModelVariant("chr1", 102, "C", "T")

    assert backend.apply_snv("ACGT", interval, variant) == "ATGT"

    with pytest.raises(backend.AlphaGenomePyTorchError, match="mismatch"):
        backend.apply_snv("ACGT", interval, backend.ModelVariant("chr1", 102, "G", "T"))
    with pytest.raises(backend.AlphaGenomePyTorchError, match="supports one"):
        backend.apply_snv(
            "ACGT", interval, backend.ModelVariant("chr1", 102, "C", "CA")
        )


def test_snapshot_crops_before_cpu_conversion_and_preserves_metadata(
    backend: ModuleType,
) -> None:
    tensor = np.arange(12, dtype=float).reshape(1, 6, 2)
    selected = _SelectedTrack(tensor[:, :, 1:2], [_Metadata("CL:0001059 DNase-seq")])
    head = _Head(selected)
    selector = backend.TrackSelector("dnase", (("ontology_curie", "CL:0001059"),))

    snapshot = backend._snapshot_from_named_outputs(
        {"dnase": head},
        selector,
        resolution=128,
        first_bin=2,
        last_bin=4,
        interval=backend.ModelInterval("chr1", 256, 512),
    )

    assert snapshot.values.shape == (2, 1)
    assert snapshot.values[:, 0].tolist() == [5.0, 7.0]
    assert snapshot.metadata == (
        {
            "track_name": "CL:0001059 DNase-seq",
            "name": "CL:0001059 DNase-seq",
            "strand": ".",
        },
    )
    assert head.criteria == {"ontology_curie": "CL:0001059"}


def test_crop_bounds_aligns_to_complete_native_bins(backend: ModuleType) -> None:
    model = backend.ModelInterval("chr1", 1_000, 2_024)
    display = backend.ModelInterval("chr1", 1_129, 1_511)

    first, last, cropped = backend._crop_bounds(model, display, 128)

    assert (first, last) == (2, 3)
    assert cropped == backend.ModelInterval("chr1", 1_256, 1_384)


def test_tal1_selectors_are_exact_and_use_only_128bp_capable_heads(
    backend: ModuleType,
) -> None:
    assert {selector.output_type for selector in backend.TAL1_TRACK_SELECTORS} == {
        "rna_seq",
        "dnase",
        "chip_histone",
    }
    assert len(backend.TAL1_TRACK_SELECTORS) == 4
    assert all(
        ("ontology_curie", "CL:0001059") in selector.metadata
        for selector in backend.TAL1_TRACK_SELECTORS
    )
    assert len({selector.signature for selector in backend.TAL1_TRACK_SELECTORS}) == 4
    assert backend.TAL1_TRACK_SELECTORS == tuple(
        track.selector for track in backend.TAL1_DISPLAY_TRACKS
    )


def test_tal1_metadata_catalog_preserves_upstream_track_indices(
    backend: ModuleType,
) -> None:
    class FakeCatalog:
        @classmethod
        def from_rows(cls, rows: list[dict[str, object]]) -> list[dict[str, object]]:
            return rows

    rows = backend._tal1_metadata_catalog(FakeCatalog)

    assert len(rows) == 768 + 384 + 1_152
    selected = [row for row in rows if row["track_name"] != "Padding"]
    assert [
        (row["output_type"], row["track_index"], row["track_name"]) for row in selected
    ] == [
        ("rna_seq", 561, "CL:0001059 polyA plus RNA-seq"),
        ("dnase", 44, "CL:0001059 DNase-seq"),
        (
            "chip_histone",
            206,
            "CL:0001059 Histone ChIP-seq H3K27ac",
        ),
        (
            "chip_histone",
            209,
            "CL:0001059 Histone ChIP-seq H3K4me1",
        ),
    ]
    assert all(row["ontology_curie"] == "CL:0001059" for row in selected)
    assert all(
        row["biosample_name"] == "common myeloid progenitor, CD34-positive"
        for row in selected
    )


def test_prediction_oom_releases_cuda_cache_without_unloading_model(
    backend: ModuleType, monkeypatch: pytest.MonkeyPatch
) -> None:
    class FakeOutOfMemoryError(RuntimeError):
        pass

    events: list[str] = []
    cuda = SimpleNamespace(
        OutOfMemoryError=FakeOutOfMemoryError,
        empty_cache=lambda: events.append("empty_cache"),
    )
    monkeypatch.setitem(sys.modules, "torch", SimpleNamespace(cuda=cuda))
    monkeypatch.setattr(backend.gc, "collect", lambda: events.append("collect"))
    model = object()
    backend._loaded_model = model
    calls = 0

    def predict(*args: object, **kwargs: object) -> list[object]:
        nonlocal calls
        calls += 1
        if calls == 2:
            raise FakeOutOfMemoryError("out of memory")
        return [object()]

    monkeypatch.setattr(backend, "_predict_sequence_tracks", predict)

    with pytest.raises(
        backend.AlphaGenomePyTorchError,
        match="Temporary accelerator allocations were released",
    ):
        backend.predict_variant_tracks(
            model,
            reference_sequence="ACGT",
            model_interval=backend.ModelInterval("chr1", 100, 104),
            display_interval=backend.ModelInterval("chr1", 100, 104),
            variant=backend.ModelVariant("chr1", 102, "C", "T"),
            selectors=(backend.TrackSelector("dnase", ()),),
            resolution=1,
        )

    assert events == ["collect", "empty_cache"]
    assert backend._loaded_model is model


def test_precision_resolution_is_hardware_aware(
    backend: ModuleType, monkeypatch: pytest.MonkeyPatch
) -> None:
    cuda = SimpleNamespace(
        is_available=lambda: True,
        is_bf16_supported=lambda: True,
    )
    monkeypatch.setitem(sys.modules, "torch", SimpleNamespace(cuda=cuda))

    assert backend.resolve_precision("cuda", "auto") == "mixed_precision"
    assert backend.resolve_precision("cpu", "auto") == "full_float32"

    cuda.is_bf16_supported = lambda: False
    assert backend.resolve_precision("cuda", "auto") == "full_float32"
    with pytest.raises(backend.AlphaGenomePyTorchError, match="bfloat16"):
        backend.resolve_precision("cuda", "mixed_precision")


def test_model_replacement_unloads_before_allocating(
    backend: ModuleType, monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    checkpoint = tmp_path / "model.safetensors"
    checkpoint.write_bytes(b"weights")
    events: list[str] = []
    previous = object()
    replacement = object()
    backend._loaded_model = previous
    backend._loaded_model_key = ("old", 1, 1, "cuda", "full_float32")

    def unload() -> None:
        events.append("unload")
        backend._loaded_model = None
        backend._loaded_model_key = None

    def load_fresh(path: Path, *, device: str, precision: str) -> object:
        assert backend._loaded_model is None
        assert path == checkpoint.resolve()
        assert (device, precision) == ("cuda", "mixed_precision")
        events.append("load")
        return replacement

    monkeypatch.setattr(backend, "version", lambda _: backend.PACKAGE_VERSION)
    monkeypatch.setattr(backend, "unload_model", unload)
    monkeypatch.setattr(backend, "_load_fresh_model", load_fresh)

    loaded = backend.load_model(
        checkpoint,
        device="cuda",
        precision="mixed_precision",
    )

    assert loaded is replacement
    assert events == ["unload", "load"]

    checkpoint.write_bytes(b"replacement weights")
    backend.load_model(
        checkpoint,
        device="cuda",
        precision="mixed_precision",
    )
    assert events == ["unload", "load", "unload", "load"]
    assert (
        backend.load_model(
            checkpoint,
            device="cuda",
            precision="mixed_precision",
        )
        is replacement
    )
    assert events == ["unload", "load", "unload", "load"]


def test_model_load_preserves_safetensors_symlink_suffix(
    backend: ModuleType, monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    target = tmp_path / "checkpoint-blob"
    target.write_bytes(b"weights")
    checkpoint = tmp_path / "model.safetensors"
    checkpoint.symlink_to(target)
    loaded = object()
    seen_paths: list[Path] = []

    def load_fresh(path: Path, *, device: str, precision: str) -> object:
        seen_paths.append(path)
        assert path.suffix == ".safetensors"
        assert (device, precision) == ("cuda", "mixed_precision")
        return loaded

    monkeypatch.setattr(backend, "version", lambda _: backend.PACKAGE_VERSION)
    monkeypatch.setattr(backend, "unload_model", lambda: None)
    monkeypatch.setattr(backend, "_load_fresh_model", load_fresh)

    assert (
        backend.load_model(checkpoint, device="cuda", precision="mixed_precision")
        is loaded
    )
    assert seen_paths == [checkpoint.absolute()]


def test_fresh_model_loads_weights_on_cpu_before_device_transfer(
    backend: ModuleType, monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    checkpoint = tmp_path / "model.safetensors"
    checkpoint.write_bytes(b"weights")
    events: list[object] = []

    class FakeModel:
        @classmethod
        def from_pretrained(cls, path: Path, *, dtype_policy: object, device: str):
            events.append(("load", path, dtype_policy, device))
            return cls()

        def to(self, device: str) -> None:
            events.append(("move", device))

        def set_track_metadata_catalog(self, catalog: object) -> None:
            events.append(("metadata", catalog))

        def eval(self) -> None:
            events.append("eval")

    class FakePolicy:
        @staticmethod
        def mixed_precision() -> str:
            return "mixed"

        @staticmethod
        def full_float32() -> str:
            return "float32"

    package = ModuleType("alphagenome_pytorch")
    package.AlphaGenome = FakeModel
    config = ModuleType("alphagenome_pytorch.config")
    config.DtypePolicy = FakePolicy
    named_outputs = ModuleType("alphagenome_pytorch.named_outputs")
    named_outputs.TrackMetadataCatalog = SimpleNamespace(
        from_rows=lambda rows: ("catalog", len(rows))
    )
    monkeypatch.setitem(sys.modules, "alphagenome_pytorch", package)
    monkeypatch.setitem(sys.modules, "alphagenome_pytorch.config", config)

    monkeypatch.setitem(sys.modules, "alphagenome_pytorch.named_outputs", named_outputs)
    backend._load_fresh_model(
        checkpoint,
        device="cuda",
        precision="mixed_precision",
    )

    assert events == [
        ("load", checkpoint, "mixed", "cpu"),
        ("metadata", ("catalog", 2_304)),
        ("move", "cuda"),
        "eval",
    ]


def test_model_dependency_is_scoped_to_the_marimo_launch_command(
    backend: ModuleType,
) -> None:
    project = tomllib.loads(Path("pyproject.toml").read_text(encoding="utf-8"))
    dependency_text = repr(project["project"]["dependencies"]) + repr(
        project.get("dependency-groups", {})
    )
    notebook = Path(
        "notebooks/alphagenome/genome_spy_alphagenome_pytorch.py"
    ).read_text(encoding="utf-8")

    assert "alphagenome-pytorch" not in dependency_text
    assert f"alphagenome-pytorch=={backend.PACKAGE_VERSION}" in notebook
    assert "huggingface-hub==1.27.0" in notebook


def test_checkpoint_identity_distinguishes_local_file_revisions(
    backend: ModuleType, tmp_path: Path
) -> None:
    checkpoint = tmp_path / "model.safetensors"
    checkpoint.write_bytes(b"first")
    first = backend.checkpoint_identity(checkpoint, pinned=False)
    checkpoint.write_bytes(b"second revision")
    second = backend.checkpoint_identity(checkpoint, pinned=False)

    assert first != second
    assert backend.checkpoint_identity(checkpoint, pinned=True) == (
        f"{backend.CHECKPOINT_REPOSITORY}:{backend.CHECKPOINT_FILENAME}"
        f"@{backend.CHECKPOINT_REVISION}"
    )


def test_prediction_cache_is_bounded_and_refreshes_existing_keys(
    backend: ModuleType,
) -> None:
    cache = {"one": 1, "two": 2}

    refreshed = backend.update_prediction_cache(cache, "one", 10, max_entries=2)
    updated = backend.update_prediction_cache(refreshed, "three", 3, max_entries=2)

    assert list(refreshed) == ["two", "one"]
    assert updated == {"one": 10, "three": 3}
    assert cache == {"one": 1, "two": 2}


def test_cropped_backend_snapshots_feed_the_arrow_adapter_directly(
    backend: ModuleType, adapter: ModuleType
) -> None:
    interval = backend.ModelInterval("chr1", 1_024, 1_280)
    selector = backend.TrackSelector(
        "dnase",
        (
            ("track_name", "CL:0001059 DNase-seq"),
            ("ontology_curie", "CL:0001059"),
        ),
    )
    metadata = (
        {
            "name": "CL:0001059 DNase-seq",
            "track_name": "CL:0001059 DNase-seq",
            "ontology_curie": "CL:0001059",
            "strand": ".",
        },
    )
    reference = backend.TrackSnapshot(np.array([[1.0], [2.0]]), metadata, 128, interval)
    alternate = backend.TrackSnapshot(np.array([[1.5], [1.0]]), metadata, 128, interval)

    frame = adapter.adapt_prediction_pairs(
        [backend.TrackSnapshotPair(reference, alternate, selector)],
        request_id="request-1",
        display_interval=interval,
    )

    assert frame.select("start0", "reference", "alternate", "delta").rows() == [
        (1_024, 1.0, 1.5, 0.5),
        (1_152, 2.0, 1.0, -1.0),
    ]
