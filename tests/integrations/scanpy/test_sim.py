"""Simulation metadata, fixed shuffle and shared renderers against public Scanpy."""

import inspect
import warnings

import numpy as np
import pytest
from scipy import sparse

import genome_spy.integrations.scanpy as gsc
from genome_spy.integrations.scanpy._timeseries_data import prepare_sim
from tests.integrations.scanpy.helpers import leaf_marks
from tests.integrations.scanpy.sim_fixture import make_sim, sim_cases


def test_signature_preserves_scanpy_and_adds_native_options():
    import scanpy as sc

    native = inspect.signature(gsc.pl.sim).parameters
    for name, parameter in inspect.signature(sc.pl.sim).parameters.items():
        assert native[name].kind == parameter.kind
        assert native[name].default == parameter.default
    assert set(native) - set(inspect.signature(sc.pl.sim).parameters) == {
        "hover",
        "zoom",
        "show_values",
        "width",
        "height",
    }


@pytest.mark.parametrize("case", sim_cases())
def test_values_boundaries_ticks_and_limits_match_scanpy(case, monkeypatch):
    import matplotlib.pyplot as plt
    import scanpy as sc

    adata, options = make_sim(), sim_cases()[case]
    before = adata.copy()
    state = np.random.get_state()
    try:
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            sc.pl.sim(adata, show=False, **options)
        ax = plt.gcf().axes[0]
        heatmap = bool(ax.images)
        expected = (
            np.asarray(ax.images[0].get_array())
            if heatmap
            else np.ma.concatenate([c.get_offsets() for c in ax.collections])
        )
        limits = [ax.get_xlim(), ax.get_ylim()]
        ticks = ax.get_xticks().tolist()
        labels = [label.get_text() for label in ax.get_xticklabels()]
        highlights = [line.get_xdata()[0] for line in ax.lines]
        xlabel = ax.get_xlabel()
        plt.close("all")
    finally:
        np.random.set_state(state)
    monkeypatch.setattr(
        sc.pl, "sim", lambda *a, **k: pytest.fail("Called upstream renderer")
    )
    monkeypatch.setattr(sc.tl, "sim", lambda *a, **k: pytest.fail("Ran simulation"))
    spec = gsc.pl.sim(adata, show=False, **options).to_dict()
    mark = next(
        m
        for m in leaf_marks(spec)
        if m.get("mark", {}).get("type") == ("rect" if heatmap else "point")
    )
    table = spec["datasets"][mark["data"]["name"]]
    if heatmap:
        actual = np.array([r["_value"] for r in table]).reshape(
            adata.n_vars, adata.n_obs
        )
        scales = spec["scales"]
    else:
        actual = np.array([[r["_time"], r["_value"]] for r in table])
        scales = {axis: mark["encoding"][axis]["scale"] for axis in ("x", "y")}
    np.testing.assert_array_equal(actual, expected)
    for axis, domain in zip(("x", "y"), limits):
        np.testing.assert_allclose(scales[axis]["domain"], domain)
    rules = [m for m in leaf_marks(spec) if m.get("mark", {}).get("type") == "rule"]
    actual_highlights = spec["datasets"][rules[0]["data"]["name"]] if rules else []
    assert [r["position"] for r in actual_highlights] == highlights
    if not options.get("shuffle"):
        track = spec["surround"]["bottom"][0]
        rows = spec["datasets"][track["data"]["name"]]
        assert [r["position"] for r in rows] == ticks
        assert [r["label"] for r in rows] == labels
    assert mark["encoding"]["x"]["axis"]["title"] == (
        xlabel if options.get("shuffle") else None
    )
    np.testing.assert_array_equal(adata.X, before.X)
    assert adata.uns == before.uns and adata.var_names.equals(before.var_names)


def test_length_fallback_and_shuffle_are_read_only_and_preserve_global_rng():
    adata = make_sim()
    del adata.uns["tmax_write"]
    _, boundaries, ticks = prepare_sim(adata, None, False)
    assert boundaries == [] and ticks == {0: "1"}
    state = np.random.get_state()
    expected = np.random.RandomState(1).choice(adata.n_obs, adata.n_obs, replace=False)
    for source in (adata, adata[:5]):
        before = source.X.copy()
        spec = gsc.pl.sim(source, shuffle=True, show=False).to_dict()
        mark = next(m for m in leaf_marks(spec) if m["mark"]["type"] == "point")
        rows = spec["datasets"][mark["data"]["name"]]
        order = (
            expected
            if source is adata
            else np.random.RandomState(1).choice(5, 5, replace=False)
        )
        np.testing.assert_array_equal(
            [r["_value"] for r in rows], before[order].T.ravel()
        )
        np.testing.assert_array_equal(source.X, before)
    after = np.random.get_state()
    assert state[0] == after[0] and state[2:] == after[2:]
    np.testing.assert_array_equal(state[1], after[1])


def test_backed_and_sparse_sources_are_rejected_before_loading(tmp_path, monkeypatch):
    import anndata as ad

    adata = make_sim()
    adata.write_h5ad(tmp_path / "simulation.h5ad")
    backed = ad.read_h5ad(tmp_path / "simulation.h5ad", backed="r")
    try:
        sources = [backed, backed[:2]]
        with monkeypatch.context() as guarded:
            guarded.setattr(
                ad.AnnData, "X", property(lambda self: pytest.fail("Read backed X"))
            )
            for source in sources:
                with pytest.raises(TypeError, match="backed/lazy"):
                    gsc.pl.sim(source, show=False)
    finally:
        backed.file.close()
    adata.X = sparse.csr_matrix(adata.X)
    monkeypatch.setattr(
        sparse.csr_matrix, "toarray", lambda *a, **k: pytest.fail("Densified sparse X")
    )
    with pytest.raises(TypeError, match="resident"):
        gsc.pl.sim(adata, show=False)


@pytest.mark.parametrize("length", [0, -1, np.inf, np.nan, True, "3"])
@pytest.mark.parametrize("stored", [False, True])
def test_invalid_realization_lengths_fail_clearly(length, stored):
    adata = make_sim()
    options = {"tmax_realization": length}
    if stored:
        adata.uns["tmax_write"] = length
        options = {}
    with pytest.raises(ValueError, match=r"gsc\.pl\.sim:.*tmax"):
        gsc.pl.sim(adata, show=False, **options)


@pytest.mark.parametrize(
    "options",
    [
        {"as_heatmap": 1},
        {"shuffle": "yes"},
        {"hover": 1},
        {"show_values": "yes"},
        {"zoom": "x"},
    ],
)
def test_invalid_flags_fail_before_optional_import(options, monkeypatch):
    monkeypatch.setattr(
        gsc.pl, "_require_scanpy", lambda *a: pytest.fail("Imported Scanpy")
    )
    with pytest.raises(TypeError, match=r"gsc\.pl\.sim:"):
        gsc.pl.sim(object(), **options)


def test_point_value_labels_and_single_variable_profiles_fail_clearly():
    with pytest.raises(NotImplementedError, match="show_values"):
        gsc.pl.sim(make_sim(), show_values=True, show=False)
    with pytest.raises(ValueError, match="requires color"):
        gsc.pl.sim(make_sim()[:, :1], show=False)
