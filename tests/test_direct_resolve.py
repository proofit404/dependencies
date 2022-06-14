"""Tests related to direct resolve rules."""


def test_direct_data_resolve(has, expect):
    """Attempt to resolve scalar types directly should raise exception.

    Scalar types are allowed to be used as dependencies for classes.

    """
    it = has(a="1")
    message = "Scalar dependencies could only be used to instantiate classes"
    expect(it).to_raise(message).when("obj.a")


def test_direct_this_resolve(let, has, expect):
    """Attempt to resolve this directly should raise exception.

    This objects are allowed to be used as dependencies for classes.

    """
    it = has(a=let.this("b"), b="1")
    message = "'this' dependencies could only be used to instantiate classes"
    expect(it).to_raise(message).when("obj.a")


def test_direct_nested_injector_resolve(has, expect):
    """Attempt to resolve nested injector directly should raise exception.

    Nested injectors are allowed to be used as this object targets.

    """
    it = has(Nested=has(foo="1"))
    message = "'Injector' dependencies could only be used to instantiate classes"
    expect(it).to_raise(message).when("obj.Nested")


def test_direct_value_resolve(let, has, expect):
    """Attempt to resolve value directly should raise exception.

    Values are allowed to be used as dependencies for classes.

    """
    it = has(a=let.value("a", "", "return 1"))
    message = "'value' dependencies could only be used to instantiate classes"
    expect(it).to_raise(message).when("obj.a")


def test_direct_package_data_resolve(define, has, expect):
    """Attempt to resolve scalar types directly should raise exception."""
    it = has(a=define.package("examples.submodule.variable"))
    message = "Scalar dependencies could only be used to instantiate classes"
    expect(it).to_raise(message).when("obj.a")


def test_direct_package_class_resolve(define, has, expect):
    """Attempt to resolve class directly should works for packages."""
    define.require("examples.submodule", "Foo")
    it = has(foo=define.package("examples.submodule.Foo"))
    expect(it).to("isinstance(obj.foo, Foo)")
