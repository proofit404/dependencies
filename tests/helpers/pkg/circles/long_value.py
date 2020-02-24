# -*- coding: utf-8 -*-
from dependencies import value


@value
def Foo(bar):
    pass  # pragma: no cover


@value
def Bar(baz):
    pass  # pragma: no cover


@value
def Baz(foo):
    pass  # pragma: no cover
