"""Sphinx configuration for the genome-spy-python documentation."""

from __future__ import annotations

import sys
from pathlib import Path

_DOCS = Path(__file__).resolve().parent
_ROOT = _DOCS.parent
sys.path.insert(0, str(_ROOT / "src"))
sys.path.insert(0, str(_DOCS / "_ext"))

from genome_spy import __version__ as _gs_version  # noqa: E402

project = "genome-spy-python"
author = "genome-spy-python contributors"
copyright = "genome-spy-python contributors"
release = _gs_version
version = _gs_version

extensions = [
    "myst_parser",
    "sphinx_design",
    "sphinx_copybutton",
    "sphinx.ext.autodoc",
    "sphinx.ext.autosummary",
    "sphinx.ext.napoleon",
    "sphinx.ext.intersphinx",
    "genomespy_gallery",
]

myst_enable_extensions = [
    "colon_fence",
    "attrs_block",
    "attrs_inline",
    "deflist",
]

# Generated gallery pages and Sphinx scaffolding are not prose sources.
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store", "examples"]

autosummary_generate = True
autodoc_typehints = "none"
autodoc_member_order = "bysource"
napoleon_google_docstring = True
napoleon_numpy_docstring = False

intersphinx_mapping = {"python": ("https://docs.python.org/3", None)}

# -- HTML output ------------------------------------------------------------
html_theme = "furo"
html_title = "genome-spy-python"
html_logo = "_static/snaketie.svg"
html_static_path = ["_static"]
templates_path = ["_templates"]
html_css_files = ["genomespy.css"]
html_js_files = ["force-light-theme.js"]
html_show_sourcelink = False
html_meta = {
    "Cache-Control": "no-cache, no-store, must-revalidate",
    "Pragma": "no-cache",
    "Expires": "0",
}

html_theme_options = {
    "light_css_variables": {
        "color-brand-primary": "#3e8cb6",
        "color-brand-content": "#3797ce",
        "font-stack": '"Lato", -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif',
    },
    "footer_icons": [
        {
            "name": "GitHub",
            "url": "https://github.com/genome-spy/genome-spy-python",
            "html": """
                <svg stroke="currentColor" fill="currentColor" stroke-width="0"
                     viewBox="0 0 16 16" height="1em" width="1em"
                     xmlns="http://www.w3.org/2000/svg">
                  <path d="M8 0C3.58 0 0 3.64 0 8.13c0 3.59 2.29 6.64 5.47 7.71.4.08.55-.18.55-.39 0-.19-.01-.83-.01-1.51-2.01.38-2.53-.5-2.69-.96-.09-.23-.48-.96-.82-1.15-.28-.15-.68-.52-.01-.53.63-.01 1.08.59 1.23.83.72 1.23 1.87.88 2.33.67.07-.53.28-.88.51-1.08-1.78-.21-3.64-.91-3.64-4.02 0-.89.31-1.62.82-2.19-.08-.2-.36-1.04.08-2.16 0 0 .67-.22 2.2.84A7.5 7.5 0 0 1 8 3.92a7.5 7.5 0 0 1 2 .27c1.53-1.06 2.2-.84 2.2-.84.44 1.12.16 1.96.08 2.16.51.57.82 1.3.82 2.19 0 3.12-1.87 3.81-3.65 4.02.29.25.54.74.54 1.51 0 1.09-.01 1.97-.01 2.24 0 .21.15.47.55.39A8.15 8.15 0 0 0 16 8.13C16 3.64 12.42 0 8 0Z"></path>
                </svg>
            """,
            "class": "",
        }
    ],
    "navigation_with_keys": True,
}
