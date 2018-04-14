"""
dependencies.contrib.django
~~~~~~~~~~~~~~~~~~~~~~~~~~~

This module implements injectable Django view.

:copyright: (c) 2016-2018 by Artem Malyshev.
:license: BSD, see LICENSE for more details.
"""

from ._django import create_view, view

__all__ = ["create_view", "view"]
