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
    from _alphagenome_interaction import (
        alternate_options,
        prediction_display_state,
        prediction_input_key,
        sequence_click_submission,
        should_run_submission,
    )
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
    from _tal1_context import gene_annotation_rows, sequence_composition_rows
    from genome_spy.datasets import load_dataset

    return (
        DEFAULT_RESOLUTION,
        Interval,
        MODEL_INPUT_WIDTH,
        ModelInterval,
        ModelVariant,
        PACKAGE_VERSION,
        PRECISION_AUTO,
        PRECISION_FLOAT32,
        PRECISION_MIXED,
        PredictionRequest,
        TAL1_DISPLAY_TRACKS,
        TAL1_TRACK_SELECTORS,
        Variant,
        adapt_prediction_pairs,
        alternate_options,
        checkpoint_identity,
        download_checkpoint,
        empty_prediction_frame,
        gene_annotation_rows,
        gs,
        importlib,
        load_dataset,
        load_model,
        mo,
        os,
        pl,
        predict_variant_tracks,
        prediction_display_state,
        prediction_input_key,
        resolve_precision,
        sequence_click_submission,
        sequence_composition_rows,
        should_run_submission,
        update_prediction_cache,
    )


@app.cell
def _(
    PACKAGE_VERSION,
    PRECISION_AUTO,
    PRECISION_FLOAT32,
    PRECISION_MIXED,
    mo,
    os,
):
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
        "Zoom into the sequence, choose an alternate allele, and click a base "
        "to predict its effect. The 450M-parameter checkpoint is loaded on the "
        "first base click and reused for later clicks. This first backend "
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
    gene_annotation_rows,
    load_dataset,
    pl,
    sequence_composition_rows,
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
    if model_interval.width != MODEL_INPUT_WIDTH:
        raise RuntimeError("Packaged TAL1 reference has an invalid model width.")
    reference_sequence = reference_asset["sequence"]
    display_offset = display_interval.start - model_interval.start
    display_sequence = reference_sequence[
        display_offset : display_offset + display_interval.width
    ]
    sequence_rows = pl.DataFrame(
        {
            "chrom": [display_interval.chromosome] * display_interval.width,
            "pos0": list(range(display_interval.start, display_interval.end)),
            "end0": list(range(display_interval.start + 1, display_interval.end + 1)),
            "pos1": list(range(display_interval.start + 1, display_interval.end + 1)),
            "base": list(display_sequence),
            "lane": ["Reference sequence"] * display_interval.width,
            "interaction_kind": ["sequence_base"] * display_interval.width,
        }
    )
    sequence_summary_rows = pl.DataFrame(
        sequence_composition_rows(display_sequence, display_interval.start)
    )
    gene_rows = pl.DataFrame(
        gene_annotation_rows(display_interval.start, display_interval.end)
    )
    selected_site_rows = pl.DataFrame({"pos0": [tal1_pos0]})
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
        gene_rows,
        model_interval,
        reference_asset,
        reference_sequence,
        selected_site_rows,
        sequence_rows,
        sequence_summary_rows,
    )


@app.cell
def _(alternate_options, default_selection, mo):
    initial_variant = {
        "selection": default_selection,
        "alternate": alternate_options(default_selection["base"])[0],
        "click_revision": 0,
    }
    get_variant, set_variant = mo.state(initial_variant)
    get_prediction_cache, set_prediction_cache = mo.state({})
    get_prediction, set_prediction = mo.state(
        {
            "status": "idle",
            "message": "Zoom into the sequence and click a base to predict.",
            "frame": None,
            "input_key": None,
            "click_revision": 0,
        }
    )
    return (
        get_prediction,
        get_prediction_cache,
        get_variant,
        set_prediction,
        set_prediction_cache,
        set_variant,
    )


@app.cell
def _(alternate_options, get_variant, mo):
    variant = get_variant()
    options = alternate_options(variant["selection"]["base"])
    alternate_base = mo.ui.radio(
        options=options,
        value=variant["alternate"],
        label="Alternate base",
        inline=True,
    )
    return (alternate_base,)


