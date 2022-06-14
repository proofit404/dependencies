"""Tests related to the Injector classes."""
# FIXME: All direct resolve paragraphs should went into single markdown file.
#
# FIXME: Code collector should be removed from the codebase.
from inspect import isclass

import pytest

from collector import CodeCollector
from dependencies import Injector
from dependencies import this
from dependencies import value
from dependencies.exceptions import DependencyError


def test_lambda_dependency(define, let, has, expect):
    """Inject lambda function."""
    foo = define.cls(
        "Foo",
        let.fun("__init__", "self, add", "self.add = add"),
        let.fun("do", "self, x", "return self.add(x, x)"),
    )
    it = has(foo=foo, add=let.fn("x, y", "x + y"))
    expect(it).to("obj.foo.do(1) == 2")


def test_function_dependency(define, let, has, expect):
    """Inject regular function."""
    foo = define.cls(
        "Foo",
        let.fun("__init__", "self, add", "self.add = add"),
        let.fun("do", "self, x", "return self.add(x, x)"),
    )
    plus = define.fun("plus", "x, y", "return x + y")
    it = has(foo=foo, add=plus)
    expect(it).to("obj.foo.do(1) == 2")


def test_inline_dependency(define, let, has, expect):
    """Inject method defined inside Injector subclass."""
    foo = define.cls(
        "Foo",
        let.fun("__init__", "self, add", "self.add = add"),
        let.fun("do", "self, x", "return self.add(x, x)"),
    )
    it = has(foo=foo, add=let.fun("add", "x, y", "return x + y"))
    expect(it).to("obj.foo.do(1) == 2")


def test_class_dependency(define, let, has, expect):
    """Inject class.

    Instantiate class from the same scope and inject its instance.

    """

    foo = define.cls(
        "Foo",
        let.fun("__init__", "self, add, bar", "self.add = add", "self.bar = bar"),
        let.fun("do", "self, x", "return self.add(self.bar.go(x), self.bar.go(x))"),
    )
    bar = define.cls(
        "Bar",
        let.fun("__init__", "self, mul", "self.mul = mul"),
        let.fun("go", "self, x", "return self.mul(x, x)"),
    )
    it = has(foo=foo, bar=bar, add=let.fn("x, y", "x + y"), mul=let.fn("x, y", "x * y"))
    expect(it).to("obj.foo.do(2) == 8")


def test_do_not_instantiate_dependencies_ended_with_class(define, let, has, expect):
    """Do not call class constructor, if it stored with name ended `_class`.

    For example, `logger_class`.

    """
    define.require("inspect", "isclass")
    foo = define.cls("Foo")
    bar = define.cls(
        "Bar", let.fun("__init__", "self, foo_class", "self.foo_class = foo_class")
    )
    it = has(foo_class=foo, bar=bar)
    expect(it).to("isclass(obj.bar.foo_class)")


def test_redefine_dependency(define, let, has, expect):
    """We can redefine dependency by inheritance from the `Injector` subclass."""
    foo = define.cls(
        "Foo",
        let.fun("__init__", "self, add", "self.add = add"),
        let.fun("do", "self, x", "return self.add(x, x)"),
    )
    it = has(foo=foo, add=let.fn("x, y", "x + y"))
    wrong = has(it, add=let.fn("x, y", "x - y"))
    expect(wrong).to("obj.foo.do(1) == 0")


def test_override_keyword_argument_if_dependency_was_specified(
    define, let, has, expect
):
    """Injector attributes takes precedence on default keyword arguments.

    Use specified dependency for constructor keyword arguments if dependency with
    desired name was mentioned in the injector.

    """
    foo = define.cls(
        "Foo",
        let.fun("__init__", "self, add, y=1", "self.add = add", "self.y = y"),
        let.fun("do", "self, x", "return self.add(x, self.y)"),
    )
    it = has(foo=foo, add=let.fn("x, y", "x + y"), y="2")
    expect(it).to("obj.foo.do(1) == 3")


def test_preserve_keyword_argument_if_dependency_was_missed(define, let, has, expect):
    """Default keyword arguments should be used if injector attribute is missing.

    Use constructor keyword arguments if dependency with desired name was missed in the
    injector.

    """
    foo = define.cls(
        "Foo",
        let.fun("__init__", "self, add, y=1", "self.add = add", "self.y = y"),
        let.fun("do", "self, x", "return self.add(x, self.y)"),
    )
    it = has(foo=foo, add=let.fn("x, y", "x + y"))
    expect(it).to("obj.foo.do(1) == 2")


