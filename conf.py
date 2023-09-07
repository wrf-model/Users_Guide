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
# import os
# import sys; sys.setrecursionlimit(1500)
# sys.path.insert(0, os.path.abspath('.'))

# -- Project information -----------------------------------------------------

project = 'WRF Users Guide'
copyright = '2021, Kelly Werner'
author = 'Kelly Werner'


# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = ['sphinx_tabs.tabs','sphinxcontrib.exceltable','sphinx_toolbox.collapse']

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
html_theme = 'agogo'

html_theme_options = {
    "headerbg":"darkslategray",
    "headerlinkcolor": "turquoise", 
    "headercolor2": "#96bd2b", 
    "linkcolor": "royalblue",
    "textalign":"right",
    "rightsidebar":"false",
}

html_js_files = {
        '_js/custom.js',
        '_js/sidebar.js'
        }

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']

html_logo = "wrf_logo.png"

html_css_files = [
    'custom.css'
]

rst_epilog = """ 
.. |br| raw:: html

         <br>

"""

#def setup(app):

# latex elements
latex_elements = {
    'papersize': 'a4paper',
    'pointsize': '12pt',
    'preamble': r'''
    \usepackage[none]{hyphenat}
    \usepackage[document]{ragged2e}
    '''
}

