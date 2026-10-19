"""Shared stored-coordinate semantics and Scanpy-compatible embedding wrappers."""

from copy import deepcopy
from hashlib import sha256
import inspect
import json
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

import genome_spy as gs
import genome_spy.integrations.scanpy as gsc
from tests.integrations.scanpy.embedding_fixture import (
    embedding_cases,
    make_embedding_adata,
)
from tests.integrations.scanpy.helpers import points, units

sc = pytest.importorskip("scanpy")
FAMILIES = ["embedding", "umap", "tsne", "diffmap", "draw_graph", "pca", "pca_scatter"]


@pytest.mark.parametrize("case", embedding_cases())
def test_complete_embedding_specs_match_pinned_reference_coordinates_and_labels(case):
    from matplotlib.colors import to_hex

    manifest = json.loads(
        (Path(__file__).with_name("fixtures") / "embedding.json").read_text()
    )
    assert (
        manifest["input_sha256"]
        == sha256(
            Path(__file__).with_name("embedding_fixture.py").read_bytes()
        ).hexdigest()
    )
    expected = manifest["cases"][case]
    family, options = embedding_cases()[case]
    spec = getattr(gsc.pl, family)(
        make_embedding_adata(),
        size=np.arange(8) * 7 + 25,
        frameon=True,
        show=False,
        **options,
    ).to_dict()
    mark = points(spec)
    data = sorted(next(iter(spec["datasets"].values())), key=lambda r: r["_order_0"])
    fields = [mark["encoding"][axis]["field"] for axis in ("x", "y")]
    np.testing.assert_array_equal(
        [[row[field] for field in fields] for row in data], expected["coordinates"]
    )
    np.testing.assert_array_equal([r["_size_0"] for r in data], expected["sizes"])
    assert [mark["encoding"][axis]["axis"]["title"] for axis in ("x", "y")] == expected[
        "labels"
    ]
    for axis in ("x", "y"):
        np.testing.assert_allclose(
            mark["encoding"][axis]["scale"]["domain"], expected[f"{axis}_domain"]
        )
    assert spec["title"]["text"] == expected["title"]
    color = mark["encoding"]["color"]
    if expected["legend"] is not None:
        assert color["legend"]["values"] == expected["legend"]
        paints = dict(
            zip(color["scale"]["domain"], color["scale"]["range"], strict=True)
        )
        assert [
            to_hex(paints[r["_color_0"]], keep_alpha=True) for r in data
        ] == expected["colors"]
    else:
        assert color["scale"]["domain"] == expected["color_domain"]


@pytest.mark.parametrize("family", FAMILIES)
def test_effective_signatures_match_pinned_scanpy_with_only_native_additions(family):
    native = inspect.signature(getattr(gsc.pl, family)).parameters
    upstream = inspect.signature(getattr(sc.pl, family)).parameters
    for name, p in upstream.items():
        if name in {"ax", "return_fig"}:
            assert name not in native
        else:
            assert native[name].kind == p.kind and native[name].default == p.default
    assert set(native) - set(upstream) == {
        "hover",
        "zoom",
        "selection",
        "obs_id",
        "width",
        "height",
    }
    assert all(
        native[name].kind == inspect.Parameter.KEYWORD_ONLY
        for name in set(native) - set(upstream)
    )
    assert gsc.pl.pca_scatter is gsc.pl.pca


@pytest.mark.parametrize(
    "family,basis",
    [
        ("umap", "umap"),
        ("tsne", "tsne"),
        ("diffmap", "diffmap"),
        ("draw_graph", "draw_graph_fa"),
        ("pca", "pca"),
        ("pca_scatter", "pca"),
    ],
)
def test_aliases_are_exactly_the_shared_embedding_chart(family, basis):
    a = make_embedding_adata()
    options = dict(
        color=["cell_type", "g1"],
        dimensions=(1, 2),
        obs_id="cell_id",
        zoom=True,
        show=False,
    )
    actual = getattr(gsc.pl, family)(a, **options).to_dict()
    expected = gsc.pl.embedding(a, basis, **options).to_dict()
    assert actual == expected


