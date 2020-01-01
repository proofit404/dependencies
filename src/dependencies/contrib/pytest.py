"""
dependencies.contrib.pytest
---------------------------

This module implements injectable Py.Test fixtures.

:copyright: (c) 2016-2020 by dry-python team.
:license: BSD, see LICENSE for more details.
"""
from _dependencies.contrib.pytest import register
from _dependencies.contrib.pytest import require


__all__ = ["register", "require"]
