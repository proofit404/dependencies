"""Tests related to direct resolve rules."""


def test_direct_data_resolve(define, has, expect):
    """Attempt to resolve scalar types directly should raise exception.

    Scalar types are allowed to be used as dependencies for classes.

    """
    a = define.var("1")
    it = has(a=a)
    message = "Scalar dependencies could only be used to instantiate classes"
    expect(it).to_raise(message).when("obj.a")


def test_direct_this_resolve(define, has, expect):
    """Attempt to resolve this directly should raise exception.

    This objects are allowed to be used as dependencies for classes.

    """
    b = define.var("1")
    it = has(a="this.b", b=b)
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
    it = has(a=let.fun("a", "", "return 1").dec("value"))
    message = "'value' dependencies could only be used to instantiate classes"
    expect(it).to_raise(message).when("obj.a")
