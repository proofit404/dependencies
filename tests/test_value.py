import pytest

from dependencies import Injector
from dependencies import value
from dependencies.exceptions import DependencyError
from helpers import CodeCollector


def test_define_value():
    class Container(Injector):

        foo = 1
        bar = 2
        baz = 3

        @value
        def result(foo, bar, baz):
            return foo + bar + baz

    assert Container.result == 6


def test_keyword_arguments():
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
def sUIvAUUeQIde(arg):
    """Declarative injector."""

    class Container(Injector):
        method = arg


@deny_method
def nVlMKQghCDAQ(arg):
    """Let notation."""

    Injector.let(method=arg)


def test_protect_against_classes():

    with pytest.raises(DependencyError) as exc_info:

        @value
        class Foo(object):
            pass  # pragma: no cover

    assert str(exc_info.value) == "'value' decorator can not be used on classes"


deny_kwargs = CodeCollector()


@deny_kwargs.parametrize
def test_protect_against_args_kwargs(code):
    """Deny value definition with varied arguments and keywords. """

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
def pqwvsBqbIiXg(arg):
    """Declarative injector."""

    class Container(Injector):
        func = arg


@deny_kwargs
def jbfjlQveNjrZ(arg):
    """Let notation."""

    Injector.let(func=arg)


def test_docstrings():
    """Access `value` documentation string."""

    assert (
        value.__doc__ == "\n"
        "    Evaluate given function during dependency injection.\n"
        "\n"
        "    Returned value is used as value of the dependency.\n"
        "\n"
        "    Used as function decorator.\n"
        "    "
    )
