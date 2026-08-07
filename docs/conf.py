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
html_theme = "pydata_sphinx_theme"
html_title = "genome-spy-python"
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
    "navbar_align": "left",
    "navbar_end": ["navbar-icon-links"],
    "show_prev_next": False,
    "icon_links": [
        {
            "name": "GitHub",
            "url": "https://github.com/genome-spy/genome-spy-python",
            "icon": "fa-brands fa-github",
        }
    ],
    "logo": {"text": "GenomeSpy for Python"},
}
html_context = {"default_mode": "light"}

# The landing page is a full-width showcase, so drop its sidebars.
html_sidebars = {"index": []}
