"""Tests related to the @value object."""
import pytest

from dependencies import Injector
from dependencies import value
from dependencies.exceptions import DependencyError
from helpers import CodeCollector


def test_define_value():
    """Evaluate @value decorated function during dependency injection process."""

    class Container(Injector):

        foo = 1
        bar = 2
        baz = 3

        @value
        def result(foo, bar, baz):
            return foo + bar + baz

    assert Container.result == 6


def test_keyword_arguments():
    """
    @value decorated function should support keyword arguments.

    If keyword argument is missing in the Injector subclass the
    default value should be used.
    """

    class Container(Injector):

        foo = 1
        bar = 2

        @value
        def result(foo, bar, baz=3):
            return foo + bar + baz

    assert Container.result == 6


def test_protect_against_classes():
    """Deny to apply @value to classes."""
    with pytest.raises(DependencyError) as exc_info:

        @value
        class Foo:
            pass  # pragma: no cover

    assert str(exc_info.value) == "'value' decorator can not be used on classes"


deny_method = CodeCollector()


@deny_method.parametrize
def test_protect_against_self(code):
    """Deny to define a value with argument called `self`."""

    class Foo:
        pass

    @value
    def method(self, foo, bar):
        pass  # pragma: no cover

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
