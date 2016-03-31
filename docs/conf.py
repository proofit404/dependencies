#!/usr/bin/env python3

extensions = []

templates_path = ['_templates']

source_suffix = '.rst'

master_doc = 'index'

project = 'dependencies'
copyright = '2016, Artem Malyshev'
author = 'Artem Malyshev'

version = '0.6'
release = '0.6'

language = None

exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

pygments_style = 'sphinx'

todo_include_todos = False

html_theme = 'alabaster'

html_static_path = ['_static']

htmlhelp_basename = 'dependenciesdoc'

latex_elements = {}

latex_documents = [
    (master_doc, 'dependencies.tex', 'dependencies Documentation', 'Artem Malyshev', 'manual'),
]

man_pages = [
    (master_doc, 'dependencies', 'dependencies Documentation', [author], 1)
]

texinfo_documents = [
    (master_doc, 'dependencies', 'dependencies Documentation', author, 'dependencies', 'One line description of project.', 'Miscellaneous'),
]
