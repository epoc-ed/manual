# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

from importlib import metadata

project = 'epoc'
copyright = '2024, Erik'
author = 'Erik'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.napoleon',
]

templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']
try:
    simple_tem_version = metadata.version('simple_tem')
except metadata.PackageNotFoundError:
    simple_tem_version = '0.0.0'
try:
    epoc_version = metadata.version('epoc')
except metadata.PackageNotFoundError:
    epoc_version = '0.0.0'

rst_prolog = f"""
.. |simple_tem_version| replace:: {simple_tem_version}
.. |epoc_version| replace:: {epoc_version}
"""

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'furo'
html_static_path = ['_static']
html_title = ""

# html_theme_options = {
#     # Disable showing the sidebar. Defaults to 'false'
#     'nosidebar': True,
# }

