from inspect import isclass

import pytest
from dependencies import DependencyError, Injector
from dependencies.injector import use_doc
from helpers import CodeCollector


def test_lambda_dependency():
    """Inject lambda function."""

    class Foo(object):

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
    """
    Inject class.

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

    assert isclass(Bar.foo_cls)


def test_redefine_dependency():
    """
    We can redefine dependency by inheritance from the `Injector`
    subclass.
    """

    class Foo(object):

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
    """
    Use specified dependency for constructor keyword arguments if
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

        def do(self, x):
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


def test_omit_parent_link_in_dir_listing():
    """
    Don't show `__parent__` link in the `dir` output.  It is an
    implementation detail.
    """

    class Foo(Injector):

        class Bar(Injector):
            pass

    assert '__parent__' not in dir(Foo.Bar)


attribute_assignment = CodeCollector()


@attribute_assignment.parametrize
def test_deny_injector_changes(code):
    """Explicitly deny change of any kind on `Injector` and its subclasses."""

    with pytest.raises(DependencyError) as exc_info:
        code()

    assert str(exc_info.value) == "'Injector' modification is not allowed"


@attribute_assignment
def mvT9oyJdXhzh():
    """Attribute assignment."""

    class Container(Injector):
        pass

    Container.foo = 1


@attribute_assignment
def fXxRX4KFUc8q():
    """Direct assignmet to the `Injector`."""

    Injector.foo = 1


@attribute_assignment
def pHfF0rbEjCsV():
    """Let notation."""

    Container = Injector.let()
    Container.foo = 1


@attribute_assignment
def xhZaIhujf34t():
    """Delete attribute."""

    class Container(Injector):
        foo = 1

    del Container.foo


@attribute_assignment
def jShuBfttg97c():
    """Delete attribute let notation."""

    Container = Injector.let(foo=1)
    del Container.foo


@attribute_assignment
def tQeRzD5ZsyTm():
    """Delete attribute from `Injector` directly."""

    del Injector.let


# Register decorator.


def test_use_decorator_inject_class():
    """We must be allowed to register class with `use` decorator."""

    Container = Injector.let(x=1, y=2)

    @Container.use.foo
    class Foo(object):

        def __init__(self, x, y):
            self.x = x
            self.y = y

        def __call__(self):
            return self.x + self.y

    assert Container.foo() == 3


def test_use_decorator_inject_function():
    """We must be allowed to register function with `use` decorator."""

    class Foo(object):

        def __init__(self, func, x, y):
            self.func = func
            self.x = x
            self.y = y

        def __call__(self):
            return self.func(self.x, self.y)

    class Container(Injector):
        foo = Foo
        x = 1
        y = 2

    @Container.use.func
    def add(first, second):
        return first + second

    assert Container.foo() == 3


def test_use_decorator_nested_injector():
    """
    We can register dependencies with `use` decorator in the nested
    injectors.
    """

    class Foo(Injector):

        class Bar(Injector):
            pass

    @Foo.Bar.use.func
    def x():
        return 1

    assert Foo.Bar.func() == 1


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

        def do(self):
            return self.a + self.b

    assert x(1, 2) == 3
    assert Y(1, 2).do() == 3


def test_use_decorator_no_name_class():
    """
    We can use `use` decorator without specifying the name of the
    class dependency explicitly.
    """

    class Foo(object):

        def __init__(self, Bar):
            self.Bar = Bar

    class Container(Injector):
        foo = Foo

    @Container.use
    class Bar(object):
        pass

    assert isinstance(Container.foo.Bar, Bar)


def test_use_decorator_no_name_function():
    """
    We can use `use` decorator without specifying the name of the
    function dependency explicitly.
    """

    class Foo(object):

        def __init__(self, do):
            self.do = do

    class Container(Injector):
        foo = Foo

    @Container.use
    def do():
        pass

    assert Container.foo.do is do


# Nested injectors.


def test_nested_injectors():
    """
    It is possible to use `Injector` subclass as attribute in the
    another `Injector` subclass.
    """

    def do_x(a, b):
        return a + b

    def do_y(c, d):
        return c * d

    class Call(object):

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


# Docstrings.


