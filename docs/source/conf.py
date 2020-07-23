# pylint: skip-file
# flake8: noqa
"""Configuration file for the Sphinx documentation builder.

This file only contains a selection of the most common options. For a
full list see the documentation:

https://www.sphinx-doc.org/en/master/usage/configuration.html

"""

import os


# -- Project information -----------------------------------------------

project = "Test Project"
copyright = "2020, Josh Huitema"
author = "Josh Huitema"

package_dir = os.path.abspath("../..")
src_dir = os.path.join(package_dir, "src")

# The full version, including alpha/beta/rc tags
with open(os.path.join(package_dir, "VERSION")) as _version_file:
    release = _version_file.read().strip()
# The semantic version, not including tags
version = release.split("-", 1)[0]


# -- General configuration ---------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.doctest",
    "sphinx.ext.inheritance_diagram",
    "sphinx.ext.napoleon",
    "sphinx_rtd_theme",
]

# Add any paths that contain templates here, relative to this directory.
templates_path = ["_templates"]

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files. This pattern also
# affects html_static_path and html_extra_path.
exclude_patterns = []


# -- Options for HTML output -------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation
# for a list of builtin themes.
html_theme = "sphinx_rtd_theme"

# Add any paths that contain custom static files (such as style sheets)
# here, relative to this directory. They are copied after the builtin
# static files, so a file named "default.css" will overwrite the builtin
# "default.css".
html_static_path = ["_static"]


# -- Extension configuration -------------------------------------------

# -- Options for intersphinx extension ---------------------------------

extensions.append("sphinx.ext.intersphinx")

# Example configuration for intersphinx: refer to the Python standard
# library.
intersphinx_mapping = {"https://docs.python.org/3/": None}

# -- Options for todo extension ----------------------------------------------

extensions.append("sphinx.ext.todo")

# If true, `todo` and `todoList` produce output, else they produce
# nothing.
todo_include_todos = True

# -- Options for autoapi extension -------------------------------------

extensions.append("autoapi.extension")

autoapi_dirs = [src_dir]
autoapi_add_toctree_entry = False
autoapi_python_class_content = "both"
autoapi_root = "reference/api"
autoapi_options = [
    "members",
    "special-members",
    "show-inheritance",
    "show-inheritance-diagram",
    "show-module-summary",
    "imported-members",
]
# autoapi_keep_files = True  # Uncomment to debug generated rst files
