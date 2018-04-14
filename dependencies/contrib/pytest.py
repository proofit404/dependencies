"""
dependencies.contrib.pytest
~~~~~~~~~~~~~~~~~~~~~~~~~~~

This module implements injectable Py.test fixtures.

:copyright: (c) 2016-2018 by Artem Malyshev.
:license: BSD, see LICENSE for more details.
"""

from ._pytest import register, require

__all__ = ["register", "require"]
