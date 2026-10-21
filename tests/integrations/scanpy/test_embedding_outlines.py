"""Outline sizes, order and opacity follow pinned Scanpy without new data reads."""

from copy import deepcopy

import numpy as np
import pytest

import genome_spy.integrations.scanpy as gsc
from tests.integrations.scanpy.embedding_fixture import make_embedding_adata
from tests.integrations.scanpy.helpers import leaf_marks, points, units
from tests.integrations.scanpy.test_embedding import FAMILIES

sc = pytest.importorskip("scanpy")
mpl = pytest.importorskip("matplotlib")
mpl.use("Agg")


@pytest.mark.parametrize(
    "options",
    [
        {},
        {"alpha": None},
        {"alpha": 0},
        {
            "alpha": 0.4,
            "outline_width": (0.2, 0.1),
            "outline_color": ("navy", "ivory"),
            "linewidths": 0,
        },
        {"edgecolor": "red", "linewidth": 2},
        {"edgecolor": "none"},
    ],
)
@pytest.mark.parametrize("marker", [".", "o"])
def test_outline_geometry_and_opacity_match_scanpy(monkeypatch, options, marker):
    import matplotlib.pyplot as plt

    a = make_embedding_adata()
    sizes = np.array([0, 36, 144, 324, 16, 4, 64, 100])
    with plt.rc_context({"figure.dpi": 100, "lines.linewidth": 1.5}):
        ax = sc.pl.umap(
            a,
            color="score",
            size=sizes,
            marker=marker,
            add_outline=True,
            show=False,
            **options,
        )
        reference = [
            (
                artist.get_sizes().copy(),
                artist.get_alpha(),
                artist.get_linewidths().copy(),
                artist.get_edgecolors().copy(),
            )
            for artist in ax.collections
        ]
        plt.close(ax.figure)
    monkeypatch.setattr(
        sc.pl, "umap", lambda *a, **k: pytest.fail("Called Scanpy plotting")
    )
    spec = gsc.pl.umap(
        a,
        color="score",
        size=sizes,
        marker=marker,
        add_outline=True,
        show=False,
        **options,
    ).to_dict()
    marks = leaf_marks(spec)
    # Numeric missing values add a separate foreground mark, never another outline.
    assert len(marks) == 4
    records = spec["datasets"][spec["data"]["name"]]
    ordered = sorted(records, key=lambda row: row["_order_0"])
    diameter = 100 / 72 * (0.5 if marker == "." else 1)
    for mark, (areas, alpha, widths, edges) in zip(
        [*marks[:2], marks[-1]], reference, strict=True
    ):
        scale = mark["encoding"]["size"]["scale"]
        native = (
            np.array([row["_size_0"] for row in ordered])
            * scale["range"][1]
            / scale["domain"][1]
        )
        np.testing.assert_allclose(native / diameter**2, areas)
        assert mark["mark"]["fillOpacity"] == (1 if alpha is None else alpha)
        if len(edges) and np.any(edges[:, 3]):
            np.testing.assert_allclose(
                mark["mark"]["strokeWidth"], widths[0] * 100 / 72
            )
        else:
            assert mark["mark"]["strokeOpacity"] == 0
    assert marks[0]["mark"]["tooltip"] is None
    assert marks[1]["mark"]["tooltip"] is None
    assert marks[-1]["mark"]["tooltip"] == {"handler": "default"}


@pytest.mark.parametrize("family", FAMILIES)
def test_outlines_reuse_coordinates_ids_sizes_and_single_source(family):
    a = make_embedding_adata()
    original = deepcopy(a)
    args = (a, "umap") if family == "embedding" else (a,)
    options = dict(
        color=["cell_type", "g1"],
        size=np.arange(8) * 7,
        obs_id="cell_id",
        show=False,
        zoom=True,
    )
    plain = getattr(gsc.pl, family)(*args, **options).to_dict()
    outlined = getattr(gsc.pl, family)(*args, add_outline=True, **options).to_dict()
    assert outlined["datasets"] == plain["datasets"]
    assert len(outlined["datasets"]) == 1
    for panel, normal in zip(units(outlined), units(plain), strict=True):
        assert "data" in panel and "transform" in panel
        marks = leaf_marks(panel)
        assert len(marks) in (3, 4)
        assert all("data" not in mark for mark in marks)
        assert not any(
            t["type"] == "collect" for mark in marks for t in mark.get("transform", [])
        )
        assert panel["resolve"]["scale"]["size"] == "independent"
        foreground = points(panel)
        for axis in ("x", "y", "key", "size"):
            assert foreground["encoding"][axis] == points(normal)["encoding"][axis]
    np.testing.assert_array_equal(a.X, original.X)
    for key in a.obsm:
        np.testing.assert_array_equal(a.obsm[key], original.obsm[key])
    assert a.obs.equals(original.obs)


@pytest.mark.parametrize(
    "options,error,match",
    [
        ({"add_outline": "yes"}, TypeError, "add_outline"),
        ({"outline_width": (0.1,)}, ValueError, "outline_width"),
        ({"outline_width": (-1, 0)}, ValueError, "outline_width"),
        ({"outline_width": (np.inf, 0)}, ValueError, "outline_width"),
        ({"outline_color": "red"}, ValueError, "outline_color"),
        ({"outline_color": ("r", "white")}, NotImplementedError, "outline_color"),
    ],
)
def test_invalid_outline_options_fail_clearly(options, error, match):
    with pytest.raises(error, match=match):
        gsc.pl.umap(
            make_embedding_adata(), show=False, **{"add_outline": True, **options}
        )


def test_disabled_outline_settings_leave_the_chart_unchanged():
    data = make_embedding_adata()
    expected = gsc.pl.umap(data, show=False).to_dict()
    assert gsc.pl.umap(data, add_outline=None, show=False).to_dict() == expected
    assert (
        gsc.pl.umap(
            data, outline_width=(0.5, 0.2), outline_color=("navy", "ivory"), show=False
        ).to_dict()
        == expected
    )
    with pytest.raises(ValueError, match="outline_width"):
        gsc.pl.umap(data, add_outline=True, outline_width=(1e200, 0), show=False)
