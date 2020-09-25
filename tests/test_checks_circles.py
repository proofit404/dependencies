"""Tests related to the circle detection in the injector definitions."""
import pytest

from dependencies import Injector
from dependencies import operation
from dependencies import Package
from dependencies import value
from dependencies.exceptions import DependencyError
from helpers import CodeCollector


circle_deps = CodeCollector()
circle_defs = CodeCollector("foo")


@circle_deps.parametrize
@circle_defs.parametrize
def test_circle_dependencies(code, foo):
    """Throw `DependencyError` if class needs a dependency named same as class.

    `Summator.foo` will fail with maximum recursion depth.

    So we need to raise exception before this attribute access.

    """
    with pytest.raises(DependencyError) as exc_info:
        code(foo())

    message = str(exc_info.value)
    assert message == "'foo' is a circular dependency in the 'Foo' constructor"


@circle_deps
def _a6d9c893a92e(Foo):
    class Summator(Injector):
        foo = Foo

    Summator.foo


@circle_deps
def _e4b38a38de7e(Foo):
    Summator = Injector(foo=Foo)

    Summator.foo


@circle_defs
def _nQpangWPMths():
    class Foo:
        def __init__(self, foo):
            pass  # pragma: no cover

    return Foo


@circle_defs
def _gjhRaqkLmRmy():
    @operation
    def Foo(foo):
        pass  # pragma: no cover

    return Foo


@circle_defs
def _kHqAxHovWKtI():
    @value
    def Foo(foo):
        pass  # pragma: no cover

    return Foo


@circle_defs
def _xoGkuXokhXpZ():
    pkg = Package("pkg")

    return pkg.circles.simple_class.Foo


@circle_defs
def _xdKqGtGJWEbR():
    pkg = Package("pkg")

    return pkg.circles.simple_operation.Foo


@circle_defs
def _jIhFqCwKXFvv():
    pkg = Package("pkg")

    return pkg.circles.simple_value.Foo


complex_circle_deps = CodeCollector()
complex_circle_defs_foo = CodeCollector("foo")
complex_circle_defs_bar = CodeCollector("bar")


@complex_circle_deps.parametrize
@complex_circle_defs_foo.parametrize
@complex_circle_defs_bar.parametrize
def test_complex_circle_dependencies(code, foo, bar):
    """Throw `DependencyError` in the case of complex dependency recursion.

    One class define an argument in its constructor.  We have second class in the
    container named for this dependency.  This class define an argument in its
    constructor named like first class in the container.  We have mutual recursion in
    this case.

    """
    with pytest.raises(DependencyError) as exc_info:
        code(foo(), bar())

    message = str(exc_info.value)
    assert message in {
        "'foo' is a circular dependency in the 'Bar' constructor",
        "'bar' is a circular dependency in the 'Foo' constructor",
    }


@complex_circle_deps
def _dcbd4c90b473(Foo, Bar):
    class Summator(Injector):
        foo = Foo
        bar = Bar

    Summator.foo


@complex_circle_deps
def _d9c4e136c92c(Foo, Bar):
    class First(Injector):
        foo = Foo

    class Second(First):
        bar = Bar

    Second.foo


@complex_circle_deps
def _b54832f696e9(Foo, Bar):
    Summator = Injector(foo=Foo, bar=Bar)

    Summator.foo


@complex_circle_deps
def _c039a81e8dce(Foo, Bar):
    Summator = Injector(foo=Foo)(bar=Bar)

    Summator.foo


@complex_circle_defs_foo
def _kodOTZfScpDc():
    class Foo:
        def __init__(self, bar):
            pass  # pragma: no cover

    return Foo


@complex_circle_defs_foo
def _tYEhWPObJRXZ():
    @operation
    def Foo(bar):
        pass  # pragma: no cover

    return Foo


@complex_circle_defs_foo
def _zklaYlyBZsEj():
    @value
    def Foo(bar):
        pass  # pragma: no cover

    return Foo


@complex_circle_defs_foo
def _xPLfwwcZNyyX():
    pkg = Package("pkg")

    return pkg.circles.complex_class.Foo


@complex_circle_defs_foo
def _nGROhaBTCNSO():
    pkg = Package("pkg")

    return pkg.circles.complex_operation.Foo


@complex_circle_defs_foo
def _fkedDYYeueXo():
    pkg = Package("pkg")

    return pkg.circles.complex_value.Foo


@complex_circle_defs_bar
def _uEevbDxHVHfN():
    class Bar:
        def __init__(self, foo):
            pass  # pragma: no cover

    return Bar


@complex_circle_defs_bar
def _emGmGzXrbaZe():
    @operation
    def Bar(foo):
        pass  # pragma: no cover

    return Bar


@complex_circle_defs_bar
def _aerRHoDXUNeV():
    @value
    def Bar(foo):
        pass  # pragma: no cover

    return Bar


