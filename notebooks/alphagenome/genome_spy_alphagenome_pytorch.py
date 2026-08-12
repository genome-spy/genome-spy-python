"""Interactive TAL1 SNV explorer backed by local AlphaGenome-PyTorch.

Launch with an ephemeral notebook-only model dependency (the project remains
free of Torch and AlphaGenome dependencies):

    uv run --python 3.12 \
      --with 'alphagenome-pytorch==0.3.1' \
      --with 'huggingface-hub==1.27.0' \
      marimo edit notebooks/alphagenome/genome_spy_alphagenome_pytorch.py
"""

import marimo

__generated_with = "0.23.16"
app = marimo.App()


@app.cell
def _():
    import importlib.metadata
    import os

    import genome_spy as gs
    import marimo as mo
    import polars as pl

    from _alphagenome_adapter import adapt_prediction_pairs, empty_prediction_frame
    from _alphagenome_pytorch import (
        DEFAULT_RESOLUTION,
        MODEL_INPUT_WIDTH,
        PACKAGE_VERSION,
        PRECISION_AUTO,
        PRECISION_FLOAT32,
        PRECISION_MIXED,
        TAL1_DISPLAY_TRACKS,
        TAL1_TRACK_SELECTORS,
        ModelInterval,
        ModelVariant,
        checkpoint_identity,
        download_checkpoint,
        load_model,
        predict_variant_tracks,
        resolve_precision,
        update_prediction_cache,
    )
    from _alphagenome_request import Interval, PredictionRequest, Variant
    from genome_spy.datasets import load_dataset

    def prediction_input_key(
        selection, alternate, checkpoint, device_name, precision_name
    ):
        return (
            selection["chrom"],
            selection["pos1"],
            selection["base"],
            alternate,
            checkpoint.strip() or "pinned-checkpoint",
            device_name,
            precision_name,
        )

    def prediction_display_state(prediction, pending_input_key):
        stale = (
            prediction["status"] == "succeeded"
            and prediction["frame"] is not None
            and prediction["input_key"] != pending_input_key
        )
        if stale:
            return "stale", "Inputs changed; the previous model result remains visible."
        return prediction["status"], prediction["message"]

    def should_apply_prediction(prediction, applied_request_id):
        return (
            prediction["frame"] is not None
            and prediction["request_id"] != applied_request_id
        )

    return (
        DEFAULT_RESOLUTION,
        MODEL_INPUT_WIDTH,
        PACKAGE_VERSION,
        PRECISION_AUTO,
        PRECISION_FLOAT32,
        PRECISION_MIXED,
        TAL1_DISPLAY_TRACKS,
        TAL1_TRACK_SELECTORS,
        Interval,
        ModelInterval,
        ModelVariant,
        PredictionRequest,
        Variant,
        adapt_prediction_pairs,
        checkpoint_identity,
        download_checkpoint,
        empty_prediction_frame,
        gs,
        importlib,
        load_model,
        load_dataset,
        mo,
        os,
        pl,
        predict_variant_tracks,
        prediction_display_state,
        prediction_input_key,
        resolve_precision,
        should_apply_prediction,
        update_prediction_cache,
    )


@app.cell
def _(PACKAGE_VERSION, PRECISION_AUTO, PRECISION_FLOAT32, PRECISION_MIXED, mo, os):
    checkpoint_path = mo.ui.text(
        value=os.environ.get("ALPHAGENOME_PYTORCH_CHECKPOINT", ""),
        label="Checkpoint (blank downloads the pinned Hugging Face file)",
        full_width=True,
    )
    device = mo.ui.dropdown(
        options=["cuda", "cpu"],
        value=os.environ.get("ALPHAGENOME_DEVICE", "cuda"),
        label="Torch device",
    )
    precision = mo.ui.dropdown(
        options=[PRECISION_AUTO, PRECISION_MIXED, PRECISION_FLOAT32],
        value=os.environ.get("ALPHAGENOME_PRECISION", PRECISION_AUTO),
        label="Compute precision",
    )
    setup = mo.md(
        "## Local AlphaGenome-PyTorch TAL1 explorer\n\n"
        "The checksummed hg38 TAL1 context is packaged with the example. "
        "The 450M-parameter checkpoint is loaded only after **Predict "
        "variant**; ordinary editing performs no model work. This first backend "
        "accepts SNVs only: the published TAL1 Jurkat insertion is scientific "
        "context, not an executable preset here. Current "
        "`alphagenome-pytorch` releases require "
        f"Python 3.12+. This notebook pins version `{PACKAGE_VERSION}` "
        "without adding it to the project dependencies."
    )
    return checkpoint_path, device, precision, setup