@app.cell
def _(
    TAL1_DISPLAY_TRACKS,
    default_selection,
    display_interval,
    empty_prediction_frame,
    gene_rows,
    gs,
    mo,
    selected_site_rows,
    sequence_rows,
    sequence_summary_rows,
):
    sequence_bases = (
        gs.layer(
            gs.Chart()
            .mark_rect(minWidth=0.5)
            .properties(
                opacity=gs.dynamic_opacity(unitsPerPixel=[40, 8], values=[0, 1])
            ),
            gs.Chart()
            .transform_filter("datum.pos0 === selectedBase")
            .mark_rect(
                fillOpacity=0,
                minWidth=1,
                stroke="#111827",
                strokeWidth=2,
            ),
            gs.Chart()
            .mark_text(
                size=13,
                fitToBand=True,
                paddingX=1.5,
                paddingY=1,
                opacity=0.8,
                flushX=False,
                tooltip=None,
            )
            .encode(color=gs.value("black"), text=gs.Text("base:N"))
            .properties(
                opacity=gs.dynamic_opacity(unitsPerPixel=[100, 10], values=[0, 1])
            ),
        )
        .encode(
            x=gs.X("pos0:Q").title(None),
            x2="end0:Q",
            y=gs.Y("lane:N").axis(None),
            color=gs.Color("base:N")
            .scale(
                domain=["A", "C", "G", "T"],
                range=["#4c78a8", "#f58518", "#54a24b", "#e45756"],
            )
            .legend(None),
            tooltip=["chrom:N", "pos1:Q", "base:N"],
        )
        .properties(
            data={"name": "sequence"},
        )
    )

    sequence_overview = (
        gs.Chart(data={"name": "sequence_summary"})
        .mark_rect(minWidth=0.5)
        .encode(
            x=gs.X("start0:Q").title(None),
            x2="end0:Q",
            color=gs.Color("gc_fraction:Q")
            .scale(domain=[0.25, 0.75], range=["#f3f4f6", "#334155"])
            .legend(None),
            tooltip=["start0:Q", "end0:Q", "bin_size:Q", "gc_fraction:Q"],
        )
        .properties(opacity=gs.dynamic_opacity(unitsPerPixel=[40, 8], values=[1, 0]))
    )
    sequence = (
        gs.layer(sequence_overview, sequence_bases)
        .properties(
            height=55,
            title="hg38 sequence: 128 bp GC overview; zoom to reveal clickable bases",
        )
        .resolve_scale(color="independent")
    )

    selected_site = (
        gs.Chart(data={"name": "selected_site"})
        .mark_rule(
            color="#111827", opacity=0.65, size=1, strokeDash=[4, 3], tooltip=None
        )
        .encode(x=gs.X("pos0:Q").title(None))
    )

    gene_base = gs.Chart(data={"name": "genes"}).encode(
        y=gs.Y("lane:O").axis(None),
        color=gs.Color("gene:N")
        .scale(domain=["TAL1", "STIL"], range=["#2563eb", "#64748b"])
        .legend(None),
        tooltip=["gene:N", "transcript:N", "strand:N", "source:N"],
    )
    gene_models = gs.layer(
        gene_base.transform_filter("datum.feature === 'transcript'")
        .mark_rule(size=2)
        .encode(x=gs.X("start0:Q").title(None), x2="end0:Q"),
        gene_base.transform_filter("datum.feature === 'exon'")
        .mark_rect(minWidth=1)
        .encode(x=gs.X("start0:Q").title(None), x2="end0:Q"),
        gene_base.transform_filter("datum.feature === 'transcript'")
        .mark_text(color="#111827", size=11, dy=-9, tooltip=None)
        .transform_formula(
            expr="(datum.strand === '-' ? '< ' : '') + datum.gene",
            as_="label",
        )
        .encode(x=gs.X("label_pos0:Q").title(None), text=gs.Text("label:N")),
        selected_site,
    ).properties(height=52, title="NCBI RefSeq genes (hg38)")

    prediction_tooltip = [
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
    ]

    def signal_panel(track_name, title):
        signal = (
            gs.Chart(data={"name": "predictions"})
            .transform_filter(f"datum.track_name === '{track_name}'")
            .transform_regex_fold(
                columnRegex=r"^(reference|alternate)$",
                asValue="value",
                asKey="series",
            )
            .mark_rect(minWidth=0.5, opacity=0.55)
            .encode(
                x=gs.X("start0:Q").title(None),
                x2="end0:Q",
                y=gs.Y("value:Q"),
                y2=gs.Y2(gs.datum(0)),
                color=gs.Color("series:N")
                .scale(
                    domain=["reference", "alternate"],
                    range=["#2563eb", "#dc2626"],
                )
                .legend(None),
                tooltip=[*prediction_tooltip, "series:N"],
            )
        )
        return gs.layer(signal, selected_site).properties(height=64, title=title)

    def delta_panel(track_name):
        delta = (
            gs.Chart(data={"name": "predictions"})
            .transform_filter(f"datum.track_name === '{track_name}'")
            .mark_rect(color="#7c3aed", minWidth=0.5, opacity=0.8)
            .encode(
                x=gs.X("start0:Q").title(None),
                x2="end0:Q",
                y=gs.Y("delta:Q").scale(zero=True).title("Δ alt − ref"),
                y2=gs.Y2(gs.datum(0)),
                tooltip=prediction_tooltip,
            )
        )
        return gs.layer(delta, selected_site).properties(height=42)

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
    ).resolve_scale(y="independent")

    chart = (
        gs.vconcat(sequence, gene_models, prediction_tracks, spacing=6)
        .properties(
            datasets={
                "sequence": [],
                "sequence_summary": [],
                "genes": [],
                "selected_site": [],
                "predictions": [],
            },
            params=[
                gs.param("selectedBase", value=default_selection["pos0"]),
            ],
            scales=gs.scales(
                x=gs.Scale(
                    domain=[display_interval.start, display_interval.end],
                    zoom=True,
                )
            ),
            width=760,
            title="TAL1 local sequence-to-function perturbation explorer",
        )
        .resolve_scale(x="shared")
    )
    view = chart.widget(
        parameter_names=("selectedBase",),
        parameter_values={
            "selectedBase": default_selection["pos0"],
        },
        enable_click_events=True,
    )
    view.set_dataset("sequence", sequence_rows)
    view.set_dataset("sequence_summary", sequence_summary_rows)
    view.set_dataset("genes", gene_rows)
    view.set_dataset("selected_site", selected_site_rows)
    view.set_dataset("predictions", empty_prediction_frame())
    chart_widget = mo.ui.anywidget(view)
    return chart_widget, view


