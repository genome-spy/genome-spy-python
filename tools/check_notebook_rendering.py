"""Render the brush notebook through a real JupyterLab server and Chromium.

Run with the Python environment being tested. It must contain the installed
package, JupyterLab, pandas, NumPy, Playwright, and Pillow. No source checkout
is added to the kernel's import path. Browser modules require network access.
"""

from __future__ import annotations

import argparse
import io
import json
import os
from pathlib import Path
import re
import secrets
import subprocess
import sys
import tempfile
import time

from PIL import Image
from playwright.sync_api import sync_playwright


def _observe_rendering(page, console: list) -> None:
    """Record browser warnings and context loss before notebook widgets load."""
    page.on(
        "console",
        lambda message: console.append({"type": message.type, "text": message.text}),
    )
    page.on(
        "requestfailed",
        lambda request: console.append(
            {"type": "requestfailed", "text": f"{request.url}: {request.failure}"}
        ),
    )
    page.add_init_script("""
        window.notebookContextEvents = [];
        for (const type of ['webglcontextlost', 'webglcontextrestored',
                            'webglcontextcreationerror']) {
            document.addEventListener(type, event => {
                window.notebookContextEvents.push({type,
                    time: performance.now(), message: event.statusMessage,
                    canvasIndex: [...document.querySelectorAll('canvas')]
                        .indexOf(event.target)});
            }, true);
        }
    """)


def _rendering_state(canvas) -> dict:
    """Read notebook and canvas state without changing the chart."""
    return canvas.evaluate("""canvas => {
        const bounds = el => {
            const r = el.getBoundingClientRect();
            const style = getComputedStyle(el);
            return {x: r.x, y: r.y, width: r.width, height: r.height,
                display: style.display, visibility: style.visibility};
        };
        const widget = window.jupyterapp?.shell.currentWidget;
        const cell = canvas.closest('.jp-CodeCell');
        const ancestors = [];
        for (let el = canvas.parentElement; el; el = el.parentElement) {
            ancestors.push({className: el.className, ...bounds(el)});
        }
        return {
            kernelStatus: widget?.sessionContext.session?.kernel?.status,
            cellIndex: [...document.querySelectorAll('.jp-CodeCell')].indexOf(cell),
            source: cell?.querySelector('.jp-InputArea')?.textContent,
            output: cell?.querySelector('.jp-OutputArea')?.textContent,
            canvas: {bufferWidth: canvas.width, bufferHeight: canvas.height, ...bounds(canvas)},
            ancestors,
            canvases: [...document.querySelectorAll('.jp-OutputArea canvas')]
                .map(el => ({bufferWidth: el.width, bufferHeight: el.height, ...bounds(el)})),
            contextEvents: window.notebookContextEvents,
            errors: [...document.querySelectorAll('.jp-OutputArea-error')]
                .map(el => el.textContent),
        };
    }""")


def _scroll_to_canvas(page, canvas) -> None:
    """Let Jupyter lay out an offscreen cell before scrolling to its chart."""
    page.wait_for_function(
        """async canvas => {
            const notebook = window.jupyterapp.shell.currentWidget.content;
            const index = notebook.widgets.findIndex(cell => cell.node.contains(canvas));
            if (index < 0) throw new Error('Chart does not belong to a notebook cell');
            await notebook.scrollToItem(index, 'start');
            return true;
        }""",
        arg=canvas.element_handle(),
    )
    canvas.scroll_into_view_if_needed()


def _check_canvas(
    page, canvas, screenshot: Path, console: list, errors: list, token: str
) -> None:
    """Assert the chart has painted; save browser state when it has not."""
    state = _rendering_state(canvas)
    pixels = canvas.screenshot(path=str(screenshot))
    # A canvas element alone can exist even when rendering failed.
    colors = Image.open(io.BytesIO(pixels)).convert("RGB").getcolors(1_000_000)
    if colors is None or len(colors) < 20:
        state.update(
            afterScreenshot=_rendering_state(canvas),
            console=console,
            pageErrors=errors,
            colorCount=None if colors is None else len(colors),
        )
        screenshot.with_suffix(".json").write_text(
            json.dumps(state, indent=2).replace(token, "<redacted>")
        )
        page.screenshot(path=str(screenshot.with_suffix(".page.png")))
        raise AssertionError("Chart canvas is blank or unexpectedly uniform")


