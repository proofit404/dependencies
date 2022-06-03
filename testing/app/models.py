class Manager:
    """Database access layer."""

    def select(self):
        """Send query."""
        return [Report(1), Report(2), Report(3)]


class Report:
    """Domain model."""

    objects = Manager()

    def __init__(self, key):
        self.key = key

    def __repr__(self):
        return f"<{self.__class__.__name__}: {self.key}>"
