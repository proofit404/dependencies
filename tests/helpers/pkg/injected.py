from dependencies import Injector, this


class Container(Injector):

    foo = 1
    bar = (this << 1).baz


class SubContainer(Injector):

    bar = (this << 1).foo


class SubSubContainer(Injector):

    bar = (this << 2).foo
