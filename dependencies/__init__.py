"""
    dependencies
    ~~~~~~~~~~~~

    Dependency Injection for Humans.

    :copyright: (c) 2016 by Artem Malyshev.
    :license: LGPL-3, see LICENSE for more details.
"""

import six

__all__ = ['Injectable', 'Injector']


class InjectableBase(type):

    def __new__(cls, name, bases, namespace):

        new = super(InjectableBase, cls).__new__

        def __init__(self, **kwargs):
            self.kwargs = kwargs

        def __getattr__(self, name):
            try:
                return self.kwargs[name]
            except KeyError:
                return getattr(super(), name)

        namespace['__init__'] = __init__
        namespace['__getattr__'] = __getattr__

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
