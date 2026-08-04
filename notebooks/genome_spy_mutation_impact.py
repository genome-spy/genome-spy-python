"""Deterministic mutation-impact prototype using Polars and Arrow IPC."""

import marimo

__generated_with = "0.23.16"

app = marimo.App()


@app.cell
def _():
    import genome_spy as gs
    import marimo as mo
    import polars as pl

    return gs, mo, pl


@app.cell
def _(pl):
    reference_sequence = "ACGTTCGAGTACCGTATGCA"
    positions = list(range(100, 100 + len(reference_sequence)))
    reference = pl.DataFrame(
        {
            "position": positions,
            "base": list(reference_sequence),
            "value": [
                round(0.25 + 0.05 * ((index * 3) % 11), 2)
                for index in range(len(reference_sequence))
            ],
        }
    )

    return reference, reference_sequence


@app.cell
def _(mo):
    mutation_input = mo.ui.text(
        value="108:G",
        label="Mutation (genomic position:base)",
    )

    return (mutation_input,)


@app.cell
def _(gs, mutation_input, pl, reference):
    valid_bases = {"A", "C", "G", "T"}
    mutation_text = mutation_input.value.strip().upper()
    mutation_error = ""
    mutation_position = None
    mutation_base = None

    try:
        position_text, mutation_base_text = mutation_text.split(":", maxsplit=1)
        mutation_position = int(position_text)
        mutation_base = mutation_base_text.strip()
        if mutation_base not in valid_bases:
            raise ValueError("base must be one of A, C, G, or T")
        if mutation_position not in reference.get_column("position").to_list():
            raise ValueError("position is outside the reference window")
    except ValueError as error:
        mutation_error = f"Invalid mutation: {error}"

    if mutation_error:
        alternate = reference
        delta = reference.with_columns(pl.lit(0.0).alias("value"))
    else:
        distance = (pl.col("position") - mutation_position).abs()
        effect = (6 - distance).clip(lower_bound=0, upper_bound=6) / 6 * 0.8
        alternate = reference.with_columns(
            pl.when(pl.col("position") == mutation_position)
            .then(pl.lit(mutation_base))
            .otherwise(pl.col("base"))
            .alias("base"),
            (pl.col("value") + effect).alias("value"),
        )
        delta = alternate.with_columns(
            (pl.col("value") - reference.get_column("value")).alias("value")
        )

    reference_url = {"url": "arrow://reference", "format": {"type": "arrow"}}
    alternate_url = {"url": "arrow://alternate", "format": {"type": "arrow"}}
    delta_url = {"url": "arrow://delta", "format": {"type": "arrow"}}

    def base_color() -> object:
        return gs.Color("base:N").scale(
            domain=["A", "C", "G", "T"],
            range=["#7BD56C", "#FF9B9B", "#86BBF1", "#FFC56C"],
        )

    reference_tiles = (
        gs.Chart(data=reference_url)
        .mark_point(
            shape="square",
            size=420,
            filled=True,
        )
        .encode(x="position:Q", color=base_color())
    )
    reference_labels = (
        gs.Chart(data=reference_url)
        .mark_text(
            size=13,
            color="black",
            tooltip=None,
        )
        .encode(x="position:Q", text="base:N")
    )
    sequence_track = gs.layer(reference_tiles, reference_labels).properties(
        height=55, title="Reference sequence"
    )

    def signal_track(data_url: dict[str, object], title: str, color: str) -> object:
        return (
            gs.Chart(data=data_url)
            .mark_point(size=70, filled=True, color=color)
            .encode(x="position:Q", y="value:Q")
            .properties(height=90, title=title)
        )

    chart = (
        gs.vconcat(
            sequence_track,
            signal_track(reference_url, "Reference signal", "#2563eb"),
            signal_track(alternate_url, "Alternate signal", "#dc2626"),
            signal_track(delta_url, "Mutation impact (delta)", "#7c3aed"),
            spacing=6,
        )
        .resolve_scale(x="shared", y="independent")
        .resolve_axis(x="shared")
        .properties(
            title="Deterministic mutation-impact prototype",
            description=(
                "A small offline example: mutation input, Polars-derived "
                "signals, and Arrow IPC-backed GenomeSpy tracks."
            ),
        )
    )
    chart_widget = chart.widget(enable_click_events=True)
    chart_widget.arrow_data = {
        "reference": gs.to_arrow_ipc(reference),
        "alternate": gs.to_arrow_ipc(alternate),
        "delta": gs.to_arrow_ipc(delta),
    }

    return chart_widget, mutation_error


@app.cell
def _(chart_widget, mo, mutation_error, mutation_input):
    if mutation_error:
        output = mo.vstack(
            [mutation_input, mo.md(f"**{mutation_error}**"), chart_widget]
        )
    else:
        clicked = chart_widget.clicked_datum
        click_summary = (
            f"Last clicked datum: `{clicked}`"
            if clicked
            else "Click a plotted point to send its datum back to Python."
        )
        output = mo.vstack(
            [
                mutation_input,
                mo.md(
                    "Enter a mutation such as `108:G`. The notebook rebuilds "
                    "reference, alternate, and delta tables with Polars, then "
                    "replaces three Arrow IPC payloads."
                ),
                mo.md(click_summary),
                chart_widget,
            ]
        )
    output


if __name__ == "__main__":
    app.run()
