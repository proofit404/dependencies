import pytest

from dependencies import Injector, DependencyError


def test_magic_methods_does_not_injected_into_api_classes():
    """`Injector` isn't affected by it metaclass.

    `__init__` and `__getattr__` should be injected in this classes.

    """

    assert '__init__' not in Injector.__dict__
    assert '__getattr__' not in Injector.__dict__


def test_injector_specify_default_dependencies():
    """Inherit from `Injector` class will specify default dependencies."""

    class Foo(object):
        def __init__(self, add):
            self.add = add
        def do(self, x):
            return self.add(x, x)

    class Summator(Injector, Foo):
        add = lambda x, y: x + y

    assert Summator().do(1) == 2


def test_initialize_subclasses_ones():
    """Apply protocol injection ones.

    Injector protocol methods injected into each subclass.  This
    allows to override specified dependencies in the inheritance
    downstream.

    """

    class Foo(object):
        pass

    class Baz(Foo):
        pass

    class Bar(Injector, Baz):
        pass

    class Xyz(Bar):
        pass

    assert '__init__' in Bar.__dict__
    assert '__init__' in Xyz.__dict__


def test_injector_does_not_store_literaly_defined_dependencies():
    """If someone define dependency literaly (i.e. write it directly
    inside Injector) we will store it in the metaclass.__new__ closure
    and not in the derived class __dict__.
    """

    class Foo(object):
        def __init__(self, add):
            self.add = add
        def do(self, x):
            return self.add(x, x)

    class Summator(Injector, Foo):
        add = lambda x, y: x + y

    assert 'add' not in Summator.__dict__


def test_inline_dependency_definition():
    """Dependencies defined inside Injector should not be method wrapped."""

    def default_go(x):
        return 'Go, {x}! Go!'.format(x=x)

    class Foo(object):
        def __init__(self, go):
            self.go = go
        def do(self, x):
            return self.go(x)

    class Bar(Injector, Foo):
        go = default_go

    class Baz(Injector, Foo):
        def go(x):
            return 'Run, {x}! Run!'.format(x=x)

    assert Bar().do('user') == 'Go, user! Go!'
    assert Baz().do('user') == 'Run, user! Run!'


def test_injector_allow_multiple_inheritance_only():
    """`Injector` may be used in multiple inheritance only."""

    with pytest.raises(DependencyError):
        class Foo(Injector):
            pass


def test_injector_any_order():
    """`Injector` may be used in any position."""

    class Foo(object):
        def __init__(self, do):
            self.do = do
        def apply(self, x):
            return self.do(x)

    class Bar(Foo, Injector):
        do = lambda x: x + 1

    assert Bar().apply(1) == 2


def test_magic_methods_not_allowed_in_the_injector():
    """`Injector` doesn't accept magic methods."""

    class Foo(object):
        pass

    with pytest.raises(DependencyError):
        class Bar(Injector, Foo):
            def __eq__(self, other):
                pass


def test_keep_default_dict_for_injector_subclass():
    """`__dict__` of `Injector` subclass should contain default members
    like `__module__`.

    """

    class Foo(object):
        pass

    class Bar(Injector, Foo):
        pass

    bar = Bar()
    assert '__module__' in Bar.__dict__
    assert '__module__' not in bar.__dict__


def test_multiple_inheritance_with_injector():
    """Multiple inheritance is allowed to use with `Injector`."""

    class Foo(object):
        def __init__(self, a):
            self.a = a
        @property
        def x(self):
            return self.a

    class Bar(object):
        def __init__(self, b):
            self.b = b
        @property
        def y(self):
            return self.b

    class Baz(object):
        def __init__(self, x, y):
            self.x = x
            self.y = y
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

    class Foo(object):
        pass

    with pytest.raises(TypeError):
        class Bar(Injector, Foo, Foo):
            pass

    with pytest.raises(TypeError):
        class Baz(Injector, Foo, Injector):
            pass


def test_redefine_injector_defaults_with_inheritance():
    """We can send dependencies into injector not only with kwargs but
    with inheritance too.

    """

    class Foo(object):
        def __init__(self, x):
            self.x = x
        def do(self):
            return self.x()

    class Bar(Injector, Foo):
        def x():
            return 1

    class Baz(Bar):
        def x():
            return 2

    assert Baz().do() == 2
    assert Baz(x=lambda: 3).do() == 3
