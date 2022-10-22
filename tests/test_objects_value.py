"""Tests related to the @value object."""
from functools import lru_cache
from random import randint

import pytest

from dependencies import Injector
from dependencies import value
from dependencies.exceptions import DependencyError


def test_define_value(e, expect):
    """Evaluate @value decorated function during dependency injection process."""

    class Container(Injector):

        get = e.Take["func"]

        @value
        def func(foo, bar, baz):
            return foo + bar + baz

        foo = 1
        bar = 2
        baz = 3

    @expect(Container)
    def case(it):
        assert it.get == 6


def test_keyword_arguments(e, expect):
    """@value decorated function should support keyword arguments.

    If keyword argument is missing in the Injector subclass the
    default value should be used.

    """

    class Container(Injector):

        get = e.Take["func"]

        @value
        def func(foo, bar, baz=3):
            return foo + bar + baz

        foo = 1
        bar = 2

    @expect(Container)
    def case(it):
        assert it.get == 6


def test_protect_against_classes():
    """Deny to apply @value to classes."""
    with pytest.raises(DependencyError) as exc_info:

        @value
        class Foo:
            pass

    assert str(exc_info.value) == "'value' decorator can not be used on classes"


def test_protect_against_self(e, expect, catch):
    """Deny to define a value with argument called `self`."""

    class Container(Injector):
        @value
        def method(self, foo, bar):
            raise RuntimeError

    @expect(Container)
    @catch("'value' decorator can not be used on methods")
    def case(it):
        it.foo


def test_allow_decorated_functions(e, expect):
    """Decorators applied to functions should keep working."""

    class Container(Injector):
        foo = e.Take["singleton"]

        @value
        @lru_cache()  # noqa: B019
        def singleton():
            return randint(0, 1000)

    @expect(Container)
    def case(it):
        assert it.foo == it.foo
