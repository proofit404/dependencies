class Foo:
    """Create method descriptor."""

    def __get__(self, instance, owner=None):
        pass  # pragma: no cover


foo_instance = Foo()


@property
def foo_property(self):
    """Create data descriptor."""
    pass  # pragma: no cover