def test_docstrings():
    """Check we can access all API entry points documentation."""

    assert Injector.__doc__ == """
Default dependencies specification DSL.

Classes inherited from this class may inject dependencies into classes
specified in it namespace.
"""
    assert Injector.let.__doc__ == (
        'Produce new Injector with some dependencies overwritten.')
    assert Injector.use.__doc__ == use_doc
    assert DependencyError.__doc__ == (
        'Broken dependencies configuration error.')

    class Foo(Injector):
        """New container."""
        pass

    assert Foo.__doc__ == 'New container.'


evaluate_classes = CodeCollector()


@evaluate_classes.parametrize
def test_evaluate_dependencies_once(code):
    """Evaluate each node in the dependencies graph once."""

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

    class Container(Injector):
        a = A
        b = B
        c = C
        d = D

    code(Container)


@evaluate_classes
def ea4367450e47(Container):
    """Each dependency evaluated once during injection."""

    x = Container.a
    assert x.b.d is x.c.d


@evaluate_classes
def dd91602f3455(Container):
    """We reevaluate each dependency for different injections."""

    assert Container.a.b.d is not Container.a.b.d
    assert Container.a.b.d is not Container.a.c.d


multiple_inheritance = CodeCollector()


@multiple_inheritance.parametrize
def test_multiple_inheritance(code):
    """We can mix injector together."""

    class Foo(object):
        pass

    class Bar(object):

        def __init__(self, foo):
            self.foo = foo

    class Baz(object):

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
def edf946cc6077(Foo, FooContainer, BarContainer, BazContainer):
    """Inheritance."""

    class Container(FooContainer, BarContainer, BazContainer):
        pass

    assert isinstance(Container.baz.bar.foo, Foo)


@multiple_inheritance
def efdc426cd096(Foo, FooContainer, BarContainer, BazContainer):
    """Inplace creation."""

    assert isinstance(
        (FooContainer & BarContainer & BazContainer).baz.bar.foo,
        Foo,
    )


inheritance_order = CodeCollector()


@inheritance_order.parametrize
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

    code(Container1, Container2, Container3)


@inheritance_order
def aa10c7747a1f(Container1, Container2, Container3):
    """Inheritance."""

    class Foo(Container1, Container2, Container3):
        pass

    assert Foo.x == 1


@inheritance_order
def e056e22f3fd5(Container1, Container2, Container3):
    """Inheritance with own attributes."""

    class Foo(Container1, Container2, Container3):
        x = 4

    assert Foo.x == 4


@inheritance_order
def d851e0414bdf(Container1, Container2, Container3):
    """Inplace creation."""

    assert (Container1 & Container2 & Container3).x == 1


subclasses_only = CodeCollector()


@subclasses_only.parametrize
def test_multiple_inheritance_deny_regular_classes(code):
    """
    We can't use classes in multiple inheritance which are not
    `Injector` subclasses.
    """

    class Foo(object):
        pass

    with pytest.raises(DependencyError) as exc_info:
        code(Foo)

    assert str(exc_info.value) == (
        'Multiple inheritance is allowed for Injector subclasses only')


@subclasses_only
def f1583394f1a6(Foo):
    """Inheritance."""

    class Bar(Injector, Foo):
        pass


@subclasses_only
def b51814725d07(Foo):
    """Inplace creation."""

    Injector & Foo


deny_magic_methods = CodeCollector()


@deny_magic_methods.parametrize
def test_deny_magic_methods_injection(code):
    """`Injector` doesn't accept magic methods."""

    with pytest.raises(DependencyError) as exc_info:
        code()

    assert str(exc_info.value) == 'Magic methods are not allowed'


@deny_magic_methods
def e78bf771747c():
    """Declarative injector."""

    class Bar(Injector):

        def __eq__(self, other):
            return False


@deny_magic_methods
def e34b88041f64():
    """Let notation."""

    class Foo(Injector):
        pass

    Foo.let(__eq__=lambda self, other: False)


@deny_magic_methods
def e83853c1eb18():
    """Use decorator."""

    Container = Injector.let()

    @Container.use.__eq__
    def eq(self, other):
        return False


attribute_error = CodeCollector()


