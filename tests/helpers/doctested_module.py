# -*- coding: utf-8 -*-
from dependencies import Injector


class Foo(object):
    def __init__(self, v):
        self.v = v


class Container(Injector):
    v = 1
    foo = Foo


def container():
    """
    >>> container()
    1

    """
    return Container.foo.v
