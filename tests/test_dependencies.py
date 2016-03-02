import pytest

from dependencies import Injector, DependencyError


def test_lambda_dependency():
    """Inject lambda function."""

    class Foo(object):
        def __init__(self, add):
            self.add = add
        def do(self, x):
            return self.add(x, x)

    class Summator(Injector):
        foo = Foo
        add = lambda x, y: x + y

    assert Summator.foo.do(1) == 2


def test_function_dependency():
    """Inject regular function."""

    class Foo(object):
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

    class Foo(object):
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

    class Foo(object):
        def __init__(self, add, bar):
            self.add = add
            self.bar = bar
        def do(self, x):
            return self.add(self.bar.go(x), self.bar.go(x))

    class Bar(object):
        def __init__(self, mul):
            self.mul = mul
        def go(self, x):
            return self.mul(x, x)

    class Summator(Injector):
        foo = Foo
        bar = Bar
        add = lambda x, y: x + y
        mul = lambda x, y: x * y

    assert Summator.foo.do(2) == 8


def test_redefine_dependency():
    """We can redefine dependency by inheritance from the `Injector`
    subclass.

    """

    class Foo(object):
        def __init__(self, add):
            self.add = add
        def do(self, x):
            return self.add(x, x)

    class Summator(Injector):
        foo = Foo
        add = lambda x, y: x + y

    class WrongSummator(Summator.__class__):
        add = lambda x, y: x - y

    assert WrongSummator.foo.do(1) == 0


def test_injector_deny_multiple_inheritance():
    """`Injector` may be used in single inheritance only."""

    class Foo(object):
        pass

    with pytest.raises(DependencyError):
        class Foo(Injector, Foo):
            pass


def test_magic_methods_not_allowed_in_the_injector():
    """`Injector` doesn't accept magic methods."""

    with pytest.raises(DependencyError):
        class Bar(Injector):
            def __eq__(self, other):
                pass


def test_attribute_error():
    """Raise attribute error if we can't find dependency."""

    class Foo(Injector):
        pass

    with pytest.raises(AttributeError):
        Foo.test


def test_circle_dependencies():
    """Throw `DependencyError` if class needs a dependency named same as class."""


    with pytest.raises(DependencyError):

        class Foo(object):
            def __init__(self, foo):
                self.foo = foo
            def do(self, x):
                return self.foo(x, x)

        class Summator(Injector):
            foo = Foo


def test_owerride_keyword_argument_if_dependency_was_specified():
    """Use specified dependency for constructor keyword arguments if
    dependency with desired name was mentioned in the injector.

    """

    class Foo(object):
        def __init__(self, add, y=1):
            self.add = add
            self.y = y
        def do(self, x):
            return self.add(x, self.y)

    class Summator(Injector):
        foo = Foo
        add = lambda x, y: x + y
        y = 2

    assert Summator.foo.do(1) == 3


def test_preserve_keyword_argument_if_dependency_was_missed():
    """Use constructor keyword arguments if dependency with desired name
    was missed in the injector.

    """

    class Foo(object):
        def __init__(self, add, y=1):
            self.add = add
            self.y = y
        def do(self, x):
            return self.add(x, self.y)

    class Summator(Injector):
        foo = Foo
        add = lambda x, y: x + y

    assert Summator.foo.do(1) == 2


def test_preserve_single_asterisk_arguments():
    """Inject `*args` into constructor."""

    class Foo(object):
        def __init__(self, func, *args):
            self.func = func
            self.args = args
        def do(self):
            return self.func(self.args)

    class Summator(Injector):
        foo = Foo
        func = sum
        args = (1, 2, 3)

    assert Summator.foo.do() == 6


def test_preserve_multiple_asterisk_arguments():
    """Inject `**kwargs` into constructor."""

    class Foo(object):
        def __init__(self, func, **kwargs):
            self.func = func
            self.kwargs = kwargs
        def do(self):
            return self.func(**self.kwargs)

    class Summator(Injector):
        foo = Foo
        func = sum
        kwargs = {
            'sequence': (1, 2, 3),
            'start': 5,
        }

    assert Summator.foo.do() == 11