@app.cell
def _(
    MODEL_INPUT_WIDTH,
    ModelInterval,
    load_dataset,
    pl,
):
    reference_asset = load_dataset("tal1_alphagenome_reference", as_format="json")
    tal1_pos1 = reference_asset["positive_control_site"]["pos1"]
    tal1_pos0 = tal1_pos1 - 1
    model_start0 = reference_asset["interval"]["start0"]
    model_interval = ModelInterval(
        reference_asset["interval"]["chrom"],
        model_start0,
        reference_asset["interval"]["end0"],
    )
    display_interval = ModelInterval("chr1", tal1_pos0 - 16_384, tal1_pos0 + 16_384)
    editor_interval = ModelInterval("chr1", tal1_pos0 - 40, tal1_pos0 + 41)
    if model_interval.width != MODEL_INPUT_WIDTH:
        raise RuntimeError("Packaged TAL1 reference has an invalid model width.")
    reference_sequence = reference_asset["sequence"]
    editor_offset = editor_interval.start - model_interval.start
    editor_sequence = reference_sequence[
        editor_offset : editor_offset + editor_interval.width
    ]
    sequence_rows = pl.DataFrame(
        {
            "chrom": [editor_interval.chromosome] * editor_interval.width,
            "pos0": list(range(editor_interval.start, editor_interval.end)),
            "end0": list(range(editor_interval.start + 1, editor_interval.end + 1)),
            "pos1": list(range(editor_interval.start + 1, editor_interval.end + 1)),
            "base": list(editor_sequence),
            "lane": ["Reference sequence"] * editor_interval.width,
            "interaction_kind": ["sequence_base"] * editor_interval.width,
            "selected_opacity": [
                1.0 if pos0 == tal1_pos0 else 0.45
                for pos0 in range(editor_interval.start, editor_interval.end)
            ],
        }
    )
    default_selection = {
        "chrom": "chr1",
        "pos0": tal1_pos0,
        "pos1": tal1_pos1,
        "base": reference_sequence[tal1_pos0 - model_interval.start],
    }
    if default_selection["base"] != reference_asset["positive_control_site"]["ref"]:
        raise RuntimeError("Packaged TAL1 positive-control REF does not match.")
    return (
        default_selection,
        display_interval,
        editor_interval,
        model_interval,
        reference_asset,
        reference_sequence,
        sequence_rows,
    )


@app.cell
def _(default_selection, mo):
    get_selected_base, set_selected_base = mo.state(default_selection)
    get_prediction_cache, set_prediction_cache = mo.state({})
    get_prediction, set_prediction = mo.state(
        {
            "status": "idle",
            "message": "Select a base and explicitly run the local model.",
            "frame": None,
            "input_key": None,
            "request_id": None,
            "variant_key": None,
        }
    )
    get_applied_request_id, set_applied_request_id = mo.state(None)
    return (
        get_applied_request_id,
        get_prediction,
        get_prediction_cache,
        get_selected_base,
        set_applied_request_id,
        set_prediction,
        set_prediction_cache,
        set_selected_base,
    )


@app.cell
def _(get_selected_base, mo):
    selected_base = get_selected_base()
    alternate_options = [
        base for base in ("A", "C", "G", "T") if base != selected_base["base"]
    ]
    alternate_base = mo.ui.radio(
        options=alternate_options,
        value=alternate_options[0],
        label="Alternate base",
        inline=True,
    )
    predict = mo.ui.run_button(label="Predict variant", kind="success")
    return alternate_base, predict, selected_base


