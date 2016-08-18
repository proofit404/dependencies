"""Dependencies test suite."""

import inspect
from textwrap import dedent

import pytest

from dependencies import Injector, DependencyError


def test_lambda_dependency():
    """Inject lambda function."""

    class Foo(object):
        def __init__(self, add):
            self.add = add
        def do(self, x):  # noqa: E301
            return self.add(x, x)

    class Summator(Injector):
        foo = Foo
        add = lambda x, y: x + y  # noqa: E731

    assert Summator.foo.do(1) == 2


def test_function_dependency():
    """Inject regular function."""

    class Foo(object):
        def __init__(self, add):
            self.add = add
        def do(self, x):  # noqa: E301
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
        def do(self, x):  # noqa: E301
            return self.add(x, x)

    class Summator(Injector):
        foo = Foo
        def add(x, y):  # noqa: E301
            return x + y

    assert Summator.foo.do(1) == 2


def test_class_dependency():
    """
    Inject class.

    Instantiate class from the same scope and inject its instance.
    """

    class Foo(object):
        def __init__(self, add, bar):
            self.add = add
            self.bar = bar
        def do(self, x):  # noqa: E301
            return self.add(self.bar.go(x), self.bar.go(x))

    class Bar(object):
        def __init__(self, mul):
            self.mul = mul
        def go(self, x):  # noqa: E301
            return self.mul(x, x)

    class Summator(Injector):
        foo = Foo
        bar = Bar
        add = lambda x, y: x + y  # noqa: E731
        mul = lambda x, y: x * y  # noqa: E731

    assert Summator.foo.do(2) == 8


def test_redefine_dependency():
    """
    We can redefine dependency by inheritance from the `Injector`
    subclass.
    """

    class Foo(object):
        def __init__(self, add):
            self.add = add
        def do(self, x):  # noqa: E301
            return self.add(x, x)

    class Summator(Injector):
        foo = Foo
        add = lambda x, y: x + y  # noqa: E731

    class WrongSummator(Summator):
        add = lambda x, y: x - y  # noqa: E731

    assert WrongSummator.foo.do(1) == 0


def test_injector_deny_multiple_inheritance():
    """`Injector` may be used in single inheritance only."""

    class Foo(object):
        pass

    with pytest.raises(DependencyError) as exc_info:
        class Foo(Injector, Foo):
            pass

    assert str(exc_info.value) == 'Multiple inheritance is not allowed'


@pytest.mark.parametrize('code', [
    # Declarative injector.
    """
    class Bar(Injector):
        def __eq__(self, other):
            return False
    """,
    # Let notation.
    """
    class Foo(Injector):
        pass

    Foo.let(__eq__=lambda self, other: False)
    """,
    # Attribute assignment.
    """
    class Foo(Injector):
        pass

    Foo.__eq__ = lambda self, other: False
    """,
])
def test_deny_magic_methods_injection(code):
    """`Injector` doesn't accept magic methods."""

    scope = {'Injector': Injector}

    with pytest.raises(DependencyError) as exc_info:
        exec(dedent(code), scope)

    assert str(exc_info.value) == 'Magic methods are not allowed'


@pytest.mark.parametrize('code', [
    # Declarative injector.
    """
    class Foo(Injector):
        pass

    Foo.test
    """,
    # Let notation.
    """
    Foo = Injector.let()

    Foo.test
    """,
    # Let notation from subclass.
    """
    class Foo(Injector):
        pass

    Foo.let().test
    """,
    # Keyword arguments in the constructor.
    """
    class Bar(object):
        def __init__(self, test, two=2):
            self.test = test
            self.two = two

    class Foo(Injector):
        bar = Bar

    Foo.bar
    """,
])
def test_attribute_error(code):
    """Raise attribute error if we can't find dependency."""

    scope = {'Injector': Injector}

    with pytest.raises(AttributeError) as exc_info:
        exec(dedent(code), scope)

    assert str(exc_info.value) in set([
        "'Foo' object has no attribute 'test'",
        "'Injector' object has no attribute 'test'",
    ])


