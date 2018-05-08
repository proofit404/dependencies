import pytest
from dependencies import Injector, operation
from dependencies.exceptions import DependencyError


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


def test_protect_against_self():
    """Deny to define an operation with argument called `self`."""

    with pytest.raises(DependencyError) as exc_info:

        @operation
        def method(self, foo, bar):
            pass

    assert str(exc_info.value) == "'operation' decorator can not be used on methods"


# TODO: Raise exception if we try to decorate a class.
#
# TODO: Operation representation with the name of the function.
#
# TODO: Support default keyword arguments.
