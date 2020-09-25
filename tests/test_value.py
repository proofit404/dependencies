"""Tests related to the @value proxy."""
from dependencies import Injector
from dependencies import value


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
