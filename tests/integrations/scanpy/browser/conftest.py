"""Shared native renderer and original grouped-data fixtures."""

from functools import cache
from importlib import import_module
import warnings

import pytest

from tests.integrations.scanpy.grouped_fixture import make_grouped_adata

playwright = pytest.importorskip("playwright.sync_api")


@pytest.fixture(scope="session")
def reference_images(tmp_path_factory):
    """Generate pinned upstream images once per family, outside the repository."""
    root = tmp_path_factory.mktemp("scanpy-references")

    @cache
    def render(family):
        """Return this family's temporary exports without refreshing tracked JSON."""
        module = (
            "generate_references"
            if family == "umap"
            else f"generate_{family}_references"
        )
        output = root / family
        import_module(f"tests.integrations.scanpy.{module}").main(output)
        return output

    return render


@pytest.fixture
def page(request):
    with playwright.sync_playwright() as runtime:
        browser = runtime.chromium.launch()
        context = browser.new_context(
            viewport={"width": 1800, "height": 1400},
            device_scale_factor=getattr(request, "param", 1),
        )
        page = context.new_page()
        errors = []
        page.on("pageerror", lambda e: errors.append(str(e)))
        yield page
        assert not errors, errors
        browser.close()


@pytest.fixture
def adata():
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", UserWarning)
        return make_grouped_adata()
