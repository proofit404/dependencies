"""Tests related to Injector classes written inside other Injector classes."""
import pytest

from dependencies import Injector
from dependencies import this
from dependencies.exceptions import DependencyError
from helpers import CodeCollector


multiple_places = CodeCollector()
nested_variant = CodeCollector("sub")


@multiple_places.parametrize
@nested_variant.parametrize
def test_one_subcontainer_multiple_parents(code, sub):
    """Same sub container can be used in many parent containers.

    This usage should not overlap those containers.

    """

    class Root:
        def __init__(self, result):
            self.result = result

    Nested = sub()
    Container1 = code(Root, 1, Nested)
    Container2 = code(Root, 2, Nested)

    assert Container1.root.result == 1
    assert Container2.root.result == 2


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


@nested_variant
def _zAJUUNLtIHxw():
    class Nested(Injector):
        bar = (this << 1).foo

    return Nested


@nested_variant
def _hvS5ZQPuMK0i():
    return Injector(bar=(this << 1).foo)


deny_direct_resolve = CodeCollector()


@deny_direct_resolve.parametrize
def test_direct_nested_injector_resolve(code):
    """Attempt to resolve nested injector directly should raise exception.

    Nested injectors are allowed to be used as this object targets.

    """
    with pytest.raises(DependencyError) as exc_info:
        code()
    expected = "'Injector' dependencies could only be used to instantiate classes"
    assert str(exc_info.value) == expected


@deny_direct_resolve
def _wlimEBYr7skq():
    class Container(Injector):
        class Nested(Injector):
            foo = 1

    Container.Nested


@deny_direct_resolve
def _bA1A3d0zf1hZ():
    Injector(Nested=Injector(foo=1)).Nested


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
