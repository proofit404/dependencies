"""Tests related to the `operations` decorator checks."""
import pytest

from dependencies import Injector
from dependencies import operation
from dependencies.exceptions import DependencyError
from helpers import CodeCollector


def test_protect_against_classes():
    """Deny to decorate classes with operation.

    Classes are injectable itself.

    """
    with pytest.raises(DependencyError) as exc_info:

        @operation
        class Foo:
            pass

    assert str(exc_info.value) == "'operation' decorator can not be used on classes"


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
def _lSxEXspkuups(arg):
    class Container(Injector):
        method = arg


@deny_method
def _qZcxoLXYnvke(arg):
    Injector(method=arg)