@attribute_error.parametrize
def test_attribute_error(code):
    """Raise attribute error if we can't find dependency."""

    with pytest.raises(AttributeError) as exc_info:
        code()

    assert str(exc_info.value) in set([
        "'Foo' object has no attribute 'test'",
        "'Injector' object has no attribute 'test'",
    ])


@attribute_error
def c58b054bfcd0():
    """Declarative injector."""

    class Foo(Injector):
        pass

    Foo.test


@attribute_error
def f9c50c81e8c9():
    """Let notation."""

    Foo = Injector.let()

    Foo.test


@attribute_error
def e2f16596a652():
    """Let notation from subclass."""

    class Foo(Injector):
        pass

    Foo.let().test


@attribute_error
def c4e7ecf75167():
    """Keyword arguments in the constructor."""

    class Bar(object):

        def __init__(self, test, two=2):
            self.test = test
            self.two = two

    class Foo(Injector):
        bar = Bar

    Foo.bar


@attribute_error
def b57e0e5295e6():
    """Use decorator."""

    Container = Injector.let()

    @Container.use.bar
    class Bar(object):

        def __init__(self, test):
            pass

    Container.bar


circle_deps = CodeCollector()


@circle_deps.parametrize
def test_circle_dependencies(code):
    """
    Throw `DependencyError` if class needs a dependency named same as
    class.  `Summator.foo` will fail with maximum recursion depth.  So
    we need to raise exception before this attribute access.
    """

    class Foo(object):

        def __init__(self, foo):
            self.foo = foo

    with pytest.raises(DependencyError) as exc_info:
        code(Foo)

    assert str(exc_info.value) == (
        "'foo' is a circle dependency in the 'Foo' constructor")


@circle_deps
def a6d9c893a92e(Foo):
    """Declarative injector."""

    class Summator(Injector):
        foo = Foo

    Summator.foo


@circle_deps
def e4b38a38de7e(Foo):
    """Let notation."""

    Summator = Injector.let(foo=Foo)

    Summator.foo


@circle_deps
def cfbda7f1a2b5(Foo):
    """Use decorator."""

    Summator = Injector.let()

    @Summator.use.foo
    class Foo(object):

        def __init__(self, foo):
            self.foo = foo

    Summator.foo


complex_circle_deps = CodeCollector()


@complex_circle_deps.parametrize
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

    with pytest.raises(DependencyError) as exc_info:
        code(Foo, Bar)

    message = str(exc_info.value)
    assert message in set([
        "'foo' is a circle dependency in the 'Bar' constructor",
        "'bar' is a circle dependency in the 'Foo' constructor",
    ])


@complex_circle_deps
def dcbd4c90b473(Foo, Bar):
    """Declarative injector."""

    class Summator(Injector):
        foo = Foo
        bar = Bar

    Summator.foo


@complex_circle_deps
def d9c4e136c92c(Foo, Bar):
    """Declarative injector with inheritance."""

    class First(Injector):
        foo = Foo

    class Second(First):
        bar = Bar

    Second.foo


@complex_circle_deps
def b54832f696e9(Foo, Bar):
    """Let notation."""

    Summator = Injector.let(foo=Foo, bar=Bar)

    Summator.foo


@complex_circle_deps
def c039a81e8dce(Foo, Bar):
    """Let notation chain."""

    Summator = Injector.let(foo=Foo).let(bar=Bar)

    Summator.foo


@complex_circle_deps
def e6529e257d1c(Foo, Bar):
    """Use decorator."""

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


long_circle_deps = CodeCollector()


@long_circle_deps.parametrize
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

    with pytest.raises(DependencyError) as exc_info:
        code(Foo, Bar, Baz)

    message = str(exc_info.value)
    assert message in set([
        "'foo' is a circle dependency in the 'Baz' constructor",
        "'bar' is a circle dependency in the 'Foo' constructor",
        "'baz' is a circle dependency in the 'Bar' constructor",
    ])


@long_circle_deps
def d2b809c03bfa(Foo, Bar, Baz):
    """Declarative injector."""

    class Summator(Injector):
        foo = Foo
        bar = Bar
        baz = Baz

    Summator.foo


