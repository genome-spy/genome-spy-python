"""Shared native renderer and original grouped-data fixtures."""

import warnings
from functools import cache
from importlib.metadata import version

import pytest

from tests.integrations.scanpy.browser.references import render_images
from tests.integrations.scanpy.expression_fixtures import make_grouped_adata

playwright = pytest.importorskip("playwright.sync_api")


@pytest.fixture(scope="session")
def reference_images(tmp_path_factory):
    """Generate pinned upstream images once per family, outside the repository."""
    root = tmp_path_factory.mktemp("scanpy-references")

    @cache
    def render(family):
        """Return this family's temporary exports without refreshing tracked JSON."""
        assert version("scanpy") == "1.11.5", (
            "Visual references use the pinned Scanpy environment"
        )
        output = root / family
        render_images(family, output)
        return output

    return render


@pytest.fixture(scope="session")
def browser():
    """Reuse Chromium while keeping every test in its own browser context."""
    with playwright.sync_playwright() as runtime:
        browser = runtime.chromium.launch()
        try:
            yield browser
        finally:
            browser.close()


@pytest.fixture
def page(request, browser):
    context = browser.new_context(
        viewport={"width": 1800, "height": 1400},
        device_scale_factor=getattr(request, "param", 1),
    )
    page = context.new_page()
    errors = []
    page.on("pageerror", lambda e: errors.append(str(e)))
    try:
        yield page
        assert not errors, errors
    finally:
        context.close()


@pytest.fixture
def adata():
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", UserWarning)
        return make_grouped_adata()