def test_preserve_missed_keyword_argument_in_the_middle(define, let, has, expect):
    """Missed injector attributes could be defined in any order.

    Use default keyword argument and override following keyword argument since it was
    specified in the constructor.

    """
    foo = define.cls(
        "Foo",
        let.fun(
            "__init__", "self, x, y=1, z=2", "self.x = x", "self.y = y", "self.z = z"
        ),
        let.fun("do", "self", "return self.x + self.y + self.z"),
    )
    it = has(foo=foo, x="5", z="1")
    expect(it).to("obj.foo.do() == 7")


def test_no_reuse_default_value_between_dependencies(define, let, has, expect, name):
    """Deny to reuse default value of keyword argument in another dependency.

    Default argument of one dependency should not affect an argument of another
    dependency with the same name.

    """
    foo = define.cls(
        "Foo", let.fun("__init__", "self, bar, x, y", "raise RuntimeError")
    )
    bar = define.cls("Bar", let.fun("__init__", "self, x, y=1", "pass"))
    it = has(foo=foo, bar=bar, x="1")
    message = f"""
Can not resolve attribute 'y':

{name(it)}.foo
  {name(it)}.y
    """
    expect(it).to_raise(message).when("obj.foo")


def test_class_named_argument_default_value(define, let, has, expect):
    """Allow classes as default argument values if argument name ends with `_class`."""
    # FIXME: Tests like this should be in a separate file.
    foo = define.cls("Foo")
    bar = define.cls(
        "Bar", let.fun("__init__", "self, foo_class=Foo", "self.foo_class = foo_class")
    )
    it = has(bar=bar)
    expect(it).to("obj.bar.foo_class is Foo")


def test_injectable_without_its_own_init(define, let, has, expect):
    """Instantiate classes without it's own constructor.

    Inject dependencies into object subclass which doesn't specify its own `__init__`.

    """
    foo = define.cls("Foo", let.fun("do", "self", "return 1"))
    it = has(foo=foo)
    expect(it).to("obj.foo.do() == 1")


def test_injectable_with_parent_init(define, let, has, expect):
    """Inject dependencies into object which parent class define `__init__`."""
    foo = define.cls(
        "Foo", let.fun("__init__", "self, x, y", "self.x = x", "self.y = y")
    )
    bar = define.cls("Bar", foo, let.fun("add", "self", "return self.x + self.y"))
    it = has(bar=bar, x="1", y="2")
    expect(it).to("obj.bar.add() == 3")


def test_injectable_with_parent_without_init(define, let, has, expect):
    """Inject dependencies into object which parent doesn't define `__init__`."""
    foo = define.cls("Foo")
    bar = define.cls("Bar", foo, let.fun("add", "self", "return 3"))
    it = has(bar=bar)
    expect(it).to("obj.bar.add() == 3")


def test_call():
    """`Injector` subclass can produce its own subclasses with call."""

    class Foo(Injector):
        x = 1

    assert issubclass(Foo(y=2), Foo)


def test_call_overwrite_dependencies():
    """`Injector()` produce `Injector` subclass with overwritten dependencies."""

    class Foo:
        def __init__(self, bar):
            self.bar = bar

    class Container(Injector):
        foo = Foo
        bar = 1

    assert Container(bar=2).foo.bar == 2


def test_call_resolve_not_overwritten_dependencies():
    """`Injector()` can resolve dependencies it doesn't touch."""

    class Foo:
        def __init__(self, bar):
            self.bar = bar

    class Container(Injector):
        foo = Foo
        bar = 1

    assert Container(baz=2).foo.bar == 1


def test_call_on_injector_directly():
    """`Injector` could be called directly."""

    class Foo:
        def __init__(self, bar):
            self.bar = bar

    class Bar:
        def __init__(self, baz):
            self.baz = baz

    assert Injector(foo=Foo, bar=Bar, baz=1).foo.bar.baz == 1


def test_show_common_class_attributes_with_dir():
    """`dir` show common class attributes."""

    class Foo(Injector):
        x = 1
        y = 2
        z = 3

    assert dir(Foo) == ["x", "y", "z"]


