"""
dependencies.proxies
~~~~~~~~~~~~~~~~~~~~

This module provides functions for lazy attribute and item access
during dependency injection process.

:copyright: (c) 2016-2018 by Artem Malyshev.
:license: BSD, see LICENSE for more details.
"""

import random
import string

from .exceptions import DependencyError


class Thisable(object):
    """Declare attribute and item access during dependency injection."""

    def __init__(self, parents):

        self.parents = parents

    def __getattr__(self, attrname):

        return proxy(self.parents, [attrname], {})

    def __lshift__(self, num):

        if not isinstance(num, int) or num <= 0:
            raise ValueError('Positive integer argument is required')
        return Thisable(num)


this = Thisable(0)


class ProxyType(type):

    def __getattr__(cls, attrname):

        parents = cls.__parents__
        expression = cls.__expression__ + ['.', attrname]
        scope = dict(**cls.__scope__)
        return proxy(parents, expression, scope)

    def __getitem__(cls, item):

        parents = cls.__parents__
        itemname = random_string()
        expression = cls.__expression__ + ['[', itemname, ']']
        scope = {itemname: item}
        scope.update(cls.__scope__)
        return proxy(parents, expression, scope)


def proxy(parents, expression, scope):

    __new__ = make_new(parents, expression, scope)
    __init__ = make_init(parents, expression)
    return ProxyType(
        'Proxy', (object,), {
            '__new__': __new__,
            '__init__': __init__,
            '__parents__': parents,
            '__expression__': expression,
            '__scope__': scope,
        })


def make_new(parents, expression, scope):

    def_expr = 'def __new__(cls, {argument}):'
    try_expr = '    try: __parent__ = __parent__.__parent__'
    except_expr = (
        "    except AttributeError: raise DependencyError('"
        "You tries to shift this more times that Injector has levels"
        "')")
    return_expr = '    return {result_expr}'
    argument = get_argument(parents, expression)
    if parents:
        expression = ['__parent__', '.'] + expression
    result_expr = ''.join(expression)
    template = '\n'.join([def_expr] + [try_expr, except_expr] *
                         (parents - 1) + [return_expr])
    code = template.format(argument=argument, result_expr=result_expr)
    scope = dict(DependencyError=DependencyError, **scope)
    exec(code, scope)
    __new__ = scope['__new__']
    return __new__


def make_init(parents, expression):

    argument = get_argument(parents, expression)
    template = 'def __init__(self, {argument}): pass'
    code = template.format(argument=argument)
    scope = {}
    exec(code, scope)
    __init__ = scope['__init__']
    return __init__


def get_argument(parents, expression):

    if parents:
        argument = '__parent__'
    else:
        argument = expression[0]
    return argument


def random_string():

    return ''.join(random.choice(string.ascii_letters) for i in range(8))