@pytest.mark.parametrize('code', [
    # Declarative injector.
    """
    class Summator(Injector):
        foo = Foo

    Summator.foo
    """,
    # Let notation.
    """
    Summator = Injector.let(foo=Foo)

    Summator.foo
    """,
    # Attribute assignment.
    """
    Summator = Injector.let()

    Summator.foo = Foo

    Summator.foo
    """,
])
def test_circle_dependencies(code):
    """
    Throw `DependencyError` if class needs a dependency named same as
    class.  `Summator.foo` will fail with maximum recursion depth.  So
    we need to raise exception before this attribute access.
    """

    class Foo(object):
        def __init__(self, foo):
            self.foo = foo

    scope = {'Injector': Injector, 'Foo': Foo}

    with pytest.raises(DependencyError) as exc_info:
        exec(dedent(code), scope)

    assert str(exc_info.value).startswith(
        "'foo' is a circle dependency in the <class 'test_dependencies."
    )
    assert str(exc_info.value).endswith(".Foo'> constructor")


@pytest.mark.parametrize('code', [
    # Declarative injector.
    """
    class Summator(Injector):
        foo = Foo
        bar = Bar

    Summator.foo
    """,
    # Declarative injector with inheritance.
    """
    class First(Injector):
        foo = Foo

    class Second(First):
        bar = Bar

    Second.foo
    """,
    # Let notation.
    """
    Summator = Injector.let(foo=Foo, bar=Bar)

    Summator.foo
    """
    # Let notation chain.
    """
    Summator = Injector.let(foo=Foo).let(bar=Bar)

    Summator.foo
    """,
    # Attribute assignment.
    """
    Summator = Injector.let()

    Summator.foo = Foo
    Summator.bar = Bar

    Summator.foo
    """,
])
def test_complex_circle_dependencies(code):
    """
    Throw `DependencyError` in the case of complex dependency recursion.

    One class define an argument in its constructor.  We have second
    class in the container named for this dependency.  This class
    define an argument in its constructor named like first class in
    the container.  We have mutual recursion in this case.
    """

    class Foo(object):
        def __init__(self, bar):
            self.bar = bar

    class Bar(object):
        def __init__(self, foo):
            self.foo = foo

    scope = {'Injector': Injector, 'Foo': Foo, 'Bar': Bar}

    with pytest.raises(DependencyError) as exc_info:
        exec(dedent(code), scope)

    message = str(exc_info.value)
    assert message.startswith("'foo'") or message.startswith("'bar'")
    part = " is a circle dependency in the <class 'test_dependencies."
    assert part in message
    assert (message.endswith(".Foo'> constructor") or
            message.endswith(".Bar'> constructor"))


@pytest.mark.parametrize('code', [
    # Declarative injector.
    """
    class Summator(Injector):
        foo = Foo
        bar = Bar
        baz = Baz

    Summator.foo
    """,
    # Declarative injector with inheritance.
    """
    class First(Injector):
        foo = Foo

    class Second(First):
        bar = Bar
        baz = Baz

    Second.foo
    """,
    # Let notation.
    """
    Summator = Injector.let(foo=Foo, bar=Bar, baz=Baz)

    Summator.foo
    """
    # Let notation chain.
    """
    Summator = Injector.let(foo=Foo).let(bar=Bar).let(baz=Baz)

    Summator.foo
    """,
    # Attribute assignment.
    """
    Summator = Injector.let()

    Summator.foo = Foo
    Summator.bar = Bar
    Summator.baz = Baz

    Summator.foo
    """,
])
def test_complex_circle_dependencies_long_circle(code):
    """
    Detect complex dependencies recursion with circles longer then two
    constructors.
    """

    class Foo(object):
        def __init__(self, bar):
            self.bar = bar

    class Bar(object):
        def __init__(self, baz):
            self.baz = baz

    class Baz(object):
        def __init__(self, foo):
            self.foo = foo

    scope = {'Injector': Injector, 'Foo': Foo, 'Bar': Bar, 'Baz': Baz}

    with pytest.raises(DependencyError) as exc_info:
        exec(dedent(code), scope)

    message = str(exc_info.value)
    assert (message.startswith("'foo'") or
            message.startswith("'bar'") or
            message.startswith("'baz'"))
    part = " is a circle dependency in the <class 'test_dependencies."
    assert part in message
    assert (message.endswith(".Foo'> constructor") or
            message.endswith(".Bar'> constructor") or
            message.endswith(".Baz'> constructor"))


