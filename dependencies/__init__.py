"""
    dependencies
    ~~~~~~~~~~~~

    Dependency Injection for Humans.

    :copyright: (c) 2016 by Artem Malyshev.
    :license: LGPL-3, see LICENSE for more details.
"""

import six

__all__ = ['Injectable', 'Injector', 'DependencyError']


def injectable_init(self, **kwargs):
    self.dependencies = kwargs


def injectable_getattr(self, name):
    try:
        return self.dependencies[name]
    except KeyError:
        raise AttributeError(
            'You should inject {0!r} dependency into {1!r} '
            'constructor'.format(name, self.__class__.__name__))


class InjectableBase(type):

    def __new__(cls, name, bases, namespace):

        for method in ('__init__', '__getattr__', '__getattribute__'):
            if method in namespace:
                raise DependencyError(
                    'Classes inherited from Injectable can not redefine'
                    ' {0!r} method'.format(method))

        new = super(InjectableBase, cls).__new__

        # Ensure initialization is only performed for subclasses of
        # Injectable (excluded Injectable class itself).
        if len(bases) == 0:
            return new(cls, name, bases, namespace)

        if len(bases) > 1:
            raise DependencyError(
                'You can not use multiple inheritance together with Injectable'
            )

        namespace['__init__'] = injectable_init
        namespace['__getattr__'] = injectable_getattr

        return new(cls, name, bases, namespace)


class InjectorBase(InjectableBase):

    def __new__(cls, name, bases, namespace):

        # Skip Injectable.__new__ method.
        new = super(InjectableBase, cls).__new__

        # Ensure initialization is only performed for subclasses of
        # Injection (excluded Injector class itself).
        if len(bases) == 0:
            return new(cls, name, bases, namespace)

        if len(bases) == 1:
            raise DependencyError(
                'You can not inherit from Injector on its own.  '
                'Add some Injectable subclasses.')

        if any((not issubclass(x, (Injectable, Injector))
                for x in bases)):
            raise DependencyError('Injector require Injectable subclasses')

        def __init__(self, **kwargs):

            dependencies = {}
            dependencies.update(namespace)
            dependencies.update(kwargs)
            injectable_init(self, **dependencies)

        ns = {'__init__': __init__}  # TODO: keep __module__ and __qualname__
        return new(cls, name, bases, ns)


class Injectable(six.with_metaclass(InjectableBase)):
    """Dependency Injection target.

    Classes inherited from this class may use constructor-based
    dependency injection.  Inherited classes can't override __init__
    and __getattr__ methods.

    """

    pass


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
