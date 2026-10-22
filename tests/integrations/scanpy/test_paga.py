"""Public PAGA reference semantics, metadata-only layout reuse and deliberate cache writes."""

import inspect
import warnings

import numpy as np
import pandas as pd
import pytest

import genome_spy.integrations.scanpy as gsc
from tests.integrations.scanpy.helpers import leaf_marks
from tests.integrations.scanpy.paga_fixture import POSITIONS, make_paga, paga_cases


def test_signature_retains_scanpy_defaults_except_omitted_matplotlib_axes():
    import scanpy as sc

    actual = inspect.signature(gsc.pl.paga).parameters
    expected = inspect.signature(sc.pl.paga).parameters
    for key, param in expected.items():
        if key in {"ax", "cax"}:
            assert key not in actual
        else:
            assert actual[key].kind == param.kind
            assert actual[key].default == param.default
    assert actual.keys() - expected.keys() == {
        "hover",
        "zoom",
        "width",
        "height",
        "kwargs",
    }


@pytest.mark.parametrize("case", paga_cases())
def test_nodes_edges_labels_bounds_and_cache_match_public_scanpy(case, monkeypatch):
    import matplotlib.pyplot as plt
    from matplotlib.colors import to_rgba
    from matplotlib.collections import LineCollection, PathCollection
    import scanpy as sc

    a = make_paga(case)
    options = paga_cases()[case]
    reference = a.copy()
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        ax = sc.pl.paga(reference, show=False, **options)
    point = next(c for c in ax.collections if isinstance(c, PathCollection))
    positions = np.asarray(point.get_offsets())
    areas = point.get_sizes()
    colors = point.get_facecolors()
    expected_edges = [
        (c.get_segments(), c.get_linewidths())
        for c in ax.collections
        if isinstance(c, LineCollection)
    ]
    labels = [t.get_text() for t in ax.texts]
    bounds = [ax.get_xlim(), ax.get_ylim()]
    plt.close("all")
    original = sc.pl.paga
    layout_calls = []

    def layout_only(data, **kwargs):
        assert data is not a and kwargs["plot"] is False
        layout_calls.append(kwargs)
        return original(data, **kwargs)

    monkeypatch.setattr(sc.pl, "paga", layout_only)
    monkeypatch.setattr(
        sc.tl, "paga", lambda *a, **k: pytest.fail("Reran PAGA analysis")
    )
    monkeypatch.setattr(
        plt, "figure", lambda *a, **k: pytest.fail("Created a Matplotlib figure")
    )
    monkeypatch.setattr(
        plt, "subplots", lambda *a, **k: pytest.fail("Created Matplotlib axes")
    )
    before = a.obs.copy(deep=True)
    stored = a.uns["paga"]["connectivities"].copy()
    old_pos = a.uns["paga"]["pos"].copy()
    spec = gsc.pl.paga(a, show=False, **options).to_dict()
    assert bool(layout_calls) == ("pos" not in options)
    mark = next(m for m in leaf_marks(spec) if m["mark"]["type"] == "point")
    rows = spec["datasets"][mark["data"]["name"]]
    np.testing.assert_allclose(
        [[r["_x"], r["_y"]] for r in rows], positions, atol=1e-10
    )
    np.testing.assert_allclose([r["_area"] for r in rows], areas)
    np.testing.assert_allclose([to_rgba(r["_color"]) for r in rows], colors)
    assert [r["_label"] for r in rows] == labels
    for axis, domain in zip(("x", "y"), bounds, strict=True):
        np.testing.assert_allclose(mark["encoding"][axis]["scale"]["domain"], domain)
    rules = [m for m in leaf_marks(spec) if m["mark"]["type"] == "rule"]
    assert len(rules) == len(expected_edges)
    for rule, (segments, widths) in zip(rules, expected_edges, strict=True):
        edges = spec["datasets"][rule["data"]["name"]]
        np.testing.assert_allclose(
            [[[r["_x"], r["_y"]], [r["_x2"], r["_y2"]]] for r in edges], segments
        )
        np.testing.assert_allclose([r["_width"] for r in edges], widths)
    np.testing.assert_allclose(
        a.uns["paga"]["pos"], positions if options.get("add_pos", True) else old_pos
    )
    pd.testing.assert_frame_equal(a.obs, before)
    assert (a.uns["paga"]["connectivities"] != stored).nnz == 0


