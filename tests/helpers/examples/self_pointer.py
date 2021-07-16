from dependencies import Injector
from dependencies import Package


current = Package("examples.self_pointer")


class Foo:
    """A dummy class."""

    bar = "baz"


class Container(Injector):
    """A dummy container."""

    foo = current.Box.foo


class Box(Injector):
    """A dummy nested container."""

    foo = Foo
