"""Tests related to compatibility with standard doctest python module."""
from dependencies import Injector


class Foo:
    """A useful class."""

    def __repr__(self):
        return "foo instance"


class Container(Injector):
    """The code written in this docstring will be executed by pytest.

    >>> Container.foo
    foo instance

    """

    foo = Foo
