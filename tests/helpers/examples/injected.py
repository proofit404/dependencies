from dependencies import Injector
from dependencies import this


class Container(Injector):
    """A dummy class for tests."""

    foo = 1
    bar = (this << 1).baz
