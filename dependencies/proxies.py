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

    def __getattr__(self, attrname):

        return proxy((attrname,), ())

    def __lshift__(self, num):

        attrs = tuple(['__parent__' for i in range(num)])
        return proxy(attrs, ())


this = Thisable()


class ProxyType(type):

    def __getattr__(cls, attrname):

        attrs = cls.__attrs__ + (attrname,)
        return proxy(attrs, ())

    def __getitem__(cls, item):

        items = cls.__items__ + (item,)
        return proxy(cls.__attrs__, items)


def proxy(attrs, items):

    __new__ = injection_hook(attrs, items)
    __init__ = make_init(attrs)
    return ProxyType('Proxy', (object,), {
        '__new__': __new__,
        '__init__': __init__,
        '__attrs__': attrs,
        '__items__': items,
    })


def injection_hook(attrs, items):

    argument = attrs[0]
    attrs_expr = '.'.join(attrs)
    item_names = [random_string() for each in items]
    items_expr = ''.join('[' + name + ']' for name in item_names)
    return_expr = attrs_expr + items_expr
    scope = dict([(k, v) for k, v in zip(item_names, items)])
    getter = make_new(argument, return_expr, scope)
    return getter


def make_new(argument, return_expr, scope):

    template = 'def __new__(cls, {argument}): return {return_expr}'
    code = template.format(argument=argument, return_expr=return_expr)
    exec(code, scope)
    __new__ = scope['__new__']
    return __new__


def make_init(arguments):

    argument = arguments[0]
    template = 'def __init__(self, {argument}): pass'
    code = template.format(argument=argument)
    scope = {}
    exec(code, scope)
    __init__ = scope['__init__']
    return __init__


def random_string():

    return ''.join(random.choice(string.ascii_letters) for i in range(8))
