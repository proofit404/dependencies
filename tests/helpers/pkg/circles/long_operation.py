# -*- coding: utf-8 -*-
from dependencies import operation


@operation
def Foo(bar):
    """Define operation with circle error."""
    pass  # pragma: no cover


@operation
def Bar(baz):
    """Define operation with circle error."""
    pass  # pragma: no cover


@operation
def Baz(foo):
    """Define operation with circle error."""
    pass  # pragma: no cover