@complex_circle_defs_bar
def _trvcvfPoOBEv():
    pkg = Package("pkg")

    return pkg.circles.complex_class.Bar


@complex_circle_defs_bar
def _sHybukyZpyjf():
    pkg = Package("pkg")

    return pkg.circles.complex_operation.Bar


@complex_circle_defs_bar
def _lNsNBNCTHPFX():
    pkg = Package("pkg")

    return pkg.circles.complex_value.Bar


long_circle_deps = CodeCollector()
long_circle_defs_foo = CodeCollector("foo")
long_circle_defs_bar = CodeCollector("bar")
long_circle_defs_baz = CodeCollector("baz")


@long_circle_deps.parametrize
@long_circle_defs_foo.parametrize
@long_circle_defs_bar.parametrize
@long_circle_defs_baz.parametrize
def test_complex_circle_dependencies_long_circle(code, foo, bar, baz):
    """Verify circle dependencies in complex object graph.

    Detect complex dependencies recursion with circles longer then two constructors.

    """
    with pytest.raises(DependencyError) as exc_info:
        code(foo(), bar(), baz())

    message = str(exc_info.value)
    assert message in {
        "'foo' is a circular dependency in the 'Baz' constructor",
        "'bar' is a circular dependency in the 'Foo' constructor",
        "'baz' is a circular dependency in the 'Bar' constructor",
    }


@long_circle_deps
def _d2b809c03bfa(Foo, Bar, Baz):
    class Summator(Injector):
        foo = Foo
        bar = Bar
        baz = Baz

    Summator.foo


@long_circle_deps
def _fc13db5b9fda(Foo, Bar, Baz):
    class First(Injector):
        foo = Foo

    class Second(First):
        bar = Bar
        baz = Baz

    Second.foo


@long_circle_deps
def _c729e6952fee(Foo, Bar, Baz):
    Summator = Injector(foo=Foo, bar=Bar, baz=Baz)

    Summator.foo


@long_circle_deps
def _d701f88a5c42(Foo, Bar, Baz):
    Summator = Injector(foo=Foo)(bar=Bar)(baz=Baz)

    Summator.foo


@long_circle_defs_foo
def _uVWBksfNYEDw():
    class Foo:
        def __init__(self, bar):
            pass  # pragma: no cover

    return Foo


@long_circle_defs_foo
def _yOscCQpEPstE():
    @operation
    def Foo(bar):
        pass  # pragma: no cover

    return Foo


@long_circle_defs_foo
def _rwJmLRVuVSqm():
    @value
    def Foo(bar):
        pass  # pragma: no cover

    return Foo


@long_circle_defs_foo
def _zAYYjvSPmIhZ():
    pkg = Package("pkg")

    return pkg.circles.long_class.Foo


@long_circle_defs_foo
def _xreTaLNoZeDz():
    pkg = Package("pkg")

    return pkg.circles.long_operation.Foo


@long_circle_defs_foo
def _qOKmbpOgeDhk():
    pkg = Package("pkg")

    return pkg.circles.long_value.Foo


@long_circle_defs_bar
def _oKtHawDksDNk():
    class Bar:
        def __init__(self, baz):
            pass  # pragma: no cover

    return Bar


@long_circle_defs_bar
def _hpRbxUtEWyGJ():
    @operation
    def Bar(baz):
        pass  # pragma: no cover

    return Bar


@long_circle_defs_bar
def _mLsXYSzlYPRO():
    @value
    def Bar(baz):
        pass  # pragma: no cover

    return Bar


@long_circle_defs_bar
def _pYMumhKUCBUy():
    pkg = Package("pkg")

    return pkg.circles.long_class.Bar


@long_circle_defs_bar
def _lCQgCPevBZXs():
    pkg = Package("pkg")

    return pkg.circles.long_operation.Bar


@long_circle_defs_bar
def _xgyyAISoreQV():
    pkg = Package("pkg")

    return pkg.circles.long_value.Bar


@long_circle_defs_baz
def _uaOWixpAMVma():
    class Baz:
        def __init__(self, foo):
            pass  # pragma: no cover

    return Baz


@long_circle_defs_baz
def _fvMICnYvGZlw():
    @operation
    def Baz(foo):
        pass  # pragma: no cover

    return Baz


@long_circle_defs_baz
def _xjpTxDebbpnm():
    @value
    def Baz(foo):
        pass  # pragma: no cover

    return Baz


@long_circle_defs_baz
def _ydSPPkZGDwPJ():
    pkg = Package("pkg")

    return pkg.circles.long_class.Baz


@long_circle_defs_baz
def _rxFZQwocGmhN():
    pkg = Package("pkg")

    return pkg.circles.long_operation.Baz


@long_circle_defs_baz
def _eFMMMVDBKCFU():
    pkg = Package("pkg")

    return pkg.circles.long_value.Baz
