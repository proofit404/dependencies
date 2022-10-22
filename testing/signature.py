class Signature:
    """Call arguments storage."""

    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)