def _run_kernel(page, code: str) -> None:
    status = page.evaluate(
        """async code => {
        const kernel = window.jupyterapp.shell.currentWidget.sessionContext.session.kernel;
        const reply = await kernel.requestExecute({code, store_history: false}).done;
        return reply.content;
    }""",
        code,
    )
    assert status["status"] == "ok", status


def _wait_kernel(page, expression: str) -> None:
    # Separate requests leave the kernel free to process widget replies.
    page.evaluate(
        """async expression => {
        const kernel = window.jupyterapp.shell.currentWidget.sessionContext.session.kernel;
        const deadline = Date.now() + 30000;
        do {
            const reply = await kernel.requestExecute({
                code: '', store_history: false,
                user_expressions: {ready: `bool(${expression})`}
            }).done;
            const result = reply.content.user_expressions.ready;
            if (result.status !== 'ok') throw new Error(JSON.stringify(result));
            if (result.data['text/plain'] === 'True') return;
            await new Promise(resolve => setTimeout(resolve, 50));
        } while (Date.now() < deadline);
        throw new Error(`Timed out waiting for Python: ${expression}`);
    }""",
        expression,
    )


def _check_workflow(page, canvas, workflow: str) -> None:
    if workflow == "python-rows":
        _check_python_rows(page, canvas)
        return
    if workflow == "agent-embed":
        _check_agent_embed(page, canvas)
        return
    if workflow in ("points", "sequence"):
        ready = (
            "0 genes selected."
            if workflow == "points"
            else "Ready. Click a cell to change that position."
        )
        page.get_by_text(ready, exact=True).wait_for()
        canvas.scroll_into_view_if_needed()
        bounds = canvas.bounding_box()
        assert bounds is not None
        if workflow == "sequence":
            page.mouse.move(bounds["x"] + 48, bounds["y"] + 200)
            page.wait_for_timeout(100)
            page.mouse.click(bounds["x"] + 48, bounds["y"] + 200)
            page.get_by_text("Edited: CCGTGCAATGCTAGCTACGATCGA", exact=True).wait_for()
            _run_kernel(
                page,
                "assert ''.join(edited_sequence) == 'C' + REFERENCE[1:]\nassert REFERENCE.startswith('A')",
            )
        else:
            for fraction in (0.45, 0.46, 0.47, 0.48, 0.49):
                page.mouse.click(
                    bounds["x"] + bounds["width"] * fraction, bounds["y"] + 270
                )
                page.wait_for_timeout(150)
                if page.get_by_text("1 genes selected.", exact=True).count():
                    break
            page.get_by_text("1 genes selected.", exact=True).wait_for()
            _run_kernel(
                page,
                "assert len(selected_genes) == 1\nassert selected_genes.iloc[0].ensgene.startswith('ENSG')",
            )
        return
    if workflow == "intervals":
        page.get_by_text(
            "Ready — brush the chart, enter a name, then save.", exact=True
        ).wait_for()
    else:
        page.get_by_text(
            "0 genes selected. Showing up to 20 rows.", exact=True
        ).wait_for()
    canvas.scroll_into_view_if_needed()
    bounds = canvas.bounding_box()
    assert bounds is not None
    x, y, width, height = (bounds[key] for key in ("x", "y", "width", "height"))
    page.mouse.move(x + width * 0.55, y + height * 0.12)
    page.mouse.down()
    page.mouse.move(
        x + width * 0.82,
        y + height * (0.25 if workflow == "intervals" else 0.85),
        steps=12,
    )
    page.mouse.up()
    if workflow == "intervals":
        page.get_by_role("textbox", name="Name:", exact=True).fill("GC-rich-region")
        page.get_by_role("textbox", name="Note:", exact=True).fill(
            "Candidate for follow-up"
        )
        page.get_by_role("button", name="Save annotation", exact=True).click()
        page.wait_for_timeout(1500)
        _run_kernel(page, "assert not ('Error:' in status.value), status.value")
        page.get_by_text("Saved 1 annotation(s).", exact=True).wait_for()
        page.get_by_role("button", name="Export BED", exact=True).click()
        page.locator('a[href*="annotations.hg38."]').wait_for()
        _run_kernel(
            page,
            """assert len(annotations) == 1
assert annotations[0]['chrom'] == 'chr5'
assert 177500000 <= annotations[0]['start'] < annotations[0]['end'] <= 177700000
bed = list(Path('.').glob('annotations.hg38.*.bed'))
assert len(bed) == 1
assert bed[0].read_text().strip().split('\\t') == [str(annotations[0][key]) for key in ('chrom', 'start', 'end', 'name')]
""",
        )
    else:
        export = page.get_by_role("button", name="Export selected genes", exact=True)
        export.click()
        page.locator('a[href*="selected-genes."]').wait_for()
        _run_kernel(
            page,
            """import pandas as pd
assert len(selected_genes) > 20
csv = list(Path('.').glob('selected-genes.*.csv'))
assert len(csv) == 1
exported = pd.read_csv(csv[0])
assert exported.ensgene.tolist() == selected_genes.ensgene.tolist()
""",
        )


