import pytest

from dependencies import Injector
from dependencies import operation
from dependencies import Package
from dependencies import value
from dependencies.exceptions import DependencyError
from helpers import CodeCollector


# Simple circle.


circle_deps = CodeCollector()
circle_defs = CodeCollector("foo")


@circle_deps.parametrize
@circle_defs.parametrize
def test_circle_dependencies(code, foo):
    """Throw `DependencyError` if class needs a dependency named same as class.

    `Summator.foo` will fail with maximum recursion depth.  So we need
    to raise exception before this attribute access.
    """

    with pytest.raises(DependencyError) as exc_info:
        code(foo())

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


@circle_defs
def nQpangWPMths():
    """Class."""

    class Foo(object):
        def __init__(self, foo):
            pass  # pragma: no cover

    return Foo


@circle_defs
def gjhRaqkLmRmy():
    """Operation."""

    @operation
    def Foo(foo):
        pass  # pragma: no cover

    return Foo


@circle_defs
def kHqAxHovWKtI():
    """Value."""

    @value
    def Foo(foo):
        pass  # pragma: no cover

    return Foo


@circle_defs
def xoGkuXokhXpZ():
    """Package link to class."""

    pkg = Package("pkg")

    return pkg.circles.simple_class.Foo


@circle_defs
def xdKqGtGJWEbR():
    """Package link to operation."""

    pkg = Package("pkg")

    return pkg.circles.simple_operation.Foo


@circle_defs
def jIhFqCwKXFvv():
    """Package link to value."""

    pkg = Package("pkg")

    return pkg.circles.simple_value.Foo


# Complex circle.


complex_circle_deps = CodeCollector()
complex_circle_defs_foo = CodeCollector("foo")
complex_circle_defs_bar = CodeCollector("bar")


@complex_circle_deps.parametrize
@complex_circle_defs_foo.parametrize
@complex_circle_defs_bar.parametrize
def test_complex_circle_dependencies(code, foo, bar):
    """Throw `DependencyError` in the case of complex dependency recursion.

    One class define an argument in its constructor.  We have second
    class in the container named for this dependency.  This class define
    an argument in its constructor named like first class in the
    container.  We have mutual recursion in this case.
    """

    with pytest.raises(DependencyError) as exc_info:
        code(foo(), bar())

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


@complex_circle_defs_foo
def kodOTZfScpDc():
    """Class."""

    class Foo(object):
        def __init__(self, bar):
            pass  # pragma: no cover

    return Foo


@complex_circle_defs_foo
def tYEhWPObJRXZ():
    """Operation."""

    @operation
    def Foo(bar):
        pass  # pragma: no cover

    return Foo


@complex_circle_defs_foo
def zklaYlyBZsEj():
    """Value."""

    @value
    def Foo(bar):
        pass  # pragma: no cover

    return Foo


@complex_circle_defs_foo
def xPLfwwcZNyyX():
    """Package link to class."""

    pkg = Package("pkg")

    return pkg.circles.complex_class.Foo


@complex_circle_defs_foo
def nGROhaBTCNSO():
    """Package link to operation."""

    pkg = Package("pkg")

    return pkg.circles.complex_operation.Foo


@complex_circle_defs_foo
def fkedDYYeueXo():
    """Package link to value."""

    pkg = Package("pkg")

    return pkg.circles.complex_value.Foo


@complex_circle_defs_bar
def uEevbDxHVHfN():
    """Class."""

    class Bar(object):
        def __init__(self, foo):
            pass  # pragma: no cover

    return Bar


@complex_circle_defs_bar
def emGmGzXrbaZe():
    """Operation."""

    @operation
    def Bar(foo):
        pass  # pragma: no cover

    return Bar


@complex_circle_defs_bar
def aerRHoDXUNeV():
    """Value."""

    @value
    def Bar(foo):
        pass  # pragma: no cover

    return Bar


@complex_circle_defs_bar
def trvcvfPoOBEv():
    """Package link to class."""

    pkg = Package("pkg")

    return pkg.circles.complex_class.Bar


