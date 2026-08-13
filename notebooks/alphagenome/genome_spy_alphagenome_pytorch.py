"""Interactive TAL1 sequence designer backed by local AlphaGenome-PyTorch.

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
    import importlib.util
    import os

    import genome_spy as gs
    import marimo as mo
    import polars as pl

    from _alphagenome_adapter import (
        adapt_prediction_pairs,
        add_sequence_chunks,
        empty_prediction_frame,
    )
    from _alphagenome_interaction import (
        BASES,
        allele_click_submission,
        prediction_display_state,
        prediction_input_key,
        should_run_submission,
        should_run_reference_prediction,
    )
    from _alphagenome_pytorch import (
        DEFAULT_RESOLUTION,
        MODEL_INPUT_WIDTH,
        PACKAGE_VERSION,
        PRECISION_AUTO,
        TAL1_DISPLAY_TRACKS,
        TAL1_TRACK_SELECTORS,
        ModelInterval,
        ModelVariant,
        apply_variants,
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
        BASES,
        DEFAULT_RESOLUTION,
        Interval,
        MODEL_INPUT_WIDTH,
        ModelInterval,
        ModelVariant,
        PACKAGE_VERSION,
        PRECISION_AUTO,
        PredictionRequest,
        TAL1_DISPLAY_TRACKS,
        TAL1_TRACK_SELECTORS,
        Variant,
        adapt_prediction_pairs,
        add_sequence_chunks,
        allele_click_submission,
        apply_variants,
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
        sequence_composition_rows,
        should_run_submission,
        should_run_reference_prediction,
        update_prediction_cache,
    )


@app.cell
def _(PACKAGE_VERSION, PRECISION_AUTO, mo, os):
    checkpoint_path = os.environ.get("ALPHAGENOME_PYTORCH_CHECKPOINT", "")
    device = os.environ.get("ALPHAGENOME_DEVICE", "cuda")
    precision = os.environ.get("ALPHAGENOME_PRECISION", PRECISION_AUTO)
    setup = mo.md(
        "## Design a TAL1 sequence and predict its regulatory effects\n\n"
        "Zoom to base resolution and click A, C, G, or T in the sequence "
        "designer. Every selected tile becomes part of one alternate sequence, "
        "and AlphaGenome refreshes the linked tracks after each edit. The model "
        f"setup is pinned to `alphagenome-pytorch` {PACKAGE_VERSION}."
    )
    return checkpoint_path, device, precision, setup


@app.cell
def _(
    BASES,
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
    display_interval = ModelInterval("chr1", 47_212_000, 47_244_768)
    if model_interval.width != MODEL_INPUT_WIDTH:
        raise RuntimeError("Packaged TAL1 reference has an invalid model width.")
    reference_sequence = reference_asset["sequence"]
    display_offset = display_interval.start - model_interval.start
    display_sequence = reference_sequence[
        display_offset : display_offset + display_interval.width
    ]
    reference_rows = pl.DataFrame(
        {
            "chrom": [display_interval.chromosome] * display_interval.width,
            "pos0": list(range(display_interval.start, display_interval.end)),
            "end0": list(range(display_interval.start + 1, display_interval.end + 1)),
            "pos1": list(range(display_interval.start + 1, display_interval.end + 1)),
            "reference": list(display_sequence),
        }
    )
    designer_rows = reference_rows.with_columns(
        pl.lit(list(BASES)).alias("alleles"),
        pl.lit("allele_choice").alias("interaction_kind"),
    )
    sequence_summary_rows = pl.DataFrame(
        sequence_composition_rows(display_sequence, display_interval.start)
    ).with_columns(pl.lit(display_interval.chromosome).alias("chrom"))
    gene_rows = pl.DataFrame(
        gene_annotation_rows(display_interval.start, display_interval.end)
    ).with_columns(pl.lit(display_interval.chromosome).alias("chrom"))
    selected_site_rows = pl.DataFrame(
        {
            "chrom": pl.Series([], dtype=pl.String),
            "pos0": pl.Series([], dtype=pl.Int64),
        }
    )
    if (
        reference_sequence[tal1_pos0 - model_interval.start]
        != reference_asset["positive_control_site"]["ref"]
    ):
        raise RuntimeError("Packaged TAL1 positive-control REF does not match.")
    return (
        designer_rows,
        display_interval,
        gene_rows,
        model_interval,
        reference_asset,
        reference_sequence,
        selected_site_rows,
        sequence_summary_rows,
        tal1_pos0,
    )


@app.cell
def _(mo):
    get_design, set_design = mo.state({"variants": (), "click_revision": 0})
    get_prediction_cache, set_prediction_cache = mo.state({})
    get_prediction, set_prediction = mo.state(
        {
            "status": "idle",
            "message": "Loading the reference sequence prediction.",
            "frame": None,
            "input_key": None,
            "click_revision": 0,
        }
    )
    return (
        get_design,
        get_prediction,
        get_prediction_cache,
        set_design,
        set_prediction,
        set_prediction_cache,
    )


@app.cell
def _(
    BASES,
    TAL1_DISPLAY_TRACKS,
    designer_rows,
    display_interval,
    empty_prediction_frame,
    gene_rows,
    gs,
    mo,
    selected_site_rows,
    sequence_summary_rows,
    tal1_pos0,
):
    base_colors = ["#4FBF45", "#4D96E8", "#E8B322", "#E85F78"]
    base_grid = (
        gs.layer(
            gs.Chart().mark_rect(
                fill="#f8fafc",
                stroke="#cbd5e1",
                strokeWidth=0.7,
                cullByVisibleRange=False,
            ),
            gs.Chart()
            .mark_text(
                size=12,
                fitToBand=True,
                paddingX=2,
                paddingY=2,
                flushX=False,
                tooltip=None,
                cullByVisibleRange=False,
            )
            .encode(color=gs.value("#111827"), text=gs.Text("allele:N")),
        )
        .encode(
            x=gs.Locus("chrom", "pos0", band=0).axis(title="Genomic position (hg38)"),
            x2=gs.Locus("chrom", "end0", band=0),
            y=gs.Y("allele:N").scale(domain=list(BASES)).axis(title=None),
            tooltip=["chrom:N", "pos1:Q", "reference:N", "allele:N"],
        )
        .properties(
            data={"name": "designer"},
        )
        .transform_flatten(fields=["alleles"], as_=["allele"])
    )
    reference_base = gs.Chart(data={"name": "designer"}).encode(
        x=gs.Locus("chrom", "pos0", band=0).axis(title="Genomic position (hg38)"),
        x2=gs.Locus("chrom", "end0", band=0),
        y=gs.Y("reference:N").scale(domain=list(BASES)).axis(title=None),
        tooltip=["chrom:N", "pos1:Q", "reference:N"],
    )
    reference_tiles = gs.layer(
        reference_base.mark_rect(
            stroke="#111827", strokeWidth=1.5, cullByVisibleRange=False
        ).encode(
            color=gs.Color("reference:N")
            .scale(
                domain=list(BASES),
                range=base_colors,
            )
            .legend(None)
        ),
        reference_base.mark_text(
            size=12,
            fitToBand=True,
            paddingX=2,
            paddingY=2,
            flushX=False,
            tooltip=None,
            cullByVisibleRange=False,
        ).encode(
            color=gs.value("#111827"),
            text=gs.Text("reference:N"),
        ),
    )
    edit_base = gs.Chart(data={"name": "edits"}).encode(
        x=gs.Locus("chrom", "pos0", band=0).axis(title="Genomic position (hg38)"),
        x2=gs.Locus("chrom", "end0", band=0),
        tooltip=["chrom:N", "pos1:Q", "reference:N", "alternate:N"],
    )
    edited_tiles = gs.layer(
        edit_base.mark_rect(
            fill="#f8fafc",
            stroke="#cbd5e1",
            strokeWidth=0.7,
            cullByVisibleRange=False,
        ).encode(y=gs.Y("reference:N").scale(domain=list(BASES)).axis(title=None)),
        edit_base.mark_text(
            size=12,
            fitToBand=True,
            paddingX=2,
            paddingY=2,
            flushX=False,
            tooltip=None,
            cullByVisibleRange=False,
        ).encode(
            y=gs.Y("reference:N").scale(domain=list(BASES)).axis(title=None),
            color=gs.value("#111827"),
            text=gs.Text("reference:N"),
        ),
        edit_base.mark_rect(
            stroke="#111827", strokeWidth=1.5, cullByVisibleRange=False
        ).encode(
            y=gs.Y("alternate:N").scale(domain=list(BASES)).axis(title=None),
            color=gs.Color("alternate:N")
            .scale(
                domain=list(BASES),
                range=base_colors,
            )
            .legend(None),
        ),
        edit_base.mark_text(
            size=12,
            fitToBand=True,
            paddingX=2,
            paddingY=2,
            flushX=False,
            tooltip=None,
            cullByVisibleRange=False,
        ).encode(
            y=gs.Y("alternate:N").scale(domain=list(BASES)).axis(title=None),
            color=gs.value("#111827"),
            text=gs.Text("alternate:N"),
        ),
    )
    sequence_overview = (
        gs.Chart(data={"name": "sequence_summary"})
        .mark_rect(minWidth=0.5)
        .encode(
            x=gs.Locus("chrom", "start0", band=0).axis(None),
            x2=gs.Locus("chrom", "end0", band=0),
            color=gs.Color("gc_fraction:Q")
            .scale(domain=[0.25, 0.75], range=["#f3f4f6", "#334155"])
            .legend(None),
            tooltip=["start0:Q", "end0:Q", "bin_size:Q", "gc_fraction:Q"],
        )
        .properties(opacity=gs.dynamic_opacity(unitsPerPixel=[20, 5], values=[1, 0]))
    )
    designer_overview = (
        gs.Chart(data={"name": "sequence_summary"})
        .mark_rect(minWidth=0.5)
        .encode(
            x=gs.Locus("chrom", "start0", band=0).axis(title="Genomic position (hg38)"),
            x2=gs.Locus("chrom", "end0", band=0),
            color=gs.Color("gc_fraction:Q")
            .scale(domain=[0.25, 0.75], range=["#f8fafc", "#94a3b8"])
            .legend(None),
            tooltip=["start0:Q", "end0:Q", "bin_size:Q", "gc_fraction:Q"],
        )
        .properties(opacity=gs.dynamic_opacity(unitsPerPixel=[20, 5], values=[1, 0]))
    )
    reference_sequence_bases = (
        gs.layer(
            gs.Chart().mark_rect(cullByVisibleRange=False),
            gs.Chart()
            .mark_text(
                size=12,
                fitToBand=True,
                paddingX=2,
                paddingY=2,
                flushX=False,
                tooltip=None,
                cullByVisibleRange=False,
            )
            .encode(color=gs.value("#111827"), text=gs.Text("reference:N")),
        )
        .encode(
            x=gs.Locus("chrom", "pos0", band=0).axis(None),
            x2=gs.Locus("chrom", "end0", band=0),
            color=gs.Color("reference:N")
            .scale(
                domain=list(BASES),
                range=base_colors,
            )
            .legend(None),
            tooltip=["chrom:N", "pos1:Q", "reference:N"],
        )
        .properties(
            data={"name": "designer"},
            opacity=gs.dynamic_opacity(unitsPerPixel=[20, 5], values=[0, 1]),
        )
    )
    reference_sequence_track = (
        gs.layer(sequence_overview, reference_sequence_bases)
        .properties(height=34, title="hg38 reference sequence")
        .resolve_scale(color="independent")
    )
    interactive_designer = gs.layer(
        base_grid, reference_tiles, edited_tiles
    ).properties(opacity=gs.dynamic_opacity(unitsPerPixel=[20, 5], values=[0, 1]))
    sequence_designer = (
        gs.layer(designer_overview, interactive_designer)
        .properties(
            height=104,
            title=(
                "Allele designer: positions are columns; click an A/C/G/T tile "
                "to build the alternate sequence"
            ),
        )
        .resolve_scale(color="independent")
    )

    selected_site = (
        gs.Chart(data={"name": "selected_site"})
        .mark_rule(
            color="#111827", opacity=0.65, size=1, strokeDash=[4, 3], tooltip=None
        )
        .encode(x=gs.Locus("chrom", "pos0", band=0))
    )

    gene_base = gs.Chart(data={"name": "genes"}).encode(
        y=gs.Y("lane:O").scale(padding=0.5, reverse=True).axis(None),
        tooltip=["gene:N", "biotype:N", "transcript:N", "strand:N", "source:N"],
    )
    gene_models = gs.layer(
        gene_base.transform_filter("datum.feature === 'transcript'")
        .mark_rule(color="#b0b0b0", size=2, tooltip=None)
        .encode(
            x=gs.Locus("chrom", "start0", band=0).axis(title=None),
            x2=gs.Locus("chrom", "end0", band=0),
        ),
        gene_base.transform_filter("datum.feature === 'exon'")
        .mark_rect(
            stroke="#505050",
            strokeWidth=1,
            minWidth=1,
            fillOpacity=0.8,
            tooltip=None,
        )
        .encode(
            x=gs.Locus("chrom", "start0", band=0).axis(title=None),
            x2=gs.Locus("chrom", "end0", band=0),
            fill=gs.Fill("biotype:N")
            .scale(
                domain=["protein_coding", "lncRNA"],
                range=["#ffbf79", "#83bcb6"],
            )
            .legend(None),
        ),
        gene_base.transform_filter("datum.feature === 'transcript'")
        .mark_text(color="#505050", size=10, yOffset=12, tooltip=None)
        .transform_formula(
            expr=(
                "(datum.strand === '-' ? '< ' : '') + datum.gene + ' - ' "
                "+ datum.transcript + (datum.strand === '+' ? ' >' : '')"
            ),
            as_="label",
        )
        .encode(
            x=gs.Locus("chrom", "label_pos0", band=0).axis(title=None),
            text=gs.Text("label:N"),
        ),
        selected_site,
    ).properties(
        height=64,
        title="TAL1 locus genes (RefSeq + Ensembl, hg38)",
    )

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
        signal_bins = (
            gs.Chart(data={"name": "predictions"})
            .transform_filter(f"datum.track_name === '{track_name}'")
            .transform_regex_fold(
                columnRegex=r"^(reference|alternate)$",
                asValue="value",
                asKey="series",
            )
        )
        overview = signal_bins.mark_rect(minWidth=0.5, opacity=0.55).encode(
            x=gs.Locus("chrom", "start0", band=0).axis(title="Genomic position (hg38)"),
            x2=gs.Locus("chrom", "end0", band=0),
            y=gs.Y("value:Q").axis(format="~g", title=None),
            y2=gs.Y2(gs.datum(0)),
            color=gs.Color("series:N")
            .scale(
                domain=["reference", "alternate"],
                range=["#2563eb", "#dc2626"],
            )
            .legend(None),
            tooltip=[*prediction_tooltip, "series:N", "value:Q"],
        )
        detail_logo = (
            signal_bins.transform_formula(
                expr=(
                    "datum.series === 'reference' ? "
                    "datum.reference_bases : datum.alternate_bases"
                ),
                as_="sequence",
            )
            .transform_flatten_sequence(field="sequence", as_=["base_offset", "base"])
            .transform_formula(expr="upper(datum.base)", as_="base")
            .transform_formula(expr="datum.start0 + datum.base_offset", as_="pos0")
            .transform_formula(
                expr="datum.series === 'reference' ? datum.value : -datum.value",
                as_="logo_value",
            )
            .mark_text(
                font="Source Sans Pro",
                fontWeight=700,
                size=90,
                squeeze=True,
                fitToBand=True,
                paddingX=0,
                paddingY=0,
                logoLetters=True,
            )
            .encode(
                x=gs.Locus("chrom", "pos0").axis(title="Genomic position (hg38)"),
                y=gs.datum(0, type="quantitative")
                .scale(zero=True, nice=False)
                .axis(format="~g", title=None),
                y2=gs.Y2("logo_value:Q"),
                text=gs.Text("base:N"),
                color=gs.Color("base:N")
                .scale(
                    domain=list(BASES),
                    range=base_colors,
                )
                .legend(None),
                tooltip=[*prediction_tooltip, "series:N", "base:N", "value:Q"],
            )
        )
        detail_baseline = signal_bins.mark_rule(
            color="#475569", opacity=0.7, size=1, tooltip=None
        ).encode(y=gs.datum(0, type="quantitative"))
        detail = gs.layer(detail_baseline, detail_logo)
        signal = gs.multiscale(
            overview,
            detail,
            stops={
                "channel": "x",
                "values": [10],
                "transition": {"type": "lerp", "halfLife": 80},
            },
        ).resolve_scale(color="independent")
        return gs.layer(signal, selected_site).properties(
            height=64,
            title=(
                f"{title} - ref above baseline, alt below; "
                "base-colored DynSeq when deeply zoomed"
            ),
        )

    def delta_panel(track_name):
        delta = (
            gs.Chart(data={"name": "predictions"})
            .transform_filter(f"datum.track_name === '{track_name}'")
            .mark_rect(color="#7c3aed", minWidth=0.5, opacity=0.8)
            .encode(
                x=gs.Locus("chrom", "start0", band=0).axis(
                    title="Genomic position (hg38)"
                ),
                x2=gs.Locus("chrom", "end0", band=0),
                y=gs.Y("delta:Q").scale(zero=True).axis(format="~g", title=None),
                y2=gs.Y2(gs.datum(0)),
                tooltip=prediction_tooltip,
            )
        )
        return gs.layer(delta, selected_site).properties(
            height=42,
            title="Delta model signal (alt - ref)",
        )

    def assay_panel(track):
        return (
            gs.vconcat(
                signal_panel(track.track_name, track.panel_title),
                delta_panel(track.track_name),
                spacing=2,
            )
            .resolve_scale(y="independent")
            .resolve_axis(x="shared")
        )

    prediction_tracks = gs.vconcat(
        *(assay_panel(track) for track in TAL1_DISPLAY_TRACKS), spacing=6
    )
    detail_tracks = (
        gs.vconcat(reference_sequence_track, sequence_designer, spacing=4)
        .properties(
            scales=gs.scales(
                x=gs.Scale(
                    domain={
                        "param": "detailBrush",
                        "initial": [
                            {
                                "chrom": display_interval.chromosome,
                                "pos": tal1_pos0 - 4,
                            },
                            {
                                "chrom": display_interval.chromosome,
                                "pos": tal1_pos0 + 4,
                            },
                        ],
                    },
                    zoom={
                        "extent": [
                            {
                                "chrom": display_interval.chromosome,
                                "pos": display_interval.start,
                            },
                            {
                                "chrom": display_interval.chromosome,
                                "pos": display_interval.end,
                            },
                        ]
                    },
                )
            )
        )
        .resolve_scale(x="shared")
    )
    overview_tracks = (
        gs.vconcat(gene_models, prediction_tracks, spacing=6)
        .properties(
            params=[
                gs.param(
                    "detailBrush",
                    persist=False,
                    push="outer",
                    select={
                        "type": "interval",
                        "encodings": ["x"],
                        "extent": "container",
                        "mark": {
                            "fill": "#2563eb",
                            "fillOpacity": 0.04,
                            "stroke": "#2563eb",
                            "strokeOpacity": 0.45,
                        },
                    },
                )
            ],
            scales=gs.scales(
                x=gs.Scale(
                    domain=[
                        {
                            "chrom": display_interval.chromosome,
                            "pos": display_interval.start,
                        },
                        {
                            "chrom": display_interval.chromosome,
                            "pos": display_interval.end,
                        },
                    ],
                    zoom={
                        "extent": [
                            {
                                "chrom": display_interval.chromosome,
                                "pos": display_interval.start,
                            },
                            {
                                "chrom": display_interval.chromosome,
                                "pos": display_interval.end,
                            },
                        ]
                    },
                )
            ),
        )
        .resolve_scale(x="shared")
    )

    chart = (
        gs.vconcat(
            detail_tracks,
            overview_tracks,
            spacing=10,
        )
        .properties(
            datasets={
                "designer": [],
                "edits": [],
                "sequence_summary": [],
                "genes": [],
                "selected_site": [],
                "predictions": [],
            },
            params=[gs.param("detailBrush")],
            assembly="hg38",
            width=760,
            title="TAL1 local sequence-to-function perturbation explorer",
        )
        .resolve_scale(x="independent")
    )
    view = chart.widget(enable_click_events=True)
    view.set_dataset("designer", designer_rows)
    view.set_dataset("sequence_summary", sequence_summary_rows)
    view.set_dataset("genes", gene_rows)
    view.set_dataset("selected_site", selected_site_rows)
    view.set_dataset("predictions", empty_prediction_frame())
    chart_widget = mo.ui.anywidget(view)
    return chart_widget, view


@app.cell
def _(allele_click_submission, chart_widget, get_design, set_design):
    clicked = dict(chart_widget.value.get("clicked_datum", {}))
    click_revision = int(chart_widget.value.get("click_revision", 0))
    submission = allele_click_submission(
        clicked, click_revision, get_design()["variants"]
    )
    if submission is not None and click_revision > get_design()["click_revision"]:
        set_design(submission)
    return (submission,)


@app.cell
def _(get_design, view):
    variants = get_design()["variants"]
    view.set_dataset(
        "edits",
        [{**variant, "end0": variant["pos0"] + 1} for variant in variants],
        format="records",
    )
    view.set_dataset(
        "selected_site",
        [{"chrom": variant["chrom"], "pos0": variant["pos0"]} for variant in variants],
        format="records",
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
    add_sequence_chunks,
    apply_variants,
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
    should_run_reference_prediction,
    submission,
    update_prediction_cache,
):
    _previous = get_prediction()
    _is_reference_run = (
        should_run_reference_prediction(submission, _previous)
        and importlib.util.find_spec("alphagenome_pytorch") is not None
    )
    if _is_reference_run or should_run_submission(submission, _previous):
        _variants = () if _is_reference_run else submission["variants"]
        _input_key = prediction_input_key(
            _variants,
            checkpoint_path,
            device,
            precision,
        )
        try:
            _resolved_precision = resolve_precision(device, precision)
            _pinned_checkpoint = not checkpoint_path.strip()
            _checkpoint = (
                checkpoint_path.strip()
                if not _pinned_checkpoint
                else download_checkpoint()
            )
            _package_version = importlib.metadata.version("alphagenome-pytorch")
            _request_variants = tuple(
                Variant(
                    variant["chrom"],
                    variant["pos1"],
                    variant["reference"],
                    variant["alternate"],
                )
                for variant in _variants
            )
            _model_variants = tuple(
                ModelVariant(
                    variant["chrom"],
                    variant["pos1"],
                    variant["reference"],
                    variant["alternate"],
                )
                for variant in _variants
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
                variants=_request_variants,
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
                    device=device,
                    precision=_resolved_precision,
                )
                _pairs = predict_variant_tracks(
                    _model,
                    reference_sequence=reference_sequence,
                    model_interval=model_interval,
                    display_interval=display_interval,
                    variants=_model_variants,
                    resolution=DEFAULT_RESOLUTION,
                )
                _frame = adapt_prediction_pairs(
                    _pairs,
                    request_id=_request.request_id,
                    display_interval=_pairs[0].reference.interval,
                )
            _frame = add_sequence_chunks(
                _frame,
                reference_sequence=reference_sequence,
                alternate_sequence=apply_variants(
                    reference_sequence, model_interval, _model_variants
                ),
                sequence_start0=model_interval.start,
            )
        except Exception as exc:
            set_prediction(
                {
                    **_previous,
                    "status": "failed",
                    "message": f"Local prediction failed: {exc}",
                    "click_revision": (
                        0 if _is_reference_run else submission["click_revision"]
                    ),
                }
            )
        else:
            _result = {
                "status": "succeeded",
                "message": (
                    "Loaded the matching prediction from this session."
                    if _was_cached
                    else (
                        "Predicted the reference sequence locally."
                        if _is_reference_run
                        else f"Predicted the {len(_variants)}-edit sequence locally."
                    )
                ),
                "frame": _frame,
                "input_key": _input_key,
                "click_revision": 0
                if _is_reference_run
                else submission["click_revision"],
            }
            if not _was_cached:
                _updated_cache = update_prediction_cache(
                    get_prediction_cache(), _request.request_id, _frame
                )
                set_prediction_cache(_updated_cache)
            set_prediction(_result)
    elif submission is not None and not submission["variants"]:
        set_prediction(
            {
                "status": "idle",
                "message": "Reference sequence restored; choose an alternate base.",
                "frame": None,
                "input_key": None,
                "click_revision": submission["click_revision"],
            }
        )
    return


@app.cell
def _(empty_prediction_frame, get_prediction, view):
    prediction = get_prediction()
    if prediction["status"] == "succeeded":
        view.set_dataset("predictions", prediction["frame"])
    elif prediction["status"] == "idle":
        view.set_dataset("predictions", empty_prediction_frame())
    return (prediction,)


@app.cell
def _(
    chart_widget,
    checkpoint_path,
    device,
    get_design,
    mo,
    precision,
    prediction,
    prediction_display_state,
    prediction_input_key,
    setup,
):
    _variants = get_design()["variants"]
    pending_input_key = prediction_input_key(
        _variants,
        checkpoint_path,
        device,
        precision,
    )
    status, message = prediction_display_state(prediction, pending_input_key)
    _edit_summary = (
        ", ".join(
            f"{variant['pos1']} {variant['reference']}->{variant['alternate']}"
            for variant in _variants
        )
        or "reference sequence"
    )
    mo.vstack(
        [
            setup,
            mo.md(
                f"**Designed sequence:** {_edit_summary}. Selected tiles define one "
                "alternate haplotype; choose the reference tile to undo an edit. "
                "Dashed guides align edited sites with the 128 bp signal and delta "
                "tracks, including distal predicted effects."
            ),
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


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
