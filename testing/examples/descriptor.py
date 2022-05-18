class Foo:
    """Create method descriptor."""

    def __get__(self, instance, owner=None):
        raise RuntimeError


foo_instance = Foo()


@property
def foo_property(self):
    """Create data descriptor."""
    raise RuntimeError
