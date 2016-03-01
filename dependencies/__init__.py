"""
    dependencies
    ~~~~~~~~~~~~

    Dependency Injection for Humans.

    :copyright: (c) 2016 by Artem Malyshev.
    :license: LGPL-3, see LICENSE for more details.
"""

import functools
import inspect

import six

__all__ = ['Injector', 'DependencyError']


class InjectorBase(type):

    def __new__(cls, name, bases, namespace):

        new = super(InjectorBase, cls).__new__

        if len(bases) == 0:
            return new(cls, name, bases, namespace)

        if len(bases) > 1:
            raise DependencyError(
                'Multiple inheritance is not allowed')

        ns = {}

        for attr in ('__module__', '__doc__', '__weakref__', '__qualname__'):
            try:
                ns[attr] = namespace.pop(attr)
            except KeyError:
                pass

        if any((x for x in namespace
                if x.startswith('__') and x.endswith('__'))):
            raise DependencyError('Magic methods are not allowed')

        def __getattr__(self, attrname):
            """Injector attribute lookup."""

            try:
                attribute = namespace[attrname]
            except KeyError:
                raise AttributeError(
                    '{0!r} object has no attribute {1!r}'
                    .format(name, attrname))

            if inspect.isfunction(attribute):
                @functools.wraps(attribute)
                def method_wrapper(self, *args, **kwargs):
                    return v(*args, **kwargs)
                return method_wrapper
            else:
                return attribute

        ns['__getattr__'] = __getattr__

        klass = new(cls, name, bases, ns)
        return klass()


class Injector(six.with_metaclass(InjectorBase)):
    """Default dependencies specification DSL.

    Classes inherited from this class may inject dependencies into
    classes specified in it namespace.

    """

    pass


class DependencyError(Exception):
    """Broken dependencies configuration error."""

    pass
