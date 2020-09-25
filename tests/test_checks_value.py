"""Tests related to the `value` decorator checks."""
import pytest

from dependencies import Injector
from dependencies import value
from dependencies.exceptions import DependencyError
from helpers import CodeCollector


def test_protect_against_classes():
    """Deny to decorate classes with @value proxy."""
    with pytest.raises(DependencyError) as exc_info:

        @value
        class Foo:
            pass  # pragma: no cover

    assert str(exc_info.value) == "'value' decorator can not be used on classes"


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
    class Container(Injector):
        method = arg


@deny_method
def _nVlMKQghCDAQ(arg):
    Injector(method=arg)