@long_circle_deps
def fc13db5b9fda(Foo, Bar, Baz):
    """Declarative injector with inheritance."""

    class First(Injector):
        foo = Foo

    class Second(First):
        bar = Bar
        baz = Baz

    Second.foo


@long_circle_deps
def c729e6952fee(Foo, Bar, Baz):
    """Let notation."""

    Summator = Injector.let(foo=Foo, bar=Bar, baz=Baz)

    Summator.foo


@long_circle_deps
def d701f88a5c42(Foo, Bar, Baz):
    """Let notation chain."""

    Summator = Injector.let(foo=Foo).let(bar=Bar).let(baz=Baz)

    Summator.foo


@long_circle_deps
def c1e1c2ec8941(Foo, Bar, Baz):
    """Use decorator."""

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


deny_varargs = CodeCollector()


@deny_varargs.parametrize
def test_deny_arbitrary_argument_list(code):
    """Raise `DependencyError` if constructor have *args argument."""

    class Foo(object):

        def __init__(self, *args):
            self.args = args

    with pytest.raises(DependencyError) as exc_info:
        code(Foo)

    message = str(exc_info.value)
    assert message == "Foo.__init__ have arbitrary argument list"


@deny_varargs
def dfe1c22c641e(Foo):
    """Declarative injector."""

    class Summator(Injector):
        foo = Foo
        args = (1, 2, 3)


@deny_varargs
def f7ef2aa82c18(Foo):
    """Let notation."""
    Injector.let(foo=Foo, args=(1, 2, 3))


@deny_varargs
def fad7d812b63c(Foo):
    """Use decorator."""

    Summator = Injector.let(args=(1, 2, 3))

    @Summator.use.foo
    class Foo(object):

        def __init__(self, *args):
            self.args = args


deny_kwargs = CodeCollector()


@deny_kwargs.parametrize
def test_deny_arbitrary_keyword_arguments(code):
    """Raise `DependencyError` if constructor have **kwargs argument."""

    class Foo(object):

        def __init__(self, **kwargs):
            self.kwargs = kwargs

    with pytest.raises(DependencyError) as exc_info:
        code(Foo)

    message = str(exc_info.value)
    assert message == "Foo.__init__ have arbitrary keyword arguments"


@deny_kwargs
def e281099be65d(Foo):
    """Declarative injector."""

    class Summator(Injector):
        foo = Foo
        kwargs = {'start': 5}


@deny_kwargs
def bcf7c5881b2c(Foo):
    """Let notation."""

    Injector.let(foo=Foo, kwargs={'start': 5})


@deny_kwargs
def ff760d162827(Foo):
    """Use decorator."""

    Summator = Injector.let(kwargs={'start': 5})

    @Summator.use.foo
    class Foo(object):

        def __init__(self, **kwargs):
            self.kwargs = kwargs


deny_varargs_kwargs = CodeCollector()


@deny_varargs_kwargs.parametrize
def test_deny_arbitrary_positional_and_keyword_arguments_together(code):
    """
    Raise `DependencyError` if constructor have *args and **kwargs
    argument.
    """

    class Foo(object):

        def __init__(self, *args, **kwargs):
            self.args = args
            self.kwargs = kwargs

    with pytest.raises(DependencyError) as exc_info:
        code(Foo)

    message = str(exc_info.value)
    assert message == (
        "Foo.__init__ have arbitrary argument list and keyword arguments")


@deny_varargs_kwargs
def efbf07f8deb6(Foo):
    """Declarative injector."""

    class Summator(Injector):
        foo = Foo
        args = (1, 2, 3)
        kwargs = {'start': 5}


@deny_varargs_kwargs
def c4362558f312(Foo):
    """Let notation."""

    Injector.let(foo=Foo, args=(1, 2, 3), kwargs={'start': 5})


@deny_varargs_kwargs
def ba95711532fe(Foo):
    """Use decorator."""

    Summator = Injector.let(args=(1, 2, 3), kwargs={'start': 5})

    @Summator.use.foo
    class Foo(object):

        def __init__(self, *args, **kwargs):
            self.args = args
            self.kwargs = kwargs


deny_let_redefine = CodeCollector()


