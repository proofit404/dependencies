from dependencies import Injector, this


class Container(Injector):

    foo = 1
    bar = (this << 1).baz
