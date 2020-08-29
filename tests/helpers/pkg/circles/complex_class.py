class Foo:
    """A definition with circle error."""

    def __init__(self, bar):
        pass  # pragma: no cover


class Bar:
    """A definition with circle error."""

    def __init__(self, foo):
        pass  # pragma: no cover
