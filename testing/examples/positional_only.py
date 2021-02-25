from dependencies import value


class Foo:
    """A dummy class for tests."""

    def __init__(self, a, /, b):
        raise RuntimeError


@value
def foo(a, /, b):
    """Return dummy value for tests."""
    raise RuntimeError
