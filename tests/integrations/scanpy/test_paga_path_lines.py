"""Native PAGA path lines against Scanpy's public data, limits and return values."""

import numpy as np
import pandas as pd
import pytest

import genome_spy as gs
import genome_spy.integrations.scanpy as gsc
from tests.integrations.scanpy.paga_path_fixture import make_path


LINE_CASES = {
    "default": {},
    "smooth": {"n_avg": 2},
    "crop": {"n_avg": 2, "xlim": (1, None)},
    "negative_crop": {"xlim": (-3, -1)},
    "empty_crop": {"xlim": (3, 1)},
    "normalize": {"n_avg": 2, "normalize_to_zero_one": True},
    "repeat": {"nodes": ["beta", "alpha", "beta"]},
    "X": {"use_raw": False},
    "raw_fallback": {},
    "filtered": {},
    "single_key": {"keys": ["g1"]},
    "single_sample": {"n_avg": 4},
    "annotations": {"annotations": ("cluster", "score", "dpt_pseudotime"), "n_avg": 2},
    "missing": {},
    "obs_key": {"keys": ["g1", "score"], "n_avg": 2},
}


@pytest.mark.parametrize("storage", ["dense", "csr", "csc"])
@pytest.mark.parametrize("case", LINE_CASES)
def test_line_values_domains_labels_and_order_match_public_scanpy(storage, case):
    import matplotlib.pyplot as plt
    import scanpy as sc

    options = LINE_CASES[case].copy()
    nodes = options.pop("nodes", ["beta", "alpha"])
    keys = options.pop("keys", ["g1", "g2"])
    fixture_case = (
        case if case in {"missing", "raw_fallback", "filtered"} else "default"
    )
    a = make_path(storage, fixture_case)
    fig, ax = plt.subplots()
    try:
        sc.pl.paga_path(a, nodes, keys, as_heatmap=False, show=False, ax=ax, **options)
        expected = [line.get_xydata().copy() for line in ax.lines]
        domains = [ax.get_xlim(), ax.get_ylim()]
        xlabel = ax.get_xlabel()
        legend = (
            None
            if ax.get_legend() is None
            else [t.get_text() for t in ax.get_legend().texts]
        )
    finally:
        plt.close(fig)
    spec = gsc.pl.paga_path(
        a, nodes, keys, as_heatmap=False, show=False, **options
    ).to_dict()
    root = spec
    spec = root["spec"]
    frame = pd.DataFrame(
        root["datasets"][spec["data"]["name"]], columns=["_sample", "_value", "_key"]
    )
    for key, curve in zip(keys, expected, strict=True):
        actual = frame.loc[frame["_key"] == key]
        np.testing.assert_array_equal(actual["_sample"], curve[:, 0])
        np.testing.assert_allclose(
            actual["_value"].to_numpy(dtype=float), curve[:, 1], equal_nan=True
        )
    for axis, domain in zip(("x", "y"), domains, strict=True):
        np.testing.assert_allclose(spec["encoding"][axis]["scale"]["domain"], domain)
    assert spec["encoding"]["x"]["axis"]["title"] == xlabel
    assert spec["encoding"]["y"]["axis"]["title"] == (
        (keys[0] if len(keys) == 1 else "Value")
        + (" (0–1)" if options.get("normalize_to_zero_one") else "")
    )
    assert spec["encoding"]["color"]["scale"]["domain"] == keys
    assert (spec["encoding"]["color"]["legend"] is None) is (legend is None)
    if legend is not None:
        assert keys == legend
    assert spec["mark"]["type"] == "rule" and spec["mark"]["strokeCap"] == "round"
    assert spec["transform"][0]["ops"] == ["lead", "lead"]
    assert spec["transform"][0]["groupby"] == ["_key"]
    assert spec["transform"][1]["type"] == "filter"
    assert "bottom" in root["surround"]


def test_line_return_data_is_uncropped_and_matches_working_public_case(monkeypatch):
    import matplotlib.pyplot as plt
    import scanpy as sc

    a = make_path()
    options = dict(
        as_heatmap=False, n_avg=2, xlim=(1, None), return_data=True, show=False
    )
    try:
        _, expected = sc.pl.paga_path(a, ["beta", "alpha"], ["g1", "g2"], **options)
    finally:
        plt.close("all")
    for owner, name in [(sc.pl, "paga_path"), (sc.tl, "paga"), (sc.tl, "dpt")]:
        monkeypatch.setattr(
            owner, name, lambda *a, **k: pytest.fail("Ran upstream plotting/analysis")
        )
    before = a.obs.copy(deep=True), repr(a.uns), a.X.copy()
    chart, frame = gsc.pl.paga_path(a, ["beta", "alpha"], ["g1", "g2"], **options)
    pd.testing.assert_frame_equal(frame, expected)
    assert len(frame) == 3
    spec = chart.to_dict()
    assert len(spec["datasets"][spec["spec"]["data"]["name"]]) == 4
    pd.testing.assert_frame_equal(a.obs, before[0])
    assert repr(a.uns) == before[1]
    np.testing.assert_array_equal(a.X, before[2])
    shown = []
    monkeypatch.setattr(gs.TopLevelSpec, "display", lambda self: shown.append(self))
    options["show"] = True
    pd.testing.assert_frame_equal(
        gsc.pl.paga_path(a, ["beta", "alpha"], ["g1", "g2"], **options), expected
    )
    assert len(shown) == 1


@pytest.mark.parametrize("bounds", [(0.5, 2), (True, None), (0,), "bad"])
def test_invalid_line_crop_fails_clearly(bounds):
    with pytest.raises(TypeError, match="xlim"):
        gsc.pl.paga_path(
            make_path(),
            ["beta", "alpha"],
            ["g1", "g2"],
            as_heatmap=False,
            xlim=bounds,
            show=False,
        )


def test_line_options_use_native_guides_and_ignore_inactive_heatmap_options():
    spec = gsc.pl.paga_path(
        make_path(),
        ["beta", "alpha"],
        ["g1", "g2"],
        as_heatmap=False,
        color_map=object(),
        color_maps_annotations=object(),
        palette_groups=["red", "gray", "blue", "green"],
        show_node_names=False,
        show_yticks=False,
        show_colorbar=False,
        legend_fontsize="large",
        legend_fontweight="bold",
        title="Profiles",
        hover=False,
        zoom="xy",
        show=False,
    ).to_dict()
    root = spec
    spec = root["spec"]
    assert spec["encoding"]["color"]["legend"]["orient"] == "bottom"
    assert root["title"]["text"] == "Profiles"
    assert spec["mark"]["tooltip"] is None
    assert "tooltip" not in spec["encoding"]
    assert all(spec["encoding"][axis]["scale"]["zoom"] is True for axis in ("x", "y"))
    assert all("name" not in spec["encoding"][axis]["scale"] for axis in ("x", "y"))
    with pytest.raises(NotImplementedError, match="distinct keys"):
        gsc.pl.paga_path(
            make_path(), ["beta", "alpha"], ["g1", "g1"], as_heatmap=False, show=False
        )
    with pytest.raises(ValueError, match="annotations must name distinct"):
        gsc.pl.paga_path(
            make_path(),
            ["beta", "alpha"],
            ["g1", "g2"],
            as_heatmap=False,
            annotations=("cluster", "cluster"),
            show=False,
        )
