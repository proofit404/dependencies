# -*- coding: utf-8 -*-
class Foo(object):
    """A definition with circle error."""

    def __init__(self, bar):
        pass  # pragma: no cover


class Bar(object):
    """A definition with circle error."""

    def __init__(self, foo):
        pass  # pragma: no cover
