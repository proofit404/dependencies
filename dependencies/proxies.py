"""
dependencies.proxies
~~~~~~~~~~~~~~~~~~~~

This module provides functions for lazy attribute and item access
during dependency injection process.

:copyright: (c) 2016 by Artem Malyshev.
:license: LGPL-3, see LICENSE for more details.
"""

import random
import string


class Thisable(object):
    """Declare attribute and item access during dependency injection."""

    def __init__(self, parents):

        self.parents = parents

    def __getattr__(self, attrname):

        expression = ['__parent__', '.'] * self.parents + [attrname]
        scope = {}
        return proxy(expression, scope)

    def __lshift__(self, num):

        if not isinstance(num, int) or num <= 0:
            raise ValueError('Positive integer argument is required')
        return Thisable(num)


this = Thisable(0)


class ProxyType(type):

    def __getattr__(cls, attrname):

        expression = cls.__expression__ + ['.', attrname]
        scope = dict(**cls.__scope__)
        return proxy(expression, scope)

    def __getitem__(cls, item):

        itemname = random_string()
        expression = cls.__expression__ + ['[', itemname, ']']
        scope = {itemname: item}
        scope.update(cls.__scope__)
        return proxy(expression, scope)


def proxy(expression, scope):

    __new__ = make_new(expression, scope)
    __init__ = make_init(expression)
    return ProxyType('Proxy', (object,), {
        '__new__': __new__,
        '__init__': __init__,
        '__expression__': expression,
        '__scope__': scope,
    })


def make_new(expression, scope):

    argument = expression[0]
    return_expr = ''.join(expression)
    template = 'def __new__(cls, {argument}): return {return_expr}'
    code = template.format(argument=argument, return_expr=return_expr)
    scope = dict(**scope)
    exec(code, scope)
    __new__ = scope['__new__']
    return __new__


def make_init(expression):

    argument = expression[0]
    template = 'def __init__(self, {argument}): pass'
    code = template.format(argument=argument)
    scope = {}
    exec(code, scope)
    __init__ = scope['__init__']
    return __init__


def random_string():

    return ''.join(random.choice(string.ascii_letters) for i in range(8))