def test_show_injected_dependencies_with_dir_once():
    """Do not repeat injected dependencies in the inheritance chain."""

    class Foo(Injector):
        x = 1

    class Bar(Foo):
        x = 2

    assert dir(Bar).count("x") == 1


def test_show_call_dependencies_with_dir():
    """`dir` show dependencies injected with call."""
    assert "x" in dir(Injector(x=1))

    class Foo(Injector):
        y = 2

    assert "x" in dir(Foo(x=1))


def test_deny_injector_attribute_assignment(has, expect):
    """Deny attribute assignment on `Injector` and its subclasses."""
    it = has(foo="1")
    message = "'Injector' modification is not allowed"
    expect(it).to_raise(message).when("obj.foo = 2")


def test_deny_injector_attribute_deletion(has, expect):
    """Deny attribute deletion on `Injector` and its subclasses."""
    it = has(foo="1")
    message = "'Injector' modification is not allowed"
    expect(it).to_raise(message).when("del obj.foo")


def test_docstrings():
    """Check we can access Injector docstring.

    It's handled by metaclass at runtime.

    """
    assert (
        Injector.__doc__
        == """Default dependencies specification DSL.

    Classes inherited from this class may inject dependencies into classes specified in
    it namespace.

    """
    )

    class Foo(Injector):
        """New container."""

        x = 1

    assert Foo.__doc__ == "New container."


def test_evaluate_dependencies_once():
    """Evaluate each node in the dependencies graph once."""

    class A:
        def __init__(self, b, c):
            self.b = b
            self.c = c

    class B:
        def __init__(self, d):
            self.d = d

    class C:
        def __init__(self, d):
            self.d = d

    class D:
        pass

    class Container(Injector):
        a = A
        b = B
        c = C
        d = D

    assert Container.a.b.d is not Container.a.b.d
    assert Container.a.b.d is not Container.a.c.d

    x = Container.a

    assert x.b.d is x.c.d


evaluate_once = CodeCollector()
evaluate_once_a = CodeCollector("a")
evaluate_once_b = CodeCollector("b")
evaluate_once_c = CodeCollector("c")
evaluate_once_d = CodeCollector("d")


@evaluate_once.parametrize
@evaluate_once_a.parametrize
@evaluate_once_b.parametrize
@evaluate_once_c.parametrize
@evaluate_once_d.parametrize
def test_evaluate_once_different_types(code, a, b, c, d):
    """Evaluate each node in the dependencies graph once.

    Arguments of dependencies of different types should be evaluated once. This rules
    applies to classes and @value objects. This is a variation of the test above written
    against all necessary inputs.

    """

    class Root:
        def __init__(self, a):
            self.a = a

    times = []
    Container = code(Root, a(), b(), c(), d(times))
    assert sum(times) == 0
    Container.root.a
    assert sum(times) == 1


@evaluate_once
def _rNYf35g94V1B(Root, A, B, C, D):
    class Container(Injector):
        root = Root
        a = A
        b = B
        c = C
        d = D

    return Container


@evaluate_once
def _uf0ibIiz0aIl(Root, A, B, C, D):
    return Injector(root=Root, a=A, b=B, c=C, d=D)


@evaluate_once_a
def _irfiju659gxv():
    class A:
        def __init__(self, b, c):
            pass

    return A


@evaluate_once_a
def _eik35aKD1khF():
    @value
    def a(b, c):
        pass

    return a


@evaluate_once_b
def _n9K1km2utmbt():
    class B:
        def __init__(self, d):
            pass

    return B


@evaluate_once_b
def _mtGW5dk9BMBw():
    @value
    def b(d):
        pass

    return b


@evaluate_once_c
def _k6pJn1sVihhd():
    class C:
        def __init__(self, d):
            pass

    return C


@evaluate_once_c
def _z7bIvBpQsr4H():
    @value
    def c(d):
        pass

    return c


@evaluate_once_d
def _wjwPzTamAceJ(times):
    class D:
        def __init__(self):
            times.append(1)

    return D


@evaluate_once_d
def _s7pP3oP4L3pZ(times):
    @value
    def d():
        times.append(1)

    return d


