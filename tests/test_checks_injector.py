"""Tests related to the Injector subclasses checks."""
import pytest

from dependencies import Injector
from dependencies import Package
from dependencies.exceptions import DependencyError
from helpers import CodeCollector


subclasses_only = CodeCollector()


@subclasses_only.parametrize
def test_multiple_inheritance_deny_regular_classes(code):
    """Only `Injector` subclasses are allowed to be used in the inheritance."""

    class Foo:
        pass

    with pytest.raises(DependencyError) as exc_info:
        code(Foo)

    message = str(exc_info.value)
    assert message == "Multiple inheritance is allowed for Injector subclasses only"


@subclasses_only
def _f1583394f1a6(Foo):
    class Bar(Injector, Foo):
        pass


@subclasses_only
def _b51814725d07(Foo):
    Injector & Foo


deny_magic_methods = CodeCollector()


@deny_magic_methods.parametrize
def test_deny_magic_methods_injection(code):
    """`Injector` doesn't accept magic methods."""
    with pytest.raises(DependencyError) as exc_info:
        code()

    assert str(exc_info.value) == "Magic methods are not allowed"


@deny_magic_methods
def _e78bf771747c():
    class Bar(Injector):
        def __eq__(self, other):
            pass  # pragma: no cover


@deny_magic_methods
def _e34b88041f64():
    def eq(self, other):
        pass  # pragma: no cover

    Injector(__eq__=eq)


deny_empty_scope = CodeCollector()


@deny_empty_scope.parametrize
def test_deny_empty_scope_extension(code):
    """`Injector` subclasses can't extend scope with empty subset."""
    with pytest.raises(DependencyError) as exc_info:
        code()

    assert str(exc_info.value) == "Extension scope can not be empty"


@deny_empty_scope
def _fQl3MI95Y1Zi():
    class Container(Injector):
        pass


@deny_empty_scope
def _pdnQASIDVq2V():
    Injector()


@deny_empty_scope
def _aWNEsKRIx12r():
    class Container(Injector):
        x = 1

    class SubContainer(Container):
        pass


@deny_empty_scope
def _myj1ZoubR68j():
    class Container(Injector):
        x = 1

    Container()


deny_descriptors = CodeCollector()
define_descriptors = CodeCollector("foo")


@deny_descriptors.parametrize
@define_descriptors.parametrize
def test_deny_descriptors(code, foo):
    """Descriptors passed to the injector have confusing expectations.

    If users pass method descriptor to the injector, they probably expect access to the
    Injector itself.

    """
    with pytest.raises(DependencyError) as exc_info:
        code(foo())

    expected_a = """
'Container.foo' contains descriptor.

Descriptors usage will be confusing inside Injector subclasses.

Use @value decorator instead, if you really need inject descriptor instance somewhere.
    """.strip()

    expected_b = """
'Injector.foo' contains descriptor.

Descriptors usage will be confusing inside Injector subclasses.

Use @value decorator instead, if you really need inject descriptor instance somewhere.
""".strip()

    expected = {expected_a, expected_b}

    message = str(exc_info.value)

    assert message in expected


@deny_descriptors
def _caOeAAu5NION(Foo):
    class Container(Injector):
        foo = Foo

    Container.foo


@deny_descriptors
def _ebVCjYc6QfKm(Foo):
    Injector(foo=Foo).foo


@define_descriptors
def _r9dddJV0mf2S():
    class Foo:
        def __get__(self, instance, owner=None):
            pass  # pragma: no cover

    return Foo()


@define_descriptors
def _rKUlUpA2fLI9():
    @property
    def foo(self):
        pass  # pragma: no cover

    return foo


@define_descriptors
def _qN0K5wmjSA81():
    examples = Package("examples")
    return examples.descriptor.foo_instance


@define_descriptors
def _toU8DccacvIc():
    examples = Package("examples")
    return examples.descriptor.foo_property