def _check_agent_embed(page, canvas) -> None:
    page.get_by_text("Ready: 0 selected", exact=True).wait_for()
    canvas.scroll_into_view_if_needed()
    before = Image.open(io.BytesIO(canvas.screenshot())).convert("RGB")
    bounds = canvas.bounding_box()
    assert bounds is not None
    page.mouse.move(bounds["x"] + bounds["width"] * 0.35, bounds["y"] + 80)
    page.mouse.down()
    page.mouse.move(bounds["x"] + bounds["width"] * 0.60, bounds["y"] + 100, steps=12)
    # Commit delivery must leave Python untouched until release.
    _run_kernel(page, "assert selected_rows == []")
    page.mouse.up()
    page.get_by_text("Ready: 2 selected", exact=True).wait_for()
    _run_kernel(page, "assert [row['id'] for row in selected_rows] == ['b', 'c']")
    after = Image.open(io.BytesIO(canvas.screenshot())).convert("RGB")
    lower = (0, before.height // 2, before.width, before.height)
    assert before.crop(lower).tobytes() != after.crop(lower).tobytes(), (
        "The Python result did not change the lower plot"
    )
    page.get_by_role("button", name="Change chart", exact=True).click()
    page.get_by_text("Ready: 0 selected", exact=True).wait_for()
    _run_kernel(
        page,
        "assert operation_future.done()\nassert operation_future.result() == 90\n"
        "assert selected_rows == []",
    )
    cleared = Image.open(io.BytesIO(canvas.screenshot())).convert("RGB")
    assert before.crop(lower).tobytes() == cleared.crop(lower).tobytes(), (
        "Clearing did not empty the lower plot"
    )
    _run_kernel(
        page,
        """async def set_range(interval):
    async with asyncio.timeout(30):
        parameter = await api.params.get('brush')
        await parameter.set_value({'type': 'interval', 'intervals': {'x': interval}})
        return await selection.get_value()
empty_task = asyncio.create_task(set_range([4.5, 4.8]))
""",
    )
    _wait_kernel(page, "empty_task.done()")
    _run_kernel(
        page,
        "assert empty_task.done()\nassert empty_task.result()['intervals']['x'] == [4.5, 4.8]\n"
        "assert empty_task.result()['active']\nassert selected_rows == []\n"
        "select_task = asyncio.create_task(set_range([1, 3]))\n"
        "old_connection_task = connection_task\nold_widget = widget\nold_api = api",
    )
    page.get_by_text("Ready: 2 selected", exact=True).wait_for()
    _wait_kernel(page, "select_task.done()")
    _run_kernel(
        page,
        "assert select_task.done()\nselect_task.result()\n"
        "assert [row['id'] for row in selected_rows] == ['a', 'b']",
    )


def _check_python_rows(page, canvas) -> None:
    page.get_by_text("Ready — 0 rows in Python", exact=False).wait_for()
    source = page.locator(".jp-OutputArea canvas").first
    source.scroll_into_view_if_needed()
    before = Image.open(io.BytesIO(canvas.screenshot())).convert("RGB")
    bounds = source.bounding_box()
    assert bounds is not None
    _run_kernel(page, "assert update_count == 1\nassert selected_rows == []")
    page.mouse.move(bounds["x"] + 190, bounds["y"] + 100)
    page.mouse.down()
    page.mouse.move(bounds["x"] + 330, bounds["y"] + 230, steps=12)
    _run_kernel(page, "assert update_count == 1\nassert selected_rows == []")
    page.mouse.up()
    page.wait_for_function("""() => [...document.querySelectorAll('.widget-label')]
        .some(el => /Ready — [1-9][0-9]* rows in Python/.test(el.textContent))""")
    _run_kernel(
        page,
        "assert 0 < len(selected_rows) < len(rows)\n"
        "assert update_count == 2\nassert latest_snapshot['active']",
    )
    assert (
        before.tobytes()
        != Image.open(io.BytesIO(canvas.screenshot())).convert("RGB").tobytes()
    )
    page.get_by_role("button", name="Clear brush", exact=True).click()
    page.get_by_text("Ready — 0 rows in Python", exact=False).wait_for()
    _run_kernel(
        page,
        "clear_task.result()\nassert selected_rows == []\nassert not latest_snapshot['active']",
    )
    assert (
        before.tobytes()
        == Image.open(io.BytesIO(canvas.screenshot())).convert("RGB").tobytes()
    )
    _run_kernel(
        page,
        """async def set_range(x, y):
    async with asyncio.timeout(30):
        parameter = await source_api.params.get('brush')
        await parameter.set_value({'type': 'interval', 'intervals': {'x': x, 'y': y}})
        return await selection.get_value()
empty_task = asyncio.create_task(set_range([30, 31], [12, 13]))
""",
    )
    _wait_kernel(page, "empty_task.done() and update_count == 4")
    _run_kernel(
        page,
        "assert empty_task.done()\nassert empty_task.result()['active']\n"
        "assert selected_rows == []\nassert update_count == 4\n"
        "select_task = asyncio.create_task(set_range([40, 50], [15, 19]))",
    )
    page.get_by_text("Ready — 103 rows in Python", exact=False).wait_for()
    _wait_kernel(page, "select_task.done()")
    _run_kernel(
        page,
        "assert len(selected_rows) == len({row['row_id'] for row in selected_rows}) == 103\n"
        "assert selected_counts == {'Chinstrap': 32, 'Adelie': 32, 'Gentoo': 39}\n"
        "assert all(40 <= row[x_field] < 50 and 15 <= row[y_field] < 19 for row in selected_rows)\n"
        "assert update_count == 5\nselect_task.result()\n"
        "old_connection_task = connection_task\nold_source_widget = source_widget\nold_target_widget = target_widget",
    )
    pixels = Image.open(io.BytesIO(canvas.screenshot())).convert("RGB")
    palette = [(191, 92, 202), (255, 108, 2), (15, 117, 116)]
    color_counts = {color: count for count, color in pixels.getcolors(1_000_000)}
    areas = [color_counts.get(color, 0) for color in palette]
    ratios = [area / count for area, count in zip(areas, [32, 32, 39], strict=True)]
    assert min(ratios) > 0 and max(ratios) / min(ratios) < 1.05, (areas, ratios)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("notebook", type=Path)
    parser.add_argument("--screenshot", type=Path, required=True)
    parser.add_argument("--check-embed-interactions", action="store_true")
    parser.add_argument(
        "--workflow",
        choices=[
            "intervals",
            "genes",
            "points",
            "sequence",
            "agent-embed",
            "python-rows",
        ],
    )
    args = parser.parse_args()
    if args.notebook.suffix == ".md":
        import nbformat

        blocks = re.findall(
            r"```python\n(.*?)```", args.notebook.read_text(), re.DOTALL
        )
        if not blocks:
            raise ValueError("The guide contains no Python examples")
        notebook = nbformat.v4.new_notebook(
            cells=[nbformat.v4.new_code_cell(block) for block in blocks],
            metadata={
                "kernelspec": {
                    "name": "python3",
                    "display_name": "Python 3",
                    "language": "python",
                }
            },
        )
    else:
        notebook = json.loads(args.notebook.read_text())
    # Test fresh execution, not saved outputs or widget state from another kernel.
    notebook["metadata"].pop("widgets", None)
    for cell in notebook["cells"]:
        if cell["cell_type"] == "code":
            cell["outputs"] = []
            cell["execution_count"] = None
            if args.check_embed_interactions:
                # Exercise attachment before the frontend has installed listeners.
                source = "".join(cell["source"]).replace(
                    "widget = chart.widget(inline=True, controls=False)",
                    "from genome_spy._widget import JupyterChart\n"
                    "widget = JupyterChart(chart, inline=True, controls=False, "
                    '_esm="await new Promise(r => setTimeout(r, 1500));\\n" + str(JupyterChart._esm))',
                )
                cell["source"] = source.splitlines(keepends=True)

    with tempfile.TemporaryDirectory(prefix="genomespy-notebook-") as directory:
        root = Path(directory)
        (root / "smoke.ipynb").write_text(json.dumps(notebook))
        runtime = root / "runtime"
        runtime.mkdir()
        env = dict(os.environ)
        # Do not let a user's Jupyter configuration mask a broken installation.
        for key in ("PYTHONPATH", "JUPYTER_PATH", "JUPYTER_CONFIG_PATH"):
            env.pop(key, None)
        env.update(
            JUPYTER_RUNTIME_DIR=str(runtime),
            JUPYTER_CONFIG_DIR=str(root / "config"),
            JUPYTER_DATA_DIR=str(root / "data"),
            PYTHONNOUSERSITE="1",
        )
        token = secrets.token_hex(24)
        with (root / "server.log").open("w+") as log:
            server = subprocess.Popen(
                [
                    sys.executable,
                    "-m",
                    "jupyterlab",
                    "--no-browser",
                    "--ServerApp.ip=127.0.0.1",
                    "--ServerApp.port=0",
                    f"--IdentityProvider.token={token}",
                    "--LabApp.expose_app_in_browser=True",
                    f"--ServerApp.root_dir={root}",
                ],
                cwd=root,
                env=env,
                stdout=log,
                stderr=subprocess.STDOUT,
            )
            try:
                deadline = time.monotonic() + 60
                while not list(runtime.glob("jpserver-*.json")):
                    if server.poll() is not None or time.monotonic() > deadline:
                        raise RuntimeError("JupyterLab failed to start")
                    time.sleep(0.2)
                info = json.loads(next(runtime.glob("jpserver-*.json")).read_text())
                url = f"http://127.0.0.1:{info['port']}"
                with sync_playwright() as playwright:
                    browser = playwright.chromium.launch()
                    try:
                        page = browser.new_page(
                            viewport={"width": 1500, "height": 1100}
                        )
                        errors: list[str] = []
                        console: list[dict] = []
                        page.on("pageerror", lambda error: errors.append(str(error)))
                        _observe_rendering(page, console)
                        page.goto(f"{url}/lab/tree/smoke.ipynb?token={token}")
                        page.wait_for_function(
                            "window.jupyterapp?.shell.currentWidget?.context?.isReady"
                        )
                        page.wait_for_function(
                            "window.jupyterapp.shell.currentWidget.sessionContext.session?.kernel"
                        )
                        prefix = page.evaluate("""async () => {
                            const kernel = window.jupyterapp.shell.currentWidget.sessionContext.session.kernel;
                            const request = kernel.requestExecute({
                                code: 'import sys; print(sys.prefix)', store_history: false
                            });
                            let output = '';
                            request.onIOPub = msg => {
                                if (msg.header.msg_type === 'stream') output += msg.content.text;
                            };
                            await request.done;
                            return output.trim();
                        }""")
                        if Path(prefix).resolve() != Path(sys.prefix).resolve():
                            raise AssertionError(f"Wrong kernel environment: {prefix}")
                        page.evaluate(
                            "window.jupyterapp.commands.execute('notebook:run-all-cells')"
                        )
                        # Check the completed chart, not an earlier tutorial preview.
                        canvas = (
                            page.locator(".jp-CodeCell")
                            .filter(has=page.locator(".jp-OutputArea canvas"))
                            .last.locator(".jp-OutputArea canvas")
                            .first
                        )
                        if args.check_embed_interactions:
                            canvas = (
                                page.locator(".jp-CodeCell")
                                .filter(has=page.locator(".jp-OutputArea canvas"))
                                .first.locator(".jp-OutputArea canvas")
                                .first
                            )
                        elif args.workflow == "python-rows":
                            canvas = page.locator(".jp-OutputArea canvas").last
                        canvas.wait_for(state="visible", timeout=120_000)
                        _scroll_to_canvas(page, canvas)
                        page.wait_for_timeout(2000)
                        if page.locator(".jp-OutputArea-error").count() or errors:
                            raise AssertionError(f"Notebook rendering errors: {errors}")
                        if args.check_embed_interactions:
                            page.get_by_text(
                                "Saved selections: 0", exact=True
                            ).wait_for()
                            page.locator(".jp-OutputArea").get_by_text(
                                "No active selection", exact=False
                            ).wait_for()
                            canvas.scroll_into_view_if_needed()
                            bounds = canvas.bounding_box()
                            assert bounds is not None
                            for count, (start, end) in enumerate(
                                [(0.2, 0.5), (0.6, 0.85)], start=1
                            ):
                                x, y = bounds["x"], bounds["y"]
                                width, height = bounds["width"], bounds["height"]
                                page.mouse.move(x + width * start, y + height * 0.4)
                                page.mouse.down()
                                page.mouse.move(
                                    x + width * end, y + height * 0.65, steps=8
                                )
                                # Changes arrive before release; no commit is saved yet.
                                page.get_by_text(
                                    "Saved selections: " + str(count - 1), exact=True
                                ).wait_for()
                                page.wait_for_function("""() => {
                                    const outputs = document.querySelectorAll('.jp-OutputArea');
                                    return [...outputs].some(el =>
                                        el.textContent.includes('Current x range:') &&
                                        !el.textContent.includes('No active selection'));
                                }""")
                                page.mouse.up()
                                page.get_by_text(
                                    f"Saved selections: {count}", exact=True
                                ).wait_for()
                            # Verify actual Python state, not only rendered text.
                            status = page.evaluate("""async () => {
                                const kernel = window.jupyterapp.shell.currentWidget.sessionContext.session.kernel;
                                const result = await kernel.requestExecute({code:
                                    'assert len(regions) == 2\\n' +
                                    'assert regions[0]["intervals"] != regions[1]["intervals"]\\n' +
                                    'assert latest_selection["active"] and selected_rows\\n' +
                                    'clear_task = asyncio.create_task(selection.clear())', store_history: false
                                }).done;
                                return result.content.status;
                            }""")
                            assert status == "ok", (
                                "Python selection state did not update"
                            )
                            page.get_by_text(
                                "Saved selections: 3", exact=True
                            ).wait_for()
                            page.locator(".jp-OutputArea").get_by_text(
                                "No active selection", exact=False
                            ).wait_for()
                            # Save a named annotation through the notebook form.
                            canvas = (
                                page.locator(".jp-CodeCell")
                                .filter(has=page.locator(".jp-OutputArea canvas"))
                                .last.locator(".jp-OutputArea canvas")
                                .first
                            )
                            page.get_by_text(
                                "Ready — brush the chart directly above this form.",
                                exact=True,
                            ).wait_for()
                            canvas.scroll_into_view_if_needed()
                            bounds = canvas.bounding_box()
                            assert bounds is not None
                            page.mouse.move(
                                bounds["x"] + bounds["width"] * 0.3,
                                bounds["y"] + bounds["height"] * 0.4,
                            )
                            page.mouse.down()
                            page.mouse.move(
                                bounds["x"] + bounds["width"] * 0.6,
                                bounds["y"] + bounds["height"] * 0.6,
                                steps=8,
                            )
                            page.mouse.up()
                            page.get_by_role("textbox", name="Name:", exact=True).fill(
                                "Example region"
                            )
                            page.get_by_role("textbox", name="Description:").fill(
                                "Saved from the brush"
                            )
                            page.get_by_role("button", name="Save annotation").click()
                            page.get_by_text(
                                "Saved 1 annotation(s) in Python memory.", exact=True
                            ).wait_for()
                            page.get_by_role("cell", name="Example region").wait_for()
                            status = page.evaluate("""async () => {
                                const kernel = window.jupyterapp.shell.currentWidget.sessionContext.session.kernel;
                                const result = await kernel.requestExecute({code:
                                    'assert len(annotations) == 1\\n' +
                                    'assert len(regions) == 3 and not latest_selection["active"]\\n' +
                                    'assert annotations[0]["name"] == "Example region"\\n' +
                                    'assert annotations[0]["description"] == "Saved from the brush"\\n' +
                                    'assert annotations[0]["start"] < annotations[0]["end"]',
                                    store_history: false
                                }).done;
                                return result.content.status;
                            }""")
                            assert status == "ok", "Annotation was not saved in Python"
                        args.screenshot.parent.mkdir(parents=True, exist_ok=True)
                        if args.workflow:
                            _check_workflow(page, canvas, args.workflow)
                        _check_canvas(
                            page, canvas, args.screenshot, console, errors, token
                        )
                        if args.workflow:
                            page.set_viewport_size({"width": 1500, "height": 1800})
                            canvas.locator(
                                "xpath=ancestor::div[contains(concat(' ', normalize-space(@class), ' '), ' jp-OutputArea ')][1]"
                            ).screenshot(path=str(args.screenshot))
                            # Rerunning resets in-memory state, not exported files.
                            page.evaluate(
                                "window.jupyterapp.commands.execute('notebook:run-all-cells')"
                            )
                            if args.workflow == "python-rows":
                                page.get_by_text(
                                    "Ready — 0 rows in Python", exact=False
                                ).wait_for()
                                _run_kernel(
                                    page,
                                    "assert selected_rows == []\nassert old_connection_task.done()\n"
                                    "assert source_widget is not old_source_widget\n"
                                    "assert target_widget is not old_target_widget\n"
                                    "assert not connection_task.done()",
                                )
                                canvas = page.locator(".jp-OutputArea canvas").last
                                _check_python_rows(page, canvas)
                                _run_kernel(
                                    page,
                                    "cleanup_task = asyncio.create_task(stop_example())",
                                )
                                _wait_kernel(page, "cleanup_task.done()")
                                _run_kernel(
                                    page,
                                    "cleanup_task.result()\nassert connection_task.cancelled()",
                                )
                            elif args.workflow == "agent-embed":
                                page.get_by_text(
                                    "Ready: 0 selected", exact=True
                                ).wait_for()
                                _run_kernel(
                                    page,
                                    "assert selected_rows == []\nassert old_connection_task.done()\n"
                                    "assert widget is not old_widget and api is not old_api\n"
                                    "assert not connection_task.done()",
                                )
                                canvas = page.locator(".jp-OutputArea canvas").last
                                _check_agent_embed(page, canvas)
                                _run_kernel(
                                    page,
                                    "cleanup_task = asyncio.create_task(stop_example())",
                                )
                                _wait_kernel(page, "cleanup_task.done()")
                                _run_kernel(
                                    page,
                                    "assert cleanup_task.done()\ncleanup_task.result()\n"
                                    "assert connection_task.cancelled()",
                                )
                            elif args.workflow == "intervals":
                                page.get_by_text(
                                    "Ready — brush the chart, enter a name, then save.",
                                    exact=True,
                                ).wait_for()
                                _run_kernel(
                                    page,
                                    "assert annotations == []\nassert len(list(Path('.').glob('annotations.hg38.*.bed'))) == 1",
                                )
                            elif args.workflow in ("points", "sequence"):
                                ready = (
                                    "0 genes selected."
                                    if args.workflow == "points"
                                    else "Ready. Click a cell to change that position."
                                )
                                page.get_by_text(ready, exact=True).wait_for()
                                _run_kernel(
                                    page,
                                    "assert selected_genes.empty"
                                    if args.workflow == "points"
                                    else "assert ''.join(edited_sequence) == REFERENCE",
                                )
                            else:
                                page.get_by_text(
                                    "0 genes selected. Showing up to 20 rows.",
                                    exact=True,
                                ).wait_for()
                                _run_kernel(
                                    page,
                                    "assert selected_genes.empty\nassert len(list(Path('.').glob('selected-genes.*.csv'))) == 1",
                                )
                    finally:
                        browser.close()
            except Exception:
                log.seek(0)
                server_log = log.read().replace(token, "<redacted>")
                args.screenshot.parent.mkdir(parents=True, exist_ok=True)
                args.screenshot.with_suffix(".server.log").write_text(server_log)
                sys.stderr.write(server_log)
                raise
            finally:
                server.terminate()
                try:
                    server.wait(timeout=15)
                except subprocess.TimeoutExpired:
                    server.kill()
                    server.wait()


if __name__ == "__main__":
    main()
