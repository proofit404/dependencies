# -*- coding: utf-8 -*-
from dependencies import value


@value
def Foo(bar):
    """Define value with circle error."""
    pass  # pragma: no cover


@value
def Bar(baz):
    """Define value with circle error."""
    pass  # pragma: no cover


@value
def Baz(foo):
    """Define value with circle error."""
    pass  # pragma: no cover
