import pytest

from dependencies import Injector
from dependencies import operation
from dependencies.exceptions import DependencyError
from helpers import CodeCollector


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


deny_method = CodeCollector()


@deny_method.parametrize
def test_protect_against_self(code):
    """Deny to define an operation with argument called `self`."""

    @operation
    def method(self, foo, bar):
        pass  # pragma: no cover

    with pytest.raises(DependencyError) as exc_info:
        code(method)

    assert str(exc_info.value) == "'operation' decorator can not be used on methods"


@deny_method
def lSxEXspkuups(arg):
    """Declarative injector."""

    class Container(Injector):
        method = arg


@deny_method
def qZcxoLXYnvke(arg):
    """Let notation."""

    Injector.let(method=arg)


def test_protect_against_classes():
    """
    Deny to decorate classes with operation.

    Classes are injectable itself.
    """
    with pytest.raises(DependencyError) as exc_info:

        @operation
        class Foo(object):
            pass

    assert str(exc_info.value) == "'operation' decorator can not be used on classes"


deny_kwargs = CodeCollector()


@deny_kwargs.parametrize
def test_protect_against_args_kwargs(code):
    """Deny operation definition with varied arguments and keywords. """

    @operation
    def func1(*args):
        pass  # pragma: no cover

    with pytest.raises(DependencyError) as exc_info:
        code(func1)

    assert str(exc_info.value) == "func1 have arbitrary argument list"

    @operation
    def func2(**kwargs):
        pass  # pragma: no cover

    with pytest.raises(DependencyError) as exc_info:
        code(func2)

    assert str(exc_info.value) == "func2 have arbitrary keyword arguments"

    @operation
    def func3(*args, **kwargs):
        pass  # pragma: no cover

    with pytest.raises(DependencyError) as exc_info:
        code(func3)

    assert (
        str(exc_info.value)
        == "func3 have arbitrary argument list and keyword arguments"
    )


@deny_kwargs
def puELUDZLxkDG(arg):
    """Declarative injector."""

    class Container(Injector):
        func = arg


@deny_kwargs
def iQXjlPlQGgSh(arg):
    """Let notation."""

    Injector.let(func=arg)
