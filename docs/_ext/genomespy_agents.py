"""Publish plain agent Markdown after successful HTML builds."""

from pathlib import Path
import sys
from typing import Any

from sphinx.application import Sphinx

_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(_ROOT))

from tools.agent_docs import publish_agent_docs  # noqa: E402


def _publish(app: Sphinx, exception: Exception | None) -> None:
    if exception is None and app.builder.format == "html":
        publish_agent_docs(_ROOT, Path(app.outdir), app.config.html_baseurl)


def setup(app: Sphinx) -> dict[str, Any]:
    """Register agent-doc publication after successful HTML builds.

    Args:
        app: Sphinx application.

    Returns:
        Extension version and parallel-read safety metadata.

    Raises:
        None.

    Example:
        >>> setup(app)  # doctest: +SKIP
    """
    app.connect("build-finished", _publish)
    return {"version": "1", "parallel_read_safe": True}
