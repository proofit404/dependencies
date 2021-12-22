variable = 1


dict_variable = {"foo": 12}


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
