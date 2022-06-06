"""Tests related to Injector classes written inside other Injector classes."""
import pytest

from collector import CodeCollector
from dependencies import Injector
from dependencies import this
from dependencies.exceptions import DependencyError


multiple_places = CodeCollector()
nested_variant = CodeCollector("stack_representation", "sub")


@multiple_places.parametrize
@nested_variant.parametrize
def test_one_subcontainer_multiple_parents(code, sub, stack_representation):
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

    Nested = sub(Baz)
    Container1 = code(Root, 1, Nested)
    Container2 = code(Root, 2, Nested)

    assert Container1.root.result == 1
    assert Container2.root.result == 2

    with pytest.raises(DependencyError) as exc_info:
        Nested.baz

    expected = f"""
You tried to shift this more times than Injector has levels:

{stack_representation}
    """.strip()

    assert str(exc_info.value) == expected


@multiple_places
def _jZeStu3dDx7Y(Root, number, Nested):
    class Container(Injector):
        root = Root
        result = this.sub.bar
        sub = Nested
        foo = number

    return Container


@multiple_places
def _tQiEZ1Hqor7v(Root, number, Nested):
    return Injector(root=Root, result=this.sub.bar, sub=Nested, foo=number)


@nested_variant(
    """
Nested.baz
  Nested.bar
    """.strip()
)
def _zAJUUNLtIHxw(Baz):
    class Nested(Injector):
        bar = (this << 1).foo
        baz = Baz

    return Nested


@nested_variant(
    """
Injector.baz
  Injector.bar
    """.strip()
)
def _hvS5ZQPuMK0i(Baz):
    return Injector(bar=(this << 1).foo, baz=Baz)


deny_depends_on = CodeCollector("stack_representation", "code")


@deny_depends_on.parametrize
def test_deny_classes_depend_on_nested_injectors(stack_representation, code):
    """Classes should not receive nested injectors as arguments of constructors."""

    class Foo:
        def __init__(self, bar):
            raise RuntimeError

    class Bar(Injector):
        baz = None

    with pytest.raises(DependencyError) as exc_info:
        code(Foo, Bar)

    expected = f"""
Do not depend on nested injectors directly.

Use this object to access inner attributes of nested injector:

{stack_representation}
    """.strip()
    assert expected == str(exc_info.value)


@deny_depends_on("Container.foo")
def _xLzoX5QDFuuw(Foo, Bar):
    class Container(Injector):
        foo = Foo
        bar = Bar

    Container.foo


@deny_depends_on("Injector.foo")
def _jrp5adysQeRH(Foo, Bar):
    Injector(foo=Foo, bar=Bar).foo
