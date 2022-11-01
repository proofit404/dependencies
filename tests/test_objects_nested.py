"""Tests related to Injector classes written inside other Injector classes."""
import pytest

from dependencies import Injector
from dependencies.exceptions import DependencyError


def test_deny_classes_depend_on_nested_injectors():
    """Classes should not receive nested injectors as arguments of constructors."""

    class Foo:
        def __init__(self, bar):
            raise RuntimeError

    class Bar(Injector):
        baz = None

    class Container(Injector):
        foo = Foo
        bar = Bar

    with pytest.raises(DependencyError) as exc_info:
        Container.foo

    expected = """
Do not depend on nested injectors directly.

Use this object to access inner attributes of nested injector:

Container.foo
    """.strip()

    assert expected == str(exc_info.value)
