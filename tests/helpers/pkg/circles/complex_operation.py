# -*- coding: utf-8 -*-
from dependencies import operation


@operation
def Foo(bar):
    pass  # pragma: no cover


@operation
def Bar(foo):
    pass  # pragma: no cover
