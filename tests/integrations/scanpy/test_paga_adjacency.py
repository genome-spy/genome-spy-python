"""Pinned legacy adjacency semantics and reuse of the native matrix renderer."""

import inspect

import numpy as np
import pytest
from scipy import sparse

import genome_spy.integrations.scanpy as gsc
from genome_spy.integrations.scanpy._paga.data import adjacency_values, adjacency_points
from tests.integrations.scanpy.helpers import leaf_marks
from tests.integrations.scanpy.paga_fixture import make_adjacency


def test_signature_preserves_upstream_parameters_and_defaults():
    import scanpy as sc

    actual = inspect.signature(gsc.pl.paga_adjacency).parameters
    expected = inspect.signature(sc.pl.paga_adjacency).parameters
    for name, parameter in expected.items():
        assert actual[name].kind == parameter.kind
        assert actual[name].default == parameter.default
    assert actual.keys() - expected.keys() == {
        "hover",
        "zoom",
        "show_values",
        "labels",
        "width",
        "height",
    }


@pytest.mark.parametrize("storage", ["csr", "csc", "lil", "coo", "dok", "bsr"])
@pytest.mark.parametrize(
    "case", ["default", "empty_tree", "constant", "missing", "singleton"]
)
def test_values_and_tree_orientation_match_direct_public_scanpy(storage, case):
    import matplotlib.pyplot as plt
    import scanpy as sc

    a = make_adjacency(storage, case)
    # Scanpy's row indexing requires CSR/CSC/LIL; COO/DOK/BSR share the same values.
    reference = make_adjacency("csr", case)
    plt.close("all")
    sc.pl.paga_adjacency(reference, show=False)
    ax = plt.gcf().axes[0]
    expected = ax.images[0].get_array()
    expected_points = np.concatenate([c.get_offsets() for c in ax.collections])
    values, points = adjacency_values(a, "connectivities", "connectivities_tree")
    np.testing.assert_equal(values, np.asarray(expected))
    np.testing.assert_array_equal(points[["_x", "_y"]], expected_points)
    spec = gsc.pl.paga_adjacency(a, show=False).to_dict()
    marks = leaf_marks(spec)
    assert [m["mark"]["type"] for m in marks] == ["rect", "point"]
    cells = spec["datasets"][marks[0]["data"]["name"]]
    np.testing.assert_equal(
        np.array(
            [np.nan if r["_value"] is None else r["_value"] for r in cells]
        ).reshape(values.shape),
        values,
    )
    if len(points):
        native_points = spec["datasets"][marks[1]["data"]["name"]]
        assert native_points == points.to_dict("records")
    assert spec["scales"]["y"]["reverse"] is True
    assert spec["scales"]["x"]["domain"] == [0, values.shape[1] - 1]
    assert "bandstep" in marks[1]["mark"]["size"]["expr"]
    assert marks[1]["mark"]["strokeWidth"] == 0
    plt.close("all")


@pytest.mark.parametrize("as_heatmap", [True, False])
def test_custom_keys_and_tree_nonzeros_preserve_sources_without_analysis(
    monkeypatch, as_heatmap
):
    import scanpy as sc
    import matplotlib.pyplot as plt

    a = make_adjacency("lil")
    a.uns = {"weights": a.uns["connectivities"], "tree": a.uns["connectivities_tree"]}
    original = {k: (m, m.toarray()) for k, m in a.uns.items()}
    monkeypatch.setattr(sc.tl, "paga", lambda *a, **k: pytest.fail("Reran PAGA"))
    monkeypatch.setattr(
        sc.pp, "neighbors", lambda *a, **k: pytest.fail("Reran neighbors")
    )
    monkeypatch.setattr(plt, "figure", lambda *a, **k: pytest.fail("Created a figure"))
    toarray = sparse.csr_matrix.toarray

    def bounded(matrix, *args, **kwargs):
        assert matrix.shape == (3, 3), "Loaded expression"
        return toarray(matrix, *args, **kwargs)

    monkeypatch.setattr(sparse.csr_matrix, "toarray", bounded)
    chart = gsc.pl.paga_adjacency(
        a,
        adjacency="weights",
        adjacency_tree="tree",
        hover=False,
        as_heatmap=as_heatmap,
        show_values=as_heatmap,
        zoom="xy",
        show=False,
    )
    marks = leaf_marks(chart.to_dict())
    assert [m["mark"]["type"] for m in marks] == (
        ["rect", "text", "point"] if as_heatmap else ["point"]
    )
    assert all(m["mark"].get("tooltip") is None for m in marks)
    assert set(a.uns) == set(original)
    for key, (matrix, values) in original.items():
        assert a.uns[key] is matrix and matrix.format == "lil"
        np.testing.assert_array_equal(matrix.toarray(), values)