@pytest.mark.parametrize("plot", [False, True])
@pytest.mark.parametrize("add_pos", [False, True])
def test_layout_never_reads_expression_or_creates_a_figure(plot, add_pos, monkeypatch):
    from anndata import AnnData
    import scanpy as sc
    import matplotlib.pyplot as plt

    a = make_paga()
    old = a.uns["paga"]["pos"].copy()
    for name in ("X", "raw", "layers"):
        original = inspect.getattr_static(AnnData, name)

        def guarded(self, _original=original):
            if self is a:
                pytest.fail("Read caller expression")
            return _original.__get__(self, type(self))

        monkeypatch.setattr(
            AnnData,
            name,
            property(guarded, original.__set__),
        )
    monkeypatch.setattr(sc.tl, "paga", lambda *a, **k: pytest.fail("Ran PAGA analysis"))
    monkeypatch.setattr(plt, "figure", lambda *a, **k: pytest.fail("Created figure"))
    result = gsc.pl.paga(a, plot=plot, add_pos=add_pos, show=False)
    assert (result is not None) == plot
    assert np.array_equal(a.uns["paga"]["pos"], old) is not add_pos


def test_supplied_positions_skip_layout_and_failures_leave_caches_unchanged(
    monkeypatch,
):
    import scanpy as sc

    a = make_paga()
    old = a.uns["paga"]["pos"].copy()
    monkeypatch.setattr(sc.pl, "paga", lambda *a, **k: pytest.fail("Computed layout"))
    gsc.pl.paga(a, pos=POSITIONS, add_pos=False, show=False)
    np.testing.assert_array_equal(a.uns["paga"]["pos"], old)
    with pytest.raises(ValueError, match="labels"):
        gsc.pl.paga(a, pos=POSITIONS, labels=["short"], show=False)
    np.testing.assert_array_equal(a.uns["paga"]["pos"], old)


@pytest.mark.parametrize(
    "option",
    [
        {"transitions": "velocity"},
        {"single_component": True},
        {"export_to_gexf": True},
        {"fontoutline": 2},
        {"text_kwds": {"color": "red"}},
        {"left_margin": 0.2},
        {"cb_kwds": {"ticks": []}},
        {"colorbar": True},
    ],
)
def test_unsupported_options_fail_before_imports_or_writes(option, monkeypatch):
    monkeypatch.setattr(
        gsc.pl, "_require_scanpy", lambda *a: pytest.fail("Imported Scanpy")
    )
    with pytest.raises(NotImplementedError, match="gsc.pl.paga:.*unsupported"):
        gsc.pl.paga(object(), **option)


@pytest.mark.parametrize(
    "option",
    [{"ax": object()}, {"cax": object()}, {"plot": 1}, {"add_pos": 1}, {"zoom": "xy"}],
)
def test_invalid_flags_and_axes_fail_clearly(option):
    with pytest.raises(TypeError, match="gsc.pl.paga:"):
        gsc.pl.paga(object(), **option)


@pytest.mark.parametrize(
    "change,error",
    [
        ("missing", ValueError),
        ("uncategorical", ValueError),
        ("shape", ValueError),
        ("nan", ValueError),
        ("loop", NotImplementedError),
    ],
)
def test_invalid_stored_graphs_are_not_recomputed(change, error):
    from scipy import sparse

    a = make_paga()
    if change == "missing":
        del a.uns["paga"]
    elif change == "uncategorical":
        a.obs["cluster"] = a.obs["cluster"].astype(str)
    elif change == "shape":
        a.uns["paga"]["connectivities"] = sparse.csr_matrix((3, 3))
    elif change == "nan":
        a.uns["paga"]["connectivities"].data[0] = np.nan
    elif change == "loop":
        graph = a.uns["paga"]["connectivities"].tolil()
        graph[0, 0] = 0.2
        a.uns["paga"]["connectivities"] = graph
    with pytest.raises(error, match="gsc.pl.paga:"):
        gsc.pl.paga(a, pos=POSITIONS, show=False)


@pytest.mark.parametrize("format", ["csr", "csc", "lil"])
def test_sparse_graph_validation_handles_storage_formats(format):
    a = make_paga()
    graph = a.uns["paga"]["connectivities"].asformat(format)
    a.uns["paga"]["connectivities"] = graph
    assert gsc.pl.paga(a, pos=POSITIONS, show=False) is not None
    graph[0, 1] = np.nan
    with pytest.raises(ValueError, match="graph weights must be finite"):
        gsc.pl.paga(a, pos=POSITIONS, show=False)
