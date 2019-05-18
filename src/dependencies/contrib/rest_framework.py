"""
dependencies.contrib.rest_framework
-----------------------------------

This module implements injectable Django Rest Framework API view.

:copyright: (c) 2016-2019 by dry-python team.
:license: BSD, see LICENSE for more details.
"""

from ._rest_framework import (
    api_view,
    generic_api_view,
    list_api_view,
    model_view_set,
    retrieve_api_view,
)


__all__ = [
    "api_view",
    "generic_api_view",
    "list_api_view",
    "model_view_set",
    "retrieve_api_view",
]