evaluate_once_nested = CodeCollector()
evaluate_once_nested_a = CodeCollector("a")
evaluate_once_nested_b = CodeCollector("b")
evaluate_once_nested_c = CodeCollector("c")
evaluate_once_nested_d = CodeCollector("d")
evaluate_once_nested_e = CodeCollector("e")


@evaluate_once_nested.parametrize
@evaluate_once_nested_a.parametrize
@evaluate_once_nested_b.parametrize
@evaluate_once_nested_c.parametrize
@evaluate_once_nested_d.parametrize
@evaluate_once_nested_e.parametrize
def test_evaluate_once_nested_container(code, a, b, c, d, e):
    """Evaluate each node in the dependencies graph once.

    This example focus on evaluating dependencies once when they do spread between
    different levels of nesting and point into each other with `this` expression.

    """
    d_times = []
    e_times = []

    class Root:
        def __init__(self, a):
            self.a = a

    Container = code(Root, a(), b(), c(), d(d_times), e(e_times))
    assert sum(d_times) == 0
    assert sum(e_times) == 0
    Container.root.a
    assert sum(d_times) == 1
    assert sum(e_times) == 1


@evaluate_once_nested
def _jz4WmFNvuMvA(Root, A, B, C, D, E):
    class Container(Injector):
        root = Root
        a = A
        b = this.Nested.b
        d = this.Nested.d
        e = E

        class Nested(Injector):
            b = B
            c = this.Nested.c
            d = this.Nested.d
            e = (this << 1).e

            class Nested(Injector):
                c = C
                d = this.Nested.d
                e = (this << 2).e

                class Nested(Injector):
                    d = D
                    e = (this << 3).e

    return Container


@evaluate_once_nested
def _eM4Wsqhs9ZgY(Root, A, B, C, D, E):
    return Injector(
        root=Root,
        a=A,
        b=this.Nested.b,
        d=this.Nested.d,
        e=E,
        Nested=Injector(
            b=B,
            c=this.Nested.c,
            d=this.Nested.d,
            e=(this << 1).e,
            Nested=Injector(
                c=C,
                d=this.Nested.d,
                e=(this << 2).e,
                Nested=Injector(d=D, e=(this << 3).e),
            ),
        ),
    )


@evaluate_once_nested_a
def _fxNSkQOelDSi():
    class A:
        def __init__(self, b, d, e):
            pass

    return A


@evaluate_once_nested_a
def _kNI9K2bXIDtb():
    @value
    def a(b, d, e):
        pass

    return a


@evaluate_once_nested_b
def _mK1iiIfP4aJx():
    class B:
        def __init__(self, c, d, e):
            pass

    return B


@evaluate_once_nested_b
def _tbtPIyWKAnm9():
    @value
    def b(c, d, e):
        pass

    return b


@evaluate_once_nested_c
def _dhUanzFtSGz8():
    class C:
        def __init__(self, d, e):
            pass

    return C


@evaluate_once_nested_c
def _u48SjCngqrsn():
    @value
    def c(d, e):
        pass

    return c


@evaluate_once_nested_d
def _hU4RLEy6zD8M(times):
    class D:
        def __init__(self, e):
            times.append(1)

    return D


@evaluate_once_nested_d
def _zLrf3TSoKacA(times):
    @value
    def d(e):
        times.append(1)

    return d


@evaluate_once_nested_e
def _gn5dOH5wCCKx(times):
    class E:
        def __init__(self):
            times.append(1)

    return E


@evaluate_once_nested_e
def _qDSvtJ7LHoNl(times):
    @value
    def e():
        times.append(1)

    return e


def test_multiple_inheritance(define, let, has, expect):
    """We can mix injector together."""
    foo = define.cls("Foo")
    bar = define.cls("Bar", let.fun("__init__", "self, foo", "self.foo = foo"))
    baz = define.cls("Baz", let.fun("__init__", "self, bar", "self.bar = bar"))
    it = has(has(foo=foo), has(bar=bar), has(baz=baz))
    expect(it).to("isinstance(obj.baz.bar.foo, Foo)")


def test_multiple_inheritance_injectors_order(define, let, has, expect):
    """Order of `Injector` subclasses should affect injection result.

    `Injector` which comes first in the subclass bases or inplace creation must have
    higher precedence.

    """

    foo = define.cls("Foo", let.fun("__init__", "self, x", "self.x = x"))

    it = has(has(foo=foo, x="1"), has(x="2"), has(x="3"))
    expect(it).to("obj.foo.x == 1")

    it = has(has(foo=foo, x="1"), has(x="2"), has(x="3"), x="4")
    expect(it).to("obj.foo.x == 4")


