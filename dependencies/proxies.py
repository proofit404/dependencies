"""
dependencies.proxies
~~~~~~~~~~~~~~~~~~~~

This module provides functions for lazy attribute and item access
during dependency injection process.

:copyright: (c) 2016 by Artem Malyshev.
:license: LGPL-3, see LICENSE for more details.
"""


# TODO: check order of ".." argument


import ast

from .exceptions import DependencyError


def attribute(*attrs):
    """Declare attribute access during dependency injection."""

    check_empty('attrs', attrs)
    attrs = ['__parent__' if attr == '..' else attr for attr in attrs]
    check_attributes(attrs)
    __new__ = attrgetter(attrs)
    __init__ = make_init(attrs)
    return type('Attribute', (object,), {
        '__new__': __new__,
        '__init__': __init__,
    })


def item(*items):
    """Declare item access during dependency injection."""

    check_empty('items', items)
    items = ['__parent__' if item == '..' else item for item in items]
    __new__ = itemgetter(items)
    __init__ = make_init(items)
    return type('Item', (object,), {
        '__new__': __new__,
        '__init__': __init__,
    })


def attrgetter(attrs):

    argument = attrs[0]
    return_expr = '.'.join(attrs)
    getter = make_new(argument, return_expr)
    return getter


def itemgetter(items):

    argument = items[0]
    attrs, items = split(items)
    check_attributes(attrs)
    # TODO: use AST Transform here or try to avoid name substitution
    # at all.
    return_expr = '.'.join(attrs) + ''.join('[' + ('"' + item.replace('"', '\\"') + '"' if isinstance(item, str) else str(item)) + ']' for item in items)
    # TODO: test against object with meaningless `str` result.
    check_empty('items', items)
    getter = make_new(argument, return_expr)
    return getter


def make_new(argument, return_expr):

    template = 'def __new__(cls, {argument}): return {return_expr}'
    code = template.format(argument=argument, return_expr=return_expr)
    scope = {}
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


def split(seq):

    istail, head, tail = False, [], []
    for item in seq:
        if istail:
            tail.append(item)
        elif item == '__parent__':
            head.append(item)
        else:
            head.append(item)
            istail = True
    return head, tail


def check_empty(argname, arg):

    if not arg:
        raise DependencyError(
            '{argname!r} argument can not be empty'
            .format(argname=argname)
        )


def check_attributes(names):

    for name in names:
        if not isinstance(name, str):
            raise TypeError('attribute name should be a string')
        try:
            ast.parse('{identifier} = None'.format(identifier=name))
        except (SyntaxError, TypeError, ValueError):
            raise DependencyError(
                '{name!r} is invalid attribute name'.format(name=name)
            )
