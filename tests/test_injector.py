"""Tests related to the Injector classes."""
from inspect import isclass

import pytest

from dependencies import Injector
from dependencies import this
from dependencies import value
from dependencies.exceptions import DependencyError
from helpers import CodeCollector


def test_lambda_dependency():
    """Inject lambda function."""

    class Foo:
        def __init__(self, add):
            self.add = add

        def do(self, x):
            return self.add(x, x)

    class Container(Injector):
        foo = Foo
        add = lambda x, y: x + y  # noqa: E731

    assert Container.foo.do(1) == 2


def test_function_dependency():
    """Inject regular function."""

    class Foo:
        def __init__(self, add):
            self.add = add

        def do(self, x):
            return self.add(x, x)

    def plus(x, y):
        return x + y

    class Container(Injector):
        foo = Foo
        add = plus

    assert Container.foo.do(1) == 2


def test_inline_dependency():
    """Inject method defined inside Injector subclass."""

    class Foo:
        def __init__(self, add):
            self.add = add

        def do(self, x):
            return self.add(x, x)

    class Container(Injector):
        foo = Foo

        def add(x, y):
            return x + y

    assert Container.foo.do(1) == 2


def test_class_dependency():
    """Inject class.

    Instantiate class from the same scope and inject its instance.

    """

    class Foo:
        def __init__(self, add, bar):
            self.add = add
            self.bar = bar

        def do(self, x):
            return self.add(self.bar.go(x), self.bar.go(x))

    class Bar:
        def __init__(self, mul):
            self.mul = mul

        def go(self, x):
            return self.mul(x, x)

    class Container(Injector):
        foo = Foo
        bar = Bar
        add = lambda x, y: x + y  # noqa: E731
        mul = lambda x, y: x * y  # noqa: E731

    assert Container.foo.do(2) == 8


def test_do_not_instantiate_dependencies_ended_with_class():
    """Do not call class constructor, if it stored with name ended `_class`.

    For example, `logger_class`.

    """

    class Foo:
        pass

    class Bar:
        def __init__(self, foo_class):
            self.foo_class = foo_class

    class Container(Injector):
        foo_class = Foo
        bar = Bar

    assert isclass(Container.bar.foo_class)


def test_redefine_dependency():
    """We can redefine dependency by inheritance from the `Injector` subclass."""

    class Foo:
        def __init__(self, add):
            self.add = add

        def do(self, x):
            return self.add(x, x)

    class Container(Injector):
        foo = Foo
        add = lambda x, y: x + y  # noqa: E731  # pragma: no cover

    class WrongContainer(Container):
        add = lambda x, y: x - y  # noqa: E731

    assert WrongContainer.foo.do(1) == 0


def test_override_keyword_argument_if_dependency_was_specified():
    """Injector attributes takes precedence on default keyword arguments.

    Use specified dependency for constructor keyword arguments if dependency with
    desired name was mentioned in the injector.

    """

    class Foo:
        def __init__(self, add, y=1):
            self.add = add
            self.y = y

        def do(self, x):
            return self.add(x, self.y)

    class Container(Injector):
        foo = Foo
        add = lambda x, y: x + y  # noqa: E731
        y = 2

    assert Container.foo.do(1) == 3


def test_preserve_keyword_argument_if_dependency_was_missed():
    """Default keyword arguments should be used if injector attribute is missing.

    Use constructor keyword arguments if dependency with desired name was missed in the
    injector.

    """

    class Foo:
        def __init__(self, add, y=1):
            self.add = add
            self.y = y

        def do(self, x):
            return self.add(x, self.y)

    class Container(Injector):
        foo = Foo
        add = lambda x, y: x + y  # noqa: E731

    assert Container.foo.do(1) == 2


def test_preserve_missed_keyword_argument_in_the_middle():
    """Missed injector attributes could be defined in any order.

    Use default keyword argument and override following keyword argument since it was
    specified in the constructor.

    """

    class Foo:
        def __init__(self, x, y=1, z=2):
            self.x = x
            self.y = y
            self.z = z

        def do(self):
            return self.x + self.y + self.z

    class Container(Injector):
        foo = Foo
        x = 5
        z = 1

    assert Container.foo.do() == 7


