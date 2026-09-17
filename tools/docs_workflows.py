"""Build live documentation workflows from the notebooks' tagged chart cells."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
NOTEBOOKS = {
    "intervals": ROOT / "notebooks" / "annotate_genomic_intervals.ipynb",
    "genes": ROOT / "notebooks" / "select_genes.ipynb",
    "points": ROOT / "notebooks" / "pick_genes.ipynb",
    "sequence": ROOT / "notebooks" / "edit_sequence.ipynb",
}


def load_spec(name: str) -> dict[str, Any]:
    """Execute only the notebook's chart cell, without opening a widget."""
    path = NOTEBOOKS[name]
    notebook = json.loads(path.read_text())
    cells = [
        cell
        for cell in notebook["cells"]
        if cell["cell_type"] == "code"
        and "workflow-chart" in cell.get("metadata", {}).get("tags", [])
    ]
    if len(cells) != 1:
        raise ValueError(f"{path.name} must have exactly one workflow-chart cell.")
    namespace: dict[str, Any] = {}
    exec(compile("".join(cells[0]["source"]), str(path), "exec"), namespace)
    return namespace["chart"].to_dict()


def embed_html(name: str, spec_url: str, bundle_url: str, script_url: str) -> str:
    """Render one direct embed and its small browser-side form."""
    if name not in NOTEBOOKS:
        raise ValueError(f"Unknown workflow: {name}")
    height = {"intervals": 446, "genes": 420, "points": 420, "sequence": 350}[name]
    fields = (
        """
      <label>Name <input name="name" required placeholder="e.g. GC-rich-region" autocomplete="off"></label>
      <label>Note <input name="note" placeholder="Optional" autocomplete="off"></label>
      <button type="submit" data-save disabled>Save annotation</button>
    """
        if name == "intervals"
        else ""
    )
    download = {"intervals": "Download BED", "sequence": "Download FASTA"}.get(
        name, "Download selected genes"
    )
    title = {
        "intervals": "Genomic interval annotation",
        "sequence": "Sequence mutator",
    }.get(name, "Gene selection")
    mount = {
        "intervals": "mountIntervals(root, api);",
        "genes": "mountGenes(root, api, spec.datasets[spec.data.name]);",
        "points": "mountPoints(root, api);",
        "sequence": "mountSequence(root, api, spec.datasets.reference);",
    }[name]
    return f"""
<section id="workflow-{name}" class="gs-workflow" aria-label="{title}">
  <div id="workflow-{name}-chart" class="gs-doc-embed" style="height:{height}px" aria-label="{title} chart"></div>
  <form>
    <fieldset disabled>
      {fields}
      <button type="button" data-clear>Clear brush</button>
      <button type="button" data-download disabled>{download}</button>
    </fieldset>
  </form>
  <p data-status role="status" aria-live="polite">Loading chart…</p>
  <div class="gs-workflow-table" tabindex="0" aria-label="Results table"><table data-results></table></div>
  <noscript>Enable JavaScript to use this demo, or download the notebook below.</noscript>
</section>
<script type="module">
import {{ embed }} from {json.dumps(bundle_url)};
import {{ mountIntervals, mountGenes, mountPoints, mountSequence }} from {json.dumps(script_url)};
const root = document.getElementById("workflow-{name}");
const c = document.getElementById("workflow-{name}-chart");
try {{
  const response = await fetch({json.dumps(spec_url)});
  if (!response.ok) throw new Error(`Could not load chart (${{response.status}})`);
  const spec = await response.json();
  spec.width = "container";
  const api = await embed(c, spec, {{ bare: true }});
  {mount}
}} catch (error) {{
  root.querySelector('[data-status]').textContent = `Unable to load demo: ${{error.message}}`;
}}
</script>
"""
