"""Dependencies test suite."""

import inspect
from textwrap import dedent

import pytest

from dependencies import Injector, attribute, item, DependencyError, use_doc


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
        def do(self):  # noqa: E301
            return self.x + self.y + self.z

    class Container(Injector):
        foo = Foo
        x = 5
        z = 1

    assert Container.foo.do() == 7


def test_cls_named_argument_default_value():
    """
    Allow classes as default argument values if argument name ends
    with `_cls`.
    """

    class Foo(object):
        pass

    class Bar(object):
        def __init__(self, foo_cls=Foo):
            self.foo_cls = foo_cls

    class Container(Injector):
        bar = Bar

    assert Container.bar.foo_cls is Foo


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


# Let notation.


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


# Dir.


def test_show_common_class_attributes_with_dir():
    """`dir` show common class attributes."""

    class Common(object):
        pass

    class Foo(Injector):
        pass

    assert dir(Common) + ['let', 'use'] == dir(Foo)


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


# Attribute assignment.


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


# Register decorator.


def test_use_decorator_inject_class():
    """We must be allowed to register class with `use` decorator."""

    Container = Injector.let(x=1, y=2)

    @Container.use.foo
    class Foo(object):
        def __init__(self, x, y):
            self.x = x
            self.y = y
        def __call__(self):  # noqa: E301
            return self.x + self.y

    assert Container.foo() == 3


def test_use_decorator_inject_function():
    """We must be allowed to register function with `use` decorator."""

    class Foo(object):
        def __init__(self, func, x, y):
            self.func = func
            self.x = x
            self.y = y
        def __call__(self):  # noqa: E301
            return self.func(self.x, self.y)

    class Container(Injector):
        foo = Foo
        x = 1
        y = 2

    @Container.use.func
    def add(first, second):
        return first + second

    assert Container.foo() == 3


def test_use_decorator_keep_argument():
    """
    Decorated class of function remains unmodified and we can use it
    as usual.
    """

    Container = Injector.let()

    @Container.use.foo
    def x(a, b):
        return a + b

    @Container.use.bar
    class Y(object):
        def __init__(self, a, b):
            self.a = a
            self.b = b
        def do(self):  # noqa: E301
            return self.a + self.b

    assert x(1, 2) == 3
    assert Y(1, 2).do() == 3


# Nested injectors.


def test_nested_injectors():
    """
    It is possible to use `Injector` subclass as attribute in the
    another `Injector` subclass.
    """

    def do_x(a, b): return a + b

    def do_y(c, d): return c * d

    class Call(object):
        def __init__(self, foo, bar):
            self.foo = foo
            self.bar = bar
        def __call__(self, one, two, three):  # noqa: E301
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


# Docstrings.


def test_docstrings():
    """Check we can access all API entry points documentation."""

    assert Injector.__doc__ == """
    Default dependencies specification DSL.

    Classes inherited from this class may inject dependencies into
    classes specified in it namespace.
    """
    assert Injector.let.__doc__ == (
        'Produce new Injector with some dependencies overwritten.'
    )
    assert Injector.use.__doc__ == use_doc
    assert DependencyError.__doc__ == (
        'Broken dependencies configuration error.'
    )

    class Foo(Injector):
        """New container."""
        pass

    assert Foo.__doc__ == 'New container.'


# Evaluate classes once.


@pytest.mark.parametrize('code', [
    # Each dependency evaluated once during injection.
    """
    class Container(Injector):
        a = A
        b = B
        c = C
        d = D

    x = Container.a
    assert x.b.d is x.c.d
    """,
    # We reevaluate each dependency for different injections.
    """
    class Container(Injector):
        a = A
        b = B
        c = C
        d = D

    assert Container.a.b.d is not Container.a.b.d
    assert Container.a.b.d is not Container.a.c.d
    """,
])
def test_evaluate_dependencies_once(code):
    """
    Evaluate each node in the dependencies graph once.

    For some reason we can't pass `Container` class into exec scope on
    Python2.6, because of some reference error.
    """

    class A(object):
        def __init__(self, b, c):
            self.b = b
            self.c = c

    class B(object):
        def __init__(self, d):
            self.d = d

    class C(object):
        def __init__(self, d):
            self.d = d

    class D(object):
        pass

    scope = {'Injector': Injector, 'A': A, 'B': B, 'C': C, 'D': D}

    exec(dedent(code), scope)


