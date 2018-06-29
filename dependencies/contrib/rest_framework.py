"""
dependencies.contrib.rest_framework
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This module implements injectable Django Rest Framework API view.

:copyright: (c) 2018 by Artem Malyshev.
:license: BSD, see LICENSE for more details.
"""

from ._rest_framework import api_view, generic_api_view, model_view_set


__all__ = ["api_view", "generic_api_view", "model_view_set"]
