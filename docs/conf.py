# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
import os
import sys
from datetime import datetime
import tomlkit

sys.path.insert(0, os.path.abspath("."))


def _get_project_meta():
    with open("../pyproject.toml") as pyproject:
        file_contents = pyproject.read()

    return tomlkit.parse(file_contents)["tool"]["poetry"]  # type: ignore


def _make_copyright(name: str, start_year: int = 2020) -> str:
    end_year = datetime.now().year
    if start_year == end_year:
        return f"{start_year}, {name}"
    return f"{start_year}-{end_year}, {name}"


pkg_meta = _get_project_meta()

# -- Project information -----------------------------------------------------

project = str(pkg_meta["name"])
copyright = _make_copyright("Ivan Fedorov")
author = "Ivan Fedorov"

# The full version, including alpha/beta/rc tags
release = str(pkg_meta["version"])


# -- General configuration ---------------------------------------------------
needs_sphinx = "3.0"

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.doctest",
    "sphinx.ext.todo",
    "sphinx.ext.coverage",
    "sphinx.ext.viewcode",
    "sphinx.ext.autosummary",
    "sphinx.ext.napoleon",
    "sphinx_autodoc_typehints",
    "pallets_sphinx_themes",
]

# Set `typing.TYPE_CHECKING` to `True`:
# https://pypi.org/project/sphinx-autodoc-typehints/
set_type_checking_flag = False
always_document_param_types = False

# Add any paths that contain templates here, relative to this directory.
templates_path = ["_templates"]

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]


# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = "flask"
html_theme_options = {"index_sidebar_logo": False}


# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ["_static"]


html_sidebars = {
    "index": ["project.html", "localtoc.html", "searchbox.html", "ethicalads.html"],
    "librupost.*": ["relations.html", "searchbox.html", "ethicalads.html"],
    "librupost": ["relations.html", "searchbox.html", "ethicalads.html"],
    "**": ["localtoc.html", "relations.html", "searchbox.html", "ethicalads.html"],
}
singlehtml_sidebars = {"index": ["project.html", "localtoc.html", "ethicalads.html"]}