def test_override_keyword_argument_if_dependency_was_specified():
    """
    Use specified dependency for constructor keyword arguments if
    dependency with desired name was mentioned in the injector.
    """

    class Foo(object):
        def __init__(self, add, y=1):
            self.add = add
            self.y = y
        def do(self, x):  # noqa: E301
            return self.add(x, self.y)

    class Summator(Injector):
        foo = Foo
        add = lambda x, y: x + y  # noqa: E731
        y = 2

    assert Summator.foo.do(1) == 3


def test_preserve_keyword_argument_if_dependency_was_missed():
    """
    Use constructor keyword arguments if dependency with desired name
    was missed in the injector.
    """

    class Foo(object):
        def __init__(self, add, y=1):
            self.add = add
            self.y = y
        def do(self, x):  # noqa: E301
            return self.add(x, self.y)

    class Summator(Injector):
        foo = Foo
        add = lambda x, y: x + y  # noqa: E731

    assert Summator.foo.do(1) == 2


def test_preserve_missed_keyword_argument_in_the_middle():
    """
    Use default keyword argument and override following keyword
    argument since it was specified in the constructor.
    """

    class Foo(object):
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


@pytest.mark.parametrize('code', [
    # Declarative injector.
    """
    class Summator(Injector):
        foo = Foo
        args = (1, 2, 3)
    """,
    # Let notation.
    """
    Injector.let(foo=Foo, args=(1, 2, 3))
    """,
    # Attribute assignment.
    """
    class Summator(Injector):
        args = (1, 2, 3)

    Summator.foo = Foo
    """,
])
def test_deny_arbitrary_argument_list(code):
    """Raise `DependencyError` if constructor have *args argument."""

    class Foo(object):
        def __init__(self, *args):
            self.args = args

    scope = {'Injector': Injector, 'Foo': Foo}

    with pytest.raises(DependencyError) as exc_info:
        exec(dedent(code), scope)

    assert str(exc_info.value).startswith("<class 'test_dependencies.")
    assert str(exc_info.value).endswith(
        "Foo'>.__init__ have arbitrary argument list"
    )


@pytest.mark.parametrize('code', [
    # Declarative injector.
    """
    class Summator(Injector):
        foo = Foo
        kwargs = {'start': 5}
    """,
    # Let notation.
    """
    Injector.let(foo=Foo, kwargs = {'start': 5})
    """,
    # Attribute assignment.
    """
    class Summator(Injector):
        kwargs = {'start': 5}

    Summator.foo = Foo
    """,
])
def test_deny_arbitrary_keyword_arguments(code):
    """Raise `DependencyError` if constructor have **kwargs argument."""

    class Foo(object):
        def __init__(self, **kwargs):
            self.kwargs = kwargs

    scope = {'Injector': Injector, 'Foo': Foo}

    with pytest.raises(DependencyError) as exc_info:
        exec(dedent(code), scope)

    assert str(exc_info.value).startswith("<class 'test_dependencies.")
    assert str(exc_info.value).endswith(
        "Foo'>.__init__ have arbitrary keyword arguments"
    )


@pytest.mark.parametrize('code', [
    # Declarative injector.
    """
    class Summator(Injector):
        foo = Foo
        args = (1, 2, 3)
        kwargs = {'start': 5}
    """,
    # Let notation.
    """
    Injector.let(foo=Foo, args=(1, 2, 3), kwargs={'start': 5})
    """,
    # Attribute assignment.
    """
    class Summator(Injector):
        args = (1, 2, 3)
        kwargs = {'start': 5}

    Summator.foo = Foo
    """,
])
def test_deny_arbitrary_positional_and_keyword_arguments_together(code):
    """
    Raise `DependencyError` if constructor have *args and **kwargs
    argument.
    """

    class Foo(object):
        def __init__(self, *args, **kwargs):
            self.args = args
            self.kwargs = kwargs

    scope = {'Injector': Injector, 'Foo': Foo}

    with pytest.raises(DependencyError) as exc_info:
        exec(dedent(code), scope)

    assert str(exc_info.value).startswith("<class 'test_dependencies.")
    assert str(exc_info.value).endswith(
        "Foo'>.__init__ have arbitrary argument list and keyword arguments"
    )


