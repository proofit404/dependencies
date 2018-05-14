"""
dependencies
~~~~~~~~~~~~

Dependency Injection for Humans.

:copyright: (c) 2016-2018 by Artem Malyshev.
:license: BSD, see LICENSE for more details.
"""

from ._injector import Injector
from ._operation import operation
from ._package import Package
from ._this import this

__all__ = ["Injector", "operation", "Package", "this"]
