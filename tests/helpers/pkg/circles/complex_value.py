from dependencies import value


@value
def Foo(bar):
    """Define value with circle error."""
    pass  # pragma: no cover


@value
def Bar(foo):
    """Define value with circle error."""
    pass  # pragma: no cover