def test_injectable_without_its_own_init():
    """
    Inject dependencies into object subclass which doesn't specify its
    own `__init__`.
    """

    class Foo(object):
        def do(self):
            return 1

    class Baz(Injector):
        foo = Foo

    assert Baz.foo.do() == 1


def test_injectable_with_parent_init():
    """
    Inject dependencies into object which parent class define
    `__init__`.
    """

    class Foo(object):
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
    """
    Inject dependencies into object which parent doesn't define
    `__init__`.
    """

    class Foo(object):
        pass

    class Bar(Foo):
        def add(self):
            return 3

    class Baz(Injector):
        bar = Bar

    assert Baz.bar.add() == 3


def test_let_factory():
    """
    `Injector` subclass can produce its own subclasses with `let`
    factory.
    """

    class Foo(Injector):
        pass

    assert issubclass(Foo.let(), Foo)


def test_let_factory_overwrite_dependencies():
    """
    `Injector.let` produce `Injector` subclass with overwritten
    dependencies.
    """

    class Foo(Injector):
        bar = 1

    assert Foo.let(bar=2).bar == 2


def test_let_factory_resolve_not_overwritten_dependencies():
    """`Injector.let` can resolve dependencies it doesn't touch."""

    class Foo(Injector):
        bar = 1

    assert Foo.let(baz=2).bar == 1


@pytest.mark.parametrize('code', [
    # Declarative injector.
    """
    class Foo(Injector):
        let = 2
    """,
    # Let notation.
    """
    class Foo(Injector):
        pass

    Foo.let(let=1)
    """,
    # Attribute assignment.
    """
    class Foo(Injector):
        pass

    Foo.let = lambda cls, **kwargs: None
    """,
])
def test_deny_to_redefine_let_attribute(code):
    """We can't redefine let attribute in the `Injector` subclasses."""

    scope = {'Injector': Injector}

    with pytest.raises(DependencyError) as exc_info:
        exec(dedent(code), scope)

    assert str(exc_info.value) == "'let' redefinition is not allowed"


def test_let_factory_on_injector_directly():
    """
    Dependencies can be specified with `let` factory applied to
    `Injector` derectly.
    """

    class Foo(object):
        def __init__(self, bar):
            self.bar = bar

    class Bar(object):
        def __init__(self, baz):
            self.baz = baz

    assert Injector.let(foo=Foo, bar=Bar, baz=1).foo.bar.baz == 1


def test_do_not_instantiate_dependencies_ended_with_cls():
    """
    Do not call class constructor, if it stored with name ended
    `_cls`.

    For example, `logger_cls`.
    """

    class Foo(object):
        pass

    class Bar(Injector):
        foo_cls = Foo

    assert inspect.isclass(Bar.foo_cls)


@pytest.mark.parametrize('code', [
    # Direct call.
    """
    Injector()
    """,
    # Subclass call.
    """
    class Foo(Injector):
        pass

    Foo()
    """,
    # Ignore any arguments passed.
    """
    Injector(1)
    """,
    # Ignore any keyword argument passed.
    """
    Injector(x=1)
    """,
])
def test_deny_to_instantiate_injector(code):
    """Deny injector instantiation."""

    scope = {'Injector': Injector}

    with pytest.raises(DependencyError) as exc_info:
        exec(dedent(code), scope)

    assert str(exc_info.value) == 'Do not instantiate Injector'


def test_show_common_class_attributes_with_dir():
    """`dir` show common class attributes."""

    class Common(object):
        pass

    class Foo(Injector):
        pass

    dir(Common) == dir(Foo)


