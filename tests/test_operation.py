"""Tests related to the @operation proxy."""
from dependencies import Injector
from dependencies import operation


def test_define_operation():
    """Create operation from the function definition."""

    class Container(Injector):

        foo = 1
        bar = 2
        baz = 3

        @operation
        def process(foo, bar, baz):
            return foo + bar + baz

    assert Container.process() == 6


def test_keyword_arguments():
    """Preserve keyword argument defaults in the operation constructor."""

    class Container(Injector):

        foo = 1
        bar = 2

        @operation
        def process(foo, bar, baz=3):
            return foo + bar + baz

    assert Container.process() == 6