# Multiple inheritance.


@pytest.mark.parametrize('code', [
    # Inheritance.
    """
    class FooContainer(Injector):
        foo = Foo

    class BarContainer(Injector):
        bar = Bar

    class BazContainer(Injector):
        baz = Baz

    class Container(FooContainer, BarContainer, BazContainer):
        pass

    assert isinstance(Container.baz.bar.foo, Foo)
    """,
    # Inplace creation.
    """
    class FooContainer(Injector):
        foo = Foo

    class BarContainer(Injector):
        bar = Bar

    class BazContainer(Injector):
        baz = Baz

    assert isinstance(
        (FooContainer & BarContainer & BazContainer).baz.bar.foo,
        Foo,
    )
    """,
])
def test_multiple_inheritance(code):
    """
    We can mix injector together.

    We can't define injectors inside test function because of Python2.6
    """

    class Foo(object):
        pass

    class Bar(object):
        def __init__(self, foo):
            self.foo = foo

    class Baz(object):
        def __init__(self, bar):
            self.bar = bar

    scope = {'Injector': Injector, 'Foo': Foo, 'Bar': Bar, 'Baz': Baz}

    exec(dedent(code), scope)


@pytest.mark.parametrize('code', [
    # Inheritance.
    """
    class Foo(Container1, Container2, Container3):
        pass

    assert Foo.x == 1
    """,
    # Inheritance with own attributes.
    """
    class Foo(Container1, Container2, Container3):
        x = 4

    assert Foo.x == 4
    """,
    # Inplace creation.
    """
    assert (Container1 & Container2 & Container3).x == 1
    """,
])
def test_multiple_inheritance_injectors_order(code):
    """
    `Injector` which comes first in the subclass bases or inplace
    creation must have higher precedence.
    """

    class Container1(Injector):
        x = 1

    class Container2(Injector):
        x = 2

    class Container3(Injector):
        x = 3

    scope = {
        'Container1': Container1,
        'Container2': Container2,
        'Container3': Container3,
    }

    exec(dedent(code), scope)


@pytest.mark.parametrize('code', [
    # Inheritance.
    """
    class Foo(Injector, Foo):
        pass
    """,
    # Inplace creation.
    """
    Injector & Foo
    """,
])
def test_multiple_inheritance_deny_regular_classes(code):
    """
    We can't use classes in multiple inheritance which are not
    `Injector` subclasses.
    """

    class Foo(object):
        pass

    scope = {'Injector': Injector, 'Foo': Foo}

    with pytest.raises(DependencyError) as exc_info:
        exec(dedent(code), scope)

    assert str(exc_info.value) == (
        'Multiple inheritance is allowed for Injector subclasses only'
    )


# Deny magic methods.


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
    # Delete attribute.
    """
    class Foo(Injector):
        pass

    del Foo.__init__
    """,
    # Use decorator.
    """
    Container = Injector.let()

    @Container.use.__eq__
    def eq(self, other):
        return False
    """,
])
def test_deny_magic_methods_injection(code):
    """`Injector` doesn't accept magic methods."""

    scope = {'Injector': Injector}

    with pytest.raises(DependencyError) as exc_info:
        exec(dedent(code), scope)

    assert str(exc_info.value) == 'Magic methods are not allowed'


# Raise `AttributeError`.


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
    # Use decorator.
    """
    Container = Injector.let()

    @Container.use.bar
    class Bar(object):
        def __init__(self, test):
            pass

    Container.bar
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


# Resolve circle dependencies.


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
    # Use decorator.
    """
    Summator = Injector.let()

    @Summator.use.foo
    class Foo(object):
        def __init__(self, foo):
            self.foo = foo

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

    assert str(exc_info.value) == (
        "'foo' is a circle dependency in the 'Foo' constructor"
    )


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
    # Use decorator.
    """
    Summator = Injector.let()

    @Summator.use.foo
    class Foo(object):
        def __init__(self, bar):
            self.bar = bar

    @Summator.use.bar
    class Bar(object):
        def __init__(self, foo):
            self.foo = foo

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
    assert message in set([
        "'foo' is a circle dependency in the 'Bar' constructor",
        "'bar' is a circle dependency in the 'Foo' constructor",
    ])


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
    # Use decorator.
    """
    Summator = Injector.let()

    @Summator.use.foo
    class Foo(object):
        def __init__(self, bar):
            self.bar = bar

    @Summator.use.bar
    class Bar(object):
        def __init__(self, baz):
            self.baz = baz

    @Summator.use.baz
    class Baz(object):
        def __init__(self, foo):
            self.foo = foo

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
    assert message in set([
        "'foo' is a circle dependency in the 'Baz' constructor",
        "'bar' is a circle dependency in the 'Foo' constructor",
        "'baz' is a circle dependency in the 'Bar' constructor",
    ])


