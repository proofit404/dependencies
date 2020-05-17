# -*- coding: utf-8 -*-
"""Tests related to the @value proxy."""
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


deny_method = CodeCollector()


@deny_method.parametrize
def test_protect_against_self(code):
    """Deny to define a value with argument called `self`."""

    @value
    def method(self, foo, bar):
        pass  # pragma: no cover

    with pytest.raises(DependencyError) as exc_info:
        code(method)

    assert str(exc_info.value) == "'value' decorator can not be used on methods"


@deny_method
def _sUIvAUUeQIde(arg):
    # Declarative injector.

    class Container(Injector):
        method = arg


@deny_method
def _nVlMKQghCDAQ(arg):
    # Let notation.
    Injector.let(method=arg)


def test_protect_against_classes():
    """Deny to decorate classes with @value proxy."""
    with pytest.raises(DependencyError) as exc_info:

        @value
        class Foo(object):
            pass  # pragma: no cover

    assert str(exc_info.value) == "'value' decorator can not be used on classes"


deny_kwargs = CodeCollector()


@deny_kwargs.parametrize
def test_protect_against_args_kwargs(code):
    """Deny value definition with varied arguments and keywords."""

    @value
    def func1(*args):
        pass  # pragma: no cover

    with pytest.raises(DependencyError) as exc_info:
        code(func1)

    assert str(exc_info.value) == "func1 have arbitrary argument list"

    @value
    def func2(**kwargs):
        pass  # pragma: no cover

    with pytest.raises(DependencyError) as exc_info:
        code(func2)

    assert str(exc_info.value) == "func2 have arbitrary keyword arguments"

    @value
    def func3(*args, **kwargs):
        pass  # pragma: no cover

    with pytest.raises(DependencyError) as exc_info:
        code(func3)

    assert (
        str(exc_info.value)
        == "func3 have arbitrary argument list and keyword arguments"
    )


@deny_kwargs
def _pqwvsBqbIiXg(arg):
    # Declarative injector.

    class Container(Injector):
        func = arg


@deny_kwargs
def _jbfjlQveNjrZ(arg):
    # Let notation.
    Injector.let(func=arg)
