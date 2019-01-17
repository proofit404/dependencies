from dependencies import Injector, Package


current = Package("pkg.self_pointer")


class Container(Injector):

    foo = current.Box.foo


class Box(Injector):

    foo = 1
