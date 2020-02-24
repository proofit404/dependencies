# -*- coding: utf-8 -*-
class Foo(object):
    def __init__(self, bar):
        pass  # pragma: no cover


class Bar(object):
    def __init__(self, foo):
        pass  # pragma: no cover
