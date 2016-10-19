"""
dependencies.proxies
~~~~~~~~~~~~~~~~~~~~

This module provides functions for lazy attribute and item access
during dependency injection process.

:copyright: (c) 2016 by Artem Malyshev.
:license: LGPL-3, see LICENSE for more details.
"""

from .exceptions import DependencyError


def attribute(*attrs):
    """TODO: write *and* test doc."""

    check_empty('attrs', attrs)
    attrs = ['__parent__' if attr == '..' else attr for attr in attrs]
    __init__ = make_init(attrs)
    __new__ = attrgetter(attrs)
    return type('Attribute', (object,), {
        '__init__': __init__,
        '__new__': __new__,
    })


def item(*items):
    """TODO: write *and* test doc."""

    check_empty('items', items)
    items = ['__parent__' if item == '..' else item for item in items]
    __init__ = make_init(items)
    __new__ = itemgetter(items)
    return type('Item', (object,), {
        '__init__': __init__,
        '__new__': __new__,
    })


def attrgetter(attrs):

    argument = attrs[0]
    return_expr = '.'.join(attrs)
    getter = make_new(argument, return_expr)
    return getter


def itemgetter(items):

    argument = items[0]
    head, tail = split(items)
    # TODO: sanitize check
    return_expr = '.'.join(head) + ''.join('["' + arg + '"]' for arg in tail)
    check_empty('items', tail)
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
    while seq:
        item = seq.pop(0)
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
            "'{argname}' argument can not be empty"
            .format(argname=argname)
        )
