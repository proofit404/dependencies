"""Tests related to descriptor checks."""
import pytest

from dependencies import Injector
from dependencies import Package
from dependencies.exceptions import DependencyError
from helpers import CodeCollector


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

    expected = """
Attribute 'foo' contains descriptor.

Descriptors usage will be confusing inside Injector subclasses.

Use @value decorator instead, if you really need inject descriptor instance somewhere.
""".strip()

    assert str(exc_info.value) == expected


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
