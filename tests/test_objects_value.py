"""Tests related to the @value object."""
from functools import lru_cache
from random import randint

import pytest

from dependencies import Injector
from dependencies import value
from dependencies.exceptions import DependencyError


def test_define_value():
    """Evaluate @value decorated function during dependency injection process."""

    class Get:
        def __init__(self, result):
            self.result = result

    class Container(Injector):

        get = Get
        foo = 1
        bar = 2
        baz = 3

        @value
        def result(foo, bar, baz):
            return foo + bar + baz

    assert Container.get.result == 6


def test_keyword_arguments():
    """@value decorated function should support keyword arguments.

    If keyword argument is missing in the Injector subclass the
    default value should be used.

    """

    class Get:
        def __init__(self, result):
            self.result = result

    class Container(Injector):

        get = Get
        foo = 1
        bar = 2

        @value
        def result(foo, bar, baz=3):
            return foo + bar + baz

    assert Container.get.result == 6


def test_protect_against_classes():
    """Deny to apply @value to classes."""
    with pytest.raises(DependencyError) as exc_info:

        @value
        class Foo:
            pass

    assert str(exc_info.value) == "'value' decorator can not be used on classes"


def test_protect_against_self():
    """Deny to define a value with argument called `self`."""

    class Foo:
        pass

    class Container(Injector):
        foo = Foo

        @value
        def method(self, foo, bar):
            raise RuntimeError

    with pytest.raises(DependencyError) as exc_info:
        Container.foo

    assert str(exc_info.value) == "'value' decorator can not be used on methods"


def test_allow_decorated_functions(expect):
    """Decorators applied to functions should keep working."""

    class Foo:
        def __init__(self, bar):
            self.bar = bar

    class Container(Injector):
        foo = Foo

        @value
        @lru_cache()  # noqa: B019
        def bar():
            return randint(0, 1000)

    @expect(Container)
    def to_be(it):
        assert it.foo.bar == it.foo.bar
