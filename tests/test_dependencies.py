import pytest

from dependencies import Injectable, Injector, DependencyError


def test_constructor_based_di():
    """Classed inherited from `Injectable` allows constructor-based DI."""

    class Foo(Injectable):
        def apply(self, command):
            return self.modifier(command)

    foo = Foo(modifier=lambda x: x.upper())
    assert foo.apply('ls') == 'LS'


def test_missing_dependency():
    """`Injectable` adherent throw `AttributeError` if some dependencies
    are missed.

    """

    class Foo(Injectable):
        def apply(self):
            self.missed

    with pytest.raises(AttributeError):
        Foo().apply()


def test_injectable_deny_multiple_inheritance():
    """`Injectable` deny multiple inheritance."""

    class Foo(object):
        message = 'test'

    with pytest.raises(DependencyError):
        class Bar(Injectable, Foo):
            pass


def test_deny_protocol_modification():
    """Classes inherited from `Injectable` can't modify suggested protocol.

    They unable to redefine `__init__`, `__getattr__` and
    `__getattribute__` magic methods.

    """

    with pytest.raises(DependencyError):
        class Foo(Injectable):
            def __init__(self):
                pass

    with pytest.raises(DependencyError):
        class Baz(Injectable):
            def __getattr__(self):
                pass

    with pytest.raises(DependencyError):
        class Bar(Injectable):
            def __getattribute__(self):
                pass


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


def test_inherit_from_injectable_subclass():
    """We can inherit from injectable subclass."""

    class Foo(Injectable):
        def apply(self, x):
            return self.go(x)

    class Bar(Foo):
        def apply(self):
            return super(Bar, self).apply(1)

    class Baz(Foo):
        def go(self, x):
            return 2

    assert Bar(go=lambda x: x).apply() == 1
    assert Baz().apply(1) == 2


def test_protect_protocol_inherit_from_injectable_subclass():
    """We can't redefine magic methods on inheritance from `Injectable`
    subclass.

    """

    class Foo(Injectable):
        pass

    with pytest.raises(DependencyError):
        class Bar(Foo):
            def __init__(self):
                pass


def test_initialize_subclasses_ones():
    """Apply protocol injection ones.

    Protocol methods injected in the first subclass only.  Next
    subclasses shouldn't be affected.

    """

    class Foo(Injectable):
        pass

    class Baz(Foo):
        pass

    assert '__init__' in Foo.__dict__
    assert '__getattr__' in Foo.__dict__

    assert '__init__' not in Baz.__dict__
    assert '__getattr__' not in Baz.__dict__

    class Bar(Injector, Baz):
        pass

    class Xyz(Bar):
        pass

    assert '__init__' in Bar.__dict__
    assert '__init__' not in Xyz.__dict__


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


def test_inline_dependency_definition():
    """Dependencies defined inside Injector should not be method wrapped."""

    def default_go(x):
        return 'Go, {x}! Go!'.format(x=x)

    class Foo(Injectable):
        def do(self, x):
            return self.go(x)

    class Bar(Injector, Foo):
        go = default_go

    class Baz(Injector, Foo):
        def go(x):  # Preserve `default_go` signature.
            return 'Run, {x}! Run!'.format(x=x)

    assert Bar().do('user') == 'Go, user! Go!'
    assert Baz().do('user') == 'Run, user! Run!'


def test_injector_allow_multiple_inheritance_only():
    """`Injector` may be used in multiple inheritance only."""

    with pytest.raises(DependencyError):
        class Foo(Injector):
            pass


def test_injector_allow_injectalble_only():
    """`Injector` allows `Injectable` in the inheritance chain only."""

    class Foo(object):
        pass

    class Bar(Injectable):
        pass

    with pytest.raises(DependencyError):
        class Baz(Injector, Bar, Foo):
            pass


def test_injector_any_order():
    """`Injector` may be used in any position."""

    class Foo(Injectable):
        def apply(self, x):
            return self.do(x)

    class Bar(Foo, Injector):
        do = lambda x: x + 1

    assert Bar().apply(1) == 2


def test_magic_methods_not_allowed_in_the_injector():
    """`Injector` doesn't accept magic methods."""

    class Foo(Injectable):
        pass

    with pytest.raises(DependencyError):
        class Bar(Injector, Foo):
            def __eq__(self, other):
                pass


def test_keep_default_dict_for_injector_subclass():
    """`__dict__` of `Injector` subclass should contain default members
    like `__module__`.

    """

    class Foo(Injectable):
        pass

    class Bar(Injector, Foo):
        pass

    bar = Bar()
    assert '__module__' in Bar.__dict__
    assert '__module__' not in bar.dependencies


def test_multiple_inheritance_with_injector():
    """Multiple inheritance is allowed to use with `Injector`."""

    class Foo(Injectable):
        @property
        def x(self):
            return self.a

    class Bar(Injectable):
        @property
        def y(self):
            return self.b

    class Baz(Injectable):
        def add(self):
            return self.x + self.y

    class Summator(Injector, Foo, Bar, Baz):
        a = 1
        b = 2

    assert 3 == Summator().add()


def test_object_inheritance_restrictions():
    """Follows `object` inheritance principles.

    Deny to use same class in the bases twice.

    """

    class Foo(Injectable):
        pass

    with pytest.raises(TypeError):
        class Bar(Injector, Foo, Foo):
            pass

    with pytest.raises(TypeError):
        class Baz(Injector, Foo, Injector):
            pass
