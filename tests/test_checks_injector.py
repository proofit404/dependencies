"""Tests related to the Injector subclasses checks."""
import pytest

from dependencies import Injector
from dependencies.exceptions import DependencyError
from helpers import CodeCollector


subclasses_only = CodeCollector()


@subclasses_only.parametrize
def test_multiple_inheritance_deny_regular_classes(code):
    """Only `Injector` subclasses are allowed to be used in the inheritance."""

    class Foo:
        pass

    with pytest.raises(DependencyError) as exc_info:
        code(Foo)

    message = str(exc_info.value)
    assert message == "Multiple inheritance is allowed for Injector subclasses only"


@subclasses_only
def _f1583394f1a6(Foo):
    class Bar(Injector, Foo):
        pass


@subclasses_only
def _b51814725d07(Foo):
    Injector & Foo


deny_magic_methods = CodeCollector()


@deny_magic_methods.parametrize
def test_deny_magic_methods_injection(code):
    """`Injector` doesn't accept magic methods."""
    with pytest.raises(DependencyError) as exc_info:
        code()

    assert str(exc_info.value) == "Magic methods are not allowed"


@deny_magic_methods
def _e78bf771747c():
    class Bar(Injector):
        def __eq__(self, other):
            pass  # pragma: no cover


@deny_magic_methods
def _e34b88041f64():
    class Foo(Injector):
        pass

    def eq(self, other):
        pass  # pragma: no cover

    Foo(__eq__=eq)
