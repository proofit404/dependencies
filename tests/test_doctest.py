# -*- coding: utf-8 -*-
"""Tests related to compatibility with standard doctest python module."""
from dependencies import Injector


class Container(Injector):
    """The code written in this docstring will be executed by pytest.

    >>> Container.foo
    1

    """

    foo = 1