# Deny arbitrary arguments in the injectable constructor.


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
    # Use decorator.
    """
    Summator = Injector.let(args=(1, 2, 3))

    @Summator.use.foo
    class Foo(object):
        def __init__(self, *args):
            self.args = args
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

    message = str(exc_info.value)
    assert message == "Foo.__init__ have arbitrary argument list"


@pytest.mark.parametrize('code', [
    # Declarative injector.
    """
    class Summator(Injector):
        foo = Foo
        kwargs = {'start': 5}
    """,
    # Let notation.
    """
    Injector.let(foo=Foo, kwargs={'start': 5})
    """,
    # Attribute assignment.
    """
    class Summator(Injector):
        kwargs = {'start': 5}

    Summator.foo = Foo
    """,
    # Use decorator.
    """
    Summator = Injector.let(kwargs={'start': 5})

    @Summator.use.foo
    class Foo(object):
        def __init__(self, **kwargs):
            self.args = args
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

    message = str(exc_info.value)
    assert message == "Foo.__init__ have arbitrary keyword arguments"


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
    # Use decorator.
    """
    Summator = Injector.let(args=(1, 2, 3), kwargs={'start': 5})

    @Summator.use.foo
    class Foo(object):
        def __init__(self, *args, **kwargs):
            self.args = args
            self.kwargs = kwargs
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

    message = str(exc_info.value)
    assert message == (
        "Foo.__init__ have arbitrary argument list and keyword arguments"
    )


# Deny to redefine let factory.


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
    # Delete attribute.
    """
    del Injector.let
    """,
    # Use decorator.
    """
    Summator = Injector.let()

    @Summator.use.let
    def let(cls, **kwargs):
        pass
    """,
])
def test_deny_to_redefine_let_attribute(code):
    """We can't redefine let attribute in the `Injector` subclasses."""

    scope = {'Injector': Injector}

    with pytest.raises(DependencyError) as exc_info:
        exec(dedent(code), scope)

    assert str(exc_info.value) == "'let' redefinition is not allowed"


# Deny to redefine use attribute.


@pytest.mark.parametrize('code', [
    # Declarative injector.
    """
    class Foo(Injector):
        use = 2
    """,
    # Let notation.
    """
    class Foo(Injector):
        pass

    Foo.let(use=1)
    """,
    # Attribute assignment.
    """
    class Foo(Injector):
        pass

    Foo.use = 2
    """,
    # Delete attribute.
    """
    del Injector.use
    """,
    # Use decorator.
    """
    Summator = Injector.let()

    @Summator.use.use
    def use():
        pass
    """,
])
def test_deny_to_redefine_use_attribute(code):
    """We can't redefine `use` attribute in the `Injector` subclasses."""

    scope = {'Injector': Injector}

    with pytest.raises(DependencyError) as exc_info:
        exec(dedent(code), scope)

    assert str(exc_info.value) == "'use' redefinition is not allowed"


# Deny `Injector` call.


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


# `_cls` named arguments values.


@pytest.mark.parametrize('code', [
    # Declarative injector.
    """
    class Bar(object):
        def __init__(self, foo=Foo):
            self.foo = foo

    class Container(Injector):
        bar = Bar
    """,
    # Let notation.
    """
    class Bar(object):
        def __init__(self, foo=Foo):
            self.foo = foo

    Injector.let(bar=Bar)
    """,
    # Attribute assignment.
    """
    class Bar(object):
        def __init__(self, foo=Foo):
            self.foo = foo

    Container = Injector.let()

    Container.bar = Bar
    """,
    # Use decorator.
    """
    Container = Injector.let()

    @Container.use.bar
    class Bar(object):
        def __init__(self, foo=Foo):
            self.foo = foo
    """,
])
def test_deny_classes_as_default_values(code):
    """
    If argument name doesn't ends with `_cls`, its default value can't
    be a class.

    For some reason python 2.6 can not pass `Bar` class into `exec`
    function and fails with `SyntaxError`.  This occurs because we
    have `Foo` class as default value for keyword argument.  Python
    2.6 can't handle such scope manipulation.  We need to duplicate
    `Bar` class definition above for that reason.
    """

    class Foo(object):
        pass

    scope = {'Injector': Injector, 'Foo': Foo}

    with pytest.raises(DependencyError) as exc_info:
        exec(dedent(code), scope)

    message = str(exc_info.value)
    assert message == "'foo' argument can not have class as its default value"