@deny_let_redefine.parametrize
def test_deny_to_redefine_let_attribute(code):
    """We can't redefine let attribute in the `Injector` subclasses."""

    with pytest.raises(DependencyError) as exc_info:
        code()

    assert str(exc_info.value) == "'let' redefinition is not allowed"


@deny_let_redefine
def a2bfa842df0c():
    """Declarative injector."""

    class Foo(Injector):
        let = 2


@deny_let_redefine
def ddd392e70db6():
    """Let notation."""

    class Foo(Injector):
        pass

    Foo.let(let=1)


@deny_let_redefine
def bdbdb2e43217():
    """Use decorator."""

    Summator = Injector.let()

    @Summator.use.let
    def let(cls, **kwargs):
        pass


deny_use_redefine = CodeCollector()


@deny_use_redefine.parametrize
def test_deny_to_redefine_use_attribute(code):
    """We can't redefine `use` attribute in the `Injector` subclasses."""

    with pytest.raises(DependencyError) as exc_info:
        code()

    assert str(exc_info.value) == "'use' redefinition is not allowed"


@deny_use_redefine
def a91da8cbb9b6():
    """Declarative injector."""

    class Foo(Injector):
        use = 2


@deny_use_redefine
def a6d8c15385a8():
    """Let notation."""

    class Foo(Injector):
        pass

    Foo.let(use=1)


@deny_use_redefine
def db56096f19d6():
    """Use decorator."""

    Summator = Injector.let()

    @Summator.use.use
    def use():
        pass


deny_call = CodeCollector()


@deny_call.parametrize
def test_deny_to_instantiate_injector(code):
    """Deny injector instantiation."""

    with pytest.raises(DependencyError) as exc_info:
        code()

    assert str(exc_info.value) == 'Do not instantiate Injector'


@deny_call
def ce52d740af31():
    """Direct call."""

    Injector()


@deny_call
def a95940f44400():
    """Subclass call."""

    class Foo(Injector):
        pass

    Foo()


@deny_call
def d10b4ba474a9():
    """Ignore any arguments passed."""

    Injector(1)


@deny_call
def d665c722baae():
    """Ignore any keyword argument passed."""

    Injector(x=1)


cls_named_arguments = CodeCollector()


@cls_named_arguments.parametrize
def test_deny_classes_as_default_values(code):
    """
    If argument name doesn't ends with `_cls`, its default value can't
    be a class.
    """

    class Foo(object):
        pass

    class Bar(object):

        def __init__(self, foo=Foo):
            self.foo = foo

    with pytest.raises(DependencyError) as exc_info:
        code(Foo, Bar)

    message = str(exc_info.value)
    assert message == "'foo' argument can not have class as its default value"


@cls_named_arguments
def dad79637580d(Foo, Bar):
    """Declarative injector."""

    class Container(Injector):
        bar = Bar


@cls_named_arguments
def bccb4f621e70(Foo, Bar):
    """Let notation."""

    Injector.let(bar=Bar)


@cls_named_arguments
def f7f8e730d2a9(Foo, Bar):
    """Use decorator."""

    Container = Injector.let()

    @Container.use.bar
    class Bar(object):

        def __init__(self, foo=Foo):
            self.foo = foo


cls_named_defaults = CodeCollector()


@cls_named_defaults.parametrize
def test_deny_non_classes_in_cls_named_arguments(code):
    """
    If argument name ends with `_cls`, it must have a class as it
    default value.
    """

    class Bar(object):

        def __init__(self, foo_cls=1):
            self.foo_cls = foo_cls

    with pytest.raises(DependencyError) as exc_info:
        code(Bar)

    message = str(exc_info.value)
    assert message == "'foo_cls' default value should be a class"


@cls_named_defaults
def a8cd70341d3d(Bar):
    """Declarative injector."""

    class Container(Injector):
        bar = Bar


@cls_named_defaults
def b859e98f2913(Bar):
    """Let notation."""

    Injector.let(bar=Bar)


@cls_named_defaults
def b11a4f8ddac5(Bar):
    """Use decorator."""

    Container = Injector.let()

    @Container.use.bar
    class Bar(object):

        def __init__(self, foo_cls=1):
            self.foo_cls = foo_cls
