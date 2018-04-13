"""
dependencies
~~~~~~~~~~~~

Dependency Injection for Humans.

:copyright: (c) 2016-2018 by Artem Malyshev.
:license: BSD, see LICENSE for more details.
"""

from .exceptions import DependencyError
from .injector import Injector
from .proxies import this

__all__ = ['Injector', 'this', 'DependencyError']
