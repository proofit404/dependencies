"""Tests related to the Injector subclasses."""
from inspect import isclass

import pytest

from dependencies import Injector
from dependencies.exceptions import DependencyError
from helpers import CodeCollector


def test_lambda_dependency():
    """Inject lambda function."""

    class Foo:
        def __init__(self, add):
            self.add = add

        def do(self, x):
            return self.add(x, x)

    class Summator(Injector):
        foo = Foo
        add = lambda x, y: x + y  # noqa: E731

    assert Summator.foo.do(1) == 2


def test_function_dependency():
    """Inject regular function."""

    class Foo:
        def __init__(self, add):
            self.add = add

        def do(self, x):
            return self.add(x, x)

    def plus(x, y):
        return x + y

    class Summator(Injector):
        foo = Foo
        add = plus

    assert Summator.foo.do(1) == 2


def test_inline_dependency():
    """Inject method defined inside Injector subclass."""

    class Foo:
        def __init__(self, add):
            self.add = add

        def do(self, x):
            return self.add(x, x)

    class Summator(Injector):
        foo = Foo

        def add(x, y):
            return x + y

    assert Summator.foo.do(1) == 2


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

    class Summator(Injector):
        foo = Foo
        bar = Bar
        add = lambda x, y: x + y  # noqa: E731
        mul = lambda x, y: x * y  # noqa: E731

    assert Summator.foo.do(2) == 8


def test_do_not_instantiate_dependencies_ended_with_class():
    """Do not call class constructor, if it stored with name ended `_class`.

    For example, `logger_class`.

    """

    class Foo:
        pass

    class Bar(Injector):
        foo_class = Foo

    assert isclass(Bar.foo_class)


def test_redefine_dependency():
    """We can redefine dependency by inheritance from the `Injector` subclass."""

    class Foo:
        def __init__(self, add):
            self.add = add

        def do(self, x):
            return self.add(x, x)

    class Summator(Injector):
        foo = Foo
        add = lambda x, y: x + y  # noqa: E731

    class WrongSummator(Summator):
        add = lambda x, y: x - y  # noqa: E731

    assert WrongSummator.foo.do(1) == 0


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

    class Summator(Injector):
        foo = Foo
        add = lambda x, y: x + y  # noqa: E731
        y = 2

    assert Summator.foo.do(1) == 3


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

    class Summator(Injector):
        foo = Foo
        add = lambda x, y: x + y  # noqa: E731

    assert Summator.foo.do(1) == 2


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
            pass

    class Bar:
        def __init__(self, x, y=1):
            pass

    class Container(Injector):
        foo = Foo
        bar = Bar
        x = 1

    with pytest.raises(DependencyError) as exc_info:
        Container.foo

    assert (
        str(exc_info.value)
        == "'Container' can not resolve attribute 'y' while building 'foo'"
    )


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
        pass

    assert issubclass(Foo(), Foo)


def test_call_overwrite_dependencies():
    """`Injector()` produce `Injector` subclass with overwritten dependencies."""

    class Foo(Injector):
        bar = 1

    assert Foo(bar=2).bar == 2


def test_call_resolve_not_overwritten_dependencies():
    """`Injector()` can resolve dependencies it doesn't touch."""

    class Foo(Injector):
        bar = 1

    assert Foo(baz=2).bar == 1


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

    class Common:
        pass

    class Foo(Injector):
        pass

    assert dir(Common) == dir(Foo)


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
        pass

    assert "x" in dir(Foo(x=1))


def test_omit_parent_link_in_dir_listing():
    """Don't show `__parent__` link in the `dir` output.

    It is an implementation detail.

    """

    class Foo(Injector):
        class Bar(Injector):
            pass

    assert "__parent__" not in dir(Foo.Bar)


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
        pass

    Container.foo = 1


@attribute_assignment
def _fXxRX4KFUc8q():
    Injector.foo = 1


@attribute_assignment
def _pHfF0rbEjCsV():
    Container = Injector()
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


