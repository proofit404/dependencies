import pytest

from dependencies import Injector, this
from dependencies.exceptions import DependencyError
from helpers import CodeCollector


circle_links = CodeCollector()


@circle_links.parametrize
def test_circle_links(code):
    """
    We can detect loops in the container hierarchy which will trigger
    recursion during injection process.  We need to raise
    `DependencyError` the same way we do with circle dependencies.
    """

    with pytest.raises(DependencyError) as exc_info:
        code()

    assert str(exc_info.value) in set(
        [
            "'foo' is a circle link in the 'Container' injector",
            "'foo' is a circle link in the 'Injector' injector",
            "'bar' is a circle link in the 'Container' injector",
            "'bar' is a circle link in the 'Injector' injector",
            "'baz' is a circle link in the 'Container' injector",
            "'baz' is a circle link in the 'Injector' injector",
        ]
    )


@circle_links
def kSSnnkw6CNPx():
    """Declarative injector.  Same level."""

    class Container(Injector):

        foo = this.foo

    Container.foo


@circle_links
def ai0hNOPGX2PI():
    """Declarative injector.  Same level.  Long loop."""

    class Container(Injector):

        foo = this.bar
        bar = this.baz
        baz = this.foo

    Container.foo


@circle_links
def n8NHZqiZN43Q():
    """Let notation.  Same level."""

    Injector.let(foo=this.foo).foo


@circle_links
def ySnRrxW6M79T():
    """Let notation.  Same level.  Long loop."""

    Injector.let(foo=this.bar, bar=this.baz, baz=this.foo).foo


@circle_links
def eaK6IxW88SNh():
    """Declarative injector.  One level deep."""

    class Container(Injector):

        foo = this.SubContainer.bar

        class SubContainer(Injector):

            bar = (this << 1).foo

    Container.foo


@circle_links
def nWhKtJb16yg6():
    """Let notation.  One level deep."""

    Injector.let(
        foo=this.SubContainer.bar, SubContainer=Injector.let(bar=(this << 1).foo)
    ).foo


@circle_links
def mF4akoHlg84C():
    """Declarative injector.  Two level deep."""

    class Container(Injector):

        foo = this.SubContainer.SubSubContainer.bar

        class SubContainer(Injector):
            class SubSubContainer(Injector):

                bar = (this << 2).foo

    Container.foo


@circle_links
def bCw8LPUeVK6J():
    """Let notation.  Two level deep."""

    Injector.let(
        foo=this.SubContainer.SubSubContainer.bar,
        SubContainer=Injector.let(SubSubContainer=Injector.let(bar=(this << 2).foo)),
    ).foo


@circle_links
def eHyErh9kExHG():
    """Declarative injector.  Two level deep.  Each level has link."""

    class Container(Injector):

        foo = this.SubContainer.bar

        class SubContainer(Injector):

            bar = this.SubSubContainer.baz

            class SubSubContainer(Injector):

                baz = (this << 2).foo

    Container.foo


@circle_links
def q0KytyVbE2XA():
    """Let notation.  Two level deep.  Each level has link."""

    Injector.let(
        foo=this.SubContainer.bar,
        SubContainer=Injector.let(
            bar=this.SubSubContainer.baz,
            SubSubContainer=Injector.let(baz=(this << 2).foo),
        ),
    ).foo


@circle_links
def vAyZepNGAUjY():
    """Declarative injector.  Cross injector links."""

    class Container(Injector):
        class SubContainer1(Injector):

            bar = (this << 1).SubContainer2.baz

        class SubContainer2(Injector):

            baz = (this << 1).SubContainer1.bar

    Container.SubContainer1.bar


@circle_links
def bLRoCCj9uNOp():
    """Let notation.  Cross injector links."""

    Injector.let(
        SubContainer1=Injector.let(bar=(this << 1).SubContainer2.baz),
        SubContainer2=Injector.let(baz=(this << 1).SubContainer1.bar),
    ).SubContainer1.bar


@circle_links.xfail  # FIXME: Make this work.
def oClqGRmWJAkA():
    """Declarative injector.  Over item access."""

    class Container(Injector):
        class SubContainer(Injector):

            foo = (this << 1).bar["sub"].foo

        bar = {"sub": SubContainer}

    Container.SubContainer.foo


@circle_links.xfail  # FIXME: Make this work.
def t41yMywZuPhA():
    """Let notation.  Over item access."""

    SubContainer = Injector.let(foo=(this << 1).bar["sub"].foo)
    Injector.let(SubContainer=SubContainer, bar={"sub": SubContainer}).SubContainer.foo


def test_false_positive_loop_lookup_protection():
    """
    We should allow proxy to point to objects with the same name if it
    does not create a circle link.
    """

    class Container(Injector):

        foo = this.SubContainer.baz

        class SubContainer(Injector):

            baz = this.foo
            foo = 1

    assert Container.foo == 1
