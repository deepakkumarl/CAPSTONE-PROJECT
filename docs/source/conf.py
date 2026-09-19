import os
import sys
from pathlib import Path

# Add project root and src directory to sys.path for autodoc
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent / "src"))

# Project information
project = "BMW Service Knowledge RAG"
copyright = "2026, BMW Service Engineering Team"
author = "BMW Service Engineering Team"
release = "1.0.0"

# General configuration
extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.autosummary",
    "sphinx.ext.napoleon",
    "sphinx.ext.viewcode",
    "myst_parser",
    "sphinx_copybutton",
]

# MyST Parser configuration
myst_enable_extensions = [
    "colon_fence",
    "deflist",
    "fieldlist",
    "html_admonition",
    "html_image",
]
myst_heading_anchors = 3
source_suffix = {
    ".rst": "restructuredtext",
    ".md": "markdown",
}

# Autodoc configuration & mocking for offline build
autodoc_mock_imports = [
    "ollama",
    "langchain_ollama",
    "langchain_huggingface",
    "langchain_community",
    "langchain_core",
    "sentence_transformers",
    "faiss",
    "torch",
    "pypdf",
    "docx",
    "pydantic",
    "pydantic_settings",
]
autodoc_default_options = {
    "members": True,
    "undoc-members": True,
    "show-inheritance": True,
}
autosummary_generate = True

templates_path = ["_templates"]
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]

# HTML output configuration
html_theme = "furo"
html_title = "BMW Service Knowledge RAG Documentation"
html_static_path = ["_static"]

# Restrained BMW-inspired theme styling
html_theme_options = {
    "sidebar_hide_name": False,
    "navigation_with_keys": True,
    "light_css_variables": {
        "color-brand-primary": "#1E3A8A",
        "color-brand-content": "#1E40AF",
    },
    "dark_css_variables": {
        "color-brand-primary": "#60A5FA",
        "color-brand-content": "#93C5FD",
    },
}