def test_no_reuse_default_value_between_dependencies():
    """Deny to reuse default value of keyword argument in another dependency.

    Default argument of one dependency should not affect an argument of another
    dependency with the same name.

    """

    class Foo:
        def __init__(self, bar, x, y):
            raise RuntimeError

    class Bar:
        def __init__(self, x, y=1):
            pass

    class Container(Injector):
        foo = Foo
        bar = Bar
        x = 1

    with pytest.raises(DependencyError) as exc_info:
        Container.foo

    assert str(exc_info.value) == "Can not resolve attribute 'y' while building 'foo'"


def test_class_named_argument_default_value():
    """Allow classes as default argument values if argument name ends with `_class`."""

    class Foo:
        pass

    class Bar:
        def __init__(self, foo_class=Foo):
            self.foo_class = foo_class

    class Container(Injector):
        bar = Bar

    assert Container.bar.foo_class is Foo


def test_injectable_without_its_own_init():
    """Instantiate classes without it's own constructor.

    Inject dependencies into object subclass which doesn't specify its own `__init__`.

    """

    class Foo:
        def do(self):
            return 1

    class Baz(Injector):
        foo = Foo

    assert Baz.foo.do() == 1


def test_injectable_with_parent_init():
    """Inject dependencies into object which parent class define `__init__`."""

    class Foo:
        def __init__(self, x, y):
            self.x = x
            self.y = y

    class Bar(Foo):
        def add(self):
            return self.x + self.y

    class Baz(Injector):
        bar = Bar
        x = 1
        y = 2

    assert Baz.bar.add() == 3


def test_injectable_with_parent_without_init():
    """Inject dependencies into object which parent doesn't define `__init__`."""

    class Foo:
        pass

    class Bar(Foo):
        def add(self):
            return 3

    class Baz(Injector):
        bar = Bar

    assert Baz.bar.add() == 3


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


def test_show_injected_dependencies_with_dir():
    """`dir` should show injected dependencies and hide `__dependencies__` container."""

    class Foo(Injector):
        x = 1

    assert "x" in dir(Foo)
    assert "__dependencies__" not in dir(Foo)


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


attribute_assignment = CodeCollector()


@attribute_assignment.parametrize
def test_deny_injector_changes(code):
    """Explicitly deny change of any kind on `Injector` and its subclasses."""
    with pytest.raises(DependencyError) as exc_info:
        code()

    assert str(exc_info.value) == "'Injector' modification is not allowed"


@attribute_assignment
def _mvT9oyJdXhzh():
    class Container(Injector):
        x = 1

    Container.foo = 1


@attribute_assignment
def _fXxRX4KFUc8q():
    Injector.foo = 1


@attribute_assignment
def _pHfF0rbEjCsV():
    Container = Injector(x=1)
    Container.foo = 1


@attribute_assignment
def _xhZaIhujf34t():
    class Container(Injector):
        foo = 1

    del Container.foo


@attribute_assignment
def _jShuBfttg97c():
    Container = Injector(foo=1)
    del Container.foo


@attribute_assignment
def _tQeRzD5ZsyTm():
    del Injector.foo


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


multiple_inheritance = CodeCollector()


@multiple_inheritance.parametrize
def test_multiple_inheritance(code):
    """We can mix injector together."""

    class Foo:
        pass

    class Bar:
        def __init__(self, foo):
            self.foo = foo

    class Baz:
        def __init__(self, bar):
            self.bar = bar

    class FooContainer(Injector):
        foo = Foo

    class BarContainer(Injector):
        bar = Bar

    class BazContainer(Injector):
        baz = Baz

    foo = code(FooContainer, BarContainer, BazContainer)

    assert isinstance(foo, Foo)


@multiple_inheritance
def _edf946cc6077(FooContainer, BarContainer, BazContainer):
    class Container(FooContainer, BarContainer, BazContainer):
        pass

    return Container.baz.bar.foo


@multiple_inheritance
def _efdc426cd096(FooContainer, BarContainer, BazContainer):
    return (FooContainer & BarContainer & BazContainer).baz.bar.foo


inheritance_order = CodeCollector("expected", "code")


@inheritance_order.parametrize
def test_multiple_inheritance_injectors_order(expected, code):
    """Order of `Injector` subclasses should affect injection result.

    `Injector` which comes first in the subclass bases or inplace creation must have
    higher precedence.

    """

    class Foo:
        def __init__(self, x):
            self.x = x

    class Container1(Injector):
        foo = Foo
        x = 1

    class Container2(Injector):
        x = 2

    class Container3(Injector):
        x = 3

    value = code(Container1, Container2, Container3)

    assert expected == value


