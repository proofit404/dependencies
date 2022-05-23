"""Tests related to the @value object."""
from functools import lru_cache
from random import randint

import pytest

from dependencies import Injector
from dependencies import value
from dependencies.exceptions import DependencyError
from helpers import CodeCollector


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


deny_method = CodeCollector()


@deny_method.parametrize
def test_protect_against_self(code):
    """Deny to define a value with argument called `self`."""

    class Foo:
        pass

    @value
    def method(self, foo, bar):
        raise RuntimeError

    with pytest.raises(DependencyError) as exc_info:
        code(Foo, method)

    assert str(exc_info.value) == "'value' decorator can not be used on methods"


@deny_method
def _sUIvAUUeQIde(Foo, arg):
    class Container(Injector):
        foo = Foo
        method = arg

    Container.foo


@deny_method
def _nVlMKQghCDAQ(Foo, arg):
    Injector(foo=Foo, method=arg).foo


deny_direct_resolve = CodeCollector()


@deny_direct_resolve.parametrize
def test_direct_value_resolve(touch, code):
    """Attempt to resolve value directly should raise exception.

    Values are allowed to be used as dependencies for classes.

    """
    with pytest.raises(DependencyError) as exc_info:
        touch(code(), "a")
    expected = "'value' dependencies could only be used to instantiate classes"
    assert str(exc_info.value) == expected


@deny_direct_resolve
def _n3XOmcCoWc0W():
    class Container(Injector):
        @value
        def a():
            return 1

    return Container


@deny_direct_resolve
def _pZKCM0OCHMML():
    @value
    def a():
        return 1

    return Injector(a=a)


decorated_functions = CodeCollector()


@decorated_functions.parametrize
def test_allow_decorated_functions(touch, code):
    """Decorators applied to functions should keep working."""

    class Foo:
        def __init__(self, bar):
            self.bar = bar

    Container = code(Foo)
    assert touch(Container, "foo").bar == touch(Container, "foo").bar


@decorated_functions
def _z4nIvE3QRpik(Foo):
    class Container(Injector):
        foo = Foo

        @value
        @lru_cache()  # noqa: B019
        def bar():
            return randint(0, 1000)

    return Container


@decorated_functions
def _q6PYNbsibDGG(Foo):
    @value
    @lru_cache()
    def bar():
        return randint(0, 1000)

    return Injector(foo=Foo, bar=bar)
