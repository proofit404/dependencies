"""
    dependencies
    ~~~~~~~~~~~~

    Dependency Injection for Humans.

    :copyright: (c) 2015 by Artem Malyshev.
    :license: LGPL-3, see LICENSE for more details.
"""

__all__ = ['Injectable', 'Injector']


class Injectable:
    """Dependency Injection target.

    Classes inherited from this class may use constructor-based
    dependency injection.  Inherited classes can't override __init__
    and __getattr__ methods.

    """

    pass


class Injector:
    """Default dependencies specification DSL.

    Classes inherited from this class may specify default dependencies
    for one or more `Injectable` classes.  Constructor-based injection
    remains for the defined class.

    """

    pass
