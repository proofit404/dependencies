"""Tests related to Injector classes written inside other Injector classes."""
import pytest

from collector import CodeCollector
from dependencies import Injector
from dependencies import this
from dependencies.exceptions import DependencyError


def test_one_subcontainer_multiple_parents(define, let, has, expect, name):
    """Same sub container can be used in many parent containers.

    This usage should not overlap those containers. And more importantly, sub container
    should not be modified after usage.

    """
    root = define.cls(
        "Root", let.fun("__init__", "self, result", "self.result = result")
    )
    baz = define.cls("Baz", let.fun("__init__", "self, bar", "raise RuntimeError"))

    nested = has(bar="(this << 1).foo", baz=baz)
    it1 = has(root=root, result="this.sub.bar", sub=nested, foo="1")
    it2 = has(root=root, result="this.sub.bar", sub=nested, foo="2")

    expect(it1).to("obj.root.result == 1")
    expect(it2).to("obj.root.result == 2")

    message = f"""
You tried to shift this more times than Injector has levels:

{name(nested)}.baz
  {name(nested)}.bar
    """.strip()
    expect(nested).to_raise(message).when("obj.baz")


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
