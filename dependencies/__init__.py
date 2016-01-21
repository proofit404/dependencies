"""
    dependencies
    ~~~~~~~~~~~~

    Dependency Injection for Humans.

    :copyright: (c) 2016 by Artem Malyshev.
    :license: LGPL-3, see LICENSE for more details.
"""

import six

__all__ = ['Injectable', 'Injector', 'DependencyError']


class DependencyError(Exception):
    """Broken dependencies configuration error."""

    pass


protocol_violation = (
    'Classes inherited from Injectable can not redefine {0} method')


def init_base(self, **kwargs):
    self.kwargs = kwargs


def getattr_base(self, name):
    try:
        return self.kwargs[name]
    except KeyError:
        return getattr(super(), name)


class InjectableBase(type):

    def __new__(cls, name, bases, namespace):

        for method in ('__init__', '__getattr__', '__getattribute__'):
            if method in namespace:
                raise DependencyError(protocol_violation.format(method))

        new = super(InjectableBase, cls).__new__

        namespace['__init__'] = init_base
        namespace['__getattr__'] = getattr_base

        return new(cls, name, bases, namespace)


@six.add_metaclass(InjectableBase)
class Injectable(object):
    """Dependency Injection target.

    Classes inherited from this class may use constructor-based
    dependency injection.  Inherited classes can't override __init__
    and __getattr__ methods.

    """

    pass


class Injector(object):
    """Default dependencies specification DSL.

    Classes inherited from this class may specify default dependencies
    for one or more `Injectable` classes.  Constructor-based injection
    remains for the defined class.

    """

    pass
