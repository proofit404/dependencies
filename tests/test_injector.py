"""Tests related to the Injector classes."""
import pytest

from dependencies import Injector
from dependencies import value
from signature import Signature


def test_lambda_dependency(expect):
    """Inject lambda function."""

    class Foo:
        def __init__(self, add):
            self.add = add

        def do(self, x):
            return self.add(x, x)

    class Container(Injector):
        foo = Foo
        add = lambda x, y: x + y  # noqa: E731

    @expect(Container)
    def case(it):
        assert it.foo.do(1) == 2


def test_function_dependency(expect):
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

    @expect(Container)
    def case(it):
        assert it.foo.do(1) == 2


def test_inline_dependency(expect):
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

    @expect(Container)
    def case(it):
        assert it.foo.do(1) == 2


def test_class_dependency(expect):
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

    @expect(Container)
    def case(it):
        assert it.foo.do(2) == 8


def test_redefine_dependency(expect):
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

    @expect(WrongContainer)
    def case(it):
        assert it.foo.do(1) == 0


def _defaults():
    class Foo:
        def __init__(self, y=1):
            self.y = y

    @value
    def foo(y=1):
        return Signature(y=y)

    yield Foo
    yield foo


@pytest.mark.parametrize("arg", _defaults())
def test_override_keyword_argument_if_dependency_was_specified(e, expect, arg):
    """Injector attributes takes precedence on default keyword arguments.

    Use specified dependency for constructor keyword arguments if dependency with
    desired name was mentioned in the injector.

    """

    class Container(Injector):
        bar = e.Take["foo"]
        foo = arg
        y = 2

    @expect(Container)
    def case(it):
        assert it.bar.y == 2


@pytest.mark.parametrize("arg", _defaults())
def test_preserve_keyword_argument_if_dependency_was_missed(e, expect, arg):
    """Default keyword arguments should be used if injector attribute is missing.

    Use constructor keyword arguments if dependency with desired name was missed in the
    injector.

    """

    class Container(Injector):
        baz = e.Take["foo"]
        foo = arg

    @expect(Container)
    def case(it):
        assert it.baz.y == 1


def _middle():
    class Foo:
        def __init__(self, x, y=1, z=2):
            self.x = x
            self.y = y
            self.z = z

    @value
    def foo(x, y=1, z=2):
        return Signature(x=x, y=y, z=z)

    yield Foo
    yield foo


@pytest.mark.parametrize("arg", _middle())
def test_preserve_missed_keyword_argument_in_the_middle(e, expect, arg):
    """Missed injector attributes could be defined in any order.

    Use default keyword argument and override following keyword argument since it was
    specified in the constructor.

    """

    class Container(Injector):
        quiz = e.Take["foo"]
        foo = arg
        x = 5
        z = 1

    @expect(Container)
    def case(it):
        assert it.quiz.x + it.quiz.y + it.quiz.z == 7


@pytest.mark.parametrize("arg", _defaults())
def test_no_reuse_default_value_between_dependencies(expect, catch, arg):
    """Deny to reuse default value of keyword argument in another dependency.

    Default argument of one dependency should not affect an argument of another
    dependency with the same name.

    """

    class Foo:
        def __init__(self, bar, y):
            raise RuntimeError

    class Container(Injector):
        foo = Foo
        bar = arg

    @expect(Container)
    @catch(
        """
Can not resolve attribute 'y':

Container.foo
  Container.y
        """
    )
    def case(it):
        it.foo


def test_injectable_without_its_own_init(expect):
    """Instantiate classes without it's own constructor.

    Inject dependencies into object subclass which doesn't specify its own `__init__`.

    """

    class Foo:
        def do(self):
            return 1

    class Baz(Injector):
        foo = Foo

    @expect(Baz)
    def case(it):
        assert it.foo.do() == 1


def test_injectable_with_parent_init(expect):
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

    @expect(Baz)
    def case(it):
        assert it.bar.add() == 3


def test_injectable_with_parent_without_init(expect):
    """Inject dependencies into object which parent doesn't define `__init__`."""

    class Foo:
        pass

    class Bar(Foo):
        def add(self):
            return 3

    class Baz(Injector):
        bar = Bar

    @expect(Baz)
    def case(it):
        assert it.bar.add() == 3


def test_show_common_class_attributes_with_dir(expect):
    """`dir` show common class attributes."""
    expect.skip_if_scope()

    class Container(Injector):
        x = 1
        y = 2
        z = 3

    @expect(Container)
    def case(it):
        assert dir(it) == ["x", "y", "z"]

    @expect(Injector(x=1, y=2, z=3))
    def case(it):
        assert dir(it) == ["x", "y", "z"]


def test_show_injected_dependencies_with_dir_once(expect):
    """Do not repeat injected dependencies in the inheritance chain."""
    expect.skip_if_scope()

    class Foo(Injector):
        x = 1

    class Bar(Foo):
        x = 2

    @expect(Bar)
    def case(it):
        assert dir(it).count("x") == 1


def test_show_call_dependencies_with_dir(expect):
    """`dir` show dependencies injected with call."""
    expect.skip_if_scope()

    class Foo(Injector):
        y = 2

    @expect(Foo(x=1))
    def case(it):
        assert "x" in dir(it)

    @expect(Injector(x=1))
    def case(it):
        assert "x" in dir(it)


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


def test_attribute_error(expect, catch):
    """Raise `DependencyError` if we can't find dependency."""

    class Container(Injector):
        x = 1

    @expect(Container)
    @catch(
        """
Can not resolve attribute 'test':

Container.test
        """
    )
    def case(it):
        it.test


def test_incomplete_dependencies_error(expect, catch):
    """Raise `DependencyError` if we can't find dependency."""

    class Foo:
        def __init__(self, test):
            raise RuntimeError

    class Container(Injector):
        foo = Foo

    @expect(Container)
    @catch(
        """
Can not resolve attribute 'test':

Container.foo
  Container.test
        """
    )
    def case(it):
        it.foo


def test_has_attribute(expect):
    """`Injector` should support `in` statement."""
    expect.skip_if_scope()

    class Container(Injector):
        foo = 1

    @expect(Container)
    def case(it):
        assert "foo" in it
        assert "bar" not in it


def test_deny_magic_methods(expect, catch):
    """`Injector` doesn't accept magic methods."""

    class Container(Injector):
        def __eq__(self, other):
            raise RuntimeError

    @expect(Container)
    @catch("Magic methods are not allowed")
    def case(it):
        it.foo
