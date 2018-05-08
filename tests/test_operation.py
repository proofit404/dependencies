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


def test_protect_against_classes():
    """
    Deny to decorate classes with operation.  Classes are injectable
    itself.
    """

    with pytest.raises(DependencyError) as exc_info:

        @operation
        class Foo(object):
            pass

    assert str(exc_info.value) == "'operation' decorator can not be used on classes"


def test_representation():
    """
    Operation class and instance should contain a name of the function
    in it.
    """

    @operation
    def process(foo, bar):
        pass

    assert repr(process) == "<class Operation[process]>"
    assert repr(process(1, "test")) == "<Operation[process] object>"


def test_docstrings():
    """Access `operation` documentation string."""

    assert (
        operation.__doc__ == "\n"
        "    Create callable class appropriated for dependency injection.\n"
        "\n"
        "    Used as function decorator.\n"
        "    "
    )