@pytest.mark.parametrize('code', [
    # Declarative injector.
    """
    class Container(Injector):
        bar = Bar
    """,
    # Let notation.
    """
    Injector.let(bar=Bar)
    """,
    # Attribute assignment.
    """
    Container = Injector.let()

    Container.bar = Bar
    """,
    # Use decorator.
    """
    Container = Injector.let()

    @Container.use.bar
    class Bar(object):
        def __init__(self, foo_cls=1):
            self.foo_cls = foo_cls
    """,
])
def test_deny_non_classes_in_cls_named_arguments(code):
    """
    If argument name ends with `_cls`, it must have a class as it
    default value.
    """

    class Bar(object):
        def __init__(self, foo_cls=1):
            self.foo_cls = foo_cls

    scope = {'Injector': Injector, 'Bar': Bar}

    with pytest.raises(DependencyError) as exc_info:
        exec(dedent(code), scope)

    message = str(exc_info.value)
    assert message == "'foo_cls' default value should be a class"


# Declarative attribute access.


def test_attribute_getter():
    """
    We can describe attribute access in the `Injector` in declarative
    manner.
    """

    class Foo(object):
        def __init__(self, one, two):
            self.one = one
            self.two = two
        def do(self):  # noqa: E301
            return self.one + self.two

    class Container(Injector):
        class SubContainer(Injector):
            foo = Foo
            one = 1
            two = 2
        foo = attribute('SubContainer', 'foo')

    foo = Container.foo
    assert isinstance(foo, Foo)
    assert foo.do() == 3


@pytest.mark.parametrize('code', [
    # Declarative injector.
    """
    class Container(Injector):
        foo = 1

        class SubContainer(Injector):
            bar = attribute('..', 'foo')
    """,
    # Let notation.
    """
    class OuterContainer(Injector):
        foo = 1

    class SubContainer(Injector):
        bar = attribute('..', 'foo')

    Container = OuterContainer.let(SubContainer=SubContainer)
    """,
    # Attribute assignment.
    """
    class Container(Injector):
        foo = 1

    class SubContainer(Injector):
        bar = attribute('..', 'foo')

    Container.SubContainer = SubContainer
    """,
    # Use decorator.
    """
    class Container(Injector):
        foo = 1

    @Container.use.SubContainer
    class SubContainer(Injector):
        bar = attribute('..', 'foo')
    """,
])
def test_attribute_getter_parent_access(code):
    """We can access attribute of outer container."""

    scope = {'Injector': Injector, 'attribute': attribute}
    exec(dedent(code), scope)
    Container = scope['Container']
    assert Container.SubContainer.bar == 1


def test_attribute_getter_few_attributes():
    """
    We resolve attribute access until we find all specified
    attributes.
    """

    class Foo(object):
        def __init__(self, one):
            self.one = one

    class Container(Injector):
        class SubContainer(Injector):
            foo = Foo
            one = 1
        foo = attribute('SubContainer', 'foo', 'one')

    assert Container.foo == 1


def test_attribute_getter_no_attributes():
    """User can't specify empty attributes chain."""

    with pytest.raises(DependencyError) as exc_info:
        attribute('foo')

    message = str(exc_info.value)
    assert message == "'attrs' argument can not be empty"


# Declarative item access.


def test_item_getter():
    """
    We can describe item access in the `Injector` in the
    declarative manner.
    """

    class Container(Injector):
        foo = {'one': 1}
        one = item('foo', 'one')

    assert Container.one == 1


def test_item_getter_few_items():
    """
    We resolve nested items until we find all specified item.
    """

    class Container(Injector):
        foo = {'one': {'two': 2}}
        two = item('foo', 'one', 'two')

    assert Container.two == 2


def test_item_getter_no_items():
    """User can't specify empty items chain."""

    with pytest.raises(DependencyError) as exc_info:
        item('foo')

    message = str(exc_info.value)
    assert message == "'items' argument can not be empty"