@app.cell
def _(
    TAL1_DISPLAY_TRACKS,
    default_selection,
    editor_interval,
    display_interval,
    empty_prediction_frame,
    gs,
    mo,
    sequence_rows,
):
    sequence = (
        gs.Chart(data={"name": "sequence"})
        .mark_rect(
            stroke="white",
            strokeWidth=0.5,
        )
        .encode(
            x=gs.X("pos0:Q").scale(domain=gs.expr("editorDomain"), nice=False),
            x2="end0:Q",
            y=gs.Y("lane:N").axis(None),
            opacity=gs.Opacity("selected_opacity:Q").scale(
                domain=[0.45, 1.0], range=[0.45, 1.0]
            ),
            color=gs.Color("base:N")
            .scale(
                domain=["A", "C", "G", "T"],
                range=["#4c78a8", "#f58518", "#54a24b", "#e45756"],
            )
            .legend(None),
            tooltip=["chrom:N", "pos1:Q", "base:N"],
        )
        .properties(height=55, title="hg38 sequence editor")
    )

    def signal_panel(track_name, title):
        return (
            gs.Chart(data={"name": "predictions"})
            .transform_filter(f"datum.track_name === '{track_name}'")
            .transform_regex_fold(
                columnRegex=r"^(reference|alternate)$",
                asValue="value",
                asKey="series",
            )
            .mark_rule(size=2, strokeCap="round", opacity=0.9)
            .encode(
                x=gs.X("start0:Q").title(None),
                x2="end0:Q",
                y=gs.Y("value:Q"),
                color=gs.Color("series:N")
                .scale(
                    domain=["reference", "alternate"],
                    range=["#2563eb", "#dc2626"],
                )
                .legend(None),
                tooltip=[
                    "chrom:N",
                    "start0:Q",
                    "end0:Q",
                    "output_type:N",
                    "track_name:N",
                    "biosample_name:N",
                    "ontology_curie:N",
                    "histone_mark:N",
                    "series:N",
                    "reference:Q",
                    "alternate:Q",
                    "delta:Q",
                ],
            )
            .properties(height=64, title=title)
        )

    def delta_panel(track_name):
        return (
            gs.Chart(data={"name": "predictions"})
            .transform_filter(f"datum.track_name === '{track_name}'")
            .mark_rule(color="#7c3aed", size=2, strokeCap="round")
            .encode(
                x=gs.X("start0:Q").title(None),
                x2="end0:Q",
                y=gs.Y("delta:Q").scale(zero=True).title("Δ alt − ref"),
                tooltip=[
                    "chrom:N",
                    "start0:Q",
                    "end0:Q",
                    "output_type:N",
                    "track_name:N",
                    "biosample_name:N",
                    "ontology_curie:N",
                    "histone_mark:N",
                    "reference:Q",
                    "alternate:Q",
                    "delta:Q",
                ],
            )
            .properties(height=42)
        )

    prediction_tracks = gs.vconcat(
        *(
            panel
            for track in TAL1_DISPLAY_TRACKS
            for panel in (
                signal_panel(track.track_name, track.panel_title),
                delta_panel(track.track_name),
            )
        ),
        spacing=2,
    ).properties(
        scales=gs.scales(
            x=gs.Scale(
                domain=[display_interval.start, display_interval.end],
                zoom=True,
            )
        )
    )

    chart = gs.vconcat(sequence, prediction_tracks, spacing=6).properties(
        datasets={"sequence": [], "predictions": []},
        params=[
            gs.param(
                "editorDomain", value=[editor_interval.start, editor_interval.end]
            ),
            gs.param("selectedBase", value=default_selection["pos0"]),
        ],
        width=760,
        title="TAL1 local sequence-to-function perturbation explorer",
    )
    view = chart.widget(
        parameter_names=("editorDomain", "selectedBase"),
        parameter_values={
            "editorDomain": [editor_interval.start, editor_interval.end],
            "selectedBase": default_selection["pos0"],
        },
        enable_click_events=True,
    )
    view.set_dataset("sequence", sequence_rows)
    view.set_dataset("predictions", empty_prediction_frame())
    chart_widget = mo.ui.anywidget(view)
    return chart_widget, view


@app.cell
def _(chart_widget, get_selected_base, set_selected_base):
    clicked = dict(chart_widget.value.get("clicked_datum", {}))
    if (
        clicked.get("interaction_kind") == "sequence_base"
        and clicked.get("pos1") == clicked.get("pos0", -2) + 1
        and clicked.get("base") in {"A", "C", "G", "T"}
    ):
        _selection = {
            "chrom": clicked["chrom"],
            "pos0": clicked["pos0"],
            "pos1": clicked["pos1"],
            "base": clicked["base"],
        }
        if _selection != get_selected_base():
            set_selected_base(_selection)
    return


@app.cell
def _(get_selected_base, pl, sequence_rows, view):
    parameter_values = dict(view.parameter_values)
    parameter_values["selectedBase"] = get_selected_base()["pos0"]
    view.parameter_values = parameter_values
    selected_pos0 = get_selected_base()["pos0"]
    view.set_dataset(
        "sequence",
        sequence_rows.with_columns(
            pl.when(pl.col("pos0") == selected_pos0)
            .then(1.0)
            .otherwise(0.45)
            .alias("selected_opacity")
        ),
    )
    return