@pytest.mark.parametrize(
    "options,error,match",
    [
        (
            {"as_heatmap": False, "show_values": True},
            NotImplementedError,
            "as_heatmap=True",
        ),
        ({"as_heatmap": 1}, TypeError, "as_heatmap"),
        ({"hover": 1}, TypeError, "hover"),
        ({"show_values": "yes"}, TypeError, "show_values"),
        ({"zoom": "x"}, TypeError, "zoom"),
        ({"width": 0}, ValueError, "width"),
        ({"color_map": "invented"}, NotImplementedError, "color_map"),
        ({"ax": None}, TypeError, "ax"),
    ],
)
def test_unsupported_options_fail_clearly(options, error, match):
    with pytest.raises(error, match=match):
        gsc.pl.paga_adjacency(make_adjacency(), show=False, **options)


@pytest.mark.parametrize(
    "key,value,match",
    [
        ("connectivities", None, "stored sparse"),
        ("connectivities_tree", None, "stored sparse"),
        ("connectivities", np.ones((3, 3)), "stored sparse"),
        ("connectivities", sparse.csr_matrix((3, 4)), "square"),
        ("connectivities", sparse.csr_matrix((0, 0)), "square"),
        ("connectivities_tree", sparse.csr_matrix((4, 4)), "match"),
        ("connectivities_tree", sparse.csr_matrix([[np.nan] * 3] * 3), "finite"),
        ("connectivities", sparse.csr_matrix([[np.inf] * 3] * 3), "finite"),
        ("connectivities", sparse.csr_matrix([[1j] * 3] * 3), "real numbers"),
    ],
)
def test_invalid_tables_fail_with_context(key, value, match):
    a = make_adjacency()
    a.uns[key] = value
    with pytest.raises(
        (ValueError, TypeError), match=f"gsc.pl.paga_adjacency.*{match}"
    ):
        gsc.pl.paga_adjacency(a, show=False)


def test_large_adjacency_rejects_before_densification(monkeypatch):
    a = make_adjacency()
    a.uns["connectivities"] = sparse.csr_matrix((501, 501))
    monkeypatch.setattr(
        sparse.csr_matrix, "toarray", lambda *a, **k: pytest.fail("Densified")
    )
    with pytest.raises(ValueError, match="250,000"):
        gsc.pl.paga_adjacency(a, show=False)


def test_sparse_arrays_and_explicit_zeros_keep_the_same_point_orientation():
    a = make_adjacency()
    a.uns["connectivities"] = sparse.csc_array(a.uns["connectivities"])
    tree = sparse.csr_array(([0.0, 0.8, -0.2], ([0, 1, 2], [0, 2, 1])), shape=(3, 3))
    a.uns["connectivities_tree"] = tree
    _, points = adjacency_values(a, "connectivities", "connectivities_tree")
    assert points.to_dict("records") == [{"_x": 1, "_y": 2}, {"_x": 2, "_y": 1}]
    assert tree.nnz == 3