def test_missing_dependency(has, expect, name):
    """Raise `DependencyError` if we can't find dependency."""
    it = has(has(x="1"), y="2")
    message = f"""
Can not resolve attribute 'test':

{name(it)}.test
    """
    expect(it).to_raise(message).when("obj.test")


def test_incomplete_dependencies_error(define, let, has, expect, name):
    """Raise `DependencyError` if we can't find dependency."""
    bar = define.cls("Bar", let.fun("__init__", "self, test", "raise RuntimeError"))
    it = has(bar=bar)
    message = f"""
Can not resolve attribute 'test':

{name(it)}.bar
  {name(it)}.test
    """
    expect(it).to_raise(message).when("obj.bar")


circle_dependencies = CodeCollector("stack_representation", "code")


@circle_dependencies.parametrize
def test_circle_dependency_error(stack_representation, code):
    """Handle circle definitions in dependency graph.

    Attempt to resolve such definition would end up with recursion error. We should
    provide readable error message from what users would be able to understand what
    exactly they defined wrong.

    """
    with pytest.raises(DependencyError) as exc_info:
        code()

    expected = f"""
Circle error found in definition of the dependency graph:

{stack_representation}
    """.strip()

    assert str(exc_info.value) == expected


@circle_dependencies(
    """
Container.foo
  Container.bar
    SubContainer.bar
      SubSubContainer.baz
        Container.quiz
          SubContainer.ham
            SubSubContainer.egg
              Container.foo
    """.strip()
)
def _dhQgq7aBGY7j():
    class Foo:
        def __init__(self, bar):
            raise RuntimeError

    class Container(Injector):
        foo = Foo
        bar = this.SubContainer.bar
        quiz = this.SubContainer.ham

        class SubContainer(Injector):
            bar = this.SubSubContainer.baz
            ham = this.SubSubContainer.egg

            class SubSubContainer(Injector):
                baz = (this << 2).quiz
                egg = (this << 2).foo

    Container.foo


@circle_dependencies(
    """
Injector.foo
  Injector.bar
    Injector.bar
      Injector.baz
        Injector.quiz
          Injector.ham
            Injector.egg
              Injector.foo
    """.strip()
)
def _nHW3zQ0Kv3se():
    class Foo:
        def __init__(self, bar):
            raise RuntimeError

    Injector(
        foo=Foo,
        bar=this.SubContainer.bar,
        quiz=this.SubContainer.ham,
        SubContainer=Injector(
            bar=this.SubSubContainer.baz,
            ham=this.SubSubContainer.egg,
            SubSubContainer=Injector(
                baz=(this << 2).quiz,
                egg=(this << 2).foo,
            ),
        ),
    ).foo


def test_has_attribute(has, expect):
    """`Injector` should support `in` statement."""
    expect.skip_if_context()
    it = has(foo="1")
    expect(it).to("'foo' in obj")
    expect(it).to("'bar' not in obj")


def test_multiple_inheritance_deny_regular_classes(define, let, has, expect):
    """Only `Injector` subclasses are allowed to be used in the inheritance."""
    foo = define.cls("Foo")
    message = "Multiple inheritance is allowed for Injector subclasses only"
    expect().to_raise(message).when(has("Injector", foo))


def test_deny_magic_methods_injection(define, let, has, expect):
    """`Injector` doesn't accept magic methods."""
    foo = define.cls("Foo")
    eq = define.fun("eq", "self, other", "raise RuntimeError")
    it = has(foo=foo, __eq__=eq)
    message = "Magic methods are not allowed"
    expect(it).to_raise(message).when("obj.foo")


def test_deny_empty_scope_extension(has, expect):
    """`Injector` subclasses can't extend scope with empty subset."""
    # FIXME: Figure out how to use this with `expect`.

    with pytest.raises(DependencyError) as exc_info:
        has()

    assert str(exc_info.value) == "Extension scope can not be empty"

    with pytest.raises(DependencyError) as exc_info:
        has(has(x=1))

    assert str(exc_info.value) == "Extension scope can not be empty"