@app.cell
def _(
    alternate_base,
    chart_widget,
    get_variant,
    sequence_click_submission,
    set_variant,
):
    clicked = dict(chart_widget.value.get("clicked_datum", {}))
    click_revision = int(chart_widget.value.get("click_revision", 0))
    submission = sequence_click_submission(
        clicked, click_revision, alternate_base.value
    )
    if submission is not None and click_revision > get_variant()["click_revision"]:
        set_variant(submission)
    return (submission,)


@app.cell
def _(get_variant, view):
    selected_pos0 = get_variant()["selection"]["pos0"]
    parameter_values = dict(view.parameter_values)
    parameter_values["selectedBase"] = selected_pos0
    view.parameter_values = parameter_values
    view.set_dataset("selected_site", [{"pos0": selected_pos0}], format="records")
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
    checkpoint_identity,
    checkpoint_path,
    device,
    display_interval,
    download_checkpoint,
    get_prediction,
    get_prediction_cache,
    importlib,
    load_model,
    model_interval,
    precision,
    predict_variant_tracks,
    prediction_input_key,
    reference_asset,
    reference_sequence,
    resolve_precision,
    set_prediction,
    set_prediction_cache,
    should_run_submission,
    submission,
    update_prediction_cache,
):
    _previous = get_prediction()
    if should_run_submission(submission, _previous):
        _selection = submission["selection"]
        _alternate = submission["alternate"]
        _input_key = prediction_input_key(
            _selection,
            _alternate,
            checkpoint_path.value,
            device.value,
            precision.value,
        )
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
            _frame = get_prediction_cache().get(_request.request_id)
            _was_cached = _frame is not None
            if not _was_cached:
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
        except Exception as exc:
            set_prediction(
                {
                    **_previous,
                    "status": "failed",
                    "message": f"Local prediction failed: {exc}",
                    "click_revision": submission["click_revision"],
                }
            )
        else:
            _result = {
                "status": "succeeded",
                "message": (
                    "Loaded the matching prediction from this session."
                    if _was_cached
                    else f"Predicted locally with alphagenome-pytorch "
                    f"{_package_version} on {device.value} "
                    f"({_resolved_precision})."
                ),
                "frame": _frame,
                "input_key": _input_key,
                "click_revision": submission["click_revision"],
            }
            if not _was_cached:
                _updated_cache = update_prediction_cache(
                    get_prediction_cache(), _request.request_id, _frame
                )
                set_prediction_cache(_updated_cache)
            set_prediction(_result)
    return


@app.cell
def _(get_prediction, view):
    prediction = get_prediction()
    if prediction["status"] == "succeeded":
        view.set_dataset("predictions", prediction["frame"])
    return (prediction,)


@app.cell
def _(
    alternate_base,
    chart_widget,
    checkpoint_path,
    device,
    get_variant,
    mo,
    precision,
    prediction,
    prediction_display_state,
    prediction_input_key,
    setup,
):
    _selection = get_variant()["selection"]
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
                "cross the Arrow boundary. Choose the alternate allele, then "
                "click any visible sequence base to run or retrieve its prediction. "
                "The dashed guide marks that exact base in every track. Signal bars "
                "show predicted activity across the locus; the delta tracks show "
                "where the edit changes that activity, including distal effects."
            ),
            mo.hstack([alternate_base, device, precision, checkpoint_path]),
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


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
