# FIXME: This should be a single letter pytest parametrized fixture
# suitable for testing classes and @value signatures. Basically, all
# parametrized tests with function call should be rewritten to use
# this fixture.


class Signature:
    """Call arguments storage."""

    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)
