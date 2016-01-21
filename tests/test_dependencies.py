import pytest

from dependencies import Injectable, Injector, DependencyError


def test_constructor_based_di():
    """Classed inherited from `Injectable` allows constructor-based DI."""

    class Foo(Injectable):
        def apply(self, command):
            return self.modifier(command)

    foo = Foo(modifier=lambda x: x.upper())
    assert foo.apply('ls') == 'LS'


def test_deny_protocol_modification():
    """Classes inherited from `Injectable` can't redefine `__init__`,
    `__getattr__` and `__getattribute__`  magic methods.
    """

    with pytest.raises(DependencyError) as error:
        class Foo(Injectable):
            def __init__(self):
                pass

    message = error.value.args[0]
    assert message == (
        'Classes inherited from Injectable '
        'can not redefine __init__ method')

    with pytest.raises(DependencyError) as error:
        class Baz(Injectable):
            def __getattr__(self):
                pass

    message = error.value.args[0]
    assert message == (
        'Classes inherited from Injectable '
        'can not redefine __getattr__ method')

    with pytest.raises(DependencyError) as error:
        class Bar(Injectable):
            def __getattribute__(self):
                pass

    message = error.value.args[0]
    assert message == (
        'Classes inherited from Injectable '
        'can not redefine __getattribute__ method')
