"""Tests related to the loops detection in the injector definition."""
from itertools import product

import pytest

from dependencies import Injector
from dependencies import Package
from dependencies import this
from dependencies.exceptions import DependencyError
from helpers import CodeCollector


flat_injector = CodeCollector()


@flat_injector.parametrize
def test_circle_links(code):
    """We can detect link loops in the same container without hierarchy."""
    with pytest.raises(DependencyError) as exc_info:
        code()

    assert str(exc_info.value) in (
        f"{a!r} is a circle link in the {b!r} injector"
        for a, b in product(["foo", "bar", "baz"], ["Container", "Injector"])
    )


@flat_injector
def _kSSnnkw6CNPx():
    class Container(Injector):
        foo = this.foo

    Container.foo  # pragma: no cover


@flat_injector
def _n8NHZqiZN43Q():
    Injector(foo=this.foo).foo


@flat_injector
def _ai0hNOPGX2PI():
    class Container(Injector):
        foo = this.bar
        bar = this.foo

    Container.foo  # pragma: no cover


@flat_injector
def _ySnRrxW6M79T():
    Injector(foo=this.bar, bar=this.foo).foo


@flat_injector
def _yfTnHHhvBmrQ():
    class Container(Injector):
        foo = this.bar
        bar = this.baz
        baz = this.foo

    Container.foo  # pragma: no cover


@flat_injector
def _ydZEbpRNlHEO():
    Injector(foo=this.bar, bar=this.baz, baz=this.foo).foo


one_level = CodeCollector()
subcontainer = CodeCollector("sub")


@one_level.parametrize
@subcontainer.parametrize
def test_circle_links_one_level(code, sub):
    """We can detect link loops in nested injectors one level deep."""
    with pytest.raises(DependencyError) as exc_info:
        code(sub())

    assert str(exc_info.value) in (
        f"{a!r} is a circle link in the {b!r} injector"
        for a, b in product(["foo", "bar"], ["Container", "Injector"])
    )


@one_level
def _eaK6IxW88SNh(sub):
    class Container(Injector):
        foo = this.SubContainer.bar
        SubContainer = sub

    Container.foo


@one_level
def _nWhKtJb16yg6(sub):
    Injector(foo=this.SubContainer.bar, SubContainer=sub).foo


@subcontainer
def _jijKOYgyZHNz():
    class SubContainer(Injector):
        bar = (this << 1).foo

    return SubContainer


@subcontainer
def _nFibPCOxGsrX():
    return Injector(bar=(this << 1).foo)


@subcontainer
def _utUTZLLngouR():
    examples = Package("examples")

    return examples.injected.SubContainer


complex_two_levels = CodeCollector()
complex_middle_container = CodeCollector("middle")
complex_lowest_container = CodeCollector("lowest")


@complex_two_levels.parametrize
@complex_middle_container.parametrize
@complex_lowest_container.parametrize
def test_circle_links_two_level_complex_loop(code, middle, lowest):
    """Search for dependency loop errors in the complex object graph.

    We can detect link loops in nested injectors two level deep without intermediate
    links.

    """
    with pytest.raises(DependencyError) as exc_info:
        code(middle(lowest()))

    assert str(exc_info.value) in (
        f"{a!r} is a circle link in the {b!r} injector"
        for a, b in product(["foo", "bar"], ["Container", "SubContainer", "Injector"])
    )


@complex_two_levels
def _mF4akoHlg84C(middle):
    class Container(Injector):
        foo = this.SubContainer.SubSubContainer.bar
        SubContainer = middle

    Container.foo


@complex_two_levels
def _bCw8LPUeVK6J(middle):
    Injector(foo=this.SubContainer.SubSubContainer.bar, SubContainer=middle).foo


@complex_middle_container
def _yPFeGKPGXPIY(lowest):
    class SubContainer(Injector):
        SubSubContainer = lowest

    return SubContainer


@complex_middle_container
def _uIRpkBWARVOQ(lowest):
    return Injector(SubSubContainer=lowest)


@complex_lowest_container
def _bJmCQECfcIzZ():
    class SubSubContainer(Injector):
        bar = (this << 2).foo

    return SubSubContainer


@complex_lowest_container
def _qzYMsyvxYFLe():
    return Injector(bar=(this << 2).foo)


@complex_lowest_container
def _epoadTufdhne():
    examples = Package("examples")

    return examples.injected.SubSubContainer


long_two_levels = CodeCollector()
long_middle_container = CodeCollector("middle")
long_lowest_container = CodeCollector("lowest")


