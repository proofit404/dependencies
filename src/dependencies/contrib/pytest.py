"""
dependencies.contrib.pytest
---------------------------

This module implements injectable Py.Test fixtures.

:copyright: (c) 2016-2019 by dry-python team.
:license: BSD, see LICENSE for more details.
"""

from ._pytest import register, require


__all__ = ["register", "require"]
