"""Optional integration imports and missing-extra errors in the base environment."""

import subprocess
import sys

import pytest

import genome_spy.integrations.scanpy as gsc
from genome_spy.integrations.scanpy import _guards


@pytest.mark.parametrize(
    "namespace",
    [
        "genome_spy",
        "genome_spy.integrations",
        "genome_spy.integrations.scanpy",
        *[
            f"genome_spy.integrations.scanpy.{family}"
            for family in (
                "_embedding",
                "_expression",
                "_paga",
                "_timeseries",
                "_qc",
                "_ranking",
            )
        ],
    ],
)
def test_namespace_import_keeps_optional_stack_unloaded(namespace: str) -> None:
    subprocess.run(
        [
            sys.executable,
            "-c",
            f"import sys; import {namespace}; assert not set(['scanpy', 'anndata', 'numpy', 'pandas', 'scipy', 'matplotlib', 'pyarrow']) & sys.modules.keys()",
        ],
        check=True,
    )


@pytest.mark.parametrize("context", ["umap", "DotPlot", "MatrixPlot"])
def test_missing_optional_dependency_has_an_actionable_error(
    monkeypatch, context
) -> None:
    def missing(_):
        raise _guards.PackageNotFoundError("scanpy")

    monkeypatch.setattr(_guards, "version", missing)
    with pytest.raises(
        ImportError, match=rf"gsc.pl.{context} requires genome-spy-python\[scanpy\]"
    ):
        if context != "umap":
            getattr(gsc.pl, context)(object(), ["g1"], "group")
        else:
            gsc.pl.umap(object(), show=False)
