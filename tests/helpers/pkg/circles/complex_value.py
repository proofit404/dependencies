# -*- coding: utf-8 -*-
from dependencies import value


@value
def Foo(bar):
    pass  # pragma: no cover


@value
def Bar(foo):
    pass  # pragma: no cover
