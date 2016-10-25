"""
dependencies
~~~~~~~~~~~~

Dependency Injection for Humans.

:copyright: (c) 2016 by Artem Malyshev.
:license: LGPL-3, see LICENSE for more details.
"""

from .injector import Injector
from .proxies import attribute, item
from .exceptions import DependencyError

__all__ = ['Injector', 'attribute', 'item', 'DependencyError']

# TODO: allow to use `use` decorator without explicit attributes
#
# TODO: write documentation for proxies module
#
# TODO: write documentation for new `use` decorator
