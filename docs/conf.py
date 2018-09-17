#!/usr/bin/env python3

project = "dependencies"

copyright = "2016-2018, Artem Malyshev"

author = "Artem Malyshev"

version = "0.15"

release = "0.15"

templates_path = ["templates"]

source_suffix = ".rst"

master_doc = "index"

language = None

exclude_patterns = ["_build"]

pygments_style = "sphinx"

html_theme = "alabaster"

html_static_path = ["static"]

html_sidebars = {
    "**": [
        "sidebarlogo.html",
        "stats.html",
        "globaltoc.html",
        "relations.html",
        "links.html",
        "searchbox.html",
    ]
}

html_theme_options = {
    "show_related": True,
    "description": "Dependency Injection for Humans.  It provides a simple low-impact implementation of an IoC container and resolution support for your classes.",
    "github_user": "dry-python",
    "github_repo": "dependencies",
    "github_type": "star",
    "github_count": True,
    "github_banner": True,
}
