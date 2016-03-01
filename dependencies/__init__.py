"""
    dependencies
    ~~~~~~~~~~~~

    Dependency Injection for Humans.

    :copyright: (c) 2016 by Artem Malyshev.
    :license: LGPL-3, see LICENSE for more details.
"""

import six

__all__ = ['Injector', 'DependencyError']


class InjectorBase(type):

    def __new__(cls, name, bases, namespace):

        new = super(InjectorBase, cls).__new__

        if len(bases) == 0:
            return new(cls, name, bases, namespace)

        if Injector in bases and len(bases) == 1:
            raise DependencyError(
                'You can not inherit from Injector on its own.  '
                'Add some Injectable subclasses.')

        ns = {}
        for attr in ('__module__', '__doc__', '__weakref__', '__qualname__'):
            try:
                ns[attr] = namespace.pop(attr)
            except KeyError:
                pass

        if any((x for x in namespace
                if x.startswith('__') and x.endswith('__'))):
            raise DependencyError('Magic methods not allowed')

        def __init__(self, **kwargs):
            dependencies = {}
            dependencies.update(namespace)
            dependencies.update(kwargs)
            super(self.__class__, self).__init__(**dependencies)

        ns['__init__'] = __init__

        return new(cls, name, bases, ns)


class Injector(six.with_metaclass(InjectorBase)):
    """Default dependencies specification DSL.

    Classes inherited from this class may specify default dependencies
    for one or more `Injectable` classes.  Constructor-based injection
    remains for the defined class.

    """

    pass


class DependencyError(Exception):
    """Broken dependencies configuration error."""

    pass
