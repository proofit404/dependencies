import pytest

from dependencies import Injector
from dependencies.exceptions import DependencyError
from helpers import CodeCollector


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

    message = str(exc_info.value)
    assert message == "'foo' is a circular dependency in the 'Foo' constructor"


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
    assert message in {
        "'foo' is a circular dependency in the 'Bar' constructor",
        "'bar' is a circular dependency in the 'Foo' constructor",
    }


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
    assert message in {
        "'foo' is a circular dependency in the 'Baz' constructor",
        "'bar' is a circular dependency in the 'Foo' constructor",
        "'baz' is a circular dependency in the 'Bar' constructor",
    }


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
