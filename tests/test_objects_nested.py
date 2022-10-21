"""Tests related to Injector classes written inside other Injector classes."""
import pytest

from dependencies import Injector
from dependencies import this
from dependencies.exceptions import DependencyError


def test_one_subcontainer_multiple_parents():
    """Same sub container can be used in many parent containers.

    This usage should not overlap those containers. And more importantly, sub container
    should not be modified after usage.

    """

    class Root:
        def __init__(self, result):
            self.result = result

    class Baz:
        def __init__(self, bar):
            raise RuntimeError

    class Nested(Injector):
        bar = (this << 1).foo
        baz = Baz

    class Container1(Injector):
        root = Root
        result = this.sub.bar
        sub = Nested
        foo = 1

    class Container2(Injector):
        root = Root
        result = this.sub.bar
        sub = Nested
        foo = 2

    assert Container1.root.result == 1
    assert Container2.root.result == 2

    with pytest.raises(DependencyError) as exc_info:
        Nested.baz

    expected = """
You tried to shift this more times than Injector has levels:

Nested.baz
  Nested.bar
    """.strip()

    assert str(exc_info.value) == expected


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
