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
import secrets
import subprocess
import sys
import tempfile
import time

from PIL import Image
from playwright.sync_api import sync_playwright


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("notebook", type=Path)
    parser.add_argument("--screenshot", type=Path, required=True)
    parser.add_argument("--check-embed-interactions", action="store_true")
    args = parser.parse_args()
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
                        page.on("pageerror", lambda error: errors.append(str(error)))
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
                        canvas.wait_for(state="visible", timeout=120_000)
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
                        pixels = canvas.screenshot(path=str(args.screenshot))
                        # A canvas element alone can exist even when rendering failed.
                        colors = (
                            Image.open(io.BytesIO(pixels))
                            .convert("RGB")
                            .getcolors(1_000_000)
                        )
                        if colors is None or len(colors) < 20:
                            raise AssertionError(
                                "Chart canvas is blank or unexpectedly uniform"
                            )
                    finally:
                        browser.close()
            except Exception:
                log.seek(0)
                sys.stderr.write(log.read())
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
