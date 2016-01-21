from dependencies import Injectable, Injector


def test_constructor_based_di():
    """Classed inherited from `Injectable` allows constructor-based DI."""

    class Foo(Injectable):
        def apply(self, command):
            return self.modifier(command)

    foo = Foo(modifier=lambda x: x.upper())
    assert foo.apply('ls') == 'LS'