def test_show_injected_dependencies_with_dir():
    """
    `dir` should show injected dependencies and hide
    `__dependencies__` container.
    """

    class Foo(Injector):
        x = 1

    assert 'x' in dir(Foo)
    assert '__dependencies__' not in dir(Foo)


def test_show_injected_dependencies_with_dir_once():
    """Do not repeat injected dependencies in the inheritance chain."""

    class Foo(Injector):
        x = 1

    class Bar(Foo):
        x = 2

    assert dir(Bar).count('x') == 1


def test_show_let_dependencies_with_dir():
    """`dir` show dependencies injected with `let`."""

    assert 'x' in dir(Injector.let(x=1))

    class Foo(Injector):
        pass

    assert 'x' in dir(Foo.let(x=1))


def test_mutable_injector():
    """We can extend existed `Injector` by attribute assignment."""

    class Foo(object):
        def __init__(self, bar):
            self.bar = bar

    class Bar(object):
        pass

    class Baz(Injector):
        pass

    Baz.foo = Foo
    Baz.bar = Bar

    assert isinstance(Baz.foo, Foo)


def test_mutable_injector_let_expression():
    """
    We can extend `Injector` created with `let` expression by
    attribute assignment.
    """

    class Foo(object):
        def __init__(self, bar):
            self.bar = bar

    class Bar(object):
        pass

    Baz = Injector.let()

    Baz.foo = Foo
    Baz.bar = Bar

    assert isinstance(Baz.foo, Foo)


def test_mutable_injector_deny_to_modify_injector():
    """Deny to modify `Injector` itself."""

    with pytest.raises(DependencyError) as exc_info:
        Injector.foo = 1

    assert str(exc_info.value) == "'Injector' modification is not allowed"


# Unregister dependency.


@pytest.mark.parametrize('code', [
    # Declarative injector.
    """
    class Baz(Injector):
        foo = Foo
        bar = Bar

    del Baz.bar

    Baz.foo
    """,
    # Let notation.
    """
    Baz = Injector.let(foo=Foo, bar=Bar)

    del Baz.bar

    Baz.foo
    """,
    # Throw `AttributeError` if someone tries to delete missing
    # dependency.
    """
    del Injector.bar
    """,
    # Throw `AttributeError` if someone tries to delete missing
    # dependency in the `Injector` subclass.
    """
    class Baz(Injector):
        pass

    del Baz.bar
    """,
])
def test_unregister_dependency(code):
    """We can unregister dependency from `Injector` subclasses."""

    class Foo(object):
        def __init__(self, bar):
            self.bar = bar

    class Bar(object):
        pass

    scope = {'Injector': Injector, 'Foo': Foo, 'Bar': Bar}

    with pytest.raises(AttributeError) as exc_info:
        exec(dedent(code), scope)

    assert str(exc_info.value) in set([
        "'Baz' object has no attribute 'bar'",
        "'Injector' object has no attribute 'bar'",
    ])


def test_unregister_do_not_use_object_constructor():
    """
    We shouldn't touch/run object `__init__` during it unregistration.
    """

    class Foo(object):
        def __init__(self):
            raise Exception

    class Bar(Injector):
        foo = Foo

    del Bar.foo


# TODO: deny to remove let from injector
#
# TODO: hide dependencies library KeyError from stack trace
#
# TODO: raise exception if init argument have class as its default
# value and its name does not ends with _cls suffix.
#
# def __init__(self, x=CustomClass) - raise error
#
# def __init__(self, x_cls=CustomClass) - work as usual
#
# TODO: test case below
#
# class Container(Injector):
#     x = CustomClass
#     x_cls = x
#
# What spec should be stored in that case?
#
# TODO: Add decorator based container modification
#
# class Container(Injector):
#     pass
#
# @Container.as.foo
# class Foo:
#     def __init__(self, x, y):
#         self.x = x
#         self.y = y
#
# TODO: Lazy injection marker for nested containers.  For example we
# have host and port in Database constructor.  We have host and port
# in the Cache constructor.  It is nice to have the possibility use
# simple `host` and `port` arguments in each class and specify this as
# hierarchy in the injector.
