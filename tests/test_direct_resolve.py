"""Tests related to direct resolve rules."""
from dependencies import Package
from dependencies import this
from dependencies import value


def test_direct_data_resolve(has, expect):
    """Attempt to resolve scalar types directly should raise exception.

    Scalar types are allowed to be used as dependencies for classes.

    """
    message = "Scalar dependencies could only be used to instantiate classes"
    Container = has(a=1)
    expect(Container).to_raise(message).when("obj.a")


def test_direct_this_resolve(has, expect):
    """Attempt to resolve this directly should raise exception.

    This objects are allowed to be used as dependencies for classes.

    """
    message = "'this' dependencies could only be used to instantiate classes"
    Container = has(a=this.b, b=1)
    expect(Container).to_raise(message).when("obj.a")


def test_direct_nested_injector_resolve(has, expect):
    """Attempt to resolve nested injector directly should raise exception.

    Nested injectors are allowed to be used as this object targets.

    """
    message = "'Injector' dependencies could only be used to instantiate classes"
    Container = has(Nested=has(foo=1))
    expect(Container).to_raise(message).when("obj.Nested")


def test_direct_value_resolve(has, expect):
    """Attempt to resolve value directly should raise exception.

    Values are allowed to be used as dependencies for classes.

    """
    message = "'value' dependencies could only be used to instantiate classes"

    @value
    def a():
        return 1

    Container = has(a=a)
    expect(Container).to_raise(message).when("obj.a")


def test_direct_package_data_resolve(has, expect):
    """Attempt to resolve scalar types directly should raise exception."""
    message = "Scalar dependencies could only be used to instantiate classes"
    examples = Package("examples")
    Container = has(a=examples.submodule.variable)
    expect(Container).to_raise(message).when("obj.a")


def test_direct_package_class_resolve(has, expect):
    """Attempt to resolve class directly should works for packages."""
    from examples.submodule import Foo

    examples = Package("examples")
    Container = has(foo=examples.submodule.Foo)
    expect(Container).to("isinstance(obj.foo, Foo)")
