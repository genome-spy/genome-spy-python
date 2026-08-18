"""Executable snippets used by the serialization and sharing guide."""

from pathlib import Path

import genome_spy as gs


records = [
    {"sample": "A", "value": 2.1, "group": "control"},
    {"sample": "B", "value": 3.4, "group": "control"},
    {"sample": "C", "value": 4.2, "group": "treated"},
]

chart = (
    gs.Chart(records)
    .mark_point(filled=True, size=120)
    .encode(
        x=gs.X("sample:N").title("Sample"),
        y=gs.Y("value:Q").title("Measurement"),
        color=gs.Color("group:N"),
    )
    .properties(height=180, title="Serializable measurements")
)


# serialization-dict-start
spec = chart.to_dict()

mark_definition = spec["mark"]
x_definition = spec["encoding"]["x"]
schema_url = spec["$schema"]
# serialization-dict-end


# serialization-json-start
json_spec = chart.to_json()
# serialization-json-end


# serialization-save-start
def save_examples(directory: Path) -> tuple[Path, Path]:
    """Save JSON and browser-runnable HTML examples in a directory."""
    json_path = directory / "measurements.json"
    html_path = directory / "measurements.html"
    chart.save(json_path)
    chart.save(html_path)
    return json_path, html_path


# serialization-save-end


CHARTS = {"chart": chart}
