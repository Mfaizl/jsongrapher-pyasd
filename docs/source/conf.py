import os
import sys

# Add the parent directory to sys.path so Sphinx can find the source code
sys.path.insert(0, os.path.abspath('../../'))

# Project information
project = 'JsonGrapher'
copyright = '2025, JsonGrapher'
author = 'JsonGrapher'
release = '0.1'

# Extensions to enable
extensions = [
    "sphinx.ext.napoleon",
    "sphinx.ext.autodoc",
    "sphinx_js",
]

js_source_path = [
    "../js_src/src/fileUtils.js",
    "../js_src/src/index.js",
    "../js_src/src/plottingUtils.js",
]

root_for_relative_js_paths = "../js_src/src"

# HTML theme to use
html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']
