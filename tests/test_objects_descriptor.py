"""Tests related to descriptor objects."""
import pytest

from dependencies import Injector
from dependencies import Package
from dependencies.exceptions import DependencyError


def test_deny_descriptors(d):
    """Descriptors passed to the injector have confusing expectations.

    If users pass method descriptor to the injector, they probably expect access to the
    Injector itself.

    """

    class Container(Injector):
        foo = d

    with pytest.raises(DependencyError) as exc_info:
        Container.foo

    expected = """
Attribute 'foo' contains descriptor.

Descriptors usage will be confusing inside Injector subclasses.

Use @value decorator instead, if you really need inject descriptor instance somewhere.
""".strip()

    assert str(exc_info.value) == expected


def _descriptors():
    class Foo:
        def __get__(self, instance, owner=None):
            raise RuntimeError

    @property
    def foo(self):
        raise RuntimeError

    examples = Package("examples")

    yield Foo()
    yield foo
    yield examples.descriptor.foo_instance
    yield examples.descriptor.foo_property


@pytest.fixture(params=_descriptors())
def d(request):
    """All possible descriptor definitions."""
    return request.param
