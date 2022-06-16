"""Tests related to the @value object."""
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


def test_protect_against_self(define, let, has, expect):
    """Deny to define a value with argument called `self`."""
    foo = define.cls("Foo")
    method = let.fun("method", "self, foo, bar", "raise RuntimeError").dec("value")
    it = has(foo=foo, method=method)
    message = "'value' decorator can not be used on methods"
    expect(it).to_raise(message).when("obj.foo")


def test_allow_decorated_functions(define, let, has, expect):
    """Decorators applied to functions should keep working."""
    define.require("functools", "lru_cache")
    define.require("random", "randint")
    foo = define.cls("Foo", let.fun("__init__", "self, bar", "self.bar = bar"))
    it = has(
        foo=foo,
        bar=let.fun("bar", "", "return randint(0, 1000)").dec("value", "lru_cache()"),
    )
    expect(it).to("obj.foo.bar == obj.foo.bar")
