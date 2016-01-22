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
    """Classes inherited from `Injectable` can't modify suggested protocol.

    They unable to redefine `__init__`, `__getattr__` and
    `__getattribute__` magic methods.

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


def test_magic_methods_does_not_injected_into_api_classes():
    """`Injectable` and `Injector` doesn't affected by their metaclasses.

    `__init__` and `__getattr__` should be injected in this classes.

    """

    assert '__init__' not in Injectable.__dict__
    assert '__init__' not in Injector.__dict__

    assert '__getattr__' not in Injectable.__dict__
    assert '__getattr__' not in Injector.__dict__


def test_injector_specify_default_dependencies():
    """Inherit from `Injector` class will specify default dependencies."""

    class Foo(Injectable):
        def do(self, x):
            return self.add(x, x)

    class Summator(Injector, Foo):
        add = lambda x, y: x + y

    assert Summator().do(1) == 2


def test_injector_does_not_store_literaly_defined_dependencies():
    """If someone define dependency literaly (i.e. write it directly
    inside Injector) we will store it in the metaclass.__new__ closure
    and not in the derived class __dict__.
    """

    class Foo(Injectable):
        def do(self, x):
            return self.add(x, x)

    class Summator(Injector, Foo):
        add = lambda x, y: x + y

    assert 'add' not in Summator.__dict__
