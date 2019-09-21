from dependencies import operation


@operation
def Foo(bar):
    pass  # pragma: no cover


@operation
def Bar(baz):
    pass  # pragma: no cover


@operation
def Baz(foo):
    pass  # pragma: no cover
