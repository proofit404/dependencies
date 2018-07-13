#!/usr/bin/env python3

templates_path = ["templates"]

source_suffix = ".rst"

master_doc = "index"

project = "dependencies"

copyright = "2016-2018, Artem Malyshev"

author = "Artem Malyshev"

version = "0.14"

release = "0.14"

language = None

exclude_patterns = ["_build"]

pygments_style = "sphinx"

todo_include_todos = False

html_theme = "alabaster"

html_sidebars = {
    "**": [
        "sidebarlogo.html",
        "globaltoc.html",
        "relations.html",
        "links.html",
        "searchbox.html",
    ]
}

html_theme_options = {
    "show_related": True,
    "github_user": "dry-python",
    "github_repo": "dependencies",
    "github_banner": True,
}