def test_basis_precedence_and_dataframe_coordinates_retain_source_precision():
    a = make_embedding_adata()
    a.obsm["tsne"] = pd.DataFrame(a.obsm["X_tsne"] * 7, index=a.obs_names)
    chart = gsc.pl.tsne(a, dimensions=(2, 0), show=False).to_dict()
    records = next(iter(chart["datasets"].values()))
    np.testing.assert_array_equal(
        [[r["_coord_2"], r["_coord_0"]] for r in records],
        a.obsm["tsne"].iloc[:, [2, 0]],
    )
    assert {r["_obs_id"] for r in records} == {f"row-{i}" for i in range(8)}
    direct = gsc.pl.embedding(a, "X_tsne", show=False).to_dict()
    assert direct["encoding"]["x"]["axis"]["title"] == "X_tsne1"


def test_component_broadcasting_uses_shared_panels_and_one_color_read(monkeypatch):
    a = make_embedding_adata()
    getter, calls = type(a.raw).obs_vector, []

    def read(owner, key):
        calls.append(key)
        return getter(owner, key)

    monkeypatch.setattr(type(a.raw), "obs_vector", read)
    spec = gsc.pl.embedding(
        a, "custom", color="g1", components="all", show=False
    ).to_dict()
    assert calls == ["g1"] and len(units(spec)) == 3 and len(spec["datasets"]) == 1
    assert [
        [points(p)["encoding"][axis]["axis"]["title"] for axis in ("x", "y")]
        for p in units(spec)
    ] == [["custom1", "custom2"], ["custom1", "custom3"], ["custom2", "custom3"]]


def test_diffmap_default_uses_first_two_stored_columns():
    a = make_embedding_adata()
    spec = gsc.pl.diffmap(a, show=False).to_dict()
    assert [spec["encoding"][axis]["axis"]["title"] for axis in ("x", "y")] == [
        "DC1",
        "DC2",
    ]
    data = next(iter(spec["datasets"].values()))
    np.testing.assert_array_equal(
        [[r["_coord_0"], r["_coord_1"]] for r in data], a.obsm["X_diffmap"][:, :2]
    )


def test_pca_variance_labels_and_hover_use_the_same_stored_metadata():
    a = make_embedding_adata()
    before = deepcopy(a.uns["pca"])
    spec = gsc.pl.pca(
        a, dimensions=(2, 0), annotate_var_explained=True, show=False
    ).to_dict()
    expected = ["PC3 (12.5%)", "PC1 (50.0%)"]
    assert [spec["encoding"][axis]["axis"]["title"] for axis in ("x", "y")] == expected
    assert [item["title"] for item in spec["encoding"]["tooltip"][-2:]] == expected
    np.testing.assert_array_equal(
        a.uns["pca"]["variance_ratio"], before["variance_ratio"]
    )
    a.uns["pca"]["variance_ratio"] = [0.5, 0.25]
    assert gsc.pl.pca(a, annotate_var_explained=True, show=False) is not None
    with pytest.raises(ValueError, match="variance_ratio"):
        gsc.pl.pca(a, components="2,3", annotate_var_explained=True, show=False)
    del a.uns["pca"]
    assert gsc.pl.pca(a, show=False) is not None


def test_draw_graph_layout_is_explicit_or_comes_from_saved_params():
    a = make_embedding_adata()
    assert (
        gsc.pl.draw_graph(a, show=False).to_dict()
        == gsc.pl.draw_graph(a, layout="fa", show=False).to_dict()
    )
    del a.uns["draw_graph"]
    assert (
        gsc.pl.draw_graph(a, layout="fr", show=False).to_dict()["encoding"]["x"][
            "axis"
        ]["title"]
        == "FR1"
    )
    with pytest.raises(ValueError, match="layout"):
        gsc.pl.draw_graph(a, show=False)
    with pytest.raises(ValueError, match="X_draw_graph_missing"):
        gsc.pl.draw_graph(a, layout="missing", show=False)


