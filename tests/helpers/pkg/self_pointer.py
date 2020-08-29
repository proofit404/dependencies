from dependencies import Injector
from dependencies import Package


current = Package("pkg.self_pointer")


class Container(Injector):
    """A dummy class for tests."""

    foo = current.Box.foo


class Box(Injector):
    """A dummy class for tests."""

    foo = 1
