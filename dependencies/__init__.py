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
#
# TODO: support parent modification
#
# For example, we create injector subclass which holds `foo = 1`.
# Then we create another subclass of this container which holds `bar =
# Bar`.  `Bar` class itself depends on `foo`.  Then we modify first
# container with assignment (now `foo = 2`).  Then we try to resolve
# `bar` from second container.  Created instance must hold the new
# value of `foo`.