@pytest.mark.parametrize("stored", [None, [], {"params": None}])
def test_malformed_embedding_metadata_fails_with_a_named_error(stored):
    a = make_embedding_adata()
    a.uns["draw_graph"] = stored
    with pytest.raises(ValueError, match="gsc.pl.draw_graph.*layout"):
        gsc.pl.draw_graph(a, show=False)
    a.uns["pca"] = stored
    with pytest.raises(ValueError, match="gsc.pl.pca.*variance_ratio"):
        gsc.pl.pca(a, annotate_var_explained=True, show=False)


@pytest.mark.parametrize("family", FAMILIES)
def test_plotting_and_python_selection_never_run_embedding_analysis(
    monkeypatch, family
):
    a = make_embedding_adata()
    before = {k: np.asarray(v).copy() for k, v in a.obsm.items()}
    for name in ("umap", "tsne", "diffmap", "draw_graph", "pca"):
        monkeypatch.setattr(sc.tl, name, lambda *a, **k: pytest.fail("Ran analysis"))
    monkeypatch.setattr(
        sc.pp, "neighbors", lambda *a, **k: pytest.fail("Ran neighbors")
    )
    options = {"basis": "custom"} if family == "embedding" else {}
    brush = gs.selection_interval("cells", encodings=["x", "y"])
    spec = getattr(gsc.pl, family)(
        a, color=["cell_type", "g1"], selection=brush, show=False, **options
    ).to_dict()
    assert len(spec["datasets"]) == 1
    for key, values in before.items():
        np.testing.assert_array_equal(a.obsm[key], values)
    basis = (
        "custom"
        if family == "embedding"
        else "draw_graph_fa"
        if family == "draw_graph"
        else "pca"
        if family == "pca_scatter"
        else family
    )
    key = basis if basis in a.obsm else f"X_{basis}"
    coordinates = np.asarray(a.obsm[key])
    low, high = np.quantile(coordinates[:, :2], [0.25, 0.75], axis=0)
    snapshot = {
        "type": "interval",
        "intervals": {"x": [low[0], high[0]], "y": [low[1], high[1]]},
    }
    expected = ((coordinates[:, :2] >= low) & (coordinates[:, :2] < high)).all(axis=1)
    np.testing.assert_array_equal(
        gsc.selection_mask(a, snapshot, basis=basis), expected
    )
    reordered = a[[7, 0, 3], :]
    np.testing.assert_array_equal(
        gsc.selection_mask(reordered, snapshot, basis=basis), expected[[7, 0, 3]]
    )


def test_stored_bases_and_observation_colors_work_without_expression_even_backed(
    tmp_path, monkeypatch
):
    import anndata as ad

    a = make_embedding_adata()
    path = tmp_path / "embeddings.h5ad"
    a.write_h5ad(path)
    backed = ad.read_h5ad(path, backed="r")
    try:
        spec = gsc.pl.pca(backed, color="cell_type", show=False).to_dict()
        assert len(next(iter(spec["datasets"].values()))) == 8
        assert len(gsc.selection_mask(backed, None, basis="pca")) == 8
        with pytest.raises(TypeError, match="backed"):
            gsc.pl.pca(backed, color="g1", show=False)
    finally:
        backed.file.close()


@pytest.mark.parametrize("basis", ["missing", None, ""])
def test_missing_or_invalid_basis_fails_without_analysis(basis):
    with pytest.raises(ValueError, match="basis|missing"):
        gsc.pl.embedding(make_embedding_adata(), basis, show=False)


def test_unsupported_internal_options_and_projection_fail_before_optional_imports(
    monkeypatch,
):
    monkeypatch.setattr(
        gsc.pl, "_require_scanpy", lambda *a: pytest.fail("Imported Scanpy")
    )
    for options in [
        {"context": "test"},
        {"annotate_var_explained": True},
        {"projection": "3d"},
    ]:
        with pytest.raises((TypeError, NotImplementedError)):
            gsc.pl.embedding(object(), "pca", **options)
