"""Notebook widget integration for GenomeSpy charts."""

from __future__ import annotations

try:
    import anywidget  # noqa: F401
except ImportError:

    class _MissingJupyterChart:
        """Fallback widget class when anywidget is not installed."""

        def __init__(self, *args: object, **kwargs: object) -> None:
            del args, kwargs
            msg = (
                "The GenomeSpy JupyterChart requires the anywidget Python package.\n"
                "Install it with:\n"
                "    pip install anywidget\n"
                "or sync this project's dependencies with:\n"
                "    uv sync --dev\n"
                "Afterwards, restart the notebook kernel."
            )
            raise ImportError(msg)

    JupyterChart: type[object] = _MissingJupyterChart
else:
    from genome_spy._widget import JupyterChart as _AnywidgetJupyterChart

    JupyterChart = _AnywidgetJupyterChart

__all__ = ["JupyterChart"]
