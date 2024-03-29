"""Tests related to the Injector classes."""
from inspect import isclass

import pytest

from dependencies import Injector
from dependencies import this
from dependencies.exceptions import DependencyError


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

    expected = """
Can not resolve attribute 'y':

Container.foo
  Container.y
    """.strip()

    assert str(exc_info.value) == expected


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


def test_deny_injector_attribute_assignment(expect):
    """Deny attribute assignment on `Injector` and its subclasses."""

    class Container(Injector):
        foo = 1

    @expect(Container, Injector)
    def to_be(it):
        with pytest.raises(DependencyError) as exc_info:
            it.foo = 1
        assert str(exc_info.value) == "'Injector' modification is not allowed"


def test_deny_injector_attribute_deletion(expect):
    """Deny attribute deletion on `Injector` and its subclasses."""

    class Container(Injector):
        foo = 1

    @expect(Container, Injector)
    def to_be(it):
        with pytest.raises(DependencyError) as exc_info:
            del it.foo
        assert str(exc_info.value) == "'Injector' modification is not allowed"


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


def test_multiple_inheritance():
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

    class Container(FooContainer, BarContainer, BazContainer):
        pass

    assert isinstance(Container.baz.bar.foo, Foo)
    assert isinstance((FooContainer & BarContainer & BazContainer).baz.bar.foo, Foo)


def test_multiple_inheritance_injectors_order():
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

    class Container4(Container1, Container2, Container3):
        pass

    class Container5(Container1, Container2, Container3):
        x = 4

    assert (Container1 & Container2 & Container3).foo.x == 1
    assert Container4.foo.x == 1
    assert Container5.foo.x == 4


def test_attribute_error():
    """Raise `DependencyError` if we can't find dependency."""

    class Foo(Injector):
        x = 1

    with pytest.raises(DependencyError) as exc_info:
        Foo.test

    expected = """
Can not resolve attribute 'test':

Foo.test
    """.strip()

    assert str(exc_info.value) == expected


def test_incomplete_dependencies_error():
    """Raise `DependencyError` if we can't find dependency."""

    class Bar:
        def __init__(self, test, two=2):
            raise RuntimeError

    class Foo(Injector):
        bar = Bar

    with pytest.raises(DependencyError) as exc_info:
        Foo.bar

    expected = """
Can not resolve attribute 'test':

Foo.bar
  Foo.test
    """.strip()

    assert str(exc_info.value) == expected


def test_circle_dependency_error():
    """Handle circle definitions in dependency graph.

    Attempt to resolve such definition would end up with recursion error. We should
    provide readable error message from what users would be able to understand what
    exactly they defined wrong.

    """

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

    with pytest.raises(DependencyError) as exc_info:
        Container.foo

    expected = """
Circle error found in definition of the dependency graph:

Container.foo
  Container.bar
    SubContainer.bar
      SubSubContainer.baz
        Container.quiz
          SubContainer.ham
            SubSubContainer.egg
              Container.foo
    """.strip()

    assert str(exc_info.value) == expected


def test_has_attribute():
    """`Injector` should support `in` statement."""

    class Container(Injector):
        foo = 1

    assert "foo" in Container
    assert "bar" not in Container


def test_multiple_inheritance_deny_regular_classes():
    """Only `Injector` subclasses are allowed to be used in the inheritance."""

    class Foo:
        pass

    expected = "Multiple inheritance is allowed for Injector subclasses only"

    with pytest.raises(DependencyError) as exc_info:

        class Bar(Injector, Foo):
            pass

    assert str(exc_info.value) == expected

    with pytest.raises(DependencyError) as exc_info:
        Injector & Foo

    assert str(exc_info.value) == expected


def test_deny_magic_methods():
    """`Injector` doesn't accept magic methods."""

    class Foo:
        pass

    class Container(Injector):
        foo = Foo

        def __eq__(self, other):
            raise RuntimeError

    with pytest.raises(DependencyError) as exc_info:
        Container.foo

    assert str(exc_info.value) == "Magic methods are not allowed"


def test_deny_empty_scope_extension():
    """`Injector` subclasses can't extend scope with empty subset."""
    with pytest.raises(DependencyError) as exc_info:

        class Foo(Injector):
            pass

    assert str(exc_info.value) == "Extension scope can not be empty"

    with pytest.raises(DependencyError) as exc_info:
        Injector()

    assert str(exc_info.value) == "Extension scope can not be empty"

    class Container(Injector):
        x = 1

    with pytest.raises(DependencyError) as exc_info:

        class Bar(Container):
            pass

    assert str(exc_info.value) == "Extension scope can not be empty"

    with pytest.raises(DependencyError) as exc_info:
        Container()

    assert str(exc_info.value) == "Extension scope can not be empty"
