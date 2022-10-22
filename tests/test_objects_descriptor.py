"""Tests related to descriptor objects."""
import pytest

from dependencies import Injector


def _descriptors():
    class Foo:
        def __get__(self, instance, owner=None):
            raise RuntimeError

    @property
    def foo(self):
        raise RuntimeError

    yield Foo()
    yield foo


@pytest.mark.parametrize("arg", _descriptors())
def test_deny_descriptors(expect, catch, arg):
    """Descriptors passed to the injector have confusing expectations.

    If users pass method descriptor to the injector, they probably expect access to the
    Injector itself.

    """

    class Container(Injector):
        foo = arg

    @expect(Container)
    @catch(
        """
Attribute 'foo' contains descriptor.

Descriptors usage will be confusing inside Injector subclasses.

Use @value decorator instead, if you really need inject descriptor instance somewhere.
        """
    )
    def case(it):
        it.bar