@complex_circle_defs_bar
def sHybukyZpyjf():
    """Package link to operation."""

    pkg = Package("pkg")

    return pkg.circles.complex_operation.Bar


@complex_circle_defs_bar
def lNsNBNCTHPFX():
    """Package link to value."""

    pkg = Package("pkg")

    return pkg.circles.complex_value.Bar


# Long circle.


long_circle_deps = CodeCollector()
long_circle_defs_foo = CodeCollector("foo")
long_circle_defs_bar = CodeCollector("bar")
long_circle_defs_baz = CodeCollector("baz")


@long_circle_deps.parametrize
@long_circle_defs_foo.parametrize
@long_circle_defs_bar.parametrize
@long_circle_defs_baz.parametrize
def test_complex_circle_dependencies_long_circle(code, foo, bar, baz):
    """Detect complex dependencies recursion with circles longer then two
    constructors."""

    with pytest.raises(DependencyError) as exc_info:
        code(foo(), bar(), baz())

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


@long_circle_defs_foo
def uVWBksfNYEDw():
    """Class."""

    class Foo(object):
        def __init__(self, bar):
            pass  # pragma: no cover

    return Foo


@long_circle_defs_foo
def yOscCQpEPstE():
    """Operation."""

    @operation
    def Foo(bar):
        pass  # pragma: no cover

    return Foo


@long_circle_defs_foo
def rwJmLRVuVSqm():
    """Value."""

    @value
    def Foo(bar):
        pass  # pragma: no cover

    return Foo


@long_circle_defs_foo
def zAYYjvSPmIhZ():
    """Package link to class."""

    pkg = Package("pkg")

    return pkg.circles.long_class.Foo


@long_circle_defs_foo
def xreTaLNoZeDz():
    """Package link to operation."""

    pkg = Package("pkg")

    return pkg.circles.long_operation.Foo


@long_circle_defs_foo
def qOKmbpOgeDhk():
    """Package link to value."""

    pkg = Package("pkg")

    return pkg.circles.long_value.Foo


@long_circle_defs_bar
def oKtHawDksDNk():
    """Class."""

    class Bar(object):
        def __init__(self, baz):
            pass  # pragma: no cover

    return Bar


@long_circle_defs_bar
def hpRbxUtEWyGJ():
    """Operation."""

    @operation
    def Bar(baz):
        pass  # pragma: no cover

    return Bar


@long_circle_defs_bar
def mLsXYSzlYPRO():
    """Value."""

    @value
    def Bar(baz):
        pass  # pragma: no cover

    return Bar


@long_circle_defs_bar
def pYMumhKUCBUy():
    """Package link to class."""

    pkg = Package("pkg")

    return pkg.circles.long_class.Bar


@long_circle_defs_bar
def lCQgCPevBZXs():
    """Package link to operation."""

    pkg = Package("pkg")

    return pkg.circles.long_operation.Bar


@long_circle_defs_bar
def xgyyAISoreQV():
    """Package link to value."""

    pkg = Package("pkg")

    return pkg.circles.long_value.Bar


@long_circle_defs_baz
def uaOWixpAMVma():
    """Class."""

    class Baz(object):
        def __init__(self, foo):
            pass  # pragma: no cover

    return Baz


@long_circle_defs_baz
def fvMICnYvGZlw():
    """Operation."""

    @operation
    def Baz(foo):
        pass  # pragma: no cover

    return Baz


@long_circle_defs_baz
def xjpTxDebbpnm():
    """Value."""

    @value
    def Baz(foo):
        pass  # pragma: no cover

    return Baz


@long_circle_defs_baz
def ydSPPkZGDwPJ():
    """Package link to class."""

    pkg = Package("pkg")

    return pkg.circles.long_class.Baz


@long_circle_defs_baz
def rxFZQwocGmhN():
    """Package link to operation."""

    pkg = Package("pkg")

    return pkg.circles.long_operation.Baz


@long_circle_defs_baz
def eFMMMVDBKCFU():
    """Package link to value."""

    pkg = Package("pkg")

    return pkg.circles.long_value.Baz
