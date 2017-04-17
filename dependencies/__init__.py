"""
dependencies
~~~~~~~~~~~~

Dependency Injection for Humans.

:copyright: (c) 2016 by Artem Malyshev.
:license: LGPL-3, see LICENSE for more details.
"""

from .exceptions import DependencyError
from .injector import Injector
from .proxies import this

__all__ = ['Injector', 'this', 'DependencyError']

# TODO: write documentation for proxies module
#
# TODO: write documentation for new `use` decorator
