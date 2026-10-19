"""Public data access and counterexamples to incompatible upstream shortcuts."""

import warnings

import numpy as np
import pandas as pd
import pytest

import genome_spy.integrations.scanpy as gsc
from genome_spy.integrations.scanpy._grouped_data import (
    expression_fractions,
    group_means,
    scale_values,
)
from tests.integrations.scanpy.fixture_data import make_adata
from tests.integrations.scanpy.grouped_fixture import make_grouped_adata

sc = pytest.importorskip("scanpy")


@pytest.mark.parametrize("family", ["dotplot", "matrixplot"])
@pytest.mark.parametrize("options", [{}, {"layer": "counts"}])
@pytest.mark.parametrize("interactive", [False, True])
def test_grouped_plots_read_unique_keys_once_through_scanpy(
    monkeypatch, family, options, interactive
):
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", UserWarning)
        a = make_grouped_adata()
    original, calls = sc.get.obs_df, []

    def read(adata, **kwargs):
        calls.append((adata, kwargs))
        frame = original(adata, **kwargs)
        frame["g1"] += 100
        return frame

    monkeypatch.setattr(sc.get, "obs_df", read)
    flags = (
        {"zoom": True, "highlight" if family == "dotplot" else "show_values": True}
        if interactive
        else {}
    )
    chart = getattr(gsc.pl, family)(
        a, ["g2", "g1", "g2"], "group", show=False, **options, **flags
    )
    assert len(calls) == 1 and calls[0][0] is a
    assert calls[0][1] == {
        "keys": ["group", "g2", "g1"],
        "use_raw": not options,
        "layer": options.get("layer"),
        "gene_symbols": None,
    }
    spec = chart.to_dict()
    records = next(rows for rows in spec["datasets"].values() if "_mean" in rows[0])
    mean = next(
        r["_mean"] for r in records if r["_group"] == "B" and r["_gene"] == "g1"
    )
    assert mean == pytest.approx(100 + (10 if options else 23 / 3))


@pytest.mark.parametrize(
    "options,source,expected",
    [
        ({}, "raw", [i % 4 for i in range(8)]),
        ({"use_raw": False}, "X", [i % 3 for i in range(8)]),
        ({"layer": "counts"}, "counts", [10 * (i % 3) for i in range(8)]),
    ],
)
def test_umap_reuses_public_vector_access_once_and_retains_coordinates(
    monkeypatch, options, source, expected
):
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", UserWarning)
        a = make_adata()
    coordinates = a.obsm["X_umap"].copy()
    calls = []
    owner = type(a.raw) if source == "raw" else type(a)
    original = owner.obs_vector

    def read(self, key, **kwargs):
        calls.append((key, kwargs))
        return original(self, key, **kwargs).copy() + 100

    monkeypatch.setattr(owner, "obs_vector", read)
    chart = gsc.pl.umap(a, color=["g1", "g1"], show=False, **options)
    assert calls == [("g1", {} if source == "raw" else {"layer": options.get("layer")})]
    records = next(iter(chart.to_dict()["datasets"].values()))
    assert [r["_value_0"] for r in records] == [100 + v for v in expected]
    assert [r["_value_1"] for r in records] == [100 + v for v in expected]
    np.testing.assert_array_equal(
        [[r["_coord_0"], r["_coord_1"]] for r in records], coordinates[:, :2]
    )
    np.testing.assert_array_equal(a.obsm["X_umap"], coordinates)


def test_aggregate_is_not_the_plotting_mean_or_expression_fraction():
    import anndata as ad

    values = pd.DataFrame(
        {"g1": [-1.0, 0, 1, 4], "g2": [np.nan, 2.0, 3, 4]},
        index=pd.CategoricalIndex(["A", "A", "B", "B"]),
    )
    a = ad.AnnData(
        values.to_numpy(),
        obs=pd.DataFrame({"group": values.index}, index=list("abcd")),
        var=pd.DataFrame(index=values.columns),
    )
    aggregated = sc.get.aggregate(a, by="group", func=["mean", "count_nonzero"])
    assert group_means(values).loc["A", "g2"] == 2
    assert np.isnan(aggregated.layers["mean"][0, 1])
    assert expression_fractions(values).loc["A", "g1"] == 0
    assert aggregated.layers["count_nonzero"][0, 0] / 2 == 0.5


def test_plotting_standard_scale_is_not_scanpy_preprocessing_scale():
    values = pd.DataFrame({"g": [1.0, 3.0, 5.0]})
    assert scale_values(values, "var")["g"].tolist() == [0, 0.5, 1]
    np.testing.assert_allclose(
        sc.pp.scale(values.to_numpy(), copy=True).ravel(), [-1, 0, 1]
    )
