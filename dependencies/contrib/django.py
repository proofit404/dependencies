"""
dependencies.contrib.django
~~~~~~~~~~~~~~~~~~~~~~~~~~~

This module implements injectable Django view.

:copyright: (c) 2016-2018 by Artem Malyshev.
:license: BSD, see LICENSE for more details.
"""

from ._django import form_view, view

__all__ = ["form_view", "view"]