@app.cell
def _(
    DEFAULT_RESOLUTION,
    Interval,
    ModelVariant,
    PredictionRequest,
    TAL1_TRACK_SELECTORS,
    Variant,
    adapt_prediction_pairs,
    alternate_base,
    checkpoint_identity,
    checkpoint_path,
    device,
    display_interval,
    download_checkpoint,
    get_prediction,
    get_prediction_cache,
    get_selected_base,
    importlib,
    load_model,
    model_interval,
    precision,
    predict,
    prediction_input_key,
    predict_variant_tracks,
    reference_asset,
    reference_sequence,
    resolve_precision,
    set_prediction,
    set_prediction_cache,
    update_prediction_cache,
):
    if predict.value:
        _selection = get_selected_base()
        _alternate = alternate_base.value
        _input_key = prediction_input_key(
            _selection,
            _alternate,
            checkpoint_path.value,
            device.value,
            precision.value,
        )
        _previous = get_prediction()
        try:
            _resolved_precision = resolve_precision(device.value, precision.value)
            _pinned_checkpoint = not checkpoint_path.value.strip()
            _checkpoint = (
                checkpoint_path.value.strip()
                if not _pinned_checkpoint
                else download_checkpoint()
            )
            _package_version = importlib.metadata.version("alphagenome-pytorch")
            _variant = Variant(
                _selection["chrom"],
                _selection["pos1"],
                _selection["base"],
                _alternate,
            )
            _request = PredictionRequest(
                package_version=_package_version,
                checkpoint_id=checkpoint_identity(
                    _checkpoint, pinned=_pinned_checkpoint
                ),
                organism="HOMO_SAPIENS",
                assembly="GRCh38",
                reference_checksum=reference_asset["sequence_sha256"],
                precision=_resolved_precision,
                resolution=DEFAULT_RESOLUTION,
                interval=Interval(
                    model_interval.chromosome, model_interval.start, model_interval.end
                ),
                display_interval=Interval(
                    display_interval.chromosome,
                    display_interval.start,
                    display_interval.end,
                ),
                variant=_variant,
                ontology_terms=("CL:0001059",),
                output_types=tuple(
                    dict.fromkeys(
                        selector.output_type for selector in TAL1_TRACK_SELECTORS
                    )
                ),
                selectors=tuple(
                    selector.signature for selector in TAL1_TRACK_SELECTORS
                ),
            )
            _cached = get_prediction_cache().get(_request.request_id)
            if _cached is None:
                _model = load_model(
                    _checkpoint,
                    device=device.value,
                    precision=_resolved_precision,
                )
                _pairs = predict_variant_tracks(
                    _model,
                    reference_sequence=reference_sequence,
                    model_interval=model_interval,
                    display_interval=display_interval,
                    variant=ModelVariant(
                        _selection["chrom"],
                        _selection["pos1"],
                        _selection["base"],
                        _alternate,
                    ),
                    resolution=DEFAULT_RESOLUTION,
                )
                _frame = adapt_prediction_pairs(
                    _pairs,
                    request_id=_request.request_id,
                    display_interval=_pairs[0].reference.interval,
                )
            else:
                _frame = _cached["frame"]
        except Exception as exc:
            set_prediction(
                {
                    **_previous,
                    "status": "failed",
                    "message": f"Local prediction failed: {exc}",
                }
            )
        else:
            _result = {
                "status": "succeeded",
                "message": (
                    "Loaded the matching prediction from this session."
                    if _cached is not None
                    else f"Predicted locally with alphagenome-pytorch "
                    f"{_package_version} on {device.value} "
                    f"({_resolved_precision})."
                ),
                "frame": _frame,
                "input_key": _input_key,
                "request_id": _request.request_id,
                "variant_key": _variant.key,
            }
            if _cached is None:
                _updated_cache = update_prediction_cache(
                    get_prediction_cache(), _request.request_id, _result
                )
                set_prediction_cache(_updated_cache)
            set_prediction(_result)
    return


@app.cell
def _(
    get_applied_request_id,
    get_prediction,
    set_applied_request_id,
    should_apply_prediction,
    view,
):
    prediction = get_prediction()
    if should_apply_prediction(prediction, get_applied_request_id()):
        view.set_dataset("predictions", prediction["frame"])
        set_applied_request_id(prediction["request_id"])
    return prediction


@app.cell
def _(
    alternate_base,
    chart_widget,
    checkpoint_path,
    device,
    get_selected_base,
    mo,
    precision,
    predict,
    prediction,
    prediction_display_state,
    prediction_input_key,
    setup,
):
    _selection = get_selected_base()
    pending_variant_key = (
        f"{_selection['chrom']}:{_selection['pos1']}:"
        f"{_selection['base']}:{alternate_base.value}"
    )
    pending_input_key = prediction_input_key(
        _selection,
        alternate_base.value,
        checkpoint_path.value,
        device.value,
        precision.value,
    )
    status, message = prediction_display_state(prediction, pending_input_key)
    mo.vstack(
        [
            setup,
            mo.md(
                f"Selected `{pending_variant_key}` on GRCh38. Inference uses a 131,072 bp "
                "context; only aligned 128 bp bins in the 32 kb display window "
                "cross the Arrow boundary."
            ),
            mo.hstack([alternate_base, device, precision, checkpoint_path, predict]),
            mo.md(f"**Status: {status}.** {message}"),
            chart_widget,
            mo.callout(
                "Predictions are molecular hypotheses, not causal or clinical evidence. "
                "Model parameters and outputs remain subject to the AlphaGenome Model Terms.",
                kind="warn",
            ),
        ]
    )
    return


if __name__ == "__main__":
    app.run()
