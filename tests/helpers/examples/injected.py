from dependencies import Injector
from dependencies import this


class Container(Injector):
    """A dummy class for tests."""

    foo = 1
    bar = (this << 1).baz


class SubContainer(Injector):
    """A dummy class for tests."""

    bar = (this << 1).foo


class SubSubContainer(Injector):
    """A dummy class for tests."""

    bar = (this << 2).foo


class SubContainer1(Injector):
    """A dummy class for tests."""

    bar = (this << 1).SubContainer2.baz


class SubContainer2(Injector):
    """A dummy class for tests."""

    baz = (this << 1).SubContainer1.bar
