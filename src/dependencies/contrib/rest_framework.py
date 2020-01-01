"""
dependencies.contrib.rest_framework
-----------------------------------

This module implements injectable Django Rest Framework API view.

:copyright: (c) 2016-2020 by dry-python team.
:license: BSD, see LICENSE for more details.
"""
from _dependencies.contrib.rest_framework import api_view
from _dependencies.contrib.rest_framework import generic_api_view
from _dependencies.contrib.rest_framework import generic_view_set
from _dependencies.contrib.rest_framework import list_api_view
from _dependencies.contrib.rest_framework import model_view_set
from _dependencies.contrib.rest_framework import retrieve_api_view
from _dependencies.contrib.rest_framework import view_set


__all__ = [
    "api_view",
    "generic_api_view",
    "generic_view_set",
    "list_api_view",
    "model_view_set",
    "retrieve_api_view",
    "view_set",
]
