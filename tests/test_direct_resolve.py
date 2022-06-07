"""Tests related to direct resolve rules."""
from dependencies import Package
from dependencies import this
from dependencies import value
from dependencies.exceptions import DependencyError


def test_direct_data_resolve(has, expect):
    """Attempt to resolve scalar types directly should raise exception.

    Scalar types are allowed to be used as dependencies for classes.

    """
    Container = has(a=1)
    _ = expect(Container).to_raise().catch(lambda obj: obj.a)
    assert _ == "Scalar dependencies could only be used to instantiate classes"


def test_direct_this_resolve(has, expect):
    """Attempt to resolve this directly should raise exception.

    This objects are allowed to be used as dependencies for classes.

    """
    Container = has(a=this.b, b=1)
    _ = expect(Container).to_raise().catch(lambda obj: obj.a)
    assert _ == "'this' dependencies could only be used to instantiate classes"


def test_direct_nested_injector_resolve(has, expect):
    """Attempt to resolve nested injector directly should raise exception.

    Nested injectors are allowed to be used as this object targets.

    """
    Container = has(Nested=has(foo=1))
    _ = expect(Container).to_raise().catch(lambda obj: obj.Nested)
    assert _ == "'Injector' dependencies could only be used to instantiate classes"


def test_direct_value_resolve(has, expect):
    """Attempt to resolve value directly should raise exception.

    Values are allowed to be used as dependencies for classes.

    """

    @value
    def a():
        return 1

    Container = has(a=a)
    _ = expect(Container).to_raise().catch(lambda obj: obj.a)
    assert _ == "'value' dependencies could only be used to instantiate classes"


def test_direct_package_data_resolve(has, expect):
    """Attempt to resolve scalar types directly should raise exception."""
    examples = Package("examples")
    Container = has(a=examples.submodule.variable)
    _ = expect(Container).to_raise().catch(lambda obj: obj.a)
    expected = "Scalar dependencies could only be used to instantiate classes"
    assert _ == expected


def test_direct_package_class_resolve(has, expect):
    """Attempt to resolve class directly should works for packages."""
    from examples.submodule import Foo

    examples = Package("examples")
    Container = has(foo=examples.submodule.Foo)
    expect(Container).to(lambda obj: isinstance(obj.foo, Foo))
