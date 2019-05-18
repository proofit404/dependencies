"""
dependencies
------------

Dependency Injection for Humans.

:copyright: (c) 2016-2019 by dry-python team.
:license: BSD, see LICENSE for more details.
"""

from ._injector import Injector
from ._operation import Operation as operation
from ._package import Package
from ._this import this
from ._value import Value as value


__all__ = ["Injector", "operation", "Package", "this", "value"]
