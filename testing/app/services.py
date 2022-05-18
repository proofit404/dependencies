class Root:
    """Service."""

    def __init__(self, nested_a, nested_b, nested_c):
        self.nested_a = nested_a
        self.nested_b = nested_b
        self.nested_c = nested_c

    def __repr__(self):
        return (
            f"{self.__class__.__name__}({self.nested_a!r}, "
            f"{self.nested_b!r}, {self.nested_c!r})"
        )

    def do(self):
        """Do stuff."""
        self.nested_a.ok()


class NestedA:
    """Service."""

    def __init__(self):
        self.success = False

    def __repr__(self):
        return f"{self.__class__.__name__}()"

    def ok(self):
        """Do stuff."""
        self.success = True


class NestedB:
    """Service."""

    def __repr__(self):
        return f"{self.__class__.__name__}()"


class NestedC:
    """Service."""

    def __repr__(self):
        return f"{self.__class__.__name__}()"
