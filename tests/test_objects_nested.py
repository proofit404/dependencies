"""Tests related to Injector classes written inside other Injector classes."""
from dependencies import Injector


def test_deny_nested_injectors(e, expect, catch):
    """Injectors can not store other Injector in it."""

    class Bar(Injector):
        foo = e.Null

    class Baz(Injector):
        bar = Bar

    @expect(Baz)
    @catch(
        """
Attribute 'bar' contains nested Injector.

Do not depend on nested injectors directly.

Use reference objects to access inner attributes of other injectors instead.
        """
    )
    def case(it):
        it.quiz
