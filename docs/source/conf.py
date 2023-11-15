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
sys.path.insert(0, os.path.abspath('../../src'))

master_doc = 'index'

# -- Project information -----------------------------------------------------

project = 'pyNAVIS'
copyright = '2018, Juan P. Dominguez-Morales'
author = 'Juan P. Dominguez-Morales'

# The full version, including alpha/beta/rc tags
release = '1.1.8'


# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [    'sphinx.ext.autodoc',
    'sphinx.ext.viewcode',
    'sphinxcontrib.napoleon', 'autodocsumm', 'recommonmark', 'sphinx-prompt']

#napoleon_use_param = False
napoleon_use_ivar = True
napoleon_use_admonition_for_notes = True
napoleon_use_rtype = False

autodoc_default_options = {
    'autosummary': True,
}



# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = []


# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = 'sphinx_rtd_theme'

html_theme_options = {
    "collapse_navigation" : False,
    "navigation_depth": -1
}

source_suffix = {
    '.rst': 'restructuredtext',
    '.txt': 'markdown',
    '.md': 'markdown',
}

html_logo = 'pyNAVIS_200.png'
html_favicon = 'pyNAVIS_favicon.png'
html_compact_lists = False
#pygments_style = 'sphinx'

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']