@inheritance_order(1)
def _aa10c7747a1f(Container1, Container2, Container3):
    class Container(Container1, Container2, Container3):
        pass

    return Container.foo.x


@inheritance_order(4)
def _e056e22f3fd5(Container1, Container2, Container3):
    class Container(Container1, Container2, Container3):
        x = 4

    return Container.foo.x


@inheritance_order(1)
def _d851e0414bdf(Container1, Container2, Container3):
    return (Container1 & Container2 & Container3).foo.x


attribute_error = CodeCollector()


@attribute_error.parametrize
def test_attribute_error(code):
    """Raise `DependencyError` if we can't find dependency."""
    with pytest.raises(DependencyError) as exc_info:
        code()

    assert str(exc_info.value) == "Can not resolve attribute 'test'"


@attribute_error
def _c58b054bfcd0():
    class Foo(Injector):
        x = 1

    Foo.test


@attribute_error
def _f9c50c81e8c9():
    Foo = Injector(x=1)

    Foo.test


@attribute_error
def _e2f16596a652():
    class Foo(Injector):
        x = 1

    Foo(y=2).test


incomplete_dependencies = CodeCollector()


@incomplete_dependencies.parametrize
def test_incomplete_dependencies_error(code):
    """Raise `DependencyError` if we can't find dependency."""
    with pytest.raises(DependencyError) as exc_info:
        code()

    assert (
        str(exc_info.value) == "Can not resolve attribute 'test' while building 'bar'"
    )


@incomplete_dependencies
def _c4e7ecf75167():
    class Bar:
        def __init__(self, test, two=2):
            raise RuntimeError

    class Foo(Injector):
        bar = Bar

    Foo.bar


@incomplete_dependencies
def _dmsMgYqbsHgB():
    class Bar:
        def __init__(self, test):
            raise RuntimeError

    Foo = Injector(bar=Bar)

    Foo.bar


has_attribute = CodeCollector()


@has_attribute.parametrize
def test_has_attribute(code):
    """`Injector` should support `in` statement."""
    container = code()
    assert "foo" in container
    assert "bar" not in container


@has_attribute
def _gwufxYkhURAF():
    class Container(Injector):
        foo = 1

    return Container


@has_attribute
def _zlZoLka31ndk():
    return Injector(foo=1)


subclasses_only = CodeCollector()


@subclasses_only.parametrize
def test_multiple_inheritance_deny_regular_classes(code):
    """Only `Injector` subclasses are allowed to be used in the inheritance."""

    class Foo:
        pass

    with pytest.raises(DependencyError) as exc_info:
        code(Foo)

    message = str(exc_info.value)
    assert message == "Multiple inheritance is allowed for Injector subclasses only"


@subclasses_only
def _f1583394f1a6(Foo):
    class Bar(Injector, Foo):
        pass


@subclasses_only
def _b51814725d07(Foo):
    Injector & Foo


deny_magic_methods = CodeCollector()


@deny_magic_methods.parametrize
def test_deny_magic_methods_injection(code):
    """`Injector` doesn't accept magic methods."""

    class Foo:
        pass

    with pytest.raises(DependencyError) as exc_info:
        code(Foo)

    assert str(exc_info.value) == "Magic methods are not allowed"


@deny_magic_methods
def _e78bf771747c(Foo):
    class Container(Injector):
        foo = Foo

        def __eq__(self, other):
            raise RuntimeError

    Container.foo


@deny_magic_methods
def _e34b88041f64(Foo):
    def eq(self, other):
        raise RuntimeError

    Injector(foo=Foo, __eq__=eq).foo


deny_empty_scope = CodeCollector()


@deny_empty_scope.parametrize
def test_deny_empty_scope_extension(code):
    """`Injector` subclasses can't extend scope with empty subset."""
    with pytest.raises(DependencyError) as exc_info:
        code()

    assert str(exc_info.value) == "Extension scope can not be empty"


@deny_empty_scope
def _fQl3MI95Y1Zi():
    class Container(Injector):
        pass


@deny_empty_scope
def _pdnQASIDVq2V():
    Injector()


@deny_empty_scope
def _aWNEsKRIx12r():
    class Container(Injector):
        x = 1

    class SubContainer(Container):
        pass


@deny_empty_scope
def _myj1ZoubR68j():
    class Container(Injector):
        x = 1

    Container()
