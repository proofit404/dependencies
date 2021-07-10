variable = 1


def function():
    """Return dummy data."""
    return 1


class Foo:
    """A dummy class for tests."""

    def do(self):
        """Return dummy data."""
        return 1


class Bar:
    """A dummy class for tests."""

    def __init__(self, a, b):
        self.a = a
        self.b = b

    def do(self):
        """Return dummy data."""
        return self.a + self.b
