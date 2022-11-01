"""Tests related to scope object."""
from dependencies import Injector


def test_sticky_scope():
    """Check sticky scope implementation.

    All objects instantiated during sticky scope life-time should be instantiated once.
    That way we would be able to access inner structures of high-level instancies which
    may protect their inner state (which is a good thing).

    """

    class App:
        def __init__(self, db):
            self.db = db

    class DB:
        pass

    class Container(Injector):
        app = App
        db = DB

    with Container as container:
        app = container.app
        db = container.db

    assert app.db is db