@long_two_levels.parametrize
@long_middle_container.parametrize
@long_lowest_container.parametrize
def test_circle_links_two_level_long_loop(code, middle, lowest):
    """Search for dependency loop errors in the complex object graph.

    We can detect link loops in nested injectors two level deep with intermediate links.

    """
    with pytest.raises(DependencyError) as exc_info:
        code(middle(lowest()))

    assert str(exc_info.value) in (
        f"{a!r} is a circle link in the {b!r} injector"
        for a, b in product(
            ["foo", "bar", "baz"], ["Container", "SubContainer", "Injector"]
        )
    )


@long_two_levels
def _eHyErh9kExHG(middle):
    class Container(Injector):
        foo = this.SubContainer.baz
        SubContainer = middle

    Container.foo


@long_two_levels
def _q0KytyVbE2XA(middle):
    Injector(foo=this.SubContainer.baz, SubContainer=middle).foo


@long_middle_container
def _mwcbtGunjMac(lowest):
    class SubContainer(Injector):
        baz = this.SubSubContainer.bar
        SubSubContainer = lowest

    return SubContainer


@long_middle_container
def _aVJRixHNhChV(lowest):
    return Injector(baz=this.SubSubContainer.bar, SubSubContainer=lowest)


@long_lowest_container
def _qRcNcKzedWaI():
    class SubSubContainer(Injector):
        bar = (this << 2).foo

    return SubSubContainer


@long_lowest_container
def _fiktpicgZWNS():
    return Injector(bar=(this << 2).foo)


@long_lowest_container
def _uugFwsWbfgXg():
    examples = Package("examples")

    return examples.injected.SubSubContainer


cross_injector_loops = CodeCollector()
subcontainer1 = CodeCollector("sub1")
subcontainer2 = CodeCollector("sub2")


@cross_injector_loops.parametrize
@subcontainer1.parametrize
@subcontainer2.parametrize
def test_cross_injector_loops(code, sub1, sub2):
    """Search for dependency loop errors in the complex object graph.

    We can detect loops between links in different `Injector` subclasses in the
    hierarchy.

    """
    with pytest.raises(DependencyError) as exc_info:
        code(sub1(), sub2())

    assert str(exc_info.value) in (
        f"{a!r} is a circle link in the {b!r} injector"
        for a, b in product(["foo", "bar", "baz"], ["Container", "Injector"])
    )


@cross_injector_loops
def _vAyZepNGAUjY(sub1, sub2):
    class Container(Injector):
        SubContainer1 = sub1
        SubContainer2 = sub2

    Container.SubContainer1.bar


@cross_injector_loops
def _bLRoCCj9uNOp(sub1, sub2):
    Injector(SubContainer1=sub1, SubContainer2=sub2).SubContainer1.bar


@subcontainer1
def _eiVzvYStvpNL():
    class SubContainer1(Injector):
        bar = (this << 1).SubContainer2.baz

    return SubContainer1


@subcontainer1
def _elifFWSpshiv():
    return Injector(bar=(this << 1).SubContainer2.baz)


@subcontainer1
def _yavnvOrgKYNS():
    examples = Package("examples")

    return examples.injected.SubContainer1


@subcontainer2
def _fFuLltxguVgC():
    class SubContainer2(Injector):
        baz = (this << 1).SubContainer1.bar

    return SubContainer2


@subcontainer2
def _rRsNsCaBSxke():
    return Injector(baz=(this << 1).SubContainer1.bar)


@subcontainer2
def _xVeDBvAxsNYP():
    examples = Package("examples")

    return examples.injected.SubContainer2


items = CodeCollector()


@items.parametrize
def test_item_access_loops(code):
    """We can detect loops created with get item access."""
    with pytest.raises(DependencyError) as exc_info:
        code()

    assert str(exc_info.value) in (
        f"{a!r} is a circle link in the {b!r} injector"
        for a, b in product(["foo"], ["Container", "Injector"])
    )


@items.xfail
def _oClqGRmWJAkA():
    class Container(Injector):
        class SubContainer(Injector):

            foo = (this << 1).bar["sub"].foo

        bar = {"sub": SubContainer}

    Container.SubContainer.foo


@items.xfail
def _t41yMywZuPhA():
    SubContainer = Injector(foo=(this << 1).bar["sub"].foo)
    Injector(SubContainer=SubContainer, bar={"sub": SubContainer}).SubContainer.foo


def test_false_positive_loop_lookup_protection():
    """Protect from false positive loop error detections.

    We should allow proxy to point to objects with the same name if it does not create a
    circle link.

    """

    class Container(Injector):

        foo = this.SubContainer.baz

        class SubContainer(Injector):

            baz = this.foo
            foo = 1

    assert Container.foo == 1