@pytest.mark.parametrize("storage", ["csr", "csc", "lil", "coo", "dok", "bsr"])
@pytest.mark.parametrize(
    "case",
    [
        "default",
        "empty_tree",
        "constant",
        "missing",
        "singleton",
        "singleton_empty",
        "all_missing",
        "row_missing",
        "diagonal",
        "negative",
    ],
)
def test_stripplot_order_colors_and_limits_match_public_scanpy(storage, case):
    import matplotlib.pyplot as plt
    from matplotlib.colors import to_rgba
    import scanpy as sc

    plt.close("all")
    sc.pl.paga_adjacency(make_adjacency("csr", case), as_heatmap=False, show=False)
    ax = plt.gcf().axes[0]
    positions = np.ma.concatenate([c.get_offsets() for c in ax.collections])
    colors = np.concatenate(
        [
            np.repeat(c.get_facecolors(), len(c.get_offsets()), axis=0)
            for c in ax.collections
        ]
    )
    visible = ~np.ma.getmaskarray(positions).any(axis=1)
    spec = gsc.pl.paga_adjacency(
        make_adjacency(storage, case), as_heatmap=False, show=False
    ).to_dict()
    rows = spec["datasets"][spec["data"]["name"]]
    drawn = [r for r in rows if r["_y"] is not None]
    np.testing.assert_equal(
        np.array([[r["_x"], r["_y"]] for r in drawn]).reshape(-1, 2),
        np.asarray(positions)[visible],
    )
    actual_colors = np.array(
        [to_rgba("black" if r["_kind"] == "Tree" else "gray") for r in drawn]
    ).reshape(-1, 4)
    np.testing.assert_allclose(actual_colors, colors[visible])
    for axis, expected in (("x", ax.get_xlim()), ("y", ax.get_ylim())):
        np.testing.assert_allclose(spec["encoding"][axis]["scale"]["domain"], expected)
        assert "name" not in spec["encoding"][axis]["scale"]
    assert spec["width"] == 496 and spec["height"] == 369.6
    assert spec["encoding"]["fill"]["legend"]["orient"] == "bottom"
    assert spec["encoding"]["fill"]["scale"]["range"] == ["#cbd5e1", "#2563a6"]
    plt.close("all")


def test_stripplot_preserves_source_target_ids_and_black_diagonal_entries():
    values, tree = adjacency_values(
        make_adjacency(case="diagonal"), "connectivities", "connectivities_tree"
    )
    points = adjacency_points(values, tree)
    assert points[["_x", "_target", "_kind"]].to_dict("records") == [
        {"_x": source, "_target": target, "_kind": kind}
        for source in range(3)
        for target, kind in [(j, "Adjacency") for j in range(3) if j != source]
        + [(source, "Tree")]
    ]
    np.testing.assert_equal(
        points["_y"].to_numpy(), [0.2, 0.6, 0.9, 0.4, 0.8, 0.8, 0.7, 0.1, 0.7]
    )


def test_stripplot_keeps_inactive_colormap_and_disables_hover():
    spec = gsc.pl.paga_adjacency(
        make_adjacency(),
        as_heatmap=False,
        color_map=object(),
        hover=False,
        zoom=True,
        show=False,
    ).to_dict()
    assert spec["mark"]["tooltip"] is None
    assert "tooltip" not in spec["encoding"]
    assert spec["encoding"]["x"]["scale"]["zoom"] is False
    assert spec["encoding"]["y"]["scale"]["zoom"] is True


@pytest.mark.parametrize("zoom", [True, "xy"])
def test_named_strips_use_index_slots_and_collect_legend_outside_labels(zoom):
    labels = ["Repeated", "Middle", "Repeated"]
    spec = gsc.pl.paga_adjacency(
        make_adjacency(), as_heatmap=False, labels=labels, zoom=zoom, show=False
    ).to_dict()
    points, text = leaf_marks(spec)
    x = points["encoding"]["x"]
    assert x["type"] == "index"
    assert x["scale"]["domain"] == [0, 2]
    assert x["scale"]["zoom"] is (zoom == "xy")
    assert x["axis"]["title"] is None
    rows = spec["datasets"][text["data"]["name"]]
    assert rows == [{"slot": i, "label": value} for i, value in enumerate(labels)]
    assert spec["resolve"]["legend"]["default"] == "collected"
    title = spec["surround"]["bottom"][0]["title"]
    assert title["text"] == "Source group" and title["orient"] == "bottom"
