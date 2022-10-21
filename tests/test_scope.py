"""Tests related to scope object."""
from dependencies import Injector
from dependencies import this


def test_hide_scope_attributes():
    """Check attributes protection.

    Scope object own attributes like graph and cache should not be awailable to the
    library user.

    """

    class Result:
        def __init__(self, graph, cache):
            self.graph = graph
            self.cache = cache

    class Container(Injector):
        result = Result
        graph = this.Nested.graph
        cache = this.Nested.cache

        class Nested(Injector):
            graph = 1
            cache = 2

    assert Container.result.graph == 1
    assert Container.result.cache == 2


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