def test_nested_injectors():
    """`Injector` subclass could be used as attribute of another `Injector` subclass."""

    def do_x(a, b):
        return a + b

    def do_y(c, d):
        return c * d

    class Call:
        def __init__(self, foo, bar):
            self.foo = foo
            self.bar = bar

        def __call__(self, one, two, three):
            return self.bar.y(self.foo.x(one, two), three)

    class Foo(Injector):
        x = do_x

    class Bar(Injector):
        y = do_y

    class Baz(Injector):
        foo = Foo
        bar = Bar
        do = Call

    assert Baz.do(1, 2, 3) == 9


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

        pass

    assert Foo.__doc__ == "New container."


evaluate_classes = CodeCollector()


@evaluate_classes.parametrize
def test_evaluate_dependencies_once(code):
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

    code(Container)


@evaluate_classes
def _ea4367450e47(Container):
    x = Container.a
    assert x.b.d is x.c.d


@evaluate_classes
def _dd91602f3455(Container):
    assert Container.a.b.d is not Container.a.b.d
    assert Container.a.b.d is not Container.a.c.d


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

    code(Foo, FooContainer, BarContainer, BazContainer)


@multiple_inheritance
def _edf946cc6077(Foo, FooContainer, BarContainer, BazContainer):
    class Container(FooContainer, BarContainer, BazContainer):
        pass

    assert isinstance(Container.baz.bar.foo, Foo)


@multiple_inheritance
def _efdc426cd096(Foo, FooContainer, BarContainer, BazContainer):
    assert isinstance((FooContainer & BarContainer & BazContainer).baz.bar.foo, Foo)


inheritance_order = CodeCollector()


@inheritance_order.parametrize
def test_multiple_inheritance_injectors_order(code):
    """Order of `Injector` subclasses should affect injection result.

    `Injector` which comes first in the subclass bases or inplace creation must have
    higher precedence.

    """

    class Container1(Injector):
        x = 1

    class Container2(Injector):
        x = 2

    class Container3(Injector):
        x = 3

    code(Container1, Container2, Container3)


@inheritance_order
def _aa10c7747a1f(Container1, Container2, Container3):
    class Foo(Container1, Container2, Container3):
        pass

    assert Foo.x == 1


@inheritance_order
def _e056e22f3fd5(Container1, Container2, Container3):
    class Foo(Container1, Container2, Container3):
        x = 4

    assert Foo.x == 4


@inheritance_order
def _d851e0414bdf(Container1, Container2, Container3):
    assert (Container1 & Container2 & Container3).x == 1


attribute_error = CodeCollector()


@attribute_error.parametrize
def test_attribute_error(code):
    """Raise `DependencyError` if we can't find dependency."""
    with pytest.raises(DependencyError) as exc_info:
        code()

    assert str(exc_info.value) in {
        "'Foo' can not resolve attribute 'test'",
        "'Injector' can not resolve attribute 'test'",
    }


@attribute_error
def _c58b054bfcd0():
    class Foo(Injector):
        pass

    Foo.test


@attribute_error
def _f9c50c81e8c9():
    Foo = Injector()

    Foo.test


@attribute_error
def _e2f16596a652():
    class Foo(Injector):
        pass

    Foo().test


incomplete_dependencies = CodeCollector()


@incomplete_dependencies.parametrize
def test_incomplete_dependencies_error(code):
    """Raise `DependencyError` if we can't find dependency."""
    with pytest.raises(DependencyError) as exc_info:
        code()

    assert str(exc_info.value) in {
        "'Foo' can not resolve attribute 'test' while building 'bar'",
        "'Injector' can not resolve attribute 'test' while building 'bar'",
    }


@incomplete_dependencies
def _c4e7ecf75167():
    class Bar:
        def __init__(self, test, two=2):
            pass  # pragma: no cover

    class Foo(Injector):
        bar = Bar

    Foo.bar


@incomplete_dependencies
def _dmsMgYqbsHgB():
    class Bar:
        def __init__(self, test):
            pass  # pragma: no cover

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
