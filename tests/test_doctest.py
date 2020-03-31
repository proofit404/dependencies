# -*- coding: utf-8 -*-
from dependencies import Injector


class Container(Injector):
    """
    >>> Container.foo
    1
    """

    foo = 1
