"""Tests related to scope object."""
from dependencies import Injector


def test_sticky_scope(e, expect):
    """Check sticky scope implementation.

    All objects instantiated during sticky scope life-time should be instantiated once.
    That way we would be able to access inner structures of high-level instancies which
    may protect their inner state (which is a good thing).

    """
    expect.skip_if_injector()

    class Container(Injector):
        app = e.Has["db"]
        db = e.Null

    @expect(Container)
    def case(it):
        assert it.app.db is it.db
